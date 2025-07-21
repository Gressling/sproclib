"""
CentrifugalPump class for SPROCLIB - Standard Process Control Library

This module contains the centrifugal pump model with quadratic head-flow curve.
"""

import numpy as np
from sproclib.unit.pump.generic.Pump import Pump


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

    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the model including algorithms, 
                  parameters, equations, and usage information.
        """
        return {
            'type': 'CentrifugalPump',
            'description': 'Centrifugal pump with quadratic head-flow characteristic curve for dynamic flow applications',
            'category': 'unit/pump',
            'algorithms': {
                'pump_curve': 'H = H₀ - K*Q² (quadratic head-flow relationship)',
                'pressure_rise': 'ΔP = ρ*g*H (hydrostatic pressure from head)',
                'power_calculation': 'P = Q*ΔP/η (brake horsepower with efficiency)',
                'affinity_laws': 'Q₂/Q₁ = (N₂/N₁), H₂/H₁ = (N₂/N₁)² for speed changes'
            },
            'parameters': {
                'H0': {
                    'value': self.H0,
                    'units': 'm',
                    'description': 'Shutoff head (head at zero flow)'
                },
                'K': {
                    'value': self.K,
                    'units': 's²/m⁵',
                    'description': 'Head-flow coefficient for quadratic curve'
                },
                'eta': {
                    'value': self.eta,
                    'units': 'dimensionless',
                    'description': 'Overall pump efficiency'
                },
                'rho': {
                    'value': self.rho,
                    'units': 'kg/m³',
                    'description': 'Liquid density'
                }
            },
            'state_variables': ['P_out'],
            'inputs': ['P_inlet', 'flow'],
            'outputs': ['P_outlet', 'Power'],
            'valid_ranges': {
                'H0': {'min': 5.0, 'max': 500.0, 'units': 'm'},
                'K': {'min': 0.1, 'max': 1000.0, 'units': 's²/m⁵'},
                'flow': {'min': 0.0, 'max': 5.0, 'units': 'm³/s'},
                'eta': {'min': 0.2, 'max': 0.90, 'units': 'dimensionless'}
            },
            'applications': ['Water supply systems', 'Chemical process circulation', 'Cooling water systems', 'Fire protection systems', 'Irrigation and drainage'],
            'limitations': ['Quadratic curve approximation', 'No cavitation modeling', 'Constant speed operation', 'Single impeller design', 'Newtonian fluids only']
        }
