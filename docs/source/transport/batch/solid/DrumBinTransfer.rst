DrumBinTransfer
===============

.. currentmodule:: transport.batch.solid

.. autoclass:: DrumBinTransfer
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The ``DrumBinTransfer`` class models batch solid transfer operations involving discharge from drums, bins, hoppers, and similar containers. This model incorporates gravity flow principles, orifice discharge equations, and bulk solid flow characteristics to predict discharge rates and emptying times.

Use Cases
---------

Drum and bin transfer operations are commonly used in:

* Chemical processing plants for powder handling
* Pharmaceutical manufacturing for API transfer
* Food processing for ingredient batching
* Mining operations for ore and concentrate handling
* Manufacturing for raw material dispensing

The model helps predict discharge behavior, optimize container design, and ensure proper material flow for batch operations.

Algorithm Description
---------------------

The model implements comprehensive solid discharge calculations:

Steady-State Algorithm
~~~~~~~~~~~~~~~~~~~~~~

1. **Gravitational Flow Analysis**: Uses Beverloo equation for granular flow through orifices
2. **Material Property Integration**: Incorporates angle of repose and flow function
3. **Discharge Rate Calculation**: Determines instantaneous discharge rate based on fill level
4. **Flow Pattern Assessment**: Evaluates mass flow vs. funnel flow conditions
5. **Emptying Time Prediction**: Integrates discharge rate over time for complete emptying

Dynamic Algorithm
~~~~~~~~~~~~~~~~~

1. **Level Tracking**: Models container level changes during discharge
2. **Flow Rate Evolution**: Accounts for decreasing head pressure effects
3. **Flow Interruption**: Handles bridging and rat-holing phenomena
4. **System Response**: Models valve opening/closing dynamics

Key Parameters
--------------

**Container Geometry**:
- Container capacity (m³)
- Discharge diameter (m)
- Container shape factor
- Wall friction angle (degrees)

**Material Properties**:
- Bulk density (kg/m³)
- Angle of repose (degrees)
- Cohesion factor
- Particle size distribution

**Operating Conditions**:
- Fill level (fraction)
- Valve opening (fraction)
- Environmental conditions
- Vibration/agitation effects

Example Usage
-------------

Basic Discharge Analysis
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from transport.batch.solid import DrumBinTransfer
   import numpy as np
   
   # Create drum transfer model
   drum = DrumBinTransfer(
       drum_capacity=0.2,           # 200 L drum
       discharge_diameter=0.1,      # 10 cm outlet
       material_density=1200.0,     # kg/m³ bulk density
       angle_of_repose=35.0,        # degrees
       discharge_coefficient=0.6    # orifice coefficient
   )
   
   # Steady-state analysis
   result = drum.steady_state([
       0.8,      # 80% fill level
       1.0,      # Fully open valve
       9.81      # Standard gravity
   ])
   
   discharge_rate, empty_time, flow_pattern = result
   
   print(f"Discharge rate: {discharge_rate:.3f} kg/s")
   print(f"Time to empty: {empty_time:.1f} seconds")
   print(f"Flow pattern: {flow_pattern}")

Dynamic Discharge Simulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Dynamic simulation of discharge process
   time_span = (0, empty_time)
   initial_conditions = [0.8, 0.0]  # [fill_level, discharged_mass]
   
   dynamic_result = drum.dynamics(
       y0=initial_conditions,
       t_span=time_span,
       inputs=[1.0, 9.81]  # [valve_opening, gravity]
   )
   
   time, states = dynamic_result
   fill_level = states[:, 0]
   discharged_mass = states[:, 1]
   
   # Plot discharge behavior
   import matplotlib.pyplot as plt
   
   plt.figure(figsize=(12, 4))
   
   plt.subplot(1, 2, 1)
   plt.plot(time, fill_level)
   plt.xlabel('Time (s)')
   plt.ylabel('Fill Level (fraction)')
   plt.title('Container Fill Level')
   plt.grid(True)
   
   plt.subplot(1, 2, 2)
   plt.plot(time, discharged_mass)
   plt.xlabel('Time (s)')
   plt.ylabel('Discharged Mass (kg)')
   plt.title('Cumulative Discharge')
   plt.grid(True)
   
   plt.tight_layout()
   plt.show()

