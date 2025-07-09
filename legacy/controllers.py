"""
Controller Module for SPROCLIB - Standard Process Control Library (Legacy Interface)

This module maintains backward compatibility by importing from the new modular 
controller package structure. For new code, import directly from the controller package:

New modular imports (recommended):
    from controller.pid.PIDController import PIDController
    from controller.tuning.ZieglerNicholsTuning import ZieglerNicholsTuning
    from controller.tuning.AMIGOTuning import AMIGOTuning
    from controller.tuning.RelayTuning import RelayTuning
    from controller.model_based.IMCController import IMCController
    from controller.state_space.StateSpaceController import StateSpaceController

Legacy imports (backward compatibility):
    from controllers import PIDController, ZieglerNicholsTuning, AMIGOTuning, RelayTuning, IMCController

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

# Import from new modular structure for backward compatibility
from controller.pid.PIDController import PIDController
from controller.tuning.ZieglerNicholsTuning import ZieglerNicholsTuning
from controller.tuning.AMIGOTuning import AMIGOTuning
from controller.tuning.RelayTuning import RelayTuning
from controller.base.TuningRule import TuningRule
from controller.model_based.IMCController import IMCController, FOPDTModel, SOPDTModel, tune_imc_lambda
from controller.state_space.StateSpaceController import StateSpaceController, StateSpaceModel

# Make all classes available at module level for backward compatibility
__all__ = [
    'PIDController',
    'TuningRule', 
    'ZieglerNicholsTuning',
    'AMIGOTuning',
    'RelayTuning',
    'IMCController',
    'FOPDTModel',
    'SOPDTModel',
    'tune_imc_lambda',
    'StateSpaceController',
    'StateSpaceModel'
]
