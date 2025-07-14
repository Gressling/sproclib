#!/usr/bin/env python3
"""
Generate plot images for ScrewFeeder example
"""

import numpy as np
import matplotlib.pyplot as plt

# Simulate ScrewFeeder behavior
def simulate_screw_feeder():
    # Time points
    time = np.linspace(0, 10, 100)
    
    # Example parameters
    screw_diameter = 0.2  # m
    pitch = 0.15  # m
    rpm = 50  # rotations per minute
    fill_ratio = 0.4  # 40% fill
    
    # Simulate flow rate with startup dynamics
    theoretical_flow = 2.5  # kg/s
    actual_flow = theoretical_flow * 0.8 * (1 - np.exp(-time/2)) * (1 + 0.05*np.sin(time*0.3))
    
    # Simulate power consumption
    power_steady = 5.0  # kW
    power = power_steady * (1 - np.exp(-time/1.5)) * (1 + 0.1*np.sin(time*0.2))
    
    # Simulate torque
    torque_steady = 150  # Nm
    torque = torque_steady * (1 - np.exp(-time/1.5)) * (1 + 0.1*np.sin(time*0.2))
    
    # Simulate efficiency
    efficiency = (actual_flow / theoretical_flow) * 100
    
    return time, actual_flow, power, torque, efficiency

def create_example_plots():
    """Create example plots showing screw feeder behavior"""
    time, flow_rate, power, torque, efficiency = simulate_screw_feeder()
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Screw Feeder System - Example Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Flow Rate vs Time
    ax1.plot(time, flow_rate, 'b-', linewidth=2, label='Actual Flow Rate')
    ax1.axhline(y=2.5*0.8, color='r', linestyle='--', label='Target Flow Rate')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Flow Rate (kg/s)')
    ax1.set_title('Flow Rate Response')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot 2: Power Consumption vs Time
    ax2.plot(time, power, 'g-', linewidth=2, label='Power Consumption')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Power (kW)')
    ax2.set_title('Power Consumption')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Plot 3: Torque vs Time
    ax3.plot(time, torque, 'r-', linewidth=2, label='Torque')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Torque (Nm)')
    ax3.set_title('Drive Torque')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # Plot 4: Efficiency vs Time
    ax4.plot(time, efficiency, 'orange', linewidth=2, label='Volumetric Efficiency')
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Efficiency (%)')
    ax4.set_title('Volumetric Efficiency')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('ScrewFeeder_example_plots.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created ScrewFeeder_example_plots.png")

def create_detailed_analysis():
    """Create detailed analysis plots"""
    # Parameter variations
    rpms = np.linspace(10, 100, 50)  # RPM
    fill_ratios = np.array([0.2, 0.3, 0.4, 0.5])  # Fill ratios
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Screw Feeder System - Detailed Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Flow Rate vs RPM for different fill ratios
    for fill_ratio in fill_ratios:
        # Simplified flow rate correlation
        flow_rate = 0.05 * rpms * fill_ratio * 0.2**2  # kg/s
        ax1.plot(rpms, flow_rate, linewidth=2, 
                label=f'Fill Ratio = {fill_ratio:.1f}')
    ax1.set_xlabel('RPM')
    ax1.set_ylabel('Flow Rate (kg/s)')
    ax1.set_title('Flow Rate vs RPM')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot 2: Power vs RPM
    power_consumption = 0.001 * rpms**2 + 0.05 * rpms + 1  # kW
    ax2.plot(rpms, power_consumption, 'ro-', linewidth=2, markersize=4)
    ax2.set_xlabel('RPM')
    ax2.set_ylabel('Power Consumption (kW)')
    ax2.set_title('Power Consumption vs RPM')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Volumetric Efficiency vs Fill Ratio
    fill_range = np.linspace(0.1, 0.8, 50)
    # Efficiency typically decreases with higher fill ratios due to back-mixing
    efficiency = 95 - 20 * fill_range  # %
    ax3.plot(fill_range, efficiency, 'g-', linewidth=2)
    ax3.set_xlabel('Fill Ratio')
    ax3.set_ylabel('Volumetric Efficiency (%)')
    ax3.set_title('Efficiency vs Fill Ratio')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Operating Envelope - Flow Rate vs Power
    flow_rates = []
    powers = []
    for rpm in rpms:
        for fill_ratio in [0.3, 0.4, 0.5]:
            flow = 0.05 * rpm * fill_ratio * 0.2**2
            power = 0.001 * rpm**2 + 0.05 * rpm + 1
            flow_rates.append(flow)
            powers.append(power)
    
    ax4.scatter(powers, flow_rates, alpha=0.6, s=30)
    ax4.set_xlabel('Power Consumption (kW)')
    ax4.set_ylabel('Flow Rate (kg/s)')
    ax4.set_title('Operating Envelope')
    ax4.grid(True, alpha=0.3)
    
    # Add efficiency contours
    power_grid = np.linspace(min(powers), max(powers), 20)
    flow_grid = np.linspace(min(flow_rates), max(flow_rates), 20)
    P, F = np.meshgrid(power_grid, flow_grid)
    specific_energy = P / (F + 0.01)  # kW/(kg/s) = kJ/kg
    contours = ax4.contour(P, F, specific_energy, levels=5, colors='red', alpha=0.5)
    ax4.clabel(contours, inline=True, fontsize=8, fmt='%.1f kJ/kg')
    
    plt.tight_layout()
    plt.savefig('ScrewFeeder_detailed_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created ScrewFeeder_detailed_analysis.png")

if __name__ == "__main__":
    create_example_plots()
    create_detailed_analysis()
    print("All ScrewFeeder plots generated successfully!")
