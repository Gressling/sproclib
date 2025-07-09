Utilities Package
=================

The utilities package provides essential control design utilities, mathematical tools,
and data processing functions for process control applications.

.. note::
   This is part of the modern modular structure of SPROCLIB. For legacy compatibility,
   see :doc:`legacy`.

Submodules
----------

Control Utils
~~~~~~~~~~~~~

.. automodule:: utilities.control_utils
   :members:
   :undoc-members:
   :show-inheritance:

Math Utils
~~~~~~~~~~

.. automodule:: utilities.math_utils
   :members:
   :undoc-members:
   :show-inheritance:

Data Utils
~~~~~~~~~~

.. automodule:: utilities.data_utils
   :members:
   :undoc-members:
   :show-inheritance:

Quick Usage
-----------

PID Controller Tuning::

    from utilities.control_utils import tune_pid
    
    # Define process model parameters
    model_params = {
        'K': 2.0,    # Process gain
        'tau': 5.0,  # Time constant
        'theta': 1.0 # Dead time
    }
    
    # Auto-tune PID controller
    pid_params = tune_pid(
        model_params, 
        method='ziegler_nichols', 
        controller_type='PID'
    )
    
    print(f"Kp = {pid_params['Kp']:.3f}")
    print(f"Ki = {pid_params['Ki']:.3f}")
    print(f"Kd = {pid_params['Kd']:.3f}")

Process Linearization::

    from utilities.control_utils import linearize
    import numpy as np
    
    # Define nonlinear model
    def reactor_model(x, u):
        T, Ca = x
        Tc = u[0]
        # Reactor dynamics
        dT_dt = 0.1 * (Tc - T) + 0.5 * Ca
        dCa_dt = -0.2 * Ca * np.exp(-1000/T)
        return np.array([dT_dt, dCa_dt])
    
    # Linearize around operating point
    x_ss = np.array([350, 2.0])  # Temperature, Concentration
    u_ss = np.array([340])       # Coolant temperature
    
    A, B = linearize(reactor_model, x_ss, u_ss)
    print("State matrix A:")
    print(A)
    print("Input matrix B:")
    print(B)

Mathematical Utilities::

    from utilities.math_utils import numerical_derivative, integrate_ode
    
    # Numerical differentiation
    def f(x):
        return x**3 + 2*x**2 - 5*x + 1
    
    df_dx = numerical_derivative(f, x=2.0, method='central')
    print(f"df/dx at x=2: {df_dx}")

Data Processing::

    from utilities.data_utils import filter_data, resample_data
    import numpy as np
    
    # Generate noisy data
    t = np.linspace(0, 10, 1000)
    signal = np.sin(t) + 0.1 * np.random.randn(len(t))
    
    # Filter data
    filtered = filter_data(signal, filter_type='lowpass', cutoff=0.1)
    
    # Resample data
    t_new, signal_new = resample_data(t, filtered, new_rate=0.1)
