Valve Operations
================

Overview
--------

The valve operations module provides comprehensive models for different valve types used in process control and flow regulation. These models include flow calculations, pressure drop analysis, and control characteristics.

Available Valve Types
---------------------

.. toctree::
   :maxdepth: 2

   control_valve
   three_way_valve
   safety_valve

Control Valve
~~~~~~~~~~~~~

The control valve model provides:

- Flow coefficient (Cv) calculations
- Pressure drop analysis
- Flow characteristics (linear, equal percentage, quick opening)
- Cavitation and flashing analysis
- Valve sizing methods

**Key Features:**

- ISA/IEC standard compliance
- Multi-phase flow calculations
- Noise prediction
- Trim design optimization
- Actuator sizing

Three-Way Valve
~~~~~~~~~~~~~~~

The three-way valve model includes:

- Mixing and diverting configurations
- Flow split calculations
- Pressure balance analysis
- Control characteristics

**Key Features:**

- Flow distribution control
- Temperature mixing applications
- Bypass flow control
- Process switching

Safety Valve
~~~~~~~~~~~~

The safety valve model provides:

- Relief capacity calculations
- Set pressure optimization
- Back pressure effects
- Sizing according to API/ASME standards

**Key Features:**

- Overpressure protection
- Multiple fluid types
- Fire case scenarios
- Thermal relief applications

Applications
------------

Valve models are used for:

- **Flow Control**: Process variable regulation
- **Pressure Control**: System pressure management
- **Safety Systems**: Overpressure protection design
- **Process Control**: Control loop design and tuning
- **Valve Sizing**: Selection and specification

Examples and Tutorials
----------------------

.. toctree::
   :maxdepth: 1

   valve_examples

See Also
--------

* :doc:`../pump/index` - Pump operations
* :doc:`../compressor/index` - Compressor operations
* :doc:`../reactor/index` - Reactor operations
