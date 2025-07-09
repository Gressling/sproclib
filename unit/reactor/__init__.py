"""
Reactor Models for SPROCLIB

This package contains various reactor models for chemical process simulation
and control design.

Available Reactors:
- CSTR: Continuous Stirred Tank Reactor
- PFR: Plug Flow Reactor with axial discretization
- BatchReactor: Batch reactor with heating/cooling
- FixedBedReactor: Fixed bed catalytic reactor

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from .cstr import CSTR
from .pfr import PlugFlowReactor
from .batch import BatchReactor
from .fixed_bed import FixedBedReactor

__all__ = ['CSTR', 'PlugFlowReactor', 'BatchReactor', 'FixedBedReactor']
