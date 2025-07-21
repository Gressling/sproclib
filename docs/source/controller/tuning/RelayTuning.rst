RelayTuning
===========

.. currentmodule:: sproclib.controller.tuning

The :class:`RelayTuning` class implements relay-based auto-tuning methods for PID controllers in chemical process systems. This approach uses relay feedback to automatically identify critical process characteristics and calculate optimal PID parameters without requiring manual step tests or process models.

.. autoclass:: RelayTuning
   :members:
   :undoc-members:
   :show-inheritance:

Theory and Applications
-----------------------

Relay auto-tuning, pioneered by Åström and Hägglund in 1984, revolutionized industrial controller tuning by providing:

- **Automated parameter identification** without operator intervention
- **Continuous operation** during tuning process
- **Robust identification** even with process noise and disturbances
- **Safety through controlled oscillation** with bounded amplitude

The method is particularly valuable in chemical engineering where:

- **Manual tuning is time-consuming** and requires skilled operators
- **Process models are unavailable** or uncertain
- **Safety requirements** prevent large process upsets
- **Continuous operation** must be maintained during tuning

Mathematical Foundation
^^^^^^^^^^^^^^^^^^^^^^^

**Relay Feedback Principle**

The relay creates controlled oscillations by switching the controller output between two levels based on the process variable:

.. math::

   u(t) = u_0 + d \times \text{sign}(e(t))

Where:

* u₀ = Bias level (typically current operating point)
* d = Relay amplitude (tuning parameter)
* e(t) = Error signal (setpoint - measurement)

**Critical Point Identification**

From the sustained oscillation:

* Ultimate gain: Ku = 4d/(π×a)
* Ultimate period: Pu = oscillation period
* Ultimate frequency: ωu = 2π/Pu

Where 'a' is the amplitude of process variable oscillation.

**PID Parameter Calculation**

Using Ziegler-Nichols equivalent relationships:

* Kc = 0.6 × Ku (proportional gain)
* τI = 0.5 × Pu (integral time)
* τD = 0.125 × Pu (derivative time)

Advanced Relay Methods
^^^^^^^^^^^^^^^^^^^^^^

**Asymmetric Relay**

For processes with asymmetric behavior:

.. math::

   u(t) = \begin{cases}
   u_0 + d_1 & \text{when } e(t) > 0 \\
   u_0 - d_2 & \text{when } e(t) < 0
   \end{cases}

**Relay with Hysteresis**

To reduce noise sensitivity:

* Switch up when e(t) > +ε
* Switch down when e(t) < -ε

Where ε is the hysteresis band.

Industrial Applications
-----------------------

CSTR Temperature Control
^^^^^^^^^^^^^^^^^^^^^^^^

For continuous stirred tank reactor with exothermic reaction:

**Process Characteristics:**

* Temperature range: 320-380 K
* Control via cooling water flow
* Safety-critical (thermal runaway risk)

**Relay Test Configuration:**

* Relay amplitude: ±2 L/min (5% of maximum flow)
* Hysteresis: ±0.5 K (noise reduction)
* Test duration: 3-4 oscillation cycles

**Typical Results:**

* Ultimate gain: Ku = 8.5 (L/min)/K
* Ultimate period: Pu = 12 minutes
* PID parameters: Kc = 5.1, τI = 6.0 min, τD = 1.5 min

**Safety Benefits:**

* Controlled oscillation amplitude (±3 K)
* Automatic termination if bounds exceeded
* Continuous monitoring of reaction conditions

Distillation Column Composition Control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For top composition control via reflux ratio:

**Process Challenges:**

* Long dead times (5-15 minutes)
* Measurement noise from gas chromatograph
* Strong interaction with bottom composition loop

**Relay Configuration:**

* Asymmetric relay (composition control is directional)
* d₁ = +0.2 reflux ratio increase
* d₂ = -0.1 reflux ratio decrease
* Hysteresis: ±0.2 mol% (GC noise tolerance)

**Identification Results:**

* Ku = 12.3 (reflux ratio change per mol%)
* Pu = 25 minutes (includes analyzer delay)
* Modified tuning for robustness: Kc = 0.4×Ku = 4.9

**Performance Improvements:**

* 40% faster disturbance rejection vs. manual tuning
* Reduced composition variance by 60%
* Improved separation efficiency

Implementation Example
----------------------

.. code-block:: python

   from sproclib.controller.tuning import RelayTuning
   
   # Configure relay test for heat exchanger
   relay_tuner = RelayTuning()
   relay_tuner.configure_test(
       amplitude_percent=5.0,    # 5% of operating range
       hysteresis=0.5,          # 0.5°C noise band
       test_duration_cycles=4    # 4 complete oscillations
   )
   
   # Execute automatic tuning
   tuning_results = relay_tuner.execute_auto_tuning()
   
   print(f"Relay tuning completed:")
   print(f"Ultimate gain: {tuning_results['Ku']:.2f}")
   print(f"Ultimate period: {tuning_results['Pu']:.1f} minutes")
   print(f"PID parameters:")
   print(f"  Kc = {tuning_results['Kc']:.2f}")
   print(f"  τI = {tuning_results['tau_I']:.1f} minutes")
   print(f"  τD = {tuning_results['tau_D']:.1f} minutes")

Automated Implementation
------------------------

**Relay Test Execution:**

