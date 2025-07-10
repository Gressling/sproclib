Functions Legacy Package
========================

.. note::
   This documentation covers the legacy functions interface.
   
   **For new projects, use the modular utility packages instead:**
   :doc:`utilities_package` - Modern modular utility functions
   
   The legacy interface is maintained for backward compatibility via the legacy package.

The functions module provides utility functions for common process control tasks, including PID tuning, system identification, linearization, and analysis.

.. note::
   The functions module contains utility functions that work with all process units and analysis tools. These functions provide convenient methods for common process control engineering tasks.
   
   For examples of function usage with process units, see:
   
   * :doc:`../examples` - Comprehensive examples showing function integration
   * :doc:`units_package` - Process units that work with utility functions

Functions Documentation
-----------------------

.. automodule:: sproclib.functions
   :members:
   :undoc-members:
   :show-inheritance:

Core Functions
--------------

Step Response Analysis
~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: functions.step_response

Calculate the step response of a system from its transfer function.

**Mathematical Background:**

For a transfer function :math:`G(s)`, the step response is:

.. math::
   y(t) = \\mathcal{L}^{-1}\\left\\{\\frac{G(s)}{s}\\right\\}

Example Usage::

    from functions import step_response
    
    # Define transfer function (FOPDT)
    num = [2.0]  # K = 2.0
    den = [5.0, 1.0]  # tau*s + 1 with tau = 5.0
    
    response = step_response((num, den), time_points=100, final_time=25)
    
    plt.plot(response['time'], response['output'])
    plt.xlabel('Time')
    plt.ylabel('Response')
    plt.title('Step Response')

Frequency Domain Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: functions.bode_plot

Generate Bode plots for frequency domain analysis.

**Mathematical Foundation:**

The Bode plot shows:

* **Magnitude:** :math:`|G(j\\omega)|` in dB = :math:`20\\log_{10}|G(j\\omega)|`
* **Phase:** :math:`\\angle G(j\\omega)` in degrees

Example Usage::

    from functions import bode_plot
    
    # Transfer function coefficients
    num = [2.0]
    den = [5.0, 1.0]
    
    bode_data = bode_plot((num, den), plot=True)
    
    # Access frequency response data
    frequencies = bode_data['frequency']
    magnitude_db = bode_data['magnitude_db']
    phase_deg = bode_data['phase_deg']

System Identification
~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: functions.fit_fopdt

Fit First-Order Plus Dead Time (FOPDT) model to step response data.

**FOPDT Model:**

.. math::
   G(s) = \\frac{K e^{-\\theta s}}{\\tau s + 1}

Where:
- :math:`K` = Process gain
- :math:`\\tau` = Time constant  
- :math:`\\theta` = Dead time

Example Usage::

    from functions import fit_fopdt
    import numpy as np
    
    # Generate synthetic data
    time = np.linspace(0, 20, 100)
    # Simulate step response with noise
    response = 2.0 * (1 - np.exp(-(time-1)/5)) * (time >= 1) + 0.05 * np.random.randn(100)
    
    # Fit FOPDT model
    params = fit_fopdt(time, response, step_size=1.0)
    
    print(f"Fitted parameters:")
    print(f"K = {params['K']:.3f}")
    print(f"tau = {params['tau']:.3f}")  
    print(f"theta = {params['theta']:.3f}")

Controller Design
-----------------

PID Tuning
~~~~~~~~~~~

.. autofunction:: functions.tune_pid

Automatically tune PID controller parameters using various methods.

**Tuning Methods:**

1. **Ziegler-Nichols** - Classic step response method
2. **AMIGO** - Advanced method for integrating processes  
3. **IMC** - Internal Model Control tuning

Example Usage::

    from functions import tune_pid
    
    # Process model parameters (FOPDT)
    process_params = {
        'K': 2.0,     # Process gain
        'tau': 5.0,   # Time constant (min)
        'theta': 1.0  # Dead time (min)
    }
    
    # Tune PID using Ziegler-Nichols
    pid_zn = tune_pid(process_params, method='ziegler_nichols', controller_type='PID')
    print(f"Ziegler-Nichols: Kp={pid_zn['Kp']:.3f}, Ki={pid_zn['Ki']:.3f}, Kd={pid_zn['Kd']:.3f}")
    
    # Tune PI using AMIGO method
    pid_amigo = tune_pid(process_params, method='amigo', controller_type='PI')
    print(f"AMIGO: Kp={pid_amigo['Kp']:.3f}, Ki={pid_amigo['Ki']:.3f}")

