"""
Mock ProcessModel base class for testing transport models.

This mock allows testing the transport models without the full SPROCLIB dependency.
"""

import numpy as np
from abc import ABC, abstractmethod


class ProcessModel(ABC):
    """Mock abstract base class for process models."""
    
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
    
    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state outputs for given inputs.
        
        Args:
            u: Input variables
            
        Returns:
            Steady-state output variables
        """
        # Default implementation - should be overridden by subclasses
        return np.array([0.0])
    
    def simulate(self, t_span: tuple, x0: np.ndarray, u_func: callable = None):
        """
        Simulate the process model over time.
        
        Args:
            t_span: Time span (t_start, t_end)
            x0: Initial state
            u_func: Function returning inputs u(t)
            
        Returns:
            Simulation results
        """
        # Simple mock implementation
        return {'t': np.linspace(t_span[0], t_span[1], 100), 'x': np.array([x0])}
    
    def describe(self) -> dict:
        """
        Base describe method - can be overridden by subclasses.
        
        Returns:
            dict: Basic model information
        """
        return {
            'class_name': self.__class__.__name__,
            'name': self.name,
            'parameters': self.parameters,
            'state_variables': self.state_variables,
            'inputs': self.inputs,
            'outputs': self.outputs
        }
