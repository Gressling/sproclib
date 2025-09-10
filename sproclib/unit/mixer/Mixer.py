"""
Mixer class for SPROCLIB - Standard Process Control Library

This module contains the stream mixer model (steady-state and dynamic).
"""

import numpy as np
from ..base import ProcessModel


class Mixer(ProcessModel):
    """Generic stream mixer model for combining multiple input streams."""
    
    def __init__(
        self,
        n_inlets: int = 2,              # Number of inlet streams
        mixing_efficiency: float = 0.95, # Mixing efficiency [-]
        volume: float = 1.0,            # Mixer volume [m³]
        heat_transfer_coeff: float = 0.0, # Heat transfer coefficient [W/K]
        ambient_temp: float = 298.15,   # Ambient temperature [K]
        pressure_drop: float = 0.0,     # Pressure drop across mixer [Pa]
        name: str = "Mixer"
    ):
        super().__init__(name)
        self.n_inlets = n_inlets
        self.mixing_efficiency = mixing_efficiency
        self.volume = volume
        self.heat_transfer_coeff = heat_transfer_coeff
        self.ambient_temp = ambient_temp
        self.pressure_drop = pressure_drop
        
        self.parameters = {
            'n_inlets': n_inlets,
            'mixing_efficiency': mixing_efficiency,
            'volume': volume,
            'heat_transfer_coeff': heat_transfer_coeff,
            'ambient_temp': ambient_temp,
            'pressure_drop': pressure_drop
        }

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state outlet conditions for stream mixing.
        
        Args:
            u: [flow_1, T_1, P_1, flow_2, T_2, P_2, ..., flow_n, T_n, P_n]
               where each stream has flow rate [kg/s], temperature [K], pressure [Pa]
        
        Returns:
            [flow_out, T_out, P_out] - outlet flow rate [kg/s], temperature [K], pressure [Pa]
        """
        # Reshape input array to separate streams
        n_streams = len(u) // 3
        streams = u.reshape(n_streams, 3)
        
        flows = streams[:, 0]      # kg/s
        temps = streams[:, 1]      # K
        pressures = streams[:, 2]  # Pa
        
        # Total mass flow rate
        total_flow = np.sum(flows)
        
        if total_flow == 0:
            return np.array([0.0, self.ambient_temp, np.min(pressures)])
        
        # Mass-weighted average temperature (energy balance)
        # Assuming constant specific heat capacity for simplicity
        cp = 4186.0  # J/kg/K (water as reference)
        
        # Energy balance: sum(m_i * cp * T_i) = m_total * cp * T_out
        weighted_temp = np.sum(flows * temps) / total_flow
        
        # Apply mixing efficiency
        T_out = self.ambient_temp + self.mixing_efficiency * (weighted_temp - self.ambient_temp)
        
        # Heat transfer to/from environment
        if self.heat_transfer_coeff > 0:
            heat_loss = self.heat_transfer_coeff * (T_out - self.ambient_temp)
            # Adjust temperature for heat loss
            T_out = T_out - heat_loss / (total_flow * cp)
        
        # Pressure: minimum inlet pressure minus pressure drop
        P_out = np.min(pressures) - self.pressure_drop
        
        return np.array([total_flow, T_out, P_out])

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Dynamic model: mass and energy balances in the mixer volume.
        
        State: [mass, energy] (mass in kg, energy in J)
        Input: [flow_1, T_1, P_1, flow_2, T_2, P_2, ..., flow_n, T_n, P_n]
        """
        mass, energy = x
        
        # Reshape input array to separate streams
        n_streams = len(u) // 3
        streams = u.reshape(n_streams, 3)
        
        flows = streams[:, 0]      # kg/s
        temps = streams[:, 1]      # K
        pressures = streams[:, 2]  # Pa
        
        # Specific heat capacity (constant)
        cp = 4186.0  # J/kg/K
        
        # Current temperature in mixer
        if mass > 0:
            T_current = energy / (mass * cp)
        else:
            T_current = self.ambient_temp
        
        # Mass balance
        mass_in = np.sum(flows)
        
        # Outlet flow rate (assume perfect level control)
        if mass > 0:
            flow_out = mass_in  # Steady-state assumption for level control
        else:
            flow_out = 0
            
        dmass_dt = mass_in - flow_out
        
        # Energy balance
        energy_in = np.sum(flows * cp * temps)
        energy_out = flow_out * cp * T_current
        
        # Heat transfer to environment
        heat_transfer = self.heat_transfer_coeff * (T_current - self.ambient_temp)
        
        denergy_dt = energy_in - energy_out - heat_transfer
        
        return np.array([dmass_dt, denergy_dt])

    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the model including algorithms, 
                  parameters, equations, and usage information.
        """
        return {
            'type': 'Mixer',
            'description': 'Stream mixer model for combining multiple input streams with mass and energy balances',
            'category': 'unit/mixer',
            'algorithms': {
                'steady_state': 'Mass-weighted mixing: T_out = Σ(m_i * T_i) / Σ(m_i), P_out = min(P_i) - ΔP',
                'dynamics': 'Dynamic mass and energy balances: dm/dt = Σ(m_in) - m_out, dE/dt = Σ(m_in*cp*T_in) - m_out*cp*T_out - Q_loss',
                'energy_balance': 'Energy conservation with heat transfer: E = m * cp * T'
            },
            'parameters': {
                'n_inlets': {
                    'value': self.n_inlets,
                    'units': 'dimensionless',
                    'description': 'Number of inlet streams (typically 2-6 for industrial mixers)'
                },
                'mixing_efficiency': {
                    'value': self.mixing_efficiency,
                    'units': 'dimensionless',
                    'description': 'Mixing efficiency (0.90-0.99 for good mixing, 0.80-0.95 for moderate mixing)'
                },
                'volume': {
                    'value': self.volume,
                    'units': 'm³',
                    'description': 'Mixer volume for dynamic calculations'
                },
                'heat_transfer_coeff': {
                    'value': self.heat_transfer_coeff,
                    'units': 'W/K',
                    'description': 'Overall heat transfer coefficient to environment'
                },
                'ambient_temp': {
                    'value': self.ambient_temp,
                    'units': 'K',
                    'description': 'Ambient temperature for heat transfer calculations'
                },
                'pressure_drop': {
                    'value': self.pressure_drop,
                    'units': 'Pa',
                    'description': 'Pressure drop across the mixer due to mixing and fittings'
                }
            },
            'state_variables': {
                'mass': 'Total mass in mixer [kg]',
                'energy': 'Total thermal energy in mixer [J]'
            },
            'inputs': {
                'flow_i': 'Mass flow rate of inlet stream i [kg/s]',
                'T_i': 'Temperature of inlet stream i [K]',
                'P_i': 'Pressure of inlet stream i [Pa]'
            },
            'outputs': {
                'flow_out': 'Total outlet flow rate [kg/s]',
                'T_out': 'Outlet temperature [K]',
                'P_out': 'Outlet pressure [Pa]'
            },
            'valid_ranges': {
                'mixing_efficiency': {'min': 0.5, 'max': 1.0, 'units': 'dimensionless'},
                'n_inlets': {'min': 2, 'max': 10, 'units': 'dimensionless'},
                'volume': {'min': 0.001, 'max': 1000.0, 'units': 'm³'},
                'temperature': {'min': 273.15, 'max': 673.15, 'units': 'K'},
                'pressure': {'min': 1000.0, 'max': 10e6, 'units': 'Pa'}
            },
            'applications': [
                'Chemical process mixing operations',
                'Water treatment blending',
                'Food and beverage processing',
                'Pharmaceutical manufacturing',
                'Petroleum refining stream combining',
                'Wastewater treatment chemical addition',
                'HVAC system stream mixing',
                'Polymer processing additive mixing'
            ],
            'limitations': [
                'Assumes constant specific heat capacity',
                'No chemical reactions considered',
                'Perfect mixing assumption (no concentration gradients)',
                'Single-phase liquid mixing only',
                'No consideration of viscosity effects',
                'Simplified heat transfer model'
            ]
        }
