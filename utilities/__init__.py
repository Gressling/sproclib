"""
Utilities Package for SPROCLIB - Standard Process Control Library

This package provides general utility functions for process control including
mathematical utilities, data processing, and helper functions.

Functions:
    step_response: Calculate step response of transfer functions
    bode_plot: Generate Bode plots for frequency analysis
    linearize: Linearize nonlinear models around operating points
    tune_pid: Automatic PID tuning using empirical rules
    
Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from .math_utils import *
from .data_utils import *
from .control_utils import *

__all__ = [
    # Math utilities
    'step_response',
    'bode_plot', 
    'linearize',
    'stability_check',
    
    # Data utilities
    'filter_data',
    'resample_data',
    'detect_outliers',
    
    # Control utilities
    'tune_pid',
    'simulate_process',
    'calculate_ise',
    'calculate_iae'
]
