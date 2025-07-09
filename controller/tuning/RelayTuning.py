"""
Relay Tuning Method for SPROCLIB

This module provides relay auto-tuning for PID controllers using the
relay feedback method.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
from typing import Dict
import logging
from ..base.TuningRule import TuningRule

logger = logging.getLogger(__name__)


class RelayTuning(TuningRule):
    """Relay tuning method for PID controllers."""
    
    def __init__(self, relay_amplitude: float = 1.0):
        """
        Initialize relay tuning.
        
        Args:
            relay_amplitude: Amplitude of relay signal
        """
        self.relay_amplitude = relay_amplitude
    
    def calculate_parameters(self, model_params: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate PID parameters from relay test results.
        
        Args:
            model_params: Must contain 'Pu' (ultimate period), 'a' (amplitude)
            
        Returns:
            Dictionary with 'Kp', 'Ki', 'Kd' parameters
        """
        Pu = model_params['Pu']  # Ultimate period
        a = model_params['a']    # Process amplitude response
        h = self.relay_amplitude
        
        # Calculate ultimate gain
        Ku = 4 * h / (np.pi * a)
        
        # Apply Ziegler-Nichols ultimate cycling rules
        Kp = Ku / 2.0
        Ki = Kp / (Pu / 2.0)
        Kd = Kp * (Pu / 8.0)
        
        return {'Kp': Kp, 'Ki': Ki, 'Kd': Kd}
