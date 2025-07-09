"""
Tank Models for SPROCLIB

This package contains tank models for liquid storage and processing
applications in chemical process simulation and control.

Available Tank Models:
- Tank: Single gravity-drained tank
- InteractingTanks: Two tanks in series

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from .single import Tank
from .interacting import InteractingTanks

__all__ = ['Tank', 'InteractingTanks']
