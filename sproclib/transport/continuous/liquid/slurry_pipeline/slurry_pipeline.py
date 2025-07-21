"""
Slurry Pipeline class for SPROCLIB - Standard Process Control Library

This module contains the slurry pipeline transport model (steady-state and dynamic).
"""

import numpy as np
try:
    from .....unit.base import ProcessModel
except ImportError:
    # Use mock for testing
    from ProcessModel_mock import ProcessModel


class SlurryPipeline(ProcessModel):
    """Slurry pipeline transport model for solid/liquid mixtures (steady-state and dynamic)."""
    
    def __init__(
        self,
        pipe_length: float = 500.0,     # Pipeline length [m]
        pipe_diameter: float = 0.2,     # Pipeline diameter [m]
        solid_concentration: float = 0.3, # Volume fraction of solids [-]
        particle_diameter: float = 1e-3, # Average particle diameter [m]
        fluid_density: float = 1000.0,  # Carrier fluid density [kg/m³]
        solid_density: float = 2500.0,  # Solid particle density [kg/m³]
        fluid_viscosity: float = 1e-3,  # Carrier fluid viscosity [Pa·s]
        flow_nominal: float = 0.05,     # Nominal volumetric flow [m³/s]
        name: str = "SlurryPipeline"
    ):
        super().__init__(name)
        self.pipe_length = pipe_length
        self.pipe_diameter = pipe_diameter
        self.solid_concentration = solid_concentration
        self.particle_diameter = particle_diameter
        self.fluid_density = fluid_density
        self.solid_density = solid_density
        self.fluid_viscosity = fluid_viscosity
        self.flow_nominal = flow_nominal
        self.parameters = {
            'pipe_length': pipe_length, 'pipe_diameter': pipe_diameter,
            'solid_concentration': solid_concentration, 'particle_diameter': particle_diameter,
            'fluid_density': fluid_density, 'solid_density': solid_density,
            'fluid_viscosity': fluid_viscosity, 'flow_nominal': flow_nominal
        }

    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Comprehensive metadata about the SlurryPipeline model including
                  algorithms, parameters, equations, and usage information.
        """
        return {
            'class_name': 'SlurryPipeline',
            'module': 'transport.continuous.liquid.SlurryPipeline',
            'description': 'Slurry pipeline transport model for solid/liquid mixtures',
            'model_type': 'Multiphase Transport Model',
            'physics': {
                'domain': 'Multiphase Fluid Mechanics',
                'phenomena': ['Solid-liquid flow', 'Particle settling', 'Friction enhancement', 'Concentration gradients'],
                'assumptions': ['Homogeneous mixture', 'Spherical particles', 'Negligible particle-particle interaction']
            },
            'algorithms': {
                'slurry_density': 'ρ_slurry = ρ_fluid * (1 - C_s) + ρ_solid * C_s',
                'effective_viscosity': 'μ_eff = μ_fluid * (1 + 2.5*C_s + 10.05*C_s²) [Einstein relation]',
                'reynolds_number': 'Re = ρ_slurry * v * D / μ_eff',
                'friction_factor': 'Depends on flow regime with solid enhancement',
                'settling_model': 'settling_factor = max(0.8, 1.0 - 0.1*v)',
                'dynamics': 'Dual time constants for pressure and concentration'
            },
            'parameters': self.parameters,
            'inputs': {
                'steady_state': ['P_inlet [Pa]', 'flow_rate [m³/s]', 'inlet_solid_concentration [-]'],
                'dynamics': ['P_inlet [Pa]', 'flow_rate [m³/s]', 'inlet_solid_concentration [-]']
            },
            'outputs': {
                'steady_state': ['P_outlet [Pa]', 'outlet_solid_concentration [-]'],
                'dynamics': ['dP_out/dt [Pa/s]', 'dC_solid/dt [1/s]']
            },
            'state_variables': ['P_out [Pa]', 'C_solid_out [-]'],
            'methods': ['steady_state', 'dynamics', 'describe'],
            'correlations': {
                'einstein_viscosity': 'For dilute suspensions',
                'friction_enhancement': 'Accounts for particle effects on wall friction'
            },
            'typical_applications': ['Mining slurries', 'Dredging operations', 'Wastewater treatment'],
            'design_considerations': ['Minimum transport velocity', 'Erosion potential', 'Settling prevention'],
            'limitations': ['Homogeneous flow assumption', 'Limited to spherical particles', 'No agglomeration effects']
        }

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state pressure drop and solid concentration for given flow.
        Args:
            u: [P_inlet, flow_rate, inlet_solid_concentration]
        Returns:
            [P_outlet, outlet_solid_concentration]
        """
        P_in, flow_rate, c_solid_in = u
        
        # Calculate slurry properties
        slurry_density = self.fluid_density * (1 - c_solid_in) + self.solid_density * c_solid_in
        
        # Effective viscosity (simplified Einstein relation)
        viscosity_factor = 1 + 2.5 * c_solid_in + 10.05 * c_solid_in**2
        effective_viscosity = self.fluid_viscosity * viscosity_factor
        
        # Flow velocity
        velocity = flow_rate / (np.pi * (self.pipe_diameter/2)**2)
        
        # Reynolds number for slurry
        Re = slurry_density * velocity * self.pipe_diameter / effective_viscosity
        
        # Friction factor with solid particle effects
        if Re < 2300:  # Laminar flow
            f = 64 / Re
        else:  # Turbulent flow
            f = 0.316 / Re**0.25
        
        # Additional pressure drop due to solids
        solid_effect_factor = 1 + 3 * c_solid_in
        pressure_drop = f * (self.pipe_length/self.pipe_diameter) * (slurry_density * velocity**2 / 2) * solid_effect_factor
        
        P_out = P_in - pressure_drop
        
        # Solid concentration may change due to settling (simplified)
        settling_factor = max(0.8, 1.0 - 0.1 * velocity)  # Less settling at higher velocities
        c_solid_out = c_solid_in * settling_factor
        
        return np.array([P_out, c_solid_out])

    @staticmethod
    def describe_steady_state() -> dict:
        """
        Describe the steady_state function algorithm and metadata.
        
        Returns:
            dict: Algorithm details, equations, and multiphase calculations
        """
        return {
            'function_name': 'steady_state',
            'purpose': 'Calculate steady-state pressure drop and concentration for slurry flow',
            'algorithm_steps': [
                '1. Calculate slurry mixture density',
                '2. Compute effective viscosity using Einstein relation',
                '3. Calculate flow velocity and Reynolds number',
                '4. Determine friction factor for slurry flow',
                '5. Apply solid effect factor for pressure drop enhancement',
                '6. Model particle settling effects on concentration'
            ],
            'equations': {
                'slurry_density': 'ρ_slurry = ρ_fluid * (1 - C_s) + ρ_solid * C_s',
                'viscosity_factor': 'η = 1 + 2.5*C_s + 10.05*C_s² [Einstein relation]',
                'effective_viscosity': 'μ_eff = μ_fluid * η',
                'velocity': 'v = Q / (π * (D/2)²)',
                'reynolds': 'Re = ρ_slurry * v * D / μ_eff',
                'friction_laminar': 'f = 64 / Re',
                'friction_turbulent': 'f = 0.316 / Re^0.25',
                'solid_effect': 'f_solid = 1 + 3 * C_s',
                'pressure_drop': 'ΔP = f * (L/D) * (ρ_slurry * v² / 2) * f_solid',
                'settling': 'settling_factor = max(0.8, 1.0 - 0.1*v)'
            },
            'input_format': '[P_inlet, flow_rate, inlet_solid_concentration]',
            'output_format': '[P_outlet, outlet_solid_concentration]',
            'computational_complexity': 'O(1)',
            'multiphase_effects': {
                'density_mixing': 'Volume-weighted average',
                'viscosity_enhancement': 'Einstein relation for spherical particles',
                'friction_enhancement': 'Empirical factor based on solid concentration',
                'settling_model': 'Velocity-dependent settling factor'
            },
            'flow_regimes': {
                'laminar': 'Re < 2300 (based on slurry properties)',
                'turbulent': 'Re ≥ 2300 (with particle effects)'
            },
            'assumptions': ['Homogeneous flow', 'Spherical particles', 'No agglomeration']
        }

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Dynamic model: pressure and concentration response.
        State: [P_out, c_solid_out]
        Input: [P_inlet, flow_rate, inlet_solid_concentration]
        """
        P_out, c_solid_out = x
        P_out_ss, c_solid_out_ss = self.steady_state(u)
        
        # Pressure response (fast)
        tau_pressure = 10.0  # s, pressure response time constant
        
        # Solid concentration response (slower due to transport delay)
        residence_time = self.pipe_length * np.pi * (self.pipe_diameter/2)**2 / u[1]
        tau_concentration = residence_time + 30.0  # s, additional mixing time
        
        dP_out_dt = (P_out_ss - P_out) / tau_pressure
        dc_solid_dt = (c_solid_out_ss - c_solid_out) / tau_concentration
        
        return np.array([dP_out_dt, dc_solid_dt])

    @staticmethod
    def describe_dynamics() -> dict:
        """
        Describe the dynamics function algorithm and metadata.
        
        Returns:
            dict: Algorithm details, differential equations, and transport delays
        """
        return {
            'function_name': 'dynamics',
            'purpose': 'Model dynamic pressure and concentration response in slurry pipeline',
            'model_type': 'Dual time constant system with transport delay',
            'algorithm_steps': [
                '1. Extract current state [P_out, c_solid_out]',
                '2. Calculate steady-state targets',
                '3. Apply fast pressure dynamics',
                '4. Calculate residence time for concentration dynamics',
                '5. Apply slower concentration dynamics with transport delay',
                '6. Return state derivatives'
            ],
            'differential_equations': {
                'pressure': 'dP_out/dt = (P_out_ss - P_out) / τ_pressure',
                'concentration': 'dc_solid/dt = (c_solid_ss - c_solid) / τ_concentration'
            },
            'time_constants': {
                'pressure': 'τ_pressure = 10.0 s (fixed)',
                'concentration': 'τ_concentration = residence_time + 30.0 s (flow-dependent)'
            },
            'transport_delay': {
                'residence_time': 't_res = V_pipe / Q = (L * π * (D/2)²) / flow_rate',
                'physical_meaning': 'Time for fluid to travel through pipeline',
                'additional_mixing': '30.0 s for concentration equilibration'
            },
            'state_variables': ['P_out [Pa]', 'c_solid_out [-]'],
            'input_format': 't, [P_out, c_solid_out], [P_inlet, flow_rate, c_solid_in]',
            'output_format': '[dP_out/dt, dc_solid/dt]',
            'stability': 'Stable for positive time constants',
            'physical_interpretation': {
                'pressure_response': 'Compressibility and momentum effects',
                'concentration_response': 'Advection, mixing, and settling dynamics',
                'coupling': 'Concentration affects pressure through density changes'
            },
            'design_implications': {
                'faster_response': 'Increase flow rate (reduces residence time)',
                'concentration_control': 'Consider transport delays in control design'
            }
        }
