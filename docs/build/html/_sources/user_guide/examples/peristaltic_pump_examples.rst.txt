Peristaltic Pump Examples
==========================

This section provides practical examples of peristaltic pump modeling and control using the transport module.

Overview
--------

Peristaltic pumps are widely used in chemical processes for their:

- Self-priming capabilities
- Gentle fluid handling
- Contamination-free operation
- Precise flow control

These examples demonstrate modeling and optimization techniques for peristaltic pump systems.

Basic Peristaltic Pump Operation
---------------------------------

Example 1: Basic Pump Modeling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from transport.continuous.liquid import PeristalticFlow
    import numpy as np
    
    # Create a peristaltic pump model
    pump = PeristalticFlow(
        tube_diameter=0.008,  # 8 mm tube
        roller_diameter=0.05,  # 5 cm roller
        number_of_rollers=6,
        tube_material='silicone'
    )
    
    # Set operating conditions
    pump.set_operating_conditions(
        rotation_speed=100,  # RPM
        fluid_viscosity=0.001,  # Pa·s
        fluid_density=1000  # kg/m³
    )
    
    # Calculate theoretical flow rate
    theoretical_flow = pump.calculate_theoretical_flow()
    actual_flow = pump.calculate_actual_flow()
    efficiency = actual_flow / theoretical_flow * 100
    
    print(f"Theoretical flow rate: {theoretical_flow:.6f} m³/s")
    print(f"Actual flow rate: {actual_flow:.6f} m³/s")
    print(f"Volumetric efficiency: {efficiency:.1f}%")

Example 2: Speed Control and Flow Rate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import matplotlib.pyplot as plt
    
    # Analyze flow rate vs pump speed
    speeds = np.linspace(10, 200, 50)  # RPM
    flow_rates = []
    
    for speed in speeds:
        pump.set_operating_conditions(rotation_speed=speed)
        flow_rates.append(pump.calculate_actual_flow())
    
    # Plot speed vs flow rate relationship
    plt.figure(figsize=(10, 6))
    plt.plot(speeds, np.array(flow_rates) * 1e6)  # Convert to mL/min
    plt.xlabel('Pump Speed (RPM)')
    plt.ylabel('Flow Rate (mL/min)')
    plt.title('Peristaltic Pump Speed vs Flow Rate')
    plt.grid(True)
    plt.show()

Advanced Pump Control
---------------------

Example 3: PID Flow Control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from controller.pid import PIDController
    import numpy as np
    
    class PeristalticPumpController:
        def __init__(self, pump, target_flow):
            self.pump = pump
            self.target_flow = target_flow
            self.pid = PIDController(kp=100, ki=10, kd=1)
            self.current_speed = 100  # Initial speed
        
        def update_control(self, measured_flow, dt):
            error = self.target_flow - measured_flow
            speed_adjustment = self.pid.update(error, dt)
            
            # Update pump speed (with limits)
            self.current_speed = np.clip(
                self.current_speed + speed_adjustment, 
                10, 300
            )
            
            self.pump.set_operating_conditions(rotation_speed=self.current_speed)
            return self.current_speed
    
    # Simulation example
    controller = PeristalticPumpController(pump, target_flow=5e-6)  # 5 mL/min
    
    # Simulate control response
    time_steps = np.linspace(0, 60, 600)  # 60 seconds
    measured_flows = []
    pump_speeds = []
    
    for i, t in enumerate(time_steps):
        if i == 0:
            measured_flow = pump.calculate_actual_flow()
        else:
            dt = time_steps[i] - time_steps[i-1]
            speed = controller.update_control(measured_flow, dt)
            measured_flow = pump.calculate_actual_flow()
            pump_speeds.append(speed)
        
        measured_flows.append(measured_flow)
    
    # Plot control response
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    ax1.plot(time_steps, np.array(measured_flows) * 1e6)
    ax1.axhline(y=controller.target_flow * 1e6, color='r', linestyle='--', label='Setpoint')
    ax1.set_ylabel('Flow Rate (mL/min)')
    ax1.set_title('PID Flow Control Response')
    ax1.grid(True)
    ax1.legend()
    
    ax2.plot(time_steps[1:], pump_speeds)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Pump Speed (RPM)')
    ax2.set_title('Pump Speed Response')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

