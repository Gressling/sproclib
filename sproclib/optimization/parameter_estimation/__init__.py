"""
Parameter Estimation Module for Chemical Process Engineering

This module provides comprehensive tools for estimating parameters from experimental data
in chemical engineering applications, including reaction kinetics, heat and mass transfer,
and thermodynamic properties.

Key Features:
- Linear and nonlinear parameter estimation
- Statistical uncertainty quantification
- Bayesian inference methods
- Model validation and diagnostics
- Economic impact analysis

Classes:
    ParameterEstimation: Main class for parameter estimation
    BayesianParameterEstimation: Bayesian inference methods
    MultiObjectiveEstimation: Multi-response parameter estimation
    
Functions:
    arrhenius_estimation: Specialized for Arrhenius parameter estimation
    heat_transfer_estimation: Heat transfer coefficient correlation
    mass_transfer_estimation: Mass transfer parameter estimation
    validate_model: Comprehensive model validation
    estimate_fopdt_parameters: FOPDT parameter estimation (legacy)
    
Examples:
    >>> from sproclib.optimization.parameter_estimation import ParameterEstimation
    >>> import numpy as np
    
    # Arrhenius parameter estimation
    >>> temps = np.array([300, 310, 320, 330, 340])
    >>> rates = np.array([0.001, 0.002, 0.004, 0.008, 0.015])
    >>> def arrhenius(T, k0, Ea):
    ...     return k0 * np.exp(-Ea / (8.314 * T))
    >>> estimator = ParameterEstimation(arrhenius, (temps, rates))
    >>> results = estimator.estimate_parameters()
    >>> print(f"Activation energy: {results.parameters[1]/1000:.1f} kJ/mol")
    
    # Heat transfer correlation
    >>> flows = np.array([10, 20, 30, 40, 50])
    >>> coeffs = np.array([250, 320, 380, 430, 470])
    >>> def correlation(flow, a, b):
    ...     return a * flow**b
    >>> estimator = ParameterEstimation(correlation, (flows, coeffs))
    >>> results = estimator.estimate_parameters()
    >>> print(f"Exponent: {results.parameters[1]:.3f}")

See Also:
    Process Optimization: Integration with optimization workflows
    Economic Optimization: Economic objective functions
    Unit Operations: Process models for parameter estimation
    
References:
    1. Bard, Y. (1974). Nonlinear Parameter Estimation. Academic Press.
    2. Englezos, P. & Kalogerakis, N. (2001). Applied Parameter Estimation 
       for Chemical Engineers. Marcel Dekker.
    3. Rawlings, J.B. & Ekerdt, J.G. (2002). Chemical Reactor Analysis 
       and Design Fundamentals. Nob Hill Publishing.
"""

from .parameter_estimation import ParameterEstimation, estimate_fopdt_parameters
from .example import main as run_example

__version__ = "1.0.0"
__author__ = "SProcLib Development Team"

# Define what gets imported with "from parameter_estimation import *"
__all__ = [
    'ParameterEstimation',
    'estimate_fopdt_parameters',
    'run_example',
    'quick_arrhenius_fit',
    'quick_power_law_fit'
]

# Module-level convenience functions
def quick_arrhenius_fit(temperatures, rate_constants, initial_guess=None):
    """
    Quick Arrhenius parameter estimation with default settings.
    
    Parameters
    ----------
    temperatures : array_like
        Temperature data (K)
    rate_constants : array_like  
        Rate constant data (same units as desired k0)
    initial_guess : list, optional
        Initial parameter guess [k0, Ea]. If None, uses automatic estimation.
        
    Returns
    -------
    dict
        Dictionary with 'k0', 'Ea', 'r_squared', and 'confidence_intervals'
        
    Examples
    --------
    >>> temps = [300, 310, 320, 330, 340]
    >>> rates = [0.001, 0.002, 0.004, 0.008, 0.015] 
    >>> results = quick_arrhenius_fit(temps, rates)
    >>> print(f"Ea = {results['Ea']/1000:.1f} kJ/mol")
    """
    import numpy as np
    
    def arrhenius_model(T, k0, Ea):
        R = 8.314  # J/(mol·K)
        return k0 * np.exp(-Ea / (R * T))
    
    if initial_guess is None:
        # Automatic initial guess from linear regression of ln(k) vs 1/T
        T_arr = np.array(temperatures)
        k_arr = np.array(rate_constants)
        
        ln_k = np.log(k_arr)
        inv_T = 1.0 / T_arr
        
        # Linear fit: ln(k) = ln(k0) - Ea/(R*T)
        coeffs = np.polyfit(inv_T, ln_k, 1)
        Ea_guess = -coeffs[0] * 8.314
        k0_guess = np.exp(coeffs[1])
        initial_guess = [k0_guess, Ea_guess]
    
    estimator = ParameterEstimation(
        model_function=arrhenius_model,
        experimental_data=(temperatures, rate_constants),
        initial_guess=initial_guess
    )
    
    results = estimator.estimate_parameters(confidence_level=0.95)
    
    return {
        'k0': results.parameters[0],
        'Ea': results.parameters[1], 
        'r_squared': results.r_squared,
        'confidence_intervals': {
            'k0': results.confidence_intervals[0],
            'Ea': results.confidence_intervals[1]
        },
        'full_results': results
    }

def quick_power_law_fit(x_data, y_data, initial_guess=None):
    """
    Quick power law fitting: y = a * x^b
    
    Parameters
    ----------
    x_data : array_like
        Independent variable data
    y_data : array_like
        Dependent variable data  
    initial_guess : list, optional
        Initial parameter guess [a, b]. If None, uses log-linear estimation.
        
    Returns
    -------
    dict
        Dictionary with 'a', 'b', 'r_squared', and 'confidence_intervals'
        
    Examples
    --------
    >>> flows = [10, 20, 30, 40, 50]
    >>> coeffs = [250, 320, 380, 430, 470]
    >>> results = quick_power_law_fit(flows, coeffs)
    >>> print(f"Exponent = {results['b']:.3f}")
    """
    import numpy as np
    
    def power_law_model(x, a, b):
        return a * x**b
    
    if initial_guess is None:
        # Log-linear estimation for initial guess
        x_arr = np.array(x_data)
        y_arr = np.array(y_data)
        
        ln_x = np.log(x_arr)
        ln_y = np.log(y_arr)
        
        # Linear fit: ln(y) = ln(a) + b*ln(x)
        coeffs = np.polyfit(ln_x, ln_y, 1)
        b_guess = coeffs[0]
        a_guess = np.exp(coeffs[1])
        initial_guess = [a_guess, b_guess]
    
    estimator = ParameterEstimation(
        model_function=power_law_model,
        experimental_data=(x_data, y_data),
        initial_guess=initial_guess
    )
    
    results = estimator.estimate_parameters(confidence_level=0.95)
    
    return {
        'a': results.parameters[0],
        'b': results.parameters[1],
        'r_squared': results.r_squared,
        'confidence_intervals': {
            'a': results.confidence_intervals[0],
            'b': results.confidence_intervals[1]
        },
        'full_results': results
    }

# Check dependencies and warn if missing
try:
    import scipy
    import numpy
    import matplotlib
except ImportError as e:
    import warnings
    warnings.warn(
        f"Parameter estimation module requires scipy, numpy, and matplotlib. "
        f"Missing dependency: {e.name}. Some functionality may be limited.",
        ImportWarning
    )
