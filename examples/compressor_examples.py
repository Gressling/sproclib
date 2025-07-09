"""
Compressor Examples - SPROCLIB
============================

This module contains examples demonstrating the usage of compressor units in SPROCLIB.
Each example includes both simple and comprehensive use cases.

Requirements:
- NumPy
- SciPy
"""

import numpy as np
import sys
import os

# Add the process_control directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unit.compressor.Compressor import Compressor


def simple_compressor_example():
    """
    Simple example of using a Compressor unit.
    
    This example demonstrates basic compressor operation with constant conditions.
    """
    print("=== Simple Compressor Example ===")
    
    # Create a compressor instance
    compressor = Compressor(name="Basic Compressor")
    
    print(f"Compressor created: {compressor.name}")
    print(f"Type: {type(compressor).__name__}")
    
    # Set initial parameters
    inlet_pressure = 1.0  # bar
    outlet_pressure = 5.0  # bar
    flow_rate = 100.0  # kg/h
    efficiency = 0.8
    
    print(f"\nOperating conditions:")
    print(f"Inlet pressure: {inlet_pressure} bar")
    print(f"Outlet pressure: {outlet_pressure} bar")
    print(f"Flow rate: {flow_rate} kg/h")
    print(f"Efficiency: {efficiency}")
    
    # Calculate compression ratio
    compression_ratio = outlet_pressure / inlet_pressure
    print(f"Compression ratio: {compression_ratio:.2f}")
    
    print("\nSimple compressor example completed successfully!")


def comprehensive_compressor_example():
    """
    Comprehensive example demonstrating advanced compressor operations.
    
    This example includes:
    - Multiple operating points
    - Performance curve analysis
    - Efficiency calculations
    - Power consumption estimation
    - Multi-stage compression
    """
    print("\n=== Comprehensive Compressor Example ===")
    
    # Create multiple compressor configurations
    compressors = {
        "Single Stage": Compressor(name="Single Stage Compressor"),
        "High Efficiency": Compressor(name="High Efficiency Compressor"),
        "Variable Speed": Compressor(name="Variable Speed Compressor")
    }
    
    # Define operating conditions matrix
    operating_conditions = [
        {"P_in": 1.0, "P_out": 3.0, "flow": 80.0, "efficiency": 0.75},
        {"P_in": 1.0, "P_out": 5.0, "flow": 100.0, "efficiency": 0.80},
        {"P_in": 1.0, "P_out": 8.0, "flow": 120.0, "efficiency": 0.78},
        {"P_in": 2.0, "P_out": 10.0, "flow": 150.0, "efficiency": 0.82}
    ]
    
    print("Performance Analysis:")
    print("-" * 80)
    print(f"{'Condition':<12} {'P_in (bar)':<12} {'P_out (bar)':<12} {'Flow (kg/h)':<12} {'Ratio':<8} {'Efficiency':<10}")
    print("-" * 80)
    
    for i, conditions in enumerate(operating_conditions):
        ratio = conditions["P_out"] / conditions["P_in"]
        print(f"{'Case ' + str(i+1):<12} {conditions['P_in']:<12.1f} {conditions['P_out']:<12.1f} "
              f"{conditions['flow']:<12.1f} {ratio:<8.2f} {conditions['efficiency']:<10.2f}")
    
    # Simulate multi-stage compression
    print("\n--- Multi-Stage Compression Analysis ---")
    
    # Define a multi-stage compression scenario
    inlet_pressure = 1.0  # bar
    final_pressure = 16.0  # bar
    num_stages = 3
    
    # Calculate optimal pressure ratios for equal work per stage
    total_ratio = final_pressure / inlet_pressure
    stage_ratio = total_ratio ** (1.0 / num_stages)
    
    print(f"Multi-stage compression from {inlet_pressure} to {final_pressure} bar")
    print(f"Number of stages: {num_stages}")
    print(f"Total compression ratio: {total_ratio:.2f}")
    print(f"Optimal stage ratio: {stage_ratio:.2f}")
    
    # Calculate pressure at each stage
    stage_pressures = [inlet_pressure]
    for stage in range(num_stages):
        next_pressure = stage_pressures[-1] * stage_ratio
        stage_pressures.append(next_pressure)
    
    print("\nStage-by-stage pressure progression:")
    for i in range(num_stages):
        stage_num = i + 1
        p_in = stage_pressures[i]
        p_out = stage_pressures[i + 1]
        print(f"Stage {stage_num}: {p_in:.2f} → {p_out:.2f} bar (ratio: {p_out/p_in:.2f})")
    
    # Performance curve simulation
    print("\n--- Performance Curve Analysis ---")
    
    # Generate performance data
    flow_rates = np.linspace(50, 200, 10)
    base_efficiency = 0.80
    
    print(f"{'Flow Rate (kg/h)':<18} {'Efficiency':<12} {'Relative Performance':<20}")
    print("-" * 50)
    
    for flow in flow_rates:
        # Simple efficiency model (decreases at extremes)
        efficiency = base_efficiency * (1 - 0.0001 * (flow - 100)**2)
        efficiency = max(0.6, min(0.85, efficiency))  # Clamp between realistic values
        
        relative_perf = efficiency / base_efficiency
        print(f"{flow:<18.1f} {efficiency:<12.3f} {relative_perf:<20.3f}")
    
    # Energy analysis
    print("\n--- Energy Analysis ---")
    
    # Estimate power consumption for different scenarios
    scenarios = [
        {"name": "Low Load", "flow": 75, "ratio": 3.0, "efficiency": 0.75},
        {"name": "Design Point", "flow": 100, "ratio": 5.0, "efficiency": 0.80},
        {"name": "High Load", "flow": 150, "ratio": 5.0, "efficiency": 0.78}
    ]
    
    print(f"{'Scenario':<15} {'Flow (kg/h)':<12} {'Ratio':<8} {'Efficiency':<10} {'Rel. Power':<12}")
    print("-" * 65)
    
    for scenario in scenarios:
        # Simplified power calculation (relative to design point)
        flow_factor = scenario["flow"] / 100.0
        compression_factor = np.log(scenario["ratio"]) / np.log(5.0)
        efficiency_factor = 0.80 / scenario["efficiency"]
        
        relative_power = flow_factor * compression_factor * efficiency_factor
        
        print(f"{scenario['name']:<15} {scenario['flow']:<12.1f} {scenario['ratio']:<8.1f} "
              f"{scenario['efficiency']:<10.2f} {relative_power:<12.2f}")
    
    print("\nComprehensive compressor example completed successfully!")


def main():
    """
    Main function to run all compressor examples.
    """
    print("SPROCLIB Compressor Examples")
    print("=" * 50)
    
    try:
        # Run simple example
        simple_compressor_example()
        
        # Run comprehensive example
        comprehensive_compressor_example()
        
        print("\n" + "=" * 50)
        print("All compressor examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
