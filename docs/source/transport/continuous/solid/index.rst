Continuous Solid Transport
==========================

The Continuous Solid Transport module provides specialized models for bulk solid handling and conveying systems in continuous operation. This module includes four distinct transport mechanisms commonly used in process industries.

.. toctree::
   :maxdepth: 2
   :caption: Solid Transport Models:

   PneumaticConveying
   ConveyorBelt
   GravityChute
   ScrewFeeder

Overview
--------

This module implements physics-based models for four categories of continuous solid transport:

1. **Pneumatic Conveying** (:doc:`PneumaticConveying`) - Gas-phase transport of bulk solids
2. **Mechanical Conveying** (:doc:`ConveyorBelt`) - Belt-based material transport
3. **Gravity Transport** (:doc:`GravityChute`) - Gravity-driven material flow
4. **Screw Feeding** (:doc:`ScrewFeeder`) - Controlled solid feeding and metering

Key Capabilities
----------------

* **Multi-Phase Flow** - Gas-solid and gravity-driven flow analysis
* **Power Optimization** - Energy-efficient transport system design
* **Flow Control** - Precise material flow rate management
* **System Sizing** - Equipment sizing and capacity optimization
* **Safety Integration** - Dust control and material handling safety

Applications
------------

Continuous solid transport is essential for:

* **Chemical Processing** - Powder and granule handling systems
* **Mining & Minerals** - Ore transport and processing operations
* **Power Generation** - Coal, ash, and biomass handling
* **Food Processing** - Grain, flour, and ingredient transport
* **Pharmaceutical** - API and excipient handling systems
* **Manufacturing** - Raw material and product conveying

Quick Start
-----------

Pneumatic Conveying Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from transport.continuous.solid import PneumaticConveying
   
   # Create pneumatic conveying model
   pneumatic = PneumaticConveying(
       pipe_length=200.0,       # 200 m transport line
       pipe_diameter=0.15,      # 15 cm diameter
       particle_diameter=3e-3,  # 3 mm particles
       particle_density=1200.0, # Plastic pellets
       gas_density=1.2,         # Air at standard conditions
       conveying_velocity=15.0  # Initial gas velocity
   )
   
   # Analyze transport performance
   result = pneumatic.steady_state([
       150000,  # Inlet pressure (Pa)
       15.0,    # Gas velocity (m/s)
       0.5      # Solid loading ratio
   ])
   
   outlet_pressure, min_velocity, power_required = result
   
   print(f"Outlet pressure: {outlet_pressure/1000:.1f} kPa")
   print(f"Minimum transport velocity: {min_velocity:.1f} m/s")
   print(f"Power requirement: {power_required:.1f} kW")

Belt Conveyor Operations
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from transport.continuous.solid import ConveyorBelt
   
   # Create belt conveyor model
   belt = ConveyorBelt(
       belt_length=100.0,       # 100 m conveyor length
       belt_width=1.2,          # 1.2 m belt width
       inclination_angle=15.0,  # 15 degree incline
       material_density=800.0,  # Bulk density (kg/m³)
       belt_speed=2.0          # Belt speed (m/s)
   )
   
   # Analyze conveyor performance
   result = belt.steady_state([
       10.0,    # Material capacity (t/h)
       2.0,     # Belt speed (m/s)
       0.8      # Load factor
   ])
   
   belt_tension, motor_power, efficiency = result
   
   print(f"Belt tension: {belt_tension:.0f} N")
   print(f"Motor power: {motor_power:.1f} kW")
   print(f"System efficiency: {efficiency:.2f}")

Gravity Chute Systems
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from transport.continuous.solid import GravityChute
   
   # Create gravity chute model
   chute = GravityChute(
       chute_length=10.0,       # 10 m chute length
       chute_width=0.5,         # 50 cm width
       inclination_angle=45.0,  # 45 degree slope
       material_density=1500.0, # Material bulk density
       friction_coefficient=0.4 # Wall friction
   )
   
   # Analyze material flow
   result = chute.steady_state([
       5.0,     # Feed rate (t/h)
       0.8,     # Fill ratio
       45.0     # Chute angle (degrees)
   ])
   
   discharge_rate, velocity_profile, flow_depth = result
   
   print(f"Discharge rate: {discharge_rate:.1f} t/h")
   print(f"Average velocity: {velocity_profile:.1f} m/s")
   print(f"Flow depth: {flow_depth:.3f} m")

Screw Feeder Control
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from transport.continuous.solid import ScrewFeeder
   
   # Create screw feeder model
   screw = ScrewFeeder(
       screw_diameter=0.2,      # 20 cm diameter
       screw_length=2.0,        # 2 m length
       screw_pitch=0.15,        # 15 cm pitch
       rotation_speed=30.0,     # 30 RPM
       material_density=900.0   # Bulk density
   )
   
   # Analyze feeding performance
   result = screw.steady_state([
       30.0,    # Rotation speed (RPM)
       0.7,     # Fill factor
       1.0      # Efficiency factor
   ])
   
   feed_rate, power_consumption, volumetric_efficiency = result
   
   print(f"Feed rate: {feed_rate:.2f} kg/s")
   print(f"Power consumption: {power_consumption:.1f} kW")
   print(f"Volumetric efficiency: {volumetric_efficiency:.2f}")

