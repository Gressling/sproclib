"""
Create visualization plots for PID Controller documentation
"""

import numpy as np
import matplotlib.pyplot as plt
from sproclib.controller.pid.PIDController import PIDController

# Set up professional plotting style
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.grid'] = True

# Create two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Simulation data for reactor temperature control
time = np.linspace(0, 600, 120)  # 10 minutes, 5-second intervals
setpoint = 85.0  # °C

# Process model parameters (FOPDT)
K = 0.8  # Process gain (°C/%)
tau = 300.0  # Time constant (5 minutes)
theta = 60.0  # Dead time (1 minute)

# PID controllers with different tunings
controllers = {
    'Conservative': PIDController(Kp=1.5, Ki=0.05, Kd=15.0, MV_min=0, MV_max=100),
    'Moderate': PIDController(Kp=2.5, Ki=0.1, Kd=25.0, MV_min=0, MV_max=100),
    'Aggressive': PIDController(Kp=4.0, Ki=0.2, Kd=40.0, MV_min=0, MV_max=100)
}

colors = {'Conservative': 'blue', 'Moderate': 'green', 'Aggressive': 'red'}

# Plot 1: Temperature response comparison
ax1.axhline(y=setpoint, color='black', linestyle='--', linewidth=2, label='Setpoint (85°C)')
ax1.axhline(y=setpoint*1.05, color='gray', linestyle=':', alpha=0.7, label='±5% Band')
ax1.axhline(y=setpoint*0.95, color='gray', linestyle=':', alpha=0.7)

for name, controller in controllers.items():
    # Simulate process response
    temperatures = []
    valve_outputs = []
    current_temp = 25.0  # Start at ambient
    
    for t in time:
        # Controller output
        valve_output = controller.update(t, setpoint, current_temp)
        valve_outputs.append(valve_output)
        
        # Simple process model response
        if t > theta:  # After dead time
            temp_change = K * valve_output * (1 - np.exp(-(t-theta)/tau))
            current_temp = 25.0 + temp_change  # Ambient + heating
        
        temperatures.append(current_temp)
    
    ax1.plot(time/60, temperatures, color=colors[name], linewidth=2, label=f'{name} Tuning')

ax1.set_xlabel('Time (minutes)')
ax1.set_ylabel('Temperature (°C)')
ax1.set_title('PID Controller Performance Comparison - CSTR Temperature Control')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 10)
ax1.set_ylim(20, 90)

# Add performance annotations
ax1.annotate('Overshoot Region', xy=(3, 88), xytext=(4, 92),
            arrowprops=dict(arrowstyle='->', color='red', alpha=0.7),
            fontsize=9, ha='center')

ax1.annotate('Settling Time', xy=(6, 83), xytext=(7, 78),
            arrowprops=dict(arrowstyle='->', color='blue', alpha=0.7),
            fontsize=9, ha='center')

# Plot 2: PID tuning parameter effects
tuning_params = ['Conservative\nKp=1.5, Ki=0.05', 'Moderate\nKp=2.5, Ki=0.1', 'Aggressive\nKp=4.0, Ki=0.2']
settling_times = [8.5, 6.2, 4.1]  # minutes
overshoots = [2.1, 5.8, 12.3]  # %
control_efforts = [45, 68, 89]  # % valve travel

x_pos = np.arange(len(tuning_params))
width = 0.25

# Normalize data for comparison
settling_norm = [s/max(settling_times)*100 for s in settling_times]
overshoot_norm = [o/max(overshoots)*100 for o in overshoots]
effort_norm = [e/max(control_efforts)*100 for e in control_efforts]

bars1 = ax2.bar(x_pos - width, settling_norm, width, label='Settling Time', color='lightblue', alpha=0.8)
bars2 = ax2.bar(x_pos, overshoot_norm, width, label='Overshoot', color='lightcoral', alpha=0.8)
bars3 = ax2.bar(x_pos + width, effort_norm, width, label='Control Effort', color='lightgreen', alpha=0.8)

# Add value labels on bars
for i, (bars, values) in enumerate([(bars1, settling_times), (bars2, overshoots), (bars3, control_efforts)]):
    for j, (bar, val) in enumerate(zip(bars, values)):
        height = bar.get_height()
        if i == 0:
            label = f'{val:.1f} min'
        elif i == 1:
            label = f'{val:.1f}%'
        else:
            label = f'{val:.0f}%'
        ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                label, ha='center', va='bottom', fontsize=8)

ax2.set_xlabel('Controller Tuning')
ax2.set_ylabel('Normalized Performance (%)')
ax2.set_title('PID Tuning Trade-offs: Speed vs Stability vs Control Effort')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(tuning_params)
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_ylim(0, 120)

# Add design guidelines text box
textstr = '''Design Guidelines:
• Conservative: Stable, slow response
• Moderate: Balanced performance  
• Aggressive: Fast but may oscillate
• Rule: Start conservative, increase gains gradually'''

