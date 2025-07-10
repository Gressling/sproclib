"""
Pipe Flow class for SPROCLIB - Standard Process Control Library

This module contains the liquid pipe flow transport model (steady-state and dynamic).
"""

import numpy as np
try:
    from ....unit.base import ProcessModel
except ImportError:
    # Use mock for testing
    from ProcessModel_mock import ProcessModel


class PipeFlow(ProcessModel):
    """Liquid pipe flow transport model (steady-state and dynamic)."""
    
    def __init__(
        self,
        pipe_length: float = 100.0,     # Pipe length [m]
        pipe_diameter: float = 0.1,     # Pipe diameter [m]
        roughness: float = 0.046e-3,    # Pipe roughness [m]
        fluid_density: float = 1000.0,  # Fluid density [kg/m³]
        fluid_viscosity: float = 1e-3,  # Fluid viscosity [Pa·s]
        elevation_change: float = 0.0,  # Elevation change [m]
        flow_nominal: float = 0.01,     # Nominal volumetric flow [m³/s]
        name: str = "PipeFlow"
    ):
        super().__init__(name)
        self.pipe_length = pipe_length
        self.pipe_diameter = pipe_diameter
        self.roughness = roughness
        self.fluid_density = fluid_density
        self.fluid_viscosity = fluid_viscosity
        self.elevation_change = elevation_change
        self.flow_nominal = flow_nominal
        self.parameters = {
            'pipe_length': pipe_length, 'pipe_diameter': pipe_diameter, 'roughness': roughness,
            'fluid_density': fluid_density, 'fluid_viscosity': fluid_viscosity, 
            'elevation_change': elevation_change, 'flow_nominal': flow_nominal
        }

    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Comprehensive metadata about the PipeFlow model including
                  algorithms, parameters, equations, and usage information.
        """
        return {
            'class_name': 'PipeFlow',
            'module': 'transport.continuous.liquid.PipeFlow',
            'description': 'Liquid pipe flow transport model for steady-state and dynamic simulation',
            'model_type': 'Transport Process Model',
            'physics': {
                'domain': 'Fluid Mechanics',
                'phenomena': ['Pressure Drop', 'Friction Loss', 'Elevation Effects'],
                'assumptions': ['Incompressible flow', 'Circular pipe', 'Steady or quasi-steady']
            },
            'algorithms': {
                'reynolds_calculation': 'Re = ρ*v*D/μ',
                'friction_factor': {
                    'laminar': 'f = 64/Re (Re < 2300)',
                    'turbulent': 'Colebrook-White approximation: f = 0.25/[log10(ε/(3.7*D) + 5.74/Re^0.9)]^2'
                },
                'pressure_drop': 'ΔP = f*(L/D)*(ρ*v²/2) + ρ*g*Δh',
                'dynamics': 'First-order lag with time constants τ_pressure=5s, τ_temperature=10s'
            },
            'parameters': self.parameters,
            'inputs': {
                'steady_state': ['P_inlet [Pa]', 'T_inlet [K]', 'flow_rate [m³/s]'],
                'dynamics': ['P_inlet [Pa]', 'T_inlet [K]', 'flow_rate [m³/s]']
            },
            'outputs': {
                'steady_state': ['P_outlet [Pa]', 'T_outlet [K]'],
                'dynamics': ['dP_out/dt [Pa/s]', 'dT_out/dt [K/s]']
            },
            'state_variables': ['P_out [Pa]', 'T_out [K]'],
            'methods': ['steady_state', 'dynamics', 'describe'],
            'references': ['Darcy-Weisbach equation', 'Colebrook-White correlation'],
            'limitations': ['Isothermal assumption for temperature', 'Single-phase liquid only'],
            'typical_applications': ['Water distribution', 'Chemical plant piping', 'Process fluid transport']
        }

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state pressure drop and outlet conditions for given flow.
        Args:
            u: [P_inlet, T_inlet, flow_rate]
        Returns:
            [P_outlet, T_outlet]
        """
        # Add describe capability to function
        if hasattr(self, '_describe_steady_state'):
            return self._describe_steady_state()
            
        P_in, T_in, flow_rate = u
        
        # Handle zero flow case
        if abs(flow_rate) < 1e-12:
            # With zero flow, only elevation pressure drop applies
            pressure_drop_elevation = self.fluid_density * 9.81 * self.elevation_change
            total_pressure_drop = pressure_drop_elevation
        else:
            # Calculate Reynolds number
            velocity = flow_rate / (np.pi * (self.pipe_diameter/2)**2)
            Re = self.fluid_density * velocity * self.pipe_diameter / self.fluid_viscosity
            
            # Calculate friction factor (Darcy-Weisbach)
            if Re < 2300:  # Laminar flow
                f = 64 / Re
            else:  # Turbulent flow (Colebrook-White approximation)
                f = 0.25 / (np.log10(self.roughness/(3.7*self.pipe_diameter) + 5.74/Re**0.9))**2
            
            # Pressure drop calculation
            pressure_drop_friction = f * (self.pipe_length/self.pipe_diameter) * (self.fluid_density * velocity**2 / 2)
            pressure_drop_elevation = self.fluid_density * 9.81 * self.elevation_change
            total_pressure_drop = pressure_drop_friction + pressure_drop_elevation
        
        P_out = P_in - total_pressure_drop
        T_out = T_in  # Assuming isothermal flow for simplicity
        
        return np.array([P_out, T_out])

    @staticmethod
    def describe_steady_state() -> dict:
        """
        Describe the steady_state function algorithm and metadata.
        
        Returns:
            dict: Algorithm details, equations, and computational steps
        """
        return {
            'function_name': 'steady_state',
            'purpose': 'Calculate steady-state pressure drop and outlet conditions',
            'algorithm_steps': [
                '1. Calculate flow velocity: v = Q / (π * (D/2)²)',
                '2. Calculate Reynolds number: Re = ρ * v * D / μ',
                '3. Determine friction factor based on flow regime',
                '4. Calculate pressure drops (friction + elevation)',
                '5. Compute outlet pressure and temperature'
            ],
            'equations': {
                'velocity': 'v = Q / A_pipe',
                'reynolds': 'Re = ρ * v * D / μ',
                'friction_laminar': 'f = 64 / Re',
                'friction_turbulent': 'f = 0.25 / [log₁₀(ε/(3.7*D) + 5.74/Re^0.9)]²',
                'pressure_drop_friction': 'ΔP_f = f * (L/D) * (ρ * v² / 2)',
                'pressure_drop_elevation': 'ΔP_e = ρ * g * Δh',
                'total_pressure_drop': 'ΔP_total = ΔP_f + ΔP_e'
            },
            'input_format': '[P_inlet, T_inlet, flow_rate]',
            'output_format': '[P_outlet, T_outlet]',
            'computational_complexity': 'O(1)',
            'numerical_methods': ['Log₁₀ calculation', 'Power operations'],
            'flow_regimes': {
                'laminar': 'Re < 2300',
                'turbulent': 'Re ≥ 2300'
            }
        }

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Dynamic model: first-order lag for pressure and temperature response.
        State: [P_out, T_out]
        Input: [P_inlet, T_inlet, flow_rate]
        """
        P_out, T_out = x
        P_out_ss, T_out_ss = self.steady_state(u)
        
        tau_pressure = 5.0  # s, pressure response time constant
        tau_temperature = 10.0  # s, temperature response time constant
        
        dP_out_dt = (P_out_ss - P_out) / tau_pressure
        dT_out_dt = (T_out_ss - T_out) / tau_temperature
        
        return np.array([dP_out_dt, dT_out_dt])

    @staticmethod
    def describe_dynamics() -> dict:
        """
        Describe the dynamics function algorithm and metadata.
        
        Returns:
            dict: Algorithm details, differential equations, and time constants
        """
        return {
            'function_name': 'dynamics',
            'purpose': 'Model dynamic response with first-order lag behavior',
            'model_type': 'First-order lag (exponential response)',
            'algorithm_steps': [
                '1. Extract current state variables [P_out, T_out]',
                '2. Calculate steady-state targets using steady_state function',
                '3. Apply first-order lag dynamics with time constants',
                '4. Return state derivatives'
            ],
            'differential_equations': {
                'pressure': 'dP_out/dt = (P_out_ss - P_out) / τ_pressure',
                'temperature': 'dT_out/dt = (T_out_ss - T_out) / τ_temperature'
            },
            'time_constants': {
                'pressure': 'τ_pressure = 5.0 s',
                'temperature': 'τ_temperature = 10.0 s'
            },
            'state_variables': ['P_out [Pa]', 'T_out [K]'],
            'input_format': 't, [P_out, T_out], [P_inlet, T_inlet, flow_rate]',
            'output_format': '[dP_out/dt, dT_out/dt]',
            'stability': 'Asymptotically stable (negative real eigenvalues)',
            'physical_interpretation': {
                'pressure_lag': 'Pipe volume and compressibility effects',
                'temperature_lag': 'Thermal mass and heat transfer effects'
            }
        }
