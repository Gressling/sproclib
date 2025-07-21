"""
AMIGO Tuning Rule for SPROCLIB

This module provides the AMIGO (Approximate M-constrained Integral Gain Optimization)
tuning method for robust PID control.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from typing import Dict, Any
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
    
    def describe(self) -> Dict[str, Any]:
        """
        Comprehensive description of AMIGO tuning method.
        
        Returns:
            Dictionary containing detailed information about the AMIGO method,
            theory, robustness features, and chemical engineering applications.
        """
        return {
            'class_name': 'AMIGOTuning',
            'controller_type': self.controller_type,
            'description': 'AMIGO (Approximate M-constrained Integral Gain Optimization) tuning method',
            'purpose': 'Provides robust PID tuning with improved performance and robustness compared to classical methods',
            
            'historical_background': {
                'developers': 'Åström and Hägglund',
                'year_developed': '2004',
                'original_publication': 'Revisiting the Ziegler-Nichols step response method for PID control',
                'motivation': 'Address limitations of classical Ziegler-Nichols tuning',
                'key_innovation': 'Optimization-based approach with robustness constraints'
            },
            
            'theoretical_foundation': {
                'basis': 'Optimization of integral performance index with robustness constraints',
                'optimization_objective': 'Minimize IAE (Integral Absolute Error) for setpoint changes',
                'robustness_constraint': 'Maximum sensitivity Ms ≤ 1.4 (ensures good stability margins)',
                'model_assumptions': 'First-Order Plus Dead Time (FOPDT) process model',
                'design_philosophy': 'Balance between performance and robustness'
            },
            
            'mathematical_formulation': {
                'process_model': 'G(s) = K * exp(-θs) / (τs + 1)',
                'performance_index': 'J = ∫₀^∞ |e(t)| dt (IAE for unit step)',
                'robustness_measure': 'Ms = max|S(jω)| where S = 1/(1+GC)',
                'constraint': 'Ms ≤ 1.4 (6.1 dB gain margin, 51° phase margin)',
                'optimization_result': 'Analytical approximations for optimal parameters'
            },
            
            'tuning_formulas': {
                'PI_controller': {
                    'Kc': '(1/K) * (0.15 + 0.35*τ/θ - τ²/(θ+τ)²)',
                    'τI': '(0.35 + 13*τ²/(τ² + 12*θ*τ + 7*θ²)) * θ',
                    'Ki': 'Kc / τI',
                    'beta': '0 if θ < τ else 1 (setpoint weighting)',
                    'characteristics': [
                        'Robust to model uncertainties',
                        'Good disturbance rejection',
                        'Moderate setpoint tracking speed'
                    ]
                },
                'PID_controller': {
                    'Kc': '(1/K) * (0.2 + 0.45*τ/θ)',
                    'τI': '(0.4*θ + 0.8*τ)/(θ + 0.1*τ) * θ',
                    'τD': '0.5*θ*τ/(0.3*θ + τ)',
                    'beta': '0 if θ < τ else 1 (setpoint weighting)',
                    'gamma': '0 (derivative on measurement)',
                    'characteristics': [
                        'Faster response than PI',
                        'Excellent robustness properties',
                        'Reduced derivative kick'
                    ]
                }
            },
            
            'robustness_features': {
                'stability_margins': {
                    'gain_margin': '≥ 6.1 dB (factor of 2.0)',
                    'phase_margin': '≥ 51 degrees',
                    'maximum_sensitivity': '≤ 1.4',
                    'delay_margin': 'Substantial tolerance to modeling errors'
                },
                'uncertainty_handling': {
                    'gain_variations': 'Robust to ±50% gain changes',
                    'time_constant_errors': 'Tolerant to τ estimation errors',
                    'dead_time_variations': 'Good performance with θ uncertainties',
                    'model_structure': 'Works well even when FOPDT approximation is rough'
                }
            },
            
            'advantages_over_classical_methods': {
                'vs_ziegler_nichols': [
                    'Better robustness (guaranteed stability margins)',
                    'Less oscillatory response',
                    'Improved disturbance rejection',
                    'More conservative for challenging processes'
                ],
                'vs_cohen_coon': [
                    'Superior robustness properties',
                    'Less aggressive tuning',
                    'Better for processes with uncertainties',
                    'Reduced overshoot'
                ],
                'vs_imc_tuning': [
                    'No tuning parameter selection required',
                    'Automatic robustness guarantee',
                    'Optimized for specific performance index',
                    'Better theoretical foundation'
                ]
            },
            
            'chemical_engineering_applications': {
                'temperature_control_systems': {
                    'description': 'Reactor and heat exchanger temperature control',
                    'benefits': [
                        'Robust to heat transfer coefficient variations',
                        'Good performance despite thermal lag uncertainties',
                        'Reduced oscillations for better product quality'
                    ],
                    'typical_performance': 'Smooth temperature transitions with minimal overshoot',
                    'safety_considerations': 'Conservative tuning reduces risk of thermal runaway'
                },
                'composition_control': {
                    'description': 'Distillation column composition control',
                    'benefits': [
                        'Stable operation despite feed composition changes',
                        'Robust to tray efficiency variations',
                        'Good rejection of feed flow disturbances'
                    ],
                    'typical_performance': 'Tight composition control with good stability',
                    'economic_impact': 'Consistent product quality reduces reprocessing costs'
                },
                'pressure_control': {
                    'description': 'Vessel and pipeline pressure control',
                    'benefits': [
                        'Stable control despite equipment fouling',
                        'Robust to valve characteristic changes',
                        'Good performance over wide operating ranges'
                    ],
                    'typical_performance': 'Smooth pressure regulation without cycling',
                    'safety_considerations': 'Stable control reduces pressure excursions'
                },
                'flow_control_cascades': {
                    'description': 'Inner flow loops in cascade control systems',
                    'benefits': [
                        'Fast and stable flow control',
                        'Robust to pump characteristic changes',
                        'Good base for outer temperature/composition loops'
                    ],
                    'typical_performance': 'Quick setpoint tracking with minimal overshoot'
                }
            },
            
            'implementation_guidelines': {
                'model_identification': {
                    'step_test_requirements': 'Same as other FOPDT-based methods',
                    'data_quality': 'Good signal-to-noise ratio important',
                    'model_validation': 'Check model fit especially for τ/θ ratio',
                    'parameter_bounds': 'Method works best for 0.1 < θ/τ < 10'
                },
                'parameter_calculation': {
                    'numerical_stability': 'Formulas are well-conditioned',
                    'sign_handling': 'Automatically handles process gain sign',
                    'unit_consistency': 'Ensure time units match for τ and θ',
                    'bounds_checking': 'Verify realistic parameter values'
                },
                'commissioning_procedure': [
                    'Identify FOPDT model from step test',
                    'Calculate AMIGO parameters',
                    'Implement with setpoint weighting',
                    'Test with small setpoint changes',
                    'Verify disturbance rejection performance'
                ]
            },
            
            'performance_characteristics': {
                'setpoint_response': {
                    'overshoot': '< 5% typical (much less than Ziegler-Nichols)',
                    'settling_time': '4-8 time constants',
                    'rise_time': '2-4 time constants',
                    'iae_optimal': 'Minimized by design for step changes'
                },
                'disturbance_rejection': {
                    'load_disturbances': 'Excellent rejection with minimal overshoot',
                    'measurement_noise': 'Good filtering with derivative on measurement',
                    'model_uncertainties': 'Robust performance maintained',
                    'recovery_time': 'Smooth return to setpoint'
                },
                'actuator_activity': {
                    'control_effort': 'Moderate and smooth',
                    'derivative_kick': 'Eliminated with gamma = 0',
                    'valve_wear': 'Reduced due to smooth control action',
                    'energy_consumption': 'Efficient due to optimized response'
                }
            },
            
            'process_suitability': {
                'highly_suitable': [
                    'Processes with significant uncertainties',
                    'Safety-critical applications',
                    'Systems requiring robust operation',
                    'Processes with varying operating conditions',
                    'Applications where retuning is difficult'
                ],
                'moderately_suitable': [
                    'Very fast processes (may be conservative)',
                    'Processes requiring aggressive control',
                    'Systems with very small dead times',
                    'Applications prioritizing speed over robustness'
                ],
                'limitations': [
                    'Not applicable to integrating processes',
                    'May be conservative for well-modeled systems',
                    'Assumes linear process behavior',
                    'Requires FOPDT model identification'
                ]
            },
            
            'industrial_validation': {
                'documented_applications': [
                    'Pulp and paper industry temperature control',
                    'Chemical reactor control systems',
                    'Power plant process control',
                    'Food processing temperature control'
                ],
                'performance_studies': 'Consistently shows 20-40% improvement in robustness',
                'user_feedback': 'Reduced commissioning time and fewer retuning events',
                'reliability_improvements': 'More stable operation with less operator intervention'
            },
            
            'software_implementation': {
                'computational_requirements': 'Simple algebraic calculations',
                'real_time_feasibility': 'Suitable for all industrial control systems',
                'parameter_storage': 'Requires Kp, Ki, Kd, beta, gamma',
                'commissioning_tools': 'Can be integrated into controller configuration software'
            }
        }
