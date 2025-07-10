
Heat Exchanger Examples
=======================

This example demonstrates the usage of heat exchanger units in SPROCLIB.

Example Output
--------------

.. code-block:: text

    SPROCLIB Heat Exchanger Examples
    ==================================================
    === Simple Heat Exchanger Examples ===
    
    --- Basic Heat Exchanger ---
    Heat exchanger created: Basic Shell-and-Tube HX
    Type: HeatExchanger
    
    Operating conditions:
    Hot fluid inlet: 150.0�C
    Hot fluid outlet: 100.0�C
    Cold fluid inlet: 25.0�C
    Hot flow rate: 5000.0 kg/h
    Cold flow rate: 4000.0 kg/h
    
    Results:
    Heat duty: 290.3 kW
    Cold fluid outlet: 87.5�C
    Heat exchanger effectiveness: 0.500
    Maximum possible heat transfer: 580.6 kW
    
    Simple heat exchanger examples completed successfully!
    
    === Comprehensive Heat Exchanger Examples ===
    
    --- Flow Configuration Comparison ---
    Common parameters:
    Hot inlet: 120.0�C, Cold inlet: 20.0�C
    Flow rates: 3600.0 kg/h each
    Overall U: 500.0 W/m��K
    Heat transfer area: 50.0 m�
    
    Configuration   Hot Outlet (�C) Cold Outlet (�C) Heat Duty (kW)  LMTD (�C)   
    -------------------------------------------------------------------------------------
    Parallel Flow   70.0            70.0             208998.7        8.4         
    Counter Flow    34.3            105.7            358122.0        14.3        
    Cross Flow      20.3            119.7            416927.8        0.3         
    
    --- NTU-Effectiveness Analysis ---
    Counter-flow Heat Exchanger Effectiveness:
    C_ratio  NTU=0.5  NTU=1.0  NTU=1.5  NTU=2.0  NTU=2.5  NTU=3.0  NTU=3.5  NTU=4.0 
    --------------------------------------------------------------------------------
    0.2      0.381    0.605    0.744    0.832    0.889    0.926    0.951    0.967   
    0.5      0.362    0.565    0.691    0.775    0.833    0.874    0.905    0.927   
    0.8      0.345    0.525    0.636    0.711    0.764    0.804    0.835    0.860   
    1.0      0.333    0.500    0.600    0.667    0.714    0.750    0.778    0.800   
    1.5      0.307    0.440    0.513    0.558    0.588    0.608    0.623    0.634   
    2.0      0.282    0.387    0.437    0.464    0.479    0.487    0.492    0.495   
    
    --- Fouling Effects Analysis ---
    Impact of Fouling on Heat Exchanger Performance:
    Clean overall U coefficient: 800.0 W/m��K
    
    Fouling Resistance Fouled U (W/m��K)  Performance Loss (%)
    ------------------------------------------------------------
    0.0000             800.0              0.0                 
    0.0001             740.7              7.4                 
    0.0003             645.2              19.4                
    0.0005             571.4              28.6                
    0.0010             444.4              44.4                
    0.0020             307.7              61.5                
    
    --- Multi-Pass Shell-and-Tube Analysis ---
    F-factor for different pass arrangements:
    (Temperature correction factor for LMTD)
    Shell Passes  Tube=2   Tube=4   Tube=6   Tube=8  
    ------------------------------------------------------------
    1             0.950    0.910    0.870    0.830   
    2             0.930    0.910    0.890    0.870   
    4             1.000    1.000    0.990    0.970   
    
    --- Heat Exchanger Sizing ---
    Sizing for 2000.0 kW duty:
    Error running examples: 'charmap' codec can't encode character '\u2192' in position 13: character maps to <undefined>

Source Code
-----------

The complete source code for this example can be found in:
``examples/heat_exchanger_examples.py``

Key Features Demonstrated
-------------------------

* Simple usage examples for quick learning
* Comprehensive analysis for advanced applications  
* Real engineering calculations and parameters
* Educational explanations and insights

This example is part of the refactored SPROCLIB where each unit class 
is now in its own file for better modularity and maintainability.
