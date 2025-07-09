"""
Math Utilities for SPROCLIB

This module provides mathematical utility functions for process control
including signal processing, numerical methods, and mathematical operations.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
from typing import Optional, Tuple, Dict, Any, List
from scipy import signal
import logging

logger = logging.getLogger(__name__)


def step_response(
    system,
    t: Optional[np.ndarray] = None,
    t_final: float = 10.0,
    input_magnitude: float = 1.0
) -> Dict[str, np.ndarray]:
    """
    Calculate step response of a system.
    
    Args:
        system: Transfer function object or (num, den) tuple
        t: Time vector (optional)
        t_final: Final time if t not provided
        input_magnitude: Step magnitude
        
    Returns:
        Dictionary with 't' and 'y' arrays
    """
    if hasattr(system, 'sys'):
        # TransferFunction object
        sys = system.sys
    else:
        # (num, den) tuple
        num, den = system
        sys = signal.TransferFunction(num, den)
    
    if t is None:
        t = np.linspace(0, t_final, 1000)
    
    tout, yout = signal.step(sys, T=t)
    yout *= input_magnitude
    
    return {'t': tout, 'y': yout}


def bode_plot(
    system,
    w: Optional[np.ndarray] = None,
    plot: bool = True,
    title: str = "Bode Plot"
) -> Dict[str, np.ndarray]:
    """
    Generate Bode plot for frequency response analysis.
    
    Args:
        system: Transfer function object or (num, den) tuple
        w: Frequency vector (optional)
        plot: Whether to create plot
        title: Plot title
        
    Returns:
        Dictionary with frequency, magnitude, and phase data
    """
    import matplotlib.pyplot as plt
    
    if hasattr(system, 'sys'):
        sys = system.sys
    else:
        num, den = system
        sys = signal.TransferFunction(num, den)
    
    if w is None:
        w = np.logspace(-2, 2, 1000)
    
    w, mag, phase = signal.bode(sys, w)
    
    if plot:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Magnitude plot
        ax1.semilogx(w/(2*np.pi), 20*np.log10(mag))
        ax1.set_ylabel('Magnitude (dB)')
        ax1.grid(True, which='both', alpha=0.3)
        ax1.set_title(title)
        
        # Phase plot
        ax2.semilogx(w/(2*np.pi), np.degrees(phase))
        ax2.set_ylabel('Phase (degrees)')
        ax2.set_xlabel('Frequency (Hz)')
        ax2.grid(True, which='both', alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    return {
        'frequency': w,
        'magnitude': mag,
        'phase': phase,
        'magnitude_db': 20*np.log10(mag),
        'phase_deg': np.degrees(phase)
    }


def linearize(
    model_func,
    x_ss: np.ndarray,
    u_ss: np.ndarray,
    epsilon: float = 1e-6
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Linearize a nonlinear model around an operating point.
    
    Args:
        model_func: Function f(x, u) returning dx/dt
        x_ss: Steady-state states
        u_ss: Steady-state inputs
        epsilon: Perturbation size for finite differences
        
    Returns:
        A, B matrices for linear model dx/dt = A*x + B*u
    """
    n_states = len(x_ss)
    n_inputs = len(u_ss)
    
    # Calculate A matrix (∂f/∂x)
    A = np.zeros((n_states, n_states))
    f0 = model_func(x_ss, u_ss)
    
    for i in range(n_states):
        x_pert = x_ss.copy()
        x_pert[i] += epsilon
        f_pert = model_func(x_pert, u_ss)
        A[:, i] = (f_pert - f0) / epsilon
    
    # Calculate B matrix (∂f/∂u)
    B = np.zeros((n_states, n_inputs))
    
    for i in range(n_inputs):
        u_pert = u_ss.copy()
        u_pert[i] += epsilon
        f_pert = model_func(x_ss, u_pert)
        B[:, i] = (f_pert - f0) / epsilon
    
    return A, B


def stability_check(A: np.ndarray) -> bool:
    """
    Check if a linear system is stable.
    
    Args:
        A: State matrix
        
    Returns:
        True if stable, False otherwise
    """
    eigenvalues = np.linalg.eigvals(A)
    return np.all(np.real(eigenvalues) < 0)


def routh_hurwitz(coeffs: np.ndarray) -> Dict[str, Any]:
    """
    Routh-Hurwitz stability criterion.
    
    Args:
        coeffs: Characteristic polynomial coefficients
        
    Returns:
        Dictionary with stability analysis
    """
    n = len(coeffs)
    
    # Create Routh array
    routh_array = np.zeros((n, (n + 1) // 2))
    
    # Fill first two rows
    routh_array[0, :] = coeffs[::2]
    if n > 1:
        routh_array[1, :len(coeffs[1::2])] = coeffs[1::2]
    
    # Fill remaining rows
    for i in range(2, n):
        for j in range((n - i + 1) // 2):
            if routh_array[i-1, 0] != 0:
                routh_array[i, j] = (routh_array[i-1, 0] * routh_array[i-2, j+1] - 
                                   routh_array[i-2, 0] * routh_array[i-1, j+1]) / routh_array[i-1, 0]
    
    # Count sign changes in first column
    first_col = routh_array[:, 0]
    sign_changes = 0
    for i in range(1, len(first_col)):
        if first_col[i] * first_col[i-1] < 0:
            sign_changes += 1
    
    stable = sign_changes == 0
    
    return {
        'stable': stable,
        'routh_array': routh_array,
        'sign_changes': sign_changes,
        'unstable_poles': sign_changes
    }


def frequency_response(
    num: np.ndarray,
    den: np.ndarray,
    w: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate frequency response.
    
    Args:
        num: Numerator coefficients
        den: Denominator coefficients
        w: Frequency vector
        
    Returns:
        Magnitude and phase arrays
    """
    sys = signal.TransferFunction(num, den)
    w, mag, phase = signal.bode(sys, w)
    return mag, phase


__all__ = [
    'step_response',
    'bode_plot',
    'linearize',
    'stability_check',
    'routh_hurwitz',
    'frequency_response'
]
