"""
BatchReactor Example

This example demonstrates the use of the BatchReactor model for simulating
a batch chemical reaction with temperature control.

Author: SPROCLIB Development Team
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import sys
import os

# Add the parent directory to sys.path to import from unit.reactor
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from unit.reactor.BatchReactor import BatchReactor


def main():
    """Main function demonstrating BatchReactor model usage."""
    
    print("="*60)
    print("BatchReactor Example")
    print("="*60)
    
    # Create BatchReactor instance
    reactor = BatchReactor(
        V=100.0,               # Reactor volume [L]
        k0=7.2e10,             # Pre-exponential factor [1/min]
        Ea=72750.0,            # Activation energy [J/mol]
        delta_H=-52000.0,      # Heat of reaction [J/mol]
        rho=1000.0,            # Density [kg/m³]
        cp=4180.0,             # Heat capacity [J/kg·K]
        U=500.0,               # Heat transfer coefficient [W/m²·K]
        A=5.0,                 # Heat transfer area [m²]
        name="Example_BatchReactor"
    )
    
    print(f"Reactor: {reactor.name}")
    print(f"Volume: {reactor.V} L")
    print(f"Heat transfer coefficient: {reactor.U} W/m²·K")
    print(f"Heat transfer area: {reactor.A} m²")
    print()
    
    # Define operating conditions
    operating_conditions = {
        'Tj': 350.0,           # Jacket temperature [K]
        'CA0': 2.0,            # Initial concentration [mol/L]
        'T0': 300.0            # Initial temperature [K]
    }
    
    print("Operating Conditions:")
    for param, value in operating_conditions.items():
        units = {'Tj': 'K', 'CA0': 'mol/L', 'T0': 'K'}
        print(f"  {param}: {value} {units[param]}")
    print()
    
    # Input vector for simulation (jacket temperature)
    u = np.array([operating_conditions['Tj']])
    
    # Initial conditions
    x0 = np.array([operating_conditions['CA0'], operating_conditions['T0']])
    
    # Calculate isothermal batch time for different conversions
    print("Isothermal Batch Time Analysis:")
    print("-" * 40)
    
    conversions = [0.5, 0.8, 0.9, 0.95, 0.99]
    T_isothermal = 350.0
    
    for conv in conversions:
        batch_time = reactor.batch_time_to_conversion(conv, operating_conditions['CA0'], T_isothermal)
        print(f"Time for {conv:.0%} conversion: {batch_time:.2f} min")
    print()
    
    # Dynamic simulation
    print("Dynamic Simulation:")
    print("-" * 30)
    
    # Time span for simulation
    t_span = (0, 120)  # 0 to 120 minutes
    t_eval = np.linspace(0, 120, 600)
    
    # Solve ODE
    def batch_ode(t, x):
        return reactor.dynamics(t, x, u)
    
    sol = solve_ivp(batch_ode, t_span, x0, t_eval=t_eval, method='RK45', rtol=1e-8)
    
    if sol.success:
        print("Dynamic simulation completed successfully")
        
        # Extract results
        time = sol.t
        CA_dynamic = sol.y[0]
        T_dynamic = sol.y[1]
        
        # Calculate conversion and reaction rate over time
        conversion_dynamic = [(operating_conditions['CA0'] - ca) / operating_conditions['CA0'] 
                            for ca in CA_dynamic]
        reaction_rate = [reactor.reaction_rate(ca, t) for ca, t in zip(CA_dynamic, T_dynamic)]
        
        print(f"Final concentration: {CA_dynamic[-1]:.4f} mol/L")
        print(f"Final temperature: {T_dynamic[-1]:.2f} K")
        print(f"Final conversion: {conversion_dynamic[-1]:.1%}")
        print(f"Maximum temperature: {np.max(T_dynamic):.2f} K")
        print(f"Time to 90% conversion: {find_time_to_conversion(time, conversion_dynamic, 0.9):.1f} min")
    else:
        print("Dynamic simulation failed")
        return
    
    # Temperature control scenario
    print("\nTemperature Control Scenario:")
    print("-" * 30)
    
    # Scenario with temperature ramping
    def temperature_profile(t):
        if t < 30:
            return 300.0  # Start at low temperature
        elif t < 60:
            return 300.0 + (350.0 - 300.0) * (t - 30) / 30  # Ramp up
        else:
            return 350.0  # Hold at high temperature
    
    def batch_ode_ramp(t, x):
        Tj = temperature_profile(t)
        return reactor.dynamics(t, x, np.array([Tj]))
    
    sol_ramp = solve_ivp(batch_ode_ramp, t_span, x0, t_eval=t_eval, method='RK45', rtol=1e-8)
    
    if sol_ramp.success:
        time_ramp = sol_ramp.t
        CA_ramp = sol_ramp.y[0]
        T_ramp = sol_ramp.y[1]
        conversion_ramp = [(operating_conditions['CA0'] - ca) / operating_conditions['CA0'] 
                          for ca in CA_ramp]
        
        print(f"Final conversion with temperature ramp: {conversion_ramp[-1]:.1%}")
        print(f"Maximum temperature with ramp: {np.max(T_ramp):.2f} K")
    
    # Multiple initial concentration study
    print("\nInitial Concentration Study:")
    print("-" * 30)
    
    initial_concentrations = [0.5, 1.0, 2.0, 3.0]
    final_conversions = []
    
    for CA0_study in initial_concentrations:
        x0_study = np.array([CA0_study, operating_conditions['T0']])
        sol_study = solve_ivp(batch_ode, (0, 120), x0_study, t_eval=np.linspace(0, 120, 100), 
                             method='RK45', rtol=1e-8)
        
        if sol_study.success:
            final_conversion = (CA0_study - sol_study.y[0][-1]) / CA0_study
            final_conversions.append(final_conversion)
            print(f"CA0 = {CA0_study:.1f} mol/L → Final conversion: {final_conversion:.1%}")
        else:
            final_conversions.append(0.0)
    
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
        print(f"Type: BatchReactor")
        print(f"Description: Batch reactor with heating/cooling")
        print(f"Parameters: V={reactor.V}, k0={reactor.k0:.2e}, Ea={reactor.Ea}")
    
    # Create plots
    create_plots(time, CA_dynamic, T_dynamic, conversion_dynamic, reaction_rate,
                time_ramp, CA_ramp, T_ramp, conversion_ramp, temperature_profile,
                initial_concentrations, final_conversions, operating_conditions)
    
    print("\nExample completed successfully!")
    print("Plots saved as batch_reactor_example_plots.png and batch_reactor_detailed_analysis.png")


def find_time_to_conversion(time, conversion, target_conversion):
    """Find time to reach target conversion."""
    for i, conv in enumerate(conversion):
        if conv >= target_conversion:
            return time[i]
    return time[-1]  # If target not reached


def create_plots(time, CA, T, conversion, reaction_rate, 
                time_ramp, CA_ramp, T_ramp, conversion_ramp, temp_profile,
                initial_concs, final_conversions, conditions):
    """Create visualization plots for BatchReactor example."""
    
    # Plot 1: Dynamic response
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Concentration vs time
    ax1.plot(time, CA, 'b-', linewidth=2, label='Concentration')
    ax1.set_xlabel('Time (min)')
    ax1.set_ylabel('Concentration (mol/L)')
    ax1.set_title('Batch Reactor Concentration')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Temperature vs time
    ax2.plot(time, T, 'r-', linewidth=2, label='Temperature')
    ax2.axhline(y=conditions['Tj'], color='orange', linestyle='--', alpha=0.7, label='Jacket Temp')
    ax2.set_xlabel('Time (min)')
    ax2.set_ylabel('Temperature (K)')
    ax2.set_title('Batch Reactor Temperature')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Conversion vs time
    ax3.plot(time, conversion, 'g-', linewidth=2, label='Conversion')
    ax3.set_xlabel('Time (min)')
    ax3.set_ylabel('Conversion (-)')
    ax3.set_title('Batch Reactor Conversion')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # Reaction rate vs time
    ax4.plot(time, reaction_rate, 'purple', linewidth=2, label='Reaction Rate')
    ax4.set_xlabel('Time (min)')
    ax4.set_ylabel('Reaction Rate (mol/L/min)')
    ax4.set_title('Reaction Rate')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('batch_reactor_example_plots.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 2: Detailed analysis
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Temperature control comparison
    ax1.plot(time, T, 'b-', linewidth=2, label='Constant Jacket')
    ax1.plot(time_ramp, T_ramp, 'r-', linewidth=2, label='Temperature Ramp')
    jacket_temp = [temp_profile(t) for t in time_ramp]
    ax1.plot(time_ramp, jacket_temp, 'orange', linestyle='--', alpha=0.7, label='Jacket Profile')
    ax1.set_xlabel('Time (min)')
    ax1.set_ylabel('Temperature (K)')
    ax1.set_title('Temperature Control Comparison')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Conversion comparison
    ax2.plot(time, conversion, 'b-', linewidth=2, label='Constant Jacket')
    ax2.plot(time_ramp, conversion_ramp, 'r-', linewidth=2, label='Temperature Ramp')
    ax2.set_xlabel('Time (min)')
    ax2.set_ylabel('Conversion (-)')
    ax2.set_title('Conversion Comparison')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Initial concentration study
    ax3.bar(range(len(initial_concs)), final_conversions, color='green', alpha=0.7)
    ax3.set_xlabel('Initial Concentration (mol/L)')
    ax3.set_ylabel('Final Conversion (-)')
    ax3.set_title('Effect of Initial Concentration')
    ax3.set_xticks(range(len(initial_concs)))
    ax3.set_xticklabels([f'{c:.1f}' for c in initial_concs])
    ax3.grid(True, alpha=0.3)
    
    # Phase portrait
    ax4.plot(CA, T, 'purple', linewidth=2, label='Trajectory')
    ax4.plot(CA[0], T[0], 'go', markersize=8, label='Start')
    ax4.plot(CA[-1], T[-1], 'ro', markersize=8, label='End')
    ax4.set_xlabel('Concentration (mol/L)')
    ax4.set_ylabel('Temperature (K)')
    ax4.set_title('Batch Reactor Phase Portrait')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('batch_reactor_detailed_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    main()
