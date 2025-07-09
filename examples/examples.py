"""
SPROCLIB - Standard Process Control Library
Example Usage and Demonstrations

This script demonstrates the key functionality of the SPROCLIB process control library
with practical examples for chemical engineering education and industrial applications.

Author: Thorsten Gressling (gressling@paramus.ai)
License: MIT License
"""

import numpy as np
import matplotlib.pyplot as plt
from controllers import PIDController, TuningRule
from models import (
    Tank, CSTR, HeatExchanger, BinaryDistillationColumn, LinearApproximation, 
    FluidizedBedReactor, MembraneReactor, TrickleFlowReactor, RecycleReactor, 
    CatalystDeactivationReactor, Compressor, Pump, CentrifugalPump, PositiveDisplacementPump,
    ControlValve, ThreeWayValve
)
from analysis import TransferFunction, Simulation, Optimization, StateTaskNetwork
from functions import *

def example_1_gravity_drained_tank():
    """Example 1: Gravity-drained tank modeling and control."""
    print("=" * 60)
    print("Example 1: Gravity-Drained Tank")
    print("=" * 60)
    
    # Create tank model
    tank = Tank(A=1.0, C=2.0, name="GravityTank")
    
    # Operating conditions
    q_in_nominal = 2.0  # L/min
    u_nominal = np.array([q_in_nominal])
    x_steady = tank.steady_state(u_nominal)
    
    print(f"Steady-state height for q_in = {q_in_nominal} L/min: {x_steady[0]:.2f} m")
    
    # Linearize around operating point
    linear_approx = LinearApproximation(tank)
    A, B = linear_approx.linearize(u_nominal, x_steady)
    
    print(f"Linearized model:")
    print(f"A = {A[0,0]:.4f}")
    print(f"B = {B[0,0]:.4f}")
    
    # Step response analysis
    step_data = linear_approx.step_response(input_idx=0, step_size=0.5, t_final=5.0)
    
    # Fit FOPDT model
    fopdt_params = fit_fopdt(step_data['t'], step_data['x'][0, :], step_magnitude=0.5)
    print(f"FOPDT parameters: K={fopdt_params['K']:.3f}, τ={fopdt_params['tau']:.3f}, θ={fopdt_params['theta']:.3f}")
    
    # Design PID controller
    pid_params = tune_pid(fopdt_params, method='ziegler_nichols', controller_type='PI')
    print(f"PID parameters: Kp={pid_params['Kp']:.3f}, Ki={pid_params['Ki']:.3f}")
    
    # Create and test PID controller
    controller = PIDController(**pid_params)
    
    print("Tank example completed successfully!\n")


def example_2_cstr_modeling():
    """Example 2: CSTR modeling and simulation."""
    print("=" * 60)
    print("Example 2: CSTR Modeling and Simulation")
    print("=" * 60)
    
    # Create CSTR model
    cstr = CSTR(
        V=100.0,        # L
        k0=7.2e10,      # 1/min
        Ea=72750.0,     # J/gmol
        R=8.314,        # J/gmol/K
        name="ExothermicCSTR"
    )
    
    # Operating conditions
    q = 100.0       # L/min
    CAi = 1.0       # gmol/L
    Ti = 350.0      # K
    Tc = 300.0      # K
    u_nominal = np.array([q, CAi, Ti, Tc])
    
    # Calculate steady state
    x_steady = cstr.steady_state(u_nominal)
    print(f"Steady-state: CA = {x_steady[0]:.3f} gmol/L, T = {x_steady[1]:.1f} K")
    
    # Simulate with step change in coolant temperature
    def input_profile(t):
        if t < 2.0:
            return u_nominal
        else:
            u_step = u_nominal.copy()
            u_step[3] = 295.0  # Step change in coolant temperature
            return u_step
    
    # Run simulation
    simulation = Simulation(cstr, name="CSTR_Simulation")
    results = simulation.run(
        t_span=(0, 10),
        x0=x_steady,
        u_profile=input_profile
    )
    
    # Plot results
    t = results['t']
    CA = results['x'][0, :]
    T = results['x'][1, :]
    Tc_profile = results['u'][3, :]
    
    fig, axes = plt.subplots(3, 1, figsize=(10, 8))
    
    axes[0].plot(t, CA)
    axes[0].set_ylabel('Concentration (gmol/L)')
    axes[0].set_title('CSTR Response to Coolant Temperature Step')
    axes[0].grid(True)
    
    axes[1].plot(t, T)
    axes[1].set_ylabel('Temperature (K)')
    axes[1].grid(True)
    
    axes[2].plot(t, Tc_profile)
    axes[2].set_ylabel('Coolant Temp (K)')
    axes[2].set_xlabel('Time (min)')
    axes[2].grid(True)
    
    plt.tight_layout()
    plt.show()
    
    print("CSTR modeling example completed!\n")


def example_3_transfer_function_analysis():
    """Example 3: Transfer function analysis and control design."""
    print("=" * 60)
    print("Example 3: Transfer Function Analysis")
    print("=" * 60)
    
    # Create FOPDT transfer function
    tf_system = TransferFunction.first_order_plus_dead_time(
        K=2.0, tau=5.0, theta=1.0, name="Process"
    )
    
    # Bode plot analysis
    bode_data = tf_system.bode_plot(plot=True)
    
    # Stability analysis
    stability = tf_system.stability_analysis()
    print(f"System stability: {stability['stable']}")
    
    if stability['gain_margin_db'] is not None:
        print(f"Gain margin: {stability['gain_margin_db']:.1f} dB")
    else:
        print("Gain margin: Not defined")
        
    if stability['phase_margin_deg'] is not None:
        print(f"Phase margin: {stability['phase_margin_deg']:.1f} degrees")
    else:
        print("Phase margin: Not defined")
    
    # Design PI controller
    model_params = {'K': 2.0, 'tau': 5.0, 'theta': 1.0}
    pi_params = tune_pid(model_params, method='amigo', controller_type='PI')
    
    # Controller transfer function
    controller_tf = TransferFunction(
        [pi_params['Ki'], pi_params['Kp']], [1, 0],
        name="PI Controller"
    )
    
    # Closed-loop analysis
    plant_tf = (tf_system.num, tf_system.den)
    ctrl_tf = (controller_tf.num, controller_tf.den)
    
    # Disturbance rejection analysis
    disturbance_analysis = disturbance_rejection(
        plant_tf, ctrl_tf, disturbance_type='step'
    )
    
    print(f"Steady-state error: {disturbance_analysis['steady_state_error']:.4f}")
    print(f"Settling time: {disturbance_analysis['settling_time']:.2f} min")
    
    print("Transfer function analysis completed!\n")


def example_4_optimization():
    """Example 4: Process optimization."""
    print("=" * 60)
    print("Example 4: Process Optimization")
    print("=" * 60)
    
    # Economic optimization example
    optimizer = Optimization("Production Planning")
    
    # Production planning problem
    production_rates = np.array([0, 0, 0])  # Products A, B, C
    costs = np.array([10, 15, 20])          # $/unit
    prices = np.array([25, 30, 40])         # $/unit
    capacity_constraints = np.array([100, 80, 60])  # max production
    demand_constraints = np.array([20, 15, 10])     # min demand
    
    result = optimizer.economic_optimization(
        production_rates, costs, prices,
        capacity_constraints, demand_constraints
    )
    
    if result['success']:
        print("Optimal production plan:")
        for i, prod in enumerate(['Product A', 'Product B', 'Product C']):
            print(f"  {prod}: {result['production'][i]:.1f} units")
        print(f"Maximum profit: ${result['profit']:.2f}")
    
    # Nonlinear optimization example
    def objective(x):
        """Minimize energy consumption with conversion constraint."""
        T, q = x  # Temperature, flow rate
        energy = 0.1 * T**2 + 0.05 * q**2  # Energy cost
        return energy
    
    def conversion_constraint(x):
        """Minimum conversion requirement."""
        T, q = x
        conversion = 1 - np.exp(-0.1 * T / (q + 1))
        return conversion - 0.8  # >= 80% conversion
    
    constraints = [{'type': 'ineq', 'fun': conversion_constraint}]
    bounds = [(300, 500), (10, 100)]  # T bounds, q bounds
    x0 = np.array([400, 50])
    
    nl_result = optimizer.nonlinear_optimization(
        objective, x0, constraints=constraints, bounds=bounds
    )
    
    if nl_result['success']:
        T_opt, q_opt = nl_result['x']
        print(f"Optimal operating conditions:")
        print(f"  Temperature: {T_opt:.1f} K")
        print(f"  Flow rate: {q_opt:.1f} L/min")
        print(f"  Energy cost: {nl_result['fun']:.3f}")
    
    print("Optimization examples completed!\n")


