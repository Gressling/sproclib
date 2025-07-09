"""
State-Space Controllers for SPROCLIB - Standard Process Control Library

This package implements state-space control methods for advanced process control
applications, including MIMO systems, reactor networks, and coupled process units.

Classes:
    StateSpaceModel: State-space model representation (A, B, C, D matrices)
    StateSpaceController: Advanced state-space controller with LQR, pole placement, and observer design
    
Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from .StateSpaceController import StateSpaceController, StateSpaceModel

__all__ = [
    'StateSpaceController',
    'StateSpaceModel'
]
