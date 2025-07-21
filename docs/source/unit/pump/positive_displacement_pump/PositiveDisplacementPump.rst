PositiveDisplacementPump
=======================

Process Description
------------------
Positive displacement pump delivering constant volumetric flow regardless of discharge pressure. Essential for precise metering, high-pressure applications, and viscous fluid handling in chemical processes.

Key Equations
-------------
**Volumetric Flow:**

.. math::

   Q = \eta_{vol} \times V_d \times N

**Power Relationship:**

.. math::

   P = \frac{Q \times \Delta P}{\eta_{overall}}

**Slip Flow (Gear Pumps):**

.. math::

   Q_{slip} = \frac{\Delta P \times clearance^3}{12\mu L}

**Torque Requirement:**

.. math::

   T = \frac{\Delta P \times V_d}{2\pi \times \eta_{mech}}

Process Parameters
------------------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Symbol
     - Range
     - Units
     - Description
   * - Displacement
     - V_d
     - 1 - 1000
     - cm³/rev
     - Volume per revolution
   * - Volumetric Efficiency
     - η_vol
     - 0.85 - 0.98
     - dimensionless
     - Accounts for slip
   * - Overall Efficiency
     - η
     - 0.70 - 0.90
     - dimensionless
     - Combined efficiency
   * - Max Pressure
     - P_max
     - 10 - 700
     - bar
     - Design pressure limit

Industrial Example
------------------

.. literalinclude:: PositiveDisplacementPump_example.py
   :language: python

Results
-------

.. literalinclude:: PositiveDisplacementPump_example.out
   :language: text

Process Behavior
----------------

.. image:: PositiveDisplacementPump_example_plots.png
   :width: 600px

Application Analysis
-------------------

.. image:: PositiveDisplacementPump_detailed_analysis.png
   :width: 500px

References
----------

1. **Wright, W.A.** "Pumping Manual, 9th Edition" Elsevier, 1999
2. **Volk, M.** "Pump Characteristics and Applications, 2nd Edition" CRC Press, 2005
3. **ANSI/HI Standards** "Positive Displacement Pumps for Nomenclature, Definitions, Application, and Operation" HI, 2017
