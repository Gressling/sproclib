"""
Interacting Tanks Model for SPROCLIB

This module provides a model for two interacting tanks in series,
commonly used for studying process dynamics and control.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import logging
from ..base import ProcessModel

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
