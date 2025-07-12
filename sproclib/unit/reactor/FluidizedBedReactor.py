"""
FluidizedBedReactor Model for SPROCLIB - Standard Process Control Library

This module implements a fluidized bed catalytic reactor model with two-phase 
(bubble and emulsion) behavior for chemical process control applications.

Author: SPROCLIB Development Team
"""

import numpy as np
from typing import Dict, Tuple, List, Optional
from scipy.optimize import fsolve
import logging

from ..base import ProcessModel

logger = logging.getLogger(__name__)


class FluidizedBedReactor(ProcessModel):
    """Fluidized bed catalytic reactor model with bubble and emulsion phases."""
    
    def __init__(
        self,
        H: float = 3.0,              # Bed height [m]
        D: float = 2.0,              # Bed diameter [m]
        U_mf: float = 0.1,           # Minimum fluidization velocity [m/s]
        rho_cat: float = 1500.0,     # Catalyst density [kg/m³]
        dp: float = 0.0005,          # Particle diameter [m]
        epsilon_mf: float = 0.5,     # Voidage at minimum fluidization [-]
        k0: float = 1e5,             # Pre-exponential factor [m³/kg·s]
        Ea: float = 60000.0,         # Activation energy [J/mol]
        delta_H: float = -80000.0,   # Heat of reaction [J/mol]
        K_bc: float = 5.0,           # Bubble-cloud mass transfer coefficient [1/s]
        K_ce: float = 20.0,          # Cloud-emulsion mass transfer coefficient [1/s]
        name: str = "FluidizedBedReactor"
    ):
        """
        Initialize fluidized bed reactor with two-phase model.
        
        Args:
            H: Bed height [m]
            D: Bed diameter [m]
            U_mf: Minimum fluidization velocity [m/s]
            rho_cat: Catalyst density [kg/m³]
            dp: Particle diameter [m]
            epsilon_mf: Voidage at minimum fluidization [-]
            k0: Pre-exponential factor [m³/kg·s]
            Ea: Activation energy [J/mol]
            delta_H: Heat of reaction [J/mol]
            K_bc: Bubble-cloud mass transfer coefficient [1/s]
            K_ce: Cloud-emulsion mass transfer coefficient [1/s]
            name: Model name
        """
        super().__init__(name)
        self.H = H
        self.D = D
        self.U_mf = U_mf
        self.rho_cat = rho_cat
        self.dp = dp
        self.epsilon_mf = epsilon_mf
        self.k0 = k0
        self.Ea = Ea
        self.delta_H = delta_H
        self.K_bc = K_bc
        self.K_ce = K_ce
        
        # Calculate derived properties
        self.A_cross = np.pi * (D/2)**2  # Cross-sectional area
        self.V_total = self.A_cross * H  # Total volume
        
        self.parameters = {
            'H': H, 'D': D, 'U_mf': U_mf, 'rho_cat': rho_cat, 'dp': dp,
            'epsilon_mf': epsilon_mf, 'k0': k0, 'Ea': Ea, 'delta_H': delta_H,
            'K_bc': K_bc, 'K_ce': K_ce
        }

    
    def fluidization_properties(self, U_g: float) -> Dict[str, float]:
        """
        Calculate fluidization properties.
        
        Args:
            U_g: Superficial gas velocity [m/s]
            
        Returns:
            Dictionary with fluidization properties
        """
        # Bubble velocity (simplified correlation)
        U_b = U_g - self.U_mf + 0.711 * np.sqrt(9.81 * self.dp)
        
        # Bubble fraction (simplified)
        if U_g > self.U_mf:
            delta = (U_g - self.U_mf) / U_b
        else:
            delta = 0.0
        
        # Emulsion phase fraction
        gamma = 1 - delta
        
        return {
            'bubble_velocity': U_b,
            'bubble_fraction': delta,
            'emulsion_fraction': gamma,
            'excess_velocity': U_g - self.U_mf
        }

    
    def reaction_rate(self, CA: float, T: float) -> float:
        """
        Calculate reaction rate in emulsion phase.
        
        Args:
            CA: Concentration in emulsion phase [mol/m³]
            T: Temperature [K]
            
        Returns:
            Reaction rate [mol/kg·s]
        """
        R = 8.314  # Gas constant [J/mol·K]
        k = self.k0 * np.exp(-self.Ea / (R * T))
        return k * CA

    
    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Fluidized bed reactor dynamics with two-phase model.
        
        State variables: [CA_bubble, CA_emulsion, T]
        Input variables: [CA_in, T_in, U_g, T_coolant]
        
        Args:
            t: Time [s]
            x: State variables
            u: Input variables
            
        Returns:
            State derivatives
        """
        CA_bubble, CA_emulsion, T = x
        CA_in, T_in, U_g, T_coolant = u
        
        # Fluidization properties
        props = self.fluidization_properties(U_g)
        delta = props['bubble_fraction']
        gamma = props['emulsion_fraction']
        U_b = props['bubble_velocity']
        
        # Reaction rate in emulsion phase
        r = self.reaction_rate(CA_emulsion, T)
        
        # Mass transfer between phases
        J_bc = self.K_bc * (CA_bubble - CA_emulsion)  # Bubble to cloud/emulsion
        
        # Bubble phase mass balance
        if delta > 0:
            dCA_bubble_dt = (U_g - self.U_mf) / (delta * self.H) * (CA_in - CA_bubble) - J_bc
        else:
            dCA_bubble_dt = 0.0
        
        # Emulsion phase mass balance
        W_cat = self.rho_cat * (1 - self.epsilon_mf) * self.V_total * gamma
        dCA_emulsion_dt = (self.U_mf / (gamma * self.H) * (CA_in - CA_emulsion) + 
                          J_bc - r * W_cat / (gamma * self.V_total))
        
        # Energy balance (simplified)
        rho_cp = 1000 * 1000  # Approximate heat capacity of gas phase
        Q_reaction = -self.delta_H * r * W_cat
        Q_cooling = 1000 * (T - T_coolant)  # Simplified cooling
        
        dT_dt = (U_g / self.H * rho_cp * (T_in - T) + Q_reaction - Q_cooling) / (rho_cp * self.V_total)
        
        return np.array([dCA_bubble_dt, dCA_emulsion_dt, dT_dt])

    
    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state concentrations and temperature.
        
        Args:
            u: Input variables [CA_in, T_in, U_g, T_coolant]
            
        Returns:
            Steady-state values [CA_bubble, CA_emulsion, T]
        """
        CA_in, T_in, U_g, T_coolant = u
        
        # Initial guess
        x0 = np.array([CA_in * 0.9, CA_in * 0.8, T_in])
        
        # Solve for steady state
        def steady_state_eqs(x):
            return self.dynamics(0, x, u)
        
        try:
            x_ss = fsolve(steady_state_eqs, x0)
            return x_ss
        except:
            logger.warning("Steady-state calculation failed, returning initial guess")
            return x0

    
    def calculate_conversion(self, CA_in: float, CA_out: float) -> float:
        """Calculate overall conversion."""
        if CA_in > 0:
            return (CA_in - CA_out) / CA_in
        return 0.0
    
    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the FluidizedBedReactor model including
                  algorithms, parameters, equations, and usage information.
        """
        return {
            'type': 'FluidizedBedReactor',
            'description': 'Fluidized bed catalytic reactor with two-phase modeling',
            'category': 'reactor',
            'algorithms': {
                'two_phase_model': 'Bubble and emulsion phase mass balances',
                'fluidization': 'Minimum fluidization velocity and regime maps',
                'mass_transfer': 'Inter-phase mass transfer coefficients',
                'reaction_kinetics': 'Heterogeneous catalysis in emulsion phase'
            },
            'applications': [
                'Fluid catalytic cracking',
                'Coal combustion and gasification',
                'Polymerization processes',
                'Roasting and calcination',
                'Waste treatment'
            ]
        }


__all__ = ['FluidizedBedReactor']
