"""
Plug Flow Reactor (PFR) Model for SPROCLIB

This module provides a PFR model with axial discretization,
reaction kinetics, and thermal dynamics.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import logging
from ..base import ProcessModel

logger = logging.getLogger(__name__)


class PlugFlowReactor(ProcessModel):
    """Plug Flow Reactor (PFR) model with axial discretization."""
    
    def __init__(
        self,
        L: float = 10.0,             # Reactor length [m]
        A_cross: float = 0.1,        # Cross-sectional area [m²]
        n_segments: int = 20,        # Number of discretization segments
        k0: float = 7.2e10,          # Pre-exponential factor [1/min]
        Ea: float = 72750.0,         # Activation energy [J/mol]
        delta_H: float = -52000.0,   # Heat of reaction [J/mol]
        rho: float = 1000.0,         # Density [kg/m³]
        cp: float = 4180.0,          # Heat capacity [J/kg·K]
        U: float = 500.0,            # Heat transfer coefficient [W/m²·K]
        D_tube: float = 0.1,         # Tube diameter [m]
        name: str = "PlugFlowReactor"
    ):
        """
        Initialize plug flow reactor with axial discretization.
        
        Args:
            L: Reactor length [m]
            A_cross: Cross-sectional area [m²]
            n_segments: Number of axial segments for discretization
            k0: Pre-exponential factor [1/min]
            Ea: Activation energy [J/mol]
            delta_H: Heat of reaction [J/mol]
            rho: Density [kg/m³]
            cp: Heat capacity [J/kg·K]
            U: Heat transfer coefficient [W/m²·K]
            D_tube: Tube diameter [m]
            name: Model name
        """
        super().__init__(name)
        self.L = L
        self.A_cross = A_cross
        self.n_segments = n_segments
        self.k0 = k0
        self.Ea = Ea
        self.delta_H = delta_H
        self.rho = rho
        self.cp = cp
        self.U = U
        self.D_tube = D_tube
        
        # Calculate segment properties
        self.dz = L / n_segments  # Segment length
        self.V_segment = A_cross * self.dz  # Volume per segment
        self.A_heat = np.pi * D_tube * self.dz  # Heat transfer area per segment
        
        self.parameters = {
            'L': L, 'A_cross': A_cross, 'n_segments': n_segments,
            'k0': k0, 'Ea': Ea, 'delta_H': delta_H, 'rho': rho, 'cp': cp,
            'U': U, 'D_tube': D_tube, 'dz': self.dz, 'V_segment': self.V_segment
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
        PFR dynamics with axial discretization.
        
        State variables (for each segment):
        x[0:n_segments]: Concentration in each segment [mol/L]
        x[n_segments:2*n_segments]: Temperature in each segment [K]
        
        Input variables:
        u[0]: Inlet flow rate [L/min]
        u[1]: Inlet concentration [mol/L]
        u[2]: Inlet temperature [K]
        u[3]: Coolant temperature [K]
        
        Args:
            t: Time
            x: State vector [CA_segments, T_segments]
            u: [q, CAi, Ti, Tc]
            
        Returns:
            State derivatives
        """
        q = u[0]      # Flow rate
        CAi = u[1]    # Inlet concentration
        Ti = u[2]     # Inlet temperature
        Tc = u[3]     # Coolant temperature
        
        # Extract concentrations and temperatures
        CA = x[0:self.n_segments]
        T = x[self.n_segments:2*self.n_segments]
        
        # Ensure positive values
        CA = np.maximum(CA, 0.0)
        T = np.maximum(T, 250.0)
        
        # Calculate derivatives
        dCAdt = np.zeros(self.n_segments)
        dTdt = np.zeros(self.n_segments)
        
        # Residence time in each segment
        tau_segment = self.V_segment / q if q > 0 else 1e6
        
        for i in range(self.n_segments):
            # Reaction rate
            r = self.reaction_rate(CA[i], T[i])
            
            # Convection terms
            if i == 0:
                # First segment - inlet conditions
                CA_in = CAi
                T_in = Ti
            else:
                # Subsequent segments
                CA_in = CA[i-1]
                T_in = T[i-1]
            
            # Material balance: dCA/dt = (CA_in - CA_out)/tau - r
            dCAdt[i] = (CA_in - CA[i]) / tau_segment - r
            
            # Energy balance: dT/dt = (T_in - T_out)/tau + (-ΔH*r)/(ρ*cp) - UA(T-Tc)/(ρ*cp*V)
            heat_generation = (-self.delta_H * r) / (self.rho * self.cp)
            heat_removal = (self.U * self.A_heat * (T[i] - Tc)) / (self.rho * self.cp * self.V_segment)
            
            dTdt[i] = (T_in - T[i]) / tau_segment + heat_generation - heat_removal
        
        return np.concatenate([dCAdt, dTdt])
    
    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state concentration and temperature profile.
        
        Args:
            u: [q, CAi, Ti, Tc]
            
        Returns:
            Steady-state values [CA_segments, T_segments]
        """
        q, CAi, Ti, Tc = u
        
        # Initialize arrays
        CA = np.zeros(self.n_segments)
        T = np.zeros(self.n_segments)
        
        # Residence time per segment
        tau_segment = self.V_segment / q if q > 0 else 1e6
        
        # March along reactor length
        CA_current = CAi
        T_current = Ti
        
        for i in range(self.n_segments):
            # Solve steady-state equations for this segment
            # At steady state: 0 = (CA_in - CA_out)/tau - r
            # 0 = (T_in - T_out)/tau + heat_generation - heat_removal
            
            # Use simple forward Euler for steady-state approximation
            r = self.reaction_rate(CA_current, T_current)
            
            # Update concentration
            CA_out = CA_current - r * tau_segment  # Simplified
            
            # Update temperature
            heat_gen = (-self.delta_H * r) / (self.rho * self.cp)
            heat_removal = (self.U * self.A_heat * (T_current - Tc)) / (self.rho * self.cp * self.V_segment)
            T_out = T_current + (heat_gen - heat_removal) * tau_segment
            
            # Store values
            CA[i] = max(0.0, CA_out)
            T[i] = max(250.0, T_out)
            
            # Update for next segment
            CA_current = CA[i]
            T_current = T[i]
        
        return np.concatenate([CA, T])
    
    def calculate_conversion(self, x: np.ndarray) -> float:
        """
        Calculate conversion at reactor exit.
        
        Args:
            x: State vector [CA_segments, T_segments]
            
        Returns:
            Conversion fraction
        """
        CA_inlet = x[0] if len(x) > 0 else 1.0
        CA_exit = x[self.n_segments - 1] if len(x) >= self.n_segments else 0.5
        
        if CA_inlet > 0:
            conversion = (CA_inlet - CA_exit) / CA_inlet
        else:
            conversion = 0.0
        
        return max(0.0, min(1.0, conversion))
    
    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the PlugFlowReactor model including
                  algorithms, parameters, equations, and usage information.
        """
        return {
            'type': 'PlugFlowReactor',
            'description': 'Plug flow reactor with axial discretization and thermal effects',
            'category': 'reactor',
            'algorithms': {
                'reaction_kinetics': 'Arrhenius equation: k = k0 * exp(-Ea/RT)',
                'material_balance': 'dCA/dt = -u*dCA/dz - k(T)*CA (per segment)',
                'energy_balance': 'dT/dt = -u*dT/dz + (-ΔH*r)/(ρ*cp) + UA(Tw-T)/(ρ*cp*V_seg)',
                'discretization': 'Axial discretization with finite differences'
            },
            'parameters': {
                'L': {'value': self.L, 'units': 'm', 'description': 'Reactor length'},
                'A_cross': {'value': self.A_cross, 'units': 'm²', 'description': 'Cross-sectional area'},
                'n_segments': {'value': self.n_segments, 'units': '-', 'description': 'Number of segments'},
                'k0': {'value': self.k0, 'units': '1/min', 'description': 'Pre-exponential factor'},
                'Ea': {'value': self.Ea, 'units': 'J/mol', 'description': 'Activation energy'},
                'delta_H': {'value': self.delta_H, 'units': 'J/mol', 'description': 'Heat of reaction'},
                'rho': {'value': self.rho, 'units': 'kg/m³', 'description': 'Density'},
                'cp': {'value': self.cp, 'units': 'J/kg·K', 'description': 'Heat capacity'},
                'U': {'value': self.U, 'units': 'W/m²·K', 'description': 'Heat transfer coefficient'},
                'D_tube': {'value': self.D_tube, 'units': 'm', 'description': 'Tube diameter'}
            },
            'state_variables': {
                'CA_segments': 'Concentration in each segment [mol/L]',
                'T_segments': 'Temperature in each segment [K]'
            },
            'inputs': {
                'q': 'Inlet flow rate [L/min]',
                'CAi': 'Inlet concentration [mol/L]',
                'Ti': 'Inlet temperature [K]',
                'Tw': 'Wall temperature [K]'
            },
            'outputs': {
                'CA_profile': 'Concentration profile [mol/L]',
                'T_profile': 'Temperature profile [K]',
                'conversion': 'Conversion at exit',
                'pressure_drop': 'Pressure drop [Pa]'
            },
            'valid_ranges': {
                'L': {'min': 0.1, 'max': 100.0, 'units': 'm'},
                'T': {'min': 250.0, 'max': 800.0, 'units': 'K'},
                'CA': {'min': 0.0, 'max': 100.0, 'units': 'mol/L'},
                'n_segments': {'min': 5, 'max': 200, 'units': '-'}
            },
            'applications': [
                'Tubular reactors',
                'Catalytic processes',
                'High-temperature reactions',
                'Continuous production',
                'Heat exchanger reactors'
            ],
            'limitations': [
                'No radial mixing assumed',
                'Single reaction kinetics',
                'Constant physical properties',
                'No catalyst deactivation',
                'Steady axial flow assumption'
            ]
        }


__all__ = ['PlugFlowReactor']