Linearization
~~~~~~~~~~~~~

.. autofunction:: functions.linearize

Linearize nonlinear process models around operating points.

**Mathematical Approach:**

For a nonlinear system :math:`\\dot{x} = f(x,u)`, the linearization around :math:`(x_0, u_0)` gives:

.. math::
   A = \\left.\\frac{\\partial f}{\\partial x}\\right|_{x_0,u_0}, \\quad B = \\left.\\frac{\\partial f}{\\partial u}\\right|_{x_0,u_0}

Example Usage::

    from functions import linearize
    from models import Tank
    
    # Create nonlinear tank model
    tank = Tank(A=1.0, C=2.0)
    
    # Linearize around operating point
    x0 = [2.0]  # height = 2.0 m
    u0 = [4.0]  # q_in = 4.0 L/min
    
    A, B = linearize(tank, x0, u0)
    
    print(f"Linear model matrices:")
    print(f"A = {A}")
    print(f"B = {B}")

Simulation and Analysis
-----------------------

Process Simulation
~~~~~~~~~~~~~~~~~~

.. autofunction:: functions.simulate_process

Simulate process dynamics with time-varying inputs.

Example Usage::

    from functions import simulate_process
    from models import CSTR
    import numpy as np
    
    # Create CSTR model
    cstr = CSTR(V=100, k0=1e10, E=8000, dHr=-50000, rho=1000, Cp=4.18)
    
    # Define time vector and inputs
    time = np.linspace(0, 100, 1000)
    
    # Step change in inlet concentration at t=50
    CA_in = np.where(time < 50, 1.0, 1.2)
    inputs = np.column_stack([
        np.ones_like(time) * 10,  # q_in = 10 L/min
        CA_in,                    # CA_in step change
        np.ones_like(time) * 300, # T_in = 300 K
        np.ones_like(time) * 290  # T_cool = 290 K
    ])
    
    # Initial conditions
    initial_state = [0.5, 350]  # [CA, T]
    
    # Simulate
    result = simulate_process(cstr, time, inputs, initial_state)
    
    # Plot results
    plt.figure(figsize=(12, 8))
    plt.subplot(2,1,1)
    plt.plot(result['time'], result['output'][:,0])
    plt.ylabel('Concentration (mol/L)')
    plt.subplot(2,1,2) 
    plt.plot(result['time'], result['output'][:,1])
    plt.ylabel('Temperature (K)')
    plt.xlabel('Time (min)')

Stability Analysis
~~~~~~~~~~~~~~~~~~

.. autofunction:: functions.stability_analysis

Analyze system stability from transfer function or state-space model.

**Stability Criteria:**

* **Poles Analysis** - All poles must have negative real parts
* **Gain Margin** - Factor by which gain can increase before instability
* **Phase Margin** - Additional phase lag before instability

Example Usage::

    from functions import stability_analysis
    
    # Transfer function for analysis
    num = [2.0]
    den = [25.0, 10.0, 1.0]  # Second-order system
    
    stability = stability_analysis((num, den))
    
    print(f"System stable: {stability['stable']}")
    print(f"Poles: {stability['poles']}")
    if stability['gain_margin_db'] is not None:
        print(f"Gain margin: {stability['gain_margin_db']:.1f} dB")
        print(f"Phase margin: {stability['phase_margin_deg']:.1f} degrees")

Optimization Functions
----------------------

Process Optimization
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: functions.optimize_operation

Optimize process operating conditions for maximum profit or minimum cost.

