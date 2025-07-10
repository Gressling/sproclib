"""
Gravity Chute class for SPROCLIB - Standard Process Control Library

This module contains the gravity chute transport model (steady-state and dynamic).
"""

import numpy as np
from ....unit.base import ProcessModel


class GravityChute(ProcessModel):
    """Gravity chute transport model for solid particles (steady-state and dynamic)."""
    
    def __init__(
        self,
        chute_length: float = 10.0,     # Chute length [m]
        chute_width: float = 0.5,       # Chute width [m]
        chute_angle: float = 0.524,     # Chute angle (30 degrees) [rad]
        surface_roughness: float = 0.3, # Surface friction coefficient [-]
        particle_density: float = 2000.0, # Particle density [kg/m³]
        particle_diameter: float = 5e-3, # Average particle diameter [m]
        air_resistance: float = 0.01,   # Air resistance coefficient [-]
        name: str = "GravityChute"
    ):
        super().__init__(name)
        self.chute_length = chute_length
        self.chute_width = chute_width
        self.chute_angle = chute_angle
        self.surface_roughness = surface_roughness
        self.particle_density = particle_density
        self.particle_diameter = particle_diameter
        self.air_resistance = air_resistance
        self.parameters = {
            'chute_length': chute_length, 'chute_width': chute_width, 'chute_angle': chute_angle,
            'surface_roughness': surface_roughness, 'particle_density': particle_density,
            'particle_diameter': particle_diameter, 'air_resistance': air_resistance
        }

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state particle velocity and flow rate.
        Args:
            u: [feed_rate, particle_size_factor, chute_loading]
        Returns:
            [outlet_velocity, mass_flow_rate]
        """
        feed_rate, size_factor, loading = u
        
        g = 9.81  # m/s²
        
        # Effective particle diameter
        eff_diameter = self.particle_diameter * size_factor
        
        # Terminal velocity calculation accounting for size
        drag_factor = self.air_resistance * (eff_diameter / self.particle_diameter)**2
        
        # Force balance for sliding particle
        # Gravitational force component along chute
        F_gravity = g * np.sin(self.chute_angle)
        
        # Friction force
        F_friction = self.surface_roughness * g * np.cos(self.chute_angle)
        
        # Net acceleration
        net_acceleration = F_gravity - F_friction
        
        # Steady-state velocity (considering air resistance)
        if net_acceleration > 0:
            terminal_velocity = np.sqrt(net_acceleration / drag_factor)
        else:
            terminal_velocity = 0.0  # Particles won't flow
        
        # Actual velocity considering loading effects
        loading_factor = max(0.5, 1.0 - 0.5 * loading)  # Reduced velocity at high loading
        actual_velocity = terminal_velocity * loading_factor
        
        # Flow rate calculation
        # Cross-sectional area occupied by particles
        particle_layer_thickness = loading * 0.1  # m, empirical
        flow_area = self.chute_width * particle_layer_thickness
        
        # Mass flow rate
        bulk_density = self.particle_density * 0.6  # Packing factor
        mass_flow_rate = min(feed_rate, flow_area * actual_velocity * bulk_density)
        
        return np.array([actual_velocity, mass_flow_rate])

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Dynamic model: particle velocity and flow rate response.
        State: [outlet_velocity, mass_flow_rate]
        Input: [feed_rate, particle_size_factor, chute_loading]
        """
        velocity, flow_rate = x
        velocity_ss, flow_ss = self.steady_state(u)
        
        # Velocity response (particle acceleration time)
        g = 9.81
        net_acceleration = g * (np.sin(self.chute_angle) - self.surface_roughness * np.cos(self.chute_angle))
        if net_acceleration > 0:
            tau_velocity = velocity_ss / net_acceleration  # Time to reach terminal velocity
        else:
            tau_velocity = 1.0  # Default
        
        # Flow rate response (transport delay)
        if velocity > 0:
            transport_time = self.chute_length / velocity
        else:
            transport_time = 10.0  # Default for zero velocity
        tau_flow = transport_time + 2.0  # s, additional response time
        
        dvelocity_dt = (velocity_ss - velocity) / max(tau_velocity, 0.5)
        dflow_dt = (flow_ss - flow_rate) / tau_flow
        
        return np.array([dvelocity_dt, dflow_dt])

    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the GravityChute model including
                  algorithms, parameters, equations, and usage information.
        """
        return {
            'class_name': 'GravityChute',
            'algorithm': 'Gravity-driven particle flow with friction and air resistance',
            'parameters': {
                'chute_length': {'value': self.chute_length, 'unit': 'm', 'description': 'Chute length'},
                'chute_width': {'value': self.chute_width, 'unit': 'm', 'description': 'Chute width'},
                'chute_angle': {'value': self.chute_angle, 'unit': 'rad', 'description': 'Chute angle'},
                'surface_roughness': {'value': self.surface_roughness, 'unit': '-', 'description': 'Surface friction coefficient'},
                'particle_density': {'value': self.particle_density, 'unit': 'kg/m³', 'description': 'Particle density'},
                'particle_diameter': {'value': self.particle_diameter, 'unit': 'm', 'description': 'Average particle diameter'},
                'air_resistance': {'value': self.air_resistance, 'unit': '-', 'description': 'Air resistance coefficient'}
            },
            'inputs': {
                'feed_rate': {'unit': 'kg/s', 'description': 'Particle feed rate'},
                'particle_size_factor': {'unit': '-', 'description': 'Particle size factor'},
                'chute_loading': {'unit': '-', 'description': 'Chute loading factor'}
            },
            'outputs': {
                'outlet_velocity': {'unit': 'm/s', 'description': 'Particle outlet velocity'},
                'mass_flow_rate': {'unit': 'kg/s', 'description': 'Mass flow rate'}
            },
            'equations': [
                'F_gravity = g * sin(chute_angle)',
                'F_friction = surface_roughness * g * cos(chute_angle)',
                'net_acceleration = F_gravity - F_friction',
                'terminal_velocity = sqrt(net_acceleration / drag_factor)'
            ],
            'working_ranges': {
                'chute_angle': '0.17-0.79 rad (10-45°)',
                'particle_density': '1000-5000 kg/m³',
                'particle_diameter': '1e-3-20e-3 m',
                'surface_roughness': '0.1-0.8'
            },
            'applications': ['Particle discharge systems', 'Gravity conveyors', 'Granular material handling'],
            'limitations': ['Assumes uniform particle size', 'No particle breakage', 'Steady flow conditions']
        }
