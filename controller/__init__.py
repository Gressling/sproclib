"""
Controller Package for SPROCLIB - Standard Process Control Library

This package provides modular controller implementations including PID controllers,
model-based controllers, and various tuning methods for automated parameter selection.

The package is organized as follows:
- base: Abstract base classes for controllers and tuning rules
- pid: PID controller implementations  
- tuning: Various tuning methods (Ziegler-Nichols, AMIGO, Relay)
- model_based: Model-based controllers (IMC, etc.)

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

# Import base classes
from .base import TuningRule

# Import PID controllers
from .pid import PIDController

# Import tuning methods
from .tuning import ZieglerNicholsTuning, AMIGOTuning, RelayTuning

# Import model-based controllers
from .model_based import IMCController, FOPDTModel, SOPDTModel, tune_imc_lambda

# Import state-space controllers
from .state_space import StateSpaceController, StateSpaceModel

# Backward compatibility imports (maintain legacy interface)
from .pid.PIDController import PIDController
from .tuning.ZieglerNicholsTuning import ZieglerNicholsTuning
from .tuning.AMIGOTuning import AMIGOTuning
from .tuning.RelayTuning import RelayTuning
from .base.TuningRule import TuningRule

__all__ = [
    # Base classes
    'TuningRule',
    
    # PID Controllers
    'PIDController',
    
    # Tuning Methods
    'ZieglerNicholsTuning',
    'AMIGOTuning', 
    'RelayTuning',
    
    # Model-Based Controllers
    'IMCController',
    'FOPDTModel',
    'SOPDTModel',
    'tune_imc_lambda',
    
    # State-Space Controllers
    'StateSpaceController',
    'StateSpaceModel'
]
