"""
Valve Examples - SPROCLIB
=========================

This module contains examples demonstrating the usage of valve units in SPROCLIB.
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

from unit.valve.ControlValve import ControlValve
from unit.valve.ThreeWayValve import ThreeWayValve


def simple_valve_examples():
    """
    Simple examples of using valve units.
    
    This example demonstrates basic valve operations with constant conditions.
    """
    print("=== Simple Valve Examples ===")
    
    # Control Valve Example
    print("\n--- Control Valve ---")
    control_valve = ControlValve(name="Basic Control Valve")
    
    print(f"Control valve created: {control_valve.name}")
    print(f"Type: {type(control_valve).__name__}")
    
    # Set valve parameters
    valve_opening = 50.0  # % open
    inlet_pressure = 10.0  # bar
    outlet_pressure = 5.0  # bar
    
    print(f"\nOperating conditions:")
    print(f"Valve opening: {valve_opening}%")
    print(f"Inlet pressure: {inlet_pressure} bar")
    print(f"Outlet pressure: {outlet_pressure} bar")
    print(f"Pressure drop: {inlet_pressure - outlet_pressure} bar")
    
    # Three-Way Valve Example
    print("\n--- Three-Way Valve ---")
    three_way_valve = ThreeWayValve(name="Basic Three-Way Valve")
    
    print(f"Three-way valve created: {three_way_valve.name}")
    print(f"Type: {type(three_way_valve).__name__}")
    
    # Set valve parameters
    split_ratio = 0.7  # 70% to outlet A, 30% to outlet B
    inlet_flow = 100.0  # kg/h
    
    print(f"\nOperating conditions:")
    print(f"Inlet flow: {inlet_flow} kg/h")
    print(f"Split ratio (A:B): {split_ratio:.1f}:{1-split_ratio:.1f}")
    print(f"Flow to outlet A: {inlet_flow * split_ratio:.1f} kg/h")
    print(f"Flow to outlet B: {inlet_flow * (1-split_ratio):.1f} kg/h")
    
    print("\nSimple valve examples completed successfully!")


def comprehensive_valve_examples():
    """
    Comprehensive examples demonstrating advanced valve operations.
    
    This example includes:
    - Control valve characteristics
    - Flow coefficient (Cv) calculations
    - Three-way valve splitting scenarios
    - Valve sizing and selection
    - Dynamic response simulation
    """
    print("\n=== Comprehensive Valve Examples ===")
    
    # Control Valve Characteristics Analysis
    print("\n--- Control Valve Characteristics ---")
    
    control_valve = ControlValve(name="Precision Control Valve")
    
    # Simulate different valve characteristics
    valve_positions = np.linspace(0, 100, 11)  # 0 to 100% open
    
    print("Valve Characteristic Curves:")
    print("-" * 60)
    print(f"{'Position (%)':<12} {'Linear':<10} {'Equal %':<10} {'Quick Open':<12} {'Butterfly':<12}")
    print("-" * 60)
    
    for position in valve_positions:
        # Different valve characteristics
        linear_flow = position / 100.0
        equal_percent = (position / 100.0) ** 0.5 if position > 0 else 0
        quick_open = 1.0 - np.exp(-3 * position / 100.0) if position > 0 else 0
        butterfly = np.sin(np.pi * position / 200.0) if position > 0 else 0
        
        print(f"{position:<12.0f} {linear_flow:<10.3f} {equal_percent:<10.3f} "
              f"{quick_open:<12.3f} {butterfly:<12.3f}")
    
    # Flow Coefficient (Cv) Analysis
    print("\n--- Flow Coefficient (Cv) Analysis ---")
    
    # Test conditions for Cv calculation
    test_conditions = [
        {"P1": 10.0, "P2": 8.0, "flow": 50.0, "SG": 1.0},  # Water
        {"P1": 15.0, "P2": 10.0, "flow": 75.0, "SG": 0.8},  # Light oil
        {"P1": 5.0, "P2": 2.0, "flow": 100.0, "SG": 1.2},   # Heavy liquid
    ]
    
    print(f"{'Test':<6} {'P1 (bar)':<10} {'P2 (bar)':<10} {'Flow (GPM)':<12} {'SG':<6} {'Cv Required':<12}")
    print("-" * 70)
    
    for i, conditions in enumerate(test_conditions):
        # Simplified Cv calculation: Cv = Q * sqrt(SG / ΔP)
        delta_p = conditions["P1"] - conditions["P2"]
        cv_required = conditions["flow"] * np.sqrt(conditions["SG"] / delta_p)
        
        print(f"{i+1:<6} {conditions['P1']:<10.1f} {conditions['P2']:<10.1f} "
              f"{conditions['flow']:<12.1f} {conditions['SG']:<6.1f} {cv_required:<12.2f}")
    
    # Three-Way Valve Splitting Analysis
    print("\n--- Three-Way Valve Splitting Analysis ---")
    
    three_way_valve = ThreeWayValve(name="Process Splitting Valve")
    
    # Simulate different splitting scenarios
    total_flow = 200.0  # kg/h
    split_ratios = np.linspace(0.1, 0.9, 9)
    
    print("Flow Splitting Scenarios:")
    print("-" * 65)
    print(f"{'Split Ratio':<12} {'Flow A (kg/h)':<15} {'Flow B (kg/h)':<15} {'Pressure Drop A':<15}")
    print("-" * 65)
    
    for ratio in split_ratios:
        flow_a = total_flow * ratio
        flow_b = total_flow * (1 - ratio)
        
        # Simplified pressure drop calculation (higher flow = higher drop)
        pressure_drop_a = 0.5 * (flow_a / 100.0) ** 2  # bar
        
        print(f"{ratio:<12.2f} {flow_a:<15.1f} {flow_b:<15.1f} {pressure_drop_a:<15.3f}")
    
    # Valve Sizing Example
    print("\n--- Valve Sizing Example ---")
    
    sizing_scenarios = [
        {"name": "Small Process", "max_flow": 50, "max_dp": 2.0, "fluid": "Water"},
        {"name": "Medium Process", "max_flow": 150, "max_dp": 5.0, "fluid": "Oil"},
        {"name": "Large Process", "max_flow": 500, "max_dp": 10.0, "fluid": "Steam"},
    ]
    
    print(f"{'Scenario':<15} {'Max Flow':<10} {'Max ΔP':<10} {'Fluid':<8} {'Min Cv':<10} {'Recommended':<12}")
    print("-" * 75)
    
    for scenario in sizing_scenarios:
        # Simplified sizing calculation
        if scenario["fluid"] == "Water":
            sg = 1.0
        elif scenario["fluid"] == "Oil":
            sg = 0.8
        else:  # Steam
            sg = 0.6
        
        min_cv = scenario["max_flow"] * np.sqrt(sg / scenario["max_dp"])
        recommended_cv = min_cv * 1.2  # 20% safety factor
        
        print(f"{scenario['name']:<15} {scenario['max_flow']:<10} {scenario['max_dp']:<10.1f} "
              f"{scenario['fluid']:<8} {min_cv:<10.2f} {recommended_cv:<12.2f}")
    
    # Dynamic Response Simulation
    print("\n--- Dynamic Response Simulation ---")
    
    # Simulate valve response to step input
    time_points = np.linspace(0, 10, 21)  # 0 to 10 seconds
    time_constant = 2.0  # seconds
    
    print("Step Response (0% to 75% opening):")
    print("-" * 40)
    print(f"{'Time (s)':<10} {'Opening (%)':<12} {'Flow (%)':<10}")
    print("-" * 40)
    
    for t in time_points:
        if t == 0:
            opening = 0.0
            flow = 0.0
        else:
            # First-order response
            opening = 75.0 * (1 - np.exp(-t / time_constant))
            flow = opening  # Assuming linear characteristic
        
        print(f"{t:<10.1f} {opening:<12.1f} {flow:<10.1f}")
    
    print("\nComprehensive valve examples completed successfully!")


def main():
    """
    Main function to run all valve examples.
    """
    print("SPROCLIB Valve Examples")
    print("=" * 50)
    
    try:
        # Run simple examples
        simple_valve_examples()
        
        # Run comprehensive examples
        comprehensive_valve_examples()
        
        print("\n" + "=" * 50)
        print("All valve examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