Advanced Applications
---------------------

Integrated Solid Handling Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Complex solid handling system with multiple transport mechanisms
   class SolidHandlingSystem:
       def __init__(self):
           # Raw material conveyor
           self.feed_conveyor = ConveyorBelt(
               belt_length=50, belt_width=1.0, inclination_angle=0
           )
           
           # Pneumatic transfer to storage
           self.pneumatic_line = PneumaticConveying(
               pipe_length=150, pipe_diameter=0.12
           )
           
           # Controlled feeding to process
           self.process_feeder = ScrewFeeder(
               screw_diameter=0.15, screw_length=1.5
           )
       
       def system_analysis(self, material_flow, transport_conditions):
           # Analyze complete material flow path
           conveyor_result = self.feed_conveyor.steady_state([
               material_flow, 2.0, 0.85
           ])
           
           pneumatic_result = self.pneumatic_line.steady_state([
               150000, 18.0, 0.4
           ])
           
           feeder_result = self.process_feeder.steady_state([
               25.0, 0.8, 0.95
           ])
           
           return {
               'conveyor_power': conveyor_result[1],
               'pneumatic_power': pneumatic_result[2],
               'feeder_rate': feeder_result[0],
               'total_power': conveyor_result[1] + pneumatic_result[2] + feeder_result[1]
           }

System Optimization
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from optimization.parameter_estimation import optimize_design
   
   def solid_transport_optimization(design_params):
       belt_speed, pneumatic_velocity, screw_speed = design_params
       
       # Create transport models
       belt = ConveyorBelt(belt_length=100, belt_width=1.2)
       pneumatic = PneumaticConveying(pipe_length=200, pipe_diameter=0.15)
       screw = ScrewFeeder(screw_diameter=0.2, screw_length=2.0)
       
       # Analyze performance
       belt_result = belt.steady_state([10.0, belt_speed, 0.8])
       pneumatic_result = pneumatic.steady_state([150000, pneumatic_velocity, 0.5])
       screw_result = screw.steady_state([screw_speed, 0.7, 1.0])
       
       # Objective: minimize total power consumption
       total_power = belt_result[1] + pneumatic_result[2] + screw_result[1]
       
       # Constraint: maintain minimum throughput
       min_throughput = min(belt_result[0], pneumatic_result[0], screw_result[0])
       
       if min_throughput < 8.0:  # Minimum 8 t/h
           return 1e6  # Penalty for infeasible design
       
       return total_power
   
   # Optimize system design
   optimal_design = optimize_design(
       solid_transport_optimization,
       bounds=[(1.0, 3.0), (12.0, 25.0), (20.0, 50.0)],
       constraints={'min_throughput': 8.0}
   )

Material-Specific Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Material database with handling properties
   materials = {
       'coal_powder': {
           'density': 700, 'angle_repose': 40, 'abrasiveness': 'high',
           'dustiness': 'high', 'flowability': 'poor'
       },
       'plastic_pellets': {
           'density': 950, 'angle_repose': 25, 'abrasiveness': 'low',
           'dustiness': 'low', 'flowability': 'excellent'
       },
       'limestone_granules': {
           'density': 1600, 'angle_repose': 35, 'abrasiveness': 'high',
           'dustiness': 'medium', 'flowability': 'good'
       }
   }
   
   def select_transport_method(material_name, flow_rate, distance):
       material = materials[material_name]
       
       # Selection logic based on material properties
       if material['flowability'] == 'excellent' and distance < 100:
           transport_method = 'belt_conveyor'
       elif material['dustiness'] == 'low' and distance > 100:
           transport_method = 'pneumatic'
       elif material['flowability'] == 'poor':
           transport_method = 'screw_feeder'
       else:
           transport_method = 'gravity_chute'
       
       print(f"Recommended transport for {material_name}: {transport_method}")
       return transport_method

Performance Monitoring
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Real-time performance monitoring system
   def monitor_solid_transport_performance(models, operating_data):
       performance_alerts = []
       
       for unit_name, model in models.items():
           expected = model.steady_state(operating_data[unit_name]['inputs'])
           actual = operating_data[unit_name]['outputs']
           
           if unit_name.startswith('pneumatic'):
               # Check for line blockage or wear
               pressure_ratio = actual[0] / expected[0]
               if pressure_ratio < 0.7:
                   performance_alerts.append(f"{unit_name}: Possible line blockage")
               
           elif unit_name.startswith('belt'):
               # Check for belt slippage or wear
               power_ratio = actual[1] / expected[1]
               if power_ratio > 1.3:
                   performance_alerts.append(f"{unit_name}: Excessive power consumption")
               
           elif unit_name.startswith('screw'):
               # Check for feeder accuracy
               rate_ratio = actual[0] / expected[0]
               if abs(1.0 - rate_ratio) > 0.1:
                   performance_alerts.append(f"{unit_name}: Feed rate deviation")
       
       return performance_alerts

See Also
--------

* :doc:`../liquid/index` - Continuous liquid transport
* :doc:`../../batch/solid/index` - Batch solid transport
* :doc:`../../../user_guide/examples/transport_examples` - Usage examples
