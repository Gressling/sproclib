"""
Example usage of ScrewFeeder class.

This script demonstrates the ScrewFeeder transport model with various
powder properties, operating conditions, and control scenarios.
"""

import numpy as np
import matplotlib.pyplot as plt
from ScrewFeeder import ScrewFeeder

def main():
    print("=" * 60)
    print("ScrewFeeder Transport Model Example")
    print("=" * 60)
    
    # Create screw feeder instance
    feeder = ScrewFeeder(
        screw_diameter=0.04,    # 40 mm screw
        screw_length=0.6,       # 60 cm length
        screw_pitch=0.02,       # 20 mm pitch
        screw_speed=120.0,      # 120 rpm
        fill_factor=0.35,       # 35% fill
        powder_density=900.0,   # Pharmaceutical powder
        powder_flowability=0.7, # Moderate flowability
        motor_torque_max=8.0,   # 8 N⋅m motor
        name="PharmaPowderFeeder"
    )
    
    print("\nScrew Feeder Parameters:")
    print(f"Screw diameter: {feeder.screw_diameter*1000:.0f} mm")
    print(f"Screw length: {feeder.screw_length*1000:.0f} mm")
    print(f"Screw pitch: {feeder.screw_pitch*1000:.0f} mm")
    print(f"Nominal speed: {feeder.screw_speed} rpm")
    print(f"Fill factor: {feeder.fill_factor}")
    print(f"Powder density: {feeder.powder_density} kg/m³")
    print(f"Flowability index: {feeder.powder_flowability}")
    print(f"Motor torque limit: {feeder.motor_torque_max} N⋅m")
    
    # Display model description
    description = feeder.describe()
    print(f"\nModel: {description['class_name']}")
    print(f"Algorithm: {description['algorithm']}")
    
    # Calculate theoretical capacity
    screw_area = np.pi * (feeder.screw_diameter/2)**2
    volume_per_rev = screw_area * feeder.screw_pitch
    theoretical_capacity = (feeder.screw_speed/60) * volume_per_rev * feeder.powder_density * feeder.fill_factor
    print(f"Theoretical capacity: {theoretical_capacity*3600:.2f} kg/h")
    
    # Test different operating conditions
    print("\n" + "=" * 50)
    print("Steady-State Performance Analysis")
    print("=" * 50)
    
    # Operating conditions: [screw_speed_setpoint, hopper_level, powder_moisture]
    test_conditions = [
        ([120.0, 0.4, 0.02], "Normal operation"),
        ([200.0, 0.4, 0.02], "High speed"),
        ([80.0, 0.4, 0.02], "Low speed"),
        ([120.0, 0.1, 0.02], "Low hopper level"),
        ([120.0, 0.6, 0.02], "High hopper level"),
        ([120.0, 0.4, 0.08], "High moisture content"),
        ([300.0, 0.5, 0.01], "Maximum throughput"),
        ([50.0, 0.2, 0.05], "Difficult conditions"),
    ]
    
    results = []
    for conditions, description in test_conditions:
        u = np.array(conditions)
        result = feeder.steady_state(u)
        results.append((conditions, result, description))
        
        # Calculate feed rate accuracy
        expected_theoretical = (u[0]/60) * volume_per_rev * feeder.powder_density * feeder.fill_factor
        accuracy = result[0] / expected_theoretical * 100 if expected_theoretical > 0 else 0
        
        print(f"\n{description}:")
        print(f"  Input: Speed={u[0]:.0f} rpm, Level={u[1]:.2f} m, Moisture={u[2]*100:.1f}%")
        print(f"  Output: Flow={result[0]*3600:.2f} kg/h, Torque={result[1]:.2f} N⋅m")
        print(f"  Accuracy: {accuracy:.1f}% of theoretical")
        if result[1] >= feeder.motor_torque_max * 0.95:
            print(f"  WARNING: Near torque limit!")
    
    # Speed sensitivity analysis
    print("\n" + "=" * 50)
    print("Speed Sensitivity Analysis")
    print("=" * 50)
    
    speeds = np.linspace(20, 400, 25)
    flow_rates = []
    torques = []
    feed_accuracies = []
    
    for speed in speeds:
        u = np.array([speed, 0.4, 0.02])
        result = feeder.steady_state(u)
        flow_rates.append(result[0])
        torques.append(result[1])
        
        # Calculate linearity
        expected = (speed/120.0) * theoretical_capacity  # Linear expectation
        accuracy = result[0] / expected * 100 if expected > 0 else 0
        feed_accuracies.append(accuracy)
    
    # Find operating range
    good_accuracy_mask = np.array(feed_accuracies) > 95
    torque_ok_mask = np.array(torques) < feeder.motor_torque_max * 0.9
    good_operation_mask = good_accuracy_mask & torque_ok_mask
    
    if np.any(good_operation_mask):
        good_speeds = speeds[good_operation_mask]
        print(f"Recommended speed range: {good_speeds[0]:.0f} - {good_speeds[-1]:.0f} rpm")
        print(f"Turndown ratio: {good_speeds[-1]/good_speeds[0]:.1f}:1")
    
    # Powder properties effect
    print("\n" + "=" * 50)
    print("Powder Properties Effect Analysis")
    print("=" * 50)
    
    powder_types = [
        (400, 0.9, "Free-flowing powder"),
        (600, 0.8, "Good flowing granules"),
        (900, 0.7, "Moderate flowing powder"),
        (1200, 0.5, "Cohesive powder"),
        (1500, 0.3, "Poor flowing powder")
    ]
    
    powder_results = []
    for density, flowability, name in powder_types:
        test_feeder = ScrewFeeder(
            screw_diameter=0.04,
            screw_length=0.6,
            screw_pitch=0.02,
            powder_density=density,
            powder_flowability=flowability,
            motor_torque_max=8.0
        )
        
        u = np.array([120.0, 0.4, 0.02])
        result = test_feeder.steady_state(u)
        powder_results.append((name, density, flowability, result))
        
        print(f"{name:25s}: ρ={density:4d} kg/m³, FI={flowability:.1f}, "
              f"Flow={result[0]*3600:6.1f} kg/h, Torque={result[1]:.2f} N⋅m")
    
    # Moisture content effect
    print("\n" + "=" * 50)
    print("Moisture Content Effect Analysis")
    print("=" * 50)
    
    moistures = np.linspace(0, 0.15, 16)  # 0 to 15% moisture
    moisture_flows = []
    moisture_torques = []
    
    for moisture in moistures:
        u = np.array([120.0, 0.4, moisture])
        result = feeder.steady_state(u)
        moisture_flows.append(result[0])
        moisture_torques.append(result[1])
    
    # Find moisture limit
    torque_limit_moisture = None
    for i, torque in enumerate(moisture_torques):
        if torque >= feeder.motor_torque_max * 0.95:
            torque_limit_moisture = moistures[i]
            break
    
    if torque_limit_moisture:
        print(f"Moisture limit for operation: ~{torque_limit_moisture*100:.1f}%")
    
    print("Moisture Effects:")
    for moisture in [0.02, 0.05, 0.10, 0.15]:
        idx = np.argmin(np.abs(moistures - moisture))
        flow_reduction = (moisture_flows[0] - moisture_flows[idx]) / moisture_flows[0] * 100
        print(f"  {moisture*100:4.1f}% moisture: "
              f"Flow={moisture_flows[idx]*3600:6.1f} kg/h "
              f"({-flow_reduction:+4.1f}%), Torque={moisture_torques[idx]:.2f} N⋅m")
    
    # Hopper level effect
    print("\n" + "=" * 50)
    print("Hopper Level Effect Analysis")
    print("=" * 50)
    
    hopper_levels = np.linspace(0.05, 0.8, 15)
    level_flows = []
    level_torques = []
    
    for level in hopper_levels:
        u = np.array([120.0, level, 0.02])
        result = feeder.steady_state(u)
        level_flows.append(result[0])
        level_torques.append(result[1])
    
    # Find critical level
    critical_level = None
    for i, flow in enumerate(level_flows):
        if flow >= level_flows[-1] * 0.95:  # 95% of maximum flow
            critical_level = hopper_levels[i]
            break
    
    if critical_level:
        print(f"Critical hopper level: {critical_level:.2f} m")
    
    print("Hopper Level Effects:")
    for level in [0.1, 0.2, 0.4, 0.6]:
        idx = np.argmin(np.abs(hopper_levels - level))
        print(f"  Level {level:.1f} m: "
              f"Flow={level_flows[idx]*3600:6.1f} kg/h, "
              f"Torque={level_torques[idx]:.2f} N⋅m")
    
    # Dynamic response analysis
    print("\n" + "=" * 50)
    print("Dynamic Response Analysis")
    print("=" * 50)
    
    # Simulate step change in speed
    dt = 1.0  # time step (s)
    t_final = 300.0  # simulation time (s)
    time = np.arange(0, t_final, dt)
    
    # Initial conditions: [flow_rate, torque]
    x = np.array([0.01, 2.0])  # kg/s, N⋅m
    
    # Step changes: speed setpoint changes
    speeds_dynamic = np.piecewise(time, 
                                 [time < 60, (time >= 60) & (time < 120), 
                                  (time >= 120) & (time < 180), time >= 180],
                                 [80, 120, 200, 150])
    
    flow_history = []
    torque_history = []
    speed_history = []
    
    for i, t in enumerate(time):
        u = np.array([speeds_dynamic[i], 0.4, 0.02])
        
        # Store current state
        flow_history.append(x[0])
        torque_history.append(x[1])
        speed_history.append(speeds_dynamic[i])
        
        # Calculate derivatives
        dxdt = feeder.dynamics(t, x, u)
        
        # Euler integration
        x = x + dxdt * dt
    
    print(f"Speed changes: 80 → 120 → 200 → 150 rpm")
    print(f"Flow response time: ~{30:.0f} s (estimated)")
    print(f"Torque response time: ~{5:.0f} s (motor dynamics)")
    
    # Screw geometry optimization
    print("\n" + "=" * 50)
    print("Screw Geometry Optimization")
    print("=" * 50)
    
    # Test different screw diameters
    diameters = [0.025, 0.03, 0.04, 0.05, 0.06]  # 25 to 60 mm
    geometry_results = []
    
    for diameter in diameters:
        test_feeder = ScrewFeeder(
            screw_diameter=diameter,
            screw_length=0.6,
            screw_pitch=diameter/2,  # P/D = 0.5
            powder_density=900.0,
            powder_flowability=0.7
        )
        
        u = np.array([120.0, 0.4, 0.02])
        result = test_feeder.steady_state(u)
        geometry_results.append((diameter, result))
        
        print(f"Diameter {diameter*1000:2.0f} mm: "
              f"Flow={result[0]*3600:6.1f} kg/h, "
              f"Torque={result[1]:.2f} N⋅m")
    
    # Flow rate control simulation
    print("\n" + "=" * 50)
    print("Flow Rate Control Simulation")
    print("=" * 50)
    
    # Simple PI controller for flow rate
    setpoint = 0.015  # kg/s target flow rate
    Kp = 1000.0  # Proportional gain
    Ki = 50.0    # Integral gain
    
    # Control simulation
    control_time = np.arange(0, 200, 2.0)
    flow_setpoints = np.where(control_time < 100, 0.010, 0.020)  # Step change
    
    x_control = np.array([0.008, 3.0])  # Initial state
    speed_control = 100.0  # Initial speed
    integral_error = 0.0
    
    control_flows = []
    control_speeds = []
    control_setpoints = []
    
    for i, t in enumerate(control_time):
        setpoint = flow_setpoints[i]
        error = setpoint - x_control[0]
        
        # PI control
        integral_error += error * 2.0  # dt = 2.0
        speed_command = 120.0 + Kp * error + Ki * integral_error
        speed_command = np.clip(speed_command, 20, 300)  # Limit speed
        
        # Store results
        control_flows.append(x_control[0])
        control_speeds.append(speed_command)
        control_setpoints.append(setpoint)
        
        # Simulate system
        u = np.array([speed_command, 0.4, 0.02])
        dxdt = feeder.dynamics(t, x_control, u)
        x_control = x_control + dxdt * 2.0
    
    print(f"Control performance:")
    print(f"  Setpoint change: {flow_setpoints[0]*3600:.1f} → {flow_setpoints[-1]*3600:.1f} kg/h")
    print(f"  Final error: {(control_setpoints[-1] - control_flows[-1])*3600:.2f} kg/h")
    print(f"  Speed range used: {min(control_speeds):.0f} - {max(control_speeds):.0f} rpm")
    
    # Create visualizations
    create_plots(feeder, speeds, flow_rates, torques, moistures, moisture_flows,
                moisture_torques, hopper_levels, level_flows, time, flow_history,
                torque_history, speed_history, powder_results, geometry_results,
                control_time, control_flows, control_speeds, control_setpoints)
    
    print("\n" + "=" * 60)
    print("Analysis Complete - Check generated plots")
    print("=" * 60)

