Controller Tuning Methods
=========================

.. currentmodule:: sproclib.controller.tuning

This package provides systematic methods for tuning PID controllers in chemical process applications. Each method addresses different tuning scenarios and process characteristics.

Overview
--------

Controller tuning is critical for achieving optimal process performance while maintaining stability and robustness. The tuning methods in this package provide:

* **Empirical tuning rules** based on process step response
* **Frequency domain methods** using ultimate gain and period
* **Model-based optimization** with robustness constraints  
* **Automated tuning procedures** for continuous operation

Available Methods
-----------------

.. toctree::
   :maxdepth: 2

   ZieglerNicholsTuning
   AMIGOTuning  
   RelayTuning

Method Comparison
-----------------

.. list-table:: Tuning Method Characteristics
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Method
     - Test Required
     - Automation Level
     - Robustness
     - Best For
   * - Ziegler-Nichols
     - Step response or Ultimate gain
     - Manual
     - Moderate
     - Initial tuning, training
   * - AMIGO
     - Process model (FOPDT)
     - Semi-automatic
     - High
     - Production systems
   * - Relay Auto-tuning
     - Relay feedback test
     - Fully automatic
     - High
     - Routine retuning

Selection Guidelines
--------------------

**Use Ziegler-Nichols when:**

* Learning controller tuning fundamentals
* Quick initial tuning is needed
* Process model is not available
* Conservative performance is acceptable

**Use AMIGO when:**

* Process model (FOPDT) is available
* Optimal performance-robustness balance needed
* Dead time is significant (τ > 0.2)
* Production system requires reliable operation

**Use Relay Auto-tuning when:**

* Automatic tuning capability is required
* Process is in continuous operation
* Skilled operators are not available
* Periodic retuning is needed

Implementation Strategy
-----------------------

**Phase 1: Initial Tuning**

1. Use Ziegler-Nichols for baseline parameters
2. Validate stability and basic performance
3. Document initial settings

**Phase 2: Optimization**

1. Perform process identification for FOPDT model
2. Apply AMIGO tuning for optimal parameters  
3. Fine-tune based on specific performance requirements

**Phase 3: Automation**

1. Implement relay auto-tuning capability
2. Set up automatic performance monitoring
3. Schedule periodic retuning as needed

Economic Impact
---------------

Proper controller tuning provides significant economic benefits:

**Energy Savings:**
* 5-15% reduction in utility consumption
* Improved heat integration efficiency
* Reduced equipment cycling losses

**Product Quality:**
* 25-50% reduction in quality variance
* Fewer off-specification products  
* Improved yield and selectivity

**Operational Benefits:**
* Reduced operator workload
* Consistent performance across shifts
* Lower maintenance costs

Industrial Examples
-------------------

**Reactor Temperature Control:**

.. code-block:: python

   # Compare tuning methods for CSTR temperature control
   from sproclib.controller.tuning import ZieglerNicholsTuning, AMIGOTuning
   
   # Process parameters from step test
   process_model = {
       'Kp': -2.5,    # K per L/min cooling
       'T': 12.0,     # minutes
       'L': 0.8,      # minutes
       'type': 'FOPDT'
   }
   
   # Ziegler-Nichols tuning
   zn_tuner = ZieglerNicholsTuning()
   zn_params = zn_tuner.tune_from_model(process_model)
   
   # AMIGO tuning
   amigo_tuner = AMIGOTuning()
   amigo_params = amigo_tuner.tune(process_model, controller_type='PI')
   
   print("Tuning Comparison:")
   print(f"ZN:    Kc={zn_params['Kc']:.2f}, τI={zn_params['tau_I']:.1f}")
   print(f"AMIGO: Kc={amigo_params['Kc']:.2f}, τI={amigo_params['tau_I']:.1f}")

**Heat Exchanger Control:**

.. code-block:: python

   # Automated relay tuning for heat exchanger
   from sproclib.controller.tuning import RelayTuning
   
   # Configure relay test
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

Best Practices
--------------

**Safety First:**

* Always test tuning changes in safe operating regions
* Have manual control backup available
* Monitor safety interlocks during tuning tests
* Use conservative tuning for safety-critical loops

**Documentation:**

* Record all tuning parameters and test conditions
* Document performance before and after changes
* Maintain tuning history for trend analysis
* Share successful tuning approaches across similar processes

**Continuous Improvement:**

* Monitor controller performance metrics regularly
* Retune when process characteristics change
* Train operators on tuning fundamentals
* Implement automatic performance monitoring

See Also
--------

* :doc:`../pid/PIDController` - PID controller implementation
* :doc:`../model_based/IMCController` - Model-based control alternative
* :doc:`../state_space/StateSpaceController` - Multivariable control
* :doc:`../../optimization/index` - Advanced optimization methods

References
----------

1. Åström, K. J., & Hägglund, T. (2006). *Advanced PID Control*. ISA.

2. Hägglund, T., & Åström, K. J. (2004). Revisiting the Ziegler-Nichols step response method for PID control. *Journal of Process Control*, 14(6), 635-650.

3. Panagopoulos, H., Åström, K. J., & Hägglund, T. (2002). Design of PID controllers based on constrained optimisation. *IEE Proceedings-Control Theory and Applications*, 149(1), 32-40.

4. Yu, C. C. (2006). *Autotuning of PID Controllers: A Relay Feedback Approach*. Springer.
