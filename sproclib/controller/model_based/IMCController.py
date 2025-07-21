"""
Internal Model Control (IMC) Controller for SPROCLIB

This module implements Internal Model Control, a model-based control strategy
that uses the inverse of the process model to cancel process dynamics.

Applications:
- Continuous reactors
- pH control systems  
- Heat exchangers
- Chemical processes with well-known dynamics

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
from typing import Optional, Callable, Dict, Any, Tuple
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ProcessModelInterface(ABC):
    """Interface for process models to be used with IMC."""
    
    @abstractmethod
    def transfer_function(self, s: complex) -> complex:
        """
        Return the process transfer function G(s) at complex frequency s.
        
        Args:
            s: Complex frequency (jω for frequency response)
            
        Returns:
            Complex transfer function value G(s)
        """
        pass
    
    @abstractmethod
    def inverse_transfer_function(self, s: complex) -> complex:
        """
        Return the inverse process transfer function G⁻¹(s) at complex frequency s.
        
        Args:
            s: Complex frequency
            
        Returns:
            Complex inverse transfer function value G⁻¹(s)
        """
        pass
    
    @abstractmethod
    def step_response(self, t: np.ndarray) -> np.ndarray:
        """
        Calculate step response of the process model.
        
        Args:
            t: Time array
            
        Returns:
            Step response array
        """
        pass


class FOPDTModel(ProcessModelInterface):
    """First Order Plus Dead Time (FOPDT) model for IMC."""
    
    def __init__(self, K: float, tau: float, theta: float):
        """
        Initialize FOPDT model: G(s) = K * exp(-θs) / (τs + 1)
        
        Args:
            K: Process gain
            tau: Time constant [time units]
            theta: Dead time [time units]
        """
        self.K = K
        self.tau = tau
        self.theta = theta
        
        # Validate parameters
        if tau <= 0:
            raise ValueError("Time constant τ must be positive")
        if theta < 0:
            raise ValueError("Dead time θ must be non-negative")
    
    def transfer_function(self, s: complex) -> complex:
        """FOPDT transfer function G(s) = K * exp(-θs) / (τs + 1)"""
        if abs(s) < 1e-12:  # Handle s ≈ 0
            return self.K
        
        dead_time_term = np.exp(-self.theta * s)
        lag_term = self.tau * s + 1
        
        return self.K * dead_time_term / lag_term
    
    def inverse_transfer_function(self, s: complex) -> complex:
        """Inverse FOPDT: G⁻¹(s) = (τs + 1) * exp(θs) / K"""
        if abs(self.K) < 1e-12:
            raise ValueError("Process gain K cannot be zero for inversion")
        
        if abs(s) < 1e-12:  # Handle s ≈ 0
            return 1.0 / self.K
        
        dead_time_term = np.exp(self.theta * s)
        lag_term = self.tau * s + 1
        
        return lag_term * dead_time_term / self.K
    
    def step_response(self, t: np.ndarray) -> np.ndarray:
        """Step response: y(t) = K * (1 - exp(-(t-θ)/τ)) * u(t-θ)"""
        response = np.zeros_like(t)
        
        # Only respond after dead time
        active_time = t >= self.theta
        if np.any(active_time):
            t_active = t[active_time] - self.theta
            response[active_time] = self.K * (1 - np.exp(-t_active / self.tau))
        
        return response
    
    def describe(self) -> Dict[str, Any]:
        """
        Comprehensive description of the FOPDT Model.
        
        Returns:
            Dictionary containing detailed information about FOPDT models,
            theory, parameter interpretation, and chemical engineering applications.
        """
        return {
            'class_name': 'FOPDTModel',
            'description': 'First Order Plus Dead Time (FOPDT) process model',
            'purpose': 'Simple yet effective model for many industrial processes',
            
            'model_parameters': {
                'K': {'value': self.K, 'description': 'Process gain (steady-state gain)', 'units': 'output_units/input_units'},
                'tau': {'value': self.tau, 'description': 'Time constant (response speed)', 'units': 'time_units'},
                'theta': {'value': self.theta, 'description': 'Dead time (transport delay)', 'units': 'time_units'}
            },
            
            'mathematical_representation': {
                'transfer_function': 'G(s) = K * exp(-θs) / (τs + 1)',
                'time_domain': 'τ * dy/dt + y = K * u(t - θ)',
                'step_response': 'y(t) = K * (1 - exp(-(t-θ)/τ)) for t ≥ θ',
                'frequency_response': 'G(jω) = K * exp(-jωθ) / (jωτ + 1)',
                'parameters': {
                    'K': 'Ratio of output change to input change at steady state',
                    'τ': 'Time to reach 63.2% of final value after step input',
                    'θ': 'Time delay before process begins to respond'
                }
            },
            
            'physical_interpretation': {
                'process_gain': {
                    'meaning': 'Sensitivity of output to input changes',
                    'positive_gain': 'Output increases when input increases',
                    'negative_gain': 'Output decreases when input increases (rare)',
                    'magnitude': 'Larger |K| means more sensitive process'
                },
                'time_constant': {
                    'meaning': 'Speed of process response',
                    'small_tau': 'Fast process response (seconds to minutes)',
                    'large_tau': 'Slow process response (hours to days)',
                    'exponential_decay': 'First-order exponential approach to steady state'
                },
                'dead_time': {
                    'sources': ['Transport delays', 'Measurement delays', 'Actuator delays', 'Chemical reaction delays'],
                    'impact': 'Makes control more difficult',
                    'rule_of_thumb': 'θ/τ < 0.5 for good controllability'
                }
            },
            
            'chemical_engineering_applications': {
                'temperature_control': {
                    'description': 'Heated tank or reactor temperature control',
                    'typical_values': {
                        'K': '0.5-2.0 °C/% valve opening',
                        'τ': '5-30 minutes (thermal time constant)',
                        'θ': '0.5-5 minutes (sensor + valve delays)'
                    },
                    'physical_basis': 'Energy balance with first-order heat transfer',
                    'limitations': 'Assumes well-mixed, constant properties'
                },
                'flow_control': {
                    'description': 'Liquid flow through control valve',
                    'typical_values': {
                        'K': '0.8-1.2 (flow gain, often near unity)',
                        'τ': '0.1-2 seconds (pipe + valve dynamics)',
                        'θ': '0.05-1 second (measurement + actuation delays)'
                    },
                    'physical_basis': 'Momentum balance with valve characteristics',
                    'limitations': 'Linear valve assumption, constant pressure drop'
                },
                'concentration_control': {
                    'description': 'Composition control in stirred tank',
                    'typical_values': {
                        'K': '0.5-3.0 mol%/L/min feed rate change',
                        'τ': '2-20 minutes (mixing time constant)',
                        'θ': '0.2-3 minutes (analyzer + sampling delays)'
                    },
                    'physical_basis': 'Material balance with perfect mixing',
                    'limitations': 'Assumes linear kinetics, perfect mixing'
                },
                'level_control': {
                    'description': 'Tank level control (with outlet restriction)',
                    'typical_values': {
                        'K': '10-100 cm/(L/min) depending on tank area',
                        'τ': '1-60 minutes (depends on tank size and outlet)',
                        'θ': '0.1-2 minutes (level sensor delays)'
                    },
                    'physical_basis': 'Mass balance with outflow resistance',
                    'limitations': 'Assumes constant outlet coefficient'
                }
            },
            
            'model_identification': {
                'step_test_method': {
                    'procedure': [
                        'Bring process to steady state',
                        'Apply step change in input (5-15%)',
                        'Record output response',
                        'Fit FOPDT parameters to data'
                    ],
                    'parameter_estimation': {
                        'K': 'Ratio of final output change to input change',
                        'tau': 'Time to reach 63.2% of final value',
                        'theta': 'Apparent delay before response begins'
                    }
                },
                'fitting_methods': [
                    'Graphical method (tangent line)',
                    'Two-point method (28.3% and 63.2% response)',
                    'Least squares regression',
                    'Process reaction curve method'
                ]
            },
            
            'control_design_implications': {
                'controller_tuning': {
                    'ziegler_nichols': 'Classical tuning rules based on K, τ, θ',
                    'lambda_tuning': 'Desired closed-loop time constant',
                    'imc_tuning': 'Internal Model Control based on FOPDT'
                },
                'performance_limitations': {
                    'dead_time_dominant': 'θ/τ > 1 makes control difficult',
                    'integrating_behavior': 'FOPDT cannot represent integrating processes',
                    'oscillatory_response': 'Cannot capture underdamped behavior'
                }
            },
            
            'frequency_domain_properties': {
                'magnitude_response': '|G(jω)| = K / √(1 + (ωτ)²)',
                'phase_response': '∠G(jω) = -ωθ - arctan(ωτ)',
                'bandwidth': 'ω_bw ≈ 1/τ (where magnitude drops 3 dB)',
                'phase_crossover': 'ω_pc where phase = -180° (if it exists)'
            },
            
            'model_validation': {
                'goodness_of_fit': [
                    'R² coefficient (should be > 0.9)',
                    'Sum of squared errors',
                    'Visual inspection of fit quality'
                ],
                'physical_reasonableness': [
                    'Positive time constant (τ > 0)',
                    'Non-negative dead time (θ ≥ 0)',
                    'Realistic gain magnitude',
                    'Consistent units'
                ],
                'model_adequacy': [
                    'Residual analysis',
                    'Independent validation data',
                    'Process knowledge consistency'
                ]
            },
            
            'advantages': [
                'Simple structure with only 3 parameters',
                'Good approximation for many processes',
                'Well-understood control design methods',
                'Easy parameter identification',
                'Analytical solutions available',
                'Widely accepted in industry'
            ],
            
            'limitations': [
                'Cannot represent higher-order dynamics',
                'No oscillatory behavior modeling',
                'Linear model only',
                'Constant parameter assumption',
                'Single time constant limitation',
                'Poor for integrating processes'
            ],
            
            'extensions_and_alternatives': {
                'sopdt': 'Second Order Plus Dead Time for better accuracy',
                'ipdt': 'Integrator Plus Dead Time for level-like processes',
                'fractional_order': 'Fractional order models for anomalous diffusion',
                'time_varying': 'Adaptive models for changing process conditions'
            }
        }


class SOPDTModel(ProcessModelInterface):
    """Second Order Plus Dead Time model for IMC."""
    
    def __init__(self, K: float, tau1: float, tau2: float, theta: float):
        """
        Initialize SOPDT model: G(s) = K * exp(-θs) / ((τ₁s + 1)(τ₂s + 1))
        
        Args:
            K: Process gain
            tau1: First time constant [time units]
            tau2: Second time constant [time units]  
            theta: Dead time [time units]
        """
        self.K = K
        self.tau1 = tau1
        self.tau2 = tau2
        self.theta = theta
        
        # Validate parameters
        if tau1 <= 0 or tau2 <= 0:
            raise ValueError("Time constants τ₁, τ₂ must be positive")
        if theta < 0:
            raise ValueError("Dead time θ must be non-negative")
    
    def transfer_function(self, s: complex) -> complex:
        """SOPDT transfer function"""
        if abs(s) < 1e-12:
            return self.K
        
        dead_time_term = np.exp(-self.theta * s)
        lag1_term = self.tau1 * s + 1
        lag2_term = self.tau2 * s + 1
        
        return self.K * dead_time_term / (lag1_term * lag2_term)
    
    def inverse_transfer_function(self, s: complex) -> complex:
        """Inverse SOPDT transfer function"""
        if abs(self.K) < 1e-12:
            raise ValueError("Process gain K cannot be zero for inversion")
        
        if abs(s) < 1e-12:
            return 1.0 / self.K
        
        dead_time_term = np.exp(self.theta * s)
        lag1_term = self.tau1 * s + 1
        lag2_term = self.tau2 * s + 1
        
        return lag1_term * lag2_term * dead_time_term / self.K
    
    def step_response(self, t: np.ndarray) -> np.ndarray:
        """Step response for second-order system"""
        response = np.zeros_like(t)
        
        active_time = t >= self.theta
        if np.any(active_time):
            t_active = t[active_time] - self.theta
            
            if abs(self.tau1 - self.tau2) < 1e-6:
                # Repeated roots case
                tau = self.tau1
                response[active_time] = self.K * (1 - (1 + t_active/tau) * np.exp(-t_active/tau))
            else:
                # Distinct roots case
                a1 = self.tau1 / (self.tau1 - self.tau2)
                a2 = self.tau2 / (self.tau2 - self.tau1)
                exp1 = np.exp(-t_active / self.tau1)
                exp2 = np.exp(-t_active / self.tau2)
                response[active_time] = self.K * (1 + a1 * exp1 + a2 * exp2)
        
        return response
    
    def describe(self) -> Dict[str, Any]:
        """
        Comprehensive description of the SOPDT Model.
        
        Returns:
            Dictionary containing detailed information about SOPDT models,
            theory, parameter interpretation, and chemical engineering applications.
        """
        return {
            'class_name': 'SOPDTModel',
            'description': 'Second Order Plus Dead Time (SOPDT) process model',
            'purpose': 'More accurate model for processes with multiple time constants',
            
            'model_parameters': {
                'K': {'value': self.K, 'description': 'Process gain (steady-state gain)', 'units': 'output_units/input_units'},
                'tau1': {'value': self.tau1, 'description': 'First time constant (dominant dynamics)', 'units': 'time_units'},
                'tau2': {'value': self.tau2, 'description': 'Second time constant (secondary dynamics)', 'units': 'time_units'},
                'theta': {'value': self.theta, 'description': 'Dead time (transport delay)', 'units': 'time_units'}
            },
            
            'mathematical_representation': {
                'transfer_function': 'G(s) = K * exp(-θs) / ((τ₁s + 1)(τ₂s + 1))',
                'expanded_form': 'G(s) = K * exp(-θs) / (τ₁τ₂s² + (τ₁ + τ₂)s + 1)',
                'time_domain_ode': 'τ₁τ₂ * d²y/dt² + (τ₁ + τ₂) * dy/dt + y = K * u(t - θ)',
                'characteristic_equation': 'τ₁τ₂s² + (τ₁ + τ₂)s + 1 = 0',
                'poles': f'p₁ = -1/τ₁ = {-1/self.tau1:.4f}, p₂ = -1/τ₂ = {-1/self.tau2:.4f}'
            },
            
            'system_classification': {
                'time_constant_ratio': self.tau1 / self.tau2 if self.tau2 != 0 else float('inf'),
                'system_type': self._classify_sopdt_type(),
                'dominant_pole': f'τ₁ = {self.tau1}' if self.tau1 > self.tau2 else f'τ₂ = {self.tau2}',
                'settling_time_estimate': f'{4 * max(self.tau1, self.tau2):.2f} time units'
            },
            
            'physical_interpretation': {
                'two_time_constants': {
                    'meaning': 'Two distinct energy/mass storage mechanisms',
                    'fast_mode': f'τ_fast = {min(self.tau1, self.tau2)} (quick initial response)',
                    'slow_mode': f'τ_slow = {max(self.tau1, self.tau2)} (long-term approach to steady state)',
                    'interaction': 'Two coupled first-order processes in series or parallel'
                },
                'step_response_characteristics': {
                    'initial_response': 'Governed by faster time constant',
                    'final_approach': 'Governed by slower time constant',
                    'shape': 'S-curve more pronounced than FOPDT',
                    'inflection_point': 'Transition between fast and slow modes'
                }
            },
            
            'chemical_engineering_applications': {
                'heat_exchanger_dynamics': {
                    'description': 'Shell-and-tube heat exchanger temperature control',
                    'physical_basis': [
                        'τ₁: Metal thermal time constant (fast)',
                        'τ₂: Fluid thermal time constant (slow)',
                        'θ: Transport delay through exchanger'
                    ],
                    'typical_values': {
                        'K': '0.7-1.3 °C/°C coolant change',
                        'τ₁': '1-5 minutes (metal response)',
                        'τ₂': '10-30 minutes (fluid response)',
                        'θ': '0.5-3 minutes (transport delay)'
                    }
                },
                'reactor_with_jacket': {
                    'description': 'Jacketed reactor temperature control',
                    'physical_basis': [
                        'τ₁: Reactor contents time constant',
                        'τ₂: Jacket fluid time constant',
                        'θ: Heat transfer and measurement delays'
                    ],
                    'typical_values': {
                        'K': '0.5-1.5 °C/% valve opening',
                        'τ₁': '3-15 minutes (reactor contents)',
                        'τ₂': '5-25 minutes (jacket dynamics)',
                        'θ': '1-5 minutes (thermal delays)'
                    }
                },
                'distillation_tray_temperature': {
                    'description': 'Tray temperature response to reboiler duty',
                    'physical_basis': [
                        'τ₁: Tray holdup time constant',
                        'τ₂: Column hydraulic time constant',
                        'θ: Vapor transport delay'
                    ],
                    'typical_values': {
                        'K': '1.0-3.0 °C/% reboiler duty',
                        'τ₁': '2-8 minutes (tray dynamics)',
                        'τ₂': '15-45 minutes (column dynamics)',
                        'θ': '3-12 minutes (vapor transport)'
                    }
                },
                'crystallizer_temperature': {
                    'description': 'Batch crystallizer temperature control',
                    'physical_basis': [
                        'τ₁: Solution thermal time constant',
                        'τ₂: Heat transfer surface time constant',
                        'θ: Cooling system transport delay'
                    ],
                    'typical_values': {
                        'K': '0.6-1.8 °C/°C coolant change',
                        'τ₁': '5-20 minutes (solution response)',
                        'τ₂': '10-40 minutes (heat transfer surface)',
                        'θ': '1-8 minutes (coolant system delay)'
                    }
                }
            },
            
            'model_identification': {
                'step_test_analysis': {
                    'data_requirements': 'Clean step response data with good signal-to-noise ratio',
                    'fitting_challenges': 'More parameters than FOPDT, requires better data',
                    'parameter_estimation': [
                        'Graphical methods (dual tangent)',
                        'Nonlinear least squares',
                        'Frequency domain fitting',
                        'Subspace identification'
                    ]
                },
                'parameter_bounds': {
                    'physical_constraints': 'τ₁ > 0, τ₂ > 0, θ ≥ 0',
                    'identifiability': 'Need τ₁ ≠ τ₂ for unique identification',
                    'time_scale_separation': 'Ideally τ₁/τ₂ > 3 for clear identification'
                }
            },
            
            'control_design_considerations': {
                'tuning_methods': {
                    'imc_design': 'Natural choice for IMC controller design',
                    'pid_tuning': 'More complex than FOPDT, may use approximations',
                    'model_reduction': 'Sometimes approximated as FOPDT for simple control'
                },
                'performance_implications': {
                    'slower_than_fopdt': 'Generally requires more conservative tuning',
                    'better_accuracy': 'More accurate process representation',
                    'controller_complexity': 'May justify more sophisticated control'
                }
            },
            
            'frequency_domain_analysis': {
                'magnitude_response': '|G(jω)| = K / (√(1 + (ωτ₁)²) * √(1 + (ωτ₂)²))',
                'phase_response': '∠G(jω) = -ωθ - arctan(ωτ₁) - arctan(ωτ₂)',
                'bandwidth': 'Lower than equivalent FOPDT due to additional pole',
                'roll_off': '-40 dB/decade at high frequencies (vs -20 for FOPDT)'
            },
            
            'step_response_analysis': {
                'response_shape': self._analyze_step_response_shape(),
                'time_to_90_percent': f'{self._estimate_90_percent_time():.2f} time units',
                'maximum_slope': self._calculate_maximum_slope(),
                'overshoot': 'None (overdamped system)' if self.tau1 > 0 and self.tau2 > 0 else 'Possible'
            },
            
            'model_validation': {
                'fit_quality_metrics': [
                    'R² coefficient (should be > 0.95 for SOPDT)',
                    'Sum of squared errors',
                    'Residual autocorrelation analysis'
                ],
                'physical_validation': [
                    'Time constants match process physics',
                    'Parameter values within reasonable ranges',
                    'Dead time consistent with transport delays'
                ],
                'model_adequacy_tests': [
                    'Residual whiteness test',
                    'Model structure validation',
                    'Cross-validation with different data sets'
                ]
            },
            
            'advantages_over_fopdt': [
                'Better accuracy for many industrial processes',
                'Captures two-time-scale behavior',
                'More realistic representation of complex dynamics',
                'Better prediction of transient behavior',
                'Superior for processes with series/parallel components'
            ],
            
            'limitations': [
                'More complex parameter identification',
                'Requires higher quality data',
                'Still limited to linear behavior',
                'Cannot represent oscillatory behavior',
                'More parameters to estimate and validate'
            ],
            
            'when_to_use_sopdt': {
                'over_fopdt': [
                    'FOPDT fit quality is poor (R² < 0.9)',
                    'Process has clear two-time-scale behavior',
                    'High accuracy requirements',
                    'Model-based control design',
                    'Process understanding is important'
                ],
                'stick_with_fopdt': [
                    'FOPDT provides adequate fit',
                    'Simple PID control is sufficient',
                    'Data quality is limited',
                    'Quick tuning is required'
                ]
            }
        }
    
    def _classify_sopdt_type(self) -> str:
        """Classify SOPDT based on time constant ratio."""
        ratio = max(self.tau1, self.tau2) / min(self.tau1, self.tau2)
        if ratio > 10:
            return "Well-separated time constants (essentially FOPDT)"
        elif ratio > 3:
            return "Moderately separated time constants"
        else:
            return "Similar time constants"
    
    def _analyze_step_response_shape(self) -> str:
        """Analyze the shape characteristics of step response."""
        if abs(self.tau1 - self.tau2) < 1e-6:
            return "Repeated poles - critically damped response"
        else:
            ratio = max(self.tau1, self.tau2) / min(self.tau1, self.tau2)
            if ratio > 5:
                return "Dominant pole behavior (similar to FOPDT)"
            else:
                return "Two-time-scale response (distinct S-curve)"
    
    def _estimate_90_percent_time(self) -> float:
        """Estimate time to reach 90% of steady state."""
        # Approximation based on dominant time constant
        return 2.3 * max(self.tau1, self.tau2) + self.theta
    
    def _calculate_maximum_slope(self) -> str:
        """Calculate maximum slope of step response."""
        if abs(self.tau1 - self.tau2) < 1e-6:
            # Repeated roots case
            max_slope = self.K / (self.tau1 * np.e)
            return f"{max_slope:.4f} output_units/time_unit"
        else:
            # Distinct roots - more complex calculation
            return "Complex calculation for distinct time constants"


class IMCController:
    """
    Internal Model Control (IMC) Controller.
    
    IMC uses the inverse of the process model to cancel process dynamics,
    providing excellent setpoint tracking and disturbance rejection.
    """
    
    def __init__(
        self,
        process_model: ProcessModelInterface,
        filter_time_constant: float,
        filter_order: int = 1,
        name: str = "IMC_Controller"
    ):
        """
        Initialize IMC controller.
        
        Args:
            process_model: Process model implementing ProcessModelInterface
            filter_time_constant: IMC filter time constant λ [time units]
            filter_order: Order of IMC filter (1 or 2)
            name: Controller name for identification
        """
        self.process_model = process_model
        self.lambda_c = filter_time_constant
        self.filter_order = filter_order
        self.name = name
        
        # Controller state
        self.setpoint_history = []
        self.output_history = []
        self.time_history = []
        self.last_update_time = None
        
        # Validate inputs
        if filter_time_constant <= 0:
            raise ValueError("Filter time constant λ must be positive")
        if filter_order not in [1, 2]:
            raise ValueError("Filter order must be 1 or 2")
        
        logger.info(f"IMC Controller '{name}' initialized with λ = {filter_time_constant}")
    
    def _imc_filter(self, s: complex) -> complex:
        """
        IMC filter transfer function f(s).
        
        For filter order n: f(s) = 1 / (λs + 1)ⁿ
        """
        denominator = self.lambda_c * s + 1
        return 1.0 / (denominator ** self.filter_order)
    
    def _controller_transfer_function(self, s: complex) -> complex:
        """
        IMC controller transfer function Q(s) = G⁻¹(s) * f(s)
        
        Where:
        - G⁻¹(s) is the inverse process model
        - f(s) is the IMC filter
        """
        try:
            g_inv = self.process_model.inverse_transfer_function(s)
            f_s = self._imc_filter(s)
            return g_inv * f_s
        except (ZeroDivisionError, OverflowError):
            # Handle numerical issues
            return 0.0
    
    def update(
        self,
        t: float,
        setpoint: float,
        process_variable: float,
        feedforward: float = 0.0
    ) -> float:
        """
        Update IMC controller and calculate control output.
        
        Args:
            t: Current time
            setpoint: Desired setpoint value
            process_variable: Current process variable (measurement)
            feedforward: Optional feedforward signal
            
        Returns:
            Controller output (manipulated variable)
        """
        # Store history
        self.setpoint_history.append(setpoint)
        self.output_history.append(process_variable)
        self.time_history.append(t)
        
        # Limit history length
        max_history = 1000
        if len(self.time_history) > max_history:
            self.setpoint_history = self.setpoint_history[-max_history:]
            self.output_history = self.output_history[-max_history:]
            self.time_history = self.time_history[-max_history:]
        
        # For discrete implementation, use simple approximation
        # In practice, this would use more sophisticated numerical methods
        error = setpoint - process_variable
        
        # Simple IMC approximation for real-time implementation
        # Full IMC requires convolution or frequency domain methods
        if self.last_update_time is not None:
            dt = t - self.last_update_time
            if dt > 0:
                # Approximate IMC response using equivalent PID parameters
                Kp, Ki, Kd = self._get_equivalent_pid_parameters()
                
                # Simple PID-like calculation (approximation)
                proportional = Kp * error
                
                # Simplified integral (would need proper integration in practice)
                integral = Ki * error * dt if hasattr(self, '_integral') else 0
                if not hasattr(self, '_integral'):
                    self._integral = 0
                self._integral += error * dt
                integral = Ki * self._integral
                
                # Simplified derivative
                if hasattr(self, '_last_error'):
                    derivative = Kd * (error - self._last_error) / dt
                else:
                    derivative = 0
                self._last_error = error
                
                output = proportional + integral + derivative + feedforward
            else:
                output = feedforward
        else:
            output = feedforward
            if not hasattr(self, '_integral'):
                self._integral = 0
        
        self.last_update_time = t
        
        # Apply output limits if specified
        if hasattr(self, 'output_limits'):
            output = np.clip(output, self.output_limits[0], self.output_limits[1])
        
        return output
    
    def _get_equivalent_pid_parameters(self) -> Tuple[float, float, float]:
        """
        Calculate equivalent PID parameters for the IMC controller.
        
        For FOPDT process G(s) = K*exp(-θs)/(τs+1) with IMC filter λ:
        Kp = τ/(K*(λ+θ))
        Ki = 1/(λ+θ)  
        Kd = 0  (for first-order filter)
        
        Returns:
            Tuple of (Kp, Ki, Kd)
        """
        if isinstance(self.process_model, FOPDTModel):
            K = self.process_model.K
            tau = self.process_model.tau
            theta = self.process_model.theta
            
            if abs(K) < 1e-12:
                raise ValueError("Process gain K cannot be zero")
            
            Kp = tau / (K * (self.lambda_c + theta))
            Ki = 1.0 / (self.lambda_c + theta)
            Kd = 0.0  # For first-order filter
            
            return Kp, Ki, Kd
        
        elif isinstance(self.process_model, SOPDTModel):
            # Approximate SOPDT as FOPDT for PID equivalence
            K = self.process_model.K
            tau_eq = self.process_model.tau1 + self.process_model.tau2
            theta = self.process_model.theta
            
            Kp = tau_eq / (K * (self.lambda_c + theta))
            Ki = 1.0 / (self.lambda_c + theta)
            Kd = (self.process_model.tau1 * self.process_model.tau2) / (K * (self.lambda_c + theta))
            
            return Kp, Ki, Kd
        
        else:
            # Default conservative values
            return 1.0, 0.1, 0.0
    
    def set_output_limits(self, min_output: float, max_output: float):
        """Set output saturation limits."""
        if min_output >= max_output:
            raise ValueError("min_output must be less than max_output")
        self.output_limits = (min_output, max_output)
        logger.info(f"IMC output limits set: [{min_output}, {max_output}]")
    
    def reset(self):
        """Reset controller internal state."""
        self.setpoint_history.clear()
        self.output_history.clear()
        self.time_history.clear()
        self.last_update_time = None
        if hasattr(self, '_integral'):
            self._integral = 0
        if hasattr(self, '_last_error'):
            delattr(self, '_last_error')
        logger.info(f"IMC Controller '{self.name}' reset")
    
    def get_tuning_parameters(self) -> Dict[str, float]:
        """Get current tuning parameters."""
        Kp, Ki, Kd = self._get_equivalent_pid_parameters()
        return {
            'lambda_c': self.lambda_c,
            'filter_order': self.filter_order,
            'equivalent_Kp': Kp,
            'equivalent_Ki': Ki,
            'equivalent_Kd': Kd
        }
    
    def frequency_response(
        self,
        omega: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate frequency response of the IMC controller.
        
        Args:
            omega: Frequency array [rad/time]
            
        Returns:
            Tuple of (magnitude, phase, frequency)
        """
        s_values = 1j * omega
        response = np.array([self._controller_transfer_function(s) for s in s_values])
        
        magnitude = np.abs(response)
        phase = np.angle(response) * 180 / np.pi  # Convert to degrees
        
        return magnitude, phase, omega
    
    def closed_loop_response(
        self,
        omega: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate closed-loop frequency response.
        
        For IMC: T(s) = G(s)*Q(s) / (1 + G(s)*Q(s))
        
        Args:
            omega: Frequency array [rad/time]
            
        Returns:
            Tuple of (magnitude, phase)
        """
        s_values = 1j * omega
        response = []
        
        for s in s_values:
            try:
                G_s = self.process_model.transfer_function(s)
                Q_s = self._controller_transfer_function(s)
                
                # Closed-loop transfer function
                GQ = G_s * Q_s
                T_s = GQ / (1 + GQ)
                response.append(T_s)
            except:
                response.append(0.0)
        
        response = np.array(response)
        magnitude = np.abs(response)
        phase = np.angle(response) * 180 / np.pi
        
        return magnitude, phase


def tune_imc_lambda(
    process_model: ProcessModelInterface,
    desired_settling_time: float,
    overshoot_limit: float = 0.05
) -> float:
    """
    Tune IMC filter time constant λ based on desired performance.
    
    Args:
        process_model: Process model
        desired_settling_time: Desired 2% settling time
        overshoot_limit: Maximum allowed overshoot (0.05 = 5%)
        
    Returns:
        Recommended λ value
    """
    if isinstance(process_model, FOPDTModel):
        tau = process_model.tau
        theta = process_model.theta
        
        # Rule of thumb: λ ≈ 0.1 to 1.0 times the dominant time constant
        # For settling time: λ ≈ (desired_settling_time - θ) / 3
        lambda_settling = max(0.1 * tau, (desired_settling_time - theta) / 3)
        
        # For overshoot constraint: λ ≥ θ for minimal overshoot
        lambda_overshoot = theta if overshoot_limit < 0.1 else 0.5 * theta
        
        # Take the larger value for conservative tuning
        lambda_recommended = max(lambda_settling, lambda_overshoot, 0.1 * tau)
        
        logger.info(f"IMC tuning: settling time constraint λ = {lambda_settling:.3f}")
        logger.info(f"IMC tuning: overshoot constraint λ = {lambda_overshoot:.3f}")
        logger.info(f"IMC tuning: recommended λ = {lambda_recommended:.3f}")
        
        return lambda_recommended
    
    else:
        # Conservative default
        return 1.0
    
    def describe(self) -> Dict[str, Any]:
        """
        Comprehensive description of the Internal Model Control (IMC) Controller.
        
        Returns:
            Dictionary containing detailed information about the IMC controller,
            its process models, tuning parameters, and industrial applications.
        """
        # Get process model information
        model_info = {}
        if isinstance(self.process_model, FOPDTModel):
            model_info = {
                'type': 'FOPDT (First Order Plus Dead Time)',
                'transfer_function': 'G(s) = K * exp(-θs) / (τs + 1)',
                'parameters': {
                    'gain': self.process_model.K,
                    'time_constant': self.process_model.tau,
                    'dead_time': self.process_model.theta
                }
            }
        elif isinstance(self.process_model, SOPDTModel):
            model_info = {
                'type': 'SOPDT (Second Order Plus Dead Time)',
                'transfer_function': 'G(s) = K * exp(-θs) / ((τ₁s + 1)(τ₂s + 1))',
                'parameters': {
                    'gain': self.process_model.K,
                    'time_constant_1': self.process_model.tau1,
                    'time_constant_2': self.process_model.tau2,
                    'dead_time': self.process_model.theta
                }
            }
        
        # Get equivalent PID parameters
        try:
            Kp, Ki, Kd = self._get_equivalent_pid_parameters()
            equivalent_pid = {
                'proportional_gain': Kp,
                'integral_gain': Ki,
                'derivative_gain': Kd
            }
        except:
            equivalent_pid = {
                'proportional_gain': 'Not available',
                'integral_gain': 'Not available',
                'derivative_gain': 'Not available'
            }
        
        return {
            'class_name': 'IMCController',
            'description': 'Internal Model Control (IMC) - Advanced model-based controller',
            'purpose': 'Provides excellent setpoint tracking and disturbance rejection using process model inversion',
            
            'control_strategy': {
                'method': 'Model-based control using process inverse',
                'principle': 'Uses internal process model to predict and compensate process behavior',
                'structure': 'Q(s) = G⁻¹(s) * f(s) where Q(s) is controller, G⁻¹(s) is model inverse, f(s) is filter',
                'advantages': [
                    'Perfect setpoint tracking (in theory)',
                    'Explicit handling of process dead time',
                    'Systematic tuning procedure',
                    'Inherent robustness through filtering'
                ]
            },
            
            'process_model': model_info,
            
            'controller_parameters': {
                'filter_time_constant': {
                    'value': self.lambda_c,
                    'symbol': 'λ',
                    'units': 'time units',
                    'description': 'Primary tuning parameter controlling closed-loop speed',
                    'typical_range': '0.1τ to 2.0τ (where τ is process time constant)',
                    'effect': 'Smaller λ = faster response but less robust, Larger λ = slower but more robust'
                },
                'filter_order': {
                    'value': self.filter_order,
                    'symbol': 'n',
                    'description': 'Order of IMC filter (usually 1 or 2)',
                    'effect': 'Higher order provides better robustness but more complex implementation'
                }
            },
            
            'equivalent_pid_parameters': equivalent_pid,
            
            'imc_theory': {
                'perfect_control': 'IMC provides perfect control when model matches process exactly',
                'robustness': 'Filter ensures stability even with model mismatch',
                'two_degree_freedom': 'Separate handling of setpoint tracking and disturbance rejection',
                'internal_model_principle': 'Controller contains model of the process being controlled'
            },
            
            'tuning_guidelines': {
                'lambda_selection': {
                    'conservative': 'λ = τ (time constant of process)',
                    'moderate': 'λ = 0.5τ',
                    'aggressive': 'λ = 0.1τ',
                    'dead_time_constraint': 'λ ≥ θ for minimal overshoot'
                },
                'performance_trade_offs': {
                    'speed_vs_robustness': 'Smaller λ gives faster response but less robustness',
                    'noise_sensitivity': 'Higher filter order reduces noise sensitivity',
                    'model_uncertainty': 'Larger λ provides better tolerance to model mismatch'
                }
            },
            
            'industrial_applications': {
                'reactor_temperature_control': {
                    'description': 'Precise temperature control in chemical reactors',
                    'model_type': 'FOPDT with large time constants',
                    'typical_lambda': '0.5 to 2.0 times thermal time constant',
                    'benefits': 'Handles thermal lag and dead time explicitly'
                },
                'distillation_composition': {
                    'description': 'Product composition control in distillation columns',
                    'model_type': 'SOPDT with significant dead time',
                    'typical_lambda': '1.0 to 3.0 times dominant time constant',
                    'benefits': 'Excellent for high-purity separation requirements'
                },
                'ph_neutralization': {
                    'description': 'pH control in wastewater treatment',
                    'model_type': 'Nonlinear, approximated by FOPDT',
                    'typical_lambda': '0.2 to 1.0 times process time constant',
                    'benefits': 'Handles process nonlinearity through model adaptation'
                },
                'heat_exchanger_control': {
                    'description': 'Outlet temperature control in heat exchangers',
                    'model_type': 'FOPDT with moderate dead time',
                    'typical_lambda': '0.5 to 1.5 times thermal time constant',
                    'benefits': 'Superior performance compared to PID for thermal processes'
                }
            },
            
            'model_requirements': {
                'fopdt_identification': {
                    'methods': ['Step test', 'Impulse response', 'Frequency response'],
                    'parameters': ['Process gain K', 'Time constant τ', 'Dead time θ'],
                    'accuracy_needed': '±10% for good IMC performance'
                },
                'model_validation': {
                    'criteria': ['Step response fit', 'Frequency response match', 'Steady-state gain'],
                    'tools': ['Cross-validation', 'Residual analysis', 'Prediction error methods']
                }
            },
            
            'implementation_considerations': {
                'digital_implementation': {
                    'sampling_time': 'Should be 5-10 times faster than λ',
                    'numerical_methods': 'Tustin transformation for filter discretization',
                    'computational_load': 'Moderate - requires model evaluation at each step'
                },
                'robustness_analysis': {
                    'gain_margin': 'Typically > 3 (9.5 dB) with proper λ selection',
                    'phase_margin': 'Typically > 45° with proper filter design',
                    'model_uncertainty': 'λ should account for expected model errors'
                },
                'performance_monitoring': {
                    'model_mismatch': 'Monitor prediction error for model degradation',
                    'adaptation': 'Consider adaptive IMC for time-varying processes',
                    'backup_control': 'Fallback to PID if model becomes unreliable'
                }
            },
            
            'advantages_over_pid': {
                'systematic_tuning': 'Only one main parameter (λ) to tune',
                'dead_time_handling': 'Explicit compensation for process delays',
                'setpoint_tracking': 'Theoretically perfect tracking with exact model',
                'disturbance_rejection': 'Excellent rejection through model prediction'
            },
            
            'limitations': {
                'model_dependency': 'Performance degrades with model inaccuracy',
                'inverse_model': 'Requires invertible process model',
                'computational_cost': 'Higher than PID due to model calculations',
                'nonlinear_processes': 'Limited to linear or linearized models'
            },
            
            'current_state': {
                'controller_name': self.name,
                'last_update_time': self.last_update_time,
                'history_length': len(self.time_history),
                'output_limits': getattr(self, 'output_limits', 'Not set'),
                'internal_states': {
                    'integral_term': getattr(self, '_integral', 0),
                    'last_error': getattr(self, '_last_error', 'Not available')
                }
            }
        }
    
    def describe(self) -> Dict[str, Any]:
        """
        Comprehensive description of the Internal Model Control (IMC) Controller.
        
        Returns:
            Dictionary containing detailed information about the IMC controller,
            its process models, tuning parameters, and industrial applications.
        """
        # Get process model information
        model_info = {}
        if isinstance(self.process_model, FOPDTModel):
            model_info = {
                'type': 'FOPDT (First Order Plus Dead Time)',
                'transfer_function': 'G(s) = K * exp(-θs) / (τs + 1)',
                'parameters': {
                    'gain': self.process_model.K,
                    'time_constant': self.process_model.tau,
                    'dead_time': self.process_model.theta
                }
            }
        elif isinstance(self.process_model, SOPDTModel):
            model_info = {
                'type': 'SOPDT (Second Order Plus Dead Time)',
                'transfer_function': 'G(s) = K * exp(-θs) / ((τ₁s + 1)(τ₂s + 1))',
                'parameters': {
                    'gain': self.process_model.K,
                    'time_constant_1': self.process_model.tau1,
                    'time_constant_2': self.process_model.tau2,
                    'dead_time': self.process_model.theta
                }
            }
        
        # Get equivalent PID parameters
        try:
            Kp, Ki, Kd = self._get_equivalent_pid_parameters()
            equivalent_pid = {
                'proportional_gain': Kp,
                'integral_gain': Ki,
                'derivative_gain': Kd
            }
        except:
            equivalent_pid = {
                'proportional_gain': 'Not available',
                'integral_gain': 'Not available',
                'derivative_gain': 'Not available'
            }
        
        return {
            'class_name': 'IMCController',
            'description': 'Internal Model Control (IMC) - Advanced model-based controller',
            'purpose': 'Provides excellent setpoint tracking and disturbance rejection using process model inversion',
            
            'control_strategy': {
                'method': 'Model-based control using process inverse',
                'principle': 'Uses internal process model to predict and compensate process behavior',
                'structure': 'Q(s) = G⁻¹(s) * f(s) where Q(s) is controller, G⁻¹(s) is model inverse, f(s) is filter',
                'advantages': [
                    'Perfect setpoint tracking (in theory)',
                    'Explicit handling of process dead time',
                    'Systematic tuning procedure',
                    'Inherent robustness through filtering'
                ]
            },
            
            'process_model': model_info,
            
            'controller_parameters': {
                'filter_time_constant': {
                    'value': self.lambda_c,
                    'symbol': 'λ',
                    'units': 'time units',
                    'description': 'Primary tuning parameter controlling closed-loop speed',
                    'typical_range': '0.1τ to 2.0τ (where τ is process time constant)',
                    'effect': 'Smaller λ = faster response but less robust, Larger λ = slower but more robust'
                },
                'filter_order': {
                    'value': self.filter_order,
                    'symbol': 'n',
                    'description': 'Order of IMC filter (usually 1 or 2)',
                    'effect': 'Higher order provides better robustness but more complex implementation'
                }
            },
            
            'equivalent_pid_parameters': equivalent_pid,
            
            'imc_theory': {
                'perfect_control': 'IMC provides perfect control when model matches process exactly',
                'robustness': 'Filter ensures stability even with model mismatch',
                'two_degree_freedom': 'Separate handling of setpoint tracking and disturbance rejection',
                'internal_model_principle': 'Controller contains model of the process being controlled'
            },
            
            'tuning_guidelines': {
                'lambda_selection': {
                    'conservative': 'λ = τ (time constant of process)',
                    'moderate': 'λ = 0.5τ',
                    'aggressive': 'λ = 0.1τ',
                    'dead_time_constraint': 'λ ≥ θ for minimal overshoot'
                },
                'performance_trade_offs': {
                    'speed_vs_robustness': 'Smaller λ gives faster response but less robustness',
                    'noise_sensitivity': 'Higher filter order reduces noise sensitivity',
                    'model_uncertainty': 'Larger λ provides better tolerance to model mismatch'
                }
            },
            
            'industrial_applications': {
                'reactor_temperature_control': {
                    'description': 'Precise temperature control in chemical reactors',
                    'model_type': 'FOPDT with large time constants',
                    'typical_lambda': '0.5 to 2.0 times thermal time constant',
                    'benefits': 'Handles thermal lag and dead time explicitly'
                },
                'distillation_composition': {
                    'description': 'Product composition control in distillation columns',
                    'model_type': 'SOPDT with significant dead time',
                    'typical_lambda': '1.0 to 3.0 times dominant time constant',
                    'benefits': 'Excellent for high-purity separation requirements'
                },
                'ph_neutralization': {
                    'description': 'pH control in wastewater treatment',
                    'model_type': 'Nonlinear, approximated by FOPDT',
                    'typical_lambda': '0.2 to 1.0 times process time constant',
                    'benefits': 'Handles process nonlinearity through model adaptation'
                },
                'heat_exchanger_control': {
                    'description': 'Outlet temperature control in heat exchangers',
                    'model_type': 'FOPDT with moderate dead time',
                    'typical_lambda': '0.5 to 1.5 times thermal time constant',
                    'benefits': 'Superior performance compared to PID for thermal processes'
                }
            },
            
            'model_requirements': {
                'fopdt_identification': {
                    'methods': ['Step test', 'Impulse response', 'Frequency response'],
                    'parameters': ['Process gain K', 'Time constant τ', 'Dead time θ'],
                    'accuracy_needed': '±10% for good IMC performance'
                },
                'model_validation': {
                    'criteria': ['Step response fit', 'Frequency response match', 'Steady-state gain'],
                    'tools': ['Cross-validation', 'Residual analysis', 'Prediction error methods']
                }
            },
            
            'implementation_considerations': {
                'digital_implementation': {
                    'sampling_time': 'Should be 5-10 times faster than λ',
                    'numerical_methods': 'Tustin transformation for filter discretization',
                    'computational_load': 'Moderate - requires model evaluation at each step'
                },
                'robustness_analysis': {
                    'gain_margin': 'Typically > 3 (9.5 dB) with proper λ selection',
                    'phase_margin': 'Typically > 45° with proper filter design',
                    'model_uncertainty': 'λ should account for expected model errors'
                },
                'performance_monitoring': {
                    'model_mismatch': 'Monitor prediction error for model degradation',
                    'adaptation': 'Consider adaptive IMC for time-varying processes',
                    'backup_control': 'Fallback to PID if model becomes unreliable'
                }
            },
            
            'advantages_over_pid': {
                'systematic_tuning': 'Only one main parameter (λ) to tune',
                'dead_time_handling': 'Explicit compensation for process delays',
                'setpoint_tracking': 'Theoretically perfect tracking with exact model',
                'disturbance_rejection': 'Excellent rejection through model prediction'
            },
            
            'limitations': {
                'model_dependency': 'Performance degrades with model inaccuracy',
                'inverse_model': 'Requires invertible process model',
                'computational_cost': 'Higher than PID due to model calculations',
                'nonlinear_processes': 'Limited to linear or linearized models'
            },
            
            'current_state': {
                'controller_name': self.name,
                'last_update_time': self.last_update_time,
                'history_length': len(self.time_history),
                'output_limits': getattr(self, 'output_limits', 'Not set'),
                'internal_states': {
                    'integral_term': getattr(self, '_integral', 0),
                    'last_error': getattr(self, '_last_error', 'Not available')
                }
            }
        }
    
    def describe(self) -> Dict[str, Any]:
        """
        Comprehensive description of the Internal Model Control (IMC) Controller.
        
        Returns:
            Dictionary containing detailed information about the IMC controller,
            its process models, tuning parameters, and industrial applications.
        """
        # Get process model information
        model_info = {}
        if isinstance(self.process_model, FOPDTModel):
            model_info = {
                'type': 'FOPDT (First Order Plus Dead Time)',
                'transfer_function': 'G(s) = K * exp(-θs) / (τs + 1)',
                'parameters': {
                    'gain': self.process_model.K,
                    'time_constant': self.process_model.tau,
                    'dead_time': self.process_model.theta
                }
            }
        elif isinstance(self.process_model, SOPDTModel):
            model_info = {
                'type': 'SOPDT (Second Order Plus Dead Time)',
                'transfer_function': 'G(s) = K * exp(-θs) / ((τ₁s + 1)(τ₂s + 1))',
                'parameters': {
                    'gain': self.process_model.K,
                    'time_constant_1': self.process_model.tau1,
                    'time_constant_2': self.process_model.tau2,
                    'dead_time': self.process_model.theta
                }
            }
        
        # Get equivalent PID parameters
        try:
            Kp, Ki, Kd = self._get_equivalent_pid_parameters()
            equivalent_pid = {
                'proportional_gain': Kp,
                'integral_gain': Ki,
                'derivative_gain': Kd
            }
        except:
            equivalent_pid = {
                'proportional_gain': 'Not available',
                'integral_gain': 'Not available',
                'derivative_gain': 'Not available'
            }
        
        return {
            'class_name': 'IMCController',
            'description': 'Internal Model Control (IMC) - Advanced model-based controller',
            'purpose': 'Provides excellent setpoint tracking and disturbance rejection using process model inversion',
            
            'control_strategy': {
                'method': 'Model-based control using process inverse',
                'principle': 'Uses internal process model to predict and compensate process behavior',
                'structure': 'Q(s) = G⁻¹(s) * f(s) where Q(s) is controller, G⁻¹(s) is model inverse, f(s) is filter',
                'advantages': [
                    'Perfect setpoint tracking (in theory)',
                    'Explicit handling of process dead time',
                    'Systematic tuning procedure',
                    'Inherent robustness through filtering'
                ]
            },
            
            'process_model': model_info,
            
            'controller_parameters': {
                'filter_time_constant': {
                    'value': self.lambda_c,
                    'symbol': 'λ',
                    'units': 'time units',
                    'description': 'Primary tuning parameter controlling closed-loop speed',
                    'typical_range': '0.1τ to 2.0τ (where τ is process time constant)',
                    'effect': 'Smaller λ = faster response but less robust, Larger λ = slower but more robust'
                },
                'filter_order': {
                    'value': self.filter_order,
                    'symbol': 'n',
                    'description': 'Order of IMC filter (usually 1 or 2)',
                    'effect': 'Higher order provides better robustness but more complex implementation'
                }
            },
            
            'equivalent_pid_parameters': equivalent_pid,
            
            'imc_theory': {
                'perfect_control': 'IMC provides perfect control when model matches process exactly',
                'robustness': 'Filter ensures stability even with model mismatch',
                'two_degree_freedom': 'Separate handling of setpoint tracking and disturbance rejection',
                'internal_model_principle': 'Controller contains model of the process being controlled'
            },
            
            'tuning_guidelines': {
                'lambda_selection': {
                    'conservative': 'λ = τ (time constant of process)',
                    'moderate': 'λ = 0.5τ',
                    'aggressive': 'λ = 0.1τ',
                    'dead_time_constraint': 'λ ≥ θ for minimal overshoot'
                },
                'performance_trade_offs': {
                    'speed_vs_robustness': 'Smaller λ gives faster response but less robustness',
                    'noise_sensitivity': 'Higher filter order reduces noise sensitivity',
                    'model_uncertainty': 'Larger λ provides better tolerance to model mismatch'
                }
            },
            
            'industrial_applications': {
                'reactor_temperature_control': {
                    'description': 'Precise temperature control in chemical reactors',
                    'model_type': 'FOPDT with large time constants',
                    'typical_lambda': '0.5 to 2.0 times thermal time constant',
                    'benefits': 'Handles thermal lag and dead time explicitly'
                },
                'distillation_composition': {
                    'description': 'Product composition control in distillation columns',
                    'model_type': 'SOPDT with significant dead time',
                    'typical_lambda': '1.0 to 3.0 times dominant time constant',
                    'benefits': 'Excellent for high-purity separation requirements'
                },
                'ph_neutralization': {
                    'description': 'pH control in wastewater treatment',
                    'model_type': 'Nonlinear, approximated by FOPDT',
                    'typical_lambda': '0.2 to 1.0 times process time constant',
                    'benefits': 'Handles process nonlinearity through model adaptation'
                },
                'heat_exchanger_control': {
                    'description': 'Outlet temperature control in heat exchangers',
                    'model_type': 'FOPDT with moderate dead time',
                    'typical_lambda': '0.5 to 1.5 times thermal time constant',
                    'benefits': 'Superior performance compared to PID for thermal processes'
                }
            },
            
            'model_requirements': {
                'fopdt_identification': {
                    'methods': ['Step test', 'Impulse response', 'Frequency response'],
                    'parameters': ['Process gain K', 'Time constant τ', 'Dead time θ'],
                    'accuracy_needed': '±10% for good IMC performance'
                },
                'model_validation': {
                    'criteria': ['Step response fit', 'Frequency response match', 'Steady-state gain'],
                    'tools': ['Cross-validation', 'Residual analysis', 'Prediction error methods']
                }
            },
            
            'implementation_considerations': {
                'digital_implementation': {
                    'sampling_time': 'Should be 5-10 times faster than λ',
                    'numerical_methods': 'Tustin transformation for filter discretization',
                    'computational_load': 'Moderate - requires model evaluation at each step'
                },
                'robustness_analysis': {
                    'gain_margin': 'Typically > 3 (9.5 dB) with proper λ selection',
                    'phase_margin': 'Typically > 45° with proper filter design',
                    'model_uncertainty': 'λ should account for expected model errors'
                },
                'performance_monitoring': {
                    'model_mismatch': 'Monitor prediction error for model degradation',
                    'adaptation': 'Consider adaptive IMC for time-varying processes',
                    'backup_control': 'Fallback to PID if model becomes unreliable'
                }
            },
            
            'advantages_over_pid': {
                'systematic_tuning': 'Only one main parameter (λ) to tune',
                'dead_time_handling': 'Explicit compensation for process delays',
                'setpoint_tracking': 'Theoretically perfect tracking with exact model',
                'disturbance_rejection': 'Excellent rejection through model prediction'
            },
            
            'limitations': {
                'model_dependency': 'Performance degrades with model inaccuracy',
                'inverse_model': 'Requires invertible process model',
                'computational_cost': 'Higher than PID due to model calculations',
                'nonlinear_processes': 'Limited to linear or linearized models'
            },
            
            'current_state': {
                'controller_name': self.name,
                'last_update_time': self.last_update_time,
                'history_length': len(self.time_history),
                'output_limits': getattr(self, 'output_limits', 'Not set'),
                'internal_states': {
                    'integral_term': getattr(self, '_integral', 0),
                    'last_error': getattr(self, '_last_error', 'Not available')
                }
            }
        }
