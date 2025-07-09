"""
Model Identification for SPROCLIB

This module provides tools for system identification and model fitting
from experimental data or step response tests.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
from typing import Optional, Tuple, Dict, Any, List
from scipy import optimize
import logging

logger = logging.getLogger(__name__)


class ModelIdentification:
    """System identification and model fitting tools."""
    
    def __init__(self, name: str = "Model Identification"):
        """
        Initialize model identification.
        
        Args:
            name: Identification name
        """
        self.name = name
        self.results = {}
    
    def fit_fopdt(
        self,
        t_data: np.ndarray,
        y_data: np.ndarray,
        step_magnitude: float = 1.0,
        initial_guess: Optional[Tuple[float, float, float]] = None
    ) -> Dict[str, Any]:
        """
        Fit First Order Plus Dead Time model to step response data.
        
        Args:
            t_data: Time data
            y_data: Response data
            step_magnitude: Magnitude of step input
            initial_guess: Initial parameter guess (K, tau, theta)
            
        Returns:
            Dictionary with fitted parameters and metrics
        """
        def fopdt_response(t, K, tau, theta):
            """FOPDT step response"""
            response = np.zeros_like(t)
            mask = t >= theta
            response[mask] = K * (1 - np.exp(-(t[mask] - theta) / tau))
            return response
        
        def objective(params):
            K, tau, theta = params
            y_pred = fopdt_response(t_data, K, tau, theta) * step_magnitude
            return np.sum((y_data - y_pred) ** 2)
        
        # Initial guess
        if initial_guess is None:
            K_guess = np.max(y_data) / step_magnitude
            tau_guess = t_data[-1] / 5  # Rough estimate
            theta_guess = 0.1
            initial_guess = (K_guess, tau_guess, theta_guess)
        
        # Optimization bounds
        bounds = [(0.1, 10 * initial_guess[0]),   # K
                  (0.01, 10 * initial_guess[1]),  # tau
                  (0, t_data[-1] / 2)]            # theta
        
        try:
            result = optimize.minimize(
                objective, initial_guess, bounds=bounds, method='L-BFGS-B'
            )
            
            if result.success:
                K_fit, tau_fit, theta_fit = result.x
                y_fit = fopdt_response(t_data, K_fit, tau_fit, theta_fit) * step_magnitude
                
                # Calculate R-squared
                ss_res = np.sum((y_data - y_fit) ** 2)
                ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
                r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
                
                logger.info(f"FOPDT fit successful: K={K_fit:.3f}, τ={tau_fit:.3f}, θ={theta_fit:.3f}")
                
                self.results = {
                    'K': K_fit,
                    'tau': tau_fit,
                    'theta': theta_fit,
                    'r_squared': r_squared,
                    'fitted_response': y_fit,
                    'residuals': y_data - y_fit,
                    'success': True
                }
            else:
                logger.error(f"FOPDT fit failed: {result.message}")
                self.results = {
                    'K': np.nan,
                    'tau': np.nan,
                    'theta': np.nan,
                    'r_squared': 0,
                    'success': False,
                    'message': result.message
                }
        
        except Exception as e:
            logger.error(f"FOPDT fit error: {e}")
            self.results = {
                'K': np.nan,
                'tau': np.nan,
                'theta': np.nan,
                'r_squared': 0,
                'success': False,
                'error': str(e)
            }
        
        return self.results
    
    def fit_sopdt(
        self,
        t_data: np.ndarray,
        y_data: np.ndarray,
        step_magnitude: float = 1.0,
        initial_guess: Optional[Tuple[float, float, float, float]] = None
    ) -> Dict[str, Any]:
        """
        Fit Second Order Plus Dead Time model to step response data.
        
        Args:
            t_data: Time data
            y_data: Response data
            step_magnitude: Magnitude of step input
            initial_guess: Initial parameter guess (K, tau1, tau2, theta)
            
        Returns:
            Dictionary with fitted parameters and metrics
        """
        def sopdt_response(t, K, tau1, tau2, theta):
            """SOPDT step response"""
            response = np.zeros_like(t)
            mask = t >= theta
            t_active = t[mask] - theta
            
            if abs(tau1 - tau2) < 1e-6:
                # Repeated roots case
                tau = tau1
                response[mask] = K * (1 - (1 + t_active/tau) * np.exp(-t_active/tau))
            else:
                # Distinct roots case
                a1 = tau1 / (tau1 - tau2)
                a2 = tau2 / (tau2 - tau1)
                exp1 = np.exp(-t_active / tau1)
                exp2 = np.exp(-t_active / tau2)
                response[mask] = K * (1 + a1 * exp1 + a2 * exp2)
            
            return response
        
        def objective(params):
            K, tau1, tau2, theta = params
            y_pred = sopdt_response(t_data, K, tau1, tau2, theta) * step_magnitude
            return np.sum((y_data - y_pred) ** 2)
        
        # Initial guess
        if initial_guess is None:
            K_guess = np.max(y_data) / step_magnitude
            tau1_guess = t_data[-1] / 8
            tau2_guess = t_data[-1] / 4
            theta_guess = 0.1
            initial_guess = (K_guess, tau1_guess, tau2_guess, theta_guess)
        
        # Optimization bounds
        bounds = [(0.1, 10 * initial_guess[0]),   # K
                  (0.01, 10 * initial_guess[1]),  # tau1
                  (0.01, 10 * initial_guess[2]),  # tau2
                  (0, t_data[-1] / 2)]            # theta
        
        try:
            result = optimize.minimize(
                objective, initial_guess, bounds=bounds, method='L-BFGS-B'
            )
            
            if result.success:
                K_fit, tau1_fit, tau2_fit, theta_fit = result.x
                y_fit = sopdt_response(t_data, K_fit, tau1_fit, tau2_fit, theta_fit) * step_magnitude
                
                # Calculate R-squared
                ss_res = np.sum((y_data - y_fit) ** 2)
                ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
                r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
                
                logger.info(f"SOPDT fit successful: K={K_fit:.3f}, τ1={tau1_fit:.3f}, τ2={tau2_fit:.3f}, θ={theta_fit:.3f}")
                
                return {
                    'K': K_fit,
                    'tau1': tau1_fit,
                    'tau2': tau2_fit,
                    'theta': theta_fit,
                    'r_squared': r_squared,
                    'fitted_response': y_fit,
                    'residuals': y_data - y_fit,
                    'success': True
                }
            else:
                logger.error(f"SOPDT fit failed: {result.message}")
                return {
                    'K': np.nan,
                    'tau1': np.nan,
                    'tau2': np.nan,
                    'theta': np.nan,
                    'r_squared': 0,
                    'success': False,
                    'message': result.message
                }
        
        except Exception as e:
            logger.error(f"SOPDT fit error: {e}")
            return {
                'K': np.nan,
                'tau1': np.nan,
                'tau2': np.nan,
                'theta': np.nan,
                'r_squared': 0,
                'success': False,
                'error': str(e)
            }
    
    def fit_transfer_function(
        self,
        freq_data: np.ndarray,
        magnitude_data: np.ndarray,
        phase_data: np.ndarray,
        model_order: Tuple[int, int] = (2, 2)
    ) -> Dict[str, Any]:
        """
        Fit transfer function to frequency response data.
        
        Args:
            freq_data: Frequency data [rad/s]
            magnitude_data: Magnitude data (linear scale)
            phase_data: Phase data [radians]
            model_order: Transfer function order (numerator, denominator)
            
        Returns:
            Dictionary with fitted transfer function
        """
        from scipy import signal
        
        # Convert to complex frequency response
        H_data = magnitude_data * np.exp(1j * phase_data)
        
        # Use vector fitting or least squares approach
        # This is a simplified implementation - in practice, use specialized tools
        
        num_order, den_order = model_order
        
        try:
            # Simplified fitting using least squares
            # Create complex frequency points
            s_data = 1j * freq_data
            
            # Set up least squares problem (simplified)
            # In practice, this requires more sophisticated vector fitting algorithms
            
            # For now, return a simple first-order fit
            if len(freq_data) > 2:
                # Simple magnitude-based fitting
                low_freq_gain = magnitude_data[0] if len(magnitude_data) > 0 else 1.0
                
                # Estimate time constant from -3dB frequency
                mag_db = 20 * np.log10(magnitude_data + 1e-12)
                try:
                    idx_3db = np.where(mag_db <= (20*np.log10(low_freq_gain) - 3))[0]
                    if len(idx_3db) > 0:
                        freq_3db = freq_data[idx_3db[0]]
                        tau_est = 1.0 / freq_3db
                    else:
                        tau_est = 1.0
                except:
                    tau_est = 1.0
                
                # Create simple first-order model
                num = [low_freq_gain]
                den = [tau_est, 1]
                
                tf_fit = signal.TransferFunction(num, den)
                
                # Calculate fit quality
                _, mag_fit, phase_fit = signal.bode(tf_fit, freq_data)
                
                mag_error = np.mean((magnitude_data - mag_fit)**2)
                phase_error = np.mean((phase_data - phase_fit)**2)
                
                return {
                    'numerator': num,
                    'denominator': den,
                    'transfer_function': tf_fit,
                    'magnitude_error': mag_error,
                    'phase_error': phase_error,
                    'success': True
                }
            else:
                return {
                    'success': False,
                    'error': 'Insufficient data points'
                }
        
        except Exception as e:
            logger.error(f"Transfer function fitting error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def validate_model(
        self,
        model_params: Dict[str, float],
        validation_data: Dict[str, np.ndarray],
        model_type: str = "fopdt"
    ) -> Dict[str, float]:
        """
        Validate fitted model against independent validation data.
        
        Args:
            model_params: Fitted model parameters
            validation_data: Dictionary with 't' and 'y' arrays
            model_type: Type of model ('fopdt', 'sopdt')
            
        Returns:
            Dictionary with validation metrics
        """
        t_val = validation_data['t']
        y_val = validation_data['y']
        
        if model_type.lower() == "fopdt":
            K = model_params['K']
            tau = model_params['tau']
            theta = model_params['theta']
            
            # Generate model prediction
            y_pred = np.zeros_like(t_val)
            mask = t_val >= theta
            t_active = t_val[mask] - theta
            y_pred[mask] = K * (1 - np.exp(-t_active / tau))
        
        elif model_type.lower() == "sopdt":
            K = model_params['K']
            tau1 = model_params['tau1']
            tau2 = model_params['tau2']
            theta = model_params['theta']
            
            # Generate model prediction
            y_pred = np.zeros_like(t_val)
            mask = t_val >= theta
            t_active = t_val[mask] - theta
            
            if abs(tau1 - tau2) < 1e-6:
                # Repeated roots
                tau = tau1
                y_pred[mask] = K * (1 - (1 + t_active/tau) * np.exp(-t_active/tau))
            else:
                # Distinct roots
                a1 = tau1 / (tau1 - tau2)
                a2 = tau2 / (tau2 - tau1)
                exp1 = np.exp(-t_active / tau1)
                exp2 = np.exp(-t_active / tau2)
                y_pred[mask] = K * (1 + a1 * exp1 + a2 * exp2)
        
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # Calculate validation metrics
        mse = np.mean((y_val - y_pred)**2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(y_val - y_pred))
        
        # R-squared
        ss_res = np.sum((y_val - y_pred)**2)
        ss_tot = np.sum((y_val - np.mean(y_val))**2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        return {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'r_squared': r_squared,
            'predicted_response': y_pred
        }

# Standalone function wrappers for backward compatibility
def fit_fopdt(
    t_data: np.ndarray,
    y_data: np.ndarray,
    step_magnitude: float = 1.0,
    initial_guess: Optional[Tuple[float, float, float]] = None
) -> Dict[str, float]:
    """
    Fit First Order Plus Dead Time model to step response data.
    
    Args:
        t_data: Time data
        y_data: Response data
        step_magnitude: Magnitude of step input
        initial_guess: Initial parameter guess (K, tau, theta)
        
    Returns:
        Dictionary with fitted parameters and metrics
    """
    identifier = ModelIdentification()
    return identifier.fit_fopdt(t_data, y_data, step_magnitude, initial_guess)
