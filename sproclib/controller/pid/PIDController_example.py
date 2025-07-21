"""
Industrial Example: CSTR Temperature Control
Typical industrial reactor temperature control using jacket cooling
"""

import numpy as np
import matplotlib.pyplot as plt
from sproclib.controller.pid.PIDController import PIDController

# Process conditions (typical industrial scale)
reactor_volume = 10.0  # m³ (10,000 L reactor)
operating_temperature = 85.0  # °C (target temperature)
jacket_area = 15.0  # m² (heat transfer area)
heat_transfer_coeff = 500.0  # W/(m²·K) (typical for jacket cooling)

# Heat generation from reaction
reaction_heat = 50000.0  # W (50 kW exothermic reaction)

print("CSTR Temperature Control System")
print("=" * 40)
print(f"Reactor Volume: {reactor_volume} m³")
print(f"Target Temperature: {operating_temperature}°C")
print(f"Reaction Heat Generation: {reaction_heat/1000:.1f} kW")
print(f"Heat Transfer Area: {jacket_area} m²")
print()

# PID Controller Design (Ziegler-Nichols tuning)
# Process characteristics: K=0.8°C/%, τ=8 minutes, θ=1.5 minutes
process_gain = 0.8  # °C/% valve opening
time_constant = 480.0  # seconds (8 minutes)
dead_time = 90.0  # seconds (1.5 minutes)

# Ziegler-Nichols PID tuning
Kp = 1.2 * time_constant / (process_gain * dead_time)  # 4.27
Ki = Kp / (2.0 * dead_time)  # 0.024 1/s
Kd = Kp * 0.5 * dead_time  # 192 s

print("Controller Tuning Parameters")
print("-" * 30)
print(f"Process Gain (K): {process_gain} °C/%")
print(f"Time Constant (τ): {time_constant/60:.1f} minutes")
print(f"Dead Time (θ): {dead_time/60:.1f} minutes")
print()
print(f"PID Parameters:")
print(f"  Kp = {Kp:.2f}")
print(f"  Ki = {Ki:.4f} 1/s")
print(f"  Kd = {Kd:.1f} s")
print()

# Create PID controller
temperature_controller = PIDController(
    Kp=Kp, 
    Ki=Ki, 
    Kd=Kd, 
    MV_min=0.0,  # 0% valve opening minimum
    MV_max=100.0  # 100% valve opening maximum
)

# Setpoint and disturbance scenario
setpoint = operating_temperature
control_interval = 5.0  # seconds (typical for temperature control)

# Simulate reactor startup and disturbance
time_sim = np.arange(0, 3600, control_interval)  # 1 hour simulation
temperatures = np.zeros_like(time_sim)
valve_outputs = np.zeros_like(time_sim)
setpoints = np.zeros_like(time_sim)

# Initial conditions
temperatures[0] = 25.0  # Start at ambient temperature
current_temp = temperatures[0]

print("Simulation Results")
print("-" * 20)
print("Time(min)  Temp(°C)  Valve(%)  Error(°C)")

# Disturbance profile
for i, t in enumerate(time_sim):
    # Add feed flow disturbance at t=1800s (30 minutes)
    if t >= 1800:
        current_setpoint = operating_temperature + 2.0  # Setpoint change
    else:
        current_setpoint = operating_temperature
    
    setpoints[i] = current_setpoint
    
    # PID controller calculation
    valve_output = temperature_controller.update(t, current_setpoint, current_temp)
    valve_outputs[i] = valve_output
    
    # Simple process model (first-order plus dead time approximation)
    # Temperature response to valve position change
    if i > 0:
        # Process dynamics simulation
        temp_change = (valve_output - 50.0) * process_gain * (control_interval / time_constant)
        current_temp += temp_change
        
        # Add measurement noise (±0.1°C)
        measurement_noise = np.random.normal(0, 0.1)
        measured_temp = current_temp + measurement_noise
    else:
        measured_temp = current_temp
    
    temperatures[i] = measured_temp
    current_temp = measured_temp
    
    # Print selected time points
    if i % 12 == 0:  # Every minute
        error = setpoints[i] - temperatures[i]
        print(f"{t/60:8.1f}  {temperatures[i]:8.1f}  {valve_outputs[i]:8.1f}  {error:8.1f}")

print()

# Performance analysis
settling_time_idx = np.where(np.abs(temperatures - operating_temperature) < 0.5)[0]
if len(settling_time_idx) > 0:
    settling_time = time_sim[settling_time_idx[0]] / 60.0  # minutes
    print(f"Settling Time (±0.5°C): {settling_time:.1f} minutes")

max_overshoot = np.max(temperatures) - operating_temperature
print(f"Maximum Overshoot: {max_overshoot:.1f}°C")

steady_state_error = np.mean(temperatures[-60:]) - operating_temperature  # Last 5 minutes
print(f"Steady State Error: {steady_state_error:.2f}°C")

# Controller effort analysis
max_valve_output = np.max(valve_outputs)
min_valve_output = np.min(valve_outputs)
valve_range = max_valve_output - min_valve_output

print(f"Valve Output Range: {min_valve_output:.1f} - {max_valve_output:.1f}%")
print(f"Control Effort: {valve_range:.1f}% valve travel")
print()

# Economic analysis
cooling_water_flow = valve_outputs * 0.5  # m³/h per % valve opening
cooling_cost = np.mean(cooling_water_flow) * 0.002  # $/m³ cooling water
daily_cooling_cost = cooling_cost * 24
annual_cooling_cost = daily_cooling_cost * 350  # operating days

print("Economic Impact")
print("-" * 15)
print(f"Average Cooling Water Flow: {np.mean(cooling_water_flow):.1f} m³/h")
print(f"Daily Cooling Cost: ${daily_cooling_cost:.2f}")
print(f"Annual Cooling Cost: ${annual_cooling_cost:.0f}")
print()

# Safety analysis
temp_excursions = np.sum(temperatures > operating_temperature + 5.0)
safety_margin = 100.0 - operating_temperature  # °C to safety limit

print("Safety Analysis")
print("-" * 15)
print(f"Temperature Excursions (>90°C): {temp_excursions} occurrences")
print(f"Safety Margin to 100°C: {safety_margin:.1f}°C")
print(f"Maximum Temperature Reached: {np.max(temperatures):.1f}°C")

# Compare with Perry's Chemical Engineers' Handbook correlations
# Typical reactor temperature control performance
print()
print("Comparison with Literature")
print("-" * 25)
print("Perry's Handbook typical performance:")
print("  - Settling time: 2-4 time constants")
print(f"  - Expected settling: {2*time_constant/60:.1f}-{4*time_constant/60:.1f} minutes")
print("  - Overshoot: <10% for well-tuned system")
print(f"  - Achieved overshoot: {(max_overshoot/operating_temperature)*100:.1f}%")

# Dimensionless analysis
Damköhler_number = reaction_heat / (heat_transfer_coeff * jacket_area * 10)  # Simplified
print(f"  - Damköhler number (Da): {Damköhler_number:.2f}")
if Damköhler_number > 1.0:
    print("    High reaction rate relative to heat removal capacity")
else:
    print("    Good heat removal capacity relative to reaction rate")
