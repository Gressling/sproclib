"""
Compressor class for SPROCLIB - Standard Process Control Library

This module contains the gas compressor model (steady-state and dynamic).
"""

import numpy as np
from ..base import ProcessModel


class Compressor(ProcessModel):
    """Generic gas compressor model (steady-state and dynamic)."""
    
    def __init__(
        self,
        eta_isentropic: float = 0.75,   # Isentropic efficiency [-]
        P_suction: float = 1e5,         # Suction pressure [Pa]
        P_discharge: float = 3e5,       # Discharge pressure [Pa]
        T_suction: float = 300.0,       # Suction temperature [K]
        gamma: float = 1.4,             # Heat capacity ratio (Cp/Cv)
        R: float = 8.314,               # Gas constant [J/mol/K]
        M: float = 0.028,               # Molar mass [kg/mol]
        flow_nominal: float = 1.0,      # Nominal molar flow [mol/s]
        name: str = "Compressor"
    ):
        super().__init__(name)
        self.eta_isentropic = eta_isentropic
        self.P_suction = P_suction
        self.P_discharge = P_discharge
        self.T_suction = T_suction
        self.gamma = gamma
        self.R = R
        self.M = M
        self.flow_nominal = flow_nominal
        self.parameters = {
            'eta_isentropic': eta_isentropic, 'P_suction': P_suction, 'P_discharge': P_discharge,
            'T_suction': T_suction, 'gamma': gamma, 'R': R, 'M': M, 'flow_nominal': flow_nominal
        }

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state outlet temperature and power for given inlet conditions and flow.
        Args:
            u: [P_suction, T_suction, P_discharge, flow]
        Returns:
            [T_out, Power]
        """
        P_suc, T_suc, P_dis, flow = u
        # Isentropic temperature rise
        T_out_isentropic = T_suc * (P_dis/P_suc)**((self.gamma-1)/self.gamma)
        # Actual temperature rise
        T_out = T_suc + (T_out_isentropic - T_suc) / self.eta_isentropic
        # Power required
        n_dot = flow  # mol/s
        Q_dot = n_dot * self.R * (T_out - T_suc) / self.M  # W
        return np.array([T_out, Q_dot])

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Dynamic model: simple first-order lag for outlet temperature.
        State: [T_out]
        Input: [P_suction, T_suction, P_discharge, flow]
        """
        T_out = x[0]
        P_suc, T_suc, P_dis, flow = u
        T_out_ss, _ = self.steady_state(u)
        tau = 2.0  # s, time constant
        dT_out_dt = (T_out_ss - T_out) / tau
        return np.array([dT_out_dt])
