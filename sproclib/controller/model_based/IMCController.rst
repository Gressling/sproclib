IMCController
=============

.. currentmodule:: sproclib.controller.model_based

The :class:`IMCController` implements Internal Model Control (IMC), a model-based control strategy that provides excellent setpoint tracking and smooth control action for chemical process systems. IMC is particularly effective for processes with significant dead time and provides a systematic design procedure with a single tuning parameter.

Theory and Applications
-----------------------

Internal Model Control is based on the principle of using an internal model of the process to predict its behavior and calculate the required control action. The approach is especially valuable in chemical engineering applications where:

* **Process models are available** - From first principles or system identification
* **Smooth control action is required** - To avoid equipment stress and wear
* **Dead time is significant** - IMC handles time delays naturally
* **Model uncertainty exists** - Built-in robustness to model mismatch

Mathematical Foundation
^^^^^^^^^^^^^^^^^^^^^^^

The IMC structure uses an internal model Gm(s) in parallel with the actual process Gp(s):

.. math::

   Q(s) = G_m^{-1}(s) \cdot f(s)

Where:

* :math:`Q(s)` - IMC controller
* :math:`G_m^{-1}(s)` - Internal model inverse  
* :math:`f(s)` - IMC filter for robustness and realizability

**Filter Design**

The IMC filter is typically chosen as:

.. math::

   f(s) = \frac{1}{(\lambda s + 1)^n}

Where:

* :math:`\lambda` - Filter time constant (only tuning parameter)
* :math:`n` - Relative degree (difference between denominator and numerator orders)

**Equivalent PID Form**

For a First-Order Plus Dead Time (FOPDT) process:

.. math::

   G_p(s) = \frac{K_p e^{-\theta_p s}}{\tau_p s + 1}

The equivalent PID parameters are:

.. math::

   K_c = \frac{\tau_p}{K_p(\lambda + \theta_p)}
   
   \tau_I = \tau_p
   
   \tau_D = 0

Control Design Methodology
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Step 1: Process Model Identification**

Identify the process as FOPDT using step testing:

* Process gain (Kp): Steady-state change in output per unit input
* Time constant (τp): Time to reach 63.2% of final value  
* Dead time (θp): Apparent time delay in response

**Step 2: Model Factorization**

Factor the process model into invertible and non-invertible parts:

.. math::

   G_p(s) = G_p^+(s) \cdot G_p^-(s)

Where:

* :math:`G_p^+(s)` - Invertible part (minimum phase)
* :math:`G_p^-(s)` - Non-invertible part (dead time, RHP zeros)

**Step 3: Controller Calculation**

.. math::

   Q(s) = \frac{1}{G_p^+(s)} \cdot f(s)

The dead time and any right-half-plane zeros remain in the non-invertible part.

**Step 4: Filter Tuning**

Select λ based on performance-robustness tradeoff:

* Small λ: Fast response, less robust
* Large λ: Slow response, more robust

Class Reference
---------------

.. autoclass:: IMCController
   :members:
   :undoc-members:
   :show-inheritance:

Industrial Applications
-----------------------

Heat Exchanger Temperature Control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IMC excels in heat exchanger applications where:

* **Process**: Shell-and-tube heat exchanger with steam heating
* **Objective**: Control outlet temperature by manipulating steam flow
* **Challenges**: Thermal time constant, measurement delays

**Typical System Characteristics:**

* Process gain: 2-5 °C per kg/h steam flow
* Time constant: 10-30 minutes (thermal mass)
* Dead time: 1-5 minutes (sensor location, measurement filter)

**IMC Benefits:**

* Smooth steam valve operation
* No derivative kick on setpoint changes
* Natural handling of measurement delays
* Excellent setpoint tracking

Distillation Column Control
^^^^^^^^^^^^^^^^^^^^^^^^^^^

For distillation composition control:

* **Inputs**: Reflux ratio, reboiler duty
* **Outputs**: Top/bottom product compositions
* **Model**: High-order with significant dead time

**Design Considerations:**

* Large time constants (10-60 minutes)
* Composition analyzer delays (2-10 minutes)  
* Strong interaction between top and bottom loops
* Economic optimization requirements

**IMC Advantages:**

* Single tuning parameter per loop
* Inherent integral action for offset elimination
* Smooth control action preserves column efficiency
* Robust to composition analyzer noise

Reactor Temperature Control
^^^^^^^^^^^^^^^^^^^^^^^^^^^

For exothermic reactor systems:

* **Process**: Continuous stirred tank reactor (CSTR)
* **Control**: Temperature via cooling water flow
* **Safety**: Prevent thermal runaway

**Process Characteristics:**

