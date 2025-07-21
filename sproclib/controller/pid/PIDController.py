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
    
    def describe(self) -> Dict[str, Any]:
        """
        Comprehensive description of the PID Controller.
        
        Returns:
            Dictionary containing detailed information about the PID controller,
            its parameters, current state, tuning characteristics, and industrial applications.
        """
        return {
            'class_name': 'PIDController',
            'description': 'Industrial-grade PID (Proportional-Integral-Derivative) Controller with advanced features',
            'purpose': 'Provides robust feedback control for single-input single-output (SISO) processes in chemical plants',
            
            'controller_parameters': {
                'proportional_gain': {
                    'value': self.Kp,
                    'symbol': 'Kp',
                    'units': 'dimensionless',
                    'description': 'Controls speed of response to current error',
                    'typical_range': '0.1 to 10.0',
                    'effect': 'Higher values increase response speed but may cause overshoot'
                },
                'integral_gain': {
                    'value': self.Ki,
                    'symbol': 'Ki',
                    'units': '1/s',
                    'description': 'Eliminates steady-state error by integrating past errors',
                    'typical_range': '0.01 to 1.0',
                    'effect': 'Higher values reduce steady-state error but may cause oscillations'
                },
                'derivative_gain': {
                    'value': self.Kd,
                    'symbol': 'Kd',
                    'units': 's',
                    'description': 'Provides predictive action based on error rate of change',
                    'typical_range': '0.1 to 10.0',
                    'effect': 'Higher values improve stability but amplify measurement noise'
                }
            },
            
            'advanced_features': {
                'setpoint_weighting': {
                    'beta': {
                        'value': self.beta,
                        'range': '0.0 to 1.0',
                        'description': 'Proportional setpoint weight (0 = derivative kick, 1 = no weighting)',
                        'industrial_benefit': 'Prevents derivative kick during setpoint changes'
                    },
                    'gamma': {
                        'value': self.gamma,
                        'range': '0.0 to 1.0',
                        'description': 'Derivative setpoint weight',
                        'industrial_benefit': 'Reduces controller output spikes during setpoint changes'
                    }
                },
                'derivative_filtering': {
                    'filter_constant': {
                        'value': self.N,
                        'typical_range': '5 to 20',
                        'description': 'Derivative filter constant to reduce high-frequency noise',
                        'industrial_benefit': 'Essential for noisy process measurements'
                    }
                },
                'output_limiting': {
                    'min_output': self.MV_min,
                    'max_output': self.MV_max,
                    'bias': self.MV_bar,
                    'description': 'Prevents actuator saturation and integrator windup',
                    'industrial_benefit': 'Protects equipment and maintains stable operation'
                },
                'anti_windup': {
                    'method': 'Back-calculation',
                    'description': 'Prevents integral term buildup when output is saturated',
                    'industrial_benefit': 'Maintains controller performance during constraints'
                }
            },
            
            'current_state': {
                'proportional_term': self.P,
                'integral_term': self.I,
                'derivative_term': self.D,
                'total_output': self.MV,
                'mode': 'Manual' if self.manual_mode else 'Automatic',
                'last_update_time': self.t_prev
            },
            
            'industrial_applications': {
                'temperature_control': {
                    'description': 'Reactor temperature control using heating/cooling jackets',
                    'typical_parameters': 'Kp=0.5-2.0, Ki=0.1-0.5, Kd=0.1-1.0',
                    'considerations': 'Thermal lag requires careful derivative tuning'
                },
                'pressure_control': {
                    'description': 'Vessel pressure control using vent valves or compressors',
                    'typical_parameters': 'Kp=1.0-5.0, Ki=0.2-1.0, Kd=0.05-0.5',
                    'considerations': 'Fast dynamics, avoid aggressive derivative action'
                },
                'flow_control': {
                    'description': 'Mass/volumetric flow control using control valves',
                    'typical_parameters': 'Kp=0.5-3.0, Ki=1.0-5.0, Kd=0.0-0.2',
                    'considerations': 'Fast process, minimal derivative action needed'
                },
                'level_control': {
                    'description': 'Tank level control using inlet/outlet flow manipulation',
                    'typical_parameters': 'Kp=0.1-1.0, Ki=0.01-0.1, Kd=0.0-0.5',
                    'considerations': 'Integrating process, conservative tuning required'
                },
                'composition_control': {
                    'description': 'Product composition control in reactors and separators',
                    'typical_parameters': 'Kp=0.2-2.0, Ki=0.05-0.3, Kd=0.1-2.0',
                    'considerations': 'Large time delays, derivative action beneficial'
                }
            },
            
            'tuning_guidelines': {
                'ziegler_nichols': 'Classic frequency response method',
                'cohen_coon': 'Good for processes with time delays',
                'lambda_tuning': 'Provides specified closed-loop time constant',
                'ime_tuning': 'Minimizes integrated error criteria',
                'aggressive_conservative': 'Dual-mode tuning based on error magnitude'
            },
            
            'performance_metrics': {
                'rise_time': 'Time to reach 90% of setpoint',
                'settling_time': 'Time to stay within ±2% of setpoint',
                'overshoot': 'Maximum deviation above setpoint (%)',
                'steady_state_error': 'Final tracking error',
                'integral_error_criteria': ['IAE', 'ISE', 'ITAE', 'ITSE']
            },
            
            'implementation_notes': {
                'sampling_time': 'Should be 5-10 times faster than process time constant',
                'derivative_kick': 'Eliminated through setpoint weighting (beta < 1)',
                'integral_windup': 'Prevented through back-calculation method',
                'noise_sensitivity': 'Derivative term filtered with time constant 1/(N*Kp)',
                'bumpless_transfer': 'Supported through tracking signal (TR)'
            },
            
            'safety_considerations': {
                'fail_safe_action': 'Define safe output value for controller failure',
                'rate_limiting': 'Consider adding rate limits for valve protection',
                'emergency_override': 'Manual mode available for emergency situations',
                'alarm_limits': 'Set process variable deviation alarms',
                'backup_control': 'Consider redundant controllers for critical loops'
            }
        }
