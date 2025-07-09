"""
Legacy Analysis Module for SPROCLIB - Standard Process Control Library

This module provides backward compatibility for legacy code.
New code should import from the modular packages:
- analysis.transfer_function for TransferFunction
- simulation.process_simulation for Simulation  
- optimization.economic_optimization for Optimization
- scheduling.state_task_network for StateTaskNetwork

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import warnings
from typing import Optional, Tuple, Dict, Any, List, Callable, Union

# Import from new modular structure
try:
    # Try relative imports first (when used as a package)
    from ..analysis.transfer_function import TransferFunction as _TransferFunction
    from ..simulation.process_simulation import ProcessSimulation as _ProcessSimulation
    from ..optimization.economic_optimization import EconomicOptimization as _EconomicOptimization
    from ..scheduling.state_task_network import StateTaskNetwork as _StateTaskNetwork
except ImportError:
    # Fall back to absolute imports (when used as standalone module)
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    
    from analysis.transfer_function import TransferFunction as _TransferFunction
    from simulation.process_simulation import ProcessSimulation as _ProcessSimulation
    from optimization.economic_optimization import EconomicOptimization as _EconomicOptimization
    from scheduling.state_task_network import StateTaskNetwork as _StateTaskNetwork

# Backward compatibility warning
warnings.warn(
    "analysis.py is deprecated. Please import from the modular packages: "
    "analysis.transfer_function, simulation.process_simulation, "
    "optimization.economic_optimization, scheduling.state_task_network",
    DeprecationWarning,
    stacklevel=2
)


# Legacy compatibility classes - just pass through to new implementations
class TransferFunction(_TransferFunction):
    """Legacy wrapper for analysis.transfer_function.TransferFunction"""
    pass


class Simulation:
    """Legacy wrapper for simulation.process_simulation.ProcessSimulation"""
    
    def __init__(self, model, name: str = "Simulation"):
        warnings.warn(
            "Simulation class is deprecated. Use simulation.process_simulation.ProcessSimulation instead.",
            DeprecationWarning,
            stacklevel=2
        )
        self._sim = _ProcessSimulation(model, None, name)
        self.model = model
        self.name = name
        self.results = {}
    
    def run(
        self,
        t_span: Tuple[float, float],
        x0,
        u_profile: Callable,
        solver: str = 'RK45',
        rtol: float = 1e-6,
        atol: float = 1e-9
    ) -> Dict[str, Any]:
        """Run simulation with specified input profile."""
        return self._sim.run_open_loop(t_span, x0, u_profile, solver, rtol, atol)
    
    def plot_results(self, variables: Optional[List[str]] = None, figsize: Tuple[int, int] = (12, 8)):
        """Plot simulation results."""
        return self._sim.plot_results(variables, figsize)


class Optimization:
    """Legacy wrapper for optimization.economic_optimization.EconomicOptimization"""
    
    def __init__(self, name: str = "Optimization"):
        warnings.warn(
            "Optimization class is deprecated. Use optimization.economic_optimization.EconomicOptimization instead.",
            DeprecationWarning,
            stacklevel=2
        )
        self._opt = _EconomicOptimization(name)
        self.name = name
        self.results = {}
    
    def linear_programming(self, *args, **kwargs):
        """Legacy linear programming method."""
        return self._opt.linear_programming(*args, **kwargs)
    
    def nonlinear_optimization(self, *args, **kwargs):
        """Legacy nonlinear optimization method."""
        return self._opt.nonlinear_optimization(*args, **kwargs)
    
    def economic_optimization(self, *args, **kwargs):
        """Legacy economic optimization method."""
        return self._opt.production_planning(*args, **kwargs)


class StateTaskNetwork(_StateTaskNetwork):
    """Legacy wrapper for scheduling.state_task_network.StateTaskNetwork"""
    
    def __init__(self, name: str = "STN"):
        warnings.warn(
            "StateTaskNetwork should be imported from scheduling.state_task_network instead.",
            DeprecationWarning,
            stacklevel=2
        )
        super().__init__(name)


# Legacy module-level exports for backward compatibility
__all__ = [
    'TransferFunction',
    'Simulation', 
    'Optimization',
    'StateTaskNetwork'
]
