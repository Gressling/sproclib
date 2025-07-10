"""
Pump class for SPROCLIB - Standard Process Control Library

This module contains the base Pump class and specialized pump models.
"""

import numpy as np
from ..base import ProcessModel


class Pump(ProcessModel):
    """Generic liquid pump model (steady-state and dynamic)."""
    
    def __init__(
        self,
        eta: float = 0.7,               # Pump efficiency [-]
        rho: float = 1000.0,            # Liquid density [kg/m^3]
        flow_nominal: float = 1.0,      # Nominal volumetric flow [m^3/s]
        delta_P_nominal: float = 2e5,   # Nominal pressure rise [Pa]
        name: str = "Pump"
    ):
        super().__init__(name)
        self.eta = eta
        self.rho = rho
        self.flow_nominal = flow_nominal
        self.delta_P_nominal = delta_P_nominal
        self.parameters = {
            'eta': eta, 'rho': rho, 'flow_nominal': flow_nominal, 'delta_P_nominal': delta_P_nominal
        }

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state outlet pressure and power for given inlet conditions and flow.
        Args:
            u: [P_inlet, flow]
        Returns:
            [P_outlet, Power]
        """
        P_in, flow = u
        delta_P = self.delta_P_nominal  # Could be a function of flow for more detail
        P_out = P_in + delta_P
        Power = flow * delta_P / self.eta  # W
        return np.array([P_out, Power])

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Dynamic model: first-order lag for outlet pressure.
        State: [P_out]
        Input: [P_inlet, flow]
        """
        P_out = x[0]
        P_in, flow = u
        P_out_ss, _ = self.steady_state(u)
        tau = 1.0  # s, time constant
        dP_out_dt = (P_out_ss - P_out) / tau
        return np.array([dP_out_dt])
