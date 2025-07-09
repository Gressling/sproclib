"""
Base classes for SPROCLIB - Standard Process Control Library

This module provides the abstract base class for all process models.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import logging
from typing import Optional, Tuple, Dict, Any, List, Callable
from abc import ABC, abstractmethod
from scipy.integrate import solve_ivp

logger = logging.getLogger(__name__)


class ProcessModel(ABC):
    """Abstract base class for process models."""
    
    def __init__(self, name: str = "ProcessModel"):
        """
        Initialize process model.
        
        Args:
            name: Model name for identification
        """
        self.name = name
        self.parameters = {}
        self.state_variables = {}
        self.inputs = {}
        self.outputs = {}
    
    @abstractmethod
    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Define the process dynamics dx/dt = f(t, x, u).
        
        Args:
            t: Time
            x: State variables
            u: Input variables
            
        Returns:
            State derivatives dx/dt
        """
        pass
    
    @abstractmethod
    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state values for given inputs.
        
        Args:
            u: Input variables
            
        Returns:
            Steady-state values
        """
        pass
    
    def simulate(
        self, 
        t_span: Tuple[float, float],
        x0: np.ndarray,
        u_func: Callable[[float], np.ndarray],
        t_eval: Optional[np.ndarray] = None
    ) -> Dict[str, np.ndarray]:
        """
        Simulate the process model.
        
        Args:
            t_span: Time span (t_start, t_end)
            x0: Initial conditions
            u_func: Function returning inputs as function of time
            t_eval: Time points for output (optional)
            
        Returns:
            Dictionary with 't', 'x', 'u' arrays
        """
        def rhs(t, x):
            u = u_func(t)
            return self.dynamics(t, x, u)
        
        sol = solve_ivp(rhs, t_span, x0, t_eval=t_eval, dense_output=True)
        
        if t_eval is None:
            t_eval = sol.t
        
        u_values = np.array([u_func(t) for t in t_eval])
        
        return {
            't': t_eval,
            'x': sol.sol(t_eval),
            'u': u_values.T
        }
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get model information summary.
        
        Returns:
            Dictionary with model information
        """
        return {
            'name': self.name,
            'type': self.__class__.__name__,
            'parameters': self.parameters,
            'n_states': len(self.state_variables),
            'n_inputs': len(self.inputs),
            'n_outputs': len(self.outputs)
        }
    
    def update_parameters(self, **kwargs):
        """
        Update model parameters.
        
        Args:
            **kwargs: Parameter updates
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                self.parameters[key] = value
            else:
                logger.warning(f"Parameter '{key}' not found in model '{self.name}'")
