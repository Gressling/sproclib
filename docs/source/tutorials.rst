Tutorials
=========

This section provides step-by-step tutorials for common process control tasks.

Tutorial 1: Basic Tank Level Control
-------------------------------------

Learn the fundamentals of level control using a gravity-drained tank.

**Objective:** Design a PID controller for tank level control

**Step 1: Model the Process**

Start by creating a tank model::

    from process_control import Tank, PIDController, simulate_process
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Create tank model (1 m² area, valve coefficient 2.0)
    tank = Tank(A=1.0, C=2.0, name="Level Control Tank")
    
    # Check steady-state behavior
    steady_state = tank.steady_state({'q_in': 4.0})
    print(f"For q_in = 4.0 L/min, steady-state height = {steady_state['h']:.2f} m")

**Step 2: Linearize Around Operating Point**

For controller design, we need a linear model::

    from process_control import LinearApproximation
    
    # Create linearization tool
    linear_approx = LinearApproximation(tank)
    
    # Linearize around q_in = 4.0 L/min (h_ss = 4.0 m)
    u_nominal = [4.0]
    A, B = linear_approx.linearize(u_nominal)
    
    print(f"Linear model: A = {A[0,0]:.3f}, B = {B[0,0]:.3f}")

**Step 3: Design PID Controller**

Use automated tuning to design the controller::

    from process_control import tune_pid, fit_fopdt
    
    # First, identify FOPDT parameters from step response
    time = np.linspace(0, 20, 100)
    step_response = 1.0 * (1 - np.exp(-time/4))  # Approximate step response
    
    fopdt_params = fit_fopdt(time, step_response, step_size=1.0)
    print(f"FOPDT parameters: K={fopdt_params['K']:.3f}, tau={fopdt_params['tau']:.3f}")
    
    # Tune PID using Ziegler-Nichols
    pid_params = tune_pid(fopdt_params, method='ziegler_nichols', controller_type='PID')
    
    # Create PID controller
    controller = PIDController(**pid_params)
    print(f"PID parameters: Kp={pid_params['Kp']:.3f}, Ki={pid_params['Ki']:.3f}, Kd={pid_params['Kd']:.3f}")

**Step 4: Closed-Loop Simulation**