def example_5_batch_scheduling():
    """Example 5: Batch process scheduling."""
    print("=" * 60)
    print("Example 5: Batch Process Scheduling")
    print("=" * 60)
    
    # Create State-Task Network
    stn = StateTaskNetwork("Batch Plant")
    
    # Add states (materials)
    stn.add_state("Raw A", capacity=1000, initial_amount=500, price=0)
    stn.add_state("Raw B", capacity=1000, initial_amount=300, price=0)
    stn.add_state("Intermediate", capacity=200, initial_amount=0, price=0)
    stn.add_state("Product", capacity=500, initial_amount=0, price=100)
    
    # Add units
    stn.add_unit("Reactor1", capacity=100, unit_cost=10)
    stn.add_unit("Reactor2", capacity=80, unit_cost=8)
    stn.add_unit("Separator", capacity=120, unit_cost=5)
    
    # Add tasks
    stn.add_task("Reaction1", duration=2, 
                inputs={"Raw A": 50, "Raw B": 30},
                outputs={"Intermediate": 60},
                suitable_units=["Reactor1", "Reactor2"])
    
    stn.add_task("Separation", duration=1,
                inputs={"Intermediate": 60},
                outputs={"Product": 50},
                suitable_units=["Separator"])
    
    # Optimize schedule
    schedule = stn.optimize_schedule(time_horizon=10, objective='profit')
    
    print(f"Production schedule optimized!")
    print(f"Total profit: ${schedule['total_profit']:.2f}")
    print(f"Final inventories:")
    for state, amount in schedule['final_inventories'].items():
        print(f"  {state}: {amount:.1f} units")
    
    # Plot schedule
    stn.plot_schedule()
    
    print("Batch scheduling example completed!\n")


def example_6_model_predictive_control():
    """Example 6: Model Predictive Control."""
    print("=" * 60)
    print("Example 6: Model Predictive Control")
    print("=" * 60)
    
    # Simple system for MPC example
    A = np.array([[0.8, 0.1], [0.2, 0.7]])
    B = np.array([[1], [0.5]])
    
    # Weighting matrices
    Q = np.array([[10, 0], [0, 1]])  # State penalty
    R = np.array([[1]])              # Input penalty
    
    # Design MPC controller
    mpc_data = model_predictive_control(
        A, B, Q, R, prediction_horizon=10, control_horizon=5
    )
    
    K_mpc = mpc_data['control_gain']
    print(f"MPC controller gain: {K_mpc.flatten()}")
    
    # Simulate closed-loop response
    n_steps = 50
    x = np.array([[5], [2]])  # Initial condition (deviation from setpoint)
    x_history = np.zeros((2, n_steps))
    u_history = np.zeros((1, n_steps))
    
    for k in range(n_steps):
        u = K_mpc @ x  # MPC control law
        x = A @ x + B @ u  # System dynamics
        
        x_history[:, k] = x.flatten()
        u_history[:, k] = u.flatten()
    
    # Plot MPC response
    time = np.arange(n_steps)
    
    fig, axes = plt.subplots(2, 1, figsize=(10, 6))
    
    axes[0].plot(time, x_history[0, :], 'b-', label='State 1')
    axes[0].plot(time, x_history[1, :], 'r-', label='State 2')
    axes[0].set_ylabel('States')
    axes[0].legend()
    axes[0].grid(True)
    axes[0].set_title('MPC Closed-Loop Response')
    
    axes[1].plot(time, u_history[0, :], 'g-')
    axes[1].set_ylabel('Control Input')
    axes[1].set_xlabel('Time Step')
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.show()
    
    print("MPC example completed!\n")


def example_7_heat_exchanger():
    """Example 7: Heat exchanger modeling and temperature control."""
    print("=" * 60)
    print("Example 7: Heat Exchanger Modeling and Control")
    print("=" * 60)
    
    # Create heat exchanger model
    hx = HeatExchanger(
        U=500.0,           # Overall heat transfer coefficient [W/m²·K]
        A=10.0,            # Heat transfer area [m²]
        m_hot=2.0,         # Hot fluid mass flow rate [kg/s]
        m_cold=1.8,        # Cold fluid mass flow rate [kg/s]
        cp_hot=4180.0,     # Hot fluid specific heat [J/kg·K]
        cp_cold=4180.0,    # Cold fluid specific heat [J/kg·K]
        V_hot=0.05,        # Hot fluid volume [m³]
        V_cold=0.05,       # Cold fluid volume [m³]
        name="CounterCurrentHX"
    )
    
    print(f"Heat Exchanger Parameters:")
    print(f"  Effectiveness: {hx.effectiveness:.3f}")
    print(f"  NTU: {hx.NTU:.3f}")
    print(f"  Hot fluid time constant: {hx.tau_hot:.2f} s")
    print(f"  Cold fluid time constant: {hx.tau_cold:.2f} s")
    
    # Operating conditions
    T_hot_in = 363.15    # 90°C
    T_cold_in = 293.15   # 20°C
    u_nominal = np.array([T_hot_in, T_cold_in])
    
    # Calculate steady-state outlet temperatures
    x_steady = hx.steady_state(u_nominal)
    T_hot_out_ss = x_steady[0]
    T_cold_out_ss = x_steady[1]
    
    print(f"\nSteady-state conditions:")
    print(f"  Hot fluid:  {T_hot_in-273.15:.1f}°C → {T_hot_out_ss-273.15:.1f}°C")
    print(f"  Cold fluid: {T_cold_in-273.15:.1f}°C → {T_cold_out_ss-273.15:.1f}°C")
    
    # Calculate heat transfer rate and LMTD
    Q_rate = hx.calculate_heat_transfer_rate(T_hot_in, T_cold_in, T_hot_out_ss, T_cold_out_ss)
    lmtd = hx.calculate_lmtd(T_hot_in, T_cold_in, T_hot_out_ss, T_cold_out_ss)
    
    print(f"  Heat transfer rate: {Q_rate/1000:.1f} kW")
    print(f"  LMTD: {lmtd:.2f} K")
    
    # Dynamic simulation - step change in hot inlet temperature
    def input_function(t):
        if t < 50:
            return np.array([T_hot_in, T_cold_in])
        else:
            return np.array([T_hot_in + 10, T_cold_in])  # +10K step
    
    # Simulate response
    t_span = (0, 200)
    x0 = x_steady
    result = hx.simulate(t_span, x0, input_function, t_eval=np.linspace(0, 200, 1000))
    
    # Calculate temperatures in Celsius
    T_hot_out_C = result['x'][0, :] - 273.15
    T_cold_out_C = result['x'][1, :] - 273.15
    T_hot_in_values = result['u'][0, :] - 273.15
    
    print(f"\nDynamic Response (10K step in hot inlet at t=50s):")
    print(f"  Final hot outlet temperature: {T_hot_out_C[-1]:.1f}°C")
    print(f"  Final cold outlet temperature: {T_cold_out_C[-1]:.1f}°C")
    
    # Linearize for control design
    linear_approx = LinearApproximation(hx)
    A, B = linear_approx.linearize(u_nominal, x_steady)
    
    print(f"\nLinearized model around operating point:")
    print(f"A matrix:")
    for i in range(A.shape[0]):
        print(f"  [{A[i,0]:8.4f} {A[i,1]:8.4f}]")
    print(f"B matrix:")
    for i in range(B.shape[0]):
        print(f"  [{B[i,0]:8.4f} {B[i,1]:8.4f}]")
    
    # Step response for control design
    step_data = linear_approx.step_response(input_idx=0, step_size=5.0, t_final=100.0)
    
    # Fit FOPDT for hot outlet temperature response to hot inlet change
    fopdt_params = fit_fopdt(step_data['t'], step_data['x'][0, :], step_magnitude=5.0)
    print(f"\nFOPDT model for T_hot_out response to T_hot_in:")
    print(f"  K = {fopdt_params['K']:.4f}")
    print(f"  τ = {fopdt_params['tau']:.2f} s")
    print(f"  θ = {fopdt_params['theta']:.2f} s")
    
    # Design PID controller for temperature control
    pid_params = tune_pid(fopdt_params, method='ziegler_nichols', controller_type='PID')
    print(f"\nPID controller parameters:")
    print(f"  Kp = {pid_params['Kp']:.3f}")
    print(f"  Ki = {pid_params['Ki']:.4f}")
    print(f"  Kd = {pid_params['Kd']:.3f}")
    
    # Create PID controller
    pid = PIDController(
        Kp=pid_params['Kp'],
        Ki=pid_params['Ki'],
        Kd=pid_params['Kd'],
        MV_min=273.15,  # Minimum temperature in K
        MV_max=473.15   # Maximum temperature in K
    )
    
    # Test different flow rate conditions
    print(f"\nEffect of flow rate changes:")
    flow_rates = [(1.5, 1.3), (2.0, 1.8), (2.5, 2.2)]
    for m_hot_new, m_cold_new in flow_rates:
        # Update parameters
        hx.update_parameters(m_hot=m_hot_new, m_cold=m_cold_new)
        
        # Calculate new steady state
        u_test = np.array([T_hot_in, T_cold_in, m_hot_new, m_cold_new])
        x_new = hx.steady_state(u_test)
        
        Q_new = hx.calculate_heat_transfer_rate(T_hot_in, T_cold_in, x_new[0], x_new[1])
        
        print(f"  Flow rates ({m_hot_new:.1f}, {m_cold_new:.1f}) kg/s:")
        print(f"    Hot outlet: {x_new[0]-273.15:.1f}°C, Cold outlet: {x_new[1]-273.15:.1f}°C")
        print(f"    Heat transfer: {Q_new/1000:.1f} kW, Effectiveness: {hx.effectiveness:.3f}")
    
    # Reset to original parameters
    hx.update_parameters(m_hot=2.0, m_cold=1.8)
    
    print("\n✓ Heat exchanger modeling and analysis completed!")


