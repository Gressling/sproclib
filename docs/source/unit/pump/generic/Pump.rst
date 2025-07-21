Pump
====

Process Description
------------------
Generic liquid pump model providing constant pressure rise for process fluid transport. Represents fundamental hydraulic behavior of pumping equipment with steady-state and dynamic response characteristics.

Key Equations
-------------
**Hydraulic Power:**

.. math::

   P_{hydraulic} = Q \times \Delta P

**Brake Power with Efficiency:**

.. math::

   P_{brake} = \frac{Q \times \Delta P}{\eta}

**Dynamic Response (First-Order):**

.. math::

   \tau \frac{dP_{out}}{dt} = P_{ss} - P_{out}

Process Parameters
------------------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Symbol
     - Range
     - Units
     - Description
   * - Efficiency
     - η
     - 0.5 - 0.85
     - dimensionless
     - Overall pump efficiency
   * - Density
     - ρ
     - 800 - 1200
     - kg/m³
     - Liquid density
   * - Nominal Flow
     - Q_nom
     - 0.001 - 10
     - m³/s
     - Design volumetric flow
   * - Pressure Rise
     - ΔP_nom
     - 50,000 - 2,000,000
     - Pa
     - Design pressure increase

Industrial Example
------------------

.. literalinclude:: Pump_example.py
   :language: python

Results
-------

.. literalinclude:: Pump_example.out
   :language: text

Process Behavior
----------------

.. image:: Pump_example_plots.png
   :width: 600px

Sensitivity Analysis
-------------------

.. image:: Pump_detailed_analysis.png
   :width: 500px

References
----------

1. **Karassik, I.J. et al.** "Pump Handbook, 4th Edition" McGraw-Hill, 2008
2. **Perry, R.H. & Green, D.W.** "Perry's Chemical Engineers' Handbook, 8th Edition" McGraw-Hill, 2008
3. **Gülich, J.F.** "Centrifugal Pumps, 3rd Edition" Springer, 2014
