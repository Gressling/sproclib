DistillationTray
===============

Process Description
------------------
Individual theoretical tray model for binary distillation systems implementing vapor-liquid equilibrium relationships and material balance dynamics for separation control design.

Key Equations
-------------
**Vapor-Liquid Equilibrium:**

.. math::
   y = \frac{\alpha \cdot x}{1 + (\alpha - 1) \cdot x}

**Material Balance:**

.. math::
   \frac{dN \cdot x}{dt} = L_{in} \cdot x_{in} + V_{in} \cdot y_{in} - L_{out} \cdot x_{out} - V_{out} \cdot y_{out}

Where:
- α = relative volatility (light/heavy component)
- x = liquid mole fraction 
- y = vapor mole fraction
- L, V = liquid and vapor flow rates (kmol/min)
- N = tray holdup (kmol)

Process Parameters
------------------
================= ============= ======================= =============================
Parameter         Units         Typical Range           Description
================= ============= ======================= =============================
Tray Holdup       kmol          0.1 - 100               Liquid molar inventory
Relative Volatility dimensionless 1.01 - 20.0           Separation difficulty factor
Liquid Flow       kmol/min      1 - 1000                Downflow from tray above
Vapor Flow        kmol/min      1 - 1500                Upflow from tray below
Composition       mole fraction 0.0 - 1.0               Light component fraction
================= ============= ======================= =============================

Industrial Example
------------------
.. literalinclude:: DistillationTray_example.py
   :language: python

Results
-------
.. literalinclude:: DistillationTray_example.out
   :language: text

Process Behavior
----------------
.. image:: DistillationTray_example_plots.png
   :width: 500px

Sensitivity Analysis
-------------------
.. image:: DistillationTray_detailed_analysis.png
   :width: 500px

References
----------
- Seborg, D.E., Edgar, T.F., Mellichamp, D.A. "Process Dynamics and Control", 4th Ed., Wiley (2016)
- McCabe, W.L., Smith, J.C., Harriott, P. "Unit Operations of Chemical Engineering", 7th Ed., McGraw-Hill (2004)
- Kister, H.Z. "Distillation Design", McGraw-Hill (1992)