Test the controller performance::

    # Simulation parameters
    time = np.linspace(0, 50, 500)
    setpoint = 3.0  # Desired height (m)
    initial_height = 1.0  # Starting height (m)
    
    # Storage for results
    heights = np.zeros_like(time)
    control_outputs = np.zeros_like(time)
    heights[0] = initial_height
    
    # Closed-loop simulation
    for i in range(1, len(time)):
        dt = time[i] - time[i-1]
        
        # PID control
        q_in = controller.update(setpoint, heights[i-1], dt)
        q_in = max(0, min(q_in, 10))  # Limit flow rate 0-10 L/min
        control_outputs[i] = q_in
        
        # Process dynamics
        dhdt = tank.dynamics(time[i-1], [heights[i-1]], [q_in])[0]
        heights[i] = heights[i-1] + dhdt * dt
    
    # Plot results
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 1, 1)
    plt.plot(time, heights, 'b-', label='Tank Height')
    plt.axhline(y=setpoint, color='r', linestyle='--', label='Setpoint')
    plt.ylabel('Height (m)')
    plt.legend()
    plt.grid(True)
    plt.title('Tank Level Control')
    
    plt.subplot(2, 1, 2)
    plt.plot(time, control_outputs, 'g-', label='Flow Rate')
    plt.ylabel('Flow Rate (L/min)')
    plt.xlabel('Time (min)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

**Step 5: Performance Analysis**

Evaluate controller performance::

    # Calculate performance metrics
    settling_time_idx = np.where(np.abs(heights - setpoint) < 0.02 * setpoint)[0]
    settling_time = time[settling_time_idx[0]] if len(settling_time_idx) > 0 else np.inf
    
    overshoot = (np.max(heights) - setpoint) / setpoint * 100
    steady_state_error = abs(heights[-1] - setpoint)
    
    print(f"Performance Metrics:")
    print(f"  Settling time (2%): {settling_time:.1f} min")
    print(f"  Overshoot: {overshoot:.1f}%")
    print(f"  Steady-state error: {steady_state_error:.3f} m")

Tutorial 2: CSTR Temperature Control
-------------------------------------

Design a cascade control system for a CSTR with temperature control.

**Objective:** Control reactor temperature with cascade control structure

**Step 1: Model the CSTR**

Create a detailed CSTR model::

    from process_control import CSTR
    
    # Create CSTR with realistic parameters
    cstr = CSTR(
        V=100,        # Volume (L)
        k0=1e10,      # Pre-exponential factor (1/min)
        E=8000,       # Activation energy (K)
        dHr=-50000,   # Heat of reaction (J/mol)
        rho=1000,     # Density (g/L)
        Cp=4.18,      # Heat capacity (J/g/K)
        UA=50000,     # Heat transfer coefficient (J/min/K)
        name="Main Reactor"
    )
    
    # Find steady-state operating point
    operating_conditions = {
        'q_in': 10.0,    # Flow rate (L/min)
        'CA_in': 1.0,    # Inlet concentration (mol/L)
        'T_in': 300.0,   # Inlet temperature (K)
        'T_cool': 285.0  # Coolant temperature (K)
    }
    
    ss = cstr.steady_state(operating_conditions)
    print(f"Steady-state: CA = {ss['CA']:.3f} mol/L, T = {ss['T']:.1f} K")

**Step 2: Design Primary (Temperature) Controller**

::

    # Linearize CSTR around operating point
    from process_control import LinearApproximation
    
    linear_cstr = LinearApproximation(cstr)
    u_nominal = [10.0, 1.0, 300.0, 285.0]  # [q, CA_in, T_in, T_cool]
    
    A, B = linear_cstr.linearize(u_nominal)
    
    # Extract temperature dynamics (T_cool -> T)
    # For FOPDT approximation from step test
    temp_params = {'K': -2.5, 'tau': 8.0, 'theta': 0.5}
    
    # Tune PI controller for temperature
    temp_pid = tune_pid(temp_params, method='amigo', controller_type='PI')
    temp_controller = PIDController(**temp_pid, output_limits=(270, 300))

**Step 3: Add Disturbance Rejection**

Test response to inlet temperature disturbances::

    # Simulation with inlet temperature disturbance
    time = np.linspace(0, 100, 1000)
    
    # Step disturbance in T_in at t=50
    T_in_profile = np.where(time < 50, 300.0, 305.0)
    
    # Simulate with temperature control
    temperatures = np.zeros_like(time)
    coolant_temps = np.zeros_like(time)
    temperatures[0] = ss['T']
    coolant_temps[0] = 285.0
    
    for i in range(1, len(time)):
        dt = time[i] - time[i-1]
        
        # Temperature controller
        T_setpoint = 350.0
        T_cool_cmd = temp_controller.update(T_setpoint, temperatures[i-1], dt)
        T_cool_cmd = max(270, min(T_cool_cmd, 300))  # Limit coolant temperature
        coolant_temps[i] = T_cool_cmd
        
        # Process dynamics
        inputs = [10.0, 1.0, T_in_profile[i-1], T_cool_cmd]
        states = [ss['CA'], temperatures[i-1]]  # Assume CA constant for simplicity
        
        derivatives = cstr.dynamics(time[i-1], states, inputs)
        temperatures[i] = temperatures[i-1] + derivatives[1] * dt
    
    # Plot results
    plt.figure(figsize=(12, 10))
    
    plt.subplot(3, 1, 1)
    plt.plot(time, T_in_profile, 'r:', label='T_in (Disturbance)')
    plt.ylabel('T_in (K)')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(3, 1, 2)
    plt.plot(time, temperatures, 'b-', label='Reactor Temperature')
    plt.axhline(y=350, color='r', linestyle='--', label='Setpoint')
    plt.ylabel('Temperature (K)')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(3, 1, 3)
    plt.plot(time, coolant_temps, 'g-', label='Coolant Temperature')
    plt.ylabel('T_cool (K)')
    plt.xlabel('Time (min)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

Tutorial 3: Optimization of Batch Process
------------------------------------------

Optimize a batch reactor operation for maximum profit.

**Objective:** Find optimal temperature profile for batch reactor

**Step 1: Define Batch Reactor Model**

::

    def batch_reactor_dynamics(t, state, temperature_profile):
        \"\"\"Batch reactor with temperature-dependent kinetics\"\"\"
        CA, CB = state
        
        # Get temperature at current time
        T = np.interp(t, temperature_profile['time'], temperature_profile['temp'])
        
        # Arrhenius kinetics: A -> B
        k = 1e8 * np.exp(-8000/T)  # Rate constant
        
        # Reaction rates
        rA = -k * CA
        rB = k * CA
        
        return [rA, rB]

**Step 2: Set up Optimization Problem**

::

    from process_control import Optimization
    from scipy.integrate import solve_ivp
    
    def objective_function(T_profile):
        \"\"\"Negative profit (for minimization)\"\"\"
        
        # Create temperature profile
        time_points = np.linspace(0, 120, 13)  # 0 to 120 min, 13 points
        temp_profile = {
            'time': time_points,
            'temp': T_profile
        }
        
        # Simulate batch reactor
        initial_state = [1.0, 0.0]  # CA0 = 1.0, CB0 = 0.0
        
        sol = solve_ivp(
            lambda t, y: batch_reactor_dynamics(t, y, temp_profile),
            [0, 120],
            initial_state,
            dense_output=True
        )
        
        # Final concentrations
        final_state = sol.y[:, -1]
        CB_final = final_state[1]
        
        # Profit calculation
        product_value = CB_final * 1000 * 100  # $/mol * mol/L * L
        
        # Energy cost (higher temperature = higher cost)
        avg_temp = np.mean(T_profile)
        energy_cost = (avg_temp - 300) * 0.1 * 120  # $/K/min * K * min
        
        profit = product_value - energy_cost
        
        return -profit  # Negative for minimization

**Step 3: Solve Optimization**

::

    from scipy.optimize import minimize
    
    # Initial guess - constant temperature
    initial_temp_profile = np.ones(13) * 320  # 320 K
    
    # Constraints - temperature limits
    bounds = [(300, 400) for _ in range(13)]  # 300-400 K for each point
    
    # Optimize
    result = minimize(
        objective_function,
        initial_temp_profile,
        method='L-BFGS-B',
        bounds=bounds
    )
    
    optimal_temps = result.x
    max_profit = -result.fun
    
    print(f"Maximum profit: ${max_profit:.2f}")
    print(f"Optimal temperature profile:")
    
    time_points = np.linspace(0, 120, 13)
    for i, (t, T) in enumerate(zip(time_points, optimal_temps)):
        print(f"  t={t:5.1f} min: T={T:5.1f} K")

**Step 4: Analyze Results**

::

    # Compare optimal vs. constant temperature operation
    plt.figure(figsize=(12, 8))
    
    # Plot optimal temperature profile
    plt.subplot(2, 2, 1)
    plt.plot(time_points, optimal_temps, 'ro-', label='Optimal')
    plt.axhline(y=320, color='b', linestyle='--', label='Constant (320K)')
    plt.ylabel('Temperature (K)')
    plt.xlabel('Time (min)')
    plt.legend()
    plt.grid(True)
    plt.title('Temperature Profiles')
    
    # Simulate both cases and plot concentrations
    # ... (simulation code)
    
    plt.tight_layout()
    plt.show()

Next Steps
----------

After completing these tutorials, you should be able to:

1. **Model chemical processes** using the provided classes
2. **Design PID controllers** with automated tuning
3. **Analyze system performance** using frequency domain methods
4. **Optimize process operations** for economic objectives

Continue with:

* **Advanced Examples** - More complex multi-unit processes
* **Theory Section** - Mathematical background on control concepts
* **API Reference** - Detailed documentation of all functions and classes

For more advanced topics, explore:

* **Model Predictive Control** for multivariable processes
* **Batch Scheduling** for campaign optimization
* **Nonlinear Control** for highly nonlinear processes
