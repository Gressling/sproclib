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
