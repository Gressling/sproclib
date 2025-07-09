"""
Linearization Utilities for SPROCLIB

This module provides utilities for linearizing nonlinear process models
around operating points for linear control design.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import logging
from typing import Optional, Tuple, Dict, Any
from ..base import ProcessModel

logger = logging.getLogger(__name__)


class LinearApproximation:
    """Linear approximation of nonlinear process models."""
    
    def __init__(self, model: ProcessModel):
        """
        Initialize linearization utility.
        
        Args:
            model: Nonlinear process model to linearize
        """
        self.model = model
        self.A = None  # State matrix
        self.B = None  # Input matrix
        self.C = None  # Output matrix
        self.D = None  # Feedthrough matrix
        self.x_ss = None  # Steady-state states
        self.u_ss = None  # Steady-state inputs
    
    def linearize(
        self,
        u_ss: np.ndarray,
        x_ss: Optional[np.ndarray] = None,
        epsilon: float = 1e-6
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Linearize model around operating point using finite differences.
        
        Args:
            u_ss: Steady-state inputs
            x_ss: Steady-state states (calculated if None)
            epsilon: Perturbation size for finite differences
            
        Returns:
            A, B matrices for linear model dx/dt = A*x + B*u
        """
        if x_ss is None:
            x_ss = self.model.steady_state(u_ss)
        
        self.u_ss = u_ss
        self.x_ss = x_ss
        
        n_states = len(x_ss)
        n_inputs = len(u_ss)
        
        # Calculate A matrix (∂f/∂x)
        A = np.zeros((n_states, n_states))
        f0 = self.model.dynamics(0, x_ss, u_ss)
        
        for i in range(n_states):
            x_pert = x_ss.copy()
            x_pert[i] += epsilon
            f_pert = self.model.dynamics(0, x_pert, u_ss)
            A[:, i] = (f_pert - f0) / epsilon
        
        # Calculate B matrix (∂f/∂u)
        B = np.zeros((n_states, n_inputs))
        
        for i in range(n_inputs):
            u_pert = u_ss.copy()
            u_pert[i] += epsilon
            f_pert = self.model.dynamics(0, x_ss, u_pert)
            B[:, i] = (f_pert - f0) / epsilon
        
        self.A = A
        self.B = B
        
        return A, B
    
    def get_transfer_function(
        self,
        output_idx: int = 0,
        input_idx: int = 0,
        s_values: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """
        Get transfer function from linearized model.
        
        Args:
            output_idx: Output variable index
            input_idx: Input variable index
            s_values: Frequency values for evaluation
            
        Returns:
            Dictionary with transfer function information
        """
        if self.A is None or self.B is None:
            raise ValueError("Model must be linearized first")
        
        # For single-input single-output case
        # G(s) = C*(sI - A)^(-1)*B + D
        # Assuming C = I (output = states) and D = 0
        
        if s_values is None:
            s_values = np.logspace(-2, 2, 100) * 1j
        
        G_values = []
        for s in s_values:
            try:
                sI_A_inv = np.linalg.inv(s * np.eye(len(self.A)) - self.A)
                G = sI_A_inv @ self.B
                G_values.append(G[output_idx, input_idx])
            except:
                G_values.append(np.nan)
        
        return {
            'frequency': s_values,
            'response': np.array(G_values),
            'A': self.A,
            'B': self.B,
            'steady_state': {'x': self.x_ss, 'u': self.u_ss}
        }
    
    def step_response(
        self,
        input_idx: int = 0,
        step_size: float = 1.0,
        t_final: float = 10.0,
        n_points: int = 100
    ) -> Dict[str, np.ndarray]:
        """
        Calculate step response of linearized model.
        
        Args:
            input_idx: Input index for step
            step_size: Magnitude of step
            t_final: Final time
            n_points: Number of time points
            
        Returns:
            Dictionary with time and response arrays
        """
        if self.A is None or self.B is None:
            raise ValueError("Model must be linearized first")
        
        from scipy.linalg import expm
        
        t = np.linspace(0, t_final, n_points)
        response = np.zeros((len(self.x_ss), n_points))
        
        # Step input vector
        u_step = np.zeros(len(self.u_ss))
        u_step[input_idx] = step_size
        
        for i, ti in enumerate(t):
            if ti == 0:
                response[:, i] = 0
            else:
                # x(t) = exp(A*t) * x0 + integral(exp(A*(t-tau)) * B * u, tau=0..t)
                # For step input: x(t) = A^(-1) * (exp(A*t) - I) * B * u
                try:
                    eAt = expm(self.A * ti)
                    A_inv_B_u = np.linalg.solve(self.A, self.B @ u_step)
                    response[:, i] = (eAt - np.eye(len(self.A))) @ A_inv_B_u
                except:
                    # If A is singular, use numerical integration
                    response[:, i] = response[:, i-1] if i > 0 else 0
        
        return {
            't': t,
            'x': response,
            'u_step': u_step
        }
