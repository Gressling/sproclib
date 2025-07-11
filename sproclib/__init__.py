"""
SPROCLIB - Standard Process Control Library

A library for chemical process control. Provides essential classes 
and functions for PID control, process modeling, simulation, optimization, 
and advanced control techniques.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
Version: 2.0.4
"""

__version__ = "2.0.4"
__author__ = "Thorsten Gressling"
__email__ = "gressling@paramus.ai"

# Legacy imports for backward compatibility (with error handling)
try:
    from .controllers import PIDController, TuningRule
except ImportError:
    pass

try:
    from .models import (
        ProcessModel, CSTR, Tank, HeatExchanger, DistillationTray, BinaryDistillationColumn, 
        LinearApproximation, PlugFlowReactor, BatchReactor, FixedBedReactor, SemiBatchReactor,
        InteractingTanks, ControlValve, ThreeWayValve
    )
except ImportError:
    pass

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
