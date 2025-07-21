CentrifugalPump
==============

Process Description
------------------
Centrifugal pump with quadratic head-flow characteristics for dynamic flow applications. Models realistic pump behavior where head decreases with increasing flow rate according to pump affinity laws.

Key Equations
-------------
**Pump Curve:**

.. math::

   H = H_0 - K \times Q^2

**Pressure-Head Relationship:**

.. math::

   \Delta P = \rho \times g \times H

**Affinity Laws:**

.. math::

   \frac{Q_2}{Q_1} = \frac{N_2}{N_1}, \quad \frac{H_2}{H_1} = \left(\frac{N_2}{N_1}\right)^2

**Specific Speed:**

.. math::

   N_s = \frac{N \sqrt{Q}}{H^{3/4}}

Process Parameters
------------------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Symbol
     - Range
     - Units
     - Description
   * - Shutoff Head
     - H₀
     - 10 - 200
     - m
     - Head at zero flow
   * - Head Coefficient
     - K
     - 1 - 500
     - s²/m⁵
     - Curve steepness
   * - Efficiency
     - η
     - 0.3 - 0.85
     - dimensionless
     - Peak efficiency
   * - Specific Speed
     - Ns
     - 10 - 200
     - dimensionless
     - Design parameter

Industrial Example
------------------

.. literalinclude:: CentrifugalPump_example.py
   :language: python

Results
-------

.. literalinclude:: CentrifugalPump_example.out
   :language: text

Process Behavior
----------------

.. image:: CentrifugalPump_example_plots.png
   :width: 600px

Performance Analysis
-------------------

.. image:: CentrifugalPump_detailed_analysis.png
   :width: 500px

References
----------

1. **Gülich, J.F.** "Centrifugal Pumps, 3rd Edition" Springer, 2014
2. **Karassik, I.J.** "Pump Handbook, 4th Edition" McGraw-Hill, 2008
3. **Stepanoff, A.J.** "Centrifugal and Axial Flow Pumps, 2nd Edition" Wiley, 1957
