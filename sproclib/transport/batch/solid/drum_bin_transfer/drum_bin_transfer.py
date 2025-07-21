"""
Drum/Bin Transfer class for SPROCLIB - Standard Process Control Library

This module contains the drum/bin solid transfer model (steady-state and dynamic).
"""

import numpy as np
try:
    from .....unit.base import ProcessModel
except ImportError:
    from unit.base.ProcessModel import ProcessModel


class DrumBinTransfer(ProcessModel):
    """Drum/bin solid transfer model for batch operations (steady-state and dynamic)."""
    
    def __init__(
        self,
        container_capacity: float = 0.5,   # Container capacity [m³]
        transfer_rate_max: float = 100.0,  # Maximum transfer rate [kg/min]
        material_density: float = 800.0,   # Material bulk density [kg/m³]
        discharge_efficiency: float = 0.9, # Discharge efficiency [-]
        handling_time: float = 120.0,      # Handling time per batch [s]
        conveyor_speed: float = 0.5,       # Conveyor speed [m/s]
        transfer_distance: float = 10.0,   # Transfer distance [m]
        name: str = "DrumBinTransfer"
    ):
        super().__init__(name)
        self.container_capacity = container_capacity
        self.transfer_rate_max = transfer_rate_max
        self.material_density = material_density
        self.discharge_efficiency = discharge_efficiency
        self.handling_time = handling_time
        self.conveyor_speed = conveyor_speed
        self.transfer_distance = transfer_distance
        self.parameters = {
            'container_capacity': container_capacity, 'transfer_rate_max': transfer_rate_max,
            'material_density': material_density, 'discharge_efficiency': discharge_efficiency,
            'handling_time': handling_time, 'conveyor_speed': conveyor_speed,
            'transfer_distance': transfer_distance
        }

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state transfer rate and batch completion time.
        Args:
            u: [container_fill_level, discharge_rate_setpoint, material_flowability]
        Returns:
            [actual_transfer_rate, batch_time_remaining]
        """
        fill_level, rate_setpoint, flowability = u
        
        # Available material mass
        available_volume = self.container_capacity * fill_level
        available_mass = available_volume * self.material_density
        
        # Effective discharge rate considering flowability
        flowability_factor = 0.5 + 0.5 * flowability  # 0.5 to 1.0 range
        max_effective_rate = self.transfer_rate_max * flowability_factor * self.discharge_efficiency
        
        # Actual transfer rate
        if available_mass > 0:
            actual_rate = min(rate_setpoint, max_effective_rate)
            
            # Reduce rate near end of batch due to incomplete discharge
            if fill_level < 0.1:  # Less than 10% full
                level_factor = fill_level / 0.1
                actual_rate *= level_factor
        else:
            actual_rate = 0.0
        
        # Calculate batch time remaining
        if actual_rate > 0 and available_mass > 0:
            discharge_time = available_mass / (actual_rate / 60.0)  # Convert to kg/s
            transport_time = self.transfer_distance / self.conveyor_speed
            total_time = discharge_time + transport_time + self.handling_time
        else:
            total_time = 0.0
        
        return np.array([actual_rate, total_time])

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Dynamic model: transfer rate and container level changes.
        State: [transfer_rate, container_fill_level]
        Input: [target_fill_level, discharge_rate_setpoint, material_flowability]
        """
        transfer_rate, fill_level = x
        rate_ss, _ = self.steady_state([fill_level, u[1], u[2]])
        
        # Transfer rate dynamics (discharge mechanism response)
        tau_rate = 10.0  # s, discharge rate response time constant
        dtransfer_rate_dt = (rate_ss - transfer_rate) / tau_rate
        
        # Container level dynamics (mass balance)
        if fill_level > 0 and transfer_rate > 0:
            mass_flow_rate = transfer_rate / 60.0  # kg/s
            volume_flow_rate = mass_flow_rate / self.material_density
            dfill_level_dt = -volume_flow_rate / self.container_capacity
        else:
            dfill_level_dt = 0.0
            if fill_level <= 0:
                transfer_rate = 0.0  # Stop transfer when empty
        
        return np.array([dtransfer_rate_dt, dfill_level_dt])

    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the DrumBinTransfer model including
                  algorithms, parameters, equations, and usage information.
        """
        return {
            'model_type': 'Drum/Bin Solid Transfer',
            'description': 'Batch solid material transfer using drums or bins with conveyor discharge',
            'algorithms': {
                'steady_state': 'Material flow rate calculation with discharge efficiency and flowability factors',
                'dynamics': 'First-order response of transfer rate and container level mass balance'
            },
            'parameters': {
                'container_capacity': {'value': self.container_capacity, 'unit': 'm³', 'description': 'Container volume capacity'},
                'transfer_rate_max': {'value': self.transfer_rate_max, 'unit': 'kg/min', 'description': 'Maximum discharge rate'},
                'material_density': {'value': self.material_density, 'unit': 'kg/m³', 'description': 'Bulk density of material'},
                'discharge_efficiency': {'value': self.discharge_efficiency, 'unit': '-', 'description': 'Discharge mechanism efficiency'},
                'handling_time': {'value': self.handling_time, 'unit': 's', 'description': 'Setup and handling time per batch'},
                'conveyor_speed': {'value': self.conveyor_speed, 'unit': 'm/s', 'description': 'Conveyor belt speed'},
                'transfer_distance': {'value': self.transfer_distance, 'unit': 'm', 'description': 'Transfer distance'}
            },
            'inputs': {
                'steady_state': ['container_fill_level [-]', 'discharge_rate_setpoint [kg/min]', 'material_flowability [-]'],
                'dynamics': ['target_fill_level [-]', 'discharge_rate_setpoint [kg/min]', 'material_flowability [-]']
            },
            'outputs': {
                'steady_state': ['actual_transfer_rate [kg/min]', 'batch_time_remaining [s]'],
                'dynamics': ['dtransfer_rate_dt [kg/min/s]', 'dfill_level_dt [1/s]']
            },
            'states': ['transfer_rate [kg/min]', 'container_fill_level [-]'],
            'equations': {
                'mass_balance': 'dmass/dt = -transfer_rate',
                'discharge_rate': 'rate = min(setpoint, max_rate * flowability * efficiency)',
                'batch_time': 'time = mass/rate + transport_time + handling_time'
            },
            'operating_ranges': {
                'container_capacity': [0.1, 2.0],
                'transfer_rate_max': [10.0, 500.0],
                'material_density': [200.0, 2000.0],
                'discharge_efficiency': [0.5, 1.0],
                'fill_level': [0.0, 1.0],
                'flowability': [0.0, 1.0]
            },
            'applications': ['Pharmaceutical powder transfer', 'Food ingredient handling', 'Chemical batch processing'],
            'assumptions': ['Constant bulk density', 'No particle segregation', 'Uniform discharge']
        }
