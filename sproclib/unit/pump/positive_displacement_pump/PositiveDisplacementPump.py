"""
PositiveDisplacementPump class for SPROCLIB - Standard Process Control Library

This module contains the positive displacement pump model (constant flow, variable pressure).
"""

import numpy as np
from sproclib.unit.pump.generic.Pump import Pump


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

    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the model including algorithms, 
                  parameters, equations, and usage information.
        """
        return {
            'type': 'PositiveDisplacementPump',
            'description': 'Positive displacement pump with constant volumetric flow and variable pressure capability',
            'category': 'unit/pump',
            'algorithms': {
                'flow_rate': 'Q = constant (independent of discharge pressure)',
                'pressure_capability': 'ΔP = variable (limited by mechanical design)',
                'power_calculation': 'P = Q*ΔP/η (constant flow, variable pressure)',
                'volumetric_efficiency': 'η_vol = Q_actual/Q_theoretical'
            },
            'parameters': {
                'flow_rate': {
                    'value': self.flow_rate,
                    'units': 'm³/s',
                    'description': 'Constant volumetric displacement per revolution'
                },
                'eta': {
                    'value': self.eta,
                    'units': 'dimensionless',
                    'description': 'Overall pump efficiency (volumetric + mechanical)'
                },
                'rho': {
                    'value': self.rho,
                    'units': 'kg/m³',
                    'description': 'Liquid density'
                },
                'delta_P_nominal': {
                    'value': self.delta_P_nominal,
                    'units': 'Pa',
                    'description': 'Design pressure rise capability'
                }
            },
            'state_variables': ['P_out'],
            'inputs': ['P_inlet'],
            'outputs': ['P_outlet', 'Power'],
            'valid_ranges': {
                'flow_rate': {'min': 1.0e-6, 'max': 1.0, 'units': 'm³/s'},
                'eta': {'min': 0.3, 'max': 0.95, 'units': 'dimensionless'},
                'delta_P_nominal': {'min': 1.0e5, 'max': 1.0e8, 'units': 'Pa'},
                'pressure': {'min': 1.0e4, 'max': 1.0e8, 'units': 'Pa'}
            },
            'applications': ['High-pressure hydraulic systems', 'Precise metering applications', 'Viscous fluid handling', 'Chemical injection systems', 'Hydraulic power units'],
            'limitations': ['Constant flow assumption', 'No slip modeling', 'Uniform fluid properties', 'No pulsation effects', 'Single-phase operation only']
        }