* Negative process gain (cooling reduces temperature)
* Fast reaction dynamics
* Safety-critical operation

**Implementation:**

.. code-block:: python

   # Reactor temperature control example
   reactor_model = {
       'gain': -1.5,      # K per m³/h cooling (negative)
       'time_constant': 8.0,  # minutes
       'dead_time': 1.0,      # minutes
       'type': 'FOPDT'
   }
   
   controller = IMCController(
       process_model=reactor_model,
       filter_time_constant=4.0,  # Conservative tuning
       name="ReactorTempIMC"
   )

Design Guidelines
-----------------

Process Model Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Model Accuracy:**

* Process gain: ±20% accuracy acceptable
* Time constant: ±30% accuracy acceptable  
* Dead time: ±1 time unit critical for performance

**Model Validation:**

.. code-block:: python

   # Validate model with step test data
   model_response = simulate_fopdt(Kp, tau_p, theta_p, step_input)
   actual_response = process_step_test_data
   
   # Calculate fit quality
   fit_error = np.mean((model_response - actual_response)**2)
   print(f"Model fit error: {fit_error:.3f}")

Filter Time Constant Selection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Tuning Guidelines:**

1. **Conservative Tuning**: λ = τp
   
   - Good robustness to model uncertainty
   - Slower response
   - Recommended for safety-critical applications

2. **Moderate Tuning**: λ = τp/2
   
   - Balanced performance-robustness tradeoff
   - Most common industrial choice
   - Good starting point for tuning

3. **Aggressive Tuning**: λ = θp
   
   - Fast response
   - Requires accurate model
   - May cause control valve wear

**Process-Specific Guidelines:**

.. code-block:: python

   # Temperature control (thermal processes)
   if process_type == "temperature":
       lambda_c = tau_p / 2  # Moderate tuning
   
   # Composition control (slow processes)  
   elif process_type == "composition":
       lambda_c = tau_p      # Conservative tuning
   
   # Flow/pressure control (fast processes)
   elif process_type == "flow":
       lambda_c = theta_p    # Can be more aggressive

Robustness Analysis
^^^^^^^^^^^^^^^^^^^

**Model Uncertainty Effects:**

IMC provides good robustness to model mismatch, but performance degrades with:

* **Gain Error**: ±50% acceptable for stability
* **Time Constant Error**: ±100% acceptable  
* **Dead Time Error**: ±50% strongly affects performance

**Robustness Measures:**

.. code-block:: python

   # Calculate robustness metrics
   def robustness_analysis(nominal_model, uncertainty_bounds):
       # Maximum sensitivity
       Ms_max = calculate_max_sensitivity(nominal_model, uncertainty_bounds)
       
       # Gain margin
       GM = calculate_gain_margin(nominal_model)
       
       # Phase margin  
       PM = calculate_phase_margin(nominal_model)
       
       return {'Ms': Ms_max, 'GM': GM, 'PM': PM}

Implementation Considerations
-----------------------------

Real-Time Implementation
^^^^^^^^^^^^^^^^^^^^^^^^

**Computational Requirements:**

* Low computational load (simple PI equivalent)
* Suitable for distributed control systems (DCS)
* Fast sampling possible (limited by process dynamics)

**Initialization:**

.. code-block:: python

   # Initialize IMC controller
   def initialize_imc_controller(process_model, lambda_c):
       controller = IMCController(
           process_model=process_model,
           filter_time_constant=lambda_c
       )
       
       # Set initial conditions
       controller.reset()
       
       return controller

Anti-Windup Protection
^^^^^^^^^^^^^^^^^^^^^^

For processes with actuator constraints:

.. code-block:: python

   # Implement anti-windup for IMC
   def update_with_antiwindup(controller, setpoint, measurement, 
                             control_limits):
       # Calculate unconstrained control output
       u_ideal = controller.update(setpoint, measurement)
       
       # Apply constraints
       u_actual = np.clip(u_ideal, control_limits[0], control_limits[1])
       
       # Anti-windup compensation
       if u_actual != u_ideal:
           controller.apply_antiwindup_correction(u_actual - u_ideal)
       
       return u_actual

Safety Integration
^^^^^^^^^^^^^^^^^^

**Alarm Management:**

* High/low controller output alarms
* Model validity monitoring
* Sensor failure detection

**Backup Control:**

.. code-block:: python

   # Backup control strategy
   def safe_control_update(imc_controller, pid_backup, setpoint, measurement):
       try:
           # Try IMC control
           if imc_controller.is_valid():
               return imc_controller.update(setpoint, measurement)
           else:
               # Fall back to PID
               return pid_backup.update(setpoint, measurement)
       except Exception as e:
           # Emergency fallback
           return calculate_safe_output(measurement)

