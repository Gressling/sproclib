"""
Distillation Tray Model for SPROCLIB

This module provides a model for individual distillation trays
in binary systems with vapor-liquid equilibrium.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import logging
from ...base import ProcessModel

logger = logging.getLogger(__name__)


class DistillationTray(ProcessModel):
    """Individual distillation tray model for binary systems."""
    
    def __init__(
        self,
        tray_number: int = 1,
        holdup: float = 1.0,         # Liquid holdup [kmol]
        alpha: float = 2.5,          # Relative volatility (-)
        name: str = "DistillationTray"
    ):
        """
        Initialize distillation tray.
        
        Args:
            tray_number: Tray number (1 = top)
            holdup: Liquid holdup on tray [kmol]
            alpha: Relative volatility (light/heavy) [-]
            name: Model name
        """
        super().__init__(name)
        self.tray_number = tray_number
        self.holdup = holdup
        self.alpha = alpha
        
        self.parameters = {
            'tray_number': tray_number,
            'holdup': holdup,
            'alpha': alpha
        }
    
    def vapor_liquid_equilibrium(self, x: float) -> float:
        """
        Calculate vapor composition using relative volatility.
        
        Args:
            x: Liquid mole fraction of light component
            
        Returns:
            Vapor mole fraction of light component
        """
        return self.alpha * x / (1 + (self.alpha - 1) * x)
    
    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Tray dynamics: component material balance.
        
        State variables:
        x[0]: Liquid mole fraction of light component on tray
        
        Input variables:
        u[0]: Liquid flow rate from tray above [kmol/min]
        u[1]: Liquid composition from tray above [mole fraction]
        u[2]: Vapor flow rate from tray below [kmol/min]
        u[3]: Vapor composition from tray below [mole fraction]
        u[4]: Liquid flow rate from this tray [kmol/min]
        u[5]: Vapor flow rate from this tray [kmol/min]
        
        Args:
            t: Time
            x: [x_tray] - liquid composition on tray
            u: [L_in, x_in, V_in, y_in, L_out, V_out]
            
        Returns:
            [dx_tray/dt]
        """
        x_tray = max(0.0, min(1.0, x[0]))  # Constrain to [0,1]
        
        L_in = u[0]      # Liquid in from above
        x_in = u[1]      # Liquid composition in
        V_in = u[2]      # Vapor in from below
        y_in = u[3]      # Vapor composition in
        L_out = u[4]     # Liquid out
        V_out = u[5]     # Vapor out
        
        # Vapor composition leaving this tray (VLE)
        y_out = self.vapor_liquid_equilibrium(x_tray)
        
        # Component material balance for light component
        # Accumulation = In - Out
        light_in = L_in * x_in + V_in * y_in
        light_out = L_out * x_tray + V_out * y_out
        
        dx_dt = (light_in - light_out) / self.holdup
        
        return np.array([dx_dt])
    
    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state composition.
        
        For steady state: dx/dt = 0
        Light_in = Light_out
        L_in * x_in + V_in * y_in = L_out * x + V_out * y
        
        Args:
            u: [L_in, x_in, V_in, y_in, L_out, V_out]
            
        Returns:
            [x_tray_ss] - steady-state liquid composition
        """
        L_in, x_in, V_in, y_in, L_out, V_out = u
        
        # Solve: L_in * x_in + V_in * y_in = L_out * x + V_out * y
        # where y = alpha * x / (1 + (alpha - 1) * x)
        
        def objective(x):
            if x < 0 or x > 1:
                return 1e6  # Penalty for invalid compositions
            y = self.vapor_liquid_equilibrium(x)
            return abs(L_in * x_in + V_in * y_in - L_out * x - V_out * y)
        
        # Find solution using simple search
        from scipy.optimize import minimize_scalar
        result = minimize_scalar(objective, bounds=(0, 1), method='bounded')
        
        return np.array([result.x])
