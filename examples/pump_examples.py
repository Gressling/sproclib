#!/usr/bin/env python3
"""
Pump Examples for SPROCLIB

This module demonstrates simple and comprehensive usage of pump models
including basic pump, centrifugal pump, and positive displacement pump.

Author: SPROCLIB Development Team
License: MIT License
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the parent directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from unit.pump.base import Pump
from unit.pump.centrifugal import CentrifugalPump
from unit.pump.positive_displacement import PositiveDisplacementPump


def simple_pump_example():
    """Simple example: Basic pump steady-state calculation."""
    
    print("=== Simple Pump Example ===")
    
    # Create a basic pump
    pump = Pump(
        eta=0.75,                    # 75% efficiency
        rho=1000.0,                  # Water density [kg/m³]
        flow_nominal=0.01,           # 10 L/s nominal flow
        delta_P_nominal=200000.0,    # 2 bar pressure rise
        name="SimpleWaterPump"
    )
    
    # Define operating conditions
    P_inlet = 101325.0  # Atmospheric pressure [Pa]
    flow_rate = 0.008   # 8 L/s actual flow [m³/s]
    
    # Calculate steady-state output
    u = np.array([P_inlet, flow_rate])
    result = pump.steady_state(u)
    
    P_outlet = result[0]
    power_required = result[1]
    
    print(f"Pump: {pump.name}")
    print(f"Inlet pressure: {P_inlet/1000:.1f} kPa")
    print(f"Flow rate: {flow_rate*1000:.1f} L/s")
    print(f"Outlet pressure: {P_outlet/1000:.1f} kPa")
    print(f"Pressure rise: {(P_outlet-P_inlet)/1000:.1f} kPa")
    print(f"Power required: {power_required/1000:.2f} kW")
    print(f"Efficiency: {pump.eta*100:.1f}%")
    print()


def comprehensive_pump_example():
    """Comprehensive example: Compare different pump types and dynamic simulation."""
    
    print("=== Comprehensive Pump Comparison Example ===")
    
    # Create different pump types
    basic_pump = Pump(eta=0.70, rho=1000.0, name="BasicPump")
    
    centrifugal_pump = CentrifugalPump(
        H0=50.0,                     # 50 m shutoff head
        K=20.0,                      # Head-flow coefficient
        eta=0.75,
        rho=1000.0,
        name="CentrifugalPump"
    )
    
    pd_pump = PositiveDisplacementPump(
        flow_rate=0.01,              # Constant 10 L/s
        eta=0.80,
        rho=1000.0,
        name="PositiveDisplacementPump"
    )
    
    pumps = [basic_pump, centrifugal_pump, pd_pump]
    
    # Test conditions
    P_inlet = 101325.0  # [Pa]
    flow_rates = np.linspace(0.005, 0.020, 10)  # 5-20 L/s [m³/s]
    
    print("Flow Rate [L/s] | Basic Pump [kW] | Centrifugal [kW] | PD Pump [kW]")
    print("-" * 65)
    
    results = {'flow': flow_rates * 1000}  # Convert to L/s for plotting
    
    for pump in pumps:
        powers = []
        
        for flow in flow_rates:
            if isinstance(pump, PositiveDisplacementPump):
                # PD pump takes only inlet pressure
                u = np.array([P_inlet])
            else:
                # Other pumps take [P_inlet, flow]
                u = np.array([P_inlet, flow])
            
            try:
                result = pump.steady_state(u)
                power = result[1] / 1000  # Convert to kW
                powers.append(power)
            except:
                powers.append(np.nan)
        
        results[pump.name] = powers
    
    # Print results table
    for i, flow in enumerate(flow_rates):
        basic_power = results['BasicPump'][i]
        centrifugal_power = results['CentrifugalPump'][i]
        pd_power = results['PositiveDisplacementPump'][i]
        
        print(f"{flow*1000:11.1f} | {basic_power:11.2f} | {centrifugal_power:12.2f} | {pd_power:9.2f}")
    
    # Create performance comparison plot
    plt.figure(figsize=(12, 8))
    
    # Plot 1: Power vs Flow Rate
    plt.subplot(2, 2, 1)
    plt.plot(results['flow'], results['BasicPump'], 'b-o', label='Basic Pump')
    plt.plot(results['flow'], results['CentrifugalPump'], 'r-s', label='Centrifugal Pump')
    plt.plot(results['flow'], results['PositiveDisplacementPump'], 'g-^', label='PD Pump')
    plt.xlabel('Flow Rate [L/s]')
    plt.ylabel('Power [kW]')
    plt.title('Power Consumption vs Flow Rate')
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Centrifugal pump characteristic curve
    plt.subplot(2, 2, 2)
    flows_detailed = np.linspace(0, 0.025, 50)
    heads = []
    powers_detailed = []
    
    for flow in flows_detailed:
        head = max(0, centrifugal_pump.H0 - centrifugal_pump.K * flow**2)
        heads.append(head)
        
        if flow > 0:
            delta_P = centrifugal_pump.rho * 9.81 * head
            power = flow * delta_P / centrifugal_pump.eta / 1000  # kW
            powers_detailed.append(power)
        else:
            powers_detailed.append(0)
    
    plt.plot(flows_detailed * 1000, heads, 'r-', linewidth=2)
    plt.xlabel('Flow Rate [L/s]')
    plt.ylabel('Head [m]')
    plt.title('Centrifugal Pump Head Curve')
    plt.grid(True)
    
    # Plot 3: Efficiency comparison
    plt.subplot(2, 2, 3)
    efficiencies = [pump.eta * 100 for pump in pumps]
    pump_names = [pump.name.replace('Pump', '') for pump in pumps]
    
    bars = plt.bar(pump_names, efficiencies, color=['blue', 'red', 'green'], alpha=0.7)
    plt.ylabel('Efficiency [%]')
    plt.title('Pump Efficiency Comparison')
    plt.ylim(0, 100)
    
    # Add value labels on bars
    for bar, eff in zip(bars, efficiencies):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{eff:.1f}%', ha='center', va='bottom')
    
    # Plot 4: Dynamic simulation of pump startup
    plt.subplot(2, 2, 4)
    
    # Simulate pump startup with first-order dynamics
    t_sim = np.linspace(0, 10, 100)  # 10 seconds
    target_pressure = basic_pump.delta_P_nominal
    
    # Simple first-order response: P(t) = P_target * (1 - exp(-t/tau))
    tau = 2.0  # Time constant [s]
    pressure_response = target_pressure * (1 - np.exp(-t_sim / tau))
    
    plt.plot(t_sim, pressure_response / 1000, 'b-', linewidth=2, label='Pressure Response')
    plt.axhline(y=target_pressure/1000, color='r', linestyle='--', alpha=0.7, label='Target Pressure')
    plt.xlabel('Time [s]')
    plt.ylabel('Pressure Rise [kPa]')
    plt.title('Pump Startup Dynamics')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(current_dir, 'pump_examples.png'), dpi=150, bbox_inches='tight')
    print(f"\nPlot saved as: {os.path.join(current_dir, 'pump_examples.png')}")
    
    # Show pump information
    print("\n=== Pump Specifications ===")
    for pump in pumps:
        info = pump.get_info()
        print(f"{info['name']}:")
        print(f"  Type: {info['type']}")
        print(f"  Parameters: {len(info['parameters'])} defined")
        for key, value in pump.parameters.items():
            if isinstance(value, float):
                print(f"    {key}: {value:.3f}")
            else:
                print(f"    {key}: {value}")
        print()


def main():
    """Run all pump examples."""
    
    print("SPROCLIB Pump Examples")
    print("=" * 50)
    print()
    
    # Run examples
    simple_pump_example()
    comprehensive_pump_example()
    
    print("Examples completed successfully!")
    print("\nTry modifying the parameters in the code to see how")
    print("different pump configurations affect performance.")


if __name__ == "__main__":
    main()
