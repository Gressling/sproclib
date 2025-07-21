"""
Control Valve Model for SPROCLIB

This module provides a control valve model with flow coefficient
characteristics, dead-time, and pressure drop compensation.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import logging
from typing import Dict
from ...base import ProcessModel

logger = logging.getLogger(__name__)


class ControlValve(ProcessModel):
    """
    Control valve model with flow coefficient (Cv) characteristics and dead-time.
    
    Features:
    - Flow coefficient-based flow calculations
    - Valve position dead-time modeling
    - Pressure drop compensation
    - Valve characteristics (linear, equal percentage, quick opening)
    - Saturation limits
    """
    
    def __init__(self, 
                 Cv_max: float = 100.0,
                 valve_type: str = "linear",
                 dead_time: float = 0.5,
                 time_constant: float = 2.0,
                 rangeability: float = 50.0,
                 name: str = "ControlValve"):
        """
        Initialize control valve model.
        
        Args:
            Cv_max: Maximum flow coefficient (gpm/psi^0.5)
            valve_type: Valve characteristic ('linear', 'equal_percentage', 'quick_opening')
            dead_time: Valve position dead-time (seconds)
            time_constant: Valve actuator time constant (seconds)  
            rangeability: Valve rangeability (Cv_max/Cv_min)
            name: Valve identifier
        """
        super().__init__(name)
        
        self.Cv_max = Cv_max
        self.valve_type = valve_type
        self.dead_time = dead_time
        self.time_constant = time_constant
        self.rangeability = rangeability
        self.Cv_min = Cv_max / rangeability
        
        # Dead-time buffer for valve position
        self.position_buffer = []
        self.time_buffer = []
        
        # State: [actual_position, flow_rate]
        self.state_names = ['valve_position', 'flow_rate']
        
        self.parameters.update({
            'Cv_max': Cv_max,
            'valve_type': valve_type,
            'dead_time': dead_time,
            'time_constant': time_constant,
            'rangeability': rangeability
        })
        
        logger.info(f"Created control valve {name} with Cv_max={Cv_max}, type={valve_type}")

    def _valve_characteristic(self, position: float) -> float:
        """
        Calculate flow coefficient based on valve position and characteristic.
        
        Args:
            position: Valve position (0-1)
            
        Returns:
            Flow coefficient Cv
        """
        # Ensure position is within bounds
        position = np.clip(position, 0.0, 1.0)
        
        if self.valve_type == "linear":
            # Linear characteristic: Cv = Cv_min + position * (Cv_max - Cv_min)
            Cv = self.Cv_min + position * (self.Cv_max - self.Cv_min)
            
        elif self.valve_type == "equal_percentage":
            # Equal percentage: Cv = Cv_min * R^position where R = rangeability
            Cv = self.Cv_min * (self.rangeability ** position)
            
        elif self.valve_type == "quick_opening":
            # Quick opening: rapid increase at low positions
            Cv = self.Cv_min + (self.Cv_max - self.Cv_min) * np.sqrt(position)
            
        else:
            raise ValueError(f"Unknown valve type: {self.valve_type}")
        
        return Cv

    def _calculate_flow(self, Cv: float, delta_P: float, rho: float = 1000.0) -> float:
        """
        Calculate flow rate using valve equation.
        
        Args:
            Cv: Flow coefficient
            delta_P: Pressure drop across valve (Pa)
            rho: Fluid density (kg/m³)
            
        Returns:
            Flow rate (m³/s)
        """
        if delta_P <= 0:
            return 0.0
        
        # Convert Cv from gpm/psi^0.5 to SI units and calculate flow
        # Standard valve equation: Q = Cv * sqrt(delta_P / rho)
        Cv_si = Cv * 6.309e-5  # Convert gpm/psi^0.5 to m³/s/(Pa^0.5)
        flow_rate = Cv_si * np.sqrt(delta_P / rho)
        
        return flow_rate

    def _update_dead_time_buffer(self, t: float, position_command: float):
        """Update the dead-time buffer for valve position."""
        self.time_buffer.append(t)
        self.position_buffer.append(position_command)
        
        # Remove old entries beyond dead_time
        while (self.time_buffer and 
               self.time_buffer[0] < t - self.dead_time - 0.1):
            self.time_buffer.pop(0)
            self.position_buffer.pop(0)

    def _get_delayed_position(self, t: float) -> float:
        """Get valve position after dead-time delay."""
        target_time = t - self.dead_time
        
        # If no history or target time is before first entry, return 0
        if not self.time_buffer or target_time < self.time_buffer[0]:
            return 0.0
            
        # If target time is after last entry, return last value
        if target_time >= self.time_buffer[-1]:
            return self.position_buffer[-1]
            
        # Linear interpolation between points
        for i in range(len(self.time_buffer) - 1):
            if (self.time_buffer[i] <= target_time <= self.time_buffer[i + 1]):
                t1, t2 = self.time_buffer[i], self.time_buffer[i + 1]
                p1, p2 = self.position_buffer[i], self.position_buffer[i + 1]
                return p1 + (p2 - p1) * (target_time - t1) / (t2 - t1)
                
        return 0.0

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Valve dynamics with dead-time and first-order lag.
        
        State: [actual_position, flow_rate]
        Input: [position_command, upstream_pressure, downstream_pressure, density]
        
        Args:
            t: Time
            x: [actual_position, flow_rate]  
            u: [position_command, P_upstream, P_downstream, rho]
            
        Returns:
            [d(position)/dt, d(flow)/dt]
        """
        actual_position, current_flow = x
        position_command, P_up, P_down, rho = u
        
        # Update dead-time buffer
        self._update_dead_time_buffer(t, position_command)
        
        # Get delayed position command
        delayed_command = self._get_delayed_position(t)
        
        # First-order lag for valve position
        dpos_dt = (delayed_command - actual_position) / self.time_constant
        
        # Calculate desired flow based on current position
        Cv = self._valve_characteristic(actual_position)
        delta_P = max(0, P_up - P_down)
        desired_flow = self._calculate_flow(Cv, delta_P, rho)
        
        # Fast flow response (much faster than valve position)
        flow_time_constant = self.time_constant / 10.0
        dflow_dt = (desired_flow - current_flow) / flow_time_constant
        
        return np.array([dpos_dt, dflow_dt])

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state valve position and flow.
        
        Args:
            u: [position_command, P_upstream, P_downstream, rho]
            
        Returns:
            [position, flow_rate]
        """
        position_command, P_up, P_down, rho = u
        
        # At steady state, actual position equals command (no dead-time effect)
        steady_position = np.clip(position_command, 0.0, 1.0)
        
        # Calculate steady-state flow
        Cv = self._valve_characteristic(steady_position)
        delta_P = max(0, P_up - P_down)
        steady_flow = self._calculate_flow(Cv, delta_P, rho)
        
        return np.array([steady_position, steady_flow])

    def get_flow_coefficient(self, position: float) -> float:
        """Get flow coefficient for given valve position."""
        return self._valve_characteristic(position)

    def get_valve_sizing_info(self) -> Dict[str, float]:
        """Get valve sizing information."""
        return {
            'Cv_max': self.Cv_max,
            'Cv_min': self.Cv_min,
            'rangeability': self.rangeability,
            'valve_type': self.valve_type,
            'dead_time': self.dead_time,
            'time_constant': self.time_constant
        }

    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the model including algorithms, 
                  parameters, equations, and usage information.
        """
        return {
            'type': 'ControlValve',
            'description': 'Control valve model with flow coefficient characteristics, dead-time, and pressure drop compensation for industrial flow control applications',
            'category': 'unit/valve',
            'algorithms': {
                'valve_characteristic': 'Cv = f(position) based on linear, equal-percentage, or quick-opening characteristics',
                'flow_calculation': 'Q = Cv * sqrt(ΔP/ρ) - Standard valve flow equation',
                'dead_time_modeling': 'First-order lag with transport delay for actuator dynamics',
                'pressure_drop': 'ΔP = P_upstream - P_downstream with flow direction logic'
            },
            'parameters': {
                'Cv_max': {
                    'value': self.Cv_max,
                    'units': 'gpm/psi^0.5',
                    'description': 'Maximum flow coefficient at fully open position'
                },
                'valve_type': {
                    'value': self.valve_type,
                    'units': 'dimensionless',
                    'description': 'Valve characteristic curve (linear, equal_percentage, quick_opening)'
                },
                'dead_time': {
                    'value': self.dead_time,
                    'units': 's',
                    'description': 'Actuator dead time delay'
                },
                'time_constant': {
                    'value': self.time_constant,
                    'units': 's',
                    'description': 'Actuator time constant for first-order response'
                },
                'rangeability': {
                    'value': self.rangeability,
                    'units': 'dimensionless',
                    'description': 'Ratio of maximum to minimum controllable flow coefficient'
                }
            },
            'state_variables': self.state_names,
            'inputs': ['position_command', 'upstream_pressure', 'downstream_pressure', 'fluid_density'],
            'outputs': ['valve_position', 'flow_rate'],
            'valid_ranges': {
                'Cv_max': {'min': 1.0, 'max': 1000.0, 'units': 'gpm/psi^0.5'},
                'position_command': {'min': 0.0, 'max': 1.0, 'units': 'fraction'},
                'pressure_drop': {'min': 0.0, 'max': 1.0e7, 'units': 'Pa'},
                'dead_time': {'min': 0.0, 'max': 60.0, 'units': 's'},
                'rangeability': {'min': 5.0, 'max': 100.0, 'units': 'dimensionless'}
            },
            'applications': ['Flow control loops', 'Pressure regulation', 'Level control systems', 'Temperature control via flow manipulation', 'Process safety shutdown systems'],
            'limitations': ['Assumes incompressible flow', 'Single-phase fluid only', 'No cavitation modeling', 'Linear actuator dynamics approximation', 'Constant fluid properties']
        }
