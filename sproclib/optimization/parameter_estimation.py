"""
Parameter Estimation for SPROCLIB

This module provides parameter estimation tools for process control
systems using experimental data and optimization techniques.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
from typing import Optional, Tuple, Dict, Any, List, Callable
from scipy.optimize import minimize, differential_evolution
import logging

logger = logging.getLogger(__name__)


class ParameterEstimation:
    """Parameter estimation for process models."""
    
    def __init__(self, name: str = "Parameter Estimation"):
        """
        Initialize parameter estimation.
        
        Args:
            name: Estimation name
        """
        self.name = name
        self.results = {}
        
        logger.info(f"Parameter estimation '{name}' initialized")
    
    def estimate_parameters(
        self,
        model_func: Callable,
        t_data: np.ndarray,
        y_data: np.ndarray,
        param_bounds: List[Tuple[float, float]],
        initial_guess: Optional[np.ndarray] = None,
        method: str = 'least_squares'
    ) -> Dict[str, Any]:
        """
        Estimate model parameters from experimental data.
        
        Args:
            model_func: Model function that takes (t, params) and returns y
            t_data: Time data
            y_data: Output data
            param_bounds: Parameter bounds [(min, max), ...]
            initial_guess: Initial parameter guess
            method: Estimation method
            
        Returns:
            Parameter estimation results
        """
        def objective(params):
            """Objective function for parameter estimation."""
            try:
                y_pred = model_func(t_data, params)
                residuals = y_data - y_pred
                return np.sum(residuals**2)  # Sum of squared errors
            except Exception as e:
                logger.warning(f"Model evaluation error: {e}")
                return 1e6  # Large penalty for invalid parameters
        
        try:
            if method.lower() == 'least_squares':
                if initial_guess is None:
                    # Use midpoint of bounds as initial guess
                    initial_guess = np.array([(b[0] + b[1]) / 2 for b in param_bounds])
                
                result = minimize(
                    objective, initial_guess, method='L-BFGS-B',
                    bounds=param_bounds
                )
                
            elif method.lower() == 'differential_evolution':
                result = differential_evolution(
                    objective, param_bounds, seed=42
                )
                
            else:
                raise ValueError(f"Unknown estimation method: {method}")
            
            if result.success:
                # Calculate model predictions and statistics
                y_pred = model_func(t_data, result.x)
                residuals = y_data - y_pred
                mse = np.mean(residuals**2)
                rmse = np.sqrt(mse)
                
                # R-squared
                ss_res = np.sum(residuals**2)
                ss_tot = np.sum((y_data - np.mean(y_data))**2)
                r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
                
                self.results = {
                    'success': True,
                    'parameters': result.x,
                    'objective_value': result.fun,
                    'y_predicted': y_pred,
                    'residuals': residuals,
                    'mse': mse,
                    'rmse': rmse,
                    'r_squared': r_squared,
                    'method': method,
                    'message': result.message
                }
                
                logger.info(f"Parameter estimation successful: RMSE = {rmse:.6f}, R² = {r_squared:.4f}")
                
            else:
                self.results = {
                    'success': False,
                    'message': result.message,
                    'method': method
                }
                logger.error(f"Parameter estimation failed: {result.message}")
            
            return self.results
            
        except Exception as e:
            logger.error(f"Parameter estimation error: {e}")
            return {
                'success': False,
                'error': str(e),
                'method': method
            }
    
    def validate_model(
        self,
        model_func: Callable,
        parameters: np.ndarray,
        t_validation: np.ndarray,
        y_validation: np.ndarray
    ) -> Dict[str, Any]:
        """
        Validate model with independent validation data.
        
        Args:
            model_func: Model function
            parameters: Estimated parameters
            t_validation: Validation time data
            y_validation: Validation output data
            
        Returns:
            Validation results
        """
        try:
            # Generate predictions
            y_pred = model_func(t_validation, parameters)
            
            # Calculate validation metrics
            residuals = y_validation - y_pred
            mse = np.mean(residuals**2)
            rmse = np.sqrt(mse)
            mae = np.mean(np.abs(residuals))
            
            # R-squared
            ss_res = np.sum(residuals**2)
            ss_tot = np.sum((y_validation - np.mean(y_validation))**2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            validation_results = {
                'y_predicted': y_pred,
                'residuals': residuals,
                'mse': mse,
                'rmse': rmse,
                'mae': mae,
                'r_squared': r_squared,
                'validation_points': len(y_validation)
            }
            
            logger.info(f"Model validation: RMSE = {rmse:.6f}, R² = {r_squared:.4f}")
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Model validation error: {e}")
            return {'error': str(e)}


# Standalone functions for backward compatibility
def estimate_fopdt_parameters(
    t_data: np.ndarray,
    y_data: np.ndarray,
    step_magnitude: float = 1.0
) -> Dict[str, Any]:
    """
    Estimate FOPDT parameters from step response data.
    
    Args:
        t_data: Time data
        y_data: Step response data
        step_magnitude: Magnitude of step input
        
    Returns:
        Estimated FOPDT parameters
    """
    def fopdt_model(t, params):
        """FOPDT model: y = K * (1 - exp(-(t-theta)/tau)) for t >= theta"""
        K, tau, theta = params
        y = np.zeros_like(t)
        mask = t >= theta
        y[mask] = K * (1 - np.exp(-(t[mask] - theta) / tau))
        return y * step_magnitude
    
    # Parameter bounds: K, tau, theta
    param_bounds = [
        (0.1, 10.0),              # K: process gain
        (0.01, max(t_data)),      # tau: time constant
        (0.0, max(t_data) / 2)    # theta: dead time
    ]
    
    estimator = ParameterEstimation("FOPDT Estimation")
    result = estimator.estimate_parameters(
        fopdt_model, t_data, y_data, param_bounds
    )
    
    if result.get('success', False):
        K, tau, theta = result['parameters']
        result.update({
            'K': K,
            'tau': tau,
            'theta': theta
        })
    
    return result


__all__ = [
    'ParameterEstimation',
    'estimate_fopdt_parameters'
]