.. code-block:: python

   class RelayAutoTuner:
       def __init__(self, process_interface):
           self.process = process_interface
           self.relay_amplitude = 0.0
           self.hysteresis = 0.0
           self.test_active = False
           
       def configure_test(self, amplitude_pct, hysteresis_units):
           """Configure relay test parameters"""
           operating_range = self.process.get_operating_range()
           self.relay_amplitude = operating_range * amplitude_pct / 100
           self.hysteresis = hysteresis_units
           
       def execute_relay_test(self, duration_cycles=4):
           """Execute automated relay test"""
           # Initialize test conditions
           start_output = self.process.get_current_output()
           setpoint = self.process.get_setpoint()
           
           # Test execution with safety monitoring
           cycle_count = 0
           while cycle_count < duration_cycles and self.test_active:
               # Relay logic with hysteresis
               pv = self.process.read_measurement()
               error = setpoint - pv
               
               if error > self.hysteresis:
                   output = start_output + self.relay_amplitude
               elif error < -self.hysteresis:
                   output = start_output - self.relay_amplitude
               else:
                   output = start_output  # Dead zone
                   
               # Apply with safety checks
               if self.check_safety_limits(pv, output):
                   self.process.set_output(output)
               else:
                   self.terminate_test("Safety limit exceeded")
                   break

Design Guidelines
-----------------

**Test Configuration:**

Relay Amplitude Selection:

* Temperature processes: d = 2-5% of normal operating range
* Composition processes: d = 0.1-0.5% of specification range
* Pressure/flow processes: d = 1-3% of operating range

Hysteresis Selection:

* General rule: ε = 2-3 × measurement noise level
* Temperature: ε = 0.5-2 °C
* Composition: ε = 0.1-0.5 mol%
* Pressure: ε = 0.02-0.1 bar

**Safety Protocols:**

Pre-Test Verification:

* Confirm process at steady state
* Check all safety interlocks active
* Verify manual control capability
* Set emergency stop conditions

Test Monitoring:

* Continuous operator oversight
* Automatic amplitude limiting
* Oscillation bounds checking
* Emergency termination triggers

Performance Benefits
--------------------

**Economic Impact:**

Tuning Time Reduction:

* Manual tuning: 4-8 hours per loop
* Relay auto-tuning: 20-60 minutes per loop
* Time savings: 80-90% reduction

Performance Improvements:

* Settling time: 20-40% faster
* Overshoot: 30-50% reduction
* Energy consumption: 5-15% decrease
* Product quality variance: 25-60% reduction

**Return on Investment:**

Typical Chemical Plant (100 control loops):

Implementation costs:

* Software integration: $50,000
* Engineering time: $30,000
* Commissioning: $20,000
* Total: $100,000

Annual benefits:

* Energy savings: $200,000
* Quality improvements: $300,000
* Maintenance reduction: $100,000
* Operator productivity: $150,000
* Total: $750,000

**ROI: 650% first year**

Advanced Features
-----------------

**Multivariable Relay Tuning:**

.. code-block:: python

   def sequential_relay_tuning(loop_list, interaction_matrix):
       """Sequential relay tuning for interacting loops"""
       
       tuned_parameters = {}
       
       for loop in loop_list:
           # Identify interaction effects
           interaction_level = calculate_interaction_strength(loop, interaction_matrix)
           
           # Adjust relay parameters for interaction
           adjusted_amplitude = base_amplitude * (1 - 0.3 * interaction_level)
           
           # Perform relay test
           test_results = execute_relay_test(loop, adjusted_amplitude)
           
           # Calculate detuned parameters
           raw_params = calculate_pid_from_relay(test_results)
           detuned_params = apply_interaction_detuning(raw_params, interaction_level)
           
           tuned_parameters[loop.name] = detuned_params
           
       return tuned_parameters

**Adaptive Relay Tuning:**

.. code-block:: python

   class AdaptiveRelayTuner:
       def __init__(self, retune_threshold=0.3):
           self.retune_threshold = retune_threshold
           self.last_tune_params = None
           self.performance_monitor = PerformanceMonitor()
           
       def monitor_and_retune(self, controller, process):
           """Monitor performance and retune when needed"""
           
           # Calculate current performance metrics
           current_performance = self.performance_monitor.assess(controller)
           
           # Check if retuning is needed
           if self.needs_retuning(current_performance):
               print("Performance degradation detected. Initiating relay retune...")
               
               # Execute new relay test
               new_params = self.execute_relay_test(process)
               
               # Smooth parameter transition
               smoothed_params = self.smooth_parameter_transition(
                   self.last_tune_params, new_params)
               
               # Update controller
               controller.update_parameters(smoothed_params)
               self.last_tune_params = smoothed_params
               
               return True
           
           return False

See Also
--------

* :doc:`ZieglerNicholsTuning` - Classic empirical tuning rules
* :doc:`AMIGOTuning` - Advanced constrained optimization tuning
* :doc:`../pid/PIDController` - PID controller implementation

References
----------

1. Åström, K. J., & Hägglund, T. (1984). Automatic tuning of simple regulators with specifications on phase and amplitude margins. *Automatica*, 20(5), 645-651.

2. Åström, K. J., & Hägglund, T. (2006). *Advanced PID Control*. ISA.

3. Yu, C. C. (2006). *Autotuning of PID Controllers: A Relay Feedback Approach*. Springer.

4. Hang, C. C., Åström, K. J., & Ho, W. K. (1991). Refinements of the Ziegler-Nichols tuning formula. *IEE Proceedings D-Control Theory and Applications*, 138(2), 111-118.
