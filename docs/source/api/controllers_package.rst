Controllers Package
===================

The controller package provides modular controller implementations for process control applications.

Overview
--------

The controller package is organized into the following subpackages:

* **base** - Abstract base classes for controllers and tuning rules
* **pid** - PID controller implementations  
* **tuning** - Various tuning methods for automated parameter selection
* **model_based** - Model-based controllers (IMC, etc.)
* **state_space** - State-space controllers for MIMO systems

Package Structure
-----------------

.. code-block:: text

   controller/
   ├── base/
   │   └── TuningRule.py          # Abstract base class for tuning rules
   ├── pid/
   │   └── PIDController.py       # Advanced PID controller
   ├── tuning/
   │   ├── ZieglerNicholsTuning.py   # Classic Ziegler-Nichols tuning
   │   ├── AMIGOTuning.py            # AMIGO robust tuning
   │   └── RelayTuning.py            # Relay auto-tuning
   ├── model_based/
   │   └── IMCController.py          # Internal Model Control
   └── state_space/
       └── StateSpaceController.py   # State-space MIMO control

Quick Start
-----------

**New Modular Imports (Recommended):**

.. code-block:: python

   from sproclib.controller.pid.PIDController import PIDController
   from sproclib.controller.tuning.ZieglerNicholsTuning import ZieglerNicholsTuning
   from sproclib.controller.model_based.IMCController import IMCController
   from sproclib.controller.state_space.StateSpaceController import StateSpaceController
   
   # Create and tune a PID controller
   tuner = ZieglerNicholsTuning(controller_type="PID")
   params = tuner.calculate_parameters({'K': 2.0, 'tau': 5.0, 'theta': 1.0})
   
   pid = PIDController(Kp=params['Kp'], Ki=params['Ki'], Kd=params['Kd'])
   
   # Or use advanced model-based control
   imc = IMCController(process_model={'K': 2.0, 'tau': 5.0, 'theta': 1.0})

Base Classes
------------

TuningRule Abstract Base Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: controller.base.TuningRule.TuningRule
   :members:
   :undoc-members:
   :show-inheritance:

The TuningRule class provides an abstract interface for all tuning methods.

PID Controllers
---------------

PIDController Class
~~~~~~~~~~~~~~~~~~~

.. autoclass:: controller.pid.PIDController.PIDController
   :members:
   :undoc-members:
   :show-inheritance:

Advanced PID controller with anti-windup, setpoint weighting, and bumpless transfer.

Tuning Methods
--------------

Ziegler-Nichols Tuning
~~~~~~~~~~~~~~~~~~~~~~

Classic tuning method based on step response characteristics.

.. autoclass:: controller.tuning.ZieglerNicholsTuning
   :members:
   :undoc-members:
   :show-inheritance:

AMIGO Tuning
~~~~~~~~~~~~

Advanced Method for Integrating and Generally Oscillating processes.

.. autoclass:: controller.tuning.AMIGOTuning
   :members:
   :undoc-members:
   :show-inheritance:

Relay Tuning
~~~~~~~~~~~~

Automatic tuning using relay feedback test.

.. autoclass:: controller.tuning.RelayTuning
   :members:
   :undoc-members:
   :show-inheritance:

Model-Based Controllers
-----------------------

The model_based package provides advanced control algorithms that use process models for improved performance.

Internal Model Control (IMC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: controller.model_based.IMCController.IMCController
   :members:
   :undoc-members:
   :show-inheritance:

Process Models for IMC
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: controller.model_based.IMCController.FOPDTModel
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: controller.model_based.IMCController.SOPDTModel
   :members:
   :undoc-members:
   :show-inheritance:

**Example:**

.. code-block:: python

   from sproclib.controller.model_based.IMCController import IMCController, FOPDTModel, tune_imc_lambda
   
   # Create process model
   model = FOPDTModel(K=2.0, tau=5.0, theta=1.0)
   
   # Auto-tune IMC filter parameter
   lambda_filter = tune_imc_lambda(model, response_time_factor=3.0)
   
   # Create IMC controller
   imc = IMCController(process_model=model, lambda_filter=lambda_filter)
   
   # Use in control loop
   for setpoint in setpoints:
       output = imc.compute(setpoint, measurement)

State-Space Controllers
-----------------------

The state_space package implements advanced MIMO control for complex process systems.

State-Space Control
~~~~~~~~~~~~~~~~~~~

.. autoclass:: controller.state_space.StateSpaceController.StateSpaceController
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: controller.state_space.StateSpaceController.StateSpaceModel
   :members:
   :undoc-members:
   :show-inheritance:

**Example:**

.. code-block:: python

   .. code-block:: python

   from sproclib.controller.state_space.StateSpaceController import StateSpaceController, StateSpaceModel
   import numpy as np
   
   # Define system matrices for a 2x2 MIMO system
   A = np.array([[-0.5, 0.2], [0.1, -0.8]])
   B = np.array([[1.0, 0.0], [0.0, 1.0]])
   C = np.array([[1.0, 0.0], [0.0, 1.0]])
   D = np.zeros((2, 2))
   
   # Create state-space model
   model = StateSpaceModel(A, B, C, D)
   
   # Design LQR controller
   Q = np.eye(2)  # State penalty
   R = np.eye(2)  # Input penalty
   
   controller = StateSpaceController(model)
   K = controller.design_lqr(Q, R)
   
   # Use in control loop
   x = np.array([0.0, 0.0])  # Initial state
   for setpoint in setpoints:
       u = controller.compute_lqr(setpoint, x, K)

Examples
--------

**Basic PID Control:**

.. code-block:: python

   from sproclib.controller.pid.PIDController import PIDController
   import numpy as np
   
   # Create PID controller
   pid = PIDController(
       Kp=1.0, Ki=0.1, Kd=0.05,
       MV_min=0.0, MV_max=100.0
   )
   
   # Simulation loop
   setpoint = 50.0
   process_value = 45.0
   
   for t in np.arange(0, 60, 0.1):
       output = pid.update(t, setpoint, process_value)
       # Apply output to process...
       # Update process_value from process...

**Automatic Tuning:**

.. code-block:: python

   from sproclib.controller.tuning.AMIGOTuning import AMIGOTuning
   from sproclib.controller.pid.PIDController import PIDController
   
   # Auto-tune using AMIGO method
   tuner = AMIGOTuning(controller_type="PID")
   model_params = {'K': 2.5, 'tau': 10.0, 'theta': 2.0}
   params = tuner.calculate_parameters(model_params)
   
   # Create tuned controller
   pid = PIDController(
       Kp=params['Kp'],
       Ki=params['Ki'], 
       Kd=params['Kd'],
       beta=params['beta'],
       gamma=params['gamma']
   )

**Relay Auto-Tuning:**

.. code-block:: python

   from sproclib.controller.tuning.RelayTuning import RelayTuning
   
   # Perform relay test first to get Pu and amplitude
   tuner = RelayTuning(relay_amplitude=5.0)
   test_results = {'Pu': 20.0, 'a': 2.5}  # From relay test
   params = tuner.calculate_parameters(test_results)
   
   pid = PIDController(Kp=params['Kp'], Ki=params['Ki'], Kd=params['Kd'])

See Also
--------

* :doc:`../examples` - Comprehensive examples showing controller usage
* :doc:`units_package` - Process units that work with controllers
* :doc:`analysis_package` - Analysis tools for controller design