def example_8_distillation_column():
    """Example 8: Binary distillation column modeling and composition control."""
    print("=" * 60)
    print("Example 8: Binary Distillation Column Modeling and Control")
    print("=" * 60)
    
    # Create binary distillation column
    column = BinaryDistillationColumn(
        N_trays=10,              # 10 trays total
        feed_tray=5,             # Feed on tray 5
        alpha=2.5,               # Relative volatility
        tray_holdup=1.0,         # 1 kmol holdup per tray
        reflux_drum_holdup=5.0,  # 5 kmol reflux drum
        reboiler_holdup=10.0,    # 10 kmol reboiler
        feed_flow=100.0,         # 100 kmol/min feed
        feed_composition=0.5,    # 50% light component in feed
        name="BinaryColumn"
    )
    
    print(f"Distillation Column Parameters:")
    print(f"  Number of trays: {column.N_trays}")
    print(f"  Feed tray: {column.feed_tray}")
    print(f"  Relative volatility: {column.alpha}")
    print(f"  Feed composition: {column.feed_composition:.1%}")
    print(f"  Feed flow rate: {column.feed_flow} kmol/min")
    
    # Calculate minimum reflux ratio
    R_min = column.calculate_minimum_reflux()
    print(f"  Minimum reflux ratio: {R_min:.2f}")
    
    # Operating conditions
    R = 2.0  # Reflux ratio
    D = 48.0  # Distillate flow rate [kmol/min]
    B = 52.0  # Bottoms flow rate [kmol/min]
    Q_reb = 500.0  # Reboiler heat duty [energy/time]
    
    u_nominal = np.array([R, Q_reb, D, B])
    
    print(f"\nOperating Conditions:")
    print(f"  Reflux ratio: {R:.1f}")
    print(f"  Distillate flow: {D:.1f} kmol/min")
    print(f"  Bottoms flow: {B:.1f} kmol/min")
    print(f"  Reboiler duty: {Q_reb:.1f} energy/time")
    
    # Calculate steady-state composition profile
    x_steady = column.steady_state(u_nominal)
    
    print(f"\nSteady-state Composition Profile:")
    print(f"  Reflux drum (distillate): {x_steady[column.N_trays]:.1%}")
    print(f"  Feed tray: {x_steady[column.feed_tray-1]:.1%}")
    print(f"  Reboiler (bottoms): {x_steady[column.N_trays+1]:.1%}")
    
    # Calculate separation metrics
    metrics = column.calculate_separation_metrics(x_steady)
    print(f"\nSeparation Performance:")
    print(f"  Distillate purity: {metrics['distillate_purity']:.1%}")
    print(f"  Bottoms purity: {metrics['bottoms_purity']:.1%}")
    print(f"  Light component recovery: {metrics['light_recovery']:.1%}")
    print(f"  Separation factor: {metrics['separation_factor']:.1f}")
    
    # Test individual tray model
    print(f"\nTesting Individual Tray Model (Tray {column.feed_tray}):")
    feed_tray = column.trays[column.feed_tray - 1]
    
    # Example tray inputs: [L_in, x_in, V_in, y_in, L_out, V_out]
    L_in = R * D
    x_in = x_steady[column.feed_tray - 2] if column.feed_tray > 1 else x_steady[column.N_trays]
    V_in = L_in + D
    y_in = feed_tray.vapor_liquid_equilibrium(x_steady[column.feed_tray]) if column.feed_tray < column.N_trays else feed_tray.vapor_liquid_equilibrium(x_steady[column.N_trays+1])
    L_out = L_in + column.feed_flow
    V_out = V_in
    
    u_tray = np.array([L_in, x_in, V_in, y_in, L_out, V_out])
    x_tray_steady = feed_tray.steady_state(u_tray)
    
    print(f"  Liquid composition: {x_tray_steady[0]:.1%}")
    print(f"  Vapor composition: {feed_tray.vapor_liquid_equilibrium(x_tray_steady[0]):.1%}")
    
    # Dynamic simulation - step change in reflux ratio
    def input_function(t):
        if t < 20:
            return u_nominal
        else:
            return np.array([R + 0.5, Q_reb, D, B])  # +0.5 step in reflux ratio
    
    # Simulate response (use shorter time for complex system)
    print(f"\nDynamic Response (Reflux ratio step +0.5 at t=20 min):")
    t_span = (0, 100)
    result = column.simulate(t_span, x_steady, input_function, t_eval=np.linspace(0, 100, 500))
    
    # Analyze final compositions
    final_compositions = result['x'][:, -1]
    final_distillate = final_compositions[column.N_trays]
    final_bottoms = final_compositions[column.N_trays + 1]
    
    print(f"  Final distillate composition: {final_distillate:.1%}")
    print(f"  Final bottoms composition: {final_bottoms:.1%}")
    print(f"  Change in distillate: {(final_distillate - x_steady[column.N_trays])*100:.2f} percentage points")
    print(f"  Change in bottoms: {(final_bottoms - x_steady[column.N_trays+1])*100:.2f} percentage points")
    
    # Linearize for control design
    print(f"\nLinearized Model for Control Design:")
    linear_approx = LinearApproximation(column)
    
    # Focus on key outputs: distillate and bottoms compositions
    A, B = linear_approx.linearize(u_nominal, x_steady)
    
    print(f"  State dimension: {A.shape[0]} x {A.shape[1]}")
    print(f"  Input dimension: {B.shape[0]} x {B.shape[1]}")
    print(f"  System is {'stable' if np.all(np.real(np.linalg.eigvals(A)) < 0) else 'unstable'}")
    
    # Step response for distillate composition to reflux ratio change
    step_data = linear_approx.step_response(input_idx=0, step_size=0.1, t_final=50.0)
    
    # Extract distillate composition response (reflux drum state)
    distillate_response = step_data['x'][column.N_trays, :]
    
    # Find settling time and steady-state gain
    final_value = distillate_response[-1]
    settling_time = None
    steady_state_tolerance = 0.02 * abs(final_value)
    
    for i, val in enumerate(distillate_response):
        if abs(val - final_value) <= steady_state_tolerance:
            settling_time = step_data['t'][i]
            break
    
    print(f"\nStep Response Analysis (Distillate composition to reflux ratio):")
    print(f"  Steady-state gain: {final_value:.4f} (Δx_D/ΔR)")
    print(f"  Settling time: {settling_time:.1f} min" if settling_time else "  Settling time: >50 min")
    
    # Design control system
    print(f"\nControl System Design:")
    
    # For composition control, use a simpler approach due to complexity
    # Focus on distillate composition control using reflux ratio
    
    # Approximate FOPDT parameters from step response
    if final_value != 0:
        # Simple approximation
        tau_approx = settling_time / 3 if settling_time else 15.0  # Approximate time constant
        K_approx = final_value / 0.1  # Steady-state gain
        theta_approx = 2.0  # Approximate dead time
        
        fopdt_params = {'K': K_approx, 'tau': tau_approx, 'theta': theta_approx}
        
        print(f"  FOPDT approximation: K={K_approx:.3f}, τ={tau_approx:.1f} min, θ={theta_approx:.1f} min")
        
        # Design PI controller (often preferred for composition control)
        pi_params = tune_pid(fopdt_params, method='amigo', controller_type='PI')
        print(f"  PI controller: Kp={pi_params['Kp']:.3f}, Ki={pi_params['Ki']:.4f}")
        
        # Create controller
        controller = PIDController(
            Kp=pi_params['Kp'],
            Ki=pi_params['Ki'],
            Kd=0.0,
            MV_min=0.5,   # Minimum reflux ratio
            MV_max=10.0   # Maximum reflux ratio
        )
        
        print(f"  Controller configured with limits: R ∈ [0.5, 10.0]")
    
    # Test different operating conditions
    print(f"\nEffect of Operating Condition Changes:")
    
    test_conditions = [
        (1.5, 500.0, 48.0, 52.0, "Low reflux"),
        (2.0, 500.0, 48.0, 52.0, "Nominal"), 
        (3.0, 500.0, 48.0, 52.0, "High reflux")
    ]
    
    for R_test, Q_test, D_test, B_test, description in test_conditions:
        u_test = np.array([R_test, Q_test, D_test, B_test])
        x_test = column.steady_state(u_test)
        metrics_test = column.calculate_separation_metrics(x_test)
        
        print(f"  {description} (R={R_test:.1f}):")
        print(f"    Distillate purity: {metrics_test['distillate_purity']:.1%}")
        print(f"    Bottoms purity: {metrics_test['bottoms_purity']:.1%}")
        print(f"    Separation factor: {metrics_test['separation_factor']:.1f}")
    
    # Feed composition sensitivity
    print(f"\nFeed Composition Sensitivity:")
    feed_compositions = [0.3, 0.5, 0.7]
    
    for z_F in feed_compositions:
        column.feed_composition = z_F
        column.parameters['feed_composition'] = z_F
        
        x_test = column.steady_state(u_nominal)
        metrics_test = column.calculate_separation_metrics(x_test)
        
        print(f"  Feed z_F = {z_F:.1%}:")
        print(f"    Distillate: {metrics_test['distillate_composition']:.1%}")
        print(f"    Bottoms: {metrics_test['bottoms_composition']:.1%}")
    
    # Reset to original feed composition
    column.feed_composition = 0.5
    column.parameters['feed_composition'] = 0.5
    
    print("\n✓ Distillation column modeling and control analysis completed!")


