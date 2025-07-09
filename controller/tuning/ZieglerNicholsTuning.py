"""
Ziegler-Nichols Tuning Rule for SPROCLIB

This module provides the classic Ziegler-Nichols tuning method for PID controllers.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from typing import Dict
import logging
from ..base.TuningRule import TuningRule

logger = logging.getLogger(__name__)


class ZieglerNicholsTuning(TuningRule):
    """Ziegler-Nichols tuning rules for PID controllers."""
    
    def __init__(self, controller_type: str = "PID"):
        """
        Initialize Ziegler-Nichols tuning.
        
        Args:
            controller_type: "P", "PI", or "PID"
        """
        self.controller_type = controller_type.upper()
        if self.controller_type not in ["P", "PI", "PID"]:
            raise ValueError("controller_type must be 'P', 'PI', or 'PID'")
    
    def calculate_parameters(self, model_params: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate PID parameters using Ziegler-Nichols tuning rules.
        
        Args:
            model_params: Must contain 'K', 'tau', 'theta' for FOPDT model
            
        Returns:
            Dictionary with 'Kp', 'Ki', 'Kd' parameters
        """
        K = model_params['K']
        tau = model_params['tau'] 
        theta = model_params['theta']
        
        if self.controller_type == "P":
            Kp = tau / (K * theta)
            return {'Kp': Kp, 'Ki': 0.0, 'Kd': 0.0}
        
        elif self.controller_type == "PI":
            Kp = 0.9 * tau / (K * theta)
            Ki = Kp / (3.33 * theta)
            return {'Kp': Kp, 'Ki': Ki, 'Kd': 0.0}
        
        else:  # PID
            Kp = 1.2 * tau / (K * theta)
            Ki = Kp / (2.0 * theta)
            Kd = Kp * 0.5 * theta
            return {'Kp': Kp, 'Ki': Ki, 'Kd': Kd}
