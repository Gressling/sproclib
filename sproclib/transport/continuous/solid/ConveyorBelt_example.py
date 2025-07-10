"""
Example usage of ConveyorBelt class.

This script demonstrates the ConveyorBelt transport model with various
operating conditions and visualizations.
"""

import numpy as np
import matplotlib.pyplot as plt
from ConveyorBelt import ConveyorBelt

def main():
    print("=" * 60)
    print("ConveyorBelt Transport Model Example")
    print("=" * 60)
    
    # Create conveyor belt instance
    conveyor = ConveyorBelt(
        belt_length=100.0,      # 100 m belt
        belt_width=1.5,         # 1.5 m wide
        belt_speed=2.0,         # 2 m/s
        belt_angle=0.1,         # ~5.7 degrees
        material_density=1800.0, # Coal density
        friction_coefficient=0.6,
        belt_load_factor=0.8,
        motor_power=25000.0,    # 25 kW motor
        name="CoalConveyor"
    )
    
    print("\nConveyor Belt Parameters:")
    print(f"Length: {conveyor.belt_length} m")
    print(f"Width: {conveyor.belt_width} m")
    print(f"Speed: {conveyor.belt_speed} m/s")
    print(f"Angle: {conveyor.belt_angle:.3f} rad ({np.degrees(conveyor.belt_angle):.1f}°)")
    print(f"Material density: {conveyor.material_density} kg/m³")
    print(f"Motor power: {conveyor.motor_power/1000:.1f} kW")
    
    # Display model description
    description = conveyor.describe()
    print(f"\nModel: {description['class_name']}")
    print(f"Algorithm: {description['algorithm']}")
    
    # Test different operating conditions
    print("\n" + "=" * 50)
    print("Steady-State Performance Analysis")
    print("=" * 50)
    
    # Operating conditions: [feed_rate, belt_speed, material_load_height]
    test_conditions = [
        ([10.0, 2.0, 0.05], "Normal operation"),
        ([25.0, 2.0, 0.08], "High load"),
        ([5.0, 1.0, 0.03], "Low speed operation"),
        ([30.0, 3.0, 0.1], "Maximum throughput"),
        ([15.0, 2.5, 0.0], "Empty belt"),
    ]
    
    results = []
    for conditions, description in test_conditions:
        u = np.array(conditions)
        result = conveyor.steady_state(u)
        results.append((conditions, result, description))
        
        print(f"\n{description}:")
        print(f"  Input: Feed={u[0]:.1f} kg/s, Speed={u[1]:.1f} m/s, Height={u[2]:.3f} m")
        print(f"  Output: Flow={result[0]:.2f} kg/s, Power={result[1]/1000:.1f} kW")
        print(f"  Efficiency: {result[0]/max(u[0], 0.1)*100:.1f}%")
    
    # Belt speed sensitivity analysis
    print("\n" + "=" * 50)
    print("Belt Speed Sensitivity Analysis")
    print("=" * 50)
    
    speeds = np.linspace(0.5, 4.0, 20)
    flow_rates = []
    power_consumption = []
    
    for speed in speeds:
        u = np.array([20.0, speed, 0.06])  # 20 kg/s feed, varying speed
        result = conveyor.steady_state(u)
        flow_rates.append(result[0])
        power_consumption.append(result[1])
    
    # Find optimal speed (maximum efficiency)
    efficiencies = np.array(flow_rates) / 20.0  # Feed rate is 20 kg/s
    optimal_idx = np.argmax(efficiencies)
    optimal_speed = speeds[optimal_idx]
    
    print(f"Optimal belt speed: {optimal_speed:.2f} m/s")
    print(f"Maximum efficiency: {efficiencies[optimal_idx]*100:.1f}%")
    print(f"Power at optimal speed: {power_consumption[optimal_idx]/1000:.1f} kW")
    
    # Dynamic response analysis
    print("\n" + "=" * 50)
    print("Dynamic Response Analysis")
    print("=" * 50)
    
    # Simulate step change in feed rate
    dt = 0.5  # time step (s)
    t_final = 300.0  # simulation time (s)
    time = np.arange(0, t_final, dt)
    
    # Initial conditions: [flow_rate, power]
    x = np.array([5.0, 8000.0])
    
    # Step change at t=60s: from 10 to 20 kg/s feed rate
    feed_rates = np.where(time < 60, 10.0, 20.0)
    
    flow_history = []
    power_history = []
    
    for i, t in enumerate(time):
        u = np.array([feed_rates[i], 2.0, 0.06])
        
        # Store current state
        flow_history.append(x[0])
        power_history.append(x[1])
        
        # Calculate derivatives
        dxdt = conveyor.dynamics(t, x, u)
        
        # Euler integration
        x = x + dxdt * dt
    
    print(f"Initial flow rate: {flow_history[0]:.2f} kg/s")
    print(f"Final flow rate: {flow_history[-1]:.2f} kg/s")
    print(f"Settling time: ~{(t_final - 60)/3:.0f} s")
    
    # Material properties effect
    print("\n" + "=" * 50)
    print("Material Properties Effect")
    print("=" * 50)
    
    materials = [
        (500, "Grain"),
        (1200, "Sand"), 
        (1800, "Coal"),
        (2500, "Ore"),
        (3200, "Iron ore")
    ]
    
    material_results = []
    for density, name in materials:
        test_conveyor = ConveyorBelt(
            belt_length=100.0,
            belt_width=1.5,
            material_density=density,
            motor_power=25000.0
        )
        
        u = np.array([15.0, 2.0, 0.06])
        result = test_conveyor.steady_state(u)
        material_results.append((name, density, result))
        
        print(f"{name:10s}: Density={density:4d} kg/m³, "
              f"Flow={result[0]:5.1f} kg/s, Power={result[1]/1000:5.1f} kW")
    
    # Power limitation analysis
    print("\n" + "=" * 50)
    print("Power Limitation Analysis")
    print("=" * 50)
    
    # Test with different motor sizes
    motor_powers = [10000, 25000, 50000, 100000]  # W
    
    for power in motor_powers:
        test_conveyor = ConveyorBelt(
            belt_length=100.0,
            belt_width=1.5,
            belt_angle=0.2,  # Steeper angle
            motor_power=power
        )
        
        u = np.array([30.0, 3.0, 0.1])  # High load conditions
        result = test_conveyor.steady_state(u)
        
        print(f"Motor: {power/1000:3.0f} kW, "
              f"Flow: {result[0]:5.1f} kg/s, "
              f"Power used: {result[1]/1000:5.1f} kW "
              f"({result[1]/power*100:4.1f}%)")
    
    # Create visualizations
    create_plots(conveyor, speeds, flow_rates, power_consumption, 
                time, flow_history, power_history, material_results)
    
    print("\n" + "=" * 60)
    print("Analysis Complete - Check generated plots")
    print("=" * 60)

