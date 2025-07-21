StateSpaceController
==================

.. currentmodule:: sproclib.controller.state_space

The :class:`StateSpaceController` provides advanced multivariable control capabilities using state-space representation for chemical process systems. This controller is particularly effective for Multiple-Input Multiple-Output (MIMO) systems commonly found in chemical engineering applications.

Theory and Applications
-----------------------

State-space control theory provides a systematic framework for designing controllers for multivariable systems. The approach is particularly valuable in chemical engineering where processes often exhibit:

* **Multiple coupled variables** - Temperature, pressure, concentration, flow rates
* **Complex dynamics** - Time delays, non-minimum phase behavior  
* **Optimization requirements** - Energy efficiency, product quality, safety constraints

Mathematical Foundation
^^^^^^^^^^^^^^^^^^^^^^^

The state-space representation of a chemical process is given by:

.. math::

   \dot{x}(t) = Ax(t) + Bu(t) + Gd(t)
   
   y(t) = Cx(t) + Du(t) + Hd(t)

Where:

* :math:`x(t)` - State vector (concentrations, temperatures, holdups)
* :math:`u(t)` - Control input vector (flow rates, heating/cooling duties)
* :math:`y(t)` - Measured output vector (sensor readings)
* :math:`d(t)` - Disturbance vector (feed composition, ambient conditions)

The controller design objectives include:

1. **Stability** - Ensuring closed-loop system stability
2. **Performance** - Meeting setpoint tracking and disturbance rejection specifications
3. **Robustness** - Maintaining performance under model uncertainty
4. **Optimality** - Minimizing economic cost functions

Control Design Methods
^^^^^^^^^^^^^^^^^^^^^^

**Linear Quadratic Regulator (LQR)**

The LQR design minimizes the quadratic cost function:

.. math::

   J = \int_0^{\infty} [x^T Q x + u^T R u] dt

Where Q and R are positive definite weighting matrices that allow tuning of state regulation vs. control effort.

**Pole Placement**

Direct assignment of closed-loop poles to achieve desired dynamic characteristics such as:

* Settling time specifications
* Damping requirements  
* Stability margins

**Observer Design**

For unmeasured states, Luenberger observers estimate the full state vector:

.. math::

   \dot{\hat{x}} = A\hat{x} + Bu + L(y - C\hat{x})

The observer gain L is designed to ensure fast and accurate state estimation.

Class Reference
---------------

.. autoclass:: StateSpaceController
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: StateSpaceModel
   :members:
   :undoc-members:
   :show-inheritance:

Industrial Applications
-----------------------

Distillation Column Control
^^^^^^^^^^^^^^^^^^^^^^^^^^^

State-space controllers excel in distillation applications where:

* **States**: Tray compositions, reflux drum level, reboiler level
* **Inputs**: Reflux ratio, reboiler duty, distillate flow
* **Outputs**: Top/bottom product compositions, temperatures

The multivariable nature allows coordinated control of product quality while maintaining material balance constraints.

**Typical System Dimensions:**

* 10-50 states (depending on number of trays)
* 2-4 manipulated variables  
* 2-6 controlled variables
* Strong coupling between temperature and composition loops

Reactor Network Control
^^^^^^^^^^^^^^^^^^^^^^^

For reactor systems with:

* **States**: Concentrations of species A, B, C, reactor temperature
* **Inputs**: Feed flow rates, cooling water flow, catalyst addition
* **Outputs**: Product concentration, temperature, conversion

The controller handles reaction kinetics coupling and heat integration between reactors.

Heat Exchanger Networks
^^^^^^^^^^^^^^^^^^^^^^^

Complex heat integration systems benefit from state-space control:

* **States**: Stream temperatures at various locations
* **Inputs**: Hot/cold fluid flow rates, bypass flows
* **Outputs**: Target temperatures, approach temperatures

The controller optimizes energy recovery while meeting process temperature requirements.

Design Guidelines
-----------------

System Analysis
^^^^^^^^^^^^^^^

Before controller design, analyze the process:

1. **Controllability Analysis**
   
   .. code-block:: python
   
      is_controllable = model.is_controllable()
      cond_number = np.linalg.cond(model.controllability_matrix())
   
   Controllability ensures that all states can be influenced by the available inputs.

2. **Observability Analysis**
   
   .. code-block:: python
   
      is_observable = model.is_observable()
      cond_number = np.linalg.cond(model.observability_matrix())
   
   Observability ensures that all states can be estimated from the available measurements.

3. **Stability Analysis**
   
   .. code-block:: python
   
      poles = model.poles()
      is_stable = model.is_stable()
   
   Open-loop stability affects controller design complexity.

Controller Tuning
^^^^^^^^^^^^^^^^^

**LQR Tuning Guidelines:**

* **Q Matrix**: Penalize important state deviations
  
  - High values for critical states (temperature, pressure)
  - Lower values for less critical states (intermediate concentrations)

* **R Matrix**: Penalize control effort
  
  - High values limit actuator usage (energy costs)
  - Low values allow aggressive control action

