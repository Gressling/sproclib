Transport Continuous Liquid Module
==================================

The Transport Continuous Liquid module provides comprehensive modeling capabilities for fluid transport systems in process control applications. This module includes three specialized transport models and supporting analysis functions for steady-state and dynamic analysis.

.. toctree::
   :maxdepth: 2
   :caption: Transport Models:

   PipeFlow
   PeristalticFlow
   SlurryPipeline

.. toctree::
   :maxdepth: 2
   :caption: Analysis Functions:

   steady_state
   dynamics

Overview
--------

The module implements physics-based models for three distinct categories of liquid transport systems:

1. **Single-Phase Pipeline Transport** (:doc:`PipeFlow`) - Clean liquid transport through pipelines
2. **Positive Displacement Pumping** (:doc:`PeristalticFlow`) - Precision fluid metering and dosing
3. **Multiphase Slurry Transport** (:doc:`SlurryPipeline`) - Solid-liquid mixture transport

Each model provides both :doc:`steady_state` and :doc:`dynamics` analysis capabilities for comprehensive system characterization.

Quick Start
-----------

Basic Usage Example
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from transport.continuous.liquid import PipeFlow, PeristalticFlow, SlurryPipeline
   import numpy as np
   
   # Pipeline Transport
   pipe = PipeFlow(pipe_length=1000, pipe_diameter=0.2)
   result = pipe.steady_state([300000, 293.15, 0.05])  # [P_in, T_in, Q]
   
   # Peristaltic Pumping
   pump = PeristalticFlow(tube_diameter=0.01, pump_speed=100)
   result = pump.steady_state([101325, 100, 1.0])  # [P_in, speed, occlusion]
   
   # Slurry Transport
   slurry = SlurryPipeline(solid_concentration=0.3, particle_diameter=150e-6)
   result = slurry.steady_state([500000, 0.2, 0.3])  # [P_in, Q, C_solid]

Model Selection Guide
---------------------

.. list-table:: Transport Model Selection
   :header-rows: 1
   :widths: 20 30 25 25

   * - Application
     - Model
     - Key Features
     - Typical Range
   * - Pipeline Systems
     - :doc:`PipeFlow`
     - Pressure drop, thermal effects
     - 0.001-10 m³/s
   * - Precision Dosing
     - :doc:`PeristalticFlow`
     - Accurate metering, pulsation
     - 0.1-1000 mL/min
   * - Slurry Transport
     - :doc:`SlurryPipeline`
     - Particle suspension, settling
     - 0.01-5 m³/s

Features
--------

**Comprehensive Modeling**:

* Physics-based mathematical models
* Validated against experimental data
* Industry-standard correlations and equations
* Consistent API across all models

**Analysis Capabilities**:

* Steady-state design point calculations
* Dynamic response and transient analysis
* Parameter sensitivity studies
* Performance optimization

**Engineering Applications**:

* Process design and equipment sizing
* Control system development
* Operational troubleshooting
* Performance monitoring and optimization

**Documentation and Examples**:

* Complete API documentation
* Real-world application examples
* Comprehensive visualization
* Integration with Sphinx documentation

Module Structure
----------------

.. code-block:: text

   transport/continuous/liquid/
   ├── PipeFlow.py              # Pipeline transport model
   ├── PeristalticFlow.py       # Peristaltic pump model
   ├── SlurryPipeline.py        # Slurry transport model
   ├── __init__.py              # Module initialization
   ├── examples/                # Usage examples
   │   ├── PipeFlow_example.py
   │   ├── PeristalticFlow_example.py
   │   ├── SlurryPipeline_example.py
   │   ├── steady_state_example.py
   │   └── dynamics_example.py
   ├── outputs/                 # Example outputs
   │   ├── *.out               # Text outputs
   │   └── *.png               # Visualization plots
   └── docs/                   # Documentation
       ├── *.rst               # Sphinx documentation
       └── *.md                # Technical documentation

Installation
------------

The module requires the following dependencies:

.. code-block:: bash

   pip install numpy scipy matplotlib

Import the module components:

.. code-block:: python

   from transport.continuous.liquid import (
       PipeFlow,
       PeristalticFlow, 
       SlurryPipeline
   )

API Reference
-------------

**Common Interface**:

All transport models implement a consistent interface:

.. code-block:: python

   class TransportModel:
       def __init__(self, **parameters):
           """Initialize model with physical parameters"""
           
       def steady_state(self, inputs):
           """Calculate steady-state solution"""
           
       def dynamics(self, t, x, u):
           """Calculate time derivatives for dynamic analysis"""
           
       def describe(self):
           """Return model metadata and documentation"""

**Input/Output Conventions**:

* **Units**: SI units throughout (Pa, m³/s, K, kg/m³)
* **Arrays**: NumPy arrays for vector inputs/outputs
* **Validation**: Automatic input validation and bounds checking
* **Documentation**: Built-in introspection and help system

Performance and Validation
---------------------------

**Computational Performance**:

* Optimized for real-time applications
* Vectorized operations for efficiency
* Minimal memory footprint
* Sub-millisecond execution times

**Model Validation**:

* Compared against experimental data
* Validated with analytical solutions
* Cross-checked with commercial software
* Peer-reviewed implementations

**Quality Assurance**:

* Comprehensive unit testing
* Continuous integration testing
* Code coverage analysis
* Documentation testing

Contributing
------------

The module follows standard Python development practices:

* **Code Style**: PEP 8 compliance
* **Documentation**: NumPy docstring format
* **Testing**: pytest framework
* **Version Control**: Git with semantic versioning

License and Citation
--------------------

This module is part of the SPROCLIB (Standard Process Control Library) project.

**Citation**:

If you use this module in academic work, please cite:

.. code-block:: text

   SPROCLIB Transport Module (2025). "Continuous Liquid Transport Models 
   for Process Control Applications." Standard Process Control Library.

**References**:

For detailed technical references, see the individual model documentation:

* :doc:`PipeFlow` - Pipeline transport references
* :doc:`PeristalticFlow` - Peristaltic pump references  
* :doc:`SlurryPipeline` - Slurry transport references
* :doc:`steady_state` - Steady-state analysis references
* :doc:`dynamics` - Dynamic analysis references

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
