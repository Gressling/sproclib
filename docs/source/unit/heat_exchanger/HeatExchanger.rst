HeatExchanger
=============

Process Description
------------------
Counter-current shell-and-tube heat exchanger for thermal energy recovery in process applications. 
Uses effectiveness-NTU method for heat transfer calculations with dynamic thermal response modeling.
Commonly applied in crude oil preheat trains, process cooling, and heat integration systems.

Key Equations
-------------

**Effectiveness-NTU Method:**

.. math::
   
   \varepsilon = \frac{1 - \exp(-NTU(1-C_r))}{1 - C_r \exp(-NTU(1-C_r))}

**Heat Transfer Rate:**

.. math::
   
   Q = \varepsilon \cdot C_{min} \cdot (T_{h,in} - T_{c,in})

**Number of Transfer Units:**

.. math::
   
   NTU = \frac{UA}{C_{min}}

**Thermal Dynamics:**

.. math::
   
   \tau \frac{dT}{dt} = T_{ss} - T

where :math:`\tau = \frac{\rho V c_p}{C}` is the thermal time constant.

Process Parameters
------------------

========================== ================ ========= ================================
Parameter                  Typical Range    Units     Description
========================== ================ ========= ================================
Overall HTC (U)            100 - 2000       W/m²·K    Heat transfer coefficient
Heat Transfer Area (A)     10 - 500         m²        Surface area for heat exchange
Hot Flow Rate              0.5 - 100        kg/s      Hot fluid mass flow rate
Cold Flow Rate             0.5 - 100        kg/s      Cold fluid mass flow rate
Effectiveness (ε)          0.1 - 0.95       -         Thermal effectiveness
NTU                        0.5 - 10         -         Number of Transfer Units
Hot Inlet Temperature      60 - 250         °C        Process heating temperature
Cold Inlet Temperature     10 - 80          °C        Cooling medium temperature
Pressure Drop              <20              kPa       Allowable pressure loss
========================== ================ ========= ================================

Industrial Example
------------------
.. literalinclude:: HeatExchanger_example.py
   :language: python

Results
-------
.. literalinclude:: HeatExchanger_example.out
   :language: text

Process Behavior
----------------
.. image:: HeatExchanger_example_plots.png
   :width: 800px
   :alt: Heat exchanger process behavior showing effectiveness-NTU curves, temperature profiles, and operating windows

The process behavior plots demonstrate:

* **Effectiveness-NTU relationship** for different heat capacity ratios with marked operating point
* **Heat transfer rate vs flow rate** showing performance optimization and effectiveness trade-offs  
* **Temperature profiles** along exchanger length illustrating counter-current heat exchange
* **Operating window** with pressure-temperature limits and heat duty contours for safe operation

Sensitivity Analysis
-------------------
.. image:: HeatExchanger_detailed_analysis.png
   :width: 800px
   :alt: Detailed parameter sensitivity analysis and design optimization for heat exchanger

The detailed analysis includes:

* **Heat transfer coefficient vs area** design space showing performance sensitivity
* **Effectiveness vs Reynolds number** correlation for turbulent flow optimization
* **Economic optimization** balancing capital cost against energy savings over equipment lifetime
* **Fouling impact analysis** demonstrating performance degradation and maintenance requirements

Engineering Applications
------------------------

**Process Industries:**
- Crude oil preheat trains (200°C hot oil, 5-15 MW duty)
- Chemical reactor cooling systems (exothermic reaction heat removal)
- Distillation column condensers and reboilers (phase change applications)
- Gas processing heat recovery (natural gas treatment plants)

**Design Considerations:**
- Minimum temperature approach: 10-20 K for economic operation
- Fouling allowance: 15-25% reduction in clean U-value
- Pressure drop limits: <10% of operating pressure
- Thermal stress management for temperature cycling

**Scale-up Guidelines:**
- Heat flux range: 5,000-50,000 W/m² for liquid-liquid service
- Velocity limits: 0.5-3 m/s shell side, 1-5 m/s tube side
- Area density: 100-500 m²/m³ for compact designs

References
----------

1. **Incropera, F.P. & DeWitt, D.P.** "Fundamentals of Heat and Mass Transfer", 7th Edition, Wiley (2011)
   - Chapter 11: Heat Exchangers - comprehensive treatment of effectiveness-NTU method

2. **Shah, R.K. & Sekulic, D.P.** "Fundamentals of Heat Exchanger Design", Wiley (2003)  
   - Detailed design methodology and thermal-hydraulic analysis for industrial applications

3. **Perry's Chemical Engineers' Handbook**, 8th Edition, McGraw-Hill (2008)
   - Section 11: Heat Transfer - practical correlations and design guidelines for process equipment
