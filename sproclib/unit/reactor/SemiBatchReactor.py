"""
Semi-Batch Reactor Model for SPROCLIB

This module provides a semi-batch reactor model with
fed-batch operation, reaction kinetics, and thermal dynamics.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import logging
from ..base import ProcessModel

logger = logging.getLogger(__name__)


class SemiBatchReactor(ProcessModel):
    """Semi-batch reactor model with fed-batch operation."""
    
    def __init__(
        self,
        V_max: float = 200.0,        # Maximum reactor volume [L]
        k0: float = 7.2e10,          # Pre-exponential factor [1/min]
        Ea: float = 72750.0,         # Activation energy [J/mol]
        delta_H: float = -52000.0,   # Heat of reaction [J/mol]
        rho: float = 1000.0,         # Density [kg/m³]
        cp: float = 4180.0,          # Heat capacity [J/kg·K]
        U: float = 500.0,            # Heat transfer coefficient [W/m²·K]
        A_heat: float = 5.0,         # Heat transfer area [m²]
        name: str = "SemiBatchReactor"
    ):
        """
        Initialize semi-batch reactor.
        
        Args:
            V_max: Maximum reactor volume [L]
            k0: Pre-exponential factor [1/min]
            Ea: Activation energy [J/mol]
            delta_H: Heat of reaction [J/mol]
            rho: Density [kg/m³]
            cp: Heat capacity [J/kg·K]
            U: Heat transfer coefficient [W/m²·K]
            A_heat: Heat transfer area [m²]
            name: Model name
        """
        super().__init__(name)
        self.V_max = V_max
        self.k0 = k0
        self.Ea = Ea
        self.delta_H = delta_H
        self.rho = rho
        self.cp = cp
        self.U = U
        self.A_heat = A_heat
        
        self.parameters = {
            'V_max': V_max, 'k0': k0, 'Ea': Ea, 'delta_H': delta_H,
            'rho': rho, 'cp': cp, 'U': U, 'A_heat': A_heat
        }
    
    def reaction_rate(self, CA: float, T: float) -> float:
        """
        Calculate reaction rate using Arrhenius equation.
        
        Args:
            CA: Concentration [mol/L]
            T: Temperature [K]
            
        Returns:
            Reaction rate [mol/L·min]
        """
        R = 8.314  # Gas constant [J/mol·K]
        k = self.k0 * np.exp(-self.Ea / (R * T))
        return k * CA  # First-order reaction
    
    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Semi-batch reactor dynamics.
        
        State variables:
        x[0]: Total moles of A [mol]
        x[1]: Temperature [K]
        x[2]: Volume [L]
        
        Input variables:
        u[0]: Feed flow rate [L/min]
        u[1]: Feed concentration [mol/L]
        u[2]: Feed temperature [K]
        u[3]: Jacket temperature [K]
        
        Args:
            t: Time
            x: [nA, T, V]
            u: [qf, CAf, Tf, Tj]
            
        Returns:
            [dnA/dt, dT/dt, dV/dt]
        """
        nA = max(0.0, x[0])   # Total moles of A
        T = max(250.0, x[1])  # Temperature
        V = max(1.0, x[2])    # Volume
        
        qf = u[0]   # Feed flow rate
        CAf = u[1]  # Feed concentration
        Tf = u[2]   # Feed temperature
        Tj = u[3]   # Jacket temperature
        
        # Current concentration
        CA = nA / V if V > 0 else 0.0
        
        # Reaction rate
        r = self.reaction_rate(CA, T)
        
        # Material balance: dnA/dt = qf*CAf - r*V
        dnAdt = qf * CAf - r * V
        
        # Volume balance: dV/dt = qf (assuming constant density)
        dVdt = qf
        
        # Energy balance: d(VρcpT)/dt = qfρcp(Tf-T) + (-ΔH)*r*V + UA(Tj-T)
        # Expanding: ρcp*V*dT/dt + ρcp*T*dV/dt = qfρcp(Tf-T) + (-ΔH)*r*V + UA(Tj-T)
        # Rearranging: dT/dt = [qfρcp(Tf-T) + (-ΔH)*r*V + UA(Tj-T) - ρcp*T*qf] / (ρcp*V)
        # Simplifying: dT/dt = qf(Tf-T)/V + (-ΔH)*r/(ρcp) + UA(Tj-T)/(ρcp*V)
        
        convective_term = qf * (Tf - T) / V if V > 0 else 0.0
        reaction_term = (-self.delta_H * r) / (self.rho * self.cp)
        heat_transfer_term = (self.U * self.A_heat * (Tj - T)) / (self.rho * self.cp * V) if V > 0 else 0.0
        
        dTdt = convective_term + reaction_term + heat_transfer_term
        
        # Limit volume to maximum
        if V >= self.V_max and qf > 0:
            dVdt = 0.0
            # Adjust material balance for overflow
            overflow_rate = qf  # Assume overflow occurs
            dnAdt = qf * CAf - r * V - overflow_rate * CA
        
        return np.array([dnAdt, dTdt, dVdt])
    
    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Semi-batch reactor doesn't have a traditional steady state.
        Returns initial conditions.
        
        Args:
            u: [qf, CAf, Tf, Tj]
            
        Returns:
            Initial conditions [nA0, T0, V0]
        """
        # Return typical initial conditions
        nA0 = 50.0   # Initial moles [mol]
        T0 = u[3] if len(u) > 3 else 300.0  # Start at jacket temperature
        V0 = 50.0    # Initial volume [L]
        
        return np.array([nA0, T0, V0])
    
    def calculate_concentration(self, nA: float, V: float) -> float:
        """
        Calculate current concentration.
        
        Args:
            nA: Total moles [mol]
            V: Volume [L]
            
        Returns:
            Concentration [mol/L]
        """
        return nA / V if V > 0 else 0.0
    
    def calculate_conversion(self, nA: float, nA0: float = 1.0) -> float:
        """
        Calculate conversion based on initial and current moles.
        
        Args:
            nA: Current moles [mol]
            nA0: Initial moles [mol]
            
        Returns:
            Conversion fraction
        """
        if nA0 > 0:
            conversion = (nA0 - nA) / nA0
        else:
            conversion = 0.0
        
        return max(0.0, min(1.0, conversion))
    
    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the SemiBatchReactor model including
                  algorithms, parameters, equations, and usage information.
        """
        return {
            'type': 'SemiBatchReactor',
            'description': 'Semi-batch reactor with fed-batch operation and variable volume',
            'category': 'reactor',
            'algorithms': {
                'reaction_kinetics': 'Arrhenius equation: k = k0 * exp(-Ea/RT)',
                'material_balance': 'dnA/dt = F_in*CA_in - k(T)*CA*V',
                'volume_balance': 'dV/dt = F_in',
                'energy_balance': 'dT/dt = heat terms with variable volume'
            },
            'applications': [
                'Fed-batch processes',
                'Controlled polymerization', 
                'Fine chemical production',
                'Crystallization',
                'Biochemical fermentation'
            ]
        }


__all__ = ['SemiBatchReactor']
