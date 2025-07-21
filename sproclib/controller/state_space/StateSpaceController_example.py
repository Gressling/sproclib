"""
Industrial Example: CSTR Network Control
Two-reactor system with recycle stream and heat integration
"""

import numpy as np
from sproclib.controller.state_space.StateSpaceController import StateSpaceController, StateSpaceModel

print("CSTR Network State-Space Control")
print("=" * 40)
print("System: Two CSTRs in series with recycle")
print("States: [CA1, T1, CA2, T2] - concentrations and temperatures")
print("Inputs: [q1, Tc1, Tc2] - feed rate, coolant temperatures") 
print("Outputs: [CA2, T2] - product concentration and temperature")
print()

# Process conditions (typical industrial scale)
reactor1_volume = 5.0  # m³
reactor2_volume = 8.0  # m³
feed_concentration = 2.0  # kmol/m³
target_concentration = 0.5  # kmol/m³
target_temperature = 350.0  # K

print("Process Conditions")
print("-" * 18)
print(f"Reactor 1 Volume: {reactor1_volume} m³")
print(f"Reactor 2 Volume: {reactor2_volume} m³")
print(f"Feed Concentration: {feed_concentration} kmol/m³")
print(f"Target Product Concentration: {target_concentration} kmol/m³")
print(f"Target Temperature: {target_temperature} K")
print()

# State-space model matrices for reactor network
# States: [CA1, T1, CA2, T2]
A = np.array([
    [-0.5, -0.02,  0.0,  0.0 ],  # dCA1/dt
    [ 0.0, -0.3,   0.0,  0.0 ],  # dT1/dt  
    [ 0.25, 0.0,  -0.4, -0.01],  # dCA2/dt
    [ 0.0,  0.15,  0.0, -0.25]   # dT2/dt
])

# Inputs: [q1, Tc1, Tc2]
B = np.array([
    [ 0.5,  0.0,  0.0],  # q1 affects CA1
    [ 0.0,  0.2,  0.0],  # Tc1 affects T1
    [ 0.0,  0.0,  0.0],  # 
    [ 0.0,  0.0,  0.15]  # Tc2 affects T2
])

# Outputs: [CA2, T2]  
C = np.array([
    [0, 0, 1, 0],  # CA2 measurement
    [0, 0, 0, 1]   # T2 measurement
])

D = np.zeros((2, 3))

print("State-Space Model")
print("-" * 17)
print("A matrix (state dynamics):")
print(A)
print("\nB matrix (input coupling):")
print(B)
print("\nC matrix (output coupling):")
print(C)
print()

# Create state-space model
model = StateSpaceModel(
    A, B, C, D,
    state_names=['CA1', 'T1', 'CA2', 'T2'],
    input_names=['q1', 'Tc1', 'Tc2'],
    output_names=['CA2', 'T2'],
    name="ReactorNetwork"
)

# System analysis
print("System Properties")
print("-" * 17)
print(f"Number of states: {model.n_states}")
print(f"Number of inputs: {model.n_inputs}")
print(f"Number of outputs: {model.n_outputs}")
print(f"Controllable: {model.is_controllable()}")
print(f"Observable: {model.is_observable()}")
print(f"Stable: {model.is_stable()}")

# Eigenvalues (poles)
poles = model.poles()
print(f"System poles: {poles}")
print()

# Create state-space controller
controller = StateSpaceController(model, name="ReactorNetworkController")

# LQR design
Q = np.diag([10.0, 1.0, 100.0, 1.0])  # State weights
R = np.diag([1.0, 0.1, 0.1])          # Input weights

print("LQR Design")
print("-" * 10)
print("Q matrix (state weights):")
print(Q)
print("\nR matrix (input weights):")
print(R)

# Design LQR controller
K_lqr, S, poles_cl = controller.design_lqr_controller(Q, R)

print(f"\nLQR gain matrix K:")
print(K_lqr)
print(f"Closed-loop poles: {poles_cl}")
print()

# Observer design
L_poles = np.array([-2.0, -2.5, -3.0, -3.5])  # Faster than controller
L_observer = controller.design_observer(L_poles)

print("Observer Design")
print("-" * 15)
print(f"Observer poles: {L_poles}")
print(f"Observer gain matrix L:")
print(L_observer)
print()

# Simulation test
initial_states = np.array([1.5, 340.0, 0.8, 345.0])  # Initial conditions
setpoints = np.array([target_concentration, target_temperature])

