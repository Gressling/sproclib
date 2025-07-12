Control Systems
===============

The control systems documentation covers control algorithms, tuning methods, and controller implementations in SPROCLIB.

.. toctree::
   :maxdepth: 2

   control_overview
   pid_controllers
   advanced_control
   tuning_methods
   state_space_control
   model_predictive_control
   controller_examples

Overview
--------

The controller package provides comprehensive control system design and implementation tools for chemical processes. This includes:

* **PID Controllers**: Classical and enhanced PID implementations
* **Advanced Control**: Model-based and adaptive control strategies  
* **Tuning Methods**: Various tuning techniques for optimal performance
* **State-Space Control**: Modern control theory implementations
* **Model Predictive Control**: Advanced multivariable control

Key Features
------------

**PID Control**
  * Standard PID implementation with anti-windup
  * Enhanced PID with derivative filtering
  * Cascade and feedforward control structures

**Advanced Controllers**
  * Internal Model Control (IMC)
  * Smith Predictor for dead-time compensation
  * Adaptive and self-tuning controllers

**Tuning Methods**
  * Ziegler-Nichols tuning rules
  * AMIGO and Lambda tuning
  * Relay auto-tuning procedures

**State-Space Methods**
  * Linear quadratic regulators (LQR)
  * State observers and estimators
  * Pole placement techniques

**Model Predictive Control**
  * Linear MPC formulations
  * Constraint handling
  * Economic optimization integration

Applications
------------

* Process control loop design
* Multivariable control systems
* Advanced process control (APC)
* Controller performance monitoring
* Control system optimization

Getting Started
---------------

For basic PID control::

    from sproclib.controller.pid import PIDController
    from sproclib.controller.tuning import ZieglerNicholsTuning
    
    # Tune controller
    tuner = ZieglerNicholsTuning(method='ultimate_gain')
    params = tuner.calculate_parameters({'K': 2.0, 'tau': 5.0, 'theta': 1.0})
    
    # Create PID controller
    pid = PIDController(Kp=params['Kp'], Ki=params['Ki'], Kd=params['Kd'])
    
    # Calculate control action
    output = pid.calculate(setpoint=75.0, process_variable=70.0, dt=0.1)

For advanced control::

    from sproclib.controller.model_based import IMCController
    
    # Create IMC controller
    imc = IMCController(process_model={'K': 2.0, 'tau': 5.0, 'theta': 1.0})
    
    # Configure controller
    imc.set_tuning_parameter(lambda_c=5.0)

See Also
--------

* :doc:`../api/controllers_package` - Complete API reference
* :doc:`../analysis/index` - System analysis tools for controller design
* :doc:`../unit/index` - Unit operations with integrated control
* :doc:`../plant/index` - Plant-level control strategies
