"""
FixedBedReactor Example

This example demonstrates the use of the FixedBedReactor model for simulating
packed bed catalytic reactors with solid catalyst particles.

Author: SPROCLIB Development Team
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the parent directory to sys.path to import from unit.reactor
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from unit.reactor.FixedBedReactor import FixedBedReactor


def main():
    """Main function demonstrating FixedBedReactor model usage."""
    
    print("="*60)
    print("FixedBedReactor Example")
    print("="*60)
    
    # Create FixedBedReactor instance
    reactor = FixedBedReactor(
        L=5.0,                 # Bed length [m]
        D=1.0,                 # Bed diameter [m]
        epsilon=0.4,           # Bed porosity [-]
        rho_cat=1500.0,        # Catalyst density [kg/m³]
        dp=0.005,              # Particle diameter [m]
        k0=1e6,                # Pre-exponential factor [m³/kg·s]
        Ea=50000.0,            # Activation energy [J/mol]
        delta_H=-50000.0,      # Heat of reaction [J/mol]
        U=100.0,               # Heat transfer coefficient [W/m²·K]
        n_segments=20,         # Number of segments
        name="Example_FixedBed"
    )
    
    print(f"Reactor: {reactor.name}")
    print(f"Bed length: {reactor.L} m")
    print(f"Bed diameter: {reactor.D} m")
    print(f"Bed porosity: {reactor.epsilon}")
    print(f"Catalyst density: {reactor.rho_cat} kg/m³")
    print(f"Particle diameter: {reactor.dp*1000:.1f} mm")
    print(f"Total bed volume: {reactor.V_total:.3f} m³")
    print(f"Void volume: {reactor.V_void:.3f} m³")
    print()
    
    # Define operating conditions
    operating_conditions = {
        'u': 0.1,              # Superficial velocity [m/s]
        'CAi': 1000.0,         # Inlet concentration [mol/m³]
        'Ti': 450.0,           # Inlet temperature [K]
        'Tw': 430.0            # Wall temperature [K]
    }
    
    print("Operating Conditions:")
    for param, value in operating_conditions.items():
        units = {'u': 'm/s', 'CAi': 'mol/m³', 'Ti': 'K', 'Tw': 'K'}
        print(f"  {param}: {value} {units[param]}")
    print()
    
    # Input vector for simulation
    u = np.array([operating_conditions[key] for key in ['u', 'CAi', 'Ti', 'Tw']])
    
    # Calculate steady-state profiles
    print("Steady-State Analysis:")
    print("-" * 30)
    
    x_ss = reactor.steady_state(u)
    
    # Extract profiles
    n_seg = reactor.n_segments
    CA_profile = x_ss[:n_seg]
    T_profile = x_ss[n_seg:]
    
    # Axial positions
    z_positions = np.linspace(0, reactor.L, n_seg)
    
    # Calculate performance metrics
    conversion = reactor.calculate_conversion(x_ss)
    residence_time = reactor.V_void / (operating_conditions['u'] * reactor.A_cross * 60)  # minutes
    space_velocity = operating_conditions['u'] * 3600 / reactor.L  # 1/h
    
    print(f"Overall conversion: {conversion:.1%}")
    print(f"Inlet concentration: {CA_profile[0]:.1f} mol/m³")
    print(f"Outlet concentration: {CA_profile[-1]:.1f} mol/m³")
    print(f"Inlet temperature: {T_profile[0]:.1f} K")
    print(f"Outlet temperature: {T_profile[-1]:.1f} K")
    print(f"Maximum temperature: {np.max(T_profile):.1f} K")
    print(f"Residence time: {residence_time:.2f} min")
    print(f"Space velocity: {space_velocity:.1f} h⁻¹")
    print()
    
    # Display reactor metadata
    print("Reactor Model Information:")
    print("-" * 30)
    
    try:
        metadata = reactor.describe()
        print(f"Type: {metadata['type']}")
        print(f"Description: {metadata['description']}")
        print("\nKey Applications:")
        for app in metadata['applications']:
            print(f"  - {app}")
    except AttributeError:
        print("describe() method not available - using basic information")
        print(f"Type: FixedBedReactor")
        print(f"Description: Packed bed catalytic reactor")
    
    # Generate plots
    print("Generating plots...")
    print("-" * 30)
    
    # Create comprehensive plots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Fixed Bed Reactor Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Concentration profile
    ax1.plot(z_positions, CA_profile, 'b-', linewidth=2, marker='o', markersize=4)
    ax1.set_xlabel('Axial Position (m)')
    ax1.set_ylabel('Concentration (mol/m³)')
    ax1.set_title('Concentration Profile')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, reactor.L)
    
    # Plot 2: Temperature profile
    ax2.plot(z_positions, T_profile, 'r-', linewidth=2, marker='s', markersize=4)
    ax2.set_xlabel('Axial Position (m)')
    ax2.set_ylabel('Temperature (K)')
    ax2.set_title('Temperature Profile')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, reactor.L)
    
    # Plot 3: Conversion profile
    conversion_profile = 1 - CA_profile / operating_conditions['CAi'] if operating_conditions['CAi'] > 0 else np.zeros_like(CA_profile)
    ax3.plot(z_positions, conversion_profile * 100, 'g-', linewidth=2, marker='^', markersize=4)
    ax3.set_xlabel('Axial Position (m)')
    ax3.set_ylabel('Conversion (%)')
    ax3.set_title('Conversion Profile')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, reactor.L)
    ax3.set_ylim(0, 100)
    
    # Plot 4: Reaction rate profile (approximate)
    # Calculate reaction rates along the bed
    rates = []
    for i in range(len(CA_profile)):
        rate = reactor.k0 * np.exp(-reactor.Ea / (8.314 * T_profile[i])) * CA_profile[i] * reactor.rho_cat * (1 - reactor.epsilon)
        rates.append(rate)
    
    ax4.plot(z_positions, rates, 'm-', linewidth=2, marker='d', markersize=4)
    ax4.set_xlabel('Axial Position (m)')
    ax4.set_ylabel('Reaction Rate (mol/m³·s)')
    ax4.set_title('Reaction Rate Profile')
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(0, reactor.L)
    
    plt.tight_layout()
    plt.savefig('fixed_bed_reactor_example_plots.png', dpi=300, bbox_inches='tight')
    print("Plot saved as: fixed_bed_reactor_example_plots.png")
    
    # Create a detailed analysis plot
    fig2, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    # Create secondary axis for temperature
    ax2_temp = ax.twinx()
    
    # Plot concentration and conversion
    line1 = ax.plot(z_positions, CA_profile, 'b-', linewidth=3, label='Concentration', marker='o', markersize=6)
    ax.set_xlabel('Axial Position (m)', fontsize=12)
    ax.set_ylabel('Concentration (mol/m³)', color='b', fontsize=12)
    ax.tick_params(axis='y', labelcolor='b')
    
    # Plot temperature
    line2 = ax2_temp.plot(z_positions, T_profile, 'r-', linewidth=3, label='Temperature', marker='s', markersize=6)
    ax2_temp.set_ylabel('Temperature (K)', color='r', fontsize=12)
    ax2_temp.tick_params(axis='y', labelcolor='r')
    
    # Add grid and formatting
    ax.grid(True, alpha=0.3)
    ax.set_title('Fixed Bed Reactor: Detailed Axial Profiles', fontsize=14, fontweight='bold', pad=20)
    
    # Add text box with key results
    textstr = f'Conversion: {conversion:.1%}\nMax Temp: {np.max(T_profile):.1f} K\nResidence Time: {residence_time:.2f} min'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)
    
    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc='center right')
    
    plt.tight_layout()
    plt.savefig('fixed_bed_reactor_detailed_analysis.png', dpi=300, bbox_inches='tight')
    print("Detailed analysis plot saved as: fixed_bed_reactor_detailed_analysis.png")
    
    plt.close('all')
    
    print("\nExample completed successfully!")


if __name__ == "__main__":
    main()