**Typical Chemical Process Values:**

.. code-block:: python

   # For temperature control (K)
   Q_temp = 1.0 / (5.0)**2  # 5K tolerance
   
   # For concentration control (mol/L)  
   Q_conc = 1.0 / (0.1)**2  # 0.1 mol/L tolerance
   
   # For flow control effort (kg/h)
   R_flow = 1.0 / (100.0)**2  # 100 kg/h effort limit

Safety Considerations
---------------------

State-space controllers require careful implementation in chemical processes:

**Constraint Handling**

* **State Constraints**: Temperature limits, pressure limits, concentration bounds
* **Input Constraints**: Valve limits, pump capacity, heating/cooling limits  
* **Rate Constraints**: Maximum rate of change for thermal equipment

**Failure Modes**

* **Sensor Failures**: Observer-based control can continue operation
* **Actuator Failures**: Reconfiguration using remaining inputs
* **Model Mismatch**: Robust design techniques address uncertainty

**Implementation Requirements**

* **Sampling Rate**: Fast enough to capture process dynamics (typically 1-10x process time constant)
* **Computational Load**: Real-time matrix operations for large systems
* **Backup Control**: Fallback to simpler controllers if computation fails

Economic Benefits
-----------------

State-space control provides economic advantages:

**Energy Savings**

* Optimal coordination of heating and cooling utilities
* Reduced energy consumption through better disturbance rejection
* Typical savings: 5-15% of energy costs

**Product Quality**

* Tighter control of product specifications
* Reduced off-specification product
* Higher product value and reduced waste

**Equipment Protection**

* Reduced cycling and wear on expensive equipment
* Extended equipment life through smooth operation
* Lower maintenance costs

Example Implementation
----------------------

Basic Controller Setup
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import numpy as np
   from sproclib.controller.state_space import StateSpaceController, StateSpaceModel
   
   # Define CSTR system matrices
   A = np.array([[-0.5, -0.1],    # Concentration and temperature dynamics  
                 [0.2, -0.3]])     # Reaction coupling
   
   B = np.array([[0.8, 0.0],      # Flow and cooling inputs
                 [0.0, 0.6]])
   
   C = np.array([[1.0, 0.0],      # Concentration measurement
                 [0.0, 1.0]])      # Temperature measurement
   
   D = np.zeros((2, 2))
   
   # Create model and controller
   model = StateSpaceModel(A, B, C, D,
                          state_names=['CA', 'T'],
                          input_names=['Flow', 'Cooling'],
                          output_names=['CA_out', 'T_out'])
   
   controller = StateSpaceController(model, name="CSTR_Controller")

LQR Design Example
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Design LQR controller
   Q = np.diag([10.0, 1.0])   # State weights (concentration more important)
   R = np.diag([1.0, 0.5])    # Input weights (flow more expensive)
   
   try:
       K, S, poles = controller.design_lqr_controller(Q, R)
       print(f"LQR gain matrix K:\n{K}")
       print(f"Closed-loop poles: {poles}")
   except AttributeError:
       print("LQR design method not implemented")

Control Loop Implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Control loop execution
   dt = 0.1  # 6-second sampling (10 samples/minute)
   
   for t in time_vector:
       # Get measurements
       measurements = process.get_measurements()
       
       # Set controller setpoints
       setpoints = np.array([target_concentration, target_temperature])
       
       # Calculate control action
       control_output = controller.update(t, setpoints, measurements)
       
       # Apply to process
       process.set_inputs(control_output)

Performance Analysis
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Analyze controller performance
   print("\n=== Controller Performance Analysis ===")
   
   # System properties
   print(f"Controllable: {model.is_controllable()}")
   print(f"Observable: {model.is_observable()}")
   print(f"Stable: {model.is_stable()}")
   
   # Performance metrics
   settling_time = calculate_settling_time(response)
   overshoot = calculate_overshoot(response)
   iae = calculate_iae(error_signal)
   
   print(f"Settling time: {settling_time:.1f} minutes")
   print(f"Overshoot: {overshoot:.1f}%")
   print(f"IAE: {iae:.3f}")

See Also
--------

* :doc:`../pid/PIDController` - Single-loop PID control
* :doc:`../model_based/IMCController` - Internal model control
* :doc:`../tuning/index` - Controller tuning methods
* :doc:`../../optimization/index` - Process optimization tools

References
----------

1. Skogestad, S., & Postlethwaite, I. (2005). *Multivariable Feedback Control: Analysis and Design*. John Wiley & Sons.

2. Ogunnaike, B. A., & Ray, W. H. (1994). *Process Dynamics, Modeling, and Control*. Oxford University Press.

3. Stephanopoulos, G. (1984). *Chemical Process Control: An Introduction to Theory and Practice*. Prentice Hall.

4. Rawlings, J. B., Mayne, D. Q., & Diehl, M. (2017). *Model Predictive Control: Theory, Computation, and Design*. Nob Hill Publishing.
