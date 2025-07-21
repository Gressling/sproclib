"""
Vacuum Transfer class for SPROCLIB - Standard Process Control Library

This module contains the vacuum powder transfer model (steady-state and dynamic).
"""

import numpy as np
try:
    from .....unit.base import ProcessModel
except ImportError:
    from unit.base.ProcessModel import ProcessModel


class VacuumTransfer(ProcessModel):
    """Vacuum powder transfer model for batch operations (steady-state and dynamic)."""
    
    def __init__(
        self,
        vacuum_pump_capacity: float = 100.0, # Vacuum pump capacity [m³/h]
        transfer_line_diameter: float = 0.05, # Transfer line diameter [m]
        transfer_line_length: float = 5.0,    # Transfer line length [m]
        powder_density: float = 600.0,        # Powder bulk density [kg/m³]
        particle_size: float = 100e-6,        # Average particle size [m]
        cyclone_efficiency: float = 0.95,     # Cyclone separator efficiency [-]
        vacuum_level_max: float = -80000.0,   # Maximum vacuum level [Pa gauge]
        filter_resistance: float = 1000.0,    # Filter resistance [Pa⋅s/m³]
        name: str = "VacuumTransfer"
    ):
        super().__init__(name)
        self.vacuum_pump_capacity = vacuum_pump_capacity
        self.transfer_line_diameter = transfer_line_diameter
        self.transfer_line_length = transfer_line_length
        self.powder_density = powder_density
        self.particle_size = particle_size
        self.cyclone_efficiency = cyclone_efficiency
        self.vacuum_level_max = vacuum_level_max
        self.filter_resistance = filter_resistance
        self.parameters = {
            'vacuum_pump_capacity': vacuum_pump_capacity, 'transfer_line_diameter': transfer_line_diameter,
            'transfer_line_length': transfer_line_length, 'powder_density': powder_density,
            'particle_size': particle_size, 'cyclone_efficiency': cyclone_efficiency,
            'vacuum_level_max': vacuum_level_max, 'filter_resistance': filter_resistance
        }

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state transfer rate and vacuum level.
        Args:
            u: [source_powder_level, vacuum_setpoint, filter_loading]
        Returns:
            [powder_transfer_rate, actual_vacuum_level]
        """
        powder_level, vacuum_setpoint, filter_loading = u
        
        # Available powder for transfer
        if powder_level <= 0:
            return np.array([0.0, 0.0])  # No transfer if no powder
        
        # Air flow calculation through transfer line
        pipe_area = np.pi * (self.transfer_line_diameter/2)**2
        
        # Pressure drop in transfer line (simplified)
        air_density = 1.2  # kg/m³ at standard conditions
        air_viscosity = 18e-6  # Pa⋅s
        
        # Vacuum level limited by pump capacity and system resistance
        pump_flow = self.vacuum_pump_capacity / 3600.0  # m³/s
        
        # System resistance
        line_resistance = 32 * air_viscosity * self.transfer_line_length / (self.transfer_line_diameter**2)
        filter_resistance_total = self.filter_resistance * (1 + filter_loading * 2)
        total_resistance = line_resistance + filter_resistance_total
        
        # Actual vacuum level
        vacuum_pressure_drop = pump_flow * total_resistance
        actual_vacuum = min(abs(vacuum_setpoint), abs(self.vacuum_level_max))
        actual_vacuum = max(actual_vacuum, vacuum_pressure_drop)
        
        # Air velocity in transfer line
        if actual_vacuum > 0:
            air_velocity = np.sqrt(2 * actual_vacuum / air_density)
        else:
            air_velocity = 0.0
        
        # Powder entrainment calculation
        # Minimum air velocity for particle pickup
        g = 9.81  # m/s²
        particle_terminal_velocity = np.sqrt(4 * g * self.particle_size * self.powder_density / (3 * 0.44 * air_density))
        pickup_velocity = 2 * particle_terminal_velocity  # Safety factor
        
        if air_velocity > pickup_velocity:
            # Solid loading ratio (empirical correlation)
            velocity_ratio = air_velocity / pickup_velocity
            max_loading_ratio = min(2.0, velocity_ratio * 0.5)  # kg solid / kg air
            
            # Air mass flow
            air_mass_flow = pump_flow * air_density
            
            # Powder transfer rate
            powder_transfer_rate = air_mass_flow * max_loading_ratio * self.cyclone_efficiency
            
            # Limit by available powder
            max_available_rate = powder_level * self.powder_density * 0.1  # 10% per minute
            powder_transfer_rate = min(powder_transfer_rate, max_available_rate)
        else:
            powder_transfer_rate = 0.0
        
        return np.array([powder_transfer_rate, -actual_vacuum])  # Return as negative gauge pressure

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Dynamic model: transfer rate and vacuum level response.
        State: [powder_transfer_rate, vacuum_level]
        Input: [source_powder_level, vacuum_setpoint, filter_loading]
        """
        transfer_rate, vacuum_level = x
        rate_ss, vacuum_ss = self.steady_state(u)
        
        # Transfer rate dynamics (powder entrainment response)
        tau_transfer = 3.0  # s, powder entrainment time constant
        
        # Vacuum level dynamics (pump and system response)
        tau_vacuum = 5.0  # s, vacuum system response time constant
        
        dtransfer_rate_dt = (rate_ss - transfer_rate) / tau_transfer
        dvacuum_dt = (vacuum_ss - vacuum_level) / tau_vacuum
        
        return np.array([dtransfer_rate_dt, dvacuum_dt])

    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the VacuumTransfer model including
                  algorithms, parameters, equations, and usage information.
        """
        return {
            'model_type': 'Vacuum Powder Transfer',
            'description': 'Pneumatic powder transfer using vacuum pump and cyclone separator',
            'algorithms': {
                'steady_state': 'Air velocity and powder entrainment calculation with cyclone separation',
                'dynamics': 'First-order response of transfer rate and vacuum level'
            },
            'parameters': {
                'vacuum_pump_capacity': {'value': self.vacuum_pump_capacity, 'unit': 'm³/h', 'description': 'Vacuum pump volumetric capacity'},
                'transfer_line_diameter': {'value': self.transfer_line_diameter, 'unit': 'm', 'description': 'Transfer line internal diameter'},
                'transfer_line_length': {'value': self.transfer_line_length, 'unit': 'm', 'description': 'Transfer line length'},
                'powder_density': {'value': self.powder_density, 'unit': 'kg/m³', 'description': 'Powder bulk density'},
                'particle_size': {'value': self.particle_size, 'unit': 'm', 'description': 'Average particle diameter'},
                'cyclone_efficiency': {'value': self.cyclone_efficiency, 'unit': '-', 'description': 'Cyclone separator efficiency'},
                'vacuum_level_max': {'value': self.vacuum_level_max, 'unit': 'Pa', 'description': 'Maximum vacuum level (gauge)'},
                'filter_resistance': {'value': self.filter_resistance, 'unit': 'Pa⋅s/m³', 'description': 'Filter pressure drop resistance'}
            },
            'inputs': {
                'steady_state': ['source_powder_level [-]', 'vacuum_setpoint [Pa]', 'filter_loading [-]'],
                'dynamics': ['source_powder_level [-]', 'vacuum_setpoint [Pa]', 'filter_loading [-]']
            },
            'outputs': {
                'steady_state': ['powder_transfer_rate [kg/s]', 'actual_vacuum_level [Pa]'],
                'dynamics': ['dtransfer_rate_dt [kg/s²]', 'dvacuum_dt [Pa/s]']
            },
            'states': ['powder_transfer_rate [kg/s]', 'vacuum_level [Pa]'],
            'equations': {
                'air_velocity': 'v = sqrt(2*ΔP/ρ_air)',
                'pickup_velocity': 'v_pickup = 2*sqrt(4*g*d_p*ρ_p/(3*C_d*ρ_air))',
                'powder_rate': 'rate = Q_air * ρ_air * loading_ratio * η_cyclone',
                'pressure_drop': 'ΔP = Q * (R_line + R_filter)'
            },
            'operating_ranges': {
                'vacuum_pump_capacity': [10.0, 500.0],
                'transfer_line_diameter': [0.02, 0.15],
                'powder_density': [200.0, 1500.0],
                'particle_size': [10e-6, 500e-6],
                'cyclone_efficiency': [0.8, 0.99],
                'vacuum_level': [-100000.0, 0.0],
                'filter_loading': [0.0, 1.0]
            },
            'applications': ['Pharmaceutical powder handling', 'Food powder transfer', 'Chemical powder processing'],
            'assumptions': ['Dilute phase transport', 'Spherical particles', 'Isothermal conditions']
        }