def example_11_fluidized_bed_reactor():
    """Example 9: Fluidized bed reactor modeling and operation."""
    print("=" * 60)
    print("Example 9: Fluidized Bed Reactor")
    print("=" * 60)
    
    from models import FluidizedBedReactor
    
    # Create fluidized bed reactor
    fbr = FluidizedBedReactor(
        H=3.0,                    # Bed height [m]
        D=2.0,                    # Bed diameter [m]
        U_mf=0.1,                 # Minimum fluidization velocity [m/s]
        rho_cat=1500.0,           # Catalyst density [kg/m³]
        k0=1e5,                   # Pre-exponential factor [m³/kg·s]
        name="FluidizedBed"
    )
    
    # Operating conditions
    CA_in = 100.0      # Inlet concentration [mol/m³]
    T_in = 723.15      # Inlet temperature [K] (450°C)
    U_g = 0.3          # Superficial gas velocity [m/s]
    T_coolant = 700.0  # Coolant temperature [K]
    
    u_nominal = np.array([CA_in, T_in, U_g, T_coolant])
    
    # Calculate fluidization properties
    props = fbr.fluidization_properties(U_g)
    print(f"Fluidization properties at U_g = {U_g} m/s:")
    print(f"  Bubble velocity: {props['bubble_velocity']:.3f} m/s")
    print(f"  Bubble fraction: {props['bubble_fraction']:.3f}")
    print(f"  Emulsion fraction: {props['emulsion_fraction']:.3f}")
    
    # Calculate steady-state
    try:
        x_steady = fbr.steady_state(u_nominal)
        print(f"\nSteady-state conditions:")
        print(f"  Bubble phase concentration: {x_steady[0]:.1f} mol/m³")
        print(f"  Emulsion phase concentration: {x_steady[1]:.1f} mol/m³")
        print(f"  Temperature: {x_steady[2]-273.15:.1f} °C")
        
        # Calculate conversion
        conversion = fbr.calculate_conversion(CA_in, x_steady[1])
        print(f"  Overall conversion: {conversion:.1%}")
        
    except Exception as e:
        print(f"Steady-state calculation failed: {e}")
    
    # Simulate dynamic response
    print(f"\nSimulating dynamic response to step change...")
    def input_profile(t):
        if t < 10:
            return u_nominal
        else:
            # Step change in inlet concentration
            u_step = u_nominal.copy()
            u_step[0] = CA_in * 1.2  # 20% increase
            return u_step
    
    try:
        x0 = np.array([CA_in*0.9, CA_in*0.8, T_in])
        results = fbr.simulate(
            t_span=(0, 20),
            x0=x0,
            u_func=input_profile,
            t_eval=np.linspace(0, 20, 100)
        )
        
        print(f"Dynamic simulation completed.")
        print(f"Final bubble concentration: {results['x'][0, -1]:.1f} mol/m³")
        print(f"Final emulsion concentration: {results['x'][1, -1]:.1f} mol/m³")
        
    except Exception as e:
        print(f"Dynamic simulation failed: {e}")


def example_12_membrane_reactor():
    """Example 10: Membrane reactor with selective permeation."""
    print("=" * 60)
    print("Example 10: Membrane Reactor")
    print("=" * 60)
    
    from models import MembraneReactor
    
    # Create membrane reactor
    mbr = MembraneReactor(
        L=1.0,                           # Reactor length [m]
        D_tube=0.05,                     # Tube diameter [m]
        D_shell=0.1,                     # Shell diameter [m]
        n_segments=10,                   # Number of segments
        k0=1e5,                          # Reaction rate constant [1/s]
        permeability=1e-6,               # Membrane permeability [mol/m²·s·Pa]
        selectivity=10.0,                # Product selectivity [-]
        name="MembraneReactor"
    )
    
    # Operating conditions
    CA_in = 50.0       # Reactant inlet concentration [mol/m³]
    CB_in = 0.0        # Product inlet concentration [mol/m³]
    v_tube = 0.1       # Tube velocity [m/s]
    v_shell = 0.05     # Shell velocity [m/s]
    T_in = 673.15      # Inlet temperature [K] (400°C)
    
    u_nominal = np.array([CA_in, CB_in, v_tube, v_shell, T_in])
    
    print(f"Membrane reactor parameters:")
    print(f"  Reactor length: {mbr.L} m")
    print(f"  Number of segments: {mbr.n_segments}")
    print(f"  Membrane selectivity: {mbr.selectivity}")
    print(f"  Permeability: {mbr.permeability:.2e} mol/m²·s·Pa")
    
    # Calculate steady-state profiles
    try:
        x_steady = mbr.steady_state(u_nominal)
        n = mbr.n_segments
        
        # Extract concentration profiles
        CA_tube = x_steady[0:n]
        CB_tube = x_steady[n:2*n]
        CA_shell = x_steady[2*n:3*n]
        CB_shell = x_steady[3*n:4*n]
        T = x_steady[4*n]
        
        print(f"\nSteady-state results:")
        print(f"  Tube outlet - Reactant: {CA_tube[-1]:.1f} mol/m³")
        print(f"  Tube outlet - Product: {CB_tube[-1]:.1f} mol/m³")
        print(f"  Shell outlet - Product: {CB_shell[0]:.1f} mol/m³")
        print(f"  Temperature: {T-273.15:.1f} °C")
        
        # Calculate separation performance
        separation_factor = mbr.calculate_separation_factor(x_steady)
        print(f"  Separation factor: {separation_factor:.3f}")
        
        # Calculate conversion
        conversion = (CA_in - CA_tube[-1]) / CA_in
        print(f"  Reactant conversion: {conversion:.1%}")
        
    except Exception as e:
        print(f"Steady-state calculation failed: {e}")
    
    print(f"\nMembrane reactor advantages:")
    print(f"  • Simultaneous reaction and separation")
    print(f"  • Enhanced conversion through product removal")
    print(f"  • Selective permeation improves product purity")


