"""
Screw Feeder class for SPROCLIB - Standard Process Control Library

This module contains the screw feeder transport model (steady-state and dynamic).
"""

import numpy as np
from .....unit.base import ProcessModel


class ScrewFeeder(ProcessModel):
    """Screw feeder transport model for precise powder feeding (steady-state and dynamic)."""
    
    def __init__(
        self,
        screw_diameter: float = 0.05,   # Screw diameter [m]
        screw_length: float = 0.5,      # Screw length [m]
        screw_pitch: float = 0.025,     # Screw pitch [m]
        screw_speed: float = 100.0,     # Screw speed [rpm]
        fill_factor: float = 0.3,       # Screw fill factor [-]
        powder_density: float = 800.0,  # Powder bulk density [kg/m³]
        powder_flowability: float = 0.8, # Powder flowability index [-]
        motor_torque_max: float = 10.0, # Maximum motor torque [N⋅m]
        name: str = "ScrewFeeder"
    ):
        super().__init__(name)
        self.screw_diameter = screw_diameter
        self.screw_length = screw_length
        self.screw_pitch = screw_pitch
        self.screw_speed = screw_speed
        self.fill_factor = fill_factor
        self.powder_density = powder_density
        self.powder_flowability = powder_flowability
        self.motor_torque_max = motor_torque_max
        self.parameters = {
            'screw_diameter': screw_diameter, 'screw_length': screw_length, 'screw_pitch': screw_pitch,
            'screw_speed': screw_speed, 'fill_factor': fill_factor, 'powder_density': powder_density,
            'powder_flowability': powder_flowability, 'motor_torque_max': motor_torque_max
        }

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state feed rate and motor torque.
        Args:
            u: [screw_speed_setpoint, hopper_level, powder_moisture]
        Returns:
            [mass_flow_rate, motor_torque]
        """
        screw_speed, hopper_level, moisture = u
        
        # Screw volumetric capacity
        screw_cross_area = np.pi * (self.screw_diameter/2)**2
        volume_per_revolution = screw_cross_area * self.screw_pitch
        
        # Theoretical volumetric flow rate
        theoretical_volume_flow = (screw_speed / 60.0) * volume_per_revolution
        
        # Effective fill factor considering hopper level and powder properties
        level_factor = min(1.0, hopper_level / 0.5)  # Reduced efficiency at low levels
        moisture_factor = max(0.7, 1.0 - 2.0 * moisture)  # Reduced flow with moisture
        flowability_factor = self.powder_flowability
        
        effective_fill = self.fill_factor * level_factor * moisture_factor * flowability_factor
        
        # Actual volumetric flow
        actual_volume_flow = theoretical_volume_flow * effective_fill
        
        # Mass flow rate
        mass_flow_rate = actual_volume_flow * self.powder_density
        
        # Motor torque calculation
        # Base torque for screw rotation
        base_torque = 0.1 * self.motor_torque_max
        
        # Load torque (proportional to material resistance)
        load_factor = effective_fill * (1 + moisture * 2)  # Moisture increases resistance
        load_torque = load_factor * 0.7 * self.motor_torque_max
        
        total_torque = base_torque + load_torque
        
        # Torque limiting
        if total_torque > self.motor_torque_max:
            # Reduce effective speed due to torque limit
            speed_reduction = self.motor_torque_max / total_torque
            mass_flow_rate *= speed_reduction
            total_torque = self.motor_torque_max
        
        return np.array([mass_flow_rate, total_torque])

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Dynamic model: feed rate and torque response.
        State: [mass_flow_rate, motor_torque]
        Input: [screw_speed_setpoint, hopper_level, powder_moisture]
        """
        flow_rate, torque = x
        flow_ss, torque_ss = self.steady_state(u)
        
        # Flow rate response (residence time in screw)
        screw_speed = u[0]
        if screw_speed > 0:
            residence_time = 60.0 * self.screw_length / (self.screw_pitch * screw_speed)
        else:
            residence_time = 10.0
        tau_flow = residence_time + 3.0  # s, additional response time
        
        # Torque response (motor dynamics)
        tau_torque = 1.0  # s, motor response time constant
        
        dflow_dt = (flow_ss - flow_rate) / tau_flow
        dtorque_dt = (torque_ss - torque) / tau_torque
        
        return np.array([dflow_dt, dtorque_dt])

    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the ScrewFeeder model including
                  algorithms, parameters, equations, and usage information.
        """
        return {
            'class_name': 'ScrewFeeder',
            'algorithm': 'Volumetric screw feeding with torque calculation and fill factor corrections',
            'parameters': {
                'screw_diameter': {'value': self.screw_diameter, 'unit': 'm', 'description': 'Screw diameter'},
                'screw_length': {'value': self.screw_length, 'unit': 'm', 'description': 'Screw length'},
                'screw_pitch': {'value': self.screw_pitch, 'unit': 'm', 'description': 'Screw pitch'},
                'screw_speed': {'value': self.screw_speed, 'unit': 'rpm', 'description': 'Screw speed'},
                'fill_factor': {'value': self.fill_factor, 'unit': '-', 'description': 'Screw fill factor'},
                'powder_density': {'value': self.powder_density, 'unit': 'kg/m³', 'description': 'Powder bulk density'},
                'powder_flowability': {'value': self.powder_flowability, 'unit': '-', 'description': 'Powder flowability index'},
                'motor_torque_max': {'value': self.motor_torque_max, 'unit': 'N⋅m', 'description': 'Maximum motor torque'}
            },
            'inputs': {
                'screw_speed_setpoint': {'unit': 'rpm', 'description': 'Screw speed setpoint'},
                'hopper_level': {'unit': 'm', 'description': 'Hopper level'},
                'powder_moisture': {'unit': '-', 'description': 'Powder moisture content'}
            },
            'outputs': {
                'mass_flow_rate': {'unit': 'kg/s', 'description': 'Mass flow rate'},
                'motor_torque': {'unit': 'N⋅m', 'description': 'Motor torque'}
            },
            'equations': [
                'volume_per_revolution = π * (screw_diameter/2)² * screw_pitch',
                'theoretical_volume_flow = (screw_speed / 60) * volume_per_revolution',
                'effective_fill = fill_factor * level_factor * moisture_factor * flowability_factor',
                'mass_flow_rate = actual_volume_flow * powder_density'
            ],
            'working_ranges': {
                'screw_speed': '10-500 rpm',
                'fill_factor': '0.1-0.8',
                'powder_density': '200-2000 kg/m³',
                'powder_flowability': '0.3-1.0'
            },
            'applications': ['Powder feeding', 'Dosing systems', 'Batch weighing', 'Process control'],
            'limitations': ['Uniform powder properties', 'No segregation effects', 'Continuous operation assumption']
        }
