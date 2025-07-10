"""
InteractingTanks Model Example

This example demonstrates the use of the InteractingTanks class for simulating
two tanks in series and analyzing multi-variable dynamics.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import sys
import os

# Add the project root to the path to import the InteractingTanks class
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from unit.tank.InteractingTanks import InteractingTanks


def step_input(t, step_time=10.0, initial_flow=0.4, final_flow=0.7):
    """Step input function for inlet flow."""
    return final_flow if t >= step_time else initial_flow


def main():
    """Main example demonstrating InteractingTanks model capabilities."""
    
    print("InteractingTanks Model Example")
    print("==============================")
    print()
    
    # Create interacting tanks instance
    print("1. Creating InteractingTanks Model")
    tanks = InteractingTanks(A1=1.2, A2=0.8, C1=0.3, C2=0.25, name="ExampleTanks")
    
    # Display tank information
    desc = tanks.describe()
    print(f"System Name: {desc['name']}")
    print(f"Description: {desc['description']}")
    print(f"Tank 1 - Area: {tanks.A1} m², Discharge: {tanks.C1} m²/min")
    print(f"Tank 2 - Area: {tanks.A2} m², Discharge: {tanks.C2} m²/min")
    print()
    
    # Initial conditions and simulation parameters
    print("2. Simulation Setup")
    h1_0, h2_0 = 1.5, 0.8  # Initial heights [m]
    t_span = (0, 60)  # Simulation time [min]
    t_eval = np.linspace(0, 60, 601)
    
    print(f"Initial heights: Tank 1 = {h1_0} m, Tank 2 = {h2_0} m")
    print(f"Simulation time: {t_span[1]} minutes")
    print()
    
    # Steady-state analysis
    print("3. Steady-State Analysis")
    q_in_initial = 0.4
    q_in_final = 0.7
    
    x_ss_initial = tanks.steady_state(np.array([q_in_initial]))
    x_ss_final = tanks.steady_state(np.array([q_in_final]))
    
    print(f"Initial flow rate: {q_in_initial} m³/min")
    print(f"Initial steady-state heights: Tank 1 = {x_ss_initial[0]:.3f} m, Tank 2 = {x_ss_initial[1]:.3f} m")
    print(f"Final flow rate: {q_in_final} m³/min")
    print(f"Final steady-state heights: Tank 1 = {x_ss_final[0]:.3f} m, Tank 2 = {x_ss_final[1]:.3f} m")
    print()
    
    # Time constant analysis (linearized)
    print("4. Linearized Time Constants")
    
    # Tank 1 time constant at final steady state
    if x_ss_final[0] > 0:
        tau1 = 2 * tanks.A1 * np.sqrt(x_ss_final[0]) / tanks.C1
        print(f"Tank 1 time constant: {tau1:.2f} min")
    
    # Tank 2 time constant at final steady state
    if x_ss_final[1] > 0:
        tau2 = 2 * tanks.A2 * np.sqrt(x_ss_final[1]) / tanks.C2
        print(f"Tank 2 time constant: {tau2:.2f} min")
    
    print()
    
    # Simulate step response
    print("5. Step Response Simulation")
    
    def tanks_dynamics(t, x):
        u = np.array([step_input(t)])
        return tanks.dynamics(t, x, u)
    
    sol = solve_ivp(tanks_dynamics, t_span, [h1_0, h2_0], t_eval=t_eval, rtol=1e-6)
    
    # Extract results
    h1_values = sol.y[0]
    h2_values = sol.y[1]
    flows_in = np.array([step_input(t) for t in t_eval])
    
    # Calculate inter-tank and outlet flows
    flows_12 = tanks.C1 * np.sqrt(np.maximum(h1_values, 0))
    flows_out = tanks.C2 * np.sqrt(np.maximum(h2_values, 0))
    
    # Calculate volumes
    volume1 = tanks.A1 * np.maximum(h1_values, 0)
    volume2 = tanks.A2 * np.maximum(h2_values, 0)
    total_volume = volume1 + volume2
    
    print(f"Simulation completed successfully")
    print(f"Final heights: Tank 1 = {h1_values[-1]:.3f} m, Tank 2 = {h2_values[-1]:.3f} m")
    print(f"Final inter-tank flow: {flows_12[-1]:.3f} m³/min")
    print(f"Final outlet flow: {flows_out[-1]:.3f} m³/min")
    print()
    
    # Response analysis
    print("6. Response Analysis")
    
    step_time = 10.0
    idx_after_step = np.where(t_eval >= step_time)[0]
    
    # Analyze tank 2 response (slower, more interesting)
    h2_initial_ss = x_ss_initial[1]
    h2_final_ss = x_ss_final[1]
    final_change_h2 = h2_final_ss - h2_initial_ss
    
    if final_change_h2 != 0:
        target_h2 = h2_initial_ss + 0.632 * final_change_h2
        
        try:
            h2_after_step = h2_values[idx_after_step]
            if final_change_h2 > 0:  # Step up
                idx_target = np.where(h2_after_step >= target_h2)[0][0]
            else:  # Step down
                idx_target = np.where(h2_after_step <= target_h2)[0][0]
            
            time_to_63_h2 = t_eval[idx_after_step[idx_target]] - step_time
            print(f"Tank 2 - Time to reach 63.2% of step change: {time_to_63_h2:.2f} min")
        except IndexError:
            print("Tank 2 - Target height not reached in simulation time")
    
    # Calculate settling times
    tolerance = 0.02 * abs(final_change_h2)
    if tolerance > 0:
        steady_range_h2 = [h2_final_ss - tolerance, h2_final_ss + tolerance]
        
        try:
            outside_tolerance = np.where((h2_values < steady_range_h2[0]) | 
                                       (h2_values > steady_range_h2[1]))[0]
            if len(outside_tolerance) > 0:
                settling_time_h2 = t_eval[outside_tolerance[-1]] - step_time
                print(f"Tank 2 - Settling time (2% criterion): {settling_time_h2:.2f} min")
        except:
            print("Tank 2 - Could not determine settling time")
    
    print()
    
    # Mass balance verification
    print("7. Mass Balance Verification")
    
    # Total system accumulation rate
    dh1dt_values = []
    dh2dt_values = []
    
    for i in range(len(t_eval)):
        u = np.array([flows_in[i]])
        x = np.array([h1_values[i], h2_values[i]])
        dxdt = tanks.dynamics(t_eval[i], x, u)
        dh1dt_values.append(dxdt[0])
        dh2dt_values.append(dxdt[1])
    
    total_accumulation = tanks.A1 * np.array(dh1dt_values) + tanks.A2 * np.array(dh2dt_values)
    net_inflow = flows_in - flows_out
    mass_balance_error = total_accumulation - net_inflow
    
    max_error = np.max(np.abs(mass_balance_error))
    print(f"Maximum mass balance error: {max_error:.2e} m³/min")
    print(f"Mass balance verification: {'PASSED' if max_error < 1e-10 else 'FAILED'}")
    print()
    
    # Create visualizations
    print("8. Creating Visualizations")
    
    # Main response plot
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('InteractingTanks Model Response Analysis', fontsize=16, fontweight='bold')
    
    # Height responses
    ax1.plot(t_eval, h1_values, 'b-', linewidth=2, label='Tank 1 Height')
    ax1.plot(t_eval, h2_values, 'r-', linewidth=2, label='Tank 2 Height')
    ax1.axhline(y=x_ss_initial[0], color='b', linestyle='--', alpha=0.5)
    ax1.axhline(y=x_ss_initial[1], color='r', linestyle='--', alpha=0.5)
    ax1.axhline(y=x_ss_final[0], color='b', linestyle=':', alpha=0.7)
    ax1.axhline(y=x_ss_final[1], color='r', linestyle=':', alpha=0.7)
    ax1.axvline(x=step_time, color='k', linestyle=':', alpha=0.5, label='Step time')
    ax1.set_xlabel('Time [min]')
    ax1.set_ylabel('Height [m]')
    ax1.set_title('Tank Heights')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Flow rates
    ax2.plot(t_eval, flows_in, 'g-', linewidth=2, label='Inlet flow')
    ax2.plot(t_eval, flows_12, 'b-', linewidth=2, label='Inter-tank flow')
    ax2.plot(t_eval, flows_out, 'r-', linewidth=2, label='Outlet flow')
    ax2.set_xlabel('Time [min]')
    ax2.set_ylabel('Flow Rate [m³/min]')
    ax2.set_title('Flow Rates')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Volumes
    ax3.plot(t_eval, volume1, 'b-', linewidth=2, label='Tank 1 Volume')
    ax3.plot(t_eval, volume2, 'r-', linewidth=2, label='Tank 2 Volume')
    ax3.plot(t_eval, total_volume, 'k--', linewidth=2, label='Total Volume')
    ax3.set_xlabel('Time [min]')
    ax3.set_ylabel('Volume [m³]')
    ax3.set_title('Tank Volumes')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Mass balance error
    ax4.plot(t_eval, mass_balance_error, 'm-', linewidth=2)
    ax4.set_xlabel('Time [min]')
    ax4.set_ylabel('Mass Balance Error [m³/min]')
    ax4.set_title('Mass Balance Error')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('InteractingTanks_example_plots.png', dpi=300, bbox_inches='tight')
    print("Main plot saved as 'InteractingTanks_example_plots.png'")
    
    # Detailed analysis plot
    fig2, ((ax5, ax6), (ax7, ax8)) = plt.subplots(2, 2, figsize=(14, 10))
    fig2.suptitle('InteractingTanks Model Detailed Analysis', fontsize=16, fontweight='bold')
    
    # Phase portrait for tank 2
    ax5.plot(h2_values, dh2dt_values, 'r-', linewidth=2)
    ax5.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax5.axvline(x=x_ss_final[1], color='k', linestyle='--', alpha=0.5, label='Final SS')
    ax5.set_xlabel('Tank 2 Height [m]')
    ax5.set_ylabel('dh2/dt [m/min]')
    ax5.set_title('Tank 2 Phase Portrait')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # Tank interaction analysis
    interaction_strength = flows_12 / (flows_in + 1e-10)  # Avoid division by zero
    ax6.plot(t_eval, interaction_strength, 'purple', linewidth=2)
    ax6.set_xlabel('Time [min]')
    ax6.set_ylabel('Interaction Strength (q12/qin)')
    ax6.set_title('Tank Interaction Strength')
    ax6.grid(True, alpha=0.3)
    
    # Residence times
    residence_time_1 = np.divide(volume1, flows_12, out=np.zeros_like(volume1), where=flows_12!=0)
    residence_time_2 = np.divide(volume2, flows_out, out=np.zeros_like(volume2), where=flows_out!=0)
    
    ax7.plot(t_eval, residence_time_1, 'b-', linewidth=2, label='Tank 1')
    ax7.plot(t_eval, residence_time_2, 'r-', linewidth=2, label='Tank 2')
    ax7.set_xlabel('Time [min]')
    ax7.set_ylabel('Residence Time [min]')
    ax7.set_title('Tank Residence Times')
    ax7.legend()
    ax7.grid(True, alpha=0.3)
    
    # Flow characteristics
    h1_range = np.linspace(0, max(h1_values) + 0.5, 100)
    h2_range = np.linspace(0, max(h2_values) + 0.5, 100)
    q12_range = tanks.C1 * np.sqrt(h1_range)
    qout_range = tanks.C2 * np.sqrt(h2_range)
    
    ax8.plot(h1_range, q12_range, 'b-', linewidth=2, label='q12 = C1√h1')
    ax8.plot(h2_range, qout_range, 'r-', linewidth=2, label='qout = C2√h2')
    ax8.scatter(h1_values[::20], flows_12[::20], c='blue', alpha=0.6, s=20)
    ax8.scatter(h2_values[::20], flows_out[::20], c='red', alpha=0.6, s=20)
    ax8.set_xlabel('Height [m]')
    ax8.set_ylabel('Flow Rate [m³/min]')
    ax8.set_title('Flow Characteristics')
    ax8.legend()
    ax8.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('InteractingTanks_detailed_analysis.png', dpi=300, bbox_inches='tight')
    print("Detailed analysis plot saved as 'InteractingTanks_detailed_analysis.png'")
    
    # System characteristics summary
    print()
    print("9. System Characteristics Summary")
    print("================================")
    print(f"Tank 1 dominant time constant: {tau1:.2f} min" if 'tau1' in locals() else "Tank 1 time constant: N/A")
    print(f"Tank 2 dominant time constant: {tau2:.2f} min" if 'tau2' in locals() else "Tank 2 time constant: N/A")
    
    if 'tau1' in locals() and 'tau2' in locals():
        if tau1 > tau2:
            print(f"Tank 1 is the slower tank (ratio: {tau1/tau2:.2f})")
        else:
            print(f"Tank 2 is the slower tank (ratio: {tau2/tau1:.2f})")
    
    print(f"System exhibits {'strong' if abs(tau1 - tau2) < 0.5 * min(tau1, tau2) else 'weak'} interaction" if 'tau1' in locals() and 'tau2' in locals() else "")
    print()
    
    print("Example completed successfully!")
    print("=====================================")


if __name__ == "__main__":
    main()