print("Simulation Test")
print("-" * 15)
print(f"Initial states: {initial_states}")
print(f"Setpoints: {setpoints}")

# Time simulation
time_points = np.linspace(0, 300, 31)  # 5 minutes, 10-second intervals
dt = 10.0  # seconds

states_history = []
outputs_history = []
inputs_history = []

current_states = initial_states.copy()

print("\nTime(min)  CA1     T1      CA2     T2      q1      Tc1     Tc2")
print("-" * 70)

for i, t in enumerate(time_points):
    # Measure outputs (with small noise)
    measurement_noise = np.random.normal(0, 0.01, 2)
    outputs = C @ current_states + measurement_noise
    
    # Controller update
    inputs = controller.update(t, setpoints, outputs)
    
    # Store history
    states_history.append(current_states.copy())
    outputs_history.append(outputs.copy())
    inputs_history.append(inputs.copy())
    
    # Print selected time points
    if i % 5 == 0:
        print(f"{t/60:7.1f}  {current_states[0]:6.2f}  {current_states[1]:6.1f}  "
              f"{current_states[2]:6.2f}  {current_states[3]:6.1f}  "
              f"{inputs[0]:6.2f}  {inputs[1]:6.1f}  {inputs[2]:6.1f}")
    
    # Process simulation (simple integration)
    if i < len(time_points) - 1:
        state_derivatives = A @ current_states + B @ inputs
        current_states += state_derivatives * dt

print()

# Performance analysis
final_outputs = outputs_history[-1]
errors = setpoints - final_outputs
settling_indices = []

for i, output_history in enumerate(np.array(outputs_history).T):
    # Find settling time (within 2% of setpoint)
    error_history = np.abs(output_history - setpoints[i])
    settled_indices = np.where(error_history < 0.02 * setpoints[i])[0]
    if len(settled_indices) > 0:
        settling_indices.append(settled_indices[0])
    else:
        settling_indices.append(len(time_points))

print("Performance Analysis")
print("-" * 20)
print(f"Final concentration error: {errors[0]:.4f} kmol/m³")
print(f"Final temperature error: {errors[1]:.2f} K")
print(f"CA2 settling time: {time_points[settling_indices[0]]/60:.1f} minutes")
print(f"T2 settling time: {time_points[settling_indices[1]]/60:.1f} minutes")
print()

# Control effort analysis
input_array = np.array(inputs_history)
max_inputs = np.max(input_array, axis=0)
min_inputs = np.min(input_array, axis=0)
input_ranges = max_inputs - min_inputs

print("Control Effort")
print("-" * 14)
print(f"Feed rate range: {min_inputs[0]:.2f} - {max_inputs[0]:.2f} m³/h")
print(f"Coolant T1 range: {min_inputs[1]:.1f} - {max_inputs[1]:.1f} K")
print(f"Coolant T2 range: {min_inputs[2]:.1f} - {max_inputs[2]:.1f} K")
print()

# Economic analysis
average_feed_rate = np.mean(input_array[:, 0])
coolant_usage_1 = np.mean(np.abs(input_array[:, 1] - 300))  # Deviation from ambient
coolant_usage_2 = np.mean(np.abs(input_array[:, 2] - 300))

feed_cost = average_feed_rate * 24 * 50  # $/day at $50/m³
cooling_cost_1 = coolant_usage_1 * 0.5 * 24  # $/day
cooling_cost_2 = coolant_usage_2 * 0.5 * 24  # $/day
total_daily_cost = feed_cost + cooling_cost_1 + cooling_cost_2

print("Economic Impact")
print("-" * 15)
print(f"Average feed rate: {average_feed_rate:.2f} m³/h")
print(f"Daily feed cost: ${feed_cost:.0f}")
print(f"Daily cooling cost (R1): ${cooling_cost_1:.0f}")
print(f"Daily cooling cost (R2): ${cooling_cost_2:.0f}")
print(f"Total daily operating cost: ${total_daily_cost:.0f}")
print()

# Comparison with SISO control
print("Advantages over SISO Control")
print("-" * 29)
print("- Simultaneous control of multiple outputs")
print("- Optimal use of all available inputs")
print("- Systematic handling of process interactions")
print("- Predictable closed-loop performance")
print("- Reduced control loop interactions")

print("\nIndustrial Applications")
print("-" * 23)
print("- Multi-component distillation columns")
print("- Reactor networks with recycle streams")
print("- Heat exchanger networks")
print("- Batch crystallization processes")
print("- Multi-stage separation systems")
