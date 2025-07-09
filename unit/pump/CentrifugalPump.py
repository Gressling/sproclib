"""
CentrifugalPump class for SPROCLIB - Standard Process Control Library

This module contains the centrifugal pump model with quadratic head-flow curve.
"""

import numpy as np
from .Pump import Pump


class CentrifugalPump(Pump):
    """Centrifugal pump with quadratic head-flow curve."""
    
    def __init__(
        self,
        H0: float = 50.0,               # Shutoff head [m]
        K: float = 20.0,                # Head-flow coefficient
        eta: float = 0.7,
        rho: float = 1000.0,
        name: str = "CentrifugalPump"
    ):
        super().__init__(eta=eta, rho=rho, name=name)
        self.H0 = H0
        self.K = K
        self.parameters.update({'H0': H0, 'K': K})

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate outlet pressure and power for given flow using pump curve.
        Args:
            u: [P_inlet, flow]
        Returns:
            [P_outlet, Power]
        """
        P_in, flow = u
        g = 9.81
        H = max(0.0, self.H0 - self.K * flow**2)  # Head [m]
        delta_P = self.rho * g * H
        P_out = P_in + delta_P
        Power = flow * delta_P / self.eta
        return np.array([P_out, Power])
