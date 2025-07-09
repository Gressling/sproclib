"""
PID Controller Implementation for SPROCLIB

This module provides an advanced PID controller with industrial features
including anti-windup, bumpless transfer, setpoint weighting, and derivative filtering.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class PIDController:
    """
    Advanced PID Controller implementation with anti-windup, bumpless transfer,
    setpoint weighting, and derivative filtering.
    
    Implementation with modern industrial features for robust process control.
    """
    
    def __init__(
        self,
        Kp: float = 1.0,
        Ki: float = 0.0,
        Kd: float = 0.0,
        MV_bar: float = 0.0,
        beta: float = 1.0,
        gamma: float = 0.0,
        N: float = 5.0,
        MV_min: float = 0.0,
        MV_max: float = 100.0,
        direct_action: bool = False
    ):
        """
        Initialize PID Controller.
        
        Args:
            Kp: Proportional gain
            Ki: Integral gain  
            Kd: Derivative gain
            MV_bar: Bias term for manipulated variable
            beta: Setpoint weighting for proportional term (0-1)
            gamma: Setpoint weighting for derivative term (0-1)
            N: Derivative filter parameter
            MV_min: Minimum output value
            MV_max: Maximum output value
            direct_action: If True, increase output for positive error
        """
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.MV_bar = MV_bar
        self.beta = beta
        self.gamma = gamma
        self.N = N
        self.MV_min = MV_min
        self.MV_max = MV_max
        self.direct_action = direct_action
        
        # Internal state variables
        self.reset()
    
    def reset(self):
        """Reset controller internal state."""
        self.t_prev = -100
        self.P = 0.0
        self.I = 0.0
        self.D = 0.0
        self.S = 0.0  # Derivative filter state
        self.MV = self.MV_bar
        self.error_prev = 0.0
        self.manual_mode = False
    
    def update(
        self, 
        t: float, 
        SP: float, 
        PV: float, 
        TR: Optional[float] = None
    ) -> float:
        """
        Update PID controller output.
        
        Args:
            t: Current time
            SP: Setpoint
            PV: Process variable (measurement)
            TR: Tracking signal for bumpless transfer (optional)
            
        Returns:
            MV: Manipulated variable output
        """
        dt = t - self.t_prev
        
        if dt <= 0:
            return self.MV
            
        # Bumpless transfer logic
        if TR is not None:
            self.I = TR - self.MV_bar - self.P - self.D
        
        # PID calculations
        error_P = self.beta * SP - PV
        error_I = SP - PV
        error_D = self.gamma * SP - PV
        
        # Proportional term
        self.P = self.Kp * error_P
        
        # Integral term with anti-windup
        self.I += self.Ki * error_I * dt
        
        # Derivative term with filtering
        self.D = self.N * self.Kp * (self.Kd * error_D - self.S) / (
            self.Kd + self.N * self.Kp * dt
        )
        
        # Calculate output
        action = 1.0 if self.direct_action else -1.0
        self.MV = self.MV_bar + action * (self.P + self.I + self.D)
        
        # Apply output limits and anti-windup
        MV_limited = np.clip(self.MV, self.MV_min, self.MV_max)
        self.I = MV_limited - self.MV_bar - action * (self.P + self.D)
        self.MV = MV_limited
        
        # Update derivative filter state
        self.S += self.D * dt
        
        # Store for next iteration
        self.t_prev = t
        self.error_prev = error_I
        
        return self.MV
    
    def set_auto_mode(self):
        """Switch to automatic mode."""
        self.manual_mode = False
    
    def set_manual_mode(self, mv_value: float):
        """Switch to manual mode with specified output."""
        self.manual_mode = True
        self.MV = np.clip(mv_value, self.MV_min, self.MV_max)
    
    def get_status(self) -> Dict[str, Any]:
        """Get controller status information."""
        return {
            'Kp': self.Kp,
            'Ki': self.Ki, 
            'Kd': self.Kd,
            'P': self.P,
            'I': self.I,
            'D': self.D,
            'MV': self.MV,
            'manual_mode': self.manual_mode
        }
