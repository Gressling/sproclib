"""
Relay Tuning Method for SPROCLIB

This module provides relay auto-tuning for PID controllers using the
relay feedback method.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
from typing import Dict, Any
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
    
    def describe(self) -> Dict[str, Any]:
        """
        Comprehensive description of relay tuning method.
        
        Returns:
            Dictionary containing detailed information about relay auto-tuning,
            theory, implementation, and chemical engineering applications.
        """
        return {
            'class_name': 'RelayTuning',
            'relay_amplitude': self.relay_amplitude,
            'description': 'Relay auto-tuning method for automatic PID controller tuning',
            'purpose': 'Determines ultimate gain and period through controlled oscillation test',
            
            'historical_background': {
                'developer': 'Karl Johan Åström and Tore Hägglund',
                'year_developed': '1984',
                'original_publication': 'Automatic Tuning of Simple Regulators with Specifications on Phase and Amplitude Margins',
                'innovation': 'First practical auto-tuning method for industrial controllers',
                'impact': 'Enabled automatic tuning in commercial PID controllers'
            },
            
            'theoretical_foundation': {
                'principle': 'Relay feedback creates controlled limit cycle oscillation',
                'frequency_domain_analysis': 'Process operates at critical frequency where phase = -180°',
                'describing_function': 'Relay characterized by describing function N = 4h/(πa)',
                'critical_point': 'Intersection of -1/N and process frequency response',
                'ultimate_parameters': {
                    'Ku': 'Ultimate gain = 4h/(πa)',
                    'Pu': 'Ultimate period from oscillation measurement',
                    'ωu': 'Ultimate frequency = 2π/Pu'
                }
            },
            
            'relay_test_procedure': {
                'setup': {
                    'controller_mode': 'Switch PID controller to manual mode',
                    'initial_condition': 'Bring process to steady state',
                    'relay_implementation': 'Replace controller output with relay',
                    'safety_considerations': 'Ensure oscillations are within safe limits'
                },
                'test_execution': {
                    'relay_logic': 'u = +h if e > 0 else -h',
                    'amplitude_selection': 'h = 5-15% of normal operating range',
                    'data_collection': 'Record process output and time',
                    'termination_criteria': '3-5 complete oscillation cycles'
                },
                'data_analysis': {
                    'period_measurement': 'Pu = time between consecutive peaks',
                    'amplitude_measurement': 'a = peak-to-peak amplitude / 2',
                    'phase_verification': 'Check 180° phase shift at oscillation',
                    'noise_filtering': 'Use averaging over multiple cycles'
                }
            },
            
            'parameter_calculation': {
                'ultimate_gain': {
                    'formula': 'Ku = 4h / (πa)',
                    'physical_meaning': 'Proportional gain at stability boundary',
                    'units': 'Same as process gain units⁻¹',
                    'sensitivity': 'Sensitive to relay amplitude and measurement accuracy'
                },
                'ziegler_nichols_rules': {
                    'P_controller': {'Kp': '0.5 * Ku', 'Ti': '∞', 'Td': '0'},
                    'PI_controller': {'Kp': '0.45 * Ku', 'Ti': 'Pu / 1.2', 'Td': '0'},
                    'PID_controller': {'Kp': '0.6 * Ku', 'Ti': 'Pu / 2', 'Td': 'Pu / 8'},
                    'alternative_rules': 'Tyreus-Luyben, Refined ZN, etc.'
                }
            },
            
            'advantages': [
                'No process model required',
                'Automatic and objective tuning',
                'Works with nonlinear processes',
                'Identifies critical process information',
                'Can be implemented online',
                'Minimal operator intervention',
                'Works for various process types',
                'Provides repeatable results'
            ],
            
            'limitations': [
                'Requires process to oscillate (may not be acceptable)',
                'Assumes process can tolerate limit cycles',
                'May take significant time for slow processes',
                'Sensitive to measurement noise',
                'Limited to processes with integrating behavior or steady state',
                'May not work with very fast processes',
                'Requires sufficient process gain'
            ],
            
            'chemical_engineering_applications': {
                'temperature_control': {
                    'description': 'Reactor and heat exchanger temperature control',
                    'considerations': [
                        'Thermal inertia allows controlled oscillations',
                        'Temperature sensors have adequate response time',
                        'Oscillations within safety limits for reactions'
                    ],
                    'typical_results': {
                        'test_duration': '30-120 minutes depending on thermal time constant',
                        'oscillation_amplitude': '±2-5°C typical',
                        'tuning_quality': 'Good for processes with dominant time constant'
                    }
                },
                'flow_control': {
                    'description': 'Flow rate control with control valves',
                    'considerations': [
                        'Fast process dynamics require high sampling rate',
                        'Flow measurements have adequate resolution',
                        'Valve characteristics affect relay response'
                    ],
                    'typical_results': {
                        'test_duration': '1-5 minutes for liquid flows',
                        'oscillation_amplitude': '±5-15% of nominal flow',
                        'tuning_quality': 'Excellent for linear valve characteristics'
                    }
                },
                'level_control': {
                    'description': 'Tank and vessel level control',
                    'considerations': [
                        'Integrating process behavior suitable for relay test',
                        'Level range allows for oscillations',
                        'Inflow/outflow capacity adequate for test'
                    ],
                    'typical_results': {
                        'test_duration': '10-60 minutes depending on tank size',
                        'oscillation_amplitude': '±5-20% of normal level range',
                        'tuning_quality': 'Good for averaging level control'
                    }
                },
                'pressure_control': {
                    'description': 'Gas pressure control systems',
                    'considerations': [
                        'Pressure oscillations within equipment limits',
                        'Gas dynamics affect oscillation quality',
                        'Compressibility effects on relay response'
                    ],
                    'typical_results': {
                        'test_duration': '5-30 minutes depending on volume',
                        'oscillation_amplitude': '±2-10% of operating pressure',
                        'tuning_quality': 'Good for gas systems with proper relay sizing'
                    }
                }
            },
            
            'implementation_considerations': {
                'relay_amplitude_selection': {
                    'guidelines': '5-15% of normal manipulated variable range',
                    'too_small': 'Poor signal-to-noise ratio, inaccurate results',
                    'too_large': 'Nonlinear effects, safety concerns',
                    'adaptive': 'Some methods automatically adjust amplitude'
                },
                'measurement_requirements': {
                    'sampling_rate': '10-20 times faster than expected oscillation',
                    'resolution': 'Adequate to detect oscillation amplitude',
                    'noise_level': 'Should be much smaller than oscillation',
                    'filtering': 'Anti-aliasing and noise filtering may be needed'
                },
                'safety_considerations': {
                    'oscillation_limits': 'Ensure oscillations within safe operating range',
                    'emergency_stop': 'Ability to abort test immediately',
                    'process_stability': 'Verify process can return to normal operation',
                    'operator_supervision': 'Continuous monitoring during test'
                },
                'test_validation': {
                    'oscillation_quality': 'Check for clean, symmetric oscillations',
                    'period_consistency': 'Verify consistent period across cycles',
                    'amplitude_stability': 'Check for stable oscillation amplitude',
                    'phase_relationship': 'Confirm proper phase between input and output'
                }
            },
            
            'modern_enhancements': {
                'relay_variants': {
                    'hysteresis_relay': 'Reduces chatter in presence of noise',
                    'preload_relay': 'Improves test for processes with deadband',
                    'dual_relay': 'Separate amplitude for positive and negative',
                    'variable_amplitude': 'Adaptive amplitude during test'
                },
                'advanced_analysis': {
                    'fourier_analysis': 'Frequency domain analysis of oscillation',
                    'multiple_points': 'Identify multiple frequency response points',
                    'model_fitting': 'Fit process model from relay test data',
                    'robustness_analysis': 'Assess tuning robustness'
                },
                'automation_features': {
                    'automatic_detection': 'Automated oscillation detection and analysis',
                    'parameter_validation': 'Automatic verification of results',
                    'safety_monitoring': 'Automatic abort on safety violations',
                    'report_generation': 'Automatic tuning report and recommendations'
                }
            },
            
            'comparison_with_alternatives': {
                'vs_step_test': {
                    'advantages': 'No model fitting required, works with nonlinear processes',
                    'disadvantages': 'Requires oscillation, may take longer'
                },
                'vs_frequency_response': {
                    'advantages': 'Simpler implementation, single test',
                    'disadvantages': 'Less frequency information, assumes linearity'
                },
                'vs_closed_loop_methods': {
                    'advantages': 'Direct identification of critical information',
                    'disadvantages': 'Open-loop test, requires manual intervention'
                }
            },
            
            'troubleshooting': {
                'no_oscillation': [
                    'Increase relay amplitude',
                    'Check process gain and dynamics',
                    'Verify relay implementation',
                    'Check for process deadband'
                ],
                'poor_oscillation': [
                    'Reduce measurement noise',
                    'Check sampling rate',
                    'Verify process linearity',
                    'Consider hysteresis relay'
                ],
                'inconsistent_results': [
                    'Extend test duration',
                    'Check for external disturbances',
                    'Verify steady initial conditions',
                    'Consider process nonlinearity'
                ]
            },
            
            'industrial_acceptance': {
                'commercial_implementations': 'Available in most modern PID controllers',
                'success_rate': 'High success rate for appropriate processes',
                'user_satisfaction': 'Generally positive due to automation',
                'maintenance_benefits': 'Reduces need for manual tuning expertise'
            }
        }