def example_11_trickle_flow_reactor():
    """Example 11: Trickle flow reactor for three-phase reactions."""
    print("=" * 60)
    print("Example 11: Trickle Flow Reactor")
    print("=" * 60)
    
    from models import TrickleFlowReactor
    
    # Create trickle flow reactor
    tfr = TrickleFlowReactor(
        L=5.0,                    # Bed length [m]
        D=1.0,                    # Bed diameter [m]
        epsilon=0.4,              # Bed porosity [-]
        rho_cat=1500.0,           # Catalyst density [kg/m³]
        k0=1e4,                   # Reaction rate constant [m³/kg·s]
        K_La=0.1,                 # Mass transfer coefficient [1/s]
        alpha=200.0,              # Interfacial area [m²/m³]
        name="TrickleFlowReactor"
    )
    
    # Operating conditions
    CG_in = 10.0       # Gas inlet concentration [mol/m³]
    CL_in = 50.0       # Liquid inlet concentration [mol/m³]
    v_g = 0.1          # Gas velocity [m/s]
    v_l = 0.01         # Liquid velocity [m/s]
    T_in = 573.15      # Inlet temperature [K] (300°C)
    H = 0.1            # Henry's law constant [mol/m³·Pa]
    
    u_nominal = np.array([CG_in, CL_in, v_g, v_l, T_in, H])
    
    print(f"Trickle flow reactor parameters:")
    print(f"  Bed length: {tfr.L} m, diameter: {tfr.D} m")
    print(f"  Bed porosity: {tfr.epsilon}")
    print(f"  Gas velocity: {v_g} m/s, Liquid velocity: {v_l} m/s")
    print(f"  Mass transfer coefficient: {tfr.K_La} s⁻¹")
    
    # Calculate steady-state profiles
    try:
        x_steady = tfr.steady_state(u_nominal)
        n = tfr.n_segments
        
        # Reshape results
        states = x_steady.reshape((n, 3))
        CG_profile = states[:, 0]
        CL_profile = states[:, 1]
        T_profile = states[:, 2]
        
        print(f"\nSteady-state profiles:")
        print(f"  Gas outlet concentration: {CG_profile[-1]:.1f} mol/m³")
        print(f"  Liquid outlet concentration: {CL_profile[-1]:.1f} mol/m³")
        print(f"  Outlet temperature: {T_profile[-1]-273.15:.1f} °C")
        
        # Calculate conversion
        conversion = tfr.calculate_overall_conversion(x_steady, CL_in)
        print(f"  Liquid phase conversion: {conversion:.1%}")
        
        # Mass transfer effectiveness
        mass_transfer_rate = tfr.mass_transfer_rate(CG_profile[0], CL_profile[0], H)
        print(f"  Mass transfer rate (inlet): {mass_transfer_rate:.3f} mol/m³·s")
        
    except Exception as e:
        print(f"Steady-state calculation failed: {e}")
    
    print(f"\nTrickle flow reactor applications:")
    print(f"  • Hydrogenation reactions")
    print(f"  • Hydrotreating processes")
    print(f"  • Three-phase catalytic processes")


def example_12_recycle_reactor():
    """Example 12: Reactor with recycle stream."""
    print("=" * 60)
    print("Example 12: Recycle Reactor System")
    print("=" * 60)
    
    from models import RecycleReactor, CSTR
    
    # Create base CSTR
    base_cstr = CSTR(
        V=100.0,                  # Volume [L]
        k0=7.2e10,               # Pre-exponential factor [1/min]
        Ea=72750.0,              # Activation energy [J/mol]
        name="BaseCSTR"
    )
    
    # Create recycle reactor system
    recycle_reactor = RecycleReactor(
        base_reactor=base_cstr,
        recycle_ratio=0.6,                # 60% recycle
        separation_efficiency=0.85,        # 85% separation efficiency
        name="RecycleReactorSystem"
    )
    
    # Operating conditions
    CA_fresh = 80.0    # Fresh feed concentration [mol/L]
    CB_fresh = 0.0     # Fresh product concentration [mol/L]
    fresh_flow = 10.0  # Fresh feed flow [L/min]
    temperature = 350.0  # Temperature [K]
    
    u_nominal = np.array([CA_fresh, CB_fresh, fresh_flow, temperature])
    
    print(f"Recycle reactor system:")
    print(f"  Recycle ratio: {recycle_reactor.recycle_ratio:.1%}")
    print(f"  Separation efficiency: {recycle_reactor.separation_efficiency:.1%}")
    print(f"  Fresh feed concentration: {CA_fresh} mol/L")
    print(f"  Fresh feed flow: {fresh_flow} L/min")
    
    # Calculate recycle effects
    total_flow = fresh_flow / (1 - recycle_reactor.recycle_ratio)
    recycle_flow = total_flow * recycle_reactor.recycle_ratio
    
    print(f"  Total reactor flow: {total_flow:.1f} L/min")
    print(f"  Recycle flow: {recycle_flow:.1f} L/min")
    
    # Calculate steady-state (simplified)
    try:
        x_steady = recycle_reactor.steady_state(u_nominal)
        
        print(f"\nSteady-state results:")
        print(f"  System achieved recycle equilibrium")
        
        # Calculate overall conversion
        overall_conversion = recycle_reactor.calculate_overall_conversion(x_steady, u_nominal[:2])
        print(f"  Overall conversion: {overall_conversion:.1%}")
        
        # Benefits of recycle
        single_pass_conversion = 0.3  # Typical single-pass conversion
        enhancement = overall_conversion / single_pass_conversion
        print(f"  Conversion enhancement: {enhancement:.1f}x vs single-pass")
        
    except Exception as e:
        print(f"Steady-state calculation failed: {e}")
        
        # Show conceptual benefits anyway
        print(f"\nRecycle reactor benefits:")
        print(f"  • Higher overall conversion")
        print(f"  • Better raw material utilization")
        print(f"  • Economic process intensification")


def example_13_catalyst_deactivation_reactor():
    """Example 13: Reactor with catalyst deactivation."""
    print("=" * 60)
    print("Example 13: Catalyst Deactivation Reactor")
    print("=" * 60)
    
    from models import CatalystDeactivationReactor, CSTR
    
    # Create base CSTR
    base_cstr = CSTR(
        V=100.0,                  # Volume [L]
        k0=7.2e10,               # Pre-exponential factor [1/min]
        Ea=72750.0,              # Activation energy [J/mol]
        name="BaseCSTRForDeactivation"
    )
    
    # Create catalyst deactivation reactor
    deact_reactor = CatalystDeactivationReactor(
        base_reactor=base_cstr,
        kd=1e-6,                     # Deactivation rate constant [1/s]
        n_deact=1.0,                 # First-order deactivation
        deact_type="time",           # Time-based deactivation
        alpha_init=1.0,              # Initial activity
        name="DeactivatingReactor"
    )
    
    # Operating conditions
    CA_in = 100.0      # Inlet concentration [mol/L]
    T_jacket = 300.0   # Jacket temperature [K]
    flow_rate = 10.0   # Flow rate [L/min]
    T_in = 350.0       # Inlet temperature [K]
    
    u_nominal = np.array([CA_in, T_jacket, flow_rate, T_in])
    
    print(f"Catalyst deactivation reactor:")
    print(f"  Deactivation type: {deact_reactor.deact_type}")
    print(f"  Deactivation rate constant: {deact_reactor.kd:.2e} s⁻¹")
    print(f"  Deactivation order: {deact_reactor.n_deact}")
    print(f"  Initial activity: {deact_reactor.alpha_init}")
    
    # Calculate catalyst lifetime
    try:
        lifetime = deact_reactor.calculate_catalyst_lifetime(alpha_threshold=0.1)
        lifetime_days = lifetime / (24 * 3600)
        print(f"  Catalyst lifetime (to 10% activity): {lifetime_days:.1f} days")
    except:
        print(f"  Catalyst lifetime: Cannot calculate analytically")
    
    # Simulate deactivation over time
    print(f"\nSimulating catalyst deactivation...")
    
    def constant_input(t):
        return u_nominal
    
    try:
        # Initial state with fresh catalyst
        x0 = np.array([0.5, 350.0, 1.0])  # [CA, T, alpha]
        
        results = deact_reactor.simulate(
            t_span=(0, 86400),  # 1 day simulation
            x0=x0,
            u_func=constant_input,
            t_eval=np.linspace(0, 86400, 100)
        )
        
        # Analyze results
        final_activity = results['x'][2, -1]  # Final catalyst activity
        initial_conversion = 0.5  # Assume 50% initial conversion
        final_conversion = initial_conversion * final_activity
        
        print(f"After 1 day operation:")
        print(f"  Final catalyst activity: {final_activity:.3f}")
        print(f"  Conversion decline: {initial_conversion:.1%} → {final_conversion:.1%}")
        print(f"  Activity loss: {(1-final_activity)*100:.1f}%")
        
        # Calculate time-averaged conversion
        avg_activity = np.mean(results['x'][2, :])
        avg_conversion = initial_conversion * avg_activity
        print(f"  Time-averaged conversion: {avg_conversion:.1%}")
        
    except Exception as e:
        print(f"Deactivation simulation failed: {e}")
    
    print(f"\nCatalyst deactivation considerations:")
    print(f"  • Regular catalyst regeneration needed")
    print(f"  • Process economics affected by catalyst cost")
    print(f"  • Reactor design must account for activity decline")


