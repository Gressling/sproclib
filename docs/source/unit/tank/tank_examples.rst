
Tank Examples
=============

This example demonstrates the usage of tank units in SPROCLIB.

Example Output
--------------

.. code-block:: text

    SPROCLIB Tank Examples
    ==================================================
    === Simple Tank Examples ===
    
    --- Single Tank ---
    Tank created: Basic Storage Tank
    Type: Tank
    
    Tank specifications:
    Total volume: 1000.0 L
    Initial level: 50.0%
    Initial volume: 500.0 L
    
    Flow rates:
    Inlet flow: 10.0 L/min
    Outlet flow: 8.0 L/min
    Net flow: 2.0 L/min
    Time to fill: 250.0 minutes
    
    --- Interacting Tanks ---
    Tank system created: Two Tank System
    Type: InteractingTanks
    
    System specifications:
    Tank 1 volume: 800.0 L (Level: 70.0%)
    Tank 2 volume: 1200.0 L (Level: 30.0%)
    Connection flow: 5.0 L/min
    
    Current volumes:
    Tank 1: 560.0 L
    Tank 2: 360.0 L
    Total liquid: 920.0 L
    
    Simple tank examples completed successfully!
    
    === Comprehensive Tank Examples ===
    
    --- Dynamic Level Control ---
    Level Control Simulation:
    Setpoint: 60.0%
    Initial level: 40.0%
    Tank volume: 2000.0 L
    
    Time (min) Level (%)  Error    Controller   Flow In   
    ------------------------------------------------------------
    0          43.0       20.0     20.0         20.0      
    5          46.0       17.0     20.0         20.0      
    10         49.0       14.0     20.0         20.0      
    15         52.0       11.0     20.0         20.0      
    20         55.0       8.0      20.0         20.0      
    25         58.0       5.0      20.0         20.0      
    30         61.0       2.0      20.0         20.0      
    35         64.0       -1.0     20.0         20.0      
    40         66.4       -4.0     17.7         17.7      
    45         66.8       -6.4     9.7          9.7       
    50         66.3       -6.8     5.6          5.6       
    55         65.2       -6.3     3.8          3.8       
    60         64.0       -5.2     3.3          3.3       
    
    --- Multi-Tank Cascade System ---
    Cascade System Configuration:
    ----------------------------------------------------------------------
    Tank     Volume (L)   Initial Level (%)  Current Volume (L)
    ----------------------------------------------------------------------
    Tank 1   500          80                 400.0             
    Tank 2   750          60                 450.0             
    Tank 3   1000         40                 400.0             
    Tank 4   1250         20                 250.0             
    
    Cascade Flow Simulation (steady state):
    --------------------------------------------------
    Tank 1: In = 12.0 L/min, Out = 13.0 L/min
    Tank 2: In = 13.0 L/min, Out = 13.5 L/min
    Tank 3: In = 13.5 L/min, Out = 13.7 L/min
    Tank 4: In = 13.7 L/min, Out = 13.4 L/min
    
    --- Heat Transfer Analysis ---
    Heat Transfer Simulation:
    Tank volume: 5.0 m�
    Heating power: 50 kW
    Initial temperature: 20.0�C
    Ambient temperature: 15.0�C
    
    Time (h)   Temp (�C)    Heat Loss (kW)  Net Heat (kW)  
    ------------------------------------------------------------
    0.0        20.0         0.5             49.5           
    0.5        20.0         0.5             49.5           
    1.0        20.0         0.5             49.5           
    1.5        20.0         0.5             49.5           
    2.0        20.0         0.5             49.5           
    2.5        20.0         0.5             49.5           
    3.0        20.0         0.5             49.5           
    3.5        20.0         0.5             49.5           
    4.0        20.0         0.5             49.5           
    
    --- Mixing and Residence Time Analysis ---
    Mixing Tank Analysis:
    Working volume: 3000.0 L
    Flow rate: 150.0 L/min
    Residence time: 20.0 minutes
    Error running examples: 'charmap' codec can't encode character '\u207b' in position 24: character maps to <undefined>

Source Code
-----------

The complete source code for this example can be found in:
``examples/tank_examples.py``

Key Features Demonstrated
-------------------------

* Simple usage examples for quick learning
* Comprehensive analysis for advanced applications  
* Real engineering calculations and parameters
* Educational explanations and insights

This example is part of the refactored SPROCLIB where each unit class 
is now in its own file for better modularity and maintainability.