def create_plots(feeder, speeds, flow_rates, torques, moistures, moisture_flows,
                moisture_torques, hopper_levels, level_flows, time, flow_history,
                torque_history, speed_history, powder_results, geometry_results,
                control_time, control_flows, control_speeds, control_setpoints):
    """Create visualization plots."""
    
    # Plot 1: Operating characteristics
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 3, 1)
    plt.plot(speeds, np.array(flow_rates)*3600, 'b-', linewidth=2, label='Actual')
    # Theoretical linear line
    theoretical = speeds * feeder.powder_density * np.pi * (feeder.screw_diameter/2)**2 * feeder.screw_pitch * feeder.fill_factor / 60
    plt.plot(speeds, theoretical*3600, 'r--', alpha=0.7, label='Theoretical')
    plt.xlabel('Screw Speed (rpm)')
    plt.ylabel('Flow Rate (kg/h)')
    plt.title('Flow Rate vs Screw Speed')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 3, 2)
    plt.plot(speeds, torques, 'g-', linewidth=2)
    plt.axhline(y=feeder.motor_torque_max, color='r', linestyle='--', alpha=0.7, label='Torque Limit')
    plt.xlabel('Screw Speed (rpm)')
    plt.ylabel('Motor Torque (N⋅m)')
    plt.title('Torque vs Screw Speed')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 3, 3)
    plt.plot(moistures*100, np.array(moisture_flows)*3600, 'purple', linewidth=2)
    plt.xlabel('Moisture Content (%)')
    plt.ylabel('Flow Rate (kg/h)')
    plt.title('Moisture Effect on Flow Rate')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 4)
    plt.plot(moistures*100, moisture_torques, 'orange', linewidth=2)
    plt.axhline(y=feeder.motor_torque_max, color='r', linestyle='--', alpha=0.7, label='Torque Limit')
    plt.xlabel('Moisture Content (%)')
    plt.ylabel('Motor Torque (N⋅m)')
    plt.title('Moisture Effect on Torque')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 3, 5)
    plt.plot(hopper_levels, np.array(level_flows)*3600, 'brown', linewidth=2)
    plt.xlabel('Hopper Level (m)')
    plt.ylabel('Flow Rate (kg/h)')
    plt.title('Hopper Level Effect')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 6)
    # Powder properties effect
    densities = [result[1] for result in powder_results]
    powder_flows = [result[3][0]*3600 for result in powder_results]
    flowabilities = [result[2] for result in powder_results]
    
    scatter = plt.scatter(densities, powder_flows, c=flowabilities, s=80, 
                         cmap='viridis', alpha=0.8)
    plt.colorbar(scatter, label='Flowability Index')
    plt.xlabel('Powder Density (kg/m³)')
    plt.ylabel('Flow Rate (kg/h)')
    plt.title('Powder Properties Effect')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('ScrewFeeder_example_plots.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 2: Dynamic response and control
    plt.figure(figsize=(12, 10))
    
    plt.subplot(2, 2, 1)
    plt.plot(time/60, np.array(flow_history)*3600, 'b-', linewidth=2, label='Flow Rate')
    plt.xlabel('Time (min)')
    plt.ylabel('Flow Rate (kg/h)')
    plt.title('Dynamic Response - Flow Rate')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 2, 2)
    plt.plot(time/60, speed_history, 'g-', linewidth=2, label='Speed Setpoint')
    plt.xlabel('Time (min)')
    plt.ylabel('Screw Speed (rpm)')
    plt.title('Dynamic Response - Speed Changes')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 2, 3)
    plt.plot(control_time/60, np.array(control_flows)*3600, 'b-', linewidth=2, label='Actual')
    plt.plot(control_time/60, np.array(control_setpoints)*3600, 'r--', linewidth=2, label='Setpoint')
    plt.xlabel('Time (min)')
    plt.ylabel('Flow Rate (kg/h)')
    plt.title('Flow Rate Control')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 2, 4)
    plt.plot(control_time/60, control_speeds, 'g-', linewidth=2)
    plt.xlabel('Time (min)')
    plt.ylabel('Speed Command (rpm)')
    plt.title('Controller Output')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('ScrewFeeder_detailed_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()
