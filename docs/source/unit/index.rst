
Unit Operations Documentation
============================

This section contains comprehensive documentation for all unit operations available in SPROCLIB.
Each unit operation provides mathematical models, simulation capabilities, and design calculations
for equipment commonly used in chemical process industries.

The unit operations are organized by equipment type and provide detailed documentation
for process modeling, control design, and optimization applications.

.. toctree::
    :maxdepth: 2
    :caption: Unit Operations:

    process/index
    reactor/index
    pump/index
    compressor/index
    valve/index
    tank/index
    heat_exchanger/index
    distillation/index
    utilities/index


Overview
--------

Each unit operation provides:

* **Mathematical Models**: Rigorous process models based on engineering principles
* **Simulation Capabilities**: Dynamic and steady-state simulation tools  
* **Design Calculations**: Sizing, performance, and optimization methods
* **Control Integration**: Interface for control system design and implementation

SPROCLIB Architecture
----------------------

The unit operations in SPROCLIB follow a modern modular architecture:

* **Individual Unit Classes**: Each unit operation is implemented as a dedicated class
* **Standardized Interface**: Common methods and properties across all units
* **Process Integration**: Seamless integration into chemical plant models
* **Control Integration**: Built-in support for control system design
* **Backward Compatibility**: Maintains compatibility with existing code

Unit Operation Categories
-------------------------

Complete Process Integration
    Multi-unit process examples demonstrating how different unit operations work 
    together in complete chemical processes with integrated control and optimization.

Reactor Operations
    Comprehensive reactor models including CSTR, PFR, batch reactors,
    and specialized reactor types with detailed reaction kinetics, heat transfer,
    and practical examples.

Pump Operations
    Centrifugal and positive displacement pump models with performance curves,
    system analysis, energy calculations, and real-world application examples.

Compressor Operations  
    Centrifugal and reciprocating compressor models with thermodynamic analysis,
    multi-stage operations, efficiency calculations, and design examples.

Valve Operations
    Control valve and three-way valve models with flow characteristics,
    pressure drop calculations, sizing methods, and control system examples.

Tank Operations
    Storage tank and process vessel models with level dynamics,
    mixing analysis, heat transfer capabilities, and practical applications.

Heat Exchanger Operations
    Shell-and-tube, plate, and specialized heat exchanger models with
    NTU-effectiveness methods, thermal design calculations, and optimization examples.

Distillation Operations
    Binary and multi-component distillation models with McCabe-Thiele analysis,
    tray-by-tray calculations, column design methods, and separation examples.

Utility Operations
    Mathematical utilities, property calculations, and supporting functions
    for process analysis and design calculations with computational examples.
