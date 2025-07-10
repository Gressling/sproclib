"""
Binary Distillation Column Model for SPROCLIB

This module provides a binary distillation column model
for control design with multiple trays and material balance dynamics.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import logging
from typing import Dict
from ...base import ProcessModel
from ..tray import DistillationTray

logger = logging.getLogger(__name__)


class BinaryDistillationColumn(ProcessModel):
    """Simplified binary distillation column model for control design."""
    
    def __init__(
        self,
        N_trays: int = 20,              # Total number of trays
        feed_tray: int = 10,            # Feed tray location
        alpha: float = 2.5,             # Relative volatility (-)
        tray_holdup: float = 1.0,       # Liquid holdup per tray [kmol]
        reflux_drum_holdup: float = 5.0, # Reflux drum holdup [kmol]
        reboiler_holdup: float = 10.0,  # Reboiler holdup [kmol]
        feed_flow: float = 100.0,       # Feed flow rate [kmol/min]
        feed_composition: float = 0.5,  # Feed composition (light component)
        name: str = "BinaryDistillationColumn"
    ):
        """
        Initialize binary distillation column.
        
        Args:
            N_trays: Total number of trays (including reboiler, excluding condenser)
            feed_tray: Feed tray number (1 = top tray)
            alpha: Relative volatility (light/heavy) [-]
            tray_holdup: Liquid holdup per tray [kmol]
            reflux_drum_holdup: Reflux drum holdup [kmol]
            reboiler_holdup: Reboiler holdup [kmol]
            feed_flow: Feed flow rate [kmol/min]
            feed_composition: Feed composition (mole fraction light component)
            name: Model name
        """
        super().__init__(name)
        self.N_trays = N_trays
        self.feed_tray = feed_tray
        self.alpha = alpha
        self.tray_holdup = tray_holdup
        self.reflux_drum_holdup = reflux_drum_holdup
        self.reboiler_holdup = reboiler_holdup
        self.feed_flow = feed_flow
        self.feed_composition = feed_composition
        
        # Create individual tray models
        self.trays = []
        for i in range(N_trays):
            tray = DistillationTray(
                tray_number=i+1,
                holdup=tray_holdup,
                alpha=alpha,
                name=f"Tray_{i+1}"
            )
            self.trays.append(tray)
        
        self.parameters = {
            'N_trays': N_trays,
            'feed_tray': feed_tray,
            'alpha': alpha,
            'tray_holdup': tray_holdup,
            'reflux_drum_holdup': reflux_drum_holdup,
            'reboiler_holdup': reboiler_holdup,
            'feed_flow': feed_flow,
            'feed_composition': feed_composition
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
        Column dynamics: material balances for all trays.
        
        State variables:
        x[0:N_trays]: Liquid compositions on trays (light component)
        x[N_trays]: Reflux drum composition
        x[N_trays+1]: Reboiler composition
        
        Input variables:
        u[0]: Reflux ratio [-]
        u[1]: Reboiler heat duty [energy/time]
        u[2]: Distillate flow rate [kmol/min]
        u[3]: Bottoms flow rate [kmol/min]
        
        Args:
            t: Time
            x: State vector [tray compositions, drum composition, reboiler composition]
            u: [R, Q_reboiler, D, B]
            
        Returns:
            State derivatives
        """
        # Extract inputs
        R = max(0.1, u[0])      # Reflux ratio
        Q_reb = u[1]            # Reboiler heat duty
        D = max(0.1, u[2])      # Distillate flow rate
        B = max(0.1, u[3])      # Bottoms flow rate
        
        # Calculate internal flows
        L = R * D               # Reflux flow rate
        V = L + D               # Vapor flow rate (above feed)
        L_below = L + self.feed_flow  # Liquid flow rate below feed
        V_below = V             # Vapor flow rate below feed (assuming saturated liquid feed)
        
        # Extract compositions
        tray_compositions = x[0:self.N_trays]
        drum_composition = x[self.N_trays]
        reboiler_composition = x[self.N_trays + 1]
        
        # Ensure compositions are in valid range
        tray_compositions = np.clip(tray_compositions, 0.001, 0.999)
        drum_composition = np.clip(drum_composition, 0.001, 0.999)
        reboiler_composition = np.clip(reboiler_composition, 0.001, 0.999)
        
        dxdt = np.zeros(self.N_trays + 2)
        
        # Tray dynamics
        for i in range(self.N_trays):
            tray_num = i + 1
            x_tray = tray_compositions[i]
            
            # Vapor composition leaving this tray
            y_tray = self.vapor_liquid_equilibrium(x_tray)
            
            if tray_num == 1:  # Top tray
                # Liquid in from reflux drum
                L_in = L
                x_in = drum_composition
                # Vapor in from tray below
                V_in = V
                y_in = self.vapor_liquid_equilibrium(tray_compositions[i+1]) if i+1 < self.N_trays else self.vapor_liquid_equilibrium(reboiler_composition)
                # Flows out
                L_out = L + D if tray_num < self.feed_tray else L_below
                V_out = V
                
            elif tray_num == self.feed_tray:  # Feed tray
                # Liquid in from tray above
                L_in = L
                x_in = tray_compositions[i-1]
                # Vapor in from tray below
                V_in = V_below
                y_in = self.vapor_liquid_equilibrium(tray_compositions[i+1]) if i+1 < self.N_trays else self.vapor_liquid_equilibrium(reboiler_composition)
                # Flows out
                L_out = L_below
                V_out = V
                
                # Add feed contribution
                feed_contribution = self.feed_flow * self.feed_composition
                
            elif tray_num == self.N_trays:  # Bottom tray (reboiler)
                # Liquid in from tray above
                L_in = L_below
                x_in = tray_compositions[i-1]
                # No vapor in from below
                V_in = 0
                y_in = 0
                # Flows out
                L_out = B
                V_out = V_below
                
            else:  # Intermediate trays
                # Liquid in from tray above
                L_in = L if tray_num < self.feed_tray else L_below
                x_in = tray_compositions[i-1]
                # Vapor in from tray below
                V_in = V if tray_num < self.feed_tray else V_below
                y_in = self.vapor_liquid_equilibrium(tray_compositions[i+1]) if i+1 < self.N_trays else self.vapor_liquid_equilibrium(reboiler_composition)
                # Flows out
                L_out = L if tray_num < self.feed_tray else L_below
                V_out = V if tray_num < self.feed_tray else V_below
            
            # Component balance for light component
            light_in = L_in * x_in + V_in * y_in
            light_out = L_out * x_tray + V_out * y_tray
            
            # Add feed if this is the feed tray
            if tray_num == self.feed_tray:
                light_in += self.feed_flow * self.feed_composition
            
            dxdt[i] = (light_in - light_out) / self.tray_holdup
        
        # Reflux drum dynamics
        # Vapor from top tray condenses, distillate and reflux leave
        y_top = self.vapor_liquid_equilibrium(tray_compositions[0])
        vapor_condensed = V * y_top
        liquid_out_drum = (L + D) * drum_composition
        
        dxdt[self.N_trays] = (vapor_condensed - liquid_out_drum) / self.reflux_drum_holdup
        
        # Reboiler dynamics
        # Liquid from bottom tray enters, vapor and bottoms leave
        if self.N_trays > 1:
            liquid_in_reb = L_below * tray_compositions[-1]
        else:
            liquid_in_reb = L_below * drum_composition
        
        y_reb = self.vapor_liquid_equilibrium(reboiler_composition)
        vapor_out_reb = V_below * y_reb
        bottoms_out = B * reboiler_composition
        
        dxdt[self.N_trays + 1] = (liquid_in_reb - vapor_out_reb - bottoms_out) / self.reboiler_holdup
        
        return dxdt
    
    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state with distillation column.
        
        Args:
            u: Input variables [R, Q_reboiler, D, B] - reflux ratio, heat duty, distillate, bottoms
            
        Returns:
            Steady-state values
        """
        R, Q_reb, D, B = u
        
        # Use Fenske-Underwood-Gilliland shortcut method approximation
        # This is a simplified version for control-oriented modeling
        
        # Calculate minimum reflux ratio (approximate)
        R_min = (self.feed_composition / (1 - self.feed_composition)) * ((1 - 0.95) / 0.95) / (self.alpha - 1)
        R_min = max(0.1, R_min)
        
        # Ensure operating reflux ratio is above minimum
        R_operating = max(R, 1.2 * R_min)
        
        # Calculate composition profile using approximate methods
        compositions = np.zeros(self.N_trays + 2)
        
        # Distillate composition (approximate)
        x_D = min(0.95, self.feed_composition * 1.8)
        compositions[self.N_trays] = x_D  # Reflux drum
        
        # Bottoms composition (approximate)
        x_B = max(0.05, self.feed_composition * 0.2)
        compositions[self.N_trays + 1] = x_B  # Reboiler
        
        # Composition profile on trays (linear approximation)
        for i in range(self.N_trays):
            if i < self.feed_tray - 1:
                # Rectifying section
                fraction = i / (self.feed_tray - 1)
                compositions[i] = x_D - fraction * (x_D - self.feed_composition)
            else:
                # Stripping section
                fraction = (i - self.feed_tray + 1) / (self.N_trays - self.feed_tray)
                compositions[i] = self.feed_composition - fraction * (self.feed_composition - x_B)
        
        # Ensure all compositions are in valid range
        compositions = np.clip(compositions, 0.001, 0.999)
        
        return compositions
    
    def calculate_separation_metrics(self, compositions: np.ndarray) -> Dict[str, float]:
        """
        Calculate key separation performance metrics.
        
        Args:
            compositions: Current composition profile
            
        Returns:
            Dictionary with separation metrics
        """
        x_D = compositions[self.N_trays]      # Distillate composition
        x_B = compositions[self.N_trays + 1]  # Bottoms composition
        
        # Recovery of light component in distillate
        light_recovery = (x_D * self.feed_flow) / (self.feed_composition * self.feed_flow) if self.feed_composition > 0 else 0
        
        # Purity metrics
        distillate_purity = x_D
        bottoms_purity = 1 - x_B  # Purity of heavy component in bottoms
        
        # Separation factor
        separation_factor = (x_D / (1 - x_D)) / (x_B / (1 - x_B)) if x_B < 0.999 and x_D > 0.001 else float('inf')
        
        return {
            'distillate_composition': x_D,
            'bottoms_composition': x_B,
            'light_recovery': light_recovery,
            'distillate_purity': distillate_purity,
            'bottoms_purity': bottoms_purity,
            'separation_factor': separation_factor
        }
    
    def calculate_minimum_reflux(self) -> float:
        """
        Calculate minimum reflux ratio using simplified approximation.
        
        Returns:
            Minimum reflux ratio
        """
        # Simplified calculation for binary system
        # Using approximate method for control-oriented modeling
        
        # For binary system, approximate minimum reflux using relative volatility
        # R_min ≈ (x_D/(1-x_D)) * (1-x_F)/x_F * 1/(α-1)
        
        # Assume target distillate composition (typical high purity)
        x_D_target = 0.95
        x_F = self.feed_composition
        
        if x_F > 0.001 and x_F < 0.999 and self.alpha > 1.001:
            R_min = (x_D_target / (1 - x_D_target)) * ((1 - x_F) / x_F) * (1 / (self.alpha - 1))
        else:
            # Fallback for edge cases
            R_min = 1.0
        
        return max(0.1, R_min)
    
    def update_parameters(self, **kwargs):
        """
        Update column parameters and recalculate derived values.
        
        Args:
            **kwargs: Parameter updates
        """
        # Update parameters
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # Update parameters dictionary
        self.parameters.update(kwargs)
        
        # Update tray models if needed
        if 'alpha' in kwargs:
            for tray in self.trays:
                tray.alpha = self.alpha
