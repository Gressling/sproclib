"""
Peristaltic Flow class for SPROCLIB - Standard Process Control Library

This module contains the peristaltic pump flow transport model (steady-state and dynamic).
"""

import numpy as np
try:
    from .....unit.base import ProcessModel
except ImportError:
    # Use mock for testing
    from ProcessModel_mock import ProcessModel


class PeristalticFlow(ProcessModel):
    """Peristaltic pump flow transport model (steady-state and dynamic)."""
    
    def __init__(
        self,
        tube_diameter: float = 0.01,    # Tube inner diameter [m]
        tube_length: float = 1.0,       # Tube length [m]
        pump_speed: float = 100.0,      # Pump speed [rpm]
        occlusion_factor: float = 0.9,  # Tube occlusion factor [-]
        fluid_density: float = 1000.0,  # Fluid density [kg/m³]
        fluid_viscosity: float = 1e-3,  # Fluid viscosity [Pa·s]
        pulsation_damping: float = 0.8, # Pulsation damping factor [-]
        name: str = "PeristalticFlow"
    ):
        super().__init__(name)
        self.tube_diameter = tube_diameter
        self.tube_length = tube_length
        self.pump_speed = pump_speed
        self.occlusion_factor = occlusion_factor
        self.fluid_density = fluid_density
        self.fluid_viscosity = fluid_viscosity
        self.pulsation_damping = pulsation_damping
        self.parameters = {
            'tube_diameter': tube_diameter, 'tube_length': tube_length, 'pump_speed': pump_speed,
            'occlusion_factor': occlusion_factor, 'fluid_density': fluid_density,
            'fluid_viscosity': fluid_viscosity, 'pulsation_damping': pulsation_damping
        }

    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Comprehensive metadata about the PeristalticFlow model including
                  algorithms, parameters, equations, and usage information.
        """
        return {
            'class_name': 'PeristalticFlow',
            'module': 'transport.continuous.liquid.PeristalticFlow',
            'description': 'Peristaltic pump flow transport model for precise fluid metering',
            'model_type': 'Positive Displacement Pump Model',
            'physics': {
                'domain': 'Fluid Mechanics & Mechanical Engineering',
                'phenomena': ['Positive displacement', 'Pulsatile flow', 'Tube compression'],
                'assumptions': ['Incompressible fluid', 'Perfect tube occlusion', 'Negligible tube elasticity']
            },
            'algorithms': {
                'theoretical_flow': 'Q_th = (N/60) * A_tube * occlusion_factor',
                'backpressure_correction': 'pressure_factor = max(0.1, 1.0 - P_in/1e6)',
                'actual_flow': 'Q_actual = Q_th * pressure_factor',
                'dynamics': 'First-order response with pulsation modeling'
            },
            'parameters': self.parameters,
            'inputs': {
                'steady_state': ['P_inlet [Pa]', 'pump_speed_setpoint [rpm]', 'occlusion_level [-]'],
                'dynamics': ['P_inlet [Pa]', 'pump_speed_setpoint [rpm]', 'occlusion_level [-]']
            },
            'outputs': {
                'steady_state': ['flow_rate [m³/s]', 'P_outlet [Pa]'],
                'dynamics': ['dflow_rate/dt [m³/s²]', 'dpulsation/dt [1/s]']
            },
            'state_variables': ['flow_rate [m³/s]', 'pulsation_amplitude [-]'],
            'methods': ['steady_state', 'dynamics', 'describe'],
            'performance_characteristics': {
                'flow_accuracy': 'Typically ±1-3%',
                'pressure_capability': 'Up to 1 MPa',
                'turndown_ratio': '1000:1'
            },
            'typical_applications': ['Analytical instruments', 'Medical devices', 'Chemical dosing'],
            'advantages': ['No valves', 'Self-priming', 'Precise metering'],
            'limitations': ['Pulsatile flow', 'Tube wear', 'Limited pressure capability']
        }

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state flow rate and pressure for given pump conditions.
        Args:
            u: [P_inlet, pump_speed_setpoint, occlusion_level]
        Returns:
            [flow_rate, P_outlet]
        """
        P_in, pump_speed, occlusion = u
        
        # Theoretical volumetric flow rate
        tube_cross_area = np.pi * (self.tube_diameter/2)**2
        theoretical_flow = (pump_speed / 60.0) * tube_cross_area * self.occlusion_factor * occlusion
        
        # Account for backpressure effects (simplified)
        pressure_factor = max(0.1, 1.0 - P_in / 1e6)  # Reduce flow at high backpressure
        actual_flow = theoretical_flow * pressure_factor
        
        # Outlet pressure (minimal pressure drop in peristaltic pumps)
        P_out = P_in + self.fluid_density * 9.81 * 0.1  # Small pressure increase
        
        return np.array([actual_flow, P_out])

    @staticmethod
    def describe_steady_state() -> dict:
        """
        Describe the steady_state function algorithm and metadata.
        
        Returns:
            dict: Algorithm details, equations, and computational steps
        """
        return {
            'function_name': 'steady_state',
            'purpose': 'Calculate steady-state flow rate and pressure for peristaltic pump',
            'algorithm_steps': [
                '1. Calculate tube cross-sectional area',
                '2. Compute theoretical flow rate based on pump speed',
                '3. Apply occlusion factor correction',
                '4. Account for backpressure effects',
                '5. Calculate outlet pressure with minimal pressure drop'
            ],
            'equations': {
                'tube_area': 'A = π * (D/2)²',
                'theoretical_flow': 'Q_th = (N/60) * A * occlusion_factor * occlusion_level',
                'pressure_factor': 'f_p = max(0.1, 1.0 - P_in/1e6)',
                'actual_flow': 'Q_actual = Q_th * f_p',
                'outlet_pressure': 'P_out = P_in + ρ * g * 0.1'
            },
            'input_format': '[P_inlet, pump_speed_setpoint, occlusion_level]',
            'output_format': '[flow_rate, P_outlet]',
            'computational_complexity': 'O(1)',
            'performance_factors': {
                'occlusion_effect': 'Directly proportional to flow rate',
                'backpressure_effect': 'Reduces flow at high inlet pressures',
                'speed_relationship': 'Linear relationship with pump speed'
            },
            'assumptions': ['Perfect tube sealing', 'Negligible slip', 'Constant occlusion efficiency']
        }

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Dynamic model: flow rate response with pulsation effects.
        State: [flow_rate, pulsation_amplitude]
        Input: [P_inlet, pump_speed_setpoint, occlusion_level]
        """
        flow_rate, pulsation = x
        flow_ss, _ = self.steady_state(u)
        pump_speed = u[1]
        
        # Flow rate dynamics
        tau_flow = 2.0  # s, flow response time constant
        dflow_dt = (flow_ss - flow_rate) / tau_flow
        
        # Pulsation dynamics (frequency related to pump speed)
        pulsation_frequency = pump_speed / 60.0  # Hz
        tau_pulsation = 0.5  # s, pulsation damping time constant
        pulsation_target = (1.0 - self.pulsation_damping) * flow_ss * 0.1
        dpulsation_dt = (pulsation_target - pulsation) / tau_pulsation
        
        return np.array([dflow_dt, dpulsation_dt])

    @staticmethod
    def describe_dynamics() -> dict:
        """
        Describe the dynamics function algorithm and metadata.
        
        Returns:
            dict: Algorithm details, differential equations, and pulsation modeling
        """
        return {
            'function_name': 'dynamics',
            'purpose': 'Model dynamic flow response with pulsation effects',
            'model_type': 'Coupled first-order system with pulsation',
            'algorithm_steps': [
                '1. Extract current state [flow_rate, pulsation_amplitude]',
                '2. Calculate steady-state flow target',
                '3. Model flow rate dynamics with first-order lag',
                '4. Model pulsation amplitude dynamics',
                '5. Return state derivatives'
            ],
            'differential_equations': {
                'flow_rate': 'dflow/dt = (flow_ss - flow) / τ_flow',
                'pulsation': 'dpulsation/dt = (pulsation_target - pulsation) / τ_pulsation'
            },
            'time_constants': {
                'flow_response': 'τ_flow = 2.0 s',
                'pulsation_damping': 'τ_pulsation = 0.5 s'
            },
            'pulsation_model': {
                'frequency': 'f_pulsation = pump_speed / 60 [Hz]',
                'amplitude_target': 'pulsation_target = (1 - damping_factor) * flow_ss * 0.1',
                'damping_effect': 'Controlled by pulsation_damping parameter'
            },
            'state_variables': ['flow_rate [m³/s]', 'pulsation_amplitude [-]'],
            'input_format': 't, [flow_rate, pulsation], [P_inlet, pump_speed, occlusion]',
            'output_format': '[dflow/dt, dpulsation/dt]',
            'stability': 'Stable for positive time constants',
            'physical_interpretation': {
                'flow_lag': 'Pump inertia and tube compliance',
                'pulsation': 'Inherent pump characteristic with damping'
            }
        }
