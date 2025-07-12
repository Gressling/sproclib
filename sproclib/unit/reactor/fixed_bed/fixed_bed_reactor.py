"""
Fixed Bed Reactor Model for SPROCLIB

This module provides a fixed bed catalytic reactor model
with axial discretization and catalyst kinetics.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import logging
from ...base import ProcessModel

class FixedBedReactor(ProcessModel):
    """Fixed bed catalytic reactor model."""
    
    def __init__(
        self,
        L: float = 5.0,              # Bed length [m]
        D: float = 1.0,              # Bed diameter [m]
        epsilon: float = 0.4,        # Bed porosity [-]
        rho_cat: float = 1500.0,     # Catalyst density [kg/m³]
        dp: float = 0.005,           # Particle diameter [m]
        k0: float = 1e6,             # Pre-exponential factor [m³/kg·s]
        Ea: float = 50000.0,         # Activation energy [J/mol]
        delta_H: float = -50000.0,   # Heat of reaction [J/mol]
        rho: float = 1000.0,         # Fluid density [kg/m³]
        cp: float = 4180.0,          # Heat capacity [J/kg·K]
        U: float = 100.0,            # Overall heat transfer coefficient [W/m²·K]
        n_segments: int = 20,        # Number of axial segments
        name: str = "FixedBedReactor"
    ):
        """
        Initialize fixed bed reactor.
        
        Args:
            L: Bed length [m]
            D: Bed diameter [m]
            epsilon: Bed porosity [-]
            rho_cat: Catalyst density [kg/m³]
            dp: Particle diameter [m]
            k0: Pre-exponential factor [m³/kg·s]
            Ea: Activation energy [J/mol]
            delta_H: Heat of reaction [J/mol]
            rho: Fluid density [kg/m³]
            cp: Heat capacity [J/kg·K]
            U: Overall heat transfer coefficient [W/m²·K]
            n_segments: Number of axial segments
            name: Model name
        """
        super().__init__(name)
        self.L = L
        self.D = D
        self.epsilon = epsilon
        self.rho_cat = rho_cat
        self.dp = dp
        self.k0 = k0
        self.Ea = Ea
        self.delta_H = delta_H
        self.rho = rho
        self.cp = cp
        self.U = U
        self.n_segments = n_segments
        
        # Calculate derived properties
        self.A_cross = np.pi * (D/2)**2  # Cross-sectional area
        self.V_total = self.A_cross * L  # Total volume
        self.V_void = self.V_total * epsilon  # Void volume
        self.dz = L / n_segments  # Segment length
        self.V_segment = self.V_void / n_segments  # Void volume per segment
        self.W_cat_segment = rho_cat * (1 - epsilon) * self.A_cross * self.dz  # Catalyst mass per segment
        self.A_heat = np.pi * D * self.dz  # Heat transfer area per segment
        
        self.parameters = {
            'L': L, 'D': D, 'epsilon': epsilon, 'rho_cat': rho_cat, 'dp': dp,
            'k0': k0, 'Ea': Ea, 'delta_H': delta_H, 'rho': rho, 'cp': cp, 'U': U,
            'n_segments': n_segments, 'A_cross': self.A_cross, 'V_segment': self.V_segment, 
            'W_cat_segment': self.W_cat_segment
        }
    
    def reaction_rate(self, CA: float, T: float) -> float:
        """
        Calculate reaction rate per unit catalyst mass.
        
        Args:
            CA: Concentration [mol/m³]
            T: Temperature [K]
            
        Returns:
            Reaction rate [mol/kg·s]
        """
        R = 8.314  # Gas constant [J/mol·K]
        k = self.k0 * np.exp(-self.Ea / (R * T))
        return k * CA  # First-order in concentration
    
    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Fixed bed reactor dynamics with axial discretization.
        
        State variables (for each segment):
        x[0:n_segments]: Concentration in each segment [mol/m³]
        x[n_segments:2*n_segments]: Temperature in each segment [K]
        
        Input variables:
        u[0]: Inlet volumetric flow rate [m³/s]
        u[1]: Inlet concentration [mol/m³]
        u[2]: Inlet temperature [K]
        u[3]: Wall temperature [K]
        
        Args:
            t: Time
            x: State vector [CA_segments, T_segments]
            u: [Q, CAi, Ti, Tw]
            
        Returns:
            State derivatives
        """
        Q = u[0]      # Volumetric flow rate
        CAi = u[1]    # Inlet concentration
        Ti = u[2]     # Inlet temperature
        Tw = u[3]     # Wall temperature
        
        # Extract concentrations and temperatures
        CA = x[0:self.n_segments]
        T = x[self.n_segments:2*self.n_segments]
        
        # Ensure positive values
        CA = np.maximum(CA, 0.0)
        T = np.maximum(T, 250.0)
        
        # Calculate derivatives
        dCAdt = np.zeros(self.n_segments)
        dTdt = np.zeros(self.n_segments)
        
        # Residence time in each segment (based on void volume)
        tau_segment = self.V_segment / Q if Q > 0 else 1e6
        
        for i in range(self.n_segments):
            # Reaction rate
            r = self.reaction_rate(CA[i], T[i])  # [mol/kg·s]
            r_vol = r * self.W_cat_segment / self.V_segment  # [mol/m³·s]
            
            # Convection terms
            if i == 0:
                # First segment - inlet conditions
                CA_in = CAi
                T_in = Ti
            else:
                # Subsequent segments
                CA_in = CA[i-1]
                T_in = T[i-1]
            
            # Material balance: dCA/dt = (CA_in - CA_out)/tau - r_vol
            dCAdt[i] = (CA_in - CA[i]) / tau_segment - r_vol
            
            # Energy balance
            heat_generation = (-self.delta_H * r_vol) / (self.rho * self.cp)
            heat_removal = (self.U * self.A_heat * (T[i] - Tw)) / (self.rho * self.cp * self.V_segment)
            
            dTdt[i] = (T_in - T[i]) / tau_segment + heat_generation - heat_removal
        
        return np.concatenate([dCAdt, dTdt])
    
    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state concentration and temperature profile.
        
        Args:
            u: [Q, CAi, Ti, Tw]
            
        Returns:
            Steady-state values [CA_segments, T_segments]
        """
        Q, CAi, Ti, Tw = u
        
        # Initialize arrays
        CA = np.zeros(self.n_segments)
        T = np.zeros(self.n_segments)
        
        # Residence time per segment
        tau_segment = self.V_segment / Q if Q > 0 else 1e6
        
        # March along reactor length
        CA_current = CAi
        T_current = Ti
        
        for i in range(self.n_segments):
            # Solve steady-state equations for this segment
            r = self.reaction_rate(CA_current, T_current)
            r_vol = r * self.W_cat_segment / self.V_segment
            
            # Update concentration
            CA_out = CA_current - r_vol * tau_segment
            
            # Update temperature
            heat_gen = (-self.delta_H * r_vol) / (self.rho * self.cp)
            heat_removal = (self.U * self.A_heat * (T_current - Tw)) / (self.rho * self.cp * self.V_segment)
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
            dict: Metadata about the FixedBedReactor model including
                  algorithms, parameters, equations, and usage information.
        """
        return {
            'type': 'FixedBedReactor',
            'description': 'Fixed bed catalytic reactor with axial discretization',
            'category': 'reactor',
            'algorithms': {
                'reaction_kinetics': 'Arrhenius equation: k = k0 * exp(-Ea/RT)',
                'material_balance': 'dCA/dt = -u*dCA/dz - k(T)*CA*W_cat/V_void',
                'energy_balance': 'dT/dt = -u*dT/dz + (-ΔH*r*W_cat)/(ρ*cp*V_void) + UA(Tw-T)/(ρ*cp*V_void)',
                'bed_properties': 'Void fraction, catalyst loading, pressure drop calculations'
            },
            'parameters': {
                'L': {'value': self.L, 'units': 'm', 'description': 'Bed length'},
                'D': {'value': self.D, 'units': 'm', 'description': 'Bed diameter'},
                'epsilon': {'value': self.epsilon, 'units': '-', 'description': 'Bed porosity'},
                'rho_cat': {'value': self.rho_cat, 'units': 'kg/m³', 'description': 'Catalyst density'},
                'dp': {'value': self.dp, 'units': 'm', 'description': 'Particle diameter'},
                'k0': {'value': self.k0, 'units': 'm³/kg·s', 'description': 'Pre-exponential factor'},
                'Ea': {'value': self.Ea, 'units': 'J/mol', 'description': 'Activation energy'},
                'delta_H': {'value': self.delta_H, 'units': 'J/mol', 'description': 'Heat of reaction'},
                'U': {'value': self.U, 'units': 'W/m²·K', 'description': 'Heat transfer coefficient'}
            },
            'state_variables': {
                'CA_segments': 'Concentration in each segment [mol/m³]',
                'T_segments': 'Temperature in each segment [K]'
            },
            'inputs': {
                'u': 'Superficial velocity [m/s]',
                'CAi': 'Inlet concentration [mol/m³]',
                'Ti': 'Inlet temperature [K]',
                'Tw': 'Wall temperature [K]'
            },
            'outputs': {
                'CA_profile': 'Concentration profile [mol/m³]',
                'T_profile': 'Temperature profile [K]',
                'conversion': 'Conversion at exit',
                'pressure_drop': 'Pressure drop [Pa]'
            },
            'valid_ranges': {
                'L': {'min': 0.1, 'max': 20.0, 'units': 'm'},
                'T': {'min': 250.0, 'max': 1000.0, 'units': 'K'},
                'epsilon': {'min': 0.2, 'max': 0.8, 'units': '-'},
                'dp': {'min': 0.001, 'max': 0.01, 'units': 'm'}
            },
            'applications': [
                'Catalytic processes',
                'Petrochemical reactors',
                'Environmental catalysis',
                'Hydrogenation reactions',
                'Oxidation processes'
            ],
            'limitations': [
                'No radial gradients',
                'Isothermal catalyst particles',
                'No catalyst deactivation',
                'Constant porosity',
                'Single reaction pathway'
            ]
        }