def create_plots(conveyor, speeds, flow_rates, power_consumption, 
                time, flow_history, power_history, material_results):
    """Create visualization plots."""
    
    # Plot 1: Speed sensitivity
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.plot(speeds, flow_rates, 'b-', linewidth=2, label='Flow Rate')
    plt.xlabel('Belt Speed (m/s)')
    plt.ylabel('Flow Rate (kg/s)')
    plt.title('Flow Rate vs Belt Speed')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 2, 2)
    plt.plot(speeds, np.array(power_consumption)/1000, 'r-', linewidth=2, label='Power')
    plt.axhline(y=conveyor.motor_power/1000, color='k', linestyle='--', label='Motor Limit')
    plt.xlabel('Belt Speed (m/s)')
    plt.ylabel('Power (kW)')
    plt.title('Power Consumption vs Belt Speed')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 2, 3)
    efficiency = np.array(flow_rates) / 20.0 * 100  # 20 kg/s feed rate
    plt.plot(speeds, efficiency, 'g-', linewidth=2)
    plt.xlabel('Belt Speed (m/s)')
    plt.ylabel('Efficiency (%)')
    plt.title('Transport Efficiency vs Belt Speed')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 4)
    # Material properties effect
    densities = [result[1] for result in material_results]
    flows = [result[2][0] for result in material_results]
    powers = [result[2][1]/1000 for result in material_results]
    
    plt.scatter(densities, flows, c='blue', s=60, alpha=0.7, label='Flow Rate')
    plt.xlabel('Material Density (kg/m³)')
    plt.ylabel('Flow Rate (kg/s)')
    plt.title('Material Density Effect')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('ConveyorBelt_example_plots.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 2: Dynamic response
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(time/60, flow_history, 'b-', linewidth=2, label='Flow Rate')
    plt.axvline(x=1, color='r', linestyle='--', alpha=0.7, label='Step Change')
    plt.xlabel('Time (min)')
    plt.ylabel('Flow Rate (kg/s)')
    plt.title('Dynamic Response - Flow Rate')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(time/60, np.array(power_history)/1000, 'r-', linewidth=2, label='Power')
    plt.axvline(x=1, color='r', linestyle='--', alpha=0.7, label='Step Change')
    plt.axhline(y=conveyor.motor_power/1000, color='k', linestyle=':', label='Motor Limit')
    plt.xlabel('Time (min)')
    plt.ylabel('Power (kW)')
    plt.title('Dynamic Response - Power')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('ConveyorBelt_detailed_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()
