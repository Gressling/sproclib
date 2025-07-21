"""
Optimization Package for SPROCLIB - Standard Process Control Library

This package provides optimization tools for process control including
economic optimization, parameter estimation, and process optimization.

Subpackages:
    economic_optimization: Economic optimization and profit maximization
    parameter_estimation: Parameter estimation from experimental data
    process_optimization: General process optimization framework
    
Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from .economic_optimization import EconomicOptimization
from .parameter_estimation import ParameterEstimation  
from .process_optimization import ProcessOptimization

__all__ = [
    'EconomicOptimization',
    'ParameterEstimation',
    'ProcessOptimization'
]
