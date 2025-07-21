ThreeWayValve
=============

Process Description
------------------
Three-way control valve for flow mixing (two inlets, one outlet) or diverting (one inlet, two outlets) applications. Enables proportional flow splitting and stream mixing control with dead-time compensation for industrial process control.

Key Equations
-------------

**Flow Coefficient Splitting:**

.. math::

   C_{v,A} = C_{v,max} \times (1 - x)

.. math::

   C_{v,B} = C_{v,max} \times x

**Flow Calculations:**

.. math::

   Q = C_v \sqrt{\frac{\Delta P}{\rho}}

**Mass Balance:**

- **Mixing**: :math:`Q_{out} = Q_{inlet1} + Q_{inlet2}`
- **Diverting**: :math:`Q_{inlet} = Q_{outlet1} + Q_{outlet2}`

**Temperature Mixing:**

.. math::

   T_{mixed} = \frac{\dot{m}_1 T_1 + \dot{m}_2 T_2}{\dot{m}_1 + \dot{m}_2}

Process Parameters
------------------

===============  ==============  ==================  ===============================
Parameter        Typical Range   Units               Description
===============  ==============  ==================  ===============================
Cv_max           10-500          gpm/psi^0.5         Maximum single-path flow coefficient
Position         0-1             fraction            Flow split ratio
Dead Time        0.5-5.0         s                   Actuator response delay
Time Constant    1-10            s                   Actuator time constant
Flow Split       0-100%          %                   Percentage to each outlet
===============  ==============  ==================  ===============================

Industrial Example
------------------

.. literalinclude:: ThreeWayValve_example.py
   :language: python

Results
-------

.. literalinclude:: ThreeWayValve_example.out
   :language: text

Process Behavior
----------------

.. image:: ThreeWayValve_example_plots.png
   :width: 500px

Sensitivity Analysis
-------------------

.. image:: ThreeWayValve_detailed_analysis.png
   :width: 500px

References
----------

1. **ANSI/ISA-75.25.01**: Test Procedure for Control Valve Response Measurement
2. **EEUA Guidelines**: Three-Way Control Valves - Selection and Sizing
3. **Crane Technical Paper 410**: Flow of Fluids Through Valves, Fittings, and Pipe
