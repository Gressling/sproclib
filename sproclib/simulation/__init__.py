"""
Simulation Package for SPROCLIB - Standard Process Control Library

This package provides comprehensive simulation tools for process control systems,
including dynamic simulation and process analysis.

Classes:
    ProcessSimulation: Dynamic process simulation with control loops
    
Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from .process_simulation import ProcessSimulation

__all__ = [
    'ProcessSimulation'
]
