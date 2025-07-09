Examples
========

This section contains examples demonstrating the usage of all SPROCLIB units,
including the **Semantic Plant Design API** that brings TensorFlow/Keras-style
syntax to chemical process control.

**Featured: Semantic Plant Design Examples** - Experience the semantic API
for chemical plant design with familiar machine learning syntax.

The examples are organized by unit type and demonstrate real engineering calculations
with educational explanations.

.. toctree::
   :maxdepth: 2
   :caption: Example Categories:

   examples/semantic_plant_example
   examples/complete_process_examples
   examples/compressor_examples
   examples/distillation_examples
   examples/heat_exchanger_examples
   examples/pump_examples
   examples/reactor_examples
   examples/tank_examples
   examples/utilities_examples
   examples/valve_examples

Overview
--------

Each example demonstrates:

* **Simple Examples**: Basic usage patterns and fundamental concepts
* **Advanced Examples**: Advanced analysis with realistic engineering scenarios
* **Code Output**: Complete execution results showing calculations and analysis
* **Engineering Context**: Real-world applications and best practices

All examples are fully executable and include:

- Process modeling and simulation
- Control system design and analysis
- Parameter estimation and optimization
- Performance evaluation and visualization
- Error handling and validation

Getting Started
---------------

To run any example, navigate to the examples directory and execute the Python file::

    cd examples
    python pump_examples.py

Or run all examples and capture outputs::

    python capture_examples_output.py

Semantic Plant Design Examples
------------------------------

**Featured: TensorFlow/Keras-Style API**

SPROCLIB introduces a semantic API for chemical plant design, 
using familiar syntax from machine learning frameworks:

**Complete Semantic Plant Example**:

.. literalinclude:: ../../examples.py
   :language: python
   :caption: Complete Semantic Plant Design Examples
   :lines: 1-50

**Key Semantic Features Demonstrated**:

* **Sequential Plant Building** - Add units like neural network layers
* **Functional Connections** - Connect units with stream specifications  
* **ML-Style Compilation** - Configure optimization objectives
* **Training-Style Optimization** - Optimize plant like training a model
* **Model-Style Evaluation** - Evaluate performance with test conditions

**Benefits of Semantic API**:

✅ **Familiar Syntax** - Leverage TensorFlow/Keras knowledge
✅ **Rapid Prototyping** - Build plants in minutes, not hours
✅ **Educational Excellence** - Perfect for teaching process control
✅ **Professional Results** - Industrial-grade calculations with simple syntax

See the complete semantic examples in:
- :doc:`semantic_plant_design` - Full API documentation
- :doc:`semantic_examples` - Working examples and tutorials
- :doc:`tensorflow_comparison` - Side-by-side syntax comparison

Example Categories
------------------

**Process Units**
  - Pumps and Compressors
  - Tanks and Vessels  
  - Valves and Flow Control
  - Heat Exchangers
  - Reactors (CSTR, PFR, Batch, etc.)
  - Distillation Columns

**Utilities and Analysis**
  - Linear Approximation
  - Statistical Analysis
  - Control System Design

**Complete Process Examples**
  - Integrated process control systems
  - Multi-unit operations
  - Advanced control strategies

Legacy Example: Complete Tank Control System
---------------------------------------------

The following is the original example demonstrating basic tank control:

.. literalinclude:: ../../examples.py
   :language: python
   :lines: 1-50
   :caption: Tank Control Example

This example demonstrates:

* Process modeling with the Tank class
* Linear approximation for control design  
* FOPDT parameter identification
* Automated PID tuning
* Closed-loop simulation and analysis

