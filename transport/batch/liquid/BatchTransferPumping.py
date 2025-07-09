"""
Batch Transfer (Pumping) class for SPROCLIB - Standard Process Control Library

This module contains the batch liquid transfer pumping model (steady-state and dynamic).
"""

import numpy as np
from ....unit.base import ProcessModel


class BatchTransferPumping(ProcessModel):
    """Batch liquid transfer pumping model (steady-state and dynamic)."""
    
    def __init__(
        self,
        pump_capacity: float = 0.01,    # Pump capacity [m³/s]
        pump_head_max: float = 50.0,    # Maximum pump head [m]
        tank_volume: float = 1.0,       # Tank volume [m³]
        pipe_length: float = 20.0,      # Transfer line length [m]
        pipe_diameter: float = 0.05,    # Transfer line diameter [m]
        fluid_density: float = 1000.0,  # Fluid density [kg/m³]
        fluid_viscosity: float = 1e-3,  # Fluid viscosity [Pa·s]
        transfer_efficiency: float = 0.85, # Transfer efficiency [-]
        name: str = "BatchTransferPumping"
    ):
        super().__init__(name)
        self.pump_capacity = pump_capacity
        self.pump_head_max = pump_head_max
        self.tank_volume = tank_volume
        self.pipe_length = pipe_length
        self.pipe_diameter = pipe_diameter
        self.fluid_density = fluid_density
        self.fluid_viscosity = fluid_viscosity
        self.transfer_efficiency = transfer_efficiency
        self.parameters = {
            'pump_capacity': pump_capacity, 'pump_head_max': pump_head_max, 'tank_volume': tank_volume,
            'pipe_length': pipe_length, 'pipe_diameter': pipe_diameter, 'fluid_density': fluid_density,
            'fluid_viscosity': fluid_viscosity, 'transfer_efficiency': transfer_efficiency
        }

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state flow rate and transfer time for batch operation.
        Args:
            u: [source_level, destination_level, pump_speed_fraction]
        Returns:
            [flow_rate, transfer_time_remaining]
        """
        source_level, dest_level, pump_speed = u
        
        # Calculate hydraulic head
        static_head = dest_level - source_level
        
        # Estimate flow rate based on pump curve
        flow_rate = self.pump_capacity * pump_speed * self.transfer_efficiency
        
        # Calculate system resistance
        if flow_rate > 0:
            velocity = flow_rate / (np.pi * (self.pipe_diameter/2)**2)
            Re = self.fluid_density * velocity * self.pipe_diameter / self.fluid_viscosity
            
            # Friction factor
            if Re > 0:
                if Re < 2300:  # Laminar
                    f = 64 / Re
                else:  # Turbulent
                    f = 0.316 / Re**0.25
            else:
                f = 0.02
            
            # Friction head loss
            friction_head = f * (self.pipe_length/self.pipe_diameter) * (velocity**2 / (2 * 9.81))
            
            # Total head required
            total_head = static_head + friction_head
            
            # Check if pump can deliver required head
            if total_head > self.pump_head_max * pump_speed:
                # Reduce flow rate due to insufficient head
                head_ratio = (self.pump_head_max * pump_speed) / total_head
                flow_rate *= head_ratio
        else:
            flow_rate = 0.0
        
        # Calculate transfer time remaining
        if source_level > 0 and flow_rate > 0:
            remaining_volume = source_level * self.tank_volume
            transfer_time = remaining_volume / flow_rate
        else:
            transfer_time = 0.0
        
        return np.array([flow_rate, transfer_time])

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Dynamic model: flow rate and tank level changes.
        State: [flow_rate, source_level]
        Input: [source_level_setpoint, destination_level, pump_speed_fraction]
        """
        flow_rate, source_level = x
        flow_ss, _ = self.steady_state([source_level, u[1], u[2]])
        
        # Flow rate dynamics (pump response)
        tau_flow = 5.0  # s, pump response time constant
        dflow_dt = (flow_ss - flow_rate) / tau_flow
        
        # Source level dynamics (mass balance)
        if source_level > 0:
            dlevel_dt = -flow_rate / self.tank_volume
        else:
            dlevel_dt = 0.0
            flow_rate = 0.0  # Stop flow when empty
        
        return np.array([dflow_dt, dlevel_dt])
