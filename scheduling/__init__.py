"""
Scheduling Package for SPROCLIB - Standard Process Control Library

This package provides batch process scheduling tools including
State-Task Networks for production scheduling.

Classes:
    StateTaskNetwork: State-Task Network scheduling framework
    
Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from .state_task_network import StateTaskNetwork

__all__ = [
    'StateTaskNetwork'
]
