PID Controller
==============

Process Description
------------------
Three-term feedback controller providing proportional, integral, and derivative control action for single-input single-output process regulation. Standard industrial controller for temperature, flow, pressure, and level control applications.

Key Equations
-------------

**Control Algorithm:**

.. math::
   u(t) = K_p \cdot e(t) + K_i \int_0^t e(\tau) d\tau + K_d \frac{de(t)}{dt}

**Transfer Function:**

.. math::
   C(s) = K_p + \frac{K_i}{s} + K_d s

Where:
- :math:`e(t) = SP - PV` (control error)
- :math:`K_p` = proportional gain [output_units/input_units]
- :math:`K_i` = integral gain [output_units/(input_units·s)]
- :math:`K_d` = derivative gain [output_units·s/input_units]

Process Parameters
------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Parameter
     - Typical Range
     - Units
     - Description
   * - Kp
     - 0.1 - 10
     - process dependent
     - Proportional gain
   * - Ki
     - 0.01 - 5
     - 1/s
     - Integral gain  
   * - Kd
     - 0 - 60
     - s
     - Derivative gain
   * - Output limits
     - 0 - 100
     - %
     - Actuator constraints
   * - Sample time
     - 0.1 - 10
     - s
     - Control execution frequency

Industrial Example
------------------

.. literalinclude:: PIDController_simple_example.py
   :language: python

Results
-------

.. literalinclude:: PIDController_example.out
   :language: text

Process Behavior
----------------

.. image:: PIDController_example_plots.png
   :width: 600px
   :alt: PID Controller Performance Comparison

The performance comparison shows trade-offs between tuning approaches:

- **Conservative tuning**: Stable response, minimal overshoot, slower settling
- **Moderate tuning**: Balanced performance for most applications  
- **Aggressive tuning**: Fast response but higher overshoot and control effort

Sensitivity Analysis
-------------------

.. image:: PIDController_detailed_analysis.png
   :width: 600px
   :alt: PID Controller Parameter Sensitivity

The detailed analysis illustrates:

- **Proportional gain effects**: Higher Kp increases response speed but may cause overshoot
- **Disturbance rejection**: PID automatically compensates for process upsets
- **Frequency response**: Controller behavior across different time scales
- **Operating map**: Steady-state valve position vs temperature relationship

Industrial Applications
----------------------

**Reactor Temperature Control:**
- Setpoint range: 50-200°C
- Control valve: 0-100% cooling/heating duty
- Typical accuracy: ±0.5-2.0°C

**Flow Control Systems:**
- Flow range: 0.1-1000 m³/h  
- Response time: 1-60 seconds
- Control valve or VFD manipulation

**Distillation Column Control:**
- Reflux ratio or reboiler duty control
- Temperature setpoints: 50-150°C
- Conservative tuning for stability

Design Guidelines
----------------

**Tuning Approach:**
1. Start with proportional-only control (Ki=Kd=0)
2. Add integral action to eliminate offset
3. Add derivative for improved transient response
4. Tune conservatively for safety-critical processes

**Performance Criteria:**
- Settling time: 2-4 process time constants
- Overshoot: <10% for well-tuned systems
- Steady-state error: <1% with integral action

References
----------

1. Åström, K.J. & Hägglund, T. (2006). *Advanced PID Control*. ISA Press.
2. Stephanopoulos, G. (1984). *Chemical Process Control: An Introduction to Theory and Practice*. Prentice Hall.
3. Seborg, D.E., Edgar, T.F., Mellichamp, D.A. & Doyle III, F.J. (2016). *Process Dynamics and Control*, 4th Edition. Wiley.
