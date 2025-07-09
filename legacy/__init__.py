"""
Legacy Module for SPROCLIB - Standard Process Control Library

This package contains backward compatibility wrappers for legacy code.
New code should use the modern modular packages instead.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import warnings

# Issue deprecation warning when legacy package is imported
warnings.warn(
    "The legacy package is deprecated. Please migrate to the new modular structure: "
    "analysis/, simulation/, optimization/, scheduling/, utilities/",
    DeprecationWarning,
    stacklevel=2
)

# Re-export legacy classes and functions for convenience
from .analysis import TransferFunction, Simulation, Optimization, StateTaskNetwork
from .functions import (
    step_response, bode_plot, linearize, tune_pid, simulate_process,
    optimize_operation, fit_fopdt, stability_analysis, disturbance_rejection,
    model_predictive_control
)

__all__ = [
    # Legacy classes
    'TransferFunction', 'Simulation', 'Optimization', 'StateTaskNetwork',
    # Legacy functions  
    'step_response', 'bode_plot', 'linearize', 'tune_pid', 'simulate_process',
    'optimize_operation', 'fit_fopdt', 'stability_analysis', 'disturbance_rejection',
    'model_predictive_control'
]