Performance Monitoring
----------------------

Key Performance Indicators
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Control Performance:**

* Integral Absolute Error (IAE)
* Settling time
* Overshoot percentage
* Control variability

**Economic Performance:**

* Energy consumption
* Product quality consistency
* Equipment wear
* Maintenance costs

**Monitoring Implementation:**

.. code-block:: python

   # Real-time performance monitoring
   class IMCPerformanceMonitor:
       def __init__(self):
           self.iae_window = []
           self.settling_times = []
           
       def update(self, setpoint, measurement, control_output):
           # Calculate current error
           error = abs(setpoint - measurement)
           self.iae_window.append(error)
           
           # Limit window size
           if len(self.iae_window) > 100:
               self.iae_window.pop(0)
           
           # Calculate metrics
           current_iae = np.mean(self.iae_window)
           
           return {'IAE': current_iae, 'error': error}

Troubleshooting Guide
---------------------

Common Issues and Solutions
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Poor Setpoint Tracking:**

* Check model accuracy (especially gain and dead time)
* Verify sensor calibration
* Consider decreasing λ (more aggressive tuning)

**Oscillatory Response:**

* Model may have incorrect dead time
* λ may be too small (increase for more filtering)
* Check for external disturbances

**Slow Response:**

* λ may be too large (decrease for faster response)  
* Process model time constant may be overestimated
* Verify actuator is not saturating

**Control Valve Wear:**

* λ too small causing excessive control action
* Add rate limiting to control output
* Consider measurement filtering

Example Implementation
----------------------

Complete Heat Exchanger Control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import numpy as np
   from sproclib.controller.model_based import IMCController
   
   # Define heat exchanger model from step test
   heat_exchanger_model = {
       'gain': 3.2,           # °C per kg/h steam
       'time_constant': 15.0, # minutes
       'dead_time': 3.0,      # minutes  
       'type': 'FOPDT'
   }
   
   # Design IMC controller
   lambda_c = heat_exchanger_model['time_constant'] / 2  # Moderate tuning
   
   controller = IMCController(
       process_model=heat_exchanger_model,
       filter_time_constant=lambda_c,
       name="HeatExchangerIMC"
   )
   
   # Control loop
   setpoint = 180.0  # °C target temperature
   
   for t in time_vector:
       # Get process measurement
       current_temp = temperature_sensor.read()
       
       # Calculate control action
       steam_flow = controller.update(t, setpoint, current_temp)
       
       # Apply constraints
       steam_flow = np.clip(steam_flow, 10.0, 100.0)  # kg/h limits
       
       # Send to actuator
       steam_valve.set_flow(steam_flow)

Advanced Features
^^^^^^^^^^^^^^^^^

**Feedforward Control:**

.. code-block:: python

   # Add feedforward for measured disturbances
   def imc_with_feedforward(controller, setpoint, measurement, disturbance):
       # IMC feedback control
       feedback_output = controller.update(setpoint, measurement)
       
       # Feedforward compensation
       feedforward_output = calculate_feedforward(disturbance)
       
       # Combine outputs
       total_output = feedback_output + feedforward_output
       
       return total_output

**Adaptive Tuning:**

.. code-block:: python

   # Adaptive filter time constant
   def adaptive_lambda(controller, performance_metrics):
       current_iae = performance_metrics['IAE']
       
       if current_iae > 1.2 * target_iae:
           # Decrease lambda for faster response
           new_lambda = controller.filter_time_constant * 0.9
           controller.set_filter_time_constant(new_lambda)
       elif current_iae < 0.8 * target_iae:
           # Increase lambda for smoother control
           new_lambda = controller.filter_time_constant * 1.1  
           controller.set_filter_time_constant(new_lambda)

See Also
--------

* :doc:`../pid/PIDController` - Traditional PID control
* :doc:`../state_space/StateSpaceController` - State-space control
* :doc:`../tuning/index` - Controller tuning methods
* :doc:`../../optimization/index` - Process optimization

References
----------

1. Morari, M., & Zafiriou, E. (1989). *Robust Process Control*. Prentice Hall.

2. Rivera, D. E., Morari, M., & Skogestad, S. (1986). Internal model control: PID controller design. *Industrial & Engineering Chemistry Process Design and Development*, 25(1), 252-265.

3. Seborg, D. E., Edgar, T. F., Mellichamp, D. A., & Doyle III, F. J. (2016). *Process Dynamics and Control*. John Wiley & Sons.

4. Ogunnaike, B. A., & Ray, W. H. (1994). *Process Dynamics, Modeling, and Control*. Oxford University Press.
