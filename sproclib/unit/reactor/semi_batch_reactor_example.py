"""
Semi-Batch Reactor Example

This example demonstrates the usage of the SemiBatchReactor class
for simulating fed-batch processes with variable feed profiles.

Author: Generated for SPROCLIB Documentation
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import sys
import os

# Add the parent directory to sys.path to import sproclib modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from unit.reactor.SemiBatchReactor import SemiBatchReactor


def fed_batch_simulation():
    """Simulate a fed-batch reactor with variable feed profile."""
    
    print("Semi-Batch Reactor Example")
    print("=" * 50)
    
    # Create reactor instance
    reactor = SemiBatchReactor(
        V_max=200.0,        # Maximum volume [L]
        k0=7.2e10,          # Pre-exponential factor [1/min]
        Ea=72750.0,         # Activation energy [J/mol]
        delta_H=-52000.0,   # Heat of reaction [J/mol]
        name="Fed-Batch Reactor"
    )
    
    print(f"Reactor: {reactor.name}")
    print(f"Maximum Volume: {reactor.V_max} L")
    print(f"Activation Energy: {reactor.Ea/1000:.1f} kJ/mol")
    print(f"Heat of Reaction: {reactor.delta_H/1000:.1f} kJ/mol")
    print()
    
    # Simulation parameters
    t_final = 120.0  # minutes
    
    # Initial conditions
    nA0 = 20.0   # Initial moles [mol]
    T0 = 300.0   # Initial temperature [K]
    V0 = 50.0    # Initial volume [L]
    x0 = np.array([nA0, T0, V0])
    
    print("Initial Conditions:")
    print(f"Initial moles: {nA0} mol")
    print(f"Initial temperature: {T0} K")
    print(f"Initial volume: {V0} L")
    print(f"Initial concentration: {nA0/V0:.2f} mol/L")
    print()
    
    # Define time-varying feed profile
    def feed_profile(t):
        """Define feed flow rate profile over time."""
        if t <= 60:
            return 1.0  # Constant feed for first hour
        elif t <= 90:
            return 0.5  # Reduced feed
        else:
            return 0.0  # No feed in final phase
    
    # Control inputs function
    def control_inputs(t):
        qf = feed_profile(t)      # Feed flow rate [L/min]
        CAf = 2.0                 # Feed concentration [mol/L]
        Tf = 310.0                # Feed temperature [K]
        Tj = 295.0                # Jacket temperature [K]
        return np.array([qf, CAf, Tf, Tj])
    
    # Define ODE system
    def reactor_ode(t, x):
        u = control_inputs(t)
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
    nA = sol.y[0]
    T = sol.y[1]
    V = sol.y[2]
    
    # Calculate derived quantities
    CA = nA / V  # Concentration [mol/L]
    conversion = (nA0 - nA) / nA0  # Conversion
    feed_rates = np.array([feed_profile(ti) for ti in t])
    
    print("Simulation completed successfully!")
    print()
    
    # Print final results
    final_time = t[-1]
    final_nA = nA[-1]
    final_T = T[-1]
    final_V = V[-1]
    final_CA = CA[-1]
    final_conversion = conversion[-1]
    
    print("Final Results:")
    print(f"Time: {final_time:.1f} min")
    print(f"Moles: {final_nA:.2f} mol")
    print(f"Temperature: {final_T:.1f} K")
    print(f"Volume: {final_V:.1f} L")
    print(f"Concentration: {final_CA:.3f} mol/L")
    print(f"Conversion: {final_conversion:.1%}")
    print()
    
    # Create comprehensive plots
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Semi-Batch Reactor Fed-Batch Operation', fontsize=16, fontweight='bold')
    
    # Plot 1: Moles vs Time
    axes[0, 0].plot(t, nA, 'b-', linewidth=2, label='Moles A')
    axes[0, 0].set_xlabel('Time (min)')
    axes[0, 0].set_ylabel('Moles (mol)')
    axes[0, 0].set_title('Reactant Moles')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend()
    
    # Plot 2: Temperature vs Time
    axes[0, 1].plot(t, T - 273.15, 'r-', linewidth=2, label='Temperature')
    axes[0, 1].axhline(y=310-273.15, color='g', linestyle='--', alpha=0.7, label='Feed Temp')
    axes[0, 1].axhline(y=295-273.15, color='c', linestyle='--', alpha=0.7, label='Jacket Temp')
    axes[0, 1].set_xlabel('Time (min)')
    axes[0, 1].set_ylabel('Temperature (°C)')
    axes[0, 1].set_title('Temperature Profile')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].legend()
    
    # Plot 3: Volume vs Time
    axes[0, 2].plot(t, V, 'g-', linewidth=2, label='Volume')
    axes[0, 2].axhline(y=reactor.V_max, color='r', linestyle='--', alpha=0.7, label='Max Volume')
    axes[0, 2].set_xlabel('Time (min)')
    axes[0, 2].set_ylabel('Volume (L)')
    axes[0, 2].set_title('Reactor Volume')
    axes[0, 2].grid(True, alpha=0.3)
    axes[0, 2].legend()
    
    # Plot 4: Concentration vs Time
    axes[1, 0].plot(t, CA, 'm-', linewidth=2, label='Concentration A')
    axes[1, 0].set_xlabel('Time (min)')
    axes[1, 0].set_ylabel('Concentration (mol/L)')
    axes[1, 0].set_title('Reactant Concentration')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend()
    
    # Plot 5: Conversion vs Time
    axes[1, 1].plot(t, conversion * 100, 'orange', linewidth=2, label='Conversion')
    axes[1, 1].set_xlabel('Time (min)')
    axes[1, 1].set_ylabel('Conversion (%)')
    axes[1, 1].set_title('Reaction Conversion')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].legend()
    
    # Plot 6: Feed Rate Profile
    axes[1, 2].plot(t, feed_rates, 'k-', linewidth=2, label='Feed Rate')
    axes[1, 2].set_xlabel('Time (min)')
    axes[1, 2].set_ylabel('Feed Rate (L/min)')
    axes[1, 2].set_title('Feed Rate Profile')
    axes[1, 2].grid(True, alpha=0.3)
    axes[1, 2].legend()
    
    plt.tight_layout()
    plt.savefig('/Users/macmini/Desktop/github/sproclib/unit/reactor/semi_batch_reactor_example_plots.png', 
                dpi=300, bbox_inches='tight')
    plt.show()
    
    # Create detailed analysis plot
    fig2, axes2 = plt.subplots(2, 2, figsize=(12, 10))
    fig2.suptitle('Semi-Batch Reactor Detailed Analysis', fontsize=16, fontweight='bold')
    
    # Calculate reaction rates
    R = 8.314  # Gas constant
    reaction_rates = []
    for i in range(len(t)):
        k = reactor.k0 * np.exp(-reactor.Ea / (R * T[i]))
        r = k * CA[i]
        reaction_rates.append(r)
    reaction_rates = np.array(reaction_rates)
    
    # Plot 1: Reaction Rate vs Time
    axes2[0, 0].plot(t, reaction_rates, 'purple', linewidth=2)
    axes2[0, 0].set_xlabel('Time (min)')
    axes2[0, 0].set_ylabel('Reaction Rate (mol/L·min)')
    axes2[0, 0].set_title('Reaction Rate Profile')
    axes2[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Concentration vs Volume
    axes2[0, 1].plot(V, CA, 'brown', linewidth=2)
    axes2[0, 1].set_xlabel('Volume (L)')
    axes2[0, 1].set_ylabel('Concentration (mol/L)')
    axes2[0, 1].set_title('Concentration vs Volume')
    axes2[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Temperature vs Conversion
    axes2[1, 0].plot(conversion * 100, T - 273.15, 'red', linewidth=2)
    axes2[1, 0].set_xlabel('Conversion (%)')
    axes2[1, 0].set_ylabel('Temperature (°C)')
    axes2[1, 0].set_title('Temperature vs Conversion')
    axes2[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Productivity over time (moles produced per unit time)
    productivity = np.gradient(nA0 - nA, t)  # Rate of product formation
    axes2[1, 1].plot(t, productivity, 'green', linewidth=2)
    axes2[1, 1].set_xlabel('Time (min)')
    axes2[1, 1].set_ylabel('Productivity (mol/min)')
    axes2[1, 1].set_title('Instantaneous Productivity')
    axes2[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/Users/macmini/Desktop/github/sproclib/unit/reactor/semi_batch_reactor_detailed_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.show()
    
    return t, nA, T, V, CA, conversion


def compare_feed_strategies():
    """Compare different feeding strategies."""
    
    print("\nComparing Different Feed Strategies")
    print("=" * 50)
    
    reactor = SemiBatchReactor(name="Comparison Reactor")
    
    # Common parameters
    t_final = 100.0
    x0 = np.array([20.0, 300.0, 50.0])  # nA0, T0, V0
    
    strategies = {
        'Constant Feed': lambda t: 1.0 if t <= 80 else 0.0,
        'Linear Decrease': lambda t: max(0, 1.5 - t/60) if t <= 90 else 0.0,
        'Exponential Decay': lambda t: 1.2 * np.exp(-t/40) if t <= 90 else 0.0
    }
    
    results = {}
    
    for strategy_name, feed_func in strategies.items():
        def control_inputs(t):
            return np.array([feed_func(t), 2.0, 310.0, 295.0])
        
        def reactor_ode(t, x):
            u = control_inputs(t)
            return reactor.dynamics(t, x, u)
        
        sol = solve_ivp(reactor_ode, (0, t_final), x0, 
                       t_eval=np.linspace(0, t_final, 500),
                       method='RK45', rtol=1e-6)
        
        if sol.success:
            results[strategy_name] = {
                't': sol.t,
                'nA': sol.y[0],
                'T': sol.y[1],
                'V': sol.y[2],
                'conversion': (x0[0] - sol.y[0]) / x0[0],
                'final_conversion': (x0[0] - sol.y[0][-1]) / x0[0]
            }
    
    # Plot comparison
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Comparison of Feed Strategies', fontsize=16, fontweight='bold')
    
    colors = ['blue', 'red', 'green']
    
    for i, (strategy, data) in enumerate(results.items()):
        color = colors[i]
        
        # Conversion
        axes[0, 0].plot(data['t'], data['conversion'] * 100, 
                       color=color, linewidth=2, label=strategy)
        
        # Temperature
        axes[0, 1].plot(data['t'], data['T'] - 273.15, 
                       color=color, linewidth=2, label=strategy)
        
        # Volume
        axes[1, 0].plot(data['t'], data['V'], 
                       color=color, linewidth=2, label=strategy)
        
        # Moles
        axes[1, 1].plot(data['t'], data['nA'], 
                       color=color, linewidth=2, label=strategy)
    
    axes[0, 0].set_xlabel('Time (min)')
    axes[0, 0].set_ylabel('Conversion (%)')
    axes[0, 0].set_title('Conversion Comparison')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend()
    
    axes[0, 1].set_xlabel('Time (min)')
    axes[0, 1].set_ylabel('Temperature (°C)')
    axes[0, 1].set_title('Temperature Comparison')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].legend()
    
    axes[1, 0].set_xlabel('Time (min)')
    axes[1, 0].set_ylabel('Volume (L)')
    axes[1, 0].set_title('Volume Comparison')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend()
    
    axes[1, 1].set_xlabel('Time (min)')
    axes[1, 1].set_ylabel('Moles (mol)')
    axes[1, 1].set_title('Reactant Moles Comparison')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.savefig('/Users/macmini/Desktop/github/sproclib/unit/reactor/semi_batch_feed_comparison.png', 
                dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print final conversions
    print("Final Conversions:")
    for strategy, data in results.items():
        print(f"{strategy}: {data['final_conversion']:.1%}")


def main():
    """Run the semi-batch reactor example."""
    
    # Test reactor introspection
    reactor = SemiBatchReactor()
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
    fed_batch_simulation()
    
    # Compare strategies
    compare_feed_strategies()
    
    print("\nSemi-batch reactor example completed successfully!")


if __name__ == "__main__":
    main()
