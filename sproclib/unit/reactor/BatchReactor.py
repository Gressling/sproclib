"""
Batch Reactor Model for SPROCLIB

This module provides a batch reactor model with
reaction kinetics and thermal dynamics.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import logging
from ..base import ProcessModel

logger = logging.getLogger(__name__)


class BatchReactor(ProcessModel):
    """Batch reactor model with heating/cooling."""
    
    def __init__(
        self,
        V: float = 100.0,            # Reactor volume [L]
        k0: float = 7.2e10,          # Pre-exponential factor [1/min]
        Ea: float = 72750.0,         # Activation energy [J/mol]
        delta_H: float = -52000.0,   # Heat of reaction [J/mol]
        rho: float = 1000.0,         # Density [kg/m³]
        cp: float = 4180.0,          # Heat capacity [J/kg·K]
        U: float = 500.0,            # Heat transfer coefficient [W/m²·K]
        A: float = 5.0,              # Heat transfer area [m²]
        name: str = "BatchReactor"
    ):
        """
        Initialize batch reactor.
        
        Args:
            V: Reactor volume [L]
            k0: Pre-exponential factor [1/min]
            Ea: Activation energy [J/mol]
            delta_H: Heat of reaction [J/mol]
            rho: Density [kg/m³]
            cp: Heat capacity [J/kg·K]
            U: Heat transfer coefficient [W/m²·K]
            A: Heat transfer area [m²]
            name: Model name
        """
        super().__init__(name)
        self.V = V
        self.k0 = k0
        self.Ea = Ea
        self.delta_H = delta_H
        self.rho = rho
        self.cp = cp
        self.U = U
        self.A = A
        
        self.parameters = {
            'V': V, 'k0': k0, 'Ea': Ea, 'delta_H': delta_H,
            'rho': rho, 'cp': cp, 'U': U, 'A': A
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
        Batch reactor dynamics.
        
        State variables:
        x[0]: Concentration [mol/L]
        x[1]: Temperature [K]
        
        Input variables:
        u[0]: Jacket temperature [K]
        
        Args:
            t: Time
            x: [CA, T]
            u: [Tj]
            
        Returns:
            [dCA/dt, dT/dt]
        """
        CA = max(0.0, x[0])
        T = max(250.0, x[1])
        Tj = u[0]  # Jacket temperature
        
        # Reaction rate
        r = self.reaction_rate(CA, T)
        
        # Material balance: dCA/dt = -r
        dCAdt = -r
        
        # Energy balance: dT/dt = (-ΔH*r)/(ρ*cp) + UA(Tj-T)/(ρ*cp*V)
        heat_generation = (-self.delta_H * r) / (self.rho * self.cp)
        heat_transfer = (self.U * self.A * (Tj - T)) / (self.rho * self.cp * self.V)
        
        dTdt = heat_generation + heat_transfer
        
        return np.array([dCAdt, dTdt])
    
    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Batch reactor doesn't have a traditional steady state.
        Returns initial conditions for given jacket temperature.
        
        Args:
            u: [Tj]
            
        Returns:
            Initial conditions [CA0, T0]
        """
        # Return typical initial conditions
        # In practice, this would be the loaded conditions
        CA0 = 1.0  # Initial concentration [mol/L]
        T0 = u[0] if len(u) > 0 else 300.0  # Start at jacket temperature
        
        return np.array([CA0, T0])
    
    def calculate_conversion(self, CA: float, CA0: float = 1.0) -> float:
        """
        Calculate conversion based on initial and current concentration.
        
        Args:
            CA: Current concentration [mol/L]
            CA0: Initial concentration [mol/L]
            
        Returns:
            Conversion fraction
        """
        if CA0 > 0:
            conversion = (CA0 - CA) / CA0
        else:
            conversion = 0.0
        
        return max(0.0, min(1.0, conversion))
    
    def batch_time_to_conversion(self, target_conversion: float, CA0: float = 1.0, T_avg: float = 350.0) -> float:
        """
        Estimate time to reach target conversion (isothermal approximation).
        
        Args:
            target_conversion: Target conversion fraction
            CA0: Initial concentration [mol/L]
            T_avg: Average temperature [K]
            
        Returns:
            Time to reach conversion [min]
        """
        if target_conversion <= 0 or target_conversion >= 1:
            return 0.0
        
        # For first-order reaction: CA = CA0 * exp(-k*t)
        # Conversion X = 1 - CA/CA0 = 1 - exp(-k*t)
        # t = -ln(1-X) / k
        
        R = 8.314
        k = self.k0 * np.exp(-self.Ea / (R * T_avg))
        
        if k > 0:
            time_required = -np.log(1 - target_conversion) / k
        else:
            time_required = float('inf')
        
        return time_required
