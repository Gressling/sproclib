BinaryDistillationColumn
========================

Process Description
------------------
Complete binary distillation column model integrating multi-tray dynamics with material balance equations for separation control design and optimization in industrial applications.

Key Equations
-------------
**Column Material Balance:**

.. math::
   \frac{dx_i}{dt} = \frac{L_{i+1} \cdot x_{i+1} + V_{i-1} \cdot y_{i-1} - L_i \cdot x_i - V_i \cdot y_i + F_i \cdot x_{F,i}}{M_i}

**Vapor-Liquid Equilibrium per Tray:**

.. math::
   y_i = \frac{\alpha \cdot x_i}{1 + (\alpha - 1) \cdot x_i}

**Separation Factor:**

.. math::
   S = \frac{x_D / (1 - x_D)}{x_B / (1 - x_B)}

**Minimum Reflux Ratio:**

.. math::
   R_{min} = \frac{x_D}{1 - x_D} \cdot \frac{1 - x_F}{x_F} \cdot \frac{1}{\alpha - 1}

Process Parameters
------------------
==================== ============= ======================= =============================
Parameter            Units         Typical Range           Description
==================== ============= ======================= =============================
Number of Trays      dimensionless 5 - 100                 Theoretical stages
Feed Tray Location   dimensionless 1 - N_trays             Optimal feed point
Reflux Ratio         dimensionless 0.1 - 50.0              L/D ratio
Relative Volatility  dimensionless 1.01 - 20.0             Separation factor
Tray Holdup          kmol          0.5 - 10.0              Per tray inventory
Reflux Drum Holdup   kmol          5.0 - 50.0              Condenser inventory
Reboiler Holdup      kmol          10.0 - 100.0            Reboiler inventory
Feed Flow            kmol/min      10 - 1000               Feed rate
==================== ============= ======================= =============================

Industrial Example
------------------
.. literalinclude:: BinaryDistillationColumn_example.py
   :language: python

Results
-------
.. literalinclude:: BinaryDistillationColumn_example.out
   :language: text

Process Behavior
----------------
.. image:: BinaryDistillationColumn_example_plots.png
   :width: 500px

Sensitivity Analysis
-------------------
.. image:: BinaryDistillationColumn_detailed_analysis.png
   :width: 500px

References
----------
- Luyben, W.L. "Distillation Design and Control Using Aspen Simulation", 2nd Ed., Wiley (2013)
- Skogestad, S. "Distillation Control", Encyclopedia of Systems and Control, Springer (2021)
- King, C.J. "Separation Processes", 2nd Ed., McGraw-Hill (1980)
