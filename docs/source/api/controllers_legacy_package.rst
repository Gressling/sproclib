Controllers Legacy Package
==========================

.. note::
   This documentation covers the legacy controllers interface.
   
   **For new projects, use the modular controller package instead:**
   :doc:`controllers_package` - Modern modular controller structure
   
   The legacy interface is maintained for backward compatibility via the legacy package.

The controllers module provides control algorithms that work with all process units in the modular structure. These controllers can be applied to any process unit that follows the standard ProcessModel interface.
   
For examples of controller usage with process units, see:

* :doc:`../examples` - Comprehensive examples showing controller integration
* :doc:`units_package` - Process units that work with controllers
* :doc:`controllers_package` - Modern modular controller documentation

Controllers Documentation
-------------------------

.. automodule:: sproclib.legacy.controllers
   :members:
   :undoc-members:
   :show-inheritance:

PIDController
~~~~~~~~~~~~~

.. autoclass:: sproclib.legacy.controllers.PIDController
   :members:
   :special-members: __init__
   :show-inheritance:

The PIDController class implements a full-featured PID controller with:

* **Anti-windup protection** - Prevents integrator saturation
* **Bumpless transfer** - Smooth transitions between manual/auto modes  
* **Setpoint weighting** - Advanced setpoint tracking
* **Output limiting** - Configurable output constraints

Example Usage::

    from legacy.controllers import PIDController
    
    # Create controller with tuned parameters
    controller = PIDController(
        Kp=1.0, Ki=0.1, Kd=0.05,
        output_limits=(-100, 100),
        anti_windup=True
    )
    
    # Control loop
    for t in time_steps:
        error = setpoint - process_variable
        output = controller.update(setpoint, process_variable, dt=0.1)
        # Apply output to process...

TuningRule
~~~~~~~~~~

.. autoclass:: controllers.TuningRule
   :members:
   :special-members: __init__
   :show-inheritance:

The TuningRule class provides automated PID tuning methods:

* **Ziegler-Nichols** - Classic tuning rules for step response
* **AMIGO** - Advanced method for integrating processes
* **Relay Tuning** - Automatic tuning using relay feedback

Example Usage::

    from controllers import TuningRule
    
    # Create tuning rule object
    tuner = TuningRule()
    
    # Tune using Ziegler-Nichols method
    pid_params = tuner.ziegler_nichols(K=2.0, tau=5.0, theta=1.0)
    
    # Apply to controller
    controller = PIDController(**pid_params)

Methods
-------

Controller Methods
~~~~~~~~~~~~~~~~~~

.. automethod:: controllers.PIDController.update
.. automethod:: controllers.PIDController.reset
.. automethod:: controllers.PIDController.set_auto_mode
.. automethod:: controllers.PIDController.set_manual_mode

Tuning Methods
~~~~~~~~~~~~~~

.. automethod:: controllers.TuningRule.ziegler_nichols
.. automethod:: controllers.TuningRule.amigo
.. automethod:: controllers.TuningRule.relay_tuning

Advanced Features
-----------------

Anti-windup Protection
~~~~~~~~~~~~~~~~~~~~~~

The PID controller includes sophisticated anti-windup protection to prevent integrator saturation::

    controller = PIDController(
        Kp=1.0, Ki=0.1, Kd=0.05,
        anti_windup=True,
        output_limits=(-100, 100)
    )

When the controller output hits limits, the integrator is automatically adjusted to prevent windup.

Setpoint Weighting
~~~~~~~~~~~~~~~~~~

For processes sensitive to setpoint changes, setpoint weighting reduces overshoot::

    controller = PIDController(
        Kp=1.0, Ki=0.1, Kd=0.05,
        setpoint_weight_proportional=0.6,
        setpoint_weight_derivative=0.0
    )

This creates a "softer" response to setpoint changes while maintaining disturbance rejection.

Bumpless Transfer
~~~~~~~~~~~~~~~~~

Smooth transitions between manual and automatic modes::

    # Switch to manual mode
    controller.set_manual_mode(manual_output=50.0)
    
    # Later, switch back to auto (no output bump)
    controller.set_auto_mode()

Performance Considerations
--------------------------

* Use appropriate sample times (typically 1/10th to 1/4th of the process time constant)
* Tune controllers based on process characteristics, not just trial and error
* Consider using derivative filtering for noisy measurements
* Implement proper exception handling for control loops

See Also
--------

* :doc:`models_legacy_package` - Process models for control design
* :doc:`functions_legacy_package` - Utility functions including tune_pid()
* :doc:`../theory` - Control theory background
