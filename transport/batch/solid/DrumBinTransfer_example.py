"""
Example file for DrumBinTransfer class

This example demonstrates the use of the DrumBinTransfer model for batch solid
material transfer operations using drums or bins with conveyor discharge.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from transport.batch.solid.DrumBinTransfer import DrumBinTransfer


def main():
    """Main function demonstrating DrumBinTransfer operations."""
    
    print("=== DrumBinTransfer Example ===")
    print()
    
    # Create DrumBinTransfer instances for different scenarios
    print("1. Creating DrumBinTransfer instances:")
    print("-" * 40)
    
    # Standard pharmaceutical transfer
    pharma_transfer = DrumBinTransfer(
        container_capacity=0.3,      # 300 L container
        transfer_rate_max=80.0,      # 80 kg/min max rate
        material_density=600.0,      # Pharmaceutical powder density
        discharge_efficiency=0.9,    # Good discharge efficiency
        handling_time=90.0,          # 1.5 min handling time
        conveyor_speed=0.4,          # 0.4 m/s conveyor speed
        transfer_distance=8.0,       # 8 m transfer distance
        name="PharmaPowderTransfer"
    )
    
    # High-capacity food ingredient transfer
    food_transfer = DrumBinTransfer(
        container_capacity=1.5,      # 1500 L container
        transfer_rate_max=300.0,     # 300 kg/min max rate
        material_density=800.0,      # Food ingredient density
        discharge_efficiency=0.95,   # Excellent discharge efficiency
        handling_time=150.0,         # 2.5 min handling time
        conveyor_speed=0.6,          # 0.6 m/s conveyor speed
        transfer_distance=15.0,      # 15 m transfer distance
        name="FoodIngredientTransfer"
    )
    
    print(f"Pharmaceutical transfer: {pharma_transfer.name}")
    print(f"  Container capacity: {pharma_transfer.container_capacity} m³")
    print(f"  Max transfer rate: {pharma_transfer.transfer_rate_max} kg/min")
    print()
    
    print(f"Food ingredient transfer: {food_transfer.name}")
    print(f"  Container capacity: {food_transfer.container_capacity} m³")
    print(f"  Max transfer rate: {food_transfer.transfer_rate_max} kg/min")
    print()
    
    # 2. Steady-state analysis
    print("2. Steady-state analysis:")
    print("-" * 25)
    
    # Test different operating conditions
    conditions = [
        {"name": "Full container, good flow", "fill": 1.0, "setpoint": 60.0, "flowability": 0.9},
        {"name": "Half full, moderate flow", "fill": 0.5, "setpoint": 60.0, "flowability": 0.6},
        {"name": "Low level, poor flow", "fill": 0.1, "setpoint": 60.0, "flowability": 0.3},
        {"name": "High setpoint, excellent flow", "fill": 0.8, "setpoint": 120.0, "flowability": 1.0}
    ]
    
    print("Pharmaceutical transfer results:")
    for condition in conditions:
        u = np.array([condition["fill"], condition["setpoint"], condition["flowability"]])
        result = pharma_transfer.steady_state(u)
        transfer_rate, batch_time = result
        
        print(f"  {condition['name']}:")
        print(f"    Transfer rate: {transfer_rate:.1f} kg/min")
        print(f"    Batch time: {batch_time:.1f} s")
        print()
    
    # 3. Dynamic simulation
    print("3. Dynamic simulation:")
    print("-" * 20)
    
    # Simulate a complete batch transfer
    time_span = np.linspace(0, 600, 301)  # 10 minutes
    dt = time_span[1] - time_span[0]
    
    # Initial conditions
    x = np.array([0.0, 1.0])  # [transfer_rate=0, fill_level=1.0]
    u = np.array([1.0, 70.0, 0.8])  # [target_fill, setpoint, flowability]
    
    # Storage for results
    transfer_rates = []
    fill_levels = []
    times = []
    
    print("Simulating batch transfer with pharma_transfer:")
    print(f"Initial conditions: rate=0 kg/min, fill=100%")
    print(f"Setpoint: {u[1]} kg/min, flowability: {u[2]}")
    print()
    
    # Euler integration
    for t in time_span:
        # Store current state
        transfer_rates.append(x[0])
        fill_levels.append(x[1])
        times.append(t)
        
        # Calculate derivatives
        if x[1] > 0:  # Continue only if material remains
            dx_dt = pharma_transfer.dynamics(t, x, u)
            # Update state
            x = x + dx_dt * dt
            x[1] = max(0.0, x[1])  # Prevent negative fill level
        else:
            break
    
    # Convert to numpy arrays
    transfer_rates = np.array(transfer_rates)
    fill_levels = np.array(fill_levels)
    times = np.array(times)
    
    # Print key results
    print("Dynamic simulation results:")
    print(f"  Final time: {times[-1]:.1f} s")
    print(f"  Final fill level: {fill_levels[-1]:.3f}")
    print(f"  Average transfer rate: {np.mean(transfer_rates[50:]):.1f} kg/min")
    print()
    
    # 4. Flowability sensitivity analysis
    print("4. Flowability sensitivity analysis:")
    print("-" * 35)
    
    flowability_range = np.linspace(0.1, 1.0, 10)
    steady_rates = []
    
    for flowability in flowability_range:
        u_test = np.array([0.8, 80.0, flowability])
        result = food_transfer.steady_state(u_test)
        steady_rates.append(result[0])
    
    steady_rates = np.array(steady_rates)
    
    print("Food transfer flowability sensitivity (80% fill, 80 kg/min setpoint):")
    for i, (flow, rate) in enumerate(zip(flowability_range, steady_rates)):
        print(f"  Flowability {flow:.1f}: {rate:.1f} kg/min")
    
    print()
    
    # 5. Model introspection
    print("5. Model introspection:")
    print("-" * 20)
    
    metadata = pharma_transfer.describe()
    print(f"Model type: {metadata['model_type']}")
    print(f"Description: {metadata['description']}")
    print()
    print("Key parameters:")
    for param, info in metadata['parameters'].items():
        print(f"  {param}: {info['value']} {info['unit']} - {info['description']}")
    print()
    
    print("Operating ranges:")
    for param, range_vals in metadata['operating_ranges'].items():
        print(f"  {param}: {range_vals[0]} - {range_vals[1]}")
    print()
    
    # 6. Create visualization plots
    print("6. Creating visualization plots...")
    create_plots(times, transfer_rates, fill_levels, flowability_range, steady_rates, pharma_transfer, food_transfer)
    print("Plots saved as DrumBinTransfer_example_plots.png and DrumBinTransfer_detailed_analysis.png")
    print()
    
    print("=== Example completed successfully ===")


def create_plots(times, transfer_rates, fill_levels, flowability_range, steady_rates, pharma_transfer, food_transfer):
    """Create visualization plots for the DrumBinTransfer example."""
    
    # Plot 1: Dynamic simulation results
    fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Transfer rate vs time
    ax1.plot(times/60, transfer_rates, 'b-', linewidth=2, label='Transfer Rate')
    ax1.set_xlabel('Time (min)')
    ax1.set_ylabel('Transfer Rate (kg/min)')
    ax1.set_title('DrumBinTransfer Dynamic Response')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Fill level vs time
    ax2.plot(times/60, fill_levels*100, 'r-', linewidth=2, label='Fill Level')
    ax2.set_xlabel('Time (min)')
    ax2.set_ylabel('Fill Level (%)')
    ax2.set_title('Container Fill Level During Transfer')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('DrumBinTransfer_example_plots.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 2: Detailed analysis
    fig2, ((ax3, ax4), (ax5, ax6)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Flowability sensitivity
    ax3.plot(flowability_range, steady_rates, 'go-', linewidth=2, markersize=6)
    ax3.set_xlabel('Flowability Index (-)')
    ax3.set_ylabel('Transfer Rate (kg/min)')
    ax3.set_title('Flowability Effect on Transfer Rate')
    ax3.grid(True, alpha=0.3)
    
    # Fill level effect on transfer rate
    fill_levels_test = np.linspace(0.05, 1.0, 20)
    rates_vs_fill = []
    for fill in fill_levels_test:
        u_test = np.array([fill, 80.0, 0.8])
        result = pharma_transfer.steady_state(u_test)
        rates_vs_fill.append(result[0])
    
    ax4.plot(fill_levels_test*100, rates_vs_fill, 'mo-', linewidth=2, markersize=4)
    ax4.set_xlabel('Fill Level (%)')
    ax4.set_ylabel('Transfer Rate (kg/min)')
    ax4.set_title('Fill Level Effect (80 kg/min setpoint)')
    ax4.grid(True, alpha=0.3)
    
    # Setpoint vs actual rate comparison
    setpoints = np.linspace(20, 150, 15)
    actual_rates_pharma = []
    actual_rates_food = []
    
    for setpoint in setpoints:
        u_test = np.array([0.8, setpoint, 0.8])
        result_pharma = pharma_transfer.steady_state(u_test)
        result_food = food_transfer.steady_state(u_test)
        actual_rates_pharma.append(result_pharma[0])
        actual_rates_food.append(result_food[0])
    
    ax5.plot(setpoints, setpoints, 'k--', alpha=0.5, label='Ideal (setpoint)')
    ax5.plot(setpoints, actual_rates_pharma, 'b-o', markersize=4, label='Pharma transfer')
    ax5.plot(setpoints, actual_rates_food, 'r-s', markersize=4, label='Food transfer')
    ax5.set_xlabel('Setpoint (kg/min)')
    ax5.set_ylabel('Actual Rate (kg/min)')
    ax5.set_title('Setpoint vs Actual Rate')
    ax5.grid(True, alpha=0.3)
    ax5.legend()
    
    # Batch time vs fill level
    batch_times = []
    for fill in fill_levels_test:
        u_test = np.array([fill, 80.0, 0.8])
        result = pharma_transfer.steady_state(u_test)
        batch_times.append(result[1]/60)  # Convert to minutes
    
    ax6.plot(fill_levels_test*100, batch_times, 'co-', linewidth=2, markersize=4)
    ax6.set_xlabel('Fill Level (%)')
    ax6.set_ylabel('Batch Time (min)')
    ax6.set_title('Batch Completion Time')
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('DrumBinTransfer_detailed_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    main()
