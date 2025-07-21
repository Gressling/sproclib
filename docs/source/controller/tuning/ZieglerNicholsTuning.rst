ZieglerNicholsTuning
===================

.. currentmodule:: sproclib.controller.tuning

The :class:`ZieglerNicholsTuning` class implements the classic Ziegler-Nichols tuning methods for PID controllers in chemical process applications. This empirical approach provides reliable starting points for controller tuning based on process step response or ultimate gain/frequency measurements.

.. autoclass:: ZieglerNicholsTuning
   :members:
   :undoc-members:
   :show-inheritance:

Theory and Applications
-----------------------

The Ziegler-Nichols tuning rules were developed in 1942 and remain widely used in chemical engineering for their simplicity and effectiveness across diverse process types. The methods are particularly valuable for:

- **Initial controller tuning** when process models are unavailable
- **Field tuning** using simple test procedures  
- **Baseline tuning** before optimization
- **Training and education** in control fundamentals

Mathematical Foundation
^^^^^^^^^^^^^^^^^^^^^^^

**Open-Loop Method (Step Response)**

From a process step response, identify:

* Process gain: Kp = Δy/Δu (steady-state)
* Dead time: L (apparent delay)
* Time constant: T (from tangent line method)

PID parameters:

* Kc = 1.2T/(KpL) 
* τI = 2L
* τD = 0.5L

**Closed-Loop Method (Ultimate Gain)**

From sustained oscillation test:

* Ultimate gain: Ku (proportional gain causing oscillation)
* Ultimate period: Pu (oscillation period)

PID parameters:

* Kc = 0.6Ku
* τI = 0.5Pu  
* τD = 0.125Pu

Industrial Applications
-----------------------

CSTR Temperature Control
^^^^^^^^^^^^^^^^^^^^^^^^

For continuous stirred tank reactor temperature control via cooling water:

**Process Characteristics:**

* Gain: -2.5 K per L/min cooling water
* Dead time: 0.8 minutes (sensor + valve delays)
* Time constant: 12 minutes (thermal mass)

**ZN Tuning Results:**

* Kc = 1.2(12)/(2.5×0.8) = 7.2 (L/min)/K
* τI = 2(0.8) = 1.6 minutes
* τD = 0.5(0.8) = 0.4 minutes

Distillation Column Composition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For distillation top composition control via reflux ratio:

**Process Characteristics:**

* Gain: 0.8 mol% per reflux ratio change
* Dead time: 4 minutes (analyzer delay)
* Time constant: 25 minutes (tray dynamics)

**ZN Tuning Results:**

* Kc = 1.2(25)/(0.8×4) = 9.4
* τI = 2(4) = 8 minutes  
* τD = 0.5(4) = 2 minutes

Implementation Example
----------------------

.. code-block:: python

   from sproclib.controller.tuning import ZieglerNicholsTuning
   
   # Step response data from heat exchanger
   step_data = {
       'time': time_vector,
       'output': temperature_response,
       'input_change': 5.0,  # kg/h steam step
       'output_change': 16.0  # °C temperature rise
   }
   
   # Apply Ziegler-Nichols tuning
   zn_tuner = ZieglerNicholsTuning()
   pid_params = zn_tuner.tune_from_step_response(step_data)
   
   print(f"ZN Tuning Results:")
   print(f"Kc = {pid_params['Kc']:.2f} (kg/h)/°C")  
   print(f"τI = {pid_params['tau_I']:.1f} minutes")
   print(f"τD = {pid_params['tau_D']:.1f} minutes")

Performance Characteristics
---------------------------

**Typical Performance Metrics:**

* Rise time: 1.5-2.5 minutes (temperature loops)
* Overshoot: 10-25% (aggressive tuning)
* Settling time: 4-8 time constants
* Steady-state error: <2% with integral action

**Economic Impact:**

* Energy efficiency: 5-12% savings in utility costs
* Product quality: Reduced variability improves yield
* Equipment protection: Smooth control reduces wear

Design Guidelines
-----------------

**Step Response Method:**

1. **Perform Step Test:**
   - Apply 5-10% step change in manual mode
   - Record response for 3-5 time constants
   - Ensure step is large enough for good signal-to-noise ratio

2. **Identify Parameters:**
   - Draw tangent line at inflection point
   - Measure L (x-intercept) and T (slope)
   - Calculate Kp from steady-state gain

3. **Calculate PID Parameters:**
   - Use ZN formulas for initial tuning
   - Fine-tune based on performance requirements

**Tuning Modifications:**

For conservative tuning (safety-critical processes):

* Kc = 0.8(ZN value) - Reduce aggressiveness
* τI = 1.5(ZN value) - Slower integral action  
* τD = 0.5(ZN value) - Less derivative action

For PI-only tuning (noisy measurements):

* Use ZN PI formulas: Kc = 0.9T/(KpL), τI = 3.3L
* Eliminates derivative kick and noise amplification
* Suitable for composition and temperature loops

See Also
--------

* :doc:`AMIGOTuning` - Advanced constrained optimization tuning
* :doc:`RelayTuning` - Automatic relay-based tuning
* :doc:`../pid/PIDController` - PID controller implementation

References
----------

1. Ziegler, J. G., & Nichols, N. B. (1942). Optimum settings for automatic controllers. *Transactions of the ASME*, 64(11), 759-768.

2. Åström, K. J., & Hägglund, T. (2006). *Advanced PID Control*. ISA.

3. Cohen, G. H., & Coon, G. A. (1953). Theoretical consideration of retarded control. *Transactions of the ASME*, 75, 827-834.
