"""
AMIGO Tuning Rule for SPROCLIB

This module provides the AMIGO (Approximate M-constrained Integral Gain Optimization)
tuning method for robust PID control.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from typing import Dict
import logging
from ..base.TuningRule import TuningRule

logger = logging.getLogger(__name__)


class AMIGOTuning(TuningRule):
    """AMIGO tuning rules for robust PID control."""
    
    def __init__(self, controller_type: str = "PID"):
        """
        Initialize AMIGO tuning.
        
        Args:
            controller_type: "PI" or "PID"
        """
        self.controller_type = controller_type.upper()
        if self.controller_type not in ["PI", "PID"]:
            raise ValueError("controller_type must be 'PI' or 'PID'")
    
    def calculate_parameters(self, model_params: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate PID parameters using AMIGO tuning rules.
        
        Args:
            model_params: Must contain 'K', 'tau', 'theta' for FOPDT model
            
        Returns:
            Dictionary with 'Kp', 'Ki', 'Kd', 'beta', 'gamma' parameters
        """
        K = model_params['K']
        tau = model_params['tau']
        theta = model_params['theta']
        
        if self.controller_type == "PI":
            Kc = (1/K) * (0.15 + 0.35*tau/theta - tau**2/(theta + tau)**2)
            tau_I = (0.35 + 13*tau**2/(tau**2 + 12*theta*tau + 7*theta**2)) * theta
            Ki = Kc / tau_I
            beta = 0 if theta < tau else 1
            return {
                'Kp': Kc, 'Ki': Ki, 'Kd': 0.0,
                'beta': beta, 'gamma': 0.0
            }
        
        else:  # PID
            Kc = (1/K) * (0.2 + 0.45*tau/theta)
            tau_I = (0.4*theta + 0.8*tau)/(theta + 0.1*tau) * theta
            tau_D = 0.5*theta*tau/(0.3*theta + tau)
            Ki = Kc / tau_I
            Kd = Kc * tau_D
            beta = 0 if theta < tau else 1
            return {
                'Kp': Kc, 'Ki': Ki, 'Kd': Kd,
                'beta': beta, 'gamma': 0.0
            }