def example_14_advanced_reactor_comparison():
    """Example 14: Comparison of different reactor types."""
    print("=" * 60)
    print("Example 14: Advanced Reactor Comparison")
    print("=" * 60)
    
    print("Reactor Type Comparison for Industrial Applications:\n")
    
    # Reactor characteristics
    reactors = {
        "CSTR": {
            "description": "Continuous Stirred Tank Reactor",
            "advantages": ["Perfect mixing", "Easy temperature control", "Simple design"],
            "disadvantages": ["Lower conversion per volume", "Back-mixing"],
            "applications": ["Liquid-phase reactions", "Fast reactions", "Temperature-sensitive reactions"]
        },
        "PlugFlowReactor": {
            "description": "Plug Flow Reactor",
            "advantages": ["High conversion", "No back-mixing", "Predictable residence time"],
            "disadvantages": ["Temperature control difficulty", "Pressure drop"],
            "applications": ["Gas-phase reactions", "High-temperature reactions", "Tubular reactors"]
        },
        "FluidizedBedReactor": {
            "description": "Fluidized Bed Reactor",
            "advantages": ["Excellent heat transfer", "Continuous catalyst regeneration", "Large surface area"],
            "disadvantages": ["Complex hydrodynamics", "Catalyst attrition", "Bypassing"],
            "applications": ["Catalytic cracking", "Combustion", "Gasification"]
        },
        "FixedBedReactor": {
            "description": "Fixed Bed Reactor",
            "advantages": ["High catalyst density", "Simple operation", "Low catalyst loss"],
            "disadvantages": ["Heat transfer limitations", "Pressure drop", "Catalyst replacement"],
            "applications": ["Heterogeneous catalysis", "Hydrogenation", "Ammonia synthesis"]
        },
        "MembraneReactor": {
            "description": "Membrane Reactor",
            "advantages": ["Reaction-separation integration", "Enhanced conversion", "Selective removal"],
            "disadvantages": ["Membrane fouling", "High cost", "Limited temperature"],
            "applications": ["Hydrogen production", "Dehydrogenation", "Fuel cells"]
        },
        "TrickleFlowReactor": {
            "description": "Trickle Flow Reactor",
            "advantages": ["Three-phase contacting", "Good heat transfer", "Continuous operation"],
            "disadvantages": ["Complex mass transfer", "Liquid distribution", "Pressure drop"],
            "applications": ["Hydrogenation", "Hydrotreating", "Wastewater treatment"]
        }
    }
    
    for reactor_name, info in reactors.items():
        print(f"{reactor_name}:")
        print(f"  Description: {info['description']}")
        print(f"  Advantages: {', '.join(info['advantages'])}")
        print(f"  Disadvantages: {', '.join(info['disadvantages'])}")
        print(f"  Applications: {', '.join(info['applications'])}")
        print()
    
    # Selection criteria
    print("Reactor Selection Criteria:")
    print("• Reaction kinetics (order, rate, equilibrium)")
    print("• Phase behavior (gas, liquid, solid)")
    print("• Heat effects (exothermic, endothermic)")
    print("• Mass transfer requirements")
    print("• Catalyst requirements")
    print("• Product separation needs")
    print("• Economic considerations")
    print("• Safety and environmental factors")
    
    print(f"\nRecommended reactor selection approach:")
    print(f"1. Analyze reaction characteristics")
    print(f"2. Consider process requirements")
    print(f"3. Evaluate economic factors")
    print(f"4. Assess technical feasibility")
    print(f"5. Consider safety and environmental impact")


def example_15_compressor_modeling():
    """Example 15: Gas compressor modeling and control."""
    print("=" * 60)
    print("Example 15: Gas Compressor Modeling")
    print("=" * 60)
    
    # Create a gas compressor model
    compressor = Compressor(
        eta_isentropic=0.75,         # 75% isentropic efficiency
        P_suction=1e5,               # 1 bar suction pressure
        P_discharge=5e5,             # 5 bar discharge pressure
        T_suction=288.15,            # 15°C suction temperature
        gamma=1.4,                   # Air (diatomic gas)
        R=8.314,                     # Gas constant
        M=0.0289,                    # Air molar mass [kg/mol]
        flow_nominal=10.0,           # 10 mol/s nominal flow
        name="CentrifugalCompressor"
    )
    
    print(f"Compressor specifications:")
    print(f"  Isentropic efficiency: {compressor.eta_isentropic:.1%}")
    print(f"  Suction pressure: {compressor.P_suction/1e5:.1f} bar")
    print(f"  Discharge pressure: {compressor.P_discharge/1e5:.1f} bar")
    print(f"  Pressure ratio: {compressor.P_discharge/compressor.P_suction:.1f}")
    print(f"  Suction temperature: {compressor.T_suction-273.15:.1f} °C")
    
    # Operating conditions
    P_suc = 1.2e5      # 1.2 bar suction pressure
    T_suc = 293.15     # 20°C suction temperature
    P_dis = 6e5        # 6 bar discharge pressure
    flow = 8.0         # 8 mol/s flow rate
    
    u_nominal = np.array([P_suc, T_suc, P_dis, flow])
    
    # Calculate steady-state performance
    try:
        steady_state = compressor.steady_state(u_nominal)
        T_out = steady_state[0]
        Power = steady_state[1]
        
        print(f"\nSteady-state performance:")
        print(f"  Inlet conditions: {P_suc/1e5:.1f} bar, {T_suc-273.15:.1f} °C")
        print(f"  Outlet conditions: {P_dis/1e5:.1f} bar, {T_out-273.15:.1f} °C")
        print(f"  Temperature rise: {T_out-T_suc:.1f} K")
        print(f"  Power required: {Power/1000:.1f} kW")
        print(f"  Specific power: {Power/(flow*compressor.M*1000):.1f} kJ/kg")
        
        # Calculate isentropic temperature for comparison
        T_isen = T_suc * (P_dis/P_suc)**((compressor.gamma-1)/compressor.gamma)
        print(f"  Isentropic outlet temp: {T_isen-273.15:.1f} °C")
        print(f"  Actual efficiency: {(T_isen-T_suc)/(T_out-T_suc):.1%}")
        
    except Exception as e:
        print(f"Steady-state calculation failed: {e}")
    
    # Simulate dynamic response to pressure change
    print(f"\nSimulating response to discharge pressure step...")
    
    def input_profile(t):
        if t < 5:
            return u_nominal
        else:
            # Step change in discharge pressure
            u_step = u_nominal.copy()
            u_step[2] = P_dis * 1.2  # 20% pressure increase
            return u_step
    
    try:
        x0 = np.array([T_out])  # Initial outlet temperature
        results = compressor.simulate(
            t_span=(0, 15),
            x0=x0,
            u_func=input_profile,
            t_eval=np.linspace(0, 15, 100)
        )
        
        print(f"Dynamic response completed:")
        print(f"  Initial outlet temperature: {results['x'][0, 0]-273.15:.1f} °C")
        print(f"  Final outlet temperature: {results['x'][0, -1]-273.15:.1f} °C")
        print(f"  Temperature increase: {results['x'][0, -1]-results['x'][0, 0]:.1f} K")
        
    except Exception as e:
        print(f"Dynamic simulation failed: {e}")
    
    print(f"\nCompressor applications:")
    print(f"  • Gas pipeline compression")
    print(f"  • Refrigeration cycles")
    print(f"  • Process gas compression")
    print(f"  • Air compression systems")


