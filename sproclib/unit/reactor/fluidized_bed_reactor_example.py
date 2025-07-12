"""
Fluidized Bed Reactor Example

This example demonstrates the usage of the FluidizedBedReactor class
for simulating catalytic processes with two-phase flow behavior.

Author: Generated for SPROCLIB Documentation
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import sys
import os

# Add the parent directory to sys.path to import sproclib modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from unit.reactor.FluidizedBedReactor import FluidizedBedReactor


def fluidized_bed_simulation():
    """Simulate a fluidized bed reactor with varying gas velocity."""
    
    print("Fluidized Bed Reactor Example")
    print("=" * 50)
    
    # Create reactor instance
    reactor = FluidizedBedReactor(
        H=3.0,              # Bed height [m]
        D=2.0,              # Bed diameter [m]
        U_mf=0.1,           # Minimum fluidization velocity [m/s]
        rho_cat=1500.0,     # Catalyst density [kg/m³]
        dp=0.0005,          # Particle diameter [m]
        k0=1e5,             # Pre-exponential factor [m³/kg·s]
        Ea=60000.0,         # Activation energy [J/mol]
        name="Fluidized Bed Reactor"
    )
    
    print(f"Reactor: {reactor.name}")
    print(f"Bed Height: {reactor.H} m")
    print(f"Bed Diameter: {reactor.D} m")
    print(f"Minimum Fluidization Velocity: {reactor.U_mf} m/s")
    print(f"Catalyst Density: {reactor.rho_cat} kg/m³")
    print(f"Particle Diameter: {reactor.dp*1000:.2f} mm")
    print(f"Activation Energy: {reactor.Ea/1000:.1f} kJ/mol")
    print()
    
    # Simulation parameters
    t_final = 300.0  # seconds
    
    # Operating conditions
    CA_in = 100.0    # Inlet concentration [mol/m³]
    T_in = 700.0     # Inlet temperature [K]
    U_g = 0.3        # Superficial gas velocity [m/s]
    T_coolant = 650.0 # Coolant temperature [K]
    
    print("Operating Conditions:")
    print(f"Inlet concentration: {CA_in} mol/m³")
    print(f"Inlet temperature: {T_in} K ({T_in-273.15:.1f} °C)")
    print(f"Superficial gas velocity: {U_g} m/s")
    print(f"Coolant temperature: {T_coolant} K ({T_coolant-273.15:.1f} °C)")
    print()
    
    # Check fluidization regime
    if U_g > reactor.U_mf:
        print(f"Reactor is fluidized (U_g > U_mf)")
        print(f"Excess velocity: {U_g - reactor.U_mf:.3f} m/s")
    else:
        print(f"Reactor is NOT fluidized (U_g < U_mf)")
    print()
    
    # Calculate fluidization properties
    props = reactor.fluidization_properties(U_g)
    print("Fluidization Properties:")
    print(f"Bubble velocity: {props['bubble_velocity']:.3f} m/s")
    print(f"Bubble fraction: {props['bubble_fraction']:.3f}")
    print(f"Emulsion fraction: {props['emulsion_fraction']:.3f}")
    print()
    
    # Initial conditions - start with inlet conditions
    CA_bubble_0 = CA_in
    CA_emulsion_0 = CA_in  
    T0 = T_in
    x0 = np.array([CA_bubble_0, CA_emulsion_0, T0])
    
    print("Initial Conditions:")
    print(f"Bubble phase concentration: {CA_bubble_0} mol/m³")
    print(f"Emulsion phase concentration: {CA_emulsion_0} mol/m³")
    print(f"Temperature: {T0} K ({T0-273.15:.1f} °C)")
    print()
    
    # Control inputs
    u = np.array([CA_in, T_in, U_g, T_coolant])
    
    # Define ODE system
    def reactor_ode(t, x):
        return reactor.dynamics(t, x, u)
    
    # Solve ODE
    print("Solving reactor dynamics...")
    t_span = (0, t_final)
    t_eval = np.linspace(0, t_final, 1000)
    
    sol = solve_ivp(reactor_ode, t_span, x0, t_eval=t_eval, 
                    method='RK45', rtol=1e-6, atol=1e-8)
    
    if not sol.success:
        print(f"Integration failed: {sol.message}")
        return
    
    t = sol.t
    CA_bubble = sol.y[0]
    CA_emulsion = sol.y[1]
    T = sol.y[2]
    
    # Calculate derived quantities
    CA_avg = props['bubble_fraction'] * CA_bubble + props['emulsion_fraction'] * CA_emulsion
    conversion = (CA_in - CA_avg) / CA_in * 100
    
    # Calculate reaction rates over time
    R_const = 8.314
    reaction_rates = []
    for i in range(len(t)):
        k = reactor.k0 * np.exp(-reactor.Ea / (R_const * T[i]))
        r = k * CA_emulsion[i]
        reaction_rates.append(r)
    reaction_rates = np.array(reaction_rates)
    
    print("Simulation completed successfully!")
    print()
    
    # Print final results
    final_time = t[-1]
    final_CA_bubble = CA_bubble[-1]
    final_CA_emulsion = CA_emulsion[-1]
    final_T = T[-1]
    final_CA_avg = CA_avg[-1]
    final_conversion = conversion[-1]
    final_reaction_rate = reaction_rates[-1]
    
    print("Final Results:")
    print(f"Time: {final_time:.1f} s")
    print(f"Bubble phase concentration: {final_CA_bubble:.2f} mol/m³")
    print(f"Emulsion phase concentration: {final_CA_emulsion:.2f} mol/m³")
    print(f"Average concentration: {final_CA_avg:.2f} mol/m³")
    print(f"Temperature: {final_T:.1f} K ({final_T-273.15:.1f} °C)")
    print(f"Conversion: {final_conversion:.1f}%")
    print(f"Reaction rate: {final_reaction_rate:.2e} mol/kg·s")
    print()
    
    # Create comprehensive plots
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Fluidized Bed Reactor Two-Phase Behavior', fontsize=16, fontweight='bold')
    
    # Plot 1: Concentrations vs Time
    axes[0, 0].plot(t, CA_bubble, 'b-', linewidth=2, label='Bubble Phase')
    axes[0, 0].plot(t, CA_emulsion, 'r-', linewidth=2, label='Emulsion Phase')
    axes[0, 0].plot(t, CA_avg, 'g--', linewidth=2, label='Average')
    axes[0, 0].axhline(y=CA_in, color='k', linestyle=':', alpha=0.7, label='Inlet')
    axes[0, 0].set_xlabel('Time (s)')
    axes[0, 0].set_ylabel('Concentration (mol/m³)')
    axes[0, 0].set_title('Phase Concentrations')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend()
    
    # Plot 2: Temperature vs Time
    axes[0, 1].plot(t, T - 273.15, 'r-', linewidth=2, label='Temperature')
    axes[0, 1].axhline(y=T_in-273.15, color='g', linestyle='--', alpha=0.7, label='Inlet Temp')
    axes[0, 1].axhline(y=T_coolant-273.15, color='c', linestyle='--', alpha=0.7, label='Coolant Temp')
    axes[0, 1].set_xlabel('Time (s)')
    axes[0, 1].set_ylabel('Temperature (°C)')
    axes[0, 1].set_title('Temperature Profile')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].legend()
    
    # Plot 3: Conversion vs Time
    axes[0, 2].plot(t, conversion, 'm-', linewidth=2, label='Conversion')
    axes[0, 2].set_xlabel('Time (s)')
    axes[0, 2].set_ylabel('Conversion (%)')
    axes[0, 2].set_title('Overall Conversion')
    axes[0, 2].grid(True, alpha=0.3)
    axes[0, 2].legend()
    
    # Plot 4: Reaction Rate vs Time
    axes[1, 0].semilogy(t, reaction_rates, 'purple', linewidth=2, label='Reaction Rate')
    axes[1, 0].set_xlabel('Time (s)')
    axes[1, 0].set_ylabel('Reaction Rate (mol/kg·s)')
    axes[1, 0].set_title('Reaction Rate Profile')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend()
    
    # Plot 5: Phase Concentration Difference
    conc_diff = CA_bubble - CA_emulsion
    axes[1, 1].plot(t, conc_diff, 'orange', linewidth=2, label='Bubble - Emulsion')
    axes[1, 1].set_xlabel('Time (s)')
    axes[1, 1].set_ylabel('Concentration Difference (mol/m³)')
    axes[1, 1].set_title('Inter-Phase Concentration Driving Force')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].legend()
    
    # Plot 6: Temperature vs Conversion
    axes[1, 2].plot(conversion, T - 273.15, 'brown', linewidth=2)
    axes[1, 2].set_xlabel('Conversion (%)')
    axes[1, 2].set_ylabel('Temperature (°C)')
    axes[1, 2].set_title('Temperature vs Conversion')
    axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/Users/macmini/Desktop/github/sproclib/unit/reactor/fluidized_bed_reactor_example_plots.png', 
                dpi=300, bbox_inches='tight')
    plt.show()
    
    return t, CA_bubble, CA_emulsion, T, conversion


def velocity_effect_study():
    """Study the effect of superficial gas velocity on reactor performance."""
    
    print("\nEffect of Superficial Gas Velocity")
    print("=" * 50)
    
    reactor = FluidizedBedReactor(name="Velocity Study Reactor")
    
    # Test different velocities
    velocities = np.array([0.05, 0.1, 0.2, 0.3, 0.5, 0.8])  # m/s
    
    # Operating conditions
    CA_in = 100.0
    T_in = 700.0
    T_coolant = 650.0
    t_final = 200.0
    
    results = {}
    
    for U_g in velocities:
        print(f"Testing U_g = {U_g:.2f} m/s")
        
        # Check if fluidized
        if U_g <= reactor.U_mf:
            print(f"  Not fluidized (U_mf = {reactor.U_mf} m/s)")
            continue
        
        # Initial conditions
        x0 = np.array([CA_in, CA_in, T_in])
        u = np.array([CA_in, T_in, U_g, T_coolant])
        
        # Solve
        def reactor_ode(t, x):
            return reactor.dynamics(t, x, u)
        
        sol = solve_ivp(reactor_ode, (0, t_final), x0, 
                       t_eval=np.linspace(0, t_final, 300),
                       method='RK45', rtol=1e-6)
        
        if sol.success:
            props = reactor.fluidization_properties(U_g)
            CA_avg = (props['bubble_fraction'] * sol.y[0] + 
                     props['emulsion_fraction'] * sol.y[1])
            conversion = (CA_in - CA_avg) / CA_in * 100
            
            results[U_g] = {
                't': sol.t,
                'CA_bubble': sol.y[0],
                'CA_emulsion': sol.y[1],
                'T': sol.y[2],
                'conversion': conversion,
                'final_conversion': conversion[-1],
                'final_temp': sol.y[2][-1],
                'bubble_fraction': props['bubble_fraction']
            }
    
    # Plot velocity effects
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Effect of Superficial Gas Velocity', fontsize=16, fontweight='bold')
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(results)))
    
    for i, (U_g, data) in enumerate(results.items()):
        color = colors[i]
        label = f'U_g = {U_g:.2f} m/s'
        
        # Conversion vs time
        axes[0, 0].plot(data['t'], data['conversion'], 
                       color=color, linewidth=2, label=label)
        
        # Temperature vs time
        axes[0, 1].plot(data['t'], data['T'] - 273.15, 
                       color=color, linewidth=2, label=label)
        
        # Emulsion concentration vs time
        axes[1, 0].plot(data['t'], data['CA_emulsion'], 
                       color=color, linewidth=2, label=label)
        
        # Bubble concentration vs time
        axes[1, 1].plot(data['t'], data['CA_bubble'], 
                       color=color, linewidth=2, label=label)
    
    axes[0, 0].set_xlabel('Time (s)')
    axes[0, 0].set_ylabel('Conversion (%)')
    axes[0, 0].set_title('Conversion vs Time')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend()
    
    axes[0, 1].set_xlabel('Time (s)')
    axes[0, 1].set_ylabel('Temperature (°C)')
    axes[0, 1].set_title('Temperature vs Time')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].legend()
    
    axes[1, 0].set_xlabel('Time (s)')
    axes[1, 0].set_ylabel('Emulsion Concentration (mol/m³)')
    axes[1, 0].set_title('Emulsion Phase Concentration')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend()
    
    axes[1, 1].set_xlabel('Time (s)')
    axes[1, 1].set_ylabel('Bubble Concentration (mol/m³)')
    axes[1, 1].set_title('Bubble Phase Concentration')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.savefig('/Users/macmini/Desktop/github/sproclib/unit/reactor/fluidized_bed_velocity_study.png', 
                dpi=300, bbox_inches='tight')
    plt.show()
    
    # Summary of velocity effects
    print("\nVelocity Effect Summary:")
    print("U_g (m/s) | Final Conv (%) | Final Temp (°C) | Bubble Frac")
    print("-" * 60)
    for U_g, data in results.items():
        print(f"{U_g:8.2f} | {data['final_conversion']:13.1f} | "
              f"{data['final_temp']-273.15:14.1f} | {data['bubble_fraction']:10.3f}")


def fluidization_regime_map():
    """Create a fluidization regime map."""
    
    print("\nFluidization Regime Analysis")
    print("=" * 50)
    
    reactor = FluidizedBedReactor()
    
    # Range of gas velocities
    U_g_range = np.linspace(0.01, 1.0, 100)
    
    bubble_fractions = []
    emulsion_fractions = []
    bubble_velocities = []
    
    for U_g in U_g_range:
        props = reactor.fluidization_properties(U_g)
        bubble_fractions.append(props['bubble_fraction'])
        emulsion_fractions.append(props['emulsion_fraction'])
        bubble_velocities.append(props['bubble_velocity'])
    
    # Create regime map
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Fluidization Regime Map', fontsize=16, fontweight='bold')
    
    # Plot 1: Phase fractions vs velocity
    axes[0].plot(U_g_range, bubble_fractions, 'b-', linewidth=2, label='Bubble Fraction')
    axes[0].plot(U_g_range, emulsion_fractions, 'r-', linewidth=2, label='Emulsion Fraction')
    axes[0].axvline(x=reactor.U_mf, color='k', linestyle='--', alpha=0.7, label='U_mf')
    axes[0].set_xlabel('Superficial Gas Velocity (m/s)')
    axes[0].set_ylabel('Phase Fraction (-)')
    axes[0].set_title('Phase Fractions')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    
    # Plot 2: Bubble velocity vs gas velocity
    axes[1].plot(U_g_range, bubble_velocities, 'g-', linewidth=2, label='Bubble Velocity')
    axes[1].plot(U_g_range, U_g_range, 'k--', alpha=0.5, label='Gas Velocity')
    axes[1].axvline(x=reactor.U_mf, color='k', linestyle='--', alpha=0.7, label='U_mf')
    axes[1].set_xlabel('Superficial Gas Velocity (m/s)')
    axes[1].set_ylabel('Velocity (m/s)')
    axes[1].set_title('Bubble Velocity')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    
    # Plot 3: Excess velocity vs bubble fraction
    excess_velocities = np.maximum(0, U_g_range - reactor.U_mf)
    axes[2].plot(excess_velocities, bubble_fractions, 'm-', linewidth=2)
    axes[2].set_xlabel('Excess Velocity (U_g - U_mf) [m/s]')
    axes[2].set_ylabel('Bubble Fraction (-)')
    axes[2].set_title('Bubble Fraction vs Excess Velocity')
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/Users/macmini/Desktop/github/sproclib/unit/reactor/fluidized_bed_regime_map.png', 
                dpi=300, bbox_inches='tight')
    plt.show()


def main():
    """Run the fluidized bed reactor example."""
    
    # Test reactor introspection
    reactor = FluidizedBedReactor()
    metadata = reactor.describe()
    
    print("Reactor Metadata:")
    print(f"Type: {metadata['type']}")
    print(f"Description: {metadata['description']}")
    print(f"Category: {metadata['category']}")
    print()
    
    print("Algorithms:")
    for alg, desc in metadata['algorithms'].items():
        print(f"  {alg}: {desc}")
    print()
    
    print("Applications:")
    for app in metadata['applications']:
        print(f"  - {app}")
    print()
    
    # Run main simulation
    fluidized_bed_simulation()
    
    # Study velocity effects
    velocity_effect_study()
    
    # Create regime map
    fluidization_regime_map()
    
    print("\nFluidized bed reactor example completed successfully!")


if __name__ == "__main__":
    main()
