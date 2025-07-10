Batch Solid Transport
=====================

The Batch Solid Transport module provides specialized models for discrete solid material handling operations commonly used in batch processing and discrete manufacturing applications.

.. toctree::
   :maxdepth: 2
   :caption: Batch Solid Models:

   DrumBinTransfer
   VacuumTransfer

Overview
--------

This module implements physics-based models for batch solid transfer systems focusing on:

1. **Container-Based Transfer** (:doc:`DrumBinTransfer`) - Drum and bin discharge operations
2. **Pneumatic Transfer** (:doc:`VacuumTransfer`) - Vacuum-based solid transport

Key Capabilities
----------------

* **Flow Rate Control** - Precise discharge rate modeling and control
* **Material Handling** - Comprehensive bulk solid flow characterization
* **Container Design** - Optimal hopper and discharge system design
* **Safety Integration** - Dust control and containment considerations
* **Batch Accuracy** - Precise material quantity control

Applications
------------

Batch solid transport is essential for:

* **Chemical Processing** - Powder and granule handling
* **Pharmaceutical Manufacturing** - API and excipient transfer
* **Food Processing** - Ingredient batching and mixing
* **Mining & Minerals** - Ore and concentrate handling
* **Manufacturing** - Raw material and component transfer

Quick Start
-----------

Drum/Bin Transfer Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from transport.batch.solid import DrumBinTransfer
   
   # Create drum transfer model
   drum_transfer = DrumBinTransfer(
       drum_capacity=0.2,       # 200 L drum capacity
       discharge_diameter=0.1,  # 10 cm outlet diameter
       material_density=1200.0, # Bulk density (kg/m³)
       angle_of_repose=35.0,    # Material flow property (degrees)
       discharge_coefficient=0.6 # Orifice discharge coefficient
   )
   
   # Analyze discharge operation
   result = drum_transfer.steady_state([
       0.15,     # Fill level (fraction)
       0.8,      # Valve opening (fraction)
       9.81      # Gravitational acceleration (m/s²)
   ])
   
   discharge_rate, empty_time, flow_pattern = result
   
   print(f"Discharge rate: {discharge_rate:.3f} kg/s")
   print(f"Empty time: {empty_time:.1f} seconds")

Vacuum Transfer Systems
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from transport.batch.solid import VacuumTransfer
   
   # Create vacuum transfer model
   vacuum_transfer = VacuumTransfer(
       transfer_line_length=20.0,   # 20 m transfer distance
       transfer_line_diameter=0.08, # 8 cm transfer line
       material_density=800.0,      # Bulk density (kg/m³)
       particle_size=2e-3,          # 2 mm average particle size
       vacuum_pump_capacity=50.0    # 50 m³/h vacuum pump
   )
   
   # Analyze vacuum transfer
   result = vacuum_transfer.steady_state([
       10.0,     # Transfer quantity (kg)
       -80000,   # Vacuum pressure (Pa, negative gauge)
       0.3       # Material pickup efficiency
   ])
   
   transfer_time, pickup_rate, energy_consumption = result
   
   print(f"Transfer time: {transfer_time:.1f} seconds")
   print(f"Pickup rate: {pickup_rate:.2f} kg/s")
   print(f"Energy consumption: {energy_consumption:.1f} kW")

Advanced Operations
~~~~~~~~~~~~~~~~~~~

Multi-Container Systems::

   # Sequential container discharge
   containers = [
       {'capacity': 0.2, 'fill_level': 0.8},
       {'capacity': 0.15, 'fill_level': 0.9},
       {'capacity': 0.25, 'fill_level': 0.7}
   ]
   
   total_discharge_time = 0
   for container in containers:
       result = drum_transfer.steady_state([
           container['fill_level'], 0.8, 9.81
       ])
       total_discharge_time += result[1]
   
   print(f"Total operation time: {total_discharge_time:.1f} seconds")

Integrated Vacuum Systems::

   # Vacuum transfer with filtration
   from utilities.process_utils import filter_efficiency
   
   # Calculate filter loading
   material_loading = 10.0 * 0.01  # 1% dust content
   filter_area = 2.0  # m² filter area
   
   # Adjust vacuum system performance
   efficiency = filter_efficiency(material_loading, filter_area)
   adjusted_result = vacuum_transfer.steady_state([
       10.0, -80000 * efficiency, 0.3
   ])

See Also
--------

* :doc:`../liquid/index` - Batch liquid transport
* :doc:`../../continuous/solid/index` - Continuous solid transport
* :doc:`../../../user_guide/examples/transport_examples` - Complete examples
