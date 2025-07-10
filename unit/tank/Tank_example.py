"""
Tank Model Example

This example demonstrates the use of the Tank class for simulating
gravity-drained tank dynamics and analyzing control system behavior.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import sys
import os

# Add the project root to the path to import the Tank class
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from unit.tank.Tank import Tank


def step_input(t, step_time=5.0, initial_flow=0.5, final_flow=0.8):
    """Step input function for inlet flow."""
    return final_flow if t >= step_time else initial_flow


def main():
    """Main example demonstrating Tank model capabilities."""
    
    print("Tank Model Example")
    print("==================")
    print()
    
    # Create tank instance
    print("1. Creating Tank Model")
    tank = Tank(A=1.5, C=0.4, name="ExampleTank")
    
    # Display tank information
    desc = tank.describe()
    print(f"Tank Name: {desc['name']}")
    print(f"Description: {desc['description']}")
    print(f"Cross-sectional Area: {tank.A} m²")
    print(f"Discharge Coefficient: {tank.C} m²/min")
    print()
    
    # Initial conditions and simulation parameters
    print("2. Simulation Setup")
    h0 = 1.0  # Initial height [m]
    t_span = (0, 30)  # Simulation time [min]
    t_eval = np.linspace(0, 30, 301)
    
    print(f"Initial height: {h0} m")
    print(f"Simulation time: {t_span[1]} minutes")
    print()
    
    # Steady-state analysis
    print("3. Steady-State Analysis")
    q_in_initial = 0.5
    q_in_final = 0.8
    
    h_ss_initial = tank.steady_state(np.array([q_in_initial]))[0]
    h_ss_final = tank.steady_state(np.array([q_in_final]))[0]
    
    print(f"Initial flow rate: {q_in_initial} m³/min")
    print(f"Initial steady-state height: {h_ss_initial:.3f} m")
    print(f"Final flow rate: {q_in_final} m³/min")
    print(f"Final steady-state height: {h_ss_final:.3f} m")
    print()
    
    # Time constant analysis
    print("4. Time Constant Analysis")
    tau_initial = tank.calculate_time_constant(h_ss_initial)
    tau_final = tank.calculate_time_constant(h_ss_final)
    
    print(f"Time constant at initial operating point: {tau_initial:.2f} min")
    print(f"Time constant at final operating point: {tau_final:.2f} min")
    print()
    
    # Simulate step response
    print("5. Step Response Simulation")
    
    def tank_dynamics(t, x):
        u = np.array([step_input(t)])
        return tank.dynamics(t, x, u)
    
    sol = solve_ivp(tank_dynamics, t_span, [h0], t_eval=t_eval, rtol=1e-6)
    
    # Calculate additional outputs
    heights = sol.y[0]
    flows_in = np.array([step_input(t) for t in t_eval])
    flows_out = np.array([tank.calculate_outlet_flow(h) for h in heights])
    volumes = np.array([tank.calculate_volume(h) for h in heights])
    
    print(f"Simulation completed successfully")
    print(f"Final height: {heights[-1]:.3f} m")
    print(f"Final outlet flow: {flows_out[-1]:.3f} m³/min")
    print(f"Final volume: {volumes[-1]:.3f} m³")
    print()
    
    # Performance metrics analysis
    print("6. Performance Metrics")
    x_final = np.array([heights[-1]])
    u_final = np.array([flows_in[-1]])
    metrics = tank.get_performance_metrics(x_final, u_final)
    
    print(f"Height: {metrics['height']:.3f} m")
    print(f"Outlet flow: {metrics['outlet_flow']:.3f} m³/min")
    print(f"Volume: {metrics['volume']:.3f} m³")
    print(f"Time constant: {metrics['time_constant']:.2f} min")
    print(f"Mass balance error: {metrics['mass_balance_error']:.6f} m³/min")
    print(f"Residence time: {metrics['residence_time']:.2f} min")
    print()
    
    # Response analysis
    print("7. Response Analysis")
    
    # Find time to reach 63.2% of final value (approximating time constant)
    final_change = h_ss_final - h_ss_initial
    target_height = h_ss_initial + 0.632 * final_change
    
    # Find time when height first exceeds target
    step_time = 5.0
    idx_after_step = np.where(t_eval >= step_time)[0]
    heights_after_step = heights[idx_after_step]
    
    try:
        idx_target = np.where(heights_after_step >= target_height)[0][0]
        time_to_63 = t_eval[idx_after_step[idx_target]] - step_time
        print(f"Time to reach 63.2% of step change: {time_to_63:.2f} min")
        print(f"Theoretical time constant: {tau_final:.2f} min")
    except IndexError:
        print("Target height not reached in simulation time")
    
    # Calculate settling time (2% criterion)
    tolerance = 0.02 * final_change
    steady_range = [h_ss_final - tolerance, h_ss_final + tolerance]
    
    try:
        # Find last time outside the tolerance band
        outside_tolerance = np.where((heights < steady_range[0]) | 
                                   (heights > steady_range[1]))[0]
        if len(outside_tolerance) > 0:
            settling_time = t_eval[outside_tolerance[-1]] - step_time
            print(f"Settling time (2% criterion): {settling_time:.2f} min")
        else:
            print("System settled immediately")
    except:
        print("Could not determine settling time")
    
    print()
    
    # Create visualization
    print("8. Creating Visualizations")
    
    # Main response plot
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Tank Model Response Analysis', fontsize=16, fontweight='bold')
    
    # Height response
    ax1.plot(t_eval, heights, 'b-', linewidth=2, label='Height')
    ax1.axhline(y=h_ss_initial, color='r', linestyle='--', alpha=0.7, label='Initial SS')
    ax1.axhline(y=h_ss_final, color='g', linestyle='--', alpha=0.7, label='Final SS')
    ax1.axvline(x=5, color='k', linestyle=':', alpha=0.5, label='Step time')
    ax1.set_xlabel('Time [min]')
    ax1.set_ylabel('Height [m]')
    ax1.set_title('Tank Height Response')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Flow comparison
    ax2.plot(t_eval, flows_in, 'r-', linewidth=2, label='Inlet flow')
    ax2.plot(t_eval, flows_out, 'b-', linewidth=2, label='Outlet flow')
    ax2.set_xlabel('Time [min]')
    ax2.set_ylabel('Flow Rate [m³/min]')
    ax2.set_title('Flow Rates')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Volume
    ax3.plot(t_eval, volumes, 'g-', linewidth=2)
    ax3.set_xlabel('Time [min]')
    ax3.set_ylabel('Volume [m³]')
    ax3.set_title('Tank Volume')
    ax3.grid(True, alpha=0.3)
    
    # Mass balance error
    mass_balance_error = flows_in - flows_out
    ax4.plot(t_eval, mass_balance_error, 'm-', linewidth=2)
    ax4.set_xlabel('Time [min]')
    ax4.set_ylabel('Mass Balance Error [m³/min]')
    ax4.set_title('Mass Balance Error (q_in - q_out)')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('Tank_example_plots.png', dpi=300, bbox_inches='tight')
    print("Main plot saved as 'Tank_example_plots.png'")
    
    # Detailed analysis plot
    fig2, ((ax5, ax6), (ax7, ax8)) = plt.subplots(2, 2, figsize=(12, 10))
    fig2.suptitle('Tank Model Detailed Analysis', fontsize=16, fontweight='bold')
    
    # Phase portrait (h vs dh/dt)
    dhdt_values = []
    for i, h in enumerate(heights):
        u = np.array([flows_in[i]])
        x = np.array([h])
        dhdt = tank.dynamics(t_eval[i], x, u)[0]
        dhdt_values.append(dhdt)
    
    ax5.plot(heights, dhdt_values, 'b-', linewidth=2)
    ax5.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax5.set_xlabel('Height [m]')
    ax5.set_ylabel('dh/dt [m/min]')
    ax5.set_title('Phase Portrait')
    ax5.grid(True, alpha=0.3)
    
    # Time constant variation
    time_constants = [tank.calculate_time_constant(h) if h > 0 else 0 for h in heights]
    ax6.plot(t_eval, time_constants, 'r-', linewidth=2)
    ax6.set_xlabel('Time [min]')
    ax6.set_ylabel('Time Constant [min]')
    ax6.set_title('Time Constant Variation')
    ax6.grid(True, alpha=0.3)
    
    # Residence time
    residence_times = []
    for i in range(len(heights)):
        if flows_out[i] > 0:
            res_time = volumes[i] / flows_out[i]
            residence_times.append(res_time)
        else:
            residence_times.append(0)
    
    ax7.plot(t_eval, residence_times, 'g-', linewidth=2)
    ax7.set_xlabel('Time [min]')
    ax7.set_ylabel('Residence Time [min]')
    ax7.set_title('Residence Time')
    ax7.grid(True, alpha=0.3)
    
    # Outlet flow vs height (nonlinear characteristic)
    h_range = np.linspace(0, max(heights) + 1, 100)
    q_out_range = [tank.calculate_outlet_flow(h) for h in h_range]
    
    ax8.plot(h_range, q_out_range, 'k-', linewidth=2, label='q = C√h')
    ax8.scatter(heights[::10], flows_out[::10], c=t_eval[::10], 
                cmap='viridis', alpha=0.7, label='Simulation')
    ax8.set_xlabel('Height [m]')
    ax8.set_ylabel('Outlet Flow [m³/min]')
    ax8.set_title('Outlet Flow Characteristic')
    ax8.legend()
    ax8.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('Tank_detailed_analysis.png', dpi=300, bbox_inches='tight')
    print("Detailed analysis plot saved as 'Tank_detailed_analysis.png'")
    
    print()
    print("Example completed successfully!")
    print("=====================================")


if __name__ == "__main__":
    main()
