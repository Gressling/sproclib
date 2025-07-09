"""
Single Tank Model

This module provides a gravity-drained tank model for level control applications.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import logging
from typing import Optional, Tuple, Dict, Any
from ..base import ProcessModel

logger = logging.getLogger(__name__)


class Tank(ProcessModel):
    """Gravity-drained tank model."""
    
    def __init__(
        self,
        A: float = 1.0,
        C: float = 1.0,
        name: str = "GravityTank"
    ):
        """
        Initialize gravity-drained tank.
        
        Args:
            A: Cross-sectional area [m²]
            C: Discharge coefficient [m²/min]
            name: Model name
        """
        super().__init__(name)
        self.A = A
        self.C = C
        self.parameters = {'A': A, 'C': C}
        
        # Define state and input variables
        self.state_variables = {
            'h': 'Tank height [m]'
        }
        
        self.inputs = {
            'q_in': 'Inlet flow rate [m³/min]'
        }
        
        self.outputs = {
            'h': 'Tank height [m]',
            'q_out': 'Outlet flow rate [m³/min]',
            'volume': 'Tank volume [m³]'
        }
    
    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Tank dynamics: dh/dt = (q_in - C*sqrt(h))/A
        
        Args:
            t: Time
            x: [height]
            u: [q_in] - inlet flow rate
            
        Returns:
            [dh/dt]
        """
        h = x[0]
        q_in = u[0]
        
        # Ensure height is non-negative
        h = max(h, 0.0)
        
        dhdt = (q_in - self.C * np.sqrt(h)) / self.A
        return np.array([dhdt])
    
    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Steady-state height: h = (q_in/C)²
        
        Args:
            u: [q_in] - inlet flow rate
            
        Returns:
            [h_ss] - steady-state height
        """
        q_in = u[0]
        h_ss = (q_in / self.C) ** 2
        return np.array([h_ss])
    
    def calculate_outlet_flow(self, h: float) -> float:
        """
        Calculate outlet flow rate based on tank height.
        
        Args:
            h: Tank height [m]
            
        Returns:
            Outlet flow rate [m³/min]
        """
        return self.C * np.sqrt(max(0.0, h))
    
    def calculate_volume(self, h: float) -> float:
        """
        Calculate tank volume based on height.
        
        Args:
            h: Tank height [m]
            
        Returns:
            Tank volume [m³]
        """
        return self.A * max(0.0, h)
    
    def calculate_time_constant(self, h_op: float) -> float:
        """
        Calculate linearized time constant at operating point.
        
        Args:
            h_op: Operating height [m]
            
        Returns:
            Time constant [min]
        """
        if h_op > 0:
            # τ = 2*A*sqrt(h)/C
            return 2 * self.A * np.sqrt(h_op) / self.C
        return float('inf')
    
    def get_performance_metrics(self, x: np.ndarray, u: np.ndarray) -> Dict[str, float]:
        """
        Calculate performance metrics.
        
        Args:
            x: [h] - current height
            u: [q_in] - inlet flow
            
        Returns:
            Dictionary with performance metrics
        """
        h = x[0]
        q_in = u[0]
        
        q_out = self.calculate_outlet_flow(h)
        volume = self.calculate_volume(h)
        time_constant = self.calculate_time_constant(h)
        
        # Mass balance error (should be zero at steady state)
        mass_balance_error = q_in - q_out
        
        return {
            'height': h,
            'outlet_flow': q_out,
            'volume': volume,
            'time_constant': time_constant,
            'mass_balance_error': mass_balance_error,
            'residence_time': volume / q_out if q_out > 0 else float('inf')
        }