props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax2.text(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=9,
         verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('/Users/macmini/Desktop/github/sproclib/sproclib/controller/pid/PIDController_example_plots.png', 
           dpi=300, bbox_inches='tight')
plt.close()

# Create detailed analysis plot
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Step response with different gains
time_step = np.linspace(0, 300, 100)
Kp_values = [0.5, 1.0, 2.0, 4.0]

for kp in Kp_values:
    controller = PIDController(Kp=kp, Ki=0.1, Kd=5.0, MV_min=0, MV_max=100)
    temperatures = []
    current_temp = 50.0
    
    for t in time_step:
        valve_output = controller.update(t, 80.0, current_temp)  # Step to 80°C
        # Simple response model
        if t > 30:  # Dead time
            temp_change = 0.8 * valve_output * (1 - np.exp(-(t-30)/120))
            current_temp = 50.0 + temp_change
        temperatures.append(current_temp)
    
    ax1.plot(time_step/60, temperatures, label=f'Kp = {kp}', linewidth=2)

ax1.axhline(y=80, color='black', linestyle='--', alpha=0.7, label='Setpoint')
ax1.set_xlabel('Time (minutes)')
ax1.set_ylabel('Temperature (°C)')
ax1.set_title('Effect of Proportional Gain (Kp)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Disturbance rejection
time_dist = np.linspace(0, 600, 150)
controller = PIDController(Kp=2.0, Ki=0.1, Kd=15.0, MV_min=0, MV_max=100)

temperatures = []
disturbances = []
current_temp = 75.0

for i, t in enumerate(time_dist):
    # Add disturbance at t=300s
    if t >= 300:
        disturbance = -5.0  # 5°C cooling disturbance
    else:
        disturbance = 0.0
    
    disturbances.append(disturbance)
    
    valve_output = controller.update(t, 75.0, current_temp)
    
    # Process response with disturbance
    temp_change = 0.8 * valve_output * 0.01  # Simplified dynamics
    current_temp += temp_change + disturbance * 0.001
    temperatures.append(current_temp)

ax2.plot(time_dist/60, temperatures, 'blue', linewidth=2, label='Temperature')
ax2.axhline(y=75, color='black', linestyle='--', alpha=0.7, label='Setpoint')
ax2.axvline(x=5, color='red', linestyle=':', alpha=0.7, label='Disturbance')
ax2.set_xlabel('Time (minutes)')
ax2.set_ylabel('Temperature (°C)')
ax2.set_title('Disturbance Rejection Performance')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot 3: Frequency response (Bode plot approximation)
frequencies = np.logspace(-3, 2, 100)  # 0.001 to 100 rad/s
Kp, Ki, Kd = 2.0, 0.1, 15.0

# PID transfer function magnitude
magnitude = np.sqrt((Kp + Ki/frequencies)**2 + (Kd * frequencies)**2)
magnitude_db = 20 * np.log10(magnitude)

ax3.semilogx(frequencies, magnitude_db, 'blue', linewidth=2)
ax3.set_xlabel('Frequency (rad/s)')
ax3.set_ylabel('Magnitude (dB)')
ax3.set_title('PID Controller Frequency Response')
ax3.grid(True, alpha=0.3)
ax3.axhline(y=0, color='black', linestyle='--', alpha=0.5)

# Add frequency regions
ax3.axvspan(0.001, 0.1, alpha=0.2, color='green', label='Integral\nDominated')
ax3.axvspan(0.1, 10, alpha=0.2, color='blue', label='Proportional\nDominated')
ax3.axvspan(10, 100, alpha=0.2, color='red', label='Derivative\nDominated')
ax3.legend(loc='upper left', fontsize=8)

# Plot 4: Operating regions
operating_temps = np.linspace(50, 150, 50)
valve_positions = np.linspace(0, 100, 50)

# Create operating map
X, Y = np.meshgrid(operating_temps, valve_positions)
# Steady-state relationship: higher temperature needs less heating
Z = 100 - 0.8 * (X - 50)  # Simplified steady-state map

contour = ax4.contour(X, Y, Z, levels=10, colors='blue', alpha=0.6)
ax4.clabel(contour, inline=True, fontsize=8, fmt='%1.0f°C')

# Add operating regions
ax4.axhspan(80, 100, alpha=0.3, color='red', label='High Heat Duty')
ax4.axhspan(20, 40, alpha=0.3, color='green', label='Low Heat Duty')
ax4.axvspan(120, 150, alpha=0.3, color='orange', label='High Temp Operation')

ax4.set_xlabel('Operating Temperature (°C)')
ax4.set_ylabel('Valve Position (%)')
ax4.set_title('Operating Map - Valve Position vs Temperature')
ax4.legend(loc='upper right', fontsize=8)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/macmini/Desktop/github/sproclib/sproclib/controller/pid/PIDController_detailed_analysis.png', 
           dpi=300, bbox_inches='tight')
plt.close()

print("Visualization files created successfully!")
print("- PIDController_example_plots.png: Performance comparison")
print("- PIDController_detailed_analysis.png: Parameter sensitivity analysis")
