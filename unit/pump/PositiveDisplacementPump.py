"""
PositiveDisplacementPump class for SPROCLIB - Standard Process Control Library

This module contains the positive displacement pump model (constant flow, variable pressure).
"""

import numpy as np
from .Pump import Pump


class PositiveDisplacementPump(Pump):
    """Positive displacement pump (constant flow, variable pressure)."""
    
    def __init__(
        self,
        flow_rate: float = 1.0,         # Constant flow [m^3/s]
        eta: float = 0.8,
        rho: float = 1000.0,
        name: str = "PositiveDisplacementPump"
    ):
        super().__init__(eta=eta, rho=rho, flow_nominal=flow_rate, name=name)
        self.flow_rate = flow_rate
        self.parameters.update({'flow_rate': flow_rate})

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate outlet pressure and power for given inlet pressure.
        Args:
            u: [P_inlet]
        Returns:
            [P_outlet, Power]
        """
        P_in = u[0]
        # Assume pump can deliver any pressure up to a max (not modeled here)
        delta_P = self.delta_P_nominal
        P_out = P_in + delta_P
        Power = self.flow_rate * delta_P / self.eta
        return np.array([P_out, Power])

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Dynamic model: first-order lag for outlet pressure.
        State: [P_out]
        Input: [P_inlet]
        """
        P_out = x[0]
        P_in = u[0]
        P_out_ss, _ = self.steady_state(u)
        tau = 0.5  # s, time constant
        dP_out_dt = (P_out_ss - P_out) / tau
        return np.array([dP_out_dt])
