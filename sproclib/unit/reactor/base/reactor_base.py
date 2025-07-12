"""
Reactor Base Class

This module provides the base class for all reactor models in SPROCLIB.
It defines the common interface and shared functionality.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
import logging

logger = logging.getLogger(__name__)


class ReactorBase(ABC):
    """
    Abstract base class for all reactor models.
    
    Provides common interface and shared functionality for reactor modeling
    including state variables, parameters, and standard methods.
    """
    
    def __init__(self, name: str = "Reactor"):
        """
        Initialize base reactor.
        
        Args:
            name: Reactor name/identifier
        """
        self.name = name
        self.parameters = {}
        self.state_variables = []
        self.inputs = []
        self.outputs = []
        
        # Logging setup
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
    
    @abstractmethod
    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Calculate reactor dynamics dx/dt = f(t, x, u).
        
        Args:
            t: Time
            x: State vector
            u: Input vector
            
        Returns:
            State derivatives dx/dt
        """
        pass
    
    def simulate(self, t_final: float = 60.0, dt: float = 0.1, 
                 x0: Optional[np.ndarray] = None, 
                 u_profile: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Simulate reactor dynamics over time.
        
        Args:
            t_final: Final simulation time
            dt: Time step
            x0: Initial state
            u_profile: Input profile over time
            
        Returns:
            Dictionary with simulation results
        """
        from scipy.integrate import odeint
        
        # Time vector
        t = np.arange(0, t_final + dt, dt)
        n_steps = len(t)
        
        # Default initial conditions
        if x0 is None:
            x0 = np.zeros(len(self.state_variables))
        
        # Default input profile (zeros)
        if u_profile is None:
            u_profile = np.zeros((n_steps, len(self.inputs)))
        elif u_profile.ndim == 1:
            u_profile = u_profile.reshape(-1, 1)
        
        # Integrate
        def ode_func(state, time_val):
            # Find closest time index for input
            idx = np.argmin(np.abs(t - time_val))
            u_current = u_profile[idx] if len(u_profile) > idx else u_profile[-1]
            return self.dynamics(time_val, state, u_current)
        
        try:
            solution = odeint(ode_func, x0, t)
        except Exception as e:
            self.logger.error(f"Integration failed: {e}")
            raise
        
        return {
            'time': t,
            'states': solution,
            'inputs': u_profile
        }
    
    def step(self, x: np.ndarray, u: np.ndarray, dt: float = 0.1) -> np.ndarray:
        """
        Single time step integration.
        
        Args:
            x: Current state
            u: Current input
            dt: Time step
            
        Returns:
            Next state
        """
        # Simple Euler integration
        dxdt = self.dynamics(0, x, u)
        return x + dt * dxdt
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get reactor information.
        
        Returns:
            Dictionary with reactor metadata
        """
        return {
            'name': self.name,
            'type': self.__class__.__name__,
            'state_variables': self.state_variables,
            'inputs': self.inputs,
            'outputs': self.outputs,
            'parameters': self.parameters
        }
    
    def update_parameters(self, **kwargs):
        """
        Update reactor parameters.
        
        Args:
            **kwargs: Parameter name-value pairs
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                self.parameters[key] = value
            else:
                self.logger.warning(f"Unknown parameter: {key}")
    
    def validate_inputs(self, x: np.ndarray, u: np.ndarray) -> tuple:
        """
        Validate and sanitize inputs.
        
        Args:
            x: State vector
            u: Input vector
            
        Returns:
            Validated (x, u) tuple
        """
        # Ensure proper array format
        x = np.atleast_1d(x)
        u = np.atleast_1d(u)
        
        # Check dimensions
        if len(x) != len(self.state_variables):
            raise ValueError(f"State vector size {len(x)} != expected {len(self.state_variables)}")
        
        if len(u) != len(self.inputs):
            self.logger.warning(f"Input vector size {len(u)} != expected {len(self.inputs)}")
        
        return x, u
    
    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(name='{self.name}')"
    
    def __str__(self) -> str:
        """Human-readable string."""
        return f"{self.name} ({self.__class__.__name__})"