Example 4: Multi-Pump System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class MultiPumpSystem:
        def __init__(self, num_pumps=3):
            self.pumps = []
            for i in range(num_pumps):
                pump = PeristalticFlow(
                    tube_diameter=0.008,
                    roller_diameter=0.05,
                    number_of_rollers=6
                )
                self.pumps.append(pump)
        
        def set_flow_rates(self, flow_rates):
            """Set individual flow rates for each pump"""
            for pump, flow_rate in zip(self.pumps, flow_rates):
                # Calculate required speed for target flow rate
                required_speed = self.calculate_required_speed(pump, flow_rate)
                pump.set_operating_conditions(rotation_speed=required_speed)
        
        def calculate_required_speed(self, pump, target_flow):
            """Calculate required speed for target flow rate"""
            # Simplified calculation (would need iterative solution in practice)
            base_speed = 100
            pump.set_operating_conditions(rotation_speed=base_speed)
            base_flow = pump.calculate_actual_flow()
            
            if base_flow > 0:
                required_speed = base_speed * (target_flow / base_flow)
                return np.clip(required_speed, 10, 300)
            return base_speed
        
        def get_total_flow(self):
            """Calculate total system flow rate"""
            return sum(pump.calculate_actual_flow() for pump in self.pumps)
    
    # Example usage
    system = MultiPumpSystem(num_pumps=3)
    target_flows = [3e-6, 4e-6, 5e-6]  # mL/min for each pump
    system.set_flow_rates(target_flows)
    
    total_flow = system.get_total_flow()
    print(f"Total system flow rate: {total_flow * 1e6:.2f} mL/min")

Pump Maintenance and Optimization
----------------------------------

Example 5: Tube Wear Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class TubeWearModel:
        def __init__(self, initial_diameter, wear_rate=1e-9):
            self.initial_diameter = initial_diameter
            self.wear_rate = wear_rate  # m per cycle
            self.cycles = 0
        
        def update_wear(self, pump_speed, duration):
            """Update tube wear based on pump operation"""
            cycles_per_second = pump_speed / 60
            new_cycles = cycles_per_second * duration
            self.cycles += new_cycles
            
            # Calculate current diameter
            wear_depth = self.wear_rate * self.cycles
            current_diameter = self.initial_diameter - 2 * wear_depth
            return max(current_diameter, self.initial_diameter * 0.7)  # Minimum diameter
        
        def predict_lifetime(self, pump_speed, failure_diameter=None):
            """Predict tube lifetime at given operating conditions"""
            if failure_diameter is None:
                failure_diameter = self.initial_diameter * 0.7
            
            max_wear_depth = (self.initial_diameter - failure_diameter) / 2
            max_cycles = max_wear_depth / self.wear_rate
            
            cycles_per_hour = pump_speed * 60
            lifetime_hours = max_cycles / cycles_per_hour
            
            return lifetime_hours
    
    # Example tube wear analysis
    wear_model = TubeWearModel(initial_diameter=0.008)
    
    speeds = [50, 100, 150, 200]
    lifetimes = [wear_model.predict_lifetime(speed) for speed in speeds]
    
    plt.figure(figsize=(10, 6))
    plt.plot(speeds, lifetimes)
    plt.xlabel('Pump Speed (RPM)')
    plt.ylabel('Predicted Tube Lifetime (hours)')
    plt.title('Tube Lifetime vs Operating Speed')
    plt.grid(True)
    plt.show()

Troubleshooting
---------------

Common Issues and Solutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Flow Rate Variations**
   - Check tube compression and wear
   - Verify roller alignment
   - Inspect tube for cracks or deformation

2. **Pulsation Issues**
   - Increase number of rollers
   - Use pulsation dampeners
   - Optimize roller timing

3. **Pump Efficiency Loss**
   - Replace worn tubing
   - Check for air leaks
   - Verify proper tube installation

Performance Optimization Tips
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Regular tube replacement schedules
- Proper tube material selection
- Optimal speed ranges for efficiency
- System pressure considerations

See Also
--------

- :doc:`pipeline_flow_examples`
- :doc:`slurry_transport_examples`
- :doc:`../pump_systems`
- :doc:`../../api/transport_package`