Multi-Container Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Sequential discharge from multiple containers
   containers = [
       {'capacity': 0.2, 'fill': 0.8, 'material': 'powder_a'},
       {'capacity': 0.15, 'fill': 0.9, 'material': 'powder_b'},
       {'capacity': 0.25, 'fill': 0.7, 'material': 'granules'}
   ]
   
   # Material-specific properties
   material_properties = {
       'powder_a': {'density': 1200, 'angle': 35, 'coeff': 0.6},
       'powder_b': {'density': 800, 'angle': 40, 'coeff': 0.55},
       'granules': {'density': 1500, 'angle': 30, 'coeff': 0.65}
   }
   
   total_time = 0
   total_mass = 0
   
   for container in containers:
       material = container['material']
       props = material_properties[material]
       
       # Create specific drum model
       drum = DrumBinTransfer(
           drum_capacity=container['capacity'],
           discharge_diameter=0.08,  # Smaller outlet for powder
           material_density=props['density'],
           angle_of_repose=props['angle'],
           discharge_coefficient=props['coeff']
       )
       
       # Analyze discharge
       result = drum.steady_state([container['fill'], 1.0, 9.81])
       discharge_rate, empty_time, flow_pattern = result
       
       mass_discharged = container['capacity'] * container['fill'] * props['density']
       total_time += empty_time
       total_mass += mass_discharged
       
       print(f"{material}: {mass_discharged:.1f} kg in {empty_time:.1f} s")
   
   print(f"Total operation: {total_mass:.1f} kg in {total_time:.1f} s")

Design Optimization
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Optimize discharge outlet size
   from optimization.parameter_estimation import minimize_scalar
   
   def discharge_time_objective(outlet_diameter):
       drum = DrumBinTransfer(
           drum_capacity=0.2,
           discharge_diameter=outlet_diameter,
           material_density=1200.0,
           angle_of_repose=35.0
       )
       
       result = drum.steady_state([0.8, 1.0, 9.81])
       return result[1]  # empty_time
   
   # Find optimal outlet diameter (minimize emptying time)
   optimal_diameter = minimize_scalar(
       discharge_time_objective,
       bounds=(0.05, 0.2),  # 5-20 cm diameter range
       constraints={'min_discharge_rate': 0.01}  # Minimum 10 g/s
   )
   
   print(f"Optimal outlet diameter: {optimal_diameter:.3f} m")

Troubleshooting Common Issues
-----------------------------

**Flow Problems**:

.. code-block:: python

   # Detect flow issues
   result = drum.steady_state([0.5, 1.0, 9.81])
   discharge_rate, empty_time, flow_pattern = result
   
   if discharge_rate < 0.001:  # Very low discharge rate
       print("Warning: Potential bridging or rat-holing")
       print("Consider:")
       print("- Increasing outlet diameter")
       print("- Adding flow aids or vibration")
       print("- Checking material moisture content")
   
   if flow_pattern == 'funnel_flow':
       print("Funnel flow detected - may cause segregation")
       print("Consider mass flow hopper design")

**Material Property Sensitivity**:

.. code-block:: python

   # Analyze sensitivity to material properties
   import numpy as np
   
   base_angle = 35.0
   angle_range = np.linspace(25, 45, 21)
   empty_times = []
   
   for angle in angle_range:
       drum = DrumBinTransfer(
           drum_capacity=0.2,
           discharge_diameter=0.1,
           material_density=1200.0,
           angle_of_repose=angle
       )
       
       result = drum.steady_state([0.8, 1.0, 9.81])
       empty_times.append(result[1])
   
   # Plot sensitivity
   plt.figure(figsize=(8, 6))
   plt.plot(angle_range, empty_times, 'b-', linewidth=2)
   plt.axvline(base_angle, color='r', linestyle='--', label='Design value')
   plt.xlabel('Angle of Repose (degrees)')
   plt.ylabel('Emptying Time (s)')
   plt.title('Sensitivity to Material Flow Properties')
   plt.grid(True)
   plt.legend()
   plt.show()

See Also
--------

* :doc:`VacuumTransfer` - Pneumatic solid transfer
* :doc:`../liquid/BatchTransferPumping` - Batch liquid transfer
* :doc:`../../continuous/solid/index` - Continuous solid transport
