Quick Start Guide
=================

This guide will get you up and running with the Standard Process Control Library using the modern modular architecture.

Modern Imports (Recommended)
-----------------------------

Import components from the new modular packages::

    # Analysis tools
    from analysis.transfer_function import TransferFunction
    from analysis.system_analysis import step_response, bode_plot
    
    # Control utilities
    from utilities.control_utils import tune_pid, simulate_process
    
    # Simulation tools
    from simulation.process_simulation import ProcessSimulation
    
    # Optimization tools
    from optimization.economic_optimization import EconomicOptimization
    
    import numpy as np
    import matplotlib.pyplot as plt

Legacy Imports (Backward Compatible)
------------------------------------

If you have existing code, legacy imports still work::

    # Legacy imports (with deprecation warnings)
    from legacy.analysis import TransferFunction
    from legacy.functions import tune_pid, step_response
    
    # Or direct legacy package import
    from legacy import TransferFunction, tune_pid

Example 1: Transfer Function Analysis
-------------------------------------

Create and analyze a transfer function::

    # Create a first-order transfer function
    tf = TransferFunction([2.0], [5.0, 1.0], name="First Order Process")
    
    # Analyze step response
    response = step_response(tf, t_final=20.0)
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(response['t'], response['y'])
    plt.xlabel('Time (s)')
    plt.ylabel('Output')
    plt.title('Step Response')
    plt.grid(True)
    plt.show()
    
    # Generate Bode plot
    bode_data = bode_plot(tf, plot=True)

Example 2: PID Controller Auto-Tuning
--------------------------------------

Auto-tune a PID controller for a process::

    # Define process model parameters (FOPDT)
    model_params = {
        'K': 2.0,    # Process gain
        'tau': 5.0,  # Time constant (s)
        'theta': 1.0 # Dead time (s)
    }
    
    # Auto-tune PID controller using Ziegler-Nichols method
    pid_params = tune_pid(
        model_params, 
        method='ziegler_nichols', 
        controller_type='PID'
    )
    
    print("PID Parameters:")
    print(f"Kp = {pid_params['Kp']:.3f}")
    print(f"Ki = {pid_params['Ki']:.3f}")
    print(f"Kd = {pid_params['Kd']:.3f}")

Example 3: Process Simulation
-----------------------------

Simulate a dynamic process::

    # Define a simple tank model
    def tank_model(t, x, u):
        """Tank dynamics: dh/dt = (Fin - Fout)/A"""
        h = x[0]  # Tank height
        Fin = u[0]  # Inlet flow
        A = 1.0   # Tank area
        
        # Outlet flow (gravity-drained)
        Fout = 2.0 * np.sqrt(max(h, 0))
        
        # Height dynamics
        dh_dt = (Fin - Fout) / A
        return [dh_dt]
    
    # Create simulation
    sim = ProcessSimulation(tank_model, name="Tank Simulation")
    
    # Define input profile (step change)
    def input_profile(t):
        return [3.0 if t >= 5 else 2.0]  # Step change at t=5
    
    # Run simulation
    results = sim.run_open_loop(
        t_span=(0, 30),
        x0=[1.0],  # Initial height = 1.0 m
        u_profile=input_profile
    )
    
    # Plot results
    sim.plot_results()
    
    # Calculate steady-state height
    h_ss = tank.steady_state({'q_in': q_in})
    print(f"Steady-state height: {h_ss['h']:.2f} m")
    
    # Simulate tank dynamics
    time = np.linspace(0, 20, 100)
    inputs = np.ones(len(time)) * q_in  # constant input
    
    result = simulate_process(tank, time, inputs, h0)
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(result['time'], result['output'])
    plt.xlabel('Time (min)')
    plt.ylabel('Tank Height (m)')
    plt.title('Tank Level Response')
    plt.grid(True)
    plt.show()

Example 3: PID Tuning
----------------------

Automatically tune PID parameters for a process::

    # Define process characteristics (FOPDT model)
    process_params = {
        'K': 2.0,     # Process gain
        'tau': 5.0,   # Time constant
        'theta': 1.0  # Dead time
    }
    
    # Auto-tune using Ziegler-Nichols method
    pid_params = tune_pid(
        process_params, 
        method='ziegler_nichols', 
        controller_type='PID'
    )
    
    print(f"Tuned PID parameters:")
    print(f"Kp = {pid_params['Kp']:.3f}")
    print(f"Ki = {pid_params['Ki']:.3f}")
    print(f"Kd = {pid_params['Kd']:.3f}")

Example 4: Transfer Function Analysis
-------------------------------------

Analyze system frequency response::

    # Create transfer function (FOPDT)
    tf = TransferFunction.first_order_plus_dead_time(
        K=2.0, tau=5.0, theta=1.0, name="Process"
    )
    
    # Generate Bode plot
    bode_data = tf.bode_plot(plot=True)
    
    # Analyze stability
    stability = tf.stability_analysis()
    print(f"System stable: {stability['stable']}")

Example 5: CSTR Modeling
------------------------

Model a continuous stirred tank reactor::

    # Create CSTR model
    cstr = CSTR(
        V=100,      # Volume (L)
        k0=1e10,    # Pre-exponential factor
        E=8000,     # Activation energy (K)
        dHr=-50000, # Heat of reaction (J/mol)
        rho=1000,   # Density (g/L)
        Cp=4.18,    # Heat capacity (J/g/K)
        name="Reactor"
    )
    
    # Define operating conditions
    conditions = {
        'q_in': 10.0,    # Flow rate (L/min)
        'CA_in': 1.0,    # Inlet concentration (mol/L)
        'T_in': 300.0,   # Inlet temperature (K)
        'T_cool': 290.0  # Cooling temperature (K)
    }
    
    # Find steady state
    steady_state = cstr.steady_state(conditions)
    print(f"Steady-state concentration: {steady_state['CA']:.3f} mol/L")
    print(f"Steady-state temperature: {steady_state['T']:.1f} K")

Next Steps
----------

Now that you've seen the basics, explore these resources:

1. **Detailed Tutorials**: Learn specific control techniques
2. **API Reference**: Complete function and class documentation  
3. **Examples**: Real-world chemical engineering applications
4. **Theory**: Background on control theory concepts

Key Concepts to Explore
-----------------------

* **Process Modeling**: Tank, CSTR, and custom models
* **Controller Design**: PID, feedforward, cascade control
* **System Analysis**: Transfer functions, frequency domain
* **Optimization**: Linear programming, nonlinear optimization
* **Advanced Control**: Model predictive control, state feedback

Tips for Success
----------------

1. **Start Simple**: Begin with basic PID control before moving to advanced topics
2. **Understand Your Process**: Model the physical system before designing control
3. **Test Thoroughly**: Use the built-in test functions to validate your models
4. **Visualize Results**: Always plot your simulation results
5. **Read the Theory**: Understand the control concepts behind the code

Getting Help
------------

* Check the **API Reference** for detailed function documentation
* Look at **Examples** for working code snippets
* Review **Theory** sections for background concepts
* Run ``python test_library.py`` to verify installation
