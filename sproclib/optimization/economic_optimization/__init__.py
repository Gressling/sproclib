"""
Economic Optimization Subpackage

This subpackage provides comprehensive economic optimization tools for 
chemical engineering applications including production planning, utility 
optimization, investment analysis, and economic model predictive control.

Classes:
    EconomicOptimization: Main economic optimization class with multiple algorithms

Functions:
    optimize_operation: Standalone operation optimization function

Example:
    >>> from sproclib.optimization.economic_optimization import EconomicOptimization
    >>> optimizer = EconomicOptimization("Production Planning")
    >>> result = optimizer.production_optimization(...)
"""

from .economic_optimization import EconomicOptimization, optimize_operation

__all__ = ['EconomicOptimization', 'optimize_operation']

# Version information
__version__ = '1.0.0'
__author__ = 'SPROCLIB Development Team'
