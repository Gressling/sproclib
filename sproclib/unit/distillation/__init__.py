"""
Distillation Models for SPROCLIB

This package contains distillation models for separation process
simulation and control design.

Available Distillation Models:
- DistillationTray: Individual tray model for binary systems
- BinaryDistillationColumn: Complete column model

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from .tray import DistillationTray
from .column import BinaryDistillationColumn

__all__ = ['DistillationTray', 'BinaryDistillationColumn']
