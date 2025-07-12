"""
Continuous Stirred Tank Reactor (CSTR) Model

This module provides a CSTR model with Arrhenius kinetics,
energy balance, and heat transfer capabilities.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import logging
from typing import Optional, Tuple, Dict, Any
from ...base import ProcessModel

logger = logging.getLogger(__name__)


class CSTR(ProcessModel):
    """Continuous Stirred Tank Reactor model."""
    
    def __init__(
        self,
        V: float = 100.0,
        k0: float = 7.2e10,
        Ea: float = 72750.0,
        R: float = 8.314,
        rho: float = 1000.0,
        Cp: float = 0.239,
        dHr: float = -50000.0,
        UA: float = 50000.0,
        name: str = "CSTR"
    ):
        """
        Initialize CSTR model.
        
        Args:
            V: Reactor volume [L]
            k0: Arrhenius pre-exponential factor [1/min]
            Ea: Activation energy [J/gmol]
            R: Gas constant [J/gmol/K]
            rho: Density [g/L]
            Cp: Heat capacity [J/g/K]
            dHr: Heat of reaction [J/gmol]
            UA: Heat transfer coefficient [J/min/K]
            name: Model name
        """
        super().__init__(name)
        self.V = V
        self.k0 = k0
        self.Ea = Ea
        self.R = R
        self.rho = rho
        self.Cp = Cp
        self.dHr = dHr
        self.UA = UA
        
        self.parameters = {
            'V': V, 'k0': k0, 'Ea': Ea, 'R': R,
            'rho': rho, 'Cp': Cp, 'dHr': dHr, 'UA': UA
        }
        
        # Define state and input variables
        self.state_variables = {
            'CA': 'Concentration [mol/L]',
            'T': 'Temperature [K]'
        }
        
        self.inputs = {
            'q': 'Flow rate [L/min]',
            'CAi': 'Inlet concentration [mol/L]',
            'Ti': 'Inlet temperature [K]',
            'Tc': 'Coolant temperature [K]'
        }
        
        self.outputs = {
            'CA': 'Outlet concentration [mol/L]',
            'T': 'Outlet temperature [K]',
            'reaction_rate': 'Reaction rate [mol/L/min]',
            'heat_generation': 'Heat generation [J/min]'
        }
    
    def reaction_rate(self, T: float) -> float:
        """Calculate reaction rate constant k(T) = k0 * exp(-Ea/RT)"""
        return self.k0 * np.exp(-self.Ea / (self.R * T))
    
    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        CSTR dynamics:
        dCA/dt = q/V*(CAi - CA) - k(T)*CA
        dT/dt = q/V*(Ti - T) + (-dHr)*k(T)*CA/(rho*Cp) + UA*(Tc - T)/(V*rho*Cp)
        
        Args:
            t: Time
            x: [CA, T] - concentration and temperature
            u: [q, CAi, Ti, Tc] - flow rate, inlet concentration, inlet temp, coolant temp
            
        Returns:
            [dCA/dt, dT/dt]
        """
        CA, T = x
        q, CAi, Ti, Tc = u
        
        # Ensure positive values
        CA = max(CA, 0.0)
        T = max(T, 250.0)  # Minimum temperature
        
        k = self.reaction_rate(T)
        
        dCAdt = q/self.V * (CAi - CA) - k * CA
        dTdt = (q/self.V * (Ti - T) + 
                (-self.dHr) * k * CA / (self.rho * self.Cp) +
                self.UA * (Tc - T) / (self.V * self.rho * self.Cp))
        
        return np.array([dCAdt, dTdt])
    
    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state for CSTR (requires numerical solution).
        
        Args:
            u: [q, CAi, Ti, Tc] - operating conditions
            
        Returns:
            [CA_ss, T_ss] - steady-state concentration and temperature
        """
        from scipy.optimize import fsolve
        
        def equations(x):
            return self.dynamics(0, x, u)
        
        # Initial guess based on inlet conditions
        x0 = np.array([u[1] * 0.5, u[2]])  # 50% conversion, inlet temperature
        
        try:
            x_ss = fsolve(equations, x0)
            return x_ss
        except:
            logger.warning("Steady-state calculation failed, returning initial guess")
            return x0
    
    def calculate_conversion(self, CA: float, CAi: float) -> float:
        """
        Calculate conversion: X = (CAi - CA) / CAi
        
        Args:
            CA: Outlet concentration [mol/L]
            CAi: Inlet concentration [mol/L]
            
        Returns:
            Conversion fraction
        """
        if CAi > 0:
            return (CAi - CA) / CAi
        return 0.0
    
    def calculate_residence_time(self, q: float) -> float:
        """
        Calculate residence time: tau = V / q
        
        Args:
            q: Flow rate [L/min]
            
        Returns:
            Residence time [min]
        """
        if q > 0:
            return self.V / q
        return float('inf')
    
    def calculate_heat_generation(self, CA: float, T: float) -> float:
        """
        Calculate heat generation rate from reaction.
        
        Args:
            CA: Concentration [mol/L]
            T: Temperature [K]
            
        Returns:
            Heat generation rate [J/min]
        """
        k = self.reaction_rate(T)
        r = k * CA  # Reaction rate [mol/L/min]
        Q_gen = (-self.dHr) * r * self.V  # Heat generation [J/min]
        return Q_gen
    
    def get_performance_metrics(self, x: np.ndarray, u: np.ndarray) -> Dict[str, float]:
        """
        Calculate key performance metrics.
        
        Args:
            x: [CA, T] - current state
            u: [q, CAi, Ti, Tc] - inputs
            
        Returns:
            Dictionary with performance metrics
        """
        CA, T = x
        q, CAi, Ti, Tc = u
        
        conversion = self.calculate_conversion(CA, CAi)
        residence_time = self.calculate_residence_time(q)
        heat_gen = self.calculate_heat_generation(CA, T)
        k = self.reaction_rate(T)
        
        return {
            'conversion': conversion,
            'residence_time': residence_time,
            'reaction_rate_constant': k,
            'heat_generation': heat_gen,
            'productivity': q * CA,  # [mol/min]
            'selectivity': 1.0,  # Assuming single reaction
            'space_time_yield': CA / residence_time if residence_time > 0 else 0.0
        }

    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the CSTR model including
                  algorithms, parameters, equations, and usage information.
        """
        return {
            'type': 'CSTR',
            'description': 'Continuous Stirred Tank Reactor with Arrhenius kinetics and energy balance',
            'category': 'reactor',
            'algorithms': {
                'reaction_kinetics': 'Arrhenius equation: k = k0 * exp(-Ea/RT)',
                'material_balance': 'dCA/dt = q/V*(CAi - CA) - k(T)*CA',
                'energy_balance': 'dT/dt = q/V*(Ti - T) + (-dHr)*k(T)*CA/(rho*Cp) + UA*(Tc - T)/(V*rho*Cp)',
                'steady_state': 'Numerical solution using scipy.optimize.fsolve'
            },
            'parameters': {
                'V': {'value': self.V, 'units': 'L', 'description': 'Reactor volume'},
                'k0': {'value': self.k0, 'units': '1/min', 'description': 'Arrhenius pre-exponential factor'},
                'Ea': {'value': self.Ea, 'units': 'J/gmol', 'description': 'Activation energy'},
                'R': {'value': self.R, 'units': 'J/gmol/K', 'description': 'Gas constant'},
                'rho': {'value': self.rho, 'units': 'g/L', 'description': 'Density'},
                'Cp': {'value': self.Cp, 'units': 'J/g/K', 'description': 'Heat capacity'},
                'dHr': {'value': self.dHr, 'units': 'J/gmol', 'description': 'Heat of reaction'},
                'UA': {'value': self.UA, 'units': 'J/min/K', 'description': 'Heat transfer coefficient'}
            },
            'state_variables': self.state_variables,
            'inputs': self.inputs,
            'outputs': self.outputs,
            'valid_ranges': {
                'V': {'min': 1.0, 'max': 10000.0, 'units': 'L'},
                'T': {'min': 250.0, 'max': 600.0, 'units': 'K'},
                'CA': {'min': 0.0, 'max': 100.0, 'units': 'mol/L'},
                'q': {'min': 0.1, 'max': 1000.0, 'units': 'L/min'}
            },
            'applications': [
                'Chemical reaction engineering',
                'Process control design',
                'Reactor optimization',
                'Safety analysis'
            ],
            'limitations': [
                'Perfect mixing assumption',
                'Single reaction assumed',
                'Constant physical properties',
                'No mass transfer limitations'
            ]
        }
