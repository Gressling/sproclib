"""
Legacy Functions Module for SPROCLIB - Standard Process Control Library

This module provides backward compatibility for legacy function-based code.
New code should import from the modular packages:
- analysis.transfer_function for transfer function utilities
- analysis.system_analysis for system analysis functions
- analysis.model_identification for model fitting functions
- utilities.control_utils for control design utilities
- simulation.process_simulation for simulation functions
- optimization.economic_optimization for optimization functions

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import warnings
from typing import Optional, Tuple, Dict, Any, List, Callable, Union, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from ..analysis.transfer_function import TransferFunction

# Import from new modular structure
try:
    # Try relative imports first (when used as a package)
    from ..analysis.system_analysis import (
        step_response as _step_response,
        bode_plot as _bode_plot,
        stability_analysis as _stability_analysis
    )
    from ..analysis.model_identification import fit_fopdt as _fit_fopdt
    from ..utilities.control_utils import (
        tune_pid as _tune_pid,
        linearize as _linearize,
        simulate_process as _simulate_process,
        model_predictive_control as _model_predictive_control,
        disturbance_rejection as _disturbance_rejection
    )
    from ..optimization.economic_optimization import optimize_operation as _optimize_operation
except ImportError:
    # Fall back to absolute imports (when used as standalone module)
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    
    from analysis.system_analysis import (
        step_response as _step_response,
        bode_plot as _bode_plot,
        stability_analysis as _stability_analysis
    )
    from analysis.model_identification import fit_fopdt as _fit_fopdt
    from utilities.control_utils import (
        tune_pid as _tune_pid,
        linearize as _linearize,
        simulate_process as _simulate_process,
        model_predictive_control as _model_predictive_control,
        disturbance_rejection as _disturbance_rejection
    )
    from optimization.economic_optimization import optimize_operation as _optimize_operation

# Backward compatibility warning
warnings.warn(
    "functions.py is deprecated. Please import from the modular packages: "
    "analysis.system_analysis, analysis.model_identification, utilities.control_utils, "
    "simulation.process_simulation, optimization.economic_optimization",
    DeprecationWarning,
    stacklevel=2
)


# Legacy function wrappers - pass through to new implementations
def step_response(
    system: Union['TransferFunction', Tuple[np.ndarray, np.ndarray]],
    t: Optional[np.ndarray] = None,
    t_final: float = 10.0,
    input_magnitude: float = 1.0
) -> Dict[str, np.ndarray]:
    """Legacy wrapper for analysis.system_analysis.step_response"""
    warnings.warn(
        "functions.step_response is deprecated. Use analysis.system_analysis.step_response instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return _step_response(system, t, t_final, input_magnitude)


def bode_plot(
    system: Union['TransferFunction', Tuple[np.ndarray, np.ndarray]],
    w: Optional[np.ndarray] = None,
    plot: bool = True,
    title: str = "Bode Plot"
) -> Dict[str, np.ndarray]:
    """Legacy wrapper for analysis.system_analysis.bode_plot"""
    warnings.warn(
        "functions.bode_plot is deprecated. Use analysis.system_analysis.bode_plot instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return _bode_plot(system, w, plot, title)


def linearize(
    model_func: Callable,
    x_ss: np.ndarray,
    u_ss: np.ndarray,
    epsilon: float = 1e-6
) -> Tuple[np.ndarray, np.ndarray]:
    """Legacy wrapper for utilities.control_utils.linearize"""
    warnings.warn(
        "functions.linearize is deprecated. Use utilities.control_utils.linearize instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return _linearize(model_func, x_ss, u_ss, epsilon)


def tune_pid(
    model_params: Dict[str, float],
    method: str = "ziegler_nichols",
    controller_type: str = "PID"
) -> Dict[str, float]:
    """Legacy wrapper for utilities.control_utils.tune_pid"""
    warnings.warn(
        "functions.tune_pid is deprecated. Use utilities.control_utils.tune_pid instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return _tune_pid(model_params, method, controller_type)


def simulate_process(
    model: Callable,
    t_span: Tuple[float, float],
    x0: np.ndarray,
    u_profile: Callable[[float], np.ndarray],
    method: str = 'RK45',
    max_step: Optional[float] = None
) -> Dict[str, np.ndarray]:
    """Legacy wrapper for utilities.control_utils.simulate_process"""
    warnings.warn(
        "functions.simulate_process is deprecated. Use utilities.control_utils.simulate_process instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return _simulate_process(model, t_span, x0, u_profile, method, max_step)


def optimize_operation(
    objective_func: Callable,
    x0: np.ndarray,
    constraints: Optional[List[Dict]] = None,
    bounds: Optional[List[Tuple]] = None,
    method: str = 'SLSQP'
) -> Dict[str, Any]:
    """Legacy wrapper for optimization.economic_optimization.optimize_operation"""
    warnings.warn(
        "functions.optimize_operation is deprecated. Use optimization.economic_optimization.optimize_operation instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return _optimize_operation(objective_func, x0, constraints, bounds, method)


def fit_fopdt(
    t_data: np.ndarray,
    y_data: np.ndarray,
    step_magnitude: float = 1.0,
    initial_guess: Optional[Tuple[float, float, float]] = None
) -> Dict[str, float]:
    """Legacy wrapper for analysis.model_identification.fit_fopdt"""
    warnings.warn(
        "functions.fit_fopdt is deprecated. Use analysis.model_identification.fit_fopdt instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return _fit_fopdt(t_data, y_data, step_magnitude, initial_guess)


def stability_analysis(
    A: np.ndarray,
    system_name: str = "System"
) -> Dict[str, Any]:
    """Legacy wrapper for analysis.system_analysis.stability_analysis"""
    warnings.warn(
        "functions.stability_analysis is deprecated. Use analysis.system_analysis.stability_analysis instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return _stability_analysis(A, system_name)


def disturbance_rejection(
    plant_tf: Tuple[np.ndarray, np.ndarray],
    controller_tf: Tuple[np.ndarray, np.ndarray],
    disturbance_type: str = "step",
    w: Optional[np.ndarray] = None
) -> Dict[str, Any]:
    """Legacy wrapper for utilities.control_utils.disturbance_rejection"""
    warnings.warn(
        "functions.disturbance_rejection is deprecated. Use utilities.control_utils.disturbance_rejection instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return _disturbance_rejection(plant_tf, controller_tf, disturbance_type, w)


def model_predictive_control(
    A: np.ndarray,
    B: np.ndarray,
    Q: np.ndarray,
    R: np.ndarray,
    prediction_horizon: int = 10,
    control_horizon: Optional[int] = None
) -> Dict[str, Any]:
    """Legacy wrapper for utilities.control_utils.model_predictive_control"""
    warnings.warn(
        "functions.model_predictive_control is deprecated. Use utilities.control_utils.model_predictive_control instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return _model_predictive_control(A, B, Q, R, prediction_horizon, control_horizon)


# Legacy module-level exports for backward compatibility
__all__ = [
    'step_response',
    'bode_plot',
    'linearize',
    'tune_pid',
    'simulate_process',
    'optimize_operation',
    'fit_fopdt',
    'stability_analysis',
    'disturbance_rejection',
    'model_predictive_control'
]
