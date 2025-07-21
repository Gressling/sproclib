"""
Industrial Example: CSTR Network Control
Simplified state-space control demonstration
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

# LQR design weights
Q = np.diag([10.0, 1.0, 100.0, 1.0])  # State weights
R = np.diag([1.0, 0.1, 0.1])          # Input weights

print("LQR Design")
print("-" * 10)
print("Q matrix (state weights):")
print(Q)
print("\nR matrix (input weights):")
print(R)
print()

# Design controller (simplified approach)
try:
    K_lqr, S, poles_cl = controller.design_lqr_controller(Q, R)
    print(f"LQR gain matrix K:")
    print(K_lqr)
    print(f"Closed-loop poles: {poles_cl}")
except Exception as e:
    print(f"LQR design note: {e}")
    # Use manual gain matrix for demonstration
    K_lqr = np.array([
        [2.5, 0.1, 8.0, 0.2],  # Control input 1
        [0.5, 4.0, 0.3, 0.1],  # Control input 2  
        [0.2, 0.1, 1.5, 6.0]   # Control input 3
    ])
    print(f"Example gain matrix K:")
    print(K_lqr)

print()

# Performance analysis
print("Performance Characteristics")
print("-" * 27)
print("Advantages of State-Space Control:")
print("- Systematic design procedures (LQR, pole placement)")
print("- Optimal performance with explicit objectives")
print("- Natural MIMO capability")
print("- Guaranteed stability margins")
print("- Internal state insight")
print()

print("Typical Applications:")
print("- Multi-component distillation columns")
print("- Reactor networks with recycle")
print("- Heat exchanger networks")
print("- Batch crystallization processes")
print("- Multi-stage separation systems")
print()

print("Design Guidelines:")
print("- Q matrix: Weight important states heavily")
print("- R matrix: Balance control effort costs")
print("- Observer: Design 3-5x faster than controller")
print("- Validation: Check controllability/observability")
print()

print("Economic Impact:")
print("- 10-20% improvement in product quality")
print("- 5-15% reduction in energy consumption")
print("- 20-40% reduction in process variability")
print("- Decreased operator workload")
print()

print("Implementation Considerations:")
print("- Requires accurate process model")
print("- Higher computational requirements")
print("- More complex commissioning")
print("- Operator training requirements")
print("- Suitable for well-instrumented processes")
