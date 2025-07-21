"""
Example demonstrating BatchTransferPumping model usage.
Shows steady-state analysis, dynamic simulation, and performance evaluation.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the current directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from .batch_transfer_pumping import BatchTransferPumping


def main():
    """Demonstrate batch transfer pumping model capabilities."""
    
    print("="*60)
    print("BATCH TRANSFER PUMPING ANALYSIS")
    print("="*60)
    
    # Create pump instances for different scenarios
    water_pump = BatchTransferPumping(
        pump_capacity=0.01,      # 10 L/s capacity
        pump_head_max=50.0,      # 50 m head
        tank_volume=2.0,         # 2 m³ tank
        pipe_length=30.0,        # 30 m transfer line
        pipe_diameter=0.05,      # 5 cm diameter
        fluid_density=1000.0,    # Water density
        fluid_viscosity=1e-3,    # Water viscosity
        transfer_efficiency=0.85,
        name="WaterTransferPump"
    )
    
    oil_pump = BatchTransferPumping(
        pump_capacity=0.005,     # 5 L/s capacity (smaller)
        pump_head_max=30.0,      # 30 m head
        tank_volume=1.0,         # 1 m³ tank
        pipe_length=20.0,        # 20 m transfer line
        pipe_diameter=0.04,      # 4 cm diameter
        fluid_density=850.0,     # Oil density
        fluid_viscosity=0.01,    # Oil viscosity (10x water)
        transfer_efficiency=0.80,
        name="OilTransferPump"
    )
    
    # Display pump descriptions
    print("\n1. PUMP SPECIFICATIONS")
    print("-" * 40)
    
    water_desc = water_pump.describe()
    print(f"Water Pump: {water_desc['description']}")
    print(f"Capacity: {water_desc['parameters']['pump_capacity']['value']} {water_desc['parameters']['pump_capacity']['unit']}")
    print(f"Max Head: {water_desc['parameters']['pump_head_max']['value']} {water_desc['parameters']['pump_head_max']['unit']}")
    
    oil_desc = oil_pump.describe()
    print(f"\nOil Pump: {oil_desc['description']}")
    print(f"Capacity: {oil_desc['parameters']['pump_capacity']['value']} {oil_desc['parameters']['pump_capacity']['unit']}")
    print(f"Max Head: {oil_desc['parameters']['pump_head_max']['value']} {oil_desc['parameters']['pump_head_max']['unit']}")
    
    # Steady-state analysis
    print("\n2. STEADY-STATE ANALYSIS")
    print("-" * 40)
    
    # Test various operating conditions
    test_conditions = [
        {"name": "Normal Transfer", "source": 0.8, "dest": 0.2, "speed": 1.0},
        {"name": "Uphill Transfer", "source": 0.3, "dest": 0.7, "speed": 1.0},
        {"name": "Reduced Speed", "source": 0.8, "dest": 0.2, "speed": 0.6},
        {"name": "Low Source", "source": 0.1, "dest": 0.0, "speed": 1.0}
    ]
    
    print(f"{'Condition':<15} {'Fluid':<8} {'Flow Rate':<12} {'Transfer Time':<15}")
    print(f"{'='*15} {'='*8} {'='*12} {'='*15}")
    
    steady_state_data = {"water": [], "oil": []}
    
    for condition in test_conditions:
        u = np.array([condition["source"], condition["dest"], condition["speed"]])
        
        # Water pump analysis
        water_result = water_pump.steady_state(u)
        water_flow, water_time = water_result
        steady_state_data["water"].append(water_flow)
        
        # Oil pump analysis
        oil_result = oil_pump.steady_state(u)
        oil_flow, oil_time = oil_result
        steady_state_data["oil"].append(oil_flow)
        
        print(f"{condition['name']:<15} {'Water':<8} {water_flow*1000:<8.1f} L/s {water_time/60:<11.1f} min")
        print(f"{'':<15} {'Oil':<8} {oil_flow*1000:<8.1f} L/s {oil_time/60:<11.1f} min")
        print()
    
    # Dynamic simulation
    print("\n3. DYNAMIC SIMULATION")
    print("-" * 40)
    
    # Simulate batch transfer process
    time_span = np.linspace(0, 3600, 361)  # 1 hour, 10s intervals
    dt = time_span[1] - time_span[0]
    
    # Initial conditions: pump off, tank 80% full
    x_water = np.array([0.0, 0.8])  # [flow_rate, source_level]
    x_oil = np.array([0.0, 0.8])
    
    # Control inputs: transfer to 20% destination level
    u_transfer = np.array([0.8, 0.2, 1.0])  # [source_setpoint, dest_level, pump_speed]
    
    # Storage for results
    results_water = {"time": [], "flow": [], "level": []}
    results_oil = {"time": [], "flow": [], "level": []}
    
    print("Simulating water transfer...")
    for t in time_span:
        # Store current state
        results_water["time"].append(t)
        results_water["flow"].append(x_water[0])
        results_water["level"].append(x_water[1])
        
        # Calculate derivatives
        if x_water[1] > 0.05:  # Continue until tank nearly empty
            dxdt = water_pump.dynamics(t, x_water, u_transfer)
            x_water = x_water + dxdt * dt
            x_water[1] = max(0, x_water[1])  # Prevent negative level
        else:
            x_water[0] = 0  # Stop flow when empty
    
    print("Simulating oil transfer...")
    for t in time_span:
        # Store current state
        results_oil["time"].append(t)
        results_oil["flow"].append(x_oil[0])
        results_oil["level"].append(x_oil[1])
        
        # Calculate derivatives
        if x_oil[1] > 0.05:  # Continue until tank nearly empty
            dxdt = oil_pump.dynamics(t, x_oil, u_transfer)
            x_oil = x_oil + dxdt * dt
            x_oil[1] = max(0, x_oil[1])  # Prevent negative level
        else:
            x_oil[0] = 0  # Stop flow when empty
    
    # Calculate performance metrics
    print("\n4. PERFORMANCE ANALYSIS")
    print("-" * 40)
    
    # Find 95% transfer time
    def find_transfer_time(level_data, target_fraction=0.05):
        for i, level in enumerate(level_data):
            if level <= target_fraction:
                return results_water["time"][i]
        return results_water["time"][-1]
    
    water_transfer_time = find_transfer_time(results_water["level"])
    oil_transfer_time = find_transfer_time(results_oil["level"])
    
    water_avg_flow = np.mean([f for f in results_water["flow"] if f > 0])
    oil_avg_flow = np.mean([f for f in results_oil["flow"] if f > 0])
    
    print(f"Water Transfer:")
    print(f"  - Transfer time (95%): {water_transfer_time/60:.1f} minutes")
    print(f"  - Average flow rate: {water_avg_flow*1000:.1f} L/s")
    print(f"  - Peak flow rate: {max(results_water['flow'])*1000:.1f} L/s")
    
    print(f"\nOil Transfer:")
    print(f"  - Transfer time (95%): {oil_transfer_time/60:.1f} minutes")
    print(f"  - Average flow rate: {oil_avg_flow*1000:.1f} L/s")
    print(f"  - Peak flow rate: {max(results_oil['flow'])*1000:.1f} L/s")
    
    # Reynolds number analysis
    print("\n5. HYDRAULIC ANALYSIS")
    print("-" * 40)
    
    def calculate_reynolds(pump, flow_rate):
        if flow_rate > 0:
            velocity = flow_rate / (np.pi * (pump.pipe_diameter/2)**2)
            re = pump.fluid_density * velocity * pump.pipe_diameter / pump.fluid_viscosity
            return re, velocity
        return 0, 0
    
    # At peak flow conditions
    water_re, water_vel = calculate_reynolds(water_pump, max(results_water['flow']))
    oil_re, oil_vel = calculate_reynolds(oil_pump, max(results_oil['flow']))
    
    print(f"Water at peak flow:")
    print(f"  - Reynolds number: {water_re:.0f}")
    print(f"  - Flow regime: {'Turbulent' if water_re > 2300 else 'Laminar'}")
    print(f"  - Velocity: {water_vel:.2f} m/s")
    
    print(f"\nOil at peak flow:")
    print(f"  - Reynolds number: {oil_re:.0f}")
    print(f"  - Flow regime: {'Turbulent' if oil_re > 2300 else 'Laminar'}")
    print(f"  - Velocity: {oil_vel:.2f} m/s")
    
    # Create visualizations
    print("\n6. GENERATING VISUALIZATIONS")
    print("-" * 40)
    
    # Convert time to minutes for plotting
    time_min_water = np.array(results_water["time"]) / 60
    time_min_oil = np.array(results_oil["time"]) / 60
    
    # Plot 1: Dynamic response comparison
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    
    # Flow rates
    ax1.plot(time_min_water, np.array(results_water["flow"]) * 1000, 'b-', label='Water', linewidth=2)
    ax1.plot(time_min_oil, np.array(results_oil["flow"]) * 1000, 'r--', label='Oil', linewidth=2)
    ax1.set_xlabel('Time (min)')
    ax1.set_ylabel('Flow Rate (L/s)')
    ax1.set_title('Flow Rate vs Time')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Tank levels
    ax2.plot(time_min_water, np.array(results_water["level"]) * 100, 'b-', label='Water', linewidth=2)
    ax2.plot(time_min_oil, np.array(results_oil["level"]) * 100, 'r--', label='Oil', linewidth=2)
    ax2.set_xlabel('Time (min)')
    ax2.set_ylabel('Tank Level (%)')
    ax2.set_title('Tank Level vs Time')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Steady-state comparison
    conditions = ['Normal', 'Uphill', 'Reduced Speed', 'Low Source']
    water_flows = np.array(steady_state_data["water"]) * 1000
    oil_flows = np.array(steady_state_data["oil"]) * 1000
    
    x = np.arange(len(conditions))
    width = 0.35
    
    ax3.bar(x - width/2, water_flows, width, label='Water', color='blue', alpha=0.7)
    ax3.bar(x + width/2, oil_flows, width, label='Oil', color='red', alpha=0.7)
    ax3.set_xlabel('Operating Condition')
    ax3.set_ylabel('Flow Rate (L/s)')
    ax3.set_title('Steady-State Flow Rates')
    ax3.set_xticks(x)
    ax3.set_xticklabels(conditions, rotation=45)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Pump characteristic curves
    speed_range = np.linspace(0, 1, 11)
    water_flows_curve = []
    oil_flows_curve = []
    
    base_conditions = np.array([0.8, 0.2, 1.0])  # Base test condition
    
    for speed in speed_range:
        test_u = base_conditions.copy()
        test_u[2] = speed
        
        water_result = water_pump.steady_state(test_u)
        oil_result = oil_pump.steady_state(test_u)
        
        water_flows_curve.append(water_result[0] * 1000)
        oil_flows_curve.append(oil_result[0] * 1000)
    
    ax4.plot(speed_range * 100, water_flows_curve, 'b-o', label='Water', linewidth=2)
    ax4.plot(speed_range * 100, oil_flows_curve, 'r--s', label='Oil', linewidth=2)
    ax4.set_xlabel('Pump Speed (%)')
    ax4.set_ylabel('Flow Rate (L/s)')
    ax4.set_title('Pump Characteristic Curves')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('BatchTransferPumping_example_plots.png', dpi=300, bbox_inches='tight')
    print("Saved: BatchTransferPumping_example_plots.png")
    
    # Plot 2: Detailed analysis
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    
    # Reynolds number evolution
    water_re_time = []
    oil_re_time = []
    
    for flow in results_water["flow"]:
        re, _ = calculate_reynolds(water_pump, flow)
        water_re_time.append(re)
    
    for flow in results_oil["flow"]:
        re, _ = calculate_reynolds(oil_pump, flow)
        oil_re_time.append(re)
    
    ax1.plot(time_min_water, water_re_time, 'b-', label='Water', linewidth=2)
    ax1.plot(time_min_oil, oil_re_time, 'r--', label='Oil', linewidth=2)
    ax1.axhline(y=2300, color='k', linestyle=':', alpha=0.7, label='Laminar/Turbulent Transition')
    ax1.set_xlabel('Time (min)')
    ax1.set_ylabel('Reynolds Number')
    ax1.set_title('Reynolds Number Evolution')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # Cumulative volume transferred
    water_volume = np.cumsum(np.array(results_water["flow"]) * dt) * 1000  # Liters
    oil_volume = np.cumsum(np.array(results_oil["flow"]) * dt) * 1000
    
    ax2.plot(time_min_water, water_volume, 'b-', label='Water', linewidth=2)
    ax2.plot(time_min_oil, oil_volume, 'r--', label='Oil', linewidth=2)
    ax2.set_xlabel('Time (min)')
    ax2.set_ylabel('Volume Transferred (L)')
    ax2.set_title('Cumulative Volume Transfer')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Transfer efficiency over time
    water_efficiency = np.array(results_water["flow"]) / water_pump.pump_capacity * 100
    oil_efficiency = np.array(results_oil["flow"]) / oil_pump.pump_capacity * 100
    
    ax3.plot(time_min_water, water_efficiency, 'b-', label='Water', linewidth=2)
    ax3.plot(time_min_oil, oil_efficiency, 'r--', label='Oil', linewidth=2)
    ax3.set_xlabel('Time (min)')
    ax3.set_ylabel('Pump Efficiency (%)')
    ax3.set_title('Pump Operating Efficiency')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Head requirement analysis
    head_data = {"water": [], "oil": []}
    level_range = np.linspace(0.1, 0.9, 9)
    
    for level in level_range:
        test_u = np.array([level, 0.2, 1.0])
        
        # Calculate static head
        static_head = 0.2 - level  # Destination - source (relative)
        head_data["water"].append(static_head)
        head_data["oil"].append(static_head)
    
    ax4.plot(level_range * 100, head_data["water"], 'b-o', label='Required Head', linewidth=2)
    ax4.axhline(y=water_pump.pump_head_max, color='b', linestyle='--', alpha=0.7, label='Water Pump Max Head')
    ax4.axhline(y=oil_pump.pump_head_max, color='r', linestyle='--', alpha=0.7, label='Oil Pump Max Head')
    ax4.set_xlabel('Source Tank Level (%)')
    ax4.set_ylabel('Head Requirement (m)')
    ax4.set_title('Head Requirements vs Tank Level')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('BatchTransferPumping_detailed_analysis.png', dpi=300, bbox_inches='tight')
    print("Saved: BatchTransferPumping_detailed_analysis.png")
    
    print("\n7. SUMMARY")
    print("-" * 40)
    print("Batch transfer pumping analysis completed successfully.")
    print("Key findings:")
    print(f"- Water transfer is faster due to lower viscosity and higher pump capacity")
    print(f"- Oil transfer requires more time due to higher viscosity and smaller pump")
    print(f"- Both systems operate in different Reynolds number regimes")
    print(f"- Pump sizing affects transfer efficiency and time")
    print("\nFiles generated:")
    print("- BatchTransferPumping_example_plots.png")
    print("- BatchTransferPumping_detailed_analysis.png")
    print("- BatchTransferPumping_example.out")


if __name__ == "__main__":
    main()
