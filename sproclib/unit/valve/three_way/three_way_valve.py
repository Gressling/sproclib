"""
Three-Way Valve Model for SPROCLIB

This module provides a three-way valve model for flow
splitting/mixing applications with dead-time and flow coefficient calculations.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import logging
from typing import Tuple
from ...base import ProcessModel

logger = logging.getLogger(__name__)


class ThreeWayValve(ProcessModel):
    """
    Three-way control valve model for flow splitting/mixing applications.
    
    Features:
    - Mixing and diverting configurations
    - Flow coefficient-based calculations  
    - Dead-time in valve position
    - Flow distribution control
    """
    
    def __init__(self,
                 Cv_max: float = 100.0,
                 valve_config: str = "mixing",  # "mixing" or "diverting"
                 dead_time: float = 0.5,
                 time_constant: float = 2.0,
                 name: str = "ThreeWayValve"):
        """
        Initialize three-way valve model.
        
        Args:
            Cv_max: Maximum flow coefficient
            valve_config: "mixing" (two inlets, one outlet) or "diverting" (one inlet, two outlets)
            dead_time: Position dead-time (seconds)
            time_constant: Actuator time constant (seconds)
            name: Valve identifier
        """
        super().__init__(name)
        
        self.Cv_max = Cv_max
        self.valve_config = valve_config
        self.dead_time = dead_time
        self.time_constant = time_constant
        
        # Dead-time buffer
        self.position_buffer = []
        self.time_buffer = []
        
        if valve_config == "mixing":
            # State: [position, flow_out]
            # Inputs: [position_command, P1_in, P2_in, P_out, rho]
            self.state_names = ['valve_position', 'flow_out']
        elif valve_config == "diverting":
            # State: [position, flow_out1, flow_out2]  
            # Inputs: [position_command, P_in, P1_out, P2_out, rho]
            self.state_names = ['valve_position', 'flow_out1', 'flow_out2']
        else:
            raise ValueError("valve_config must be 'mixing' or 'diverting'")
            
        self.parameters.update({
            'Cv_max': Cv_max,
            'valve_config': valve_config,
            'dead_time': dead_time,
            'time_constant': time_constant
        })
        
        logger.info(f"Created 3-way valve {name}, config={valve_config}")

    def _calculate_cv_split(self, position: float) -> Tuple[float, float]:
        """
        Calculate flow coefficients for both paths based on position.
        
        Args:
            position: Valve position (0=fully path A, 1=fully path B)
            
        Returns:
            (Cv_A, Cv_B): Flow coefficients for paths A and B
        """
        position = np.clip(position, 0.0, 1.0)
        
        # Linear characteristic for simplicity
        Cv_A = self.Cv_max * (1.0 - position)
        Cv_B = self.Cv_max * position
        
        return Cv_A, Cv_B

    def _update_dead_time_buffer(self, t: float, position_command: float):
        """Update dead-time buffer."""
        self.time_buffer.append(t)
        self.position_buffer.append(position_command)
        
        while (self.time_buffer and 
               self.time_buffer[0] < t - self.dead_time - 0.1):
            self.time_buffer.pop(0)
            self.position_buffer.pop(0)

    def _get_delayed_position(self, t: float) -> float:
        """Get delayed valve position."""
        target_time = t - self.dead_time
        
        if not self.time_buffer or target_time < self.time_buffer[0]:
            return 0.0
            
        if target_time >= self.time_buffer[-1]:
            return self.position_buffer[-1]
            
        for i in range(len(self.time_buffer) - 1):
            if (self.time_buffer[i] <= target_time <= self.time_buffer[i + 1]):
                t1, t2 = self.time_buffer[i], self.time_buffer[i + 1]
                p1, p2 = self.position_buffer[i], self.position_buffer[i + 1]
                return p1 + (p2 - p1) * (target_time - t1) / (t2 - t1)
                
        return 0.0

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Three-way valve dynamics.
        
        For mixing: u = [position_command, P1_in, P2_in, P_out, rho]
        For diverting: u = [position_command, P_in, P1_out, P2_out, rho]
        """
        if self.valve_config == "mixing":
            return self._mixing_dynamics(t, x, u)
        else:
            return self._diverting_dynamics(t, x, u)

    def _mixing_dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """Mixing valve dynamics."""
        position, flow_out = x
        position_cmd, P1_in, P2_in, P_out, rho = u
        
        self._update_dead_time_buffer(t, position_cmd)
        delayed_cmd = self._get_delayed_position(t)
        
        # Position dynamics
        dpos_dt = (delayed_cmd - position) / self.time_constant
        
        # Flow calculation
        Cv_A, Cv_B = self._calculate_cv_split(position)
        
        # Calculate flows from both inlets
        Cv_si = 6.309e-5  # Conversion factor
        delta_P1 = max(0, P1_in - P_out)
        delta_P2 = max(0, P2_in - P_out)
        
        flow1 = Cv_A * Cv_si * np.sqrt(delta_P1 / rho) if delta_P1 > 0 else 0
        flow2 = Cv_B * Cv_si * np.sqrt(delta_P2 / rho) if delta_P2 > 0 else 0
        
        desired_flow_out = flow1 + flow2
        
        # Flow response
        flow_tau = self.time_constant / 10.0
        dflow_dt = (desired_flow_out - flow_out) / flow_tau
        
        return np.array([dpos_dt, dflow_dt])

    def _diverting_dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """Diverting valve dynamics."""
        position, flow_out1, flow_out2 = x
        position_cmd, P_in, P1_out, P2_out, rho = u
        
        self._update_dead_time_buffer(t, position_cmd)
        delayed_cmd = self._get_delayed_position(t)
        
        # Position dynamics
        dpos_dt = (delayed_cmd - position) / self.time_constant
        
        # Flow calculation  
        Cv_A, Cv_B = self._calculate_cv_split(position)
        
        Cv_si = 6.309e-5
        delta_P1 = max(0, P_in - P1_out)
        delta_P2 = max(0, P_in - P2_out)
        
        desired_flow1 = Cv_A * Cv_si * np.sqrt(delta_P1 / rho) if delta_P1 > 0 else 0
        desired_flow2 = Cv_B * Cv_si * np.sqrt(delta_P2 / rho) if delta_P2 > 0 else 0
        
        # Flow responses
        flow_tau = self.time_constant / 10.0
        dflow1_dt = (desired_flow1 - flow_out1) / flow_tau
        dflow2_dt = (desired_flow2 - flow_out2) / flow_tau
        
        return np.array([dpos_dt, dflow1_dt, dflow2_dt])

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """Calculate steady-state flows."""
        if self.valve_config == "mixing":
            position_cmd, P1_in, P2_in, P_out, rho = u
            position = np.clip(position_cmd, 0.0, 1.0)
            
            Cv_A, Cv_B = self._calculate_cv_split(position)
            Cv_si = 6.309e-5
            
            delta_P1 = max(0, P1_in - P_out)
            delta_P2 = max(0, P2_in - P_out)
            
            flow1 = Cv_A * Cv_si * np.sqrt(delta_P1 / rho) if delta_P1 > 0 else 0
            flow2 = Cv_B * Cv_si * np.sqrt(delta_P2 / rho) if delta_P2 > 0 else 0
            
            return np.array([position, flow1 + flow2])
            
        else:  # diverting
            position_cmd, P_in, P1_out, P2_out, rho = u
            position = np.clip(position_cmd, 0.0, 1.0)
            
            Cv_A, Cv_B = self._calculate_cv_split(position)
            Cv_si = 6.309e-5
            
            delta_P1 = max(0, P_in - P1_out)
            delta_P2 = max(0, P_in - P2_out)
            
            flow1 = Cv_A * Cv_si * np.sqrt(delta_P1 / rho) if delta_P1 > 0 else 0
            flow2 = Cv_B * Cv_si * np.sqrt(delta_P2 / rho) if delta_P2 > 0 else 0
            
            return np.array([position, flow1, flow2])

    def get_flow_split(self, position: float) -> Tuple[float, float]:
        """Get flow split percentages for given position."""
        Cv_A, Cv_B = self._calculate_cv_split(position)
        total_Cv = Cv_A + Cv_B
        if total_Cv > 0:
            return Cv_A / total_Cv, Cv_B / total_Cv
        return 0.5, 0.5

    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the model including algorithms, 
                  parameters, equations, and usage information.
        """
        return {
            'type': 'ThreeWayValve',
            'description': 'Three-way control valve for flow mixing or diverting applications with dead-time and flow coefficient modeling',
            'category': 'unit/valve',
            'algorithms': {
                'flow_splitting': 'Cv_A = Cv_max * (1-position), Cv_B = Cv_max * position',
                'mixing_flow': 'Q_out = Q_inlet1 + Q_inlet2 for mixing configuration',
                'diverting_flow': 'Q_inlet = Q_outlet1 + Q_outlet2 for diverting configuration',
                'flow_calculation': 'Q = Cv * sqrt(ΔP/ρ) for each flow path',
                'dead_time_modeling': 'Transport delay with linear interpolation'
            },
            'parameters': {
                'Cv_max': {
                    'value': self.Cv_max,
                    'units': 'gpm/psi^0.5',
                    'description': 'Maximum flow coefficient for single path'
                },
                'valve_config': {
                    'value': self.valve_config,
                    'units': 'dimensionless',
                    'description': 'Valve configuration (mixing or diverting)'
                },
                'dead_time': {
                    'value': self.dead_time,
                    'units': 's',
                    'description': 'Actuator dead time delay'
                },
                'time_constant': {
                    'value': self.time_constant,
                    'units': 's',
                    'description': 'Actuator time constant'
                }
            },
            'state_variables': self.state_names,
            'inputs': ['position_command'] + (['inlet1_pressure', 'inlet2_pressure', 'outlet_pressure'] if self.valve_config == 'mixing' else ['inlet_pressure', 'outlet1_pressure', 'outlet2_pressure']) + ['fluid_density'],
            'outputs': self.state_names,
            'valid_ranges': {
                'Cv_max': {'min': 1.0, 'max': 1000.0, 'units': 'gpm/psi^0.5'},
                'position_command': {'min': 0.0, 'max': 1.0, 'units': 'fraction'},
                'pressure': {'min': 0.0, 'max': 1.0e7, 'units': 'Pa'},
                'dead_time': {'min': 0.0, 'max': 60.0, 'units': 's'}
            },
            'applications': ['Stream mixing in chemical reactors', 'Flow diversion for different process units', 'Temperature control via hot/cold stream mixing', 'Bypass control systems', 'Product blending operations'],
            'limitations': ['Assumes incompressible flow', 'Linear flow coefficient splitting', 'Single-phase fluid only', 'No interaction between flow paths', 'Constant fluid properties assumed']
        }
