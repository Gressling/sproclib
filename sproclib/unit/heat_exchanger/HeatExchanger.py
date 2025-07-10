"""
Heat Exchanger Model

This module provides a counter-current heat exchanger model with thermal dynamics
using effectiveness-NTU method.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import logging
from typing import Optional, Tuple, Dict, Any
from ..base import ProcessModel

logger = logging.getLogger(__name__)


class HeatExchanger(ProcessModel):
    """Counter-current heat exchanger model with thermal dynamics."""
    
    def __init__(
        self,
        U: float = 500.0,           # Overall heat transfer coefficient [W/m²·K]
        A: float = 10.0,            # Heat transfer area [m²]
        m_hot: float = 1.0,         # Hot fluid mass flow rate [kg/s]
        m_cold: float = 1.2,        # Cold fluid mass flow rate [kg/s]
        cp_hot: float = 4180.0,     # Hot fluid specific heat [J/kg·K]
        cp_cold: float = 4180.0,    # Cold fluid specific heat [J/kg·K]
        V_hot: float = 0.1,         # Hot fluid volume [m³]
        V_cold: float = 0.1,        # Cold fluid volume [m³]
        rho_hot: float = 1000.0,    # Hot fluid density [kg/m³]
        rho_cold: float = 1000.0,   # Cold fluid density [kg/m³]
        name: str = "HeatExchanger"
    ):
        """
        Initialize counter-current heat exchanger.
        
        Args:
            U: Overall heat transfer coefficient [W/m²·K]
            A: Heat transfer area [m²]
            m_hot: Hot fluid mass flow rate [kg/s]
            m_cold: Cold fluid mass flow rate [kg/s]
            cp_hot: Hot fluid specific heat [J/kg·K]
            cp_cold: Cold fluid specific heat [J/kg·K]
            V_hot: Hot fluid volume [m³]
            V_cold: Cold fluid volume [m³]
            rho_hot: Hot fluid density [kg/m³]
            rho_cold: Cold fluid density [kg/m³]
            name: Model name
        """
        super().__init__(name)
        self.U = U
        self.A = A
        self.m_hot = m_hot
        self.m_cold = m_cold
        self.cp_hot = cp_hot
        self.cp_cold = cp_cold
        self.V_hot = V_hot
        self.V_cold = V_cold
        self.rho_hot = rho_hot
        self.rho_cold = rho_cold
        
        # Calculate heat capacities
        self.C_hot = m_hot * cp_hot      # Hot fluid heat capacity rate [W/K]
        self.C_cold = m_cold * cp_cold   # Cold fluid heat capacity rate [W/K]
        self.C_min = min(self.C_hot, self.C_cold)
        self.C_max = max(self.C_hot, self.C_cold)
        self.C_ratio = self.C_min / self.C_max if self.C_max > 0 else 0
        
        # Calculate NTU (Number of Transfer Units)
        self.NTU = U * A / self.C_min if self.C_min > 0 else 0
        
        # Calculate effectiveness for counter-current configuration
        if abs(self.C_ratio - 1.0) < 1e-6:
            self.effectiveness = self.NTU / (1 + self.NTU)
        else:
            if self.NTU > 0:
                exp_term = np.exp(-self.NTU * (1 - self.C_ratio))
                self.effectiveness = (1 - exp_term) / (1 - self.C_ratio * exp_term)
            else:
                self.effectiveness = 0
        
        # Thermal time constants
        self.tau_hot = self.rho_hot * self.V_hot * self.cp_hot / self.C_hot if self.C_hot > 0 else np.inf
        self.tau_cold = self.rho_cold * self.V_cold * self.cp_cold / self.C_cold if self.C_cold > 0 else np.inf
        
        self.parameters = {
            'U': U, 'A': A, 'm_hot': m_hot, 'm_cold': m_cold,
            'cp_hot': cp_hot, 'cp_cold': cp_cold, 'V_hot': V_hot, 'V_cold': V_cold,
            'rho_hot': rho_hot, 'rho_cold': rho_cold, 'effectiveness': self.effectiveness,
            'NTU': self.NTU, 'tau_hot': self.tau_hot, 'tau_cold': self.tau_cold
        }
        
        # Define state and input variables
        self.state_variables = {
            'T_hot_out': 'Hot fluid outlet temperature [K]',
            'T_cold_out': 'Cold fluid outlet temperature [K]'
        }
        
        self.inputs = {
            'T_hot_in': 'Hot fluid inlet temperature [K]',
            'T_cold_in': 'Cold fluid inlet temperature [K]',
            'm_hot': 'Hot fluid mass flow rate [kg/s]',
            'm_cold': 'Cold fluid mass flow rate [kg/s]'
        }
        
        self.outputs = {
            'T_hot_out': 'Hot fluid outlet temperature [K]',
            'T_cold_out': 'Cold fluid outlet temperature [K]',
            'Q': 'Heat transfer rate [W]',
            'effectiveness': 'Heat exchanger effectiveness [-]'
        }
    
    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Heat exchanger dynamics with thermal time constants.
        
        Args:
            t: Time
            x: [T_hot_out, T_cold_out]
            u: [T_hot_in, T_cold_in, m_hot_new, m_cold_new]
            
        Returns:
            [dT_hot_out/dt, dT_cold_out/dt]
        """
        T_hot_out = x[0]
        T_cold_out = x[1]
        T_hot_in = u[0]
        T_cold_in = u[1]
        
        # Update flow rates if provided
        if len(u) > 2:
            m_hot_current = u[2] if u[2] > 0 else self.m_hot
            m_cold_current = u[3] if u[3] > 0 else self.m_cold
        else:
            m_hot_current = self.m_hot
            m_cold_current = self.m_cold
        
        # Recalculate heat capacity rates with current flow rates
        C_hot_current = m_hot_current * self.cp_hot
        C_cold_current = m_cold_current * self.cp_cold
        C_min_current = min(C_hot_current, C_cold_current)
        C_max_current = max(C_hot_current, C_cold_current)
        
        # Recalculate effectiveness with current conditions
        if C_min_current > 0:
            C_ratio_current = C_min_current / C_max_current
            NTU_current = self.U * self.A / C_min_current
            
            if abs(C_ratio_current - 1.0) < 1e-6:
                eff_current = NTU_current / (1 + NTU_current)
            else:
                exp_term = np.exp(-NTU_current * (1 - C_ratio_current))
                eff_current = (1 - exp_term) / (1 - C_ratio_current * exp_term)
        else:
            eff_current = 0.0
        
        # Calculate steady-state outlet temperatures using effectiveness-NTU method
        Q_max = C_min_current * (T_hot_in - T_cold_in)
        Q_actual = eff_current * Q_max
        
        if C_hot_current > 0:
            T_hot_out_ss = T_hot_in - Q_actual / C_hot_current
        else:
            T_hot_out_ss = T_hot_in
            
        if C_cold_current > 0:
            T_cold_out_ss = T_cold_in + Q_actual / C_cold_current
        else:
            T_cold_out_ss = T_cold_in
        
        # Calculate time constants with current flow rates
        if m_hot_current > 0:
            tau_hot_current = self.rho_hot * self.V_hot * self.cp_hot / C_hot_current
        else:
            tau_hot_current = self.tau_hot
            
        if m_cold_current > 0:
            tau_cold_current = self.rho_cold * self.V_cold * self.cp_cold / C_cold_current
        else:
            tau_cold_current = self.tau_cold
        
        # First-order dynamics towards steady-state
        dT_hot_out_dt = (T_hot_out_ss - T_hot_out) / tau_hot_current
        dT_cold_out_dt = (T_cold_out_ss - T_cold_out) / tau_cold_current
        
        return np.array([dT_hot_out_dt, dT_cold_out_dt])
    
    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state outlet temperatures.
        
        Args:
            u: [T_hot_in, T_cold_in, m_hot, m_cold]
            
        Returns:
            [T_hot_out_ss, T_cold_out_ss]
        """
        T_hot_in = u[0]
        T_cold_in = u[1]
        
        # Use flow rates if provided, otherwise use design values
        if len(u) > 2:
            m_hot = u[2] if u[2] > 0 else self.m_hot
            m_cold = u[3] if u[3] > 0 else self.m_cold
        else:
            m_hot = self.m_hot
            m_cold = self.m_cold
        
        # Calculate heat capacity rates
        C_hot = m_hot * self.cp_hot
        C_cold = m_cold * self.cp_cold
        C_min = min(C_hot, C_cold)
        C_max = max(C_hot, C_cold)
        
        if C_min > 0:
            C_ratio = C_min / C_max
            NTU = self.U * self.A / C_min
            
            # Effectiveness for counter-current heat exchanger
            if abs(C_ratio - 1.0) < 1e-6:
                effectiveness = NTU / (1 + NTU)
            else:
                exp_term = np.exp(-NTU * (1 - C_ratio))
                effectiveness = (1 - exp_term) / (1 - C_ratio * exp_term)
            
            # Calculate heat transfer and outlet temperatures
            Q_max = C_min * (T_hot_in - T_cold_in)
            Q_actual = effectiveness * Q_max
            
            T_hot_out_ss = T_hot_in - Q_actual / C_hot
            T_cold_out_ss = T_cold_in + Q_actual / C_cold
        else:
            # No flow case
            T_hot_out_ss = T_hot_in
            T_cold_out_ss = T_cold_in
        
        return np.array([T_hot_out_ss, T_cold_out_ss])
    
    def calculate_heat_transfer_rate(self, T_hot_in: float, T_cold_in: float, 
                                   T_hot_out: float, T_cold_out: float) -> float:
        """
        Calculate the actual heat transfer rate.
        
        Args:
            T_hot_in: Hot fluid inlet temperature [K]
            T_cold_in: Cold fluid inlet temperature [K]
            T_hot_out: Hot fluid outlet temperature [K]
            T_cold_out: Cold fluid outlet temperature [K]
            
        Returns:
            Heat transfer rate [W]
        """
        Q_hot = self.C_hot * (T_hot_in - T_hot_out)
        Q_cold = self.C_cold * (T_cold_out - T_cold_in)
        
        # Return average (should be equal in steady state)
        return (Q_hot + Q_cold) / 2
    
    def calculate_lmtd(self, T_hot_in: float, T_cold_in: float, 
                       T_hot_out: float, T_cold_out: float) -> float:
        """
        Calculate Log Mean Temperature Difference (LMTD).
        
        Args:
            T_hot_in: Hot fluid inlet temperature [K]
            T_cold_in: Cold fluid inlet temperature [K]
            T_hot_out: Hot fluid outlet temperature [K]
            T_cold_out: Cold fluid outlet temperature [K]
            
        Returns:
            LMTD [K]
        """
        # Temperature differences at each end
        delta_T1 = T_hot_in - T_cold_out   # Hot inlet - Cold outlet
        delta_T2 = T_hot_out - T_cold_in   # Hot outlet - Cold inlet
        
        if abs(delta_T1 - delta_T2) < 1e-6:
            # Avoid division by zero when temperature differences are equal
            return delta_T1
        else:
            return (delta_T1 - delta_T2) / np.log(delta_T1 / delta_T2)
    
    def get_performance_metrics(self, x: np.ndarray, u: np.ndarray) -> Dict[str, float]:
        """
        Calculate performance metrics.
        
        Args:
            x: [T_hot_out, T_cold_out] - outlet temperatures
            u: [T_hot_in, T_cold_in, ...] - inlet conditions
            
        Returns:
            Dictionary with performance metrics
        """
        T_hot_out, T_cold_out = x
        T_hot_in, T_cold_in = u[0], u[1]
        
        Q = self.calculate_heat_transfer_rate(T_hot_in, T_cold_in, T_hot_out, T_cold_out)
        lmtd = self.calculate_lmtd(T_hot_in, T_cold_in, T_hot_out, T_cold_out)
        
        # Calculate current effectiveness
        Q_max = self.C_min * (T_hot_in - T_cold_in) if T_hot_in > T_cold_in else 0
        effectiveness = Q / Q_max if Q_max > 0 else 0
        
        return {
            'heat_transfer_rate': Q,
            'effectiveness': effectiveness,
            'lmtd': lmtd,
            'ntu': self.NTU,
            'hot_outlet_temp': T_hot_out,
            'cold_outlet_temp': T_cold_out,
            'temperature_approach': min(T_hot_out - T_cold_in, T_hot_in - T_cold_out)
        }