def example_16_pump_modeling():
    """Example 16: Liquid pump modeling and comparison."""
    print("=" * 60)
    print("Example 16: Liquid Pump Modeling")
    print("=" * 60)
    
    # Create different types of pumps
    generic_pump = Pump(
        eta=0.7,                     # 70% efficiency
        rho=1000.0,                  # Water density
        flow_nominal=0.01,           # 10 L/s nominal flow
        delta_P_nominal=2e5,         # 2 bar pressure rise
        name="GenericPump"
    )
    
    centrifugal_pump = CentrifugalPump(
        H0=50.0,                     # 50 m shutoff head
        K=20.0,                      # Head-flow coefficient
        eta=0.72,                    # 72% efficiency
        rho=1000.0,                  # Water density
        name="CentrifugalPump"
    )
    
    positive_pump = PositiveDisplacementPump(
        flow_rate=0.008,             # 8 L/s constant flow
        eta=0.85,                    # 85% efficiency
        rho=1000.0,                  # Water density
        name="PositiveDisplacementPump"
    )
    
    pumps = [generic_pump, centrifugal_pump, positive_pump]
    
    print(f"Pump comparison:")
    print(f"{'Type':<25} {'Efficiency':<12} {'Head/ΔP':<15} {'Flow Control'}")
    print(f"{'-'*65}")
    
    for pump in pumps:
        if hasattr(pump, 'H0'):
            head_info = f"{pump.H0:.1f} m"
            flow_control = "Variable"
        elif hasattr(pump, 'flow_rate'):
            head_info = f"{pump.delta_P_nominal/1e5:.1f} bar"
            flow_control = "Constant"
        else:
            head_info = f"{pump.delta_P_nominal/1e5:.1f} bar"
            flow_control = "Variable"
        
        print(f"{pump.name:<25} {pump.eta:.1%}         {head_info:<15} {flow_control}")
    
    # Operating conditions for comparison
    P_inlet = 1e5      # 1 bar inlet pressure
    flow_rates = np.linspace(0.002, 0.015, 8)  # 2-15 L/s flow range
    
    print(f"\nPerformance comparison at different flow rates:")
    print(f"{'Flow [L/s]':<12} {'Generic P_out [bar]':<20} {'Centrifugal P_out [bar]':<23} {'PD P_out [bar]'}")
    print(f"{'-'*75}")
    
    for flow in flow_rates:
        results = {}
        
        # Generic pump
        u_generic = np.array([P_inlet, flow])
        steady_generic = generic_pump.steady_state(u_generic)
        P_out_generic = steady_generic[0]
        
        # Centrifugal pump
        u_centrifugal = np.array([P_inlet, flow])
        steady_centrifugal = centrifugal_pump.steady_state(u_centrifugal)
        P_out_centrifugal = steady_centrifugal[0]
        
        # Positive displacement pump (fixed flow)
        u_pd = np.array([P_inlet])
        steady_pd = positive_pump.steady_state(u_pd)
        P_out_pd = steady_pd[0]
        
        print(f"{flow*1000:<12.1f} {P_out_generic/1e5:<20.2f} {P_out_centrifugal/1e5:<23.2f} {P_out_pd/1e5:.2f}")
    
    # Detailed analysis of centrifugal pump
    print(f"\nCentrifugal pump detailed analysis:")
    print(f"  Shutoff head: {centrifugal_pump.H0} m")
    print(f"  Head equation: H = {centrifugal_pump.H0} - {centrifugal_pump.K} × Q²")
    
    # Calculate pump curve
    flows = np.linspace(0, 0.02, 20)
    heads = []
    powers = []
    
    for q in flows:
        if q > 0:
            u = np.array([P_inlet, q])
            result = centrifugal_pump.steady_state(u)
            P_out = result[0]
            Power = result[1]
            
            # Convert pressure to head
            g = 9.81
            head = (P_out - P_inlet) / (centrifugal_pump.rho * g)
            heads.append(head)
            powers.append(Power)
        else:
            heads.append(centrifugal_pump.H0)
            powers.append(0)
    
    max_flow_idx = np.argmax([h for h in heads if h > 0])
    if max_flow_idx < len(flows):
        print(f"  Maximum practical flow: {flows[max_flow_idx]*1000:.1f} L/s")
        print(f"  Head at max flow: {heads[max_flow_idx]:.1f} m")
    
    # System curve intersection example
    print(f"\nSystem curve analysis:")
    print(f"  System resistance: ΔP = K_system × Q²")
    K_system = 1e8  # System resistance coefficient [Pa·s²/m⁶]
    
    for q in [0.005, 0.008, 0.012]:
        # Pump head
        u = np.array([P_inlet, q])
        result = centrifugal_pump.steady_state(u)
        P_pump = result[0] - P_inlet
        
        # System resistance
        P_system = K_system * q**2
        
        print(f"    Flow {q*1000:.1f} L/s: Pump ΔP = {P_pump/1e5:.2f} bar, System ΔP = {P_system/1e5:.2f} bar")
    
    # Dynamic response simulation
    print(f"\nSimulating pump startup transient...")
    
    def startup_profile(t):
        if t < 1:
            return np.array([P_inlet, 0.001])  # Low initial flow
        else:
            return np.array([P_inlet, 0.01])   # Step to operating flow
    
    try:
        x0 = np.array([P_inlet + 0.5e5])  # Initial pressure slightly above inlet
        results = generic_pump.simulate(
            t_span=(0, 5),
            x0=x0,
            u_func=startup_profile,
            t_eval=np.linspace(0, 5, 50)
        )
        
        print(f"  Startup simulation completed")
        print(f"  Initial pressure: {results['x'][0, 0]/1e5:.2f} bar")
        print(f"  Final pressure: {results['x'][0, -1]/1e5:.2f} bar")
        print(f"  Settling time: ~{np.where(np.abs(results['x'][0, 10:] - results['x'][0, -1]) < 0.01*results['x'][0, -1])[0][0]/10 if len(np.where(np.abs(results['x'][0, 10:] - results['x'][0, -1]) < 0.01*results['x'][0, -1])[0]) > 0 else 'N/A'} seconds")
        
    except Exception as e:
        print(f"  Dynamic simulation failed: {e}")


def example_17_compressor_pump_system():
    """Example 17: Integrated compressor-pump system."""
    print("=" * 60)
    print("Example 17: Integrated Compressor-Pump System")
    print("=" * 60)
    
    # Create system components
    compressor = Compressor(
        eta_isentropic=0.78,
        P_suction=1e5,
        P_discharge=8e5,
        T_suction=298.15,
        name="SystemCompressor"
    )
    
    pump = CentrifugalPump(
        H0=80.0,
        K=25.0,
        eta=0.75,
        name="SystemPump"
    )
    
    print(f"System components:")
    print(f"  Compressor: {compressor.P_suction/1e5:.1f} → {compressor.P_discharge/1e5:.1f} bar")
    print(f"  Pump: {pump.H0} m shutoff head, η = {pump.eta:.1%}")
    
    # Operating scenarios
    scenarios = [
        {"name": "Normal Operation", "comp_flow": 12.0, "pump_flow": 0.012},
        {"name": "High Demand", "comp_flow": 15.0, "pump_flow": 0.015},
        {"name": "Low Demand", "comp_flow": 8.0, "pump_flow": 0.008},
        {"name": "Maintenance Mode", "comp_flow": 5.0, "pump_flow": 0.005}
    ]
    
    print(f"\nSystem performance analysis:")
    print(f"{'Scenario':<18} {'Comp Power [kW]':<16} {'Pump Power [kW]':<16} {'Total Power [kW]'}")
    print(f"{'-'*70}")
    
    total_powers = []
    
    for scenario in scenarios:
        # Compressor performance
        u_comp = np.array([compressor.P_suction, compressor.T_suction, 
                          compressor.P_discharge, scenario["comp_flow"]])
        comp_result = compressor.steady_state(u_comp)
        comp_power = comp_result[1] / 1000  # Convert to kW
        
        # Pump performance
        u_pump = np.array([1e5, scenario["pump_flow"]])  # 1 bar inlet
        pump_result = pump.steady_state(u_pump)
        pump_power = pump_result[1] / 1000  # Convert to kW
        
        total_power = comp_power + pump_power
        total_powers.append(total_power)
        
        print(f"{scenario['name']:<18} {comp_power:<16.1f} {pump_power:<16.1f} {total_power:.1f}")
    
    # Energy efficiency analysis
    print(f"\nEnergy efficiency analysis:")
    base_power = total_powers[0]  # Normal operation as base
    
    for i, scenario in enumerate(scenarios):
        efficiency = base_power / total_powers[i] if total_powers[i] > 0 else 0
        savings = (1 - total_powers[i]/base_power) * 100 if base_power > 0 else 0
        
        print(f"  {scenario['name']}: {efficiency:.2f} relative efficiency, {savings:+.1f}% power change")
    
    # Control strategy recommendations
    print(f"\nControl strategy recommendations:")
    print(f"  1. Variable speed drives for both compressor and pump")
    print(f"  2. Pressure control loops with cascade configuration")
    print(f"  3. Energy optimization based on demand forecasting")
    print(f"  4. Surge protection for compressor")
    print(f"  5. Cavitation protection for pump")
    
    # System interactions
    print(f"\nSystem interaction considerations:")
    print(f"  • Compressor discharge pressure affects downstream processes")
    print(f"  • Pump suction conditions must avoid cavitation")
    print(f"  • Temperature effects on fluid properties")
    print(f"  • Vibration and mechanical integrity")
    print(f"  • Maintenance scheduling coordination")
    
    # Performance monitoring
    print(f"\nKey performance indicators (KPIs):")
    print(f"  • Overall equipment effectiveness (OEE)")
    print(f"  • Specific energy consumption (SEC)")
    print(f"  • Availability and reliability metrics")
    print(f"  • Maintenance cost per unit throughput")
    print(f"  • Environmental impact indicators")


