Batch Liquid Transport
======================

The Batch Liquid Transport module provides specialized models for discrete liquid transfer operations commonly used in batch processing applications.

.. toctree::
   :maxdepth: 2
   :caption: Batch Liquid Models:

   BatchTransferPumping

Overview
--------

This module implements physics-based models for batch liquid transfer systems focusing on:

1. **Pump-Based Transfer** (:doc:`BatchTransferPumping`) - Controlled liquid transfer using pumps

Key Capabilities
----------------

* **Volume Control** - Precise batch volume measurement and control
* **Transfer Time Prediction** - Accurate cycle time estimation
* **Pump Performance** - Integration of pump curves and efficiency factors
* **System Hydraulics** - Complete hydraulic analysis including friction losses
* **Level Control** - Tank level monitoring and control integration

Applications
------------

Batch liquid transfer is essential for:

* **Chemical Batch Processing** - Reactor charging and product transfer
* **Pharmaceutical Manufacturing** - GMP-compliant material handling
* **Food Processing** - Sanitary batch operations
* **Laboratory Systems** - Precise sample and reagent transfer

Quick Start
-----------

Basic Batch Transfer Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from transport.batch.liquid import BatchTransferPumping
   
   # Create batch transfer model
   transfer = BatchTransferPumping(
       tank_volume=2.0,         # Source tank capacity (m³)
       transfer_volume=0.5,     # Target batch size (m³)
       pump_capacity=0.01,      # Pump flow rate (m³/s)
       pipe_length=50.0,        # Transfer line length (m)
       pipe_diameter=0.05,      # Transfer line diameter (m)
       static_head=5.0          # Elevation difference (m)
   )
   
   # Perform steady-state analysis
   result = transfer.steady_state([
       0.5,      # Transfer volume (m³)
       101325,   # System pressure (Pa)
       293.15    # Fluid temperature (K)
   ])
   
   transfer_time, accuracy, residual_volume = result
   
   print(f"Transfer time: {transfer_time:.1f} seconds")
   print(f"Volume accuracy: {accuracy:.3f}%")
   print(f"Residual volume: {residual_volume:.4f} m³")

Advanced Operations
~~~~~~~~~~~~~~~~~~~

Dynamic Transfer Analysis::

   # Run dynamic simulation
   time_span = (0, 300)  # 5 minute simulation
   dynamic_result = transfer.dynamics(
       y0=[2.0, 0.0],  # Initial conditions [source_level, transferred_volume]
       t_span=time_span,
       inputs=[0.5, 101325, 293.15]
   )
   
   time, states = dynamic_result
   source_level = states[:, 0]
   transferred_volume = states[:, 1]

Multi-Batch Operations::

   # Sequential batch transfers
   batch_volumes = [0.5, 0.3, 0.7]  # Multiple batch sizes
   results = []
   
   for volume in batch_volumes:
       result = transfer.steady_state([volume, 101325, 293.15])
       results.append(result)
       print(f"Batch {volume} m³: {result[0]:.1f} seconds")

See Also
--------

* :doc:`../solid/index` - Batch solid transport
* :doc:`../../continuous/liquid/index` - Continuous liquid transport
* :doc:`../../../user_guide/examples/transport_examples` - Complete examples