Run this example::

    python examples.py
        
        # CSTR dynamics
        current_state = [concentrations[i-1], temperatures[i-1]]
        inputs = [10.0, 1.0, 300.0, T_cool_cmd]
        
        derivatives = cstr.dynamics(time[i-1], current_state, inputs)
        
        concentrations[i] = concentrations[i-1] + derivatives[0] * dt
        temperatures[i] = temperatures[i-1] + derivatives[1] * dt
    
    # Plot results
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    axes[0].plot(time, T_setpoint, 'r--', label='Setpoint', linewidth=2)
    axes[0].plot(time, temperatures, 'b-', label='Temperature')
    axes[0].set_ylabel('Temperature (K)')
    axes[0].legend()
    axes[0].grid(True)
    axes[0].set_title('CSTR Temperature Control')
    
    axes[1].plot(time, concentrations, 'g-', label='Concentration')
    axes[1].set_ylabel('CA (mol/L)')
    axes[1].legend()
    axes[1].grid(True)
    
    axes[2].plot(time, coolant_temps, 'm-', label='Coolant Temperature')
    axes[2].set_ylabel('T_cool (K)')
    axes[2].set_xlabel('Time (min)')
    axes[2].legend()
    axes[2].grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # Performance analysis
    step_time = 100
    final_temp = np.mean(temperatures[-100:])  # Average of last 100 points
    target_temp = 360.0
    
    settling_idx = np.where((time > step_time) & 
                           (np.abs(temperatures - target_temp) < 0.02 * target_temp))[0]
    settling_time = time[settling_idx[0]] - step_time if len(settling_idx) > 0 else np.inf
    
    print(f"\\nPerformance for setpoint change 350->360 K:")
    print(f"  Settling time (2%): {settling_time:.1f} min")
    print(f"  Final temperature: {final_temp:.1f} K")
    print(f"  Steady-state error: {abs(final_temp - target_temp):.2f} K")

Example 3: Transfer Function Analysis
-------------------------------------

Frequency domain analysis of a process control system.

