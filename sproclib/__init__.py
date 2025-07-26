"""
SPROCLIB - Standard Process Control Library

A library for chemical process control. Provides essential classes 
and functions for PID control, process modeling, simulation, optimization, 
and advanced control techniques.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
Version: 3.0.0
"""

__version__ = "3.0.0"
__author__ = "Thorsten Gressling"
__email__ = "gressling@paramus.ai"

# Legacy imports for backward compatibility (with error handling)
try:
    from .controllers import PIDController, TuningRule
except ImportError:
    pass

# Import reactor models from new organized structure
try:
    from .unit.reactor import (
        CSTR, BatchReactor, PlugFlowReactor, FixedBedReactor, 
        SemiBatchReactor, FluidizedBedReactor
    )
except ImportError:
    # Fallback to old structure if new one not available
    CSTR = BatchReactor = PlugFlowReactor = FixedBedReactor = None
    SemiBatchReactor = FluidizedBedReactor = None

# Import other unit operations
try:
    from .unit.tank.Tank import Tank
    from .unit.heat_exchanger.HeatExchanger import HeatExchanger
    from .unit.distillation.DistillationTray import DistillationTray
    from .unit.distillation.BinaryDistillationColumn import BinaryDistillationColumn
    from .unit.valve.ControlValve import ControlValve
    from .unit.valve.ThreeWayValve import ThreeWayValve
except ImportError:
    # Create placeholder classes for backward compatibility
    Tank = HeatExchanger = DistillationTray = BinaryDistillationColumn = None
    ControlValve = ThreeWayValve = None

# Legacy models import (deprecated but maintained for compatibility)
try:
    from .models import (
        ProcessModel, LinearApproximation, InteractingTanks
    )
except ImportError:
    # Create basic ProcessModel if not available
    try:
        from .base import ProcessModel
    except ImportError:
        class ProcessModel:
            pass
    LinearApproximation = InteractingTanks = None

try:
    from .analysis import TransferFunction, Simulation, Optimization, StateTaskNetwork
except ImportError:
    pass

try:
    from .functions import (
        step_response, bode_plot, linearize, tune_pid, simulate_process,
        optimize_operation, fit_fopdt, stability_analysis, disturbance_rejection,
        model_predictive_control
    )
except ImportError:
    pass

# Modern modular imports (recommended for new code)
try:
    from .unit.tank.Tank import Tank as UnitTank
    from .unit.pump.Pump import Pump
    from .unit.compressor.Compressor import Compressor
except ImportError:
    pass

try:
    from .controller.pid.PIDController import PIDController as ModularPIDController
    from .controller.tuning.ZieglerNicholsTuning import ZieglerNicholsTuning
except ImportError:
    pass

__all__ = [
    # Classes
    "PIDController", "TuningRule", "ProcessModel", "CSTR", "Tank", 
    "HeatExchanger", "DistillationTray", "BinaryDistillationColumn", "LinearApproximation", 
    "PlugFlowReactor", "BatchReactor", "FixedBedReactor", "SemiBatchReactor", "InteractingTanks",
    "ControlValve", "ThreeWayValve",
    "TransferFunction", "Simulation", "Optimization", "StateTaskNetwork",
    # Functions
    "step_response", "bode_plot", "linearize", "tune_pid", "simulate_process",
    "optimize_operation", "fit_fopdt", "stability_analysis", "disturbance_rejection",
    "model_predictive_control"
]
