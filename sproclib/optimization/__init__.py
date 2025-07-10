"""
Optimization Package for SPROCLIB - Standard Process Control Library

This package provides optimization tools for process control including
economic optimization, parameter estimation, and real-time optimization.

Classes:
    ProcessOptimization: General process optimization framework
    EconomicOptimization: Economic optimization and profit maximization
    ParameterEstimation: Parameter estimation from experimental data
    
Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from .process_optimization import ProcessOptimization
from .economic_optimization import EconomicOptimization
from .parameter_estimation import ParameterEstimation

__all__ = [
    'ProcessOptimization',
    'EconomicOptimization',
    'ParameterEstimation'
]
