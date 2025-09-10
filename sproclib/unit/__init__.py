"""
Process Unit Models for SPROCLIB - Standard Process Control Library

This package contains modular process unit models organized by type.
Each unit is implemented as its own class in a separate directory 
for easy contribution and maintenance.

Available Units:
- base: Abstract base classes
- reactor: Reactor models (CSTR, PFR, Batch, Fixed Bed)
- tank: Tank models (Single, Interacting)
- heat_exchanger: Heat exchanger models
- distillation: Distillation models (Tray, Column)
- valve: Valve models (Control, Three-way)
- pump: Pump models (Centrifugal, Positive Displacement)
- compressor: Compressor models
- mixer: Mixer models for stream combining
- utilities: Linearization and analysis utilities

For Contributors:
Each process unit should be implemented in its own directory with:
- __init__.py: Main class implementation
- README.md: Documentation and usage examples
- examples.py: Usage examples (optional)
- tests.py: Unit tests (optional)

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

# Import base classes
from .base import ProcessModel

# Import core units that are known to work
from .reactor.cstr import CSTR
from .tank.interacting import InteractingTanks
from .heat_exchanger import HeatExchanger

# Import additional units with error handling
try:
    # Tank models
    from .tank import Tank
    
    # Pump models  
    from .pump import Pump, CentrifugalPump, PositiveDisplacementPump
    
    # Valve models
    from .valve import ControlValve, ThreeWayValve
    
    # Compressor models
    from .compressor import Compressor
    
    # Mixer models
    from .mixer import Mixer
    
    # Utilities
    from .utilities import LinearApproximation
    
    # Additional reactor models
    from .reactor.batch import BatchReactor
    from .reactor.plug_flow import PlugFlowReactor
    from .reactor.fixed_bed import FixedBedReactor
    from .reactor.semi_batch import SemiBatchReactor
    from .reactor.fluidized_bed import FluidizedBedReactor
    
    # Distillation models
    from .distillation.tray import DistillationTray
    from .distillation.column import BinaryDistillationColumn

except ImportError as e:
    print(f"Warning: Some units could not be imported: {e}")
    pass  # Some units may not be fully implemented yet

__all__ = [
    # Base classes
    'ProcessModel',
    
    # Core working units
    'CSTR',
    'InteractingTanks',
    'HeatExchanger',
]

# Add additional units to __all__ if they were successfully imported
import sys
current_module = sys.modules[__name__]

# Check what was successfully imported and add to __all__
optional_units = [
    'Tank', 'Pump', 'CentrifugalPump', 'PositiveDisplacementPump',
    'ControlValve', 'ThreeWayValve', 'Compressor', 'Mixer', 'LinearApproximation',
    'BatchReactor', 'PlugFlowReactor', 'FixedBedReactor', 'SemiBatchReactor',
    'FluidizedBedReactor', 'DistillationTray', 'BinaryDistillationColumn'
]

for unit in optional_units:
    if hasattr(current_module, unit):
        __all__.append(unit)