.. code-block:: python
   :caption: Frequency Domain Analysis

    from process_control import TransferFunction, PIDController
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Create process transfer function (FOPDT)
    process = TransferFunction.first_order_plus_dead_time(
        K=2.0, tau=10.0, theta=2.0, name="Process"
    )
    
    print(f"Process transfer function: G(s) = {process}")
    
    # Design PID controller
    pid_params = tune_pid(
        {'K': 2.0, 'tau': 10.0, 'theta': 2.0}, 
        method='ziegler_nichols', 
        controller_type='PID'
    )
    
    # Create controller transfer function
    # PID: C(s) = Kp + Ki/s + Kd*s
    Kp, Ki, Kd = pid_params['Kp'], pid_params['Ki'], pid_params['Kd']
    
    # For analysis, approximate derivative as Kd*s/(tau_d*s + 1) with tau_d = Kd/10/Kp
    tau_d = Kd / (10 * Kp) if Kp != 0 else 0.1
    
    # PID transfer function: (Kp*(tau_d*s + 1) + Ki*tau_d/s + Kd*s) / (tau_d*s + 1)
    controller_num = [Kd + Kp*tau_d, Kp + Ki*tau_d, Ki]
    controller_den = [tau_d, 1, 0]  # Note: added zero for integrator
    
    controller = TransferFunction(controller_num, controller_den, name="PID Controller")
    
    # Closed-loop analysis
    print(f"\\nController: C(s) = {controller}")
    print(f"PID Parameters: Kp={Kp:.3f}, Ki={Ki:.3f}, Kd={Kd:.3f}")
    
    # Open-loop analysis
    print("\\n=== Open-Loop Analysis ===")
    
    # Create frequency vector
    frequencies = np.logspace(-3, 1, 1000)  # 0.001 to 10 rad/min
    
    # Process Bode plot
    process_bode = process.bode_plot(frequencies=frequencies, plot=False)
    
    # Controller Bode plot
    controller_bode = controller.bode_plot(frequencies=frequencies, plot=False)
    
    # Open-loop = Process * Controller
    open_loop_mag = process_bode['magnitude'] * controller_bode['magnitude']
    open_loop_phase = process_bode['phase'] + controller_bode['phase']
    
    # Stability analysis
    # Find gain crossover (where |GC| = 1)
    gain_crossover_idx = np.argmin(np.abs(open_loop_mag - 1.0))
    gain_crossover_freq = frequencies[gain_crossover_idx]
    phase_margin = 180 + open_loop_phase[gain_crossover_idx]
    
    # Find phase crossover (where phase = -180°)
    phase_crossover_idx = np.argmin(np.abs(open_loop_phase + 180))
    phase_crossover_freq = frequencies[phase_crossover_idx]
    gain_margin_db = -20 * np.log10(open_loop_mag[phase_crossover_idx])
    
    print(f"Gain crossover frequency: {gain_crossover_freq:.3f} rad/min")
    print(f"Phase margin: {phase_margin:.1f} degrees")
    print(f"Phase crossover frequency: {phase_crossover_freq:.3f} rad/min")
    print(f"Gain margin: {gain_margin_db:.1f} dB")
    
    # Closed-loop analysis
    print("\\n=== Closed-Loop Analysis ===")
    
    # Closed-loop transfer function: GC/(1+GC)
    # This requires careful polynomial manipulation for general case
    # For demonstration, we'll compute frequency response directly
    
    closed_loop_mag = open_loop_mag / np.sqrt((1 + open_loop_mag*np.cos(np.radians(open_loop_phase)))**2 + 
                                             (open_loop_mag*np.sin(np.radians(open_loop_phase)))**2)
    
    # Plot analysis results
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Open-loop Bode plot
    axes[0,0].semilogx(frequencies, 20*np.log10(open_loop_mag), 'b-', linewidth=2)
    axes[0,0].axhline(y=0, color='r', linestyle='--', alpha=0.7)
    axes[0,0].axvline(x=gain_crossover_freq, color='g', linestyle=':', alpha=0.7)
    axes[0,0].set_ylabel('Magnitude (dB)')
    axes[0,0].set_title('Open-Loop Bode Plot')
    axes[0,0].grid(True)
    
    axes[1,0].semilogx(frequencies, open_loop_phase, 'b-', linewidth=2)
    axes[1,0].axhline(y=-180, color='r', linestyle='--', alpha=0.7)
    axes[1,0].axvline(x=gain_crossover_freq, color='g', linestyle=':', alpha=0.7)
    axes[1,0].set_ylabel('Phase (degrees)')
    axes[1,0].set_xlabel('Frequency (rad/min)')
    axes[1,0].grid(True)
    
    # Nyquist plot
    real_part = open_loop_mag * np.cos(np.radians(open_loop_phase))
    imag_part = open_loop_mag * np.sin(np.radians(open_loop_phase))
    
    axes[0,1].plot(real_part, imag_part, 'b-', linewidth=2, label='GC(jω)')
    axes[0,1].plot(-1, 0, 'ro', markersize=8, label='Critical Point (-1,0)')
    axes[0,1].axhline(y=0, color='k', linestyle='-', alpha=0.3)
    axes[0,1].axvline(x=0, color='k', linestyle='-', alpha=0.3)
    axes[0,1].set_xlabel('Real Part')
    axes[0,1].set_ylabel('Imaginary Part')
    axes[0,1].set_title('Nyquist Plot')
    axes[0,1].legend()
    axes[0,1].grid(True)
    axes[0,1].axis('equal')
    
    # Closed-loop frequency response
    axes[1,1].semilogx(frequencies, 20*np.log10(closed_loop_mag), 'r-', linewidth=2)
    axes[1,1].axhline(y=-3, color='g', linestyle='--', alpha=0.7, label='-3 dB')
    axes[1,1].set_ylabel('Magnitude (dB)')
    axes[1,1].set_xlabel('Frequency (rad/min)')
    axes[1,1].set_title('Closed-Loop Frequency Response')
    axes[1,1].legend()
    axes[1,1].grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # Step response analysis
    print("\\n=== Step Response Analysis ===")
    step_time = np.linspace(0, 60, 600)
    
    # Approximate closed-loop step response
    # (This would normally require inverse Laplace transform)
    # For demonstration, we'll simulate
    
    # Simple approximation for closed-loop response
    tau_cl = 1 / gain_crossover_freq  # Approximate closed-loop time constant
    step_response = 1 - np.exp(-step_time / tau_cl)
    
    plt.figure(figsize=(10, 6))
    plt.plot(step_time, step_response, 'b-', linewidth=2, label='Closed-loop Step Response')
    plt.axhline(y=1, color='r', linestyle='--', alpha=0.7, label='Final Value')
    plt.axhline(y=0.98, color='g', linestyle=':', alpha=0.7, label='2% Settling')
    plt.xlabel('Time (min)')
    plt.ylabel('Response')
    plt.title('Closed-Loop Step Response')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Summary
    print("\\n=== Control System Summary ===")
    print(f"System appears {'STABLE' if phase_margin > 0 and gain_margin_db > 0 else 'UNSTABLE'}")
    print(f"Gain margin: {gain_margin_db:.1f} dB (>6 dB recommended)")
    print(f"Phase margin: {phase_margin:.1f}° (>30° recommended)")
    print(f"Bandwidth (approx): {gain_crossover_freq:.3f} rad/min")

Example 4: Batch Process Optimization
--------------------------------------

Optimize a batch reactor operation for maximum profit.

