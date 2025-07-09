
Valve Examples
==============

This example demonstrates the usage of valve units in SPROCLIB.

Example Output
--------------

.. code-block:: text

    SPROCLIB Valve Examples
    ==================================================
    === Simple Valve Examples ===
    
    --- Control Valve ---
    Control valve created: Basic Control Valve
    Type: ControlValve
    
    Operating conditions:
    Valve opening: 50.0%
    Inlet pressure: 10.0 bar
    Outlet pressure: 5.0 bar
    Pressure drop: 5.0 bar
    
    --- Three-Way Valve ---
    Three-way valve created: Basic Three-Way Valve
    Type: ThreeWayValve
    
    Operating conditions:
    Inlet flow: 100.0 kg/h
    Split ratio (A:B): 0.7:0.3
    Flow to outlet A: 70.0 kg/h
    Flow to outlet B: 30.0 kg/h
    
    Simple valve examples completed successfully!
    
    === Comprehensive Valve Examples ===
    
    --- Control Valve Characteristics ---
    Valve Characteristic Curves:
    ------------------------------------------------------------
    Position (%) Linear     Equal %    Quick Open   Butterfly   
    ------------------------------------------------------------
    0            0.000      0.000      0.000        0.000       
    10           0.100      0.316      0.259        0.156       
    20           0.200      0.447      0.451        0.309       
    30           0.300      0.548      0.593        0.454       
    40           0.400      0.632      0.699        0.588       
    50           0.500      0.707      0.777        0.707       
    60           0.600      0.775      0.835        0.809       
    70           0.700      0.837      0.878        0.891       
    80           0.800      0.894      0.909        0.951       
    90           0.900      0.949      0.933        0.988       
    100          1.000      1.000      0.950        1.000       
    
    --- Flow Coefficient (Cv) Analysis ---
    Test   P1 (bar)   P2 (bar)   Flow (GPM)   SG     Cv Required 
    ----------------------------------------------------------------------
    1      10.0       8.0        50.0         1.0    35.36       
    2      15.0       10.0       75.0         0.8    30.00       
    3      5.0        2.0        100.0        1.2    63.25       
    
    --- Three-Way Valve Splitting Analysis ---
    Flow Splitting Scenarios:
    -----------------------------------------------------------------
    Split Ratio  Flow A (kg/h)   Flow B (kg/h)   Pressure Drop A
    -----------------------------------------------------------------
    0.10         20.0            180.0           0.020          
    0.20         40.0            160.0           0.080          
    0.30         60.0            140.0           0.180          
    0.40         80.0            120.0           0.320          
    0.50         100.0           100.0           0.500          
    0.60         120.0           80.0            0.720          
    0.70         140.0           60.0            0.980          
    0.80         160.0           40.0            1.280          
    0.90         180.0           20.0            1.620          
    
    --- Valve Sizing Example ---
    Error running examples: 'charmap' codec can't encode character '\u0394' in position 31: character maps to <undefined>

Source Code
-----------

The complete source code for this example can be found in:
``examples/valve_examples.py``

Key Features Demonstrated
-------------------------

* Simple usage examples for quick learning
* Comprehensive analysis for advanced applications  
* Real engineering calculations and parameters
* Educational explanations and insights

This example is part of the refactored SPROCLIB where each unit class 
is now in its own file for better modularity and maintainability.
