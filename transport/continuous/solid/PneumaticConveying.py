"""
Pneumatic Conveying class for SPROCLIB - Standard Process Control Library

This module contains the pneumatic conveying transport model (steady-state and dynamic).
"""

import numpy as np
from ....unit.base import ProcessModel


class PneumaticConveying(ProcessModel):
    """Pneumatic conveying transport model for solid particles (steady-state and dynamic)."""
    
    def __init__(
        self,
        pipe_length: float = 100.0,     # Conveying line length [m]
        pipe_diameter: float = 0.1,     # Pipe diameter [m]
        particle_density: float = 1500.0, # Particle density [kg/m³]
        particle_diameter: float = 500e-6, # Average particle diameter [m]
        air_density: float = 1.2,       # Air density [kg/m³]
        air_viscosity: float = 18e-6,   # Air viscosity [Pa·s]
        conveying_velocity: float = 20.0, # Conveying air velocity [m/s]
        solid_loading_ratio: float = 10.0, # Solid to air mass ratio [-]
        name: str = "PneumaticConveying"
    ):
        super().__init__(name)
        self.pipe_length = pipe_length
        self.pipe_diameter = pipe_diameter
        self.particle_density = particle_density
        self.particle_diameter = particle_diameter
        self.air_density = air_density
        self.air_viscosity = air_viscosity
        self.conveying_velocity = conveying_velocity
        self.solid_loading_ratio = solid_loading_ratio
        self.parameters = {
            'pipe_length': pipe_length, 'pipe_diameter': pipe_diameter,
            'particle_density': particle_density, 'particle_diameter': particle_diameter,
            'air_density': air_density, 'air_viscosity': air_viscosity,
            'conveying_velocity': conveying_velocity, 'solid_loading_ratio': solid_loading_ratio
        }

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state pressure drop and particle velocity for given conditions.
        Args:
            u: [P_inlet, air_flow_rate, solid_mass_flow]
        Returns:
            [P_outlet, particle_velocity]
        """
        P_in, air_flow, solid_flow = u
        
        # Calculate air velocity
        pipe_area = np.pi * (self.pipe_diameter/2)**2
        air_velocity = air_flow / (pipe_area * self.air_density)
        
        # Particle terminal velocity
        g = 9.81  # m/s²
        Re_particle = self.air_density * air_velocity * self.particle_diameter / self.air_viscosity
        
        # Drag coefficient (sphere)
        if Re_particle < 1:
            Cd = 24 / Re_particle
        elif Re_particle < 1000:
            Cd = 24 / Re_particle * (1 + 0.15 * Re_particle**0.687)
        else:
            Cd = 0.44
        
        # Terminal velocity
        v_terminal = np.sqrt(4 * g * self.particle_diameter * (self.particle_density - self.air_density) / 
                           (3 * Cd * self.air_density))
        
        # Particle velocity (fraction of air velocity)
        slip_factor = min(0.9, v_terminal / air_velocity)
        particle_velocity = air_velocity * (1 - slip_factor)
        
        # Pressure drop calculation
        # Air-only pressure drop
        f_air = 0.316 / (Re_particle**0.25)  # Smooth pipe approximation
        dp_air = f_air * (self.pipe_length/self.pipe_diameter) * (self.air_density * air_velocity**2 / 2)
        
        # Additional pressure drop due to solids
        solid_loading = solid_flow / air_flow
        acceleration_dp = solid_loading * self.air_density * air_velocity**2
        friction_dp = 0.1 * solid_loading * dp_air  # Empirical correlation
        
        total_pressure_drop = dp_air + acceleration_dp + friction_dp
        P_out = P_in - total_pressure_drop
        
        return np.array([P_out, particle_velocity])

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Dynamic model: pressure and particle velocity response.
        State: [P_out, particle_velocity]
        Input: [P_inlet, air_flow_rate, solid_mass_flow]
        """
        P_out, v_particle = x
        P_out_ss, v_particle_ss = self.steady_state(u)
        
        # Pressure response (fast)
        tau_pressure = 3.0  # s, pressure response time constant
        
        # Particle velocity response (related to particle acceleration)
        particle_mass = self.particle_density * (4/3) * np.pi * (self.particle_diameter/2)**3
        tau_velocity = particle_mass / (6 * np.pi * self.air_viscosity * self.particle_diameter/2)
        
        dP_out_dt = (P_out_ss - P_out) / tau_pressure
        dv_particle_dt = (v_particle_ss - v_particle) / tau_velocity
        
        return np.array([dP_out_dt, dv_particle_dt])
