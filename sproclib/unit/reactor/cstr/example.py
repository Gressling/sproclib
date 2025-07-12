"""
CSTR (Continuous Stirred Tank Reactor) Example

This example demonstrates the use of the CSTR model for simulating
a continuous chemical reaction with temperature control.

Author: SPROCLIB Development Team
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import sys
import os

# Add the parent directory to sys.path to import from unit.reactor
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from unit.reactor.cstr import CSTR


def main():
    """Main function demonstrating CSTR model usage."""
    
    print("="*60)
    print("CSTR (Continuous Stirred Tank Reactor) Example")
    print("="*60)
    
    # Create CSTR instance
    reactor = CSTR(
        V=100.0,           # Reactor volume [L]
        k0=7.2e10,         # Pre-exponential factor [1/min]
        Ea=72750.0,        # Activation energy [J/gmol]
        dHr=-50000.0,      # Heat of reaction [J/gmol]
        UA=50000.0,        # Heat transfer coefficient [J/min/K]
        name="Example_CSTR"
    )
    
    print(f"Reactor: {reactor.name}")
    print(f"Volume: {reactor.V} L")
    print(f"Heat transfer coefficient: {reactor.UA} J/min/K")
    print()
    
    # Define operating conditions
    operating_conditions = {
        'q': 10.0,         # Flow rate [L/min]
        'CAi': 1.0,        # Inlet concentration [mol/L]
        'Ti': 350.0,       # Inlet temperature [K]
        'Tc': 300.0        # Coolant temperature [K]
    }
    
    print("Operating Conditions:")
    for param, value in operating_conditions.items():
        units = {'q': 'L/min', 'CAi': 'mol/L', 'Ti': 'K', 'Tc': 'K'}
        print(f"  {param}: {value} {units[param]}")
    print()
    
    # Input vector for simulation
    u = np.array([operating_conditions[key] for key in ['q', 'CAi', 'Ti', 'Tc']])
    
    # Calculate steady state
    print("Steady State Analysis:")
    print("-" * 30)
    
    x_ss = reactor.steady_state(u)
    CA_ss, T_ss = x_ss
    
    print(f"Steady-state concentration: {CA_ss:.4f} mol/L")
    print(f"Steady-state temperature: {T_ss:.2f} K")
    
    # Calculate performance metrics at steady state
    metrics = reactor.get_performance_metrics(x_ss, u)
    print(f"Conversion: {metrics['conversion']:.1%}")
    print(f"Residence time: {metrics['residence_time']:.2f} min")
    print(f"Reaction rate constant: {metrics['reaction_rate_constant']:.2e} 1/min")
    print(f"Heat generation: {metrics['heat_generation']:.0f} J/min")
    print(f"Productivity: {metrics['productivity']:.3f} mol/min")
    print()
    
    # Dynamic simulation
    print("Dynamic Simulation:")
    print("-" * 30)
    
    # Initial conditions (startup from inlet conditions)
    x0 = np.array([operating_conditions['CAi'], operating_conditions['Ti']])
    
    # Time span for simulation
    t_span = (0, 60)  # 0 to 60 minutes
    t_eval = np.linspace(0, 60, 300)
    
    # Solve ODE
    def cstr_ode(t, x):
        return reactor.dynamics(t, x, u)
    
    sol = solve_ivp(cstr_ode, t_span, x0, t_eval=t_eval, method='RK45', rtol=1e-8)
    
    if sol.success:
        print("Dynamic simulation completed successfully")
        
        # Extract results
        time = sol.t
        CA_dynamic = sol.y[0]
        T_dynamic = sol.y[1]
        
        # Calculate conversion over time
        conversion_dynamic = [(operating_conditions['CAi'] - ca) / operating_conditions['CAi'] 
                            for ca in CA_dynamic]
        
        print(f"Final concentration: {CA_dynamic[-1]:.4f} mol/L")
        print(f"Final temperature: {T_dynamic[-1]:.2f} K")
        print(f"Final conversion: {conversion_dynamic[-1]:.1%}")
        print(f"Time to 95% of steady state: {find_settling_time(time, CA_dynamic, CA_ss):.1f} min")
    else:
        print("Dynamic simulation failed")
        return
    
    # Step response analysis
    print("\nStep Response Analysis:")
    print("-" * 30)
    
    # Step change in coolant temperature at t=30 min
    step_time = 30.0
    
    def step_input(t):
        if t < step_time:
            return u  # Original conditions
        else:
            u_step = u.copy()
            u_step[3] = 280.0  # Lower coolant temperature
            return u_step
    
    def cstr_ode_step(t, x):
        return reactor.dynamics(t, x, step_input(t))
    
    # Simulate step response
    t_span_step = (0, 100)
    t_eval_step = np.linspace(0, 100, 500)
    
    sol_step = solve_ivp(cstr_ode_step, t_span_step, x0, t_eval=t_eval_step, 
                        method='RK45', rtol=1e-8)
    
    if sol_step.success:
        time_step = sol_step.t
        CA_step = sol_step.y[0]
        T_step = sol_step.y[1]
        
        print(f"Temperature change after step: {T_step[-1] - T_step[0]:.2f} K")
        print(f"Concentration change after step: {CA_step[-1] - CA_step[0]:.4f} mol/L")
    
    # Display reactor metadata
    print("\nReactor Model Information:")
    print("-" * 30)
    
    try:
        metadata = reactor.describe()
        print(f"Type: {metadata['type']}")
        print(f"Description: {metadata['description']}")
        print("\nKey Equations:")
        for name, eq in metadata['algorithms'].items():
            print(f"  {name}: {eq}")
        
        print("\nValid Operating Ranges:")
        for param, range_info in metadata['valid_ranges'].items():
            print(f"  {param}: {range_info['min']}-{range_info['max']} {range_info['units']}")
    except AttributeError:
        print("describe() method not available - using basic information")
        print(f"Type: CSTR")
        print(f"Description: Continuous Stirred Tank Reactor model")
        print(f"Parameters: V={reactor.V}, k0={reactor.k0:.2e}, Ea={reactor.Ea}")
    
    # Create plots
    create_plots(time, CA_dynamic, T_dynamic, conversion_dynamic, 
                time_step, CA_step, T_step, step_time, operating_conditions)
    
    print("\nExample completed successfully!")
    print("Plots saved as cstr_example_plots.png and cstr_detailed_analysis.png")


def find_settling_time(time, response, steady_value, tolerance=0.05):
    """Find settling time (time to reach within 5% of steady state)."""
    target = abs(steady_value)
    tolerance_band = target * tolerance
    
    for i in range(len(response)-1, 0, -1):
        if abs(response[i] - steady_value) > tolerance_band:
            return time[i+1] if i+1 < len(time) else time[-1]
    
    return time[0]


def create_plots(time, CA, T, conversion, time_step, CA_step, T_step, step_time, conditions):
    """Create visualization plots for CSTR example."""
    
    # Plot 1: Dynamic response
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Concentration vs time
    ax1.plot(time, CA, 'b-', linewidth=2, label='Concentration')
    ax1.set_xlabel('Time (min)')
    ax1.set_ylabel('Concentration (mol/L)')
    ax1.set_title('CSTR Concentration Response')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Temperature vs time
    ax2.plot(time, T, 'r-', linewidth=2, label='Temperature')
    ax2.set_xlabel('Time (min)')
    ax2.set_ylabel('Temperature (K)')
    ax2.set_title('CSTR Temperature Response')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Conversion vs time
    ax3.plot(time, conversion, 'g-', linewidth=2, label='Conversion')
    ax3.set_xlabel('Time (min)')
    ax3.set_ylabel('Conversion (-)')
    ax3.set_title('CSTR Conversion Response')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # Phase portrait (Concentration vs Temperature)
    ax4.plot(CA, T, 'purple', linewidth=2, label='Trajectory')
    ax4.plot(CA[0], T[0], 'go', markersize=8, label='Start')
    ax4.plot(CA[-1], T[-1], 'ro', markersize=8, label='End')
    ax4.set_xlabel('Concentration (mol/L)')
    ax4.set_ylabel('Temperature (K)')
    ax4.set_title('CSTR Phase Portrait')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('cstr_example_plots.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 2: Step response analysis
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
    
    # Concentration step response
    ax1.plot(time_step, CA_step, 'b-', linewidth=2)
    ax1.axvline(x=step_time, color='k', linestyle='--', alpha=0.7, label='Step change')
    ax1.set_ylabel('Concentration (mol/L)')
    ax1.set_title('CSTR Step Response - Concentration')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Temperature step response
    ax2.plot(time_step, T_step, 'r-', linewidth=2)
    ax2.axvline(x=step_time, color='k', linestyle='--', alpha=0.7, label='Step change')
    ax2.set_ylabel('Temperature (K)')
    ax2.set_title('CSTR Step Response - Temperature')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Coolant temperature input
    coolant_temp = [conditions['Tc'] if t < step_time else 280.0 for t in time_step]
    ax3.plot(time_step, coolant_temp, 'orange', linewidth=2, label='Coolant Temperature')
    ax3.set_xlabel('Time (min)')
    ax3.set_ylabel('Coolant Temperature (K)')
    ax3.set_title('Input - Coolant Temperature Step Change')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    plt.tight_layout()
    plt.savefig('cstr_detailed_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    main()
