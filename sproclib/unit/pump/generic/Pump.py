"""
Pump class for SPROCLIB - Standard Process Control Library

This module contains the base Pump class and specialized pump models.
"""

import numpy as np
from sproclib.unit.base import ProcessModel


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

    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the model including algorithms, 
                  parameters, equations, and usage information.
        """
        return {
            'type': 'Pump',
            'description': 'Generic liquid pump model for fluid transport with constant pressure rise',
            'category': 'unit/pump',
            'algorithms': {
                'pressure_rise': 'ΔP = P_nominal (constant pressure rise)',
                'power_calculation': 'P = Q * ΔP / η (hydraulic power with efficiency)',
                'dynamic_response': 'First-order lag: τ(dP/dt) = P_ss - P_out'
            },
            'parameters': {
                'eta': {
                    'value': self.eta,
                    'units': 'dimensionless',
                    'description': 'Overall pump efficiency (hydraulic + mechanical)'
                },
                'rho': {
                    'value': self.rho,
                    'units': 'kg/m³',
                    'description': 'Liquid density'
                },
                'flow_nominal': {
                    'value': self.flow_nominal,
                    'units': 'm³/s',
                    'description': 'Design volumetric flow rate'
                },
                'delta_P_nominal': {
                    'value': self.delta_P_nominal,
                    'units': 'Pa',
                    'description': 'Design pressure rise across pump'
                }
            },
            'state_variables': ['P_out'],
            'inputs': ['P_inlet', 'flow'],
            'outputs': ['P_outlet', 'Power'],
            'valid_ranges': {
                'eta': {'min': 0.1, 'max': 0.95, 'units': 'dimensionless'},
                'flow': {'min': 0.0, 'max': 10.0, 'units': 'm³/s'},
                'pressure': {'min': 1.0e4, 'max': 1.0e7, 'units': 'Pa'},
                'delta_P_nominal': {'min': 1.0e4, 'max': 5.0e6, 'units': 'Pa'}
            },
            'applications': ['General liquid transport', 'Process circulation loops', 'Boiler feedwater systems', 'Chemical transfer operations', 'HVAC systems'],
            'limitations': ['Constant pressure rise assumption', 'No pump curve modeling', 'Single-phase liquid only', 'No cavitation effects', 'Constant efficiency assumption']
        }