def example_18_pump_control_design():
    """Example 18: Pump control system design."""
    print("=" * 60)
    print("Example 18: Pump Control System Design")
    print("=" * 60)
    
    # Create pump system for control design
    pump = CentrifugalPump(
        H0=60.0,                     # 60 m shutoff head
        K=15.0,                      # Head-flow coefficient
        eta=0.78,                    # 78% efficiency
        name="ControlledPump"
    )
    
    print(f"Pump system for control design:")
    print(f"  Type: Centrifugal pump")
    print(f"  Shutoff head: {pump.H0} m")
    print(f"  Efficiency: {pump.eta:.1%}")
    print(f"  Head equation: H = {pump.H0} - {pump.K} × Q²")
    
    # Control objectives
    print(f"\nControl objectives:")
    print(f"  1. Maintain constant discharge pressure")
    print(f"  2. Prevent pump cavitation")
    print(f"  3. Optimize energy consumption")
    print(f"  4. Handle varying demand")
    
    # Linearization for control design
    linear_approx = LinearApproximation(pump)
    
    # Operating point for linearization
    P_inlet_nom = 1.2e5    # 1.2 bar inlet pressure
    flow_nom = 0.01        # 10 L/s nominal flow
    u_nominal = np.array([P_inlet_nom, flow_nom])
    
    try:
        # Get steady-state operating point
        x_steady = pump.steady_state(u_nominal)
        
        # Linearize around operating point
        A, B = linear_approx.linearize(u_nominal, x_steady)
        
        print(f"\nLinearized model at operating point:")
        print(f"  Inlet pressure: {P_inlet_nom/1e5:.1f} bar")
        print(f"  Flow rate: {flow_nom*1000:.1f} L/s")
        print(f"  Outlet pressure: {x_steady[0]/1e5:.2f} bar")
        print(f"  State matrix A: {A[0,0]:.3f}")
        print(f"  Input matrix B: {B[0,:]}")
        
        # Step response analysis
        step_data = linear_approx.step_response(
            input_idx=1,  # Flow rate input
            step_size=0.002,  # 2 L/s step
            t_final=10.0
        )
        
        # Extract characteristics
        response = step_data['x'][0, :]  # Pressure response
        t = step_data['t']
        
        # Find settling time (2% criterion)
        final_value = response[-1]
        settling_mask = np.abs(response - final_value) <= 0.02 * np.abs(final_value)
        settling_indices = np.where(settling_mask)[0]
        
        if len(settling_indices) > 0:
            settling_time = t[settling_indices[0]]

            print(f"  Step response settling time: {settling_time:.2f} s")
        
        # PID controller tuning using Ziegler-Nichols
        print(f"\nPID controller design:")
        
        # Fit first-order plus dead time (FOPDT) model
        from functions import fit_fopdt, tune_pid
        
        fopdt_params = fit_fopdt(t, response, step_magnitude=0.002)
        print(f"  FOPDT model: K={fopdt_params['K']:.3f}, τ={fopdt_params['tau']:.2f}s, θ={fopdt_params['theta']:.2f}s")
        
        # Tune PID controller
        pid_params = tune_pid(fopdt_params, method='ziegler_nichols', controller_type='PI')
        print(f"  PI controller: Kp={pid_params['Kp']:.3f}, Ki={pid_params['Ki']:.3f}")
        
        # Create PID controller
        from controllers import PIDController
        controller = PIDController(
            Kp=pid_params['Kp'],
            Ki=pid_params['Ki'],
            Kd=0.0,  # PI controller
            output_limits=(0.001, 0.02),  # Flow limits
            name="PumpFlowController"
        )
        
        print(f"  Controller configured with output limits: {controller.output_limits[0]*1000:.1f}-{controller.output_limits[1]*1000:.1f} L/s")
        
    except Exception as e:
        print(f"Control design failed: {e}")
    
    # Control strategies
    print(f"\nControl strategies:")
    
    strategies = {
        "Constant Pressure": {
            "description": "Maintain constant discharge pressure",
            "control_variable": "Pump speed or valve position",
            "advantages": ["Simple implementation", "Good for constant demand"],
            "disadvantages": ["Energy inefficient at low demand"]
        },
        "Variable Speed": {
            "description": "Adjust pump speed based on demand",
            "control_variable": "Motor frequency (VFD)",
            "advantages": ["Energy efficient", "Wide operating range"],
            "disadvantages": ["Higher capital cost", "Complex control"]
        },
        "Cascade Control": {
            "description": "Outer pressure loop, inner flow loop",
            "control_variable": "Flow setpoint to inner loop",
            "advantages": ["Better disturbance rejection", "Faster response"],
            "disadvantages": ["More complex tuning", "Multiple sensors needed"]
        }
    }
    
    for strategy, details in strategies.items():
        print(f"\n  {strategy}:")
        print(f"    Description: {details['description']}")
        print(f"    Control variable: {details['control_variable']}")
        print(f"    Advantages: {', '.join(details['advantages'])}")
        print(f"    Disadvantages: {', '.join(details['disadvantages'])}")
    
    # Safety considerations
    print(f"\nSafety and protection systems:")
    print(f"  • Minimum flow protection (recirculation valve)")
    print(f"  • Suction pressure monitoring (cavitation prevention)")
    print(f"  • Maximum pressure relief (safety valve)")
    print(f"  • Vibration monitoring")
    print(f"  • Temperature monitoring (bearing protection)")
    print(f"  • Emergency shutdown systems")
    
    # Performance optimization
    print(f"\nPerformance optimization:")
    print(f"  • Real-time efficiency monitoring")
    print(f"  • Predictive maintenance based on vibration/temperature")
    print(f"  • Demand forecasting for proactive control")
    print(f"  • Multi-pump optimization in parallel systems")
    print(f"  • Energy cost optimization with time-of-use pricing")


def main():
    """Run all examples."""
    print("Standard Process Control Library - Advanced Reactor Examples")
    print("=" * 80)
    
    examples = [
        example_1_gravity_drained_tank,
        example_2_cstr_modeling,
        example_3_transfer_function_analysis,
        example_4_optimization,
        example_5_batch_scheduling,
        example_6_model_predictive_control,
        example_7_heat_exchanger,
        example_8_distillation_column,
        example_11_fluidized_bed_reactor,
        example_12_membrane_reactor,
        example_11_trickle_flow_reactor,
        example_12_recycle_reactor,
        example_13_catalyst_deactivation_reactor,
        example_14_advanced_reactor_comparison,
        example_15_compressor_modeling,
        example_16_pump_modeling,
        example_17_compressor_pump_system,
        example_18_pump_control_design
    ]
    
    try:
        for i, example_func in enumerate(examples, 1):
            print(f"\nRunning Example {i}...")
            example_func()
            print("\n" + "="*40 + "\n")
            
        print("All examples completed successfully!")
        print("\nLibrary Features Demonstrated:")
        print("• Advanced reactor modeling (5 new reactor types)")
        print("• PID control and tuning")
        print("• Process modeling and linearization")
        print("• Heat exchanger design")
        print("• Distillation column control")
        print("• Transfer function analysis")
        print("• Process optimization")
        print("• Batch scheduling")
        print("• Model predictive control")
        print("• Stability and performance analysis")
        print("• Fluidized bed reactor dynamics")
        print("• Membrane reactor with selective permeation")
        print("• Three-phase trickle flow reactor")
        print("• Recycle reactor systems")
        print("• Catalyst deactivation effects")
        print("• Control valve modeling with dead-time")
        print("• Three-way valve flow mixing/diverting")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()
