Compressor
==========

Process Description
------------------
Gas compressor model implementing isentropic compression theory with efficiency corrections for industrial applications including natural gas pipelines, refrigeration cycles, and process gas compression systems.

Key Equations
-------------

**Isentropic Temperature Rise:**

.. math::
   T_2^s = T_1 \left(\frac{P_2}{P_1}\right)^{\frac{\gamma-1}{\gamma}}

**Actual Temperature with Efficiency:**

.. math::
   T_2 = T_1 + \frac{T_2^s - T_1}{\eta_{isentropic}}

**Compression Power:**

.. math::
   W = \dot{n} \cdot R \cdot \frac{T_2 - T_1}{M}

Where γ is the heat capacity ratio (Cp/Cv), η is isentropic efficiency, ṅ is molar flow rate, R is the universal gas constant, and M is molar mass.

Process Parameters
------------------

+-----------------+-------------+-------+----------------------------------------+
| Parameter       | Range       | Units | Description                            |
+=================+=============+=======+========================================+
| η_isentropic    | 0.70-0.90   | -     | Isentropic efficiency                  |
+-----------------+-------------+-------+----------------------------------------+
| Pressure Ratio  | 1.5-10      | -     | P_discharge/P_suction                  |
+-----------------+-------------+-------+----------------------------------------+
| Suction Temp    | 250-350     | K     | Inlet gas temperature                  |
+-----------------+-------------+-------+----------------------------------------+
| Suction Press   | 1-50        | bar   | Inlet gas pressure                     |
+-----------------+-------------+-------+----------------------------------------+
| Flow Rate       | 10-10000    | Nm³/h | Volumetric flow at standard conditions |
+-----------------+-------------+-------+----------------------------------------+

Industrial Example
------------------
.. literalinclude:: Compressor_example.py
   :language: python

Results
-------
.. literalinclude:: Compressor_example.out
   :language: text

Process Behavior
----------------
.. image:: Compressor_example_plots.png
   :width: 700px
   :alt: Compressor performance curves showing outlet temperature and power consumption vs pressure ratio for different flow rates

The performance curves demonstrate typical centrifugal compressor behavior with:

- Linear relationship between pressure ratio and outlet temperature
- Quadratic power consumption with pressure ratio
- Flow rate proportional scaling of power requirements
- Safe operating limits below 150°C outlet temperature

Sensitivity Analysis
-------------------
.. image:: Compressor_detailed_analysis.png
   :width: 700px
   :alt: Detailed analysis including operating maps, gas property sensitivity, and economic optimization

The detailed analysis reveals:

- **Operating Map:** Temperature contours across flow and pressure ratio ranges
- **Gas Property Effects:** Different heat capacity ratios (γ) significantly affect compression behavior
- **Polytropic Comparison:** Real gas behavior deviations from ideal isentropic assumptions
- **Economic Optimization:** Life cycle cost minimization balances capital and operating expenses

Industrial Applications
----------------------

**Natural Gas Pipelines:** Transmission compression stations with pressure ratios of 1.5-2.5 per stage, typically operating at 80-85% isentropic efficiency.

**Refrigeration Systems:** Vapor compression cycles for industrial cooling with pressure ratios up to 4:1 for single-stage applications.

**Process Gas Compression:** Chemical plant applications including hydrogen recycle, synthesis gas compression, and pneumatic conveying systems.

Design Considerations
--------------------

**Mechanical Limits:**
- Maximum tip speed: 250-300 m/s for centrifugal compressors
- Outlet temperature limit: 150°C for standard materials
- Surge margin: 15-20% above surge line for stable operation

**Thermodynamic Constraints:**
- Ideal gas assumption valid for most applications above 2 bar
- Compression ratio limited by temperature rise and efficiency
- Multi-stage compression required for high pressure ratios

References
----------

1. **Perry's Chemical Engineers' Handbook, 8th Edition** - Section 10: Transport and Storage of Fluids
2. **Compressor Handbook** by Paul C. Hanlon - Comprehensive treatment of compressor design and operation  
3. **Gas Turbine Engineering Handbook** by Meherwan P. Boyce - Industrial gas compression applications
