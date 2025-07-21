ControlValve
============

Process Description
------------------
Industrial control valve with flow coefficient characteristics for automated flow regulation in chemical processes. Implements equal percentage, linear, and quick opening valve characteristics with actuator dead-time and first-order lag dynamics.

Key Equations
-------------

**Flow Equation:**

.. math::

   Q = C_v \sqrt{\frac{\Delta P}{\rho}}

Where:
- Q = Volumetric flow rate (m³/s)
- Cv = Flow coefficient (gpm/psi^0.5)
- ΔP = Pressure drop (Pa)
- ρ = Fluid density (kg/m³)

**Valve Characteristics:**

- **Linear**: :math:`C_v = C_{v,min} + x(C_{v,max} - C_{v,min})`
- **Equal Percentage**: :math:`C_v = C_{v,min} \times R^x`
- **Quick Opening**: :math:`C_v = C_{v,min} + (C_{v,max} - C_{v,min})\sqrt{x}`

**Actuator Dynamics:**

.. math::

   \tau \frac{dx}{dt} + x = x_{cmd}(t - t_d)

Where τ = time constant, td = dead time

Process Parameters
------------------

=============  ==============  ==================  ===============================
Parameter      Typical Range   Units               Description
=============  ==============  ==================  ===============================
Cv_max         10-500          gpm/psi^0.5         Maximum flow coefficient
Rangeability   20-50           dimensionless       Cv_max/Cv_min ratio
Dead Time      0.5-5.0         s                   Actuator response delay
Time Constant  1-10            s                   Actuator time constant
Position       0-1             fraction            Valve opening
=============  ==============  ==================  ===============================

Industrial Example
------------------

.. literalinclude:: ControlValve_example.py
   :language: python

Results
-------

.. literalinclude:: ControlValve_example.out
   :language: text

Process Behavior
----------------

.. image:: ControlValve_example_plots.png
   :width: 500px

Sensitivity Analysis
-------------------

.. image:: ControlValve_detailed_analysis.png
   :width: 500px

References
----------

1. **ISA-75.01.01**: Control Valve Sizing Equations
2. **Perry's Chemical Engineers' Handbook**: Chapter 6 - Fluid and Particle Dynamics  
3. **Fisher Controls**: Control Valve Handbook - Valve sizing and characteristics
