
Compressor Examples
===================

This example demonstrates the usage of compressor units in SPROCLIB.

Example Output
--------------

.. code-block:: text

    SPROCLIB Compressor Examples
    ==================================================
    === Simple Compressor Example ===
    Compressor created: Basic Compressor
    Type: Compressor
    
    Operating conditions:
    Inlet pressure: 1.0 bar
    Outlet pressure: 5.0 bar
    Flow rate: 100.0 kg/h
    Efficiency: 0.8
    Compression ratio: 5.00
    
    Simple compressor example completed successfully!
    
    === Comprehensive Compressor Example ===
    Performance Analysis:
    --------------------------------------------------------------------------------
    Condition    P_in (bar)   P_out (bar)  Flow (kg/h)  Ratio    Efficiency
    --------------------------------------------------------------------------------
    Case 1       1.0          3.0          80.0         3.00     0.75      
    Case 2       1.0          5.0          100.0        5.00     0.80      
    Case 3       1.0          8.0          120.0        8.00     0.78      
    Case 4       2.0          10.0         150.0        5.00     0.82      
    
    --- Multi-Stage Compression Analysis ---
    Multi-stage compression from 1.0 to 16.0 bar
    Number of stages: 3
    Total compression ratio: 16.00
    Optimal stage ratio: 2.52
    
    Stage-by-stage pressure progression:
    Error running examples: 'charmap' codec can't encode character '\u2192' in position 14: character maps to <undefined>

Source Code
-----------

The complete source code for this example can be found in:
``examples/compressor_examples.py``

Key Features Demonstrated
-------------------------

* Simple usage examples for quick learning
* Comprehensive analysis for advanced applications  
* Real engineering calculations and parameters
* Educational explanations and insights

This example is part of the refactored SPROCLIB where each unit class 
is now in its own file for better modularity and maintainability.