Example Usage::

    from functions import optimize_operation
    
    # Define objective function (profit)
    def profit_function(variables):
        temperature, flow_rate = variables
        revenue = production_rate(temperature, flow_rate) * product_price
        energy_cost = energy_consumption(temperature) * energy_price
        return -(revenue - energy_cost)  # Negative for minimization
    
    # Define constraints
    constraints = [
        {'type': 'ineq', 'fun': lambda x: 400 - x[0]},  # T <= 400 K
        {'type': 'ineq', 'fun': lambda x: x[0] - 250},  # T >= 250 K
        {'type': 'ineq', 'fun': lambda x: 20 - x[1]},   # Flow <= 20 L/min
        {'type': 'ineq', 'fun': lambda x: x[1] - 5}     # Flow >= 5 L/min
    ]
    
    # Initial guess
    x0 = [300, 10]  # [Temperature, Flow rate]
    
    # Optimize
    result = optimize_operation(profit_function, x0, constraints=constraints)
    
    print(f"Optimal temperature: {result['x'][0]:.1f} K")
    print(f"Optimal flow rate: {result['x'][1]:.1f} L/min")
    print(f"Maximum profit: ${-result['fun']:.2f}")

Advanced Control
----------------

Disturbance Rejection
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: functions.disturbance_rejection

Analyze and design for disturbance rejection performance.

Example Usage::

    from functions import disturbance_rejection
    
    # Plant and controller transfer functions
    plant_tf = ([2.0], [5.0, 1.0])      # Process
    controller_tf = ([1.0, 0.1], [1.0, 0])  # PI controller
    
    # Analyze step disturbance rejection
    analysis = disturbance_rejection(
        plant_tf, 
        controller_tf, 
        disturbance_type='step'
    )
    
    print(f"Steady-state error: {analysis['steady_state_error']:.3f}")
    print(f"Settling time: {analysis['settling_time']:.1f} min")

Model Predictive Control
~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: functions.model_predictive_control

Basic Model Predictive Control (MPC) implementation.

**MPC Formulation:**

MPC solves the optimization problem:

.. math::
   \\min_{\\Delta u} \\sum_{i=1}^{N_p} ||y_{k+i} - r_{k+i}||_Q^2 + \\sum_{i=0}^{N_c-1} ||\\Delta u_{k+i}||_R^2

Subject to constraints on inputs, outputs, and input moves.

Example Usage::

    from functions import model_predictive_control
    import numpy as np
    
    # System matrices (discrete-time state space)
    A = np.array([[0.8, 0.1], [0, 0.9]])
    B = np.array([[1], [0.5]])
    C = np.array([[1, 0]])
    
    # MPC parameters
    prediction_horizon = 10
    control_horizon = 3
    Q = np.array([[1]])  # Output weight
    R = np.array([[0.1]])  # Input weight
    
    # Current state and reference
    current_state = np.array([1.0, 0.5])
    reference = np.array([2.0])
    
    # Compute MPC control action
    control_action = model_predictive_control(
        A, B, C, 
        prediction_horizon, control_horizon,
        Q, R,
        current_state, reference
    )
    
    print(f"MPC control action: {control_action}")

Utility Functions
-----------------

Helper Functions
~~~~~~~~~~~~~~~~

The module includes several utility functions for common tasks:

* **Input validation** - Check parameter ranges and types
* **Unit conversions** - Convert between different unit systems
* **Data preprocessing** - Filter and condition measurement data
* **Plotting utilities** - Standardized plotting functions

Performance Guidelines
----------------------

Function Selection
~~~~~~~~~~~~~~~~~~

Choose appropriate functions based on your application:

* **step_response()** - Quick system characterization
* **bode_plot()** - Frequency domain design
* **tune_pid()** - Automated controller design
* **simulate_process()** - Detailed dynamic analysis

Computational Efficiency
~~~~~~~~~~~~~~~~~~~~~~~~

For better performance:

* Use appropriate time steps (not too small)
* Cache expensive calculations (steady-state solutions)
* Vectorize operations when possible
* Consider parallel processing for parameter studies

Error Handling
~~~~~~~~~~~~~~

All functions include comprehensive error checking:

* Parameter validation
* Numerical stability checks  
* Graceful degradation for edge cases
* Informative error messages

See Also
--------

* :doc:`controllers_legacy_package` - PID controllers that use these tuning functions
* :doc:`models_legacy_package` - Process models for simulation and linearization
* :doc:`analysis_legacy_package` - Advanced analysis classes
* :doc:`../examples` - Complete examples using these functions
