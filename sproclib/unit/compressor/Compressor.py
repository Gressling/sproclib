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

    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the model including algorithms, 
                  parameters, equations, and usage information.
        """
        return {
            'type': 'Compressor',
            'description': 'Gas compressor model with isentropic compression and efficiency losses',
            'category': 'unit/compressor',
            'algorithms': {
                'steady_state': 'Isentropic compression with efficiency correction: T_out = T_in + (T_isentropic - T_in)/η',
                'dynamics': 'First-order lag response for outlet temperature: τ(dT_out/dt) = T_ss - T_out',
                'power_calculation': 'Power = n_dot * R * (T_out - T_in) / M'
            },
            'parameters': {
                'eta_isentropic': {
                    'value': self.eta_isentropic,
                    'units': 'dimensionless',
                    'description': 'Isentropic efficiency (typically 0.70-0.85 for centrifugal, 0.75-0.90 for axial)'
                },
                'P_suction': {
                    'value': self.P_suction,
                    'units': 'Pa',
                    'description': 'Suction pressure (inlet pressure)'
                },
                'P_discharge': {
                    'value': self.P_discharge,
                    'units': 'Pa',
                    'description': 'Discharge pressure (outlet pressure)'
                },
                'T_suction': {
                    'value': self.T_suction,
                    'units': 'K',
                    'description': 'Suction temperature (inlet temperature)'
                },
                'gamma': {
                    'value': self.gamma,
                    'units': 'dimensionless',
                    'description': 'Heat capacity ratio Cp/Cv (1.4 for air, 1.3 for natural gas)'
                },
                'R': {
                    'value': self.R,
                    'units': 'J/mol/K',
                    'description': 'Universal gas constant'
                },
                'M': {
                    'value': self.M,
                    'units': 'kg/mol',
                    'description': 'Molar mass of gas being compressed'
                },
                'flow_nominal': {
                    'value': self.flow_nominal,
                    'units': 'mol/s',
                    'description': 'Nominal molar flow rate for design point'
                }
            },
            'state_variables': {
                'T_out': 'Outlet temperature [K]'
            },
            'inputs': {
                'P_suction': 'Suction pressure [Pa]',
                'T_suction': 'Suction temperature [K]',  
                'P_discharge': 'Discharge pressure [Pa]',
                'flow': 'Molar flow rate [mol/s]'
            },
            'outputs': {
                'T_out': 'Outlet temperature [K]',
                'Power': 'Compression power [W]'
            },
            'valid_ranges': {
                'eta_isentropic': {'min': 0.5, 'max': 0.95, 'units': 'dimensionless'},
                'P_ratio': {'min': 1.0, 'max': 20.0, 'units': 'dimensionless'},
                'T_suction': {'min': 200.0, 'max': 600.0, 'units': 'K'},
                'flow': {'min': 0.0, 'max': 1000.0, 'units': 'mol/s'}
            },
            'applications': [
                'Natural gas transmission pipelines',
                'Refrigeration cycles',
                'Air conditioning systems',
                'Process gas compression',
                'Pneumatic conveying systems',
                'Gas turbine fuel systems'
            ],
            'limitations': [
                'Assumes ideal gas behavior',
                'No consideration of surge or choke limits',
                'Constant isentropic efficiency across operating range',
                'No mechanical losses included',
                'First-order dynamics approximation'
            ]
        }
