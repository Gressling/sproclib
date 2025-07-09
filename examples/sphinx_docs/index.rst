
SPROCLIB Examples Documentation
===============================

This section contains comprehensive examples demonstrating the usage of all SPROCLIB units.
Each example includes both simple introductory cases and comprehensive advanced analysis.

The examples are organized by unit type and demonstrate real engineering calculations
with educational explanations.

.. toctree::
    :maxdepth: 2
    :caption: Example Categories:

    complete_process_examples
    compressor_examples
    distillation_examples
    heat_exchanger_examples
    pump_examples
    reactor_examples
    tank_examples
    utilities_examples
    valve_examples


Overview
--------

Each example demonstrates:

* **Simple Examples**: Basic operations for quick learning
* **Comprehensive Examples**: Advanced analysis and calculations  
* **Real Engineering Data**: Realistic parameters and calculations
* **Educational Content**: Clear explanations and engineering insights

Refactored Architecture
-----------------------

These examples showcase the refactored SPROCLIB architecture where:

* Each unit class is in its own dedicated file
* Better discoverability through class-named files
* Improved maintainability and modularity
* Clear import structure and dependencies
* Backward compatibility maintained

Example Categories
------------------

Pump Examples
    Demonstrates CentrifugalPump and PositiveDisplacementPump operations,
    performance analysis, and system curves.

Compressor Examples  
    Shows compressor performance, multi-stage compression analysis,
    and energy optimization.

Valve Examples
    Covers ControlValve and ThreeWayValve operations, flow characteristics,
    and sizing calculations.

Tank Examples
    Illustrates tank systems, level control, interacting tanks,
    and mixing analysis.

Reactor Examples
    Comprehensive reactor analysis including CSTR, PFR, batch reactors,
    and specialized reactor types with kinetics.

Heat Exchanger Examples
    Heat transfer calculations, different configurations,
    NTU-effectiveness method, and sizing.

Distillation Examples
    Binary distillation analysis, McCabe-Thiele method,
    and tray calculations.

Utilities Examples
    Mathematical utilities, regression analysis,
    and data fitting tools.

Complete Process Examples
    Integrated multi-unit process simulations demonstrating
    how all units work together.
