Transport Systems
================

The transport systems documentation covers fluid transport, pipeline modeling, and multiphase flow components in SPROCLIB.

.. toctree::
   :maxdepth: 2

   transport_overview
   pipeline_systems
   pump_systems
   flow_control
   multiphase_transport
   transport_examples

Overview
--------

The transport package provides comprehensive tools for modeling and analyzing fluid transport systems in chemical processes. This includes:

* **Pipeline Systems**: Pressure drop calculations, network analysis, and flow distribution
* **Pump Systems**: Centrifugal and positive displacement pump modeling
* **Flow Control**: Valve characteristics, control strategies, and flow regulation
* **Multiphase Transport**: Gas-liquid, liquid-liquid, and solid-liquid transport phenomena

Key Features
------------

**Pipeline Modeling**
  * Pressure drop calculations for various pipe configurations
  * Network analysis for complex piping systems
  * Flow distribution and balancing

**Pump Characteristics**
  * Centrifugal pump performance curves
  * NPSH calculations and cavitation analysis
  * Variable speed drive optimization

**Flow Control Systems**
  * Control valve sizing and characteristics
  * Flow control loop design
  * Pressure regulation strategies

**Multiphase Flow**
  * Two-phase flow correlations
  * Phase separation equipment
  * Slurry transport calculations

Applications
------------

* Process plant hydraulic design
* Pipeline network optimization
* Pump selection and sizing
* Flow control system design
* Multiphase transport analysis

Getting Started
---------------

For basic transport system modeling::

    from sproclib.transport import Pipeline, CentrifugalPump, ControlValve
    
    # Create pipeline system
    pipeline = Pipeline(diameter=0.1, length=100, roughness=0.045e-3)
    
    # Add pump
    pump = CentrifugalPump(H0=50.0, eta=0.75)
    
    # Calculate pressure drop
    pressure_drop = pipeline.calculate_pressure_drop(flow_rate=0.05)

See Also
--------

* :doc:`../api/transport_package` - Complete API reference
* :doc:`../unit/index` - Unit operations that work with transport systems
* :doc:`../plant/index` - Plant-level integration examples
