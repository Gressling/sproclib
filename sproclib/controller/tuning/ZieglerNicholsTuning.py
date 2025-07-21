"""
Ziegler-Nichols Tuning Rule for SPROCLIB

This module provides the classic Ziegler-Nichols tuning method for PID controllers.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from typing import Dict, Any
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
    
    def describe(self) -> Dict[str, Any]:
        """
        Comprehensive description of Ziegler-Nichols tuning method.
        
        Returns:
            Dictionary containing detailed information about the tuning method,
            theory, applications, and chemical engineering context.
        """
        return {
            'class_name': 'ZieglerNicholsTuning',
            'controller_type': self.controller_type,
            'description': 'Classic Ziegler-Nichols tuning method for PID controllers',
            'purpose': 'Provides systematic tuning rules based on FOPDT model parameters',
            
            'historical_background': {
                'developers': 'John G. Ziegler and Nathaniel B. Nichols',
                'year_developed': '1942',
                'original_publication': 'Optimum Settings for Automatic Controllers (Trans. ASME, 1942)',
                'significance': 'First systematic approach to PID tuning based on process dynamics',
                'impact': 'Most widely used tuning method in industrial control'
            },
            
            'tuning_theory': {
                'basis': 'First-Order Plus Dead Time (FOPDT) model approximation',
                'model_form': 'G(s) = K * exp(-θs) / (τs + 1)',
                'parameters': {
                    'K': 'Process gain (steady-state gain)',
                    'τ': 'Process time constant (how fast process responds)',
                    'θ': 'Process dead time (transport delay)'
                },
                'design_objective': 'Quarter decay ratio (25% overshoot decay per cycle)',
                'performance_criteria': [
                    'Fast response to setpoint changes',
                    'Reasonable stability margins',
                    'Moderate control effort'
                ]
            },
            
            'tuning_formulas': {
                'P_controller': {
                    'Kp': 'τ / (K * θ)',
                    'Ki': '0',
                    'Kd': '0',
                    'characteristics': ['No steady-state error for disturbances', 'Offset for setpoint changes']
                },
                'PI_controller': {
                    'Kp': '0.9 * τ / (K * θ)',
                    'Ki': 'Kp / (3.33 * θ)',
                    'Kd': '0',
                    'characteristics': ['No steady-state error', 'Slower than P controller', 'No derivative kick']
                },
                'PID_controller': {
                    'Kp': '1.2 * τ / (K * θ)',
                    'Ki': 'Kp / (2.0 * θ)',
                    'Kd': 'Kp * 0.5 * θ',
                    'characteristics': ['Fastest response', 'May be aggressive for some processes', 'Derivative kick possible']
                }
            },
            
            'applicability': {
                'suitable_processes': [
                    'Single-capacity processes (FOPDT approximation valid)',
                    'Processes with dominant time constant',
                    'Systems with moderate dead time (θ/τ < 1)',
                    'Temperature control loops',
                    'Flow control systems',
                    'Level control (non-integrating)'
                ],
                'less_suitable': [
                    'Integrating processes',
                    'Processes with large dead time (θ/τ > 1)',
                    'Highly oscillatory systems',
                    'Very fast processes',
                    'Systems with significant nonlinearity'
                ]
            },
            
            'chemical_engineering_applications': {
                'reactor_temperature_control': {
                    'description': 'CSTR temperature control using jacket cooling',
                    'typical_parameters': {
                        'K': '0.8-1.2 °C/% (gain from coolant to temperature)',
                        'τ': '5-20 minutes (thermal time constant)',
                        'θ': '0.5-3 minutes (sensor and valve delays)'
                    },
                    'tuning_considerations': [
                        'Conservative tuning for safety',
                        'Consider reactor thermal runaway',
                        'Account for coolant capacity limitations'
                    ]
                },
                'distillation_temperature_control': {
                    'description': 'Tray temperature control in distillation column',
                    'typical_parameters': {
                        'K': '1.5-3.0 °C/% (gain from reboiler to tray)',
                        'τ': '10-30 minutes (column hydraulic time constant)',
                        'θ': '2-8 minutes (measurement and actuator delays)'
                    },
                    'tuning_considerations': [
                        'Slower tuning for column stability',
                        'Consider tray holdup dynamics',
                        'Account for vapor-liquid equilibrium'
                    ]
                },
                'heat_exchanger_control': {
                    'description': 'Outlet temperature control of shell-and-tube heat exchanger',
                    'typical_parameters': {
                        'K': '0.5-1.5 °C/% (gain from utility to outlet)',
                        'τ': '2-10 minutes (thermal time constant)',
                        'θ': '0.2-2 minutes (transport and measurement delays)'
                    },
                    'tuning_considerations': [
                        'Fast response for good heat recovery',
                        'Consider fouling effects on dynamics',
                        'Account for utility temperature variations'
                    ]
                },
                'flow_control': {
                    'description': 'Flow rate control using control valve',
                    'typical_parameters': {
                        'K': '0.8-1.2 (dimensionless flow gain)',
                        'τ': '0.1-2 seconds (valve and piping dynamics)',
                        'θ': '0.05-0.5 seconds (measurement delays)'
                    },
                    'tuning_considerations': [
                        'Fast response required',
                        'Consider valve characteristics',
                        'Account for pressure drop variations'
                    ]
                }
            },
            
            'advantages': [
                'Simple and straightforward to apply',
                'Only requires FOPDT model identification',
                'Widely accepted in industry',
                'Good starting point for controller tuning',
                'Provides reasonable performance for many processes',
                'Well-documented and understood'
            ],
            
            'limitations': [
                'May produce aggressive tuning for some processes',
                'Not optimal for all performance criteria',
                'Based on quarter decay ratio objective',
                'May not provide best disturbance rejection',
                'Assumes FOPDT model adequacy',
                'Does not consider actuator limitations'
            ],
            
            'implementation_guidelines': {
                'model_identification': {
                    'step_test': 'Apply 5-15% step change to manipulated variable',
                    'data_requirements': 'Record response until new steady state',
                    'fitting_methods': ['Tangent method', 'Two-point method', 'Regression method'],
                    'validation': 'Check model accuracy with independent test'
                },
                'parameter_calculation': {
                    'units_consistency': 'Ensure consistent units for K, τ, θ',
                    'sign_convention': 'Use positive K for positive gain processes',
                    'dead_time_handling': 'Include all delays (measurement, valve, transport)'
                },
                'implementation_tips': [
                    'Start with PI tuning for most applications',
                    'Add derivative action only if needed',
                    'Consider detuning for robustness',
                    'Test with simulation before implementation'
                ]
            },
            
            'performance_expectations': {
                'setpoint_response': {
                    'overshoot': '25% for PID, less for PI',
                    'settling_time': '4-6 time constants',
                    'rise_time': '1-2 time constants'
                },
                'disturbance_rejection': {
                    'peak_deviation': 'Depends on disturbance magnitude',
                    'recovery_time': '3-5 time constants',
                    'steady_state_error': 'Zero for PI and PID'
                },
                'robustness': {
                    'gain_margin': '2-6 dB typical',
                    'phase_margin': '30-60 degrees typical',
                    'sensitivity': 'Moderate to model uncertainties'
                }
            },
            
            'comparison_with_alternatives': {
                'vs_cohen_coon': 'ZN more conservative, CC faster but less robust',
                'vs_lambda_tuning': 'ZN based on stability, Lambda based on speed',
                'vs_imc_tuning': 'ZN empirical, IMC model-based with filter',
                'vs_relay_tuning': 'ZN uses step test, Relay uses oscillation test'
            },
            
            'modern_enhancements': {
                'robust_zn': 'Modified formulas for better robustness',
                'adaptive_zn': 'Online parameter adjustment',
                'fuzzy_zn': 'Fuzzy logic enhancement of classical rules',
                'multivariable_zn': 'Extensions for MIMO systems'
            }
        }
