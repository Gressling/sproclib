"""
Industrial Example: CSTR Temperature Control
Simplified example showing PID controller behavior
"""

import numpy as np
from sproclib.controller.pid.PIDController import PIDController

print("CSTR Temperature Control System")
print("=" * 40)
print("Reactor Volume: 10.0 m³")
print("Target Temperature: 85.0°C")
print("Process Gain: 0.8 °C/%")
print("Time Constant: 8.0 minutes")
print("Dead Time: 1.5 minutes")
print()

# PID Controller (Ziegler-Nichols tuning)
Kp = 2.5  # Proportional gain
Ki = 0.1  # Integral gain (1/s)  
Kd = 10.0  # Derivative gain (s)

print(f"PID Parameters:")
print(f"  Kp = {Kp}")
print(f"  Ki = {Ki} 1/s")
print(f"  Kd = {Kd} s")
print()

# Create controller
controller = PIDController(Kp=Kp, Ki=Ki, Kd=Kd, MV_min=0.0, MV_max=100.0)

# Test data: temperature response during startup
time_points = [0, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600]  # seconds
temperatures = [25, 35, 48, 62, 71, 78, 82, 84, 85, 85, 85]  # °C
setpoint = 85.0  # °C

print("Simulation Results")
print("-" * 30)
print("Time(min)  Temp(°C)  Valve(%)  Error(°C)")

valve_outputs = []
for i, (t, temp) in enumerate(zip(time_points, temperatures)):
    # Controller update
    valve_output = controller.update(t, setpoint, temp)
    valve_outputs.append(valve_output)
    
    error = setpoint - temp
    print(f"{t/60:8.1f}  {temp:8.1f}  {valve_output:8.1f}  {error:8.1f}")

print()

# Performance metrics
final_error = setpoint - temperatures[-1]
max_valve = max(valve_outputs)
min_valve = min(valve_outputs)

print("Performance Analysis")
print("-" * 20)
print(f"Final Error: {final_error:.1f}°C")
print(f"Valve Range: {min_valve:.1f} - {max_valve:.1f}%")
print(f"Control Effort: {max_valve - min_valve:.1f}% valve travel")
print()

# Industrial relevance
print("Industrial Applications")
print("-" * 22)
print("- Reactor temperature control via jacket cooling")
print("- Distillation column reboiler duty control")  
print("- Heat exchanger outlet temperature control")
print("- Crystallizer temperature profile control")
print()

print("Typical Industrial Parameters")
print("-" * 29)
print("Operating Temperature: 50-200°C")
print("Control Valve Range: 0-100%")
print("Response Time: 5-30 minutes")
print("Accuracy: ±0.5-2.0°C")
print("Control Interval: 1-10 seconds")
print()

print("Economic Impact")
print("-" * 15)
print("Energy savings: 5-15% with proper tuning")
print("Product quality improvement: 2-8%")
print("Reduced operator intervention: 60-80%")
print("Maintenance cost reduction: 10-25%")
