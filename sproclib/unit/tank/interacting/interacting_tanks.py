"""
Interacting Tanks Model for SPROCLIB

This module provides a model for two interacting tanks in series,
commonly used for studying process dynamics and control.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import logging
from sproclib.unit.base import ProcessModel

logger = logging.getLogger(__name__)


class InteractingTanks(ProcessModel):
    """Two interacting tanks in series."""
    
    def __init__(
        self,
        A1: float = 1.0,
        A2: float = 1.0,
        C1: float = 1.0,
        C2: float = 1.0,
        name: str = "InteractingTanks"
    ):
        """
        Initialize interacting tanks model.
        
        Args:
            A1, A2: Cross-sectional areas [m²]
            C1, C2: Discharge coefficients [m²/min]
            name: Model name
        """
        super().__init__(name)
        self.A1 = A1
        self.A2 = A2
        self.C1 = C1
        self.C2 = C2
        self.parameters = {'A1': A1, 'A2': A2, 'C1': C1, 'C2': C2}
    
    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Interacting tanks dynamics:
        dh1/dt = (q_in - C1*sqrt(h1))/A1
        dh2/dt = (C1*sqrt(h1) - C2*sqrt(h2))/A2
        
        Args:
            t: Time
            x: [h1, h2] - tank heights
            u: [q_in] - inlet flow rate
            
        Returns:
            [dh1/dt, dh2/dt]
        """
        h1, h2 = x
        q_in = u[0]
        
        # Ensure heights are non-negative
        h1 = max(h1, 0.0)
        h2 = max(h2, 0.0)
        
        q12 = self.C1 * np.sqrt(h1)  # Flow from tank 1 to tank 2
        q_out = self.C2 * np.sqrt(h2)  # Outflow from tank 2
        
        dh1dt = (q_in - q12) / self.A1
        dh2dt = (q12 - q_out) / self.A2
        
        return np.array([dh1dt, dh2dt])
    
    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the InteractingTanks model including
                  algorithms, parameters, equations, and usage information.
        """
        return {
            'name': 'InteractingTanks',
            'class_name': 'InteractingTanks',
            'description': 'Two interacting tanks in series for process dynamics studies',
            'algorithm': 'Coupled nonlinear ODEs based on material balance for each tank',
            'equations': {
                'tank1_dynamics': 'dh1/dt = (q_in - C1*sqrt(h1))/A1',
                'tank2_dynamics': 'dh2/dt = (C1*sqrt(h1) - C2*sqrt(h2))/A2',
                'flow_12': 'q12 = C1*sqrt(h1)',
                'outlet_flow': 'q_out = C2*sqrt(h2)',
                'steady_state': 'h1_ss = (q_in/C1)², h2_ss = (q_in/C2)²'
            },
            'parameters': {
                'A1': {'description': 'Tank 1 cross-sectional area', 'units': 'm²', 'typical_range': '[0.1, 10]'},
                'A2': {'description': 'Tank 2 cross-sectional area', 'units': 'm²', 'typical_range': '[0.1, 10]'},
                'C1': {'description': 'Tank 1 discharge coefficient', 'units': 'm²/min', 'typical_range': '[0.01, 1]'},
                'C2': {'description': 'Tank 2 discharge coefficient', 'units': 'm²/min', 'typical_range': '[0.01, 1]'}
            },
            'state_variables': {
                'h1': 'Tank 1 height [m]',
                'h2': 'Tank 2 height [m]'
            },
            'inputs': {
                'q_in': 'Inlet flow rate to tank 1 [m³/min]'
            },
            'outputs': {
                'h1': 'Tank 1 height [m]',
                'h2': 'Tank 2 height [m]',
                'q12': 'Flow from tank 1 to tank 2 [m³/min]',
                'q_out': 'Outlet flow from tank 2 [m³/min]'
            },
            'typical_applications': [
                'Process dynamics studies',
                'Control system design',
                'Educational demonstrations',
                'Multi-tank level control systems'
            ],
            'working_ranges': {
                'height': {'min': 0.0, 'max': 10.0, 'units': 'm'},
                'flow_rate': {'min': 0.0, 'max': 5.0, 'units': 'm³/min'},
                'time_constants': {'typical': [2, 200], 'units': 'min'}
            },
            'assumptions': [
                'Incompressible fluid',
                'Constant cross-sectional areas',
                'Gravity-driven discharge',
                'Turbulent flow through outlets',
                'Perfect mixing in each tank'
            ],
            'limitations': [
                'Cannot handle negative heights',
                'Assumes steady discharge coefficients',
                'Neglects pipe dynamics between tanks'
            ]
        }

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Steady-state heights for interacting tanks.
        
        Args:
            u: [q_in] - inlet flow rate
            
        Returns:
            [h1_ss, h2_ss] - steady-state heights
        """
        q_in = u[0]
        
        # At steady state: q_in = C1*sqrt(h1) = C2*sqrt(h2)
        h2_ss = (q_in / self.C2) ** 2
        h1_ss = (q_in / self.C1) ** 2
        
        return np.array([h1_ss, h2_ss])