.. code-block:: python
   :caption: Batch Process Optimization

    from process_control import Optimization, StateTaskNetwork
    import numpy as np
    from scipy.optimize import minimize
    from scipy.integrate import solve_ivp
    import matplotlib.pyplot as plt
    
    # Define batch reactor model
    def batch_reactor_dynamics(t, state, params):
        \"\"\"
        Batch reactor: A + B -> C
        Temperature-dependent kinetics
        \"\"\"
        CA, CB, CC, T = state
        
        # Arrhenius kinetics
        k = params['k0'] * np.exp(-params['E'] / T)
        
        # Reaction rate
        rate = k * CA * CB
        
        # Energy balance (simplified)
        Q_reaction = rate * params['dHr'] * params['V']  # Heat generation
        Q_removal = params['UA'] * (T - params['T_ambient'])  # Heat removal
        
        dT_dt = (Q_reaction - Q_removal) / (params['rho'] * params['Cp'] * params['V'])
        
        return [-rate, -rate, rate, dT_dt]
    
    # Batch reactor parameters
    reactor_params = {
        'V': 1000,        # Volume (L)
        'k0': 1e12,       # Pre-exponential factor (L/mol/min)
        'E': 8000,        # Activation energy (K)
        'dHr': -50000,    # Heat of reaction (J/mol)
        'UA': 10000,      # Heat transfer coefficient (J/min/K)
        'rho': 1000,      # Density (g/L)
        'Cp': 4.18,       # Heat capacity (J/g/K)
        'T_ambient': 300  # Ambient temperature (K)
    }
    
    def simulate_batch(T_profile_params, plot_results=False):
        \"\"\"
        Simulate batch reactor with temperature profile
        T_profile_params: [T_initial, T_final, ramp_time]
        \"\"\"
        T_initial, T_final, ramp_time = T_profile_params
        
        # Define temperature profile
        def temperature_profile(t):
            if t < ramp_time:
                return T_initial + (T_final - T_initial) * t / ramp_time
            else:
                return T_final
        
        # Modified dynamics function with temperature profile
        def dynamics_with_profile(t, state):
            T_setpoint = temperature_profile(t)
            # For simplicity, assume perfect temperature control
            modified_state = [state[0], state[1], state[2], T_setpoint]
            return batch_reactor_dynamics(t, modified_state, reactor_params)[:3] + [0]
        
        # Initial conditions
        CA0, CB0, CC0 = 2.0, 1.5, 0.0  # mol/L
        initial_state = [CA0, CB0, CC0, T_initial]
        
        # Simulate
        batch_time = 120  # minutes
        sol = solve_ivp(
            dynamics_with_profile,
            [0, batch_time],
            initial_state,
            dense_output=True,
            rtol=1e-6
        )
        
        if plot_results:
            t_plot = np.linspace(0, batch_time, 1000)
            y_plot = sol.sol(t_plot)
            T_plot = [temperature_profile(t) for t in t_plot]
            
            fig, axes = plt.subplots(2, 2, figsize=(12, 8))
            
            axes[0,0].plot(t_plot, y_plot[0], label='CA')
            axes[0,0].plot(t_plot, y_plot[1], label='CB')
            axes[0,0].plot(t_plot, y_plot[2], label='CC')
            axes[0,0].set_ylabel('Concentration (mol/L)')
            axes[0,0].legend()
            axes[0,0].grid(True)
            axes[0,0].set_title('Concentrations')
            
            axes[0,1].plot(t_plot, T_plot)
            axes[0,1].set_ylabel('Temperature (K)')
            axes[0,1].grid(True)
            axes[0,1].set_title('Temperature Profile')
            
            # Reaction rate
            rates = []
            for i in range(len(t_plot)):
                k = reactor_params['k0'] * np.exp(-reactor_params['E'] / T_plot[i])
                rate = k * y_plot[0,i] * y_plot[1,i]
                rates.append(rate)
            
            axes[1,0].plot(t_plot, rates)
            axes[1,0].set_ylabel('Reaction Rate (mol/L/min)')
            axes[1,0].set_xlabel('Time (min)')
            axes[1,0].grid(True)
            axes[1,0].set_title('Reaction Rate')
            
            # Cumulative production
            CC_production = y_plot[2] * reactor_params['V'] / 1000  # kmol
            axes[1,1].plot(t_plot, CC_production)
            axes[1,1].set_ylabel('Product C (kmol)')
            axes[1,1].set_xlabel('Time (min)')
            axes[1,1].grid(True)
            axes[1,1].set_title('Cumulative Production')
            
            plt.tight_layout()
            plt.show()
        
        # Return final concentrations
        final_state = sol.y[:, -1]
        return final_state
    
    # Define economic objective
    def batch_profit(T_profile_params):
        \"\"\"Calculate batch profit for given temperature profile\"\"\"
        try:
            final_state = simulate_batch(T_profile_params)
            CA_final, CB_final, CC_final, _ = final_state
            
            # Revenue from product C
            product_value = CC_final * reactor_params['V'] / 1000 * 1000  # kmol * $/kmol
            
            # Cost of unreacted raw materials (opportunity cost)
            waste_cost = (CA_final + CB_final) * reactor_params['V'] / 1000 * 100  # kmol * $/kmol
            
            # Energy cost (proportional to temperature)
            T_initial, T_final, ramp_time = T_profile_params
            avg_temp = (T_initial + T_final) / 2
            energy_cost = (avg_temp - 300) * 0.5 * 120  # $/K/min * K * min
            
            profit = product_value - waste_cost - energy_cost
            
            return -profit  # Negative for minimization
            
        except:
            return 1e6  # Large penalty for failed simulations
    
    # Optimization
    print("=== Batch Reactor Optimization ===")
    
    # Decision variables: [T_initial, T_final, ramp_time]
    # Bounds: Temperature 300-400 K, ramp time 0-60 min
    bounds = [(300, 400), (300, 400), (0, 60)]
    
    # Initial guess
    x0 = [320, 350, 30]
    
    print(f"Initial guess: T_initial={x0[0]}K, T_final={x0[1]}K, ramp_time={x0[2]}min")
    
    # Simulate initial case
    print("\\nSimulating initial case...")
    initial_profit = -batch_profit(x0)
    print(f"Initial profit: ${initial_profit:.2f}")
    
    # Optimize
    print("\\nOptimizing...")
    result = minimize(
        batch_profit,
        x0,
        method='L-BFGS-B',
        bounds=bounds,
        options={'disp': True, 'maxiter': 50}
    )
    
    optimal_params = result.x
    optimal_profit = -result.fun
    
    print(f"\\n=== Optimization Results ===")
    print(f"Optimal parameters:")
    print(f"  Initial temperature: {optimal_params[0]:.1f} K")
    print(f"  Final temperature: {optimal_params[1]:.1f} K")  
    print(f"  Ramp time: {optimal_params[2]:.1f} min")
    print(f"\\nOptimal profit: ${optimal_profit:.2f}")
    print(f"Profit improvement: ${optimal_profit - initial_profit:.2f}")
    print(f"Relative improvement: {(optimal_profit - initial_profit)/initial_profit*100:.1f}%")
    
    # Compare optimal vs initial operation
    print("\\n=== Comparison: Initial vs Optimal ===")
    
    print("\\nInitial operation:")
    initial_final = simulate_batch(x0)
    print(f"  Final concentrations: CA={initial_final[0]:.3f}, CB={initial_final[1]:.3f}, CC={initial_final[2]:.3f} mol/L")
    
    print("\\nOptimal operation:")
    optimal_final = simulate_batch(optimal_params)
    print(f"  Final concentrations: CA={optimal_final[0]:.3f}, CB={optimal_final[1]:.3f}, CC={optimal_final[2]:.3f} mol/L")
    
    print(f"\\nProduct improvement: {(optimal_final[2] - initial_final[2])/initial_final[2]*100:.1f}%")
    
    # Plot optimal operation
    print("\\nPlotting optimal operation...")
    simulate_batch(optimal_params, plot_results=True)

Running the Examples
--------------------

To run these examples:

1. **Individual Examples**: Copy and paste the code into Python scripts
2. **Complete Examples**: Run the main examples file::

    python examples.py

3. **Interactive Exploration**: Use Jupyter notebooks for step-by-step analysis

Each example includes:

* **Complete, runnable code**
* **Detailed explanations** of the control concepts
* **Performance analysis** and metrics
* **Visualization** of results
* **Extension suggestions** for further exploration

See Also
--------

* :doc:`tutorials` - Step-by-step learning guides
* :doc:`api/units_package` - Modular API documentation
* :doc:`theory` - Mathematical background on control theory
