"""
Reactor Models for SPROCLIB

This package contains various reactor models for chemical process simulation
and control design. Each reactor type is organized in its own subpackage 
containing the class definition, documentation, tests, and examples.

Available Reactors:
- CSTR: Continuous Stirred Tank Reactor
- BatchReactor: Batch reactor with heating/cooling  
- PlugFlowReactor: Plug Flow Reactor with axial discretization
- FixedBedReactor: Fixed bed catalytic reactor
- SemiBatchReactor: Semi-batch reactor with feed control
- FluidizedBedReactor: Fluidized bed reactor with two-phase modeling

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

# Import all reactor classes from their subpackages
from .cstr import CSTR
from .batch import BatchReactor  
from .plug_flow import PlugFlowReactor
from .fixed_bed import FixedBedReactor
from .semi_batch import SemiBatchReactor
from .fluidized_bed import FluidizedBedReactor

__all__ = [
    'CSTR',
    'BatchReactor', 
    'PlugFlowReactor',
    'FixedBedReactor',
    'SemiBatchReactor',
    'FluidizedBedReactor'
]

# Package metadata
__version__ = '2.0.0'
__author__ = 'Thorsten Gressling'
__description__ = 'Chemical reactor models for process simulation'

# Reactor categories for easy discovery
REACTOR_CATEGORIES = {
    'continuous': ['CSTR', 'PlugFlowReactor'],
    'batch': ['BatchReactor', 'SemiBatchReactor'],
    'heterogeneous': ['FixedBedReactor', 'FluidizedBedReactor'],
    'homogeneous': ['CSTR', 'BatchReactor', 'PlugFlowReactor', 'SemiBatchReactor']
}

def list_reactors():
    """List all available reactor types."""
    return __all__

def get_reactor_info(reactor_name):
    """Get detailed information about a specific reactor type."""
    reactor_map = {
        'CSTR': CSTR,
        'BatchReactor': BatchReactor,
        'PlugFlowReactor': PlugFlowReactor, 
        'FixedBedReactor': FixedBedReactor,
        'SemiBatchReactor': SemiBatchReactor,
        'FluidizedBedReactor': FluidizedBedReactor
    }
    
    if reactor_name in reactor_map:
        reactor_class = reactor_map[reactor_name]
        if hasattr(reactor_class, 'describe'):
            return reactor_class().describe()
        else:
            return {
                'type': reactor_name,
                'description': f'{reactor_name} reactor model',
                'class': reactor_class
            }
    else:
        raise ValueError(f"Unknown reactor type: {reactor_name}. Available: {list_reactors()}")
