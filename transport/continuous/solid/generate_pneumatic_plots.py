#!/usr/bin/env python3
"""
Generate plot images for PneumaticConveying example
"""

import numpy as np
import matplotlib.pyplot as plt

# Simulate PneumaticConveying behavior
def simulate_pneumatic_conveying():
    # Time points
    time = np.linspace(0, 10, 100)
    
    # Example parameters
    pipe_diameter = 0.15  # m
    pipe_length = 50  # m
    air_velocity = 25  # m/s
    particle_density = 1500  # kg/m³
    particle_size = 0.002  # m
    
    # Simulate pressure drop over time with startup dynamics
    pressure_drop_steady = 2500  # Pa
    pressure_drop = pressure_drop_steady * (1 - np.exp(-time/2))
    
    # Simulate flow rate with some variation
    flow_rate_steady = 5.0  # kg/s
    flow_rate = flow_rate_steady * (1 - np.exp(-time/1.5)) * (1 + 0.1*np.sin(time*0.5))
    
    # Simulate air velocity with control response
    air_velocity_response = air_velocity * (1 - np.exp(-time/1.8))
    
    # Simulate particle velocity (typically 70-80% of air velocity)
    particle_velocity = 0.75 * air_velocity_response
    
    return time, pressure_drop, flow_rate, air_velocity_response, particle_velocity

def create_example_plots():
    """Create example plots showing pneumatic conveying behavior"""
    time, pressure_drop, flow_rate, air_velocity, particle_velocity = simulate_pneumatic_conveying()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Pneumatic Conveying System - Example Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Pressure Drop vs Time
    ax1.plot(time, pressure_drop/1000, 'b-', linewidth=2, label='Pressure Drop')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Pressure Drop (kPa)')
    ax1.set_title('Pressure Drop Response')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot 2: Flow Rate vs Time
    ax2.plot(time, flow_rate, 'g-', linewidth=2, label='Solid Flow Rate')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Flow Rate (kg/s)')
    ax2.set_title('Solid Flow Rate Response')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Plot 3: Velocities vs Time
    ax3.plot(time, air_velocity, 'r-', linewidth=2, label='Air Velocity')
    ax3.plot(time, particle_velocity, 'orange', linewidth=2, label='Particle Velocity')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Velocity (m/s)')
    ax3.set_title('Air and Particle Velocities')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # Plot 4: Phase Diagram - Flow Rate vs Air Velocity
    ax4.scatter(air_velocity[::5], flow_rate[::5], c=time[::5], cmap='viridis', s=30)
    ax4.set_xlabel('Air Velocity (m/s)')
    ax4.set_ylabel('Flow Rate (kg/s)')
    ax4.set_title('Operating Envelope')
    ax4.grid(True, alpha=0.3)
    cbar = plt.colorbar(ax4.scatter(air_velocity[::5], flow_rate[::5], c=time[::5], cmap='viridis', s=30), ax=ax4)
    cbar.set_label('Time (s)')
    
    plt.tight_layout()
    plt.savefig('PneumaticConveying_example_plots.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created PneumaticConveying_example_plots.png")

def create_detailed_analysis():
    """Create detailed analysis plots"""
    # Parameter variations
    pipe_diameters = np.array([0.10, 0.15, 0.20, 0.25])  # m
    air_velocities = np.linspace(15, 35, 50)  # m/s
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Pneumatic Conveying System - Detailed Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Pressure Drop vs Air Velocity for different pipe diameters
    for diameter in pipe_diameters:
        # Simplified pressure drop correlation
        pressure_drop = 0.5 * 1.2 * air_velocities**2 * (50/diameter) * 0.02  # Pa
        ax1.plot(air_velocities, pressure_drop/1000, linewidth=2, 
                label=f'D = {diameter:.2f} m')
    ax1.set_xlabel('Air Velocity (m/s)')
    ax1.set_ylabel('Pressure Drop (kPa)')
    ax1.set_title('Pressure Drop vs Air Velocity')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot 2: Minimum Transport Velocity
    particle_sizes = np.array([0.001, 0.002, 0.005, 0.010])  # m
    min_velocities = []
    for size in particle_sizes:
        # Simplified minimum velocity correlation
        v_min = 10 * np.sqrt(size * 1000)  # m/s
        min_velocities.append(v_min)
    
    ax2.plot(particle_sizes*1000, min_velocities, 'ro-', linewidth=2, markersize=6)
    ax2.set_xlabel('Particle Size (mm)')
    ax2.set_ylabel('Minimum Transport Velocity (m/s)')
    ax2.set_title('Minimum Transport Velocity')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Conveying Capacity vs Air Velocity
    flow_rates = []
    for vel in air_velocities:
        # Simplified capacity correlation
        if vel > 18:  # Above minimum transport velocity
            flow_rate = 0.3 * (vel - 18) * 0.15**2  # kg/s
            flow_rates.append(max(0, flow_rate))
        else:
            flow_rates.append(0)
    
    ax3.plot(air_velocities, flow_rates, 'g-', linewidth=2)
    ax3.axvline(x=18, color='r', linestyle='--', label='Min Transport Velocity')
    ax3.set_xlabel('Air Velocity (m/s)')
    ax3.set_ylabel('Conveying Capacity (kg/s)')
    ax3.set_title('Conveying Capacity')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # Plot 4: Operating Regions
    velocity_range = np.linspace(10, 40, 100)
    dilute_phase = velocity_range > 18
    dense_phase = (velocity_range <= 18) & (velocity_range > 5)
    no_transport = velocity_range <= 5
    
    ax4.fill_between(velocity_range, 0, 1, where=dilute_phase, 
                     alpha=0.3, color='green', label='Dilute Phase')
    ax4.fill_between(velocity_range, 0, 1, where=dense_phase, 
                     alpha=0.3, color='orange', label='Dense Phase')
    ax4.fill_between(velocity_range, 0, 1, where=no_transport, 
                     alpha=0.3, color='red', label='No Transport')
    ax4.set_xlabel('Air Velocity (m/s)')
    ax4.set_ylabel('Relative Region')
    ax4.set_title('Operating Regions')
    ax4.set_ylim(0, 1)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('PneumaticConveying_detailed_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created PneumaticConveying_detailed_analysis.png")

if __name__ == "__main__":
    create_example_plots()
    create_detailed_analysis()
    print("All PneumaticConveying plots generated successfully!")
