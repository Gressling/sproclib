"""
Conveyor Belt class for SPROCLIB - Standard Process Control Library

This module contains the conveyor belt transport model (steady-state and dynamic).
"""

import numpy as np
from .....unit.base import ProcessModel


class ConveyorBelt(ProcessModel):
    """Conveyor belt transport model for granular materials (steady-state and dynamic)."""
    
    def __init__(
        self,
        belt_length: float = 50.0,      # Belt length [m]
        belt_width: float = 1.0,        # Belt width [m]
        belt_speed: float = 1.0,        # Belt speed [m/s]
        belt_angle: float = 0.0,        # Belt inclination angle [rad]
        material_density: float = 1500.0, # Bulk material density [kg/m³]
        friction_coefficient: float = 0.6, # Material-belt friction coefficient [-]
        belt_load_factor: float = 0.8,  # Belt loading factor (0-1) [-]
        motor_power: float = 10000.0,   # Motor power [W]
        name: str = "ConveyorBelt"
    ):
        super().__init__(name)
        self.belt_length = belt_length
        self.belt_width = belt_width
        self.belt_speed = belt_speed
        self.belt_angle = belt_angle
        self.material_density = material_density
        self.friction_coefficient = friction_coefficient
        self.belt_load_factor = belt_load_factor
        self.motor_power = motor_power
        self.parameters = {
            'belt_length': belt_length, 'belt_width': belt_width, 'belt_speed': belt_speed,
            'belt_angle': belt_angle, 'material_density': material_density,
            'friction_coefficient': friction_coefficient, 'belt_load_factor': belt_load_factor,
            'motor_power': motor_power
        }

    def steady_state(self, u: np.ndarray) -> np.ndarray:
        """
        Calculate steady-state material flow rate and power consumption.
        Args:
            u: [feed_rate, belt_speed_setpoint, material_load_height]
        Returns:
            [material_flow_rate, power_consumption]
        """
        feed_rate, belt_speed, load_height = u
        
        # Material flow rate calculation
        # Cross-sectional area of material on belt
        material_area = self.belt_width * load_height * self.belt_load_factor
        theoretical_flow = material_area * belt_speed * self.material_density
        
        # Actual flow limited by feed rate
        actual_flow = min(theoretical_flow, feed_rate)
        
        # Power consumption calculation
        # Material transport power
        g = 9.81  # m/s²
        material_weight = actual_flow * g / belt_speed  # N/m
        
        # Power components
        horizontal_power = material_weight * belt_speed * 0.02  # Rolling resistance
        vertical_power = material_weight * belt_speed * np.sin(self.belt_angle)  # Lifting power
        belt_friction_power = 0.1 * self.motor_power  # Belt friction (constant)
        
        total_power = horizontal_power + vertical_power + belt_friction_power
        
        # Power limit check
        if total_power > self.motor_power:
            # Reduce speed if power exceeded
            available_transport_power = self.motor_power - belt_friction_power
            max_material_power = available_transport_power - vertical_power
            if max_material_power > 0:
                max_speed = max_material_power / (material_weight * 0.02)
                belt_speed = min(belt_speed, max_speed)
                actual_flow = material_area * belt_speed * self.material_density
                total_power = self.motor_power
        
        return np.array([actual_flow, total_power])

    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        Dynamic model: material flow and power response.
        State: [material_flow_rate, power_consumption]
        Input: [feed_rate, belt_speed_setpoint, material_load_height]
        """
        flow_rate, power = x
        flow_ss, power_ss = self.steady_state(u)
        
        # Flow rate dynamics (transport delay)
        transport_time = self.belt_length / u[1]  # Belt speed
        tau_flow = transport_time + 5.0  # s, additional settling time
        
        # Power response (motor dynamics)
        tau_power = 2.0  # s, motor response time constant
        
        dflow_dt = (flow_ss - flow_rate) / tau_flow
        dpower_dt = (power_ss - power) / tau_power
        
        return np.array([dflow_dt, dpower_dt])

    def describe(self) -> dict:
        """
        Introspect metadata for documentation and algorithm querying.
        
        Returns:
            dict: Metadata about the ConveyorBelt model including
                  algorithms, parameters, equations, and usage information.
        """
        return {
            'class_name': 'ConveyorBelt',
            'algorithm': 'Conveyor belt transport model using material flow rate and power calculations',
            'parameters': {
                'belt_length': {'value': self.belt_length, 'unit': 'm', 'description': 'Belt length'},
                'belt_width': {'value': self.belt_width, 'unit': 'm', 'description': 'Belt width'},
                'belt_speed': {'value': self.belt_speed, 'unit': 'm/s', 'description': 'Belt speed'},
                'belt_angle': {'value': self.belt_angle, 'unit': 'rad', 'description': 'Belt inclination angle'},
                'material_density': {'value': self.material_density, 'unit': 'kg/m³', 'description': 'Bulk material density'},
                'friction_coefficient': {'value': self.friction_coefficient, 'unit': '-', 'description': 'Material-belt friction coefficient'},
                'belt_load_factor': {'value': self.belt_load_factor, 'unit': '-', 'description': 'Belt loading factor (0-1)'},
                'motor_power': {'value': self.motor_power, 'unit': 'W', 'description': 'Motor power'}
            },
            'inputs': {
                'feed_rate': {'unit': 'kg/s', 'description': 'Material feed rate'},
                'belt_speed_setpoint': {'unit': 'm/s', 'description': 'Belt speed setpoint'},
                'material_load_height': {'unit': 'm', 'description': 'Material load height on belt'}
            },
            'outputs': {
                'material_flow_rate': {'unit': 'kg/s', 'description': 'Actual material flow rate'},
                'power_consumption': {'unit': 'W', 'description': 'Motor power consumption'}
            },
            'equations': [
                'material_area = belt_width * load_height * belt_load_factor',
                'theoretical_flow = material_area * belt_speed * material_density',
                'horizontal_power = material_weight * belt_speed * 0.02',
                'vertical_power = material_weight * belt_speed * sin(belt_angle)'
            ],
            'working_ranges': {
                'belt_speed': '0.1-5.0 m/s',
                'belt_angle': '0-0.52 rad (0-30°)',
                'material_density': '500-3000 kg/m³',
                'belt_load_factor': '0.3-1.0'
            },
            'applications': ['Bulk material transport', 'Mining operations', 'Material handling systems'],
            'limitations': ['Steady flow assumption', 'Uniform material distribution', 'No spillage consideration']
        }
