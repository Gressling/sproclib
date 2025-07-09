"""
SPROCLIB - Standard Process Control Library

A library for chemical process control. Provides essential classes 
and functions for PID control, process modeling, simulation, optimization, 
and advanced control techniques.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
Version: 1.0.0
"""

# Legacy imports for backward compatibility
from .controllers import PIDController, TuningRule
from .models import (
    ProcessModel, CSTR, Tank, HeatExchanger, DistillationTray, BinaryDistillationColumn, 
    LinearApproximation, PlugFlowReactor, BatchReactor, FixedBedReactor, SemiBatchReactor,
    InteractingTanks, ControlValve, ThreeWayValve
)
from .analysis import TransferFunction, Simulation, Optimization, StateTaskNetwork
from .functions import (
    step_response, bode_plot, linearize, tune_pid, simulate_process,
    optimize_operation, fit_fopdt, stability_analysis, disturbance_rejection,
    model_predictive_control
)

# Modern modular imports (recommended for new code)
# Physical process units
from .unit.tank.Tank import Tank as UnitTank
from .unit.pump.Pump import Pump
from .unit.compressor.Compressor import Compressor

# Controllers
from .controller.pid.PIDController import PIDController as ModularPIDController
from .controller.tuning.ZieglerNicholsTuning import ZieglerNicholsTuning

__version__ = "1.0.0"
__author__ = "Thorsten Gressling"

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
