
Utilities Examples
==================

This example demonstrates the usage of utilities units in SPROCLIB.

Example Output
--------------

.. code-block:: text

    SPROCLIB Utilities Examples
    ==================================================
    === Simple Utilities Examples ===
    
    --- Linear Approximation ---
    Linear approximation created for model: Test Model
    Type: LinearApproximation
    
    Data points:
    X values: [10, 20, 30, 40, 50]
    Y values: [25, 45, 70, 90, 115]
    
    Linear approximation:
    Slope: 2.250
    Intercept: 1.500
    Equation: y = 2.250x + 1.500
    R-squared: 0.9985
    
    Interpolation/Extrapolation:
    X        Y (predicted)   Type           
    ----------------------------------------
    15       35.25           Interpolation  
    25       57.75           Interpolation  
    35       80.25           Interpolation  
    55       125.25          Extrapolation  
    
    Simple utilities examples completed successfully!
    
    === Comprehensive Utilities Examples ===
    
    --- Multiple Linear Regression ---
    Multiple Linear Regression Analysis:
    Conversion = f(Temperature, Pressure, Residence Time)
    
    Regression equation:
    Error running examples: 'charmap' codec can't encode character '\u03c4' in position 54: character maps to <undefined>

Source Code
-----------

The complete source code for this example can be found in:
``examples/utilities_examples.py``

Key Features Demonstrated
-------------------------

* Simple usage examples for quick learning
* Comprehensive analysis for advanced applications  
* Real engineering calculations and parameters
* Educational explanations and insights

This example is part of the refactored SPROCLIB where each unit class 
is now in its own file for better modularity and maintainability.
