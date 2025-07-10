Batch Transport Module
=====================

The Transport Batch module provides modeling capabilities for discrete material transfer operations in process control applications. This module includes specialized models for both liquid and solid batch transport operations with supporting analysis functions.

.. toctree::
   :maxdepth: 2
   :caption: Batch Transport Operations:

   liquid/index
   solid/index

Overview
--------

The module implements physics-based models for two distinct categories of batch transport systems:

1. **Batch Liquid Transport** (:doc:`liquid/index`) - Discrete liquid transfer operations
2. **Batch Solid Transport** (:doc:`solid/index`) - Discrete solid material handling

Each model provides both steady-state and dynamic analysis capabilities for comprehensive batch operation characterization.

Features
--------

* **Discrete Volume Control** - Precise batch size management and control
* **Transfer Time Optimization** - Minimize cycle times while maintaining accuracy
* **Equipment Sizing** - Proper pump, container, and system component sizing
* **Safety Integration** - Built-in safety considerations for batch operations
* **Quality Assurance** - Contamination prevention and batch integrity

Batch transport operations are essential in:

* **Chemical Processing** - Batch reactors and mixing operations
* **Pharmaceutical Manufacturing** - GMP-compliant material transfer
* **Food & Beverage** - Sanitary batch processing
* **Laboratory Operations** - Precise sample and reagent handling
* **Water Treatment** - Chemical dosing and batch treatment

Quick Start
-----------

Basic Batch Liquid Transfer
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from transport.batch.liquid import BatchTransferPumping
   
   # Create batch transfer system
   transfer = BatchTransferPumping(
       tank_volume=2.0,         # 2 m³ source tank
       transfer_volume=0.5,     # 500 L batch size
       pump_capacity=0.01,      # 10 L/s pump
       pipe_length=50.0         # 50 m transfer line
   )
   
   # Analyze batch operation
   result = transfer.steady_state([0.5, 101325, 293.15])
   transfer_time, accuracy, residual = result

See Also
--------

* :doc:`../continuous/index` - Continuous transport operations
* :doc:`../../api/transport_package` - Complete API reference
* :doc:`../../user_guide/examples/transport_examples` - Usage examples
