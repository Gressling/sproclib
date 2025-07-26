"""
StateSpaceController Examples - SPROCLIB Process Control Library

This module demonstrates practical applications of the StateSpaceController
for various chemical engineering processes including reactor networks,
heat exchanger systems, and distillation columns.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Optional
import sys
import os

# Add the process_control directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sproclib.controller.state_space.StateSpaceController import StateSpaceController, StateSpaceModel


def example_reactor_network():
    """
    Example: Control of a 3-reactor network with recycle streams.
    
    This example demonstrates MIMO control of interconnected CSTRs
    with first-order reactions and material recycle.
    """
    print("=" * 60)
    print("EXAMPLE 1: REACTOR NETWORK CONTROL")
    print("=" * 60)
    
    # System parameters
    k1, k2, k3 = 0.12, 0.18, 0.25  # Reaction rate constants [1/min]
    V1, V2, V3 = 2.0, 3.0, 1.5     # Reactor volumes [L]
    F12, F23 = 0.8, 0.6            # Interconnection flows [L/min]
    F31 = 0.3                       # Recycle flow [L/min]
    
    # State-space matrices
    # States: [CA1, CA2, CA3] - concentrations in each reactor
    # Inputs: [F_feed1, F_feed2] - feed flows to reactors 1 and 2
    A = np.array([
        [-(k1 + F12/V1) + F31/V1, 0, F31/V1],
        [F12/V2, -(k2 + F23/V2), 0],
        [0, F23/V3, -(k3 + F31/V3)]
    ])
    
    B = np.array([
        [1/V1, 0],      # Feed to reactor 1
        [0, 1/V2],      # Feed to reactor 2  
        [0, 0]          # No direct feed to reactor 3
    ])
    
    C = np.eye(3)  # All concentrations measured
    
    # Create state-space model
    model = StateSpaceModel(
        A=A, B=B, C=C,
        state_names=['CA_R1', 'CA_R2', 'CA_R3'],
        input_names=['Feed_R1', 'Feed_R2'],
        output_names=['Analyzer_R1', 'Analyzer_R2', 'Analyzer_R3']
    )
    
    print(f"System properties:")
    print(f"- States: {model.n_states}, Inputs: {model.n_inputs}, Outputs: {model.n_outputs}")
    print(f"- Controllable: {model.is_controllable()}")
    print(f"- Observable: {model.is_observable()}")
    
    # Create controller
    controller = StateSpaceController(model)
    
    # Design LQR controller
    Q = np.diag([50.0, 30.0, 20.0])  # State penalties (higher for upstream reactors)
    R = np.diag([1.0, 1.0])          # Input penalties
    K = controller.design_lqr_controller(Q, R)
    
    # Calculate closed-loop poles
    A_cl = model.A - model.B @ K
    poles = np.linalg.eigvals(A_cl)
    
    print(f"\nLQR Controller Design:")
    print(f"- Gain matrix K:\n{K}")
    print(f"- Closed-loop poles: {poles}")
    
    # Simulate setpoint tracking
    x0 = np.array([0.9, 0.7, 0.5])      # Initial concentrations [mol/L]
    setpoint = np.array([0.6, 0.4, 0.2]) # Target concentrations [mol/L]
    
    time_points = np.linspace(0, 30, 300)
    states, inputs, outputs = controller.simulate_response(
        x0=x0, setpoint=setpoint, time_points=time_points, K=K
    )
    
    # Performance metrics
    settling_time = controller.calculate_settling_time(states, setpoint)
    steady_state_error = np.abs(states[-1, :] - setpoint)
    
    print(f"\nPerformance Metrics:")
    print(f"- Settling time: {settling_time:.2f} min")
    print(f"- Steady-state error: {steady_state_error}")
    
    return model, controller, time_points, states, inputs, outputs


def example_heat_exchanger_network():
    """
    Example: Control of a heat exchanger network for temperature regulation.
    
    This example shows temperature control in a multi-stream heat integration
    network with thermal coupling between streams.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: HEAT EXCHANGER NETWORK CONTROL")
    print("=" * 60)
    
    # System parameters
    m1, m2, m3 = 100, 150, 80       # Mass flow rates [kg/h]
    cp1, cp2, cp3 = 2.1, 2.3, 2.0   # Heat capacities [kJ/kg·K]
    UA12, UA23 = 50, 40             # Heat transfer coefficients [kJ/h·K]
    V1, V2, V3 = 0.5, 0.8, 0.4      # Heat exchanger volumes [m³]
    
    # State-space matrices for temperature dynamics
    # States: [T1, T2, T3] - temperatures of each stream
    # Inputs: [Q_heater1, Q_cooler2] - heating/cooling duties
    A = np.array([
        [-(UA12)/(m1*cp1*V1), UA12/(m1*cp1*V1), 0],
        [UA12/(m2*cp2*V2), -(UA12+UA23)/(m2*cp2*V2), UA23/(m2*cp2*V2)],
        [0, UA23/(m3*cp3*V3), -UA23/(m3*cp3*V3)]
    ])
    
    B = np.array([
        [1/(m1*cp1*V1), 0],           # Heater on stream 1
        [0, -1/(m2*cp2*V2)],          # Cooler on stream 2
        [0, 0]                        # No direct heating on stream 3
    ])
    
    C = np.eye(3)  # Temperature sensors on all streams
    
    # Create model
    model = StateSpaceModel(
        A=A, B=B, C=C,
        state_names=['T_Stream1', 'T_Stream2', 'T_Stream3'],
        input_names=['Heater_Duty', 'Cooler_Duty'],
        output_names=['TT_Stream1', 'TT_Stream2', 'TT_Stream3']
    )
    
    controller = StateSpaceController(model)
    
    # Design controller with pole placement
    desired_poles = [-0.5, -0.8, -1.2]  # Specify desired response speeds
    K = controller.design_pole_placement_controller(desired_poles)
    
    print(f"Pole Placement Controller:")
    print(f"- Desired poles: {desired_poles}")
    print(f"- Gain matrix K:\n{K}")
    
    # Simulate temperature disturbance rejection
    x0 = np.array([80.0, 60.0, 40.0])    # Initial temperatures [°C]
    setpoint = np.array([75.0, 65.0, 45.0])  # Target temperatures [°C]
    
    time_points = np.linspace(0, 20, 200)
    states, inputs, outputs = controller.simulate_response(
        x0=x0, setpoint=setpoint, time_points=time_points, K=K
    )
    
    print(f"\nTemperature Control Results:")
    print(f"- Initial temperatures: {x0} °C")
    print(f"- Final temperatures: {states[-1, :]} °C")
    print(f"- Target temperatures: {setpoint} °C")
    
    return model, controller, time_points, states, inputs


def example_distillation_column():
    """
    Example: State-space control of a distillation column.
    
    This example demonstrates MIMO control of a binary distillation column
    with tray temperature control using reflux and reboiler duty.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: DISTILLATION COLUMN CONTROL")
    print("=" * 60)
    
    # System parameters for 5-tray column
    n_trays = 5
    alpha = 2.5       # Relative volatility
    M = 10.0          # Molar holdup per tray [kmol]
    
    # Simplified linear model for composition dynamics
    # States: [x1, x2, x3, x4, x5] - mole fractions on each tray
    # Inputs: [R, Qr] - reflux ratio and reboiler duty
    
    # Vapor-liquid equilibrium and material balance effects
    A = np.array([
        [-0.5, 0.3, 0, 0, 0],
        [0.2, -0.7, 0.3, 0, 0],
        [0, 0.2, -0.7, 0.3, 0],
        [0, 0, 0.2, -0.7, 0.3],
        [0, 0, 0, 0.2, -0.5]
    ])
    
    B = np.array([
        [0.8, 0],      # Reflux affects top tray most
        [0.3, 0],
        [0.1, 0],
        [0, 0.1],
        [0, 0.8]       # Reboiler affects bottom tray most
    ])
    
    C = np.array([
        [1, 0, 0, 0, 0],    # Composition analyzer on tray 1
        [0, 0, 1, 0, 0],    # Composition analyzer on tray 3
        [0, 0, 0, 0, 1]     # Composition analyzer on tray 5
    ])
    
    # Create model
    model = StateSpaceModel(
        A=A, B=B, C=C,
        state_names=[f'x_Tray{i+1}' for i in range(n_trays)],
        input_names=['Reflux_Ratio', 'Reboiler_Duty'],
        output_names=['AC_Tray1', 'AC_Tray3', 'AC_Tray5']
    )
    
    controller = StateSpaceController(model)
    
    # Design LQR controller
    Q = np.diag([100, 10, 1, 10, 100])  # Higher penalties on end trays
    R = np.diag([1, 5])                 # Penalty on manipulated variables
    K, _, poles = controller.design_lqr(Q, R)
    
    # Design observer for unmeasured trays
    observer_poles = [-2, -2.5, -3, -3.5, -4]  # Faster than controller
    L = controller.design_observer(observer_poles)
    
    print(f"Distillation Column Control Design:")
    print(f"- LQR gain matrix K:\n{K}")
    print(f"- Observer gain matrix L:\n{L}")
    print(f"- Closed-loop poles: {poles}")
    
    # Simulate feed composition disturbance
    x0 = np.array([0.95, 0.85, 0.5, 0.15, 0.05])    # Initial compositions
    setpoint = np.array([0.98, 0.90, 0.5, 0.10, 0.02])  # Target compositions
    
    time_points = np.linspace(0, 50, 500)
    states, inputs, outputs = controller.simulate_response(
        x0=x0, setpoint=setpoint, time_points=time_points, K=K
    )
    
    print(f"\nDistillation Control Results:")
    print(f"- Distillate purity (tray 1): {states[-1, 0]:.4f}")
    print(f"- Bottoms purity (tray 5): {1-states[-1, 4]:.4f}")
    
    return model, controller, time_points, states, inputs


def example_observer_based_control():
    """
    Example: Observer-based state feedback control.
    
    This example shows how to implement observer-based control when
    not all states are measurable.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: OBSERVER-BASED CONTROL")
    print("=" * 60)
    
    # Create a system where only some states are measurable
    A = np.array([
        [-0.5, 0.2, 0.1],
        [0.1, -0.8, 0.3],
        [0.0, 0.1, -0.6]
    ])
    
    B = np.array([
        [1.0, 0.0],
        [0.5, 0.5],
        [0.0, 1.0]
    ])
    
    C = np.array([
        [1.0, 0.0, 0.0],  # Only first and third states measured
        [0.0, 0.0, 1.0]
    ])
    
    model = StateSpaceModel(
        A=A, B=B, C=C,
        state_names=['x1', 'x2_unmeasured', 'x3'],
        input_names=['u1', 'u2'],
        output_names=['y1', 'y3']
    )
    
    controller = StateSpaceController(model)
    
    # Design state feedback controller
    Q = np.eye(3)
    R = np.eye(2)
    K, _, _ = controller.design_lqr(Q, R)
    
    # Design observer for state estimation
    desired_observer_poles = [-2.0, -2.5, -3.0]  # Faster than controller
    L = controller.design_observer(desired_observer_poles)
    
    print(f"Observer-Based Control:")
    print(f"- Only {model.n_outputs} of {model.n_states} states are measured")
    print(f"- State feedback gain K:\n{K}")
    print(f"- Observer gain L:\n{L}")
    
    # Simulate with observer
    x0 = np.array([1.0, 0.5, -0.5])  # True initial state
    x0_est = np.array([0.8, 0.0, -0.3])  # Initial state estimate (with error)
    setpoint = np.array([0.0, 0.0, 0.0])
    
    time_points = np.linspace(0, 15, 150)
    
    # Simulate observer-based control
    states_true, states_est, inputs, outputs = controller.simulate_observer_control(
        x0_true=x0, x0_est=x0_est, setpoint=setpoint,
        time_points=time_points, K=K, L=L
    )
    
    # Calculate estimation error
    estimation_error = np.abs(states_true - states_est)
    final_error = estimation_error[-1, :]
    
    print(f"\nObserver Performance:")
    print(f"- Initial estimation error: {np.abs(x0 - x0_est)}")
    print(f"- Final estimation error: {final_error}")
    print(f"- Observer convergence: {'Good' if np.max(final_error) < 0.1 else 'Poor'}")
    
    return model, controller, time_points, states_true, states_est, inputs


def plot_all_examples():
    """Generate plots for all examples."""
    print("\n" + "=" * 60)
    print("GENERATING EXAMPLE PLOTS")
    print("=" * 60)
    
    # Create figure with subplots for all examples
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Example 1: Reactor Network
    try:
        _, _, time1, states1, inputs1, _ = example_reactor_network()
        ax = axes[0, 0]
        ax.plot(time1, states1[:, 0], 'b-', label='CA_R1', linewidth=2)
        ax.plot(time1, states1[:, 1], 'r-', label='CA_R2', linewidth=2)
        ax.plot(time1, states1[:, 2], 'g-', label='CA_R3', linewidth=2)
        ax.axhline(y=0.6, color='b', linestyle='--', alpha=0.7)
        ax.axhline(y=0.4, color='r', linestyle='--', alpha=0.7)
        ax.axhline(y=0.2, color='g', linestyle='--', alpha=0.7)
        ax.set_title('Reactor Network Control')
        ax.set_ylabel('Concentration (mol/L)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    except Exception as e:
        print(f"Error plotting Example 1: {e}")
    
    # Example 2: Heat Exchanger Network
    try:
        _, _, time2, states2, inputs2 = example_heat_exchanger_network()
        ax = axes[0, 1]
        ax.plot(time2, states2[:, 0], 'r-', label='T_Stream1', linewidth=2)
        ax.plot(time2, states2[:, 1], 'b-', label='T_Stream2', linewidth=2)
        ax.plot(time2, states2[:, 2], 'g-', label='T_Stream3', linewidth=2)
        ax.axhline(y=75, color='r', linestyle='--', alpha=0.7)
        ax.axhline(y=65, color='b', linestyle='--', alpha=0.7)
        ax.axhline(y=45, color='g', linestyle='--', alpha=0.7)
        ax.set_title('Heat Exchanger Network Control')
        ax.set_ylabel('Temperature (°C)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    except Exception as e:
        print(f"Error plotting Example 2: {e}")
    
    # Example 3: Distillation Column
    try:
        _, _, time3, states3, inputs3 = example_distillation_column()
        ax = axes[1, 0]
        ax.plot(time3, states3[:, 0], 'b-', label='x_Tray1', linewidth=2)
        ax.plot(time3, states3[:, 2], 'r-', label='x_Tray3', linewidth=2)
        ax.plot(time3, states3[:, 4], 'g-', label='x_Tray5', linewidth=2)
        ax.set_title('Distillation Column Control')
        ax.set_ylabel('Mole Fraction')
        ax.set_xlabel('Time (min)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    except Exception as e:
        print(f"Error plotting Example 3: {e}")
    
    # Example 4: Observer-Based Control
    try:
        _, _, time4, states_true, states_est, inputs4 = example_observer_based_control()
        ax = axes[1, 1]
        ax.plot(time4, states_true[:, 1], 'b-', label='True x2', linewidth=2)
        ax.plot(time4, states_est[:, 1], 'r--', label='Estimated x2', linewidth=2)
        ax.plot(time4, np.abs(states_true[:, 1] - states_est[:, 1]), 'g:', 
                label='Estimation Error', linewidth=2)
        ax.set_title('Observer-Based Control')
        ax.set_ylabel('State Value')
        ax.set_xlabel('Time (min)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    except Exception as e:
        print(f"Error plotting Example 4: {e}")
    
    plt.tight_layout()
    plt.savefig('statespace_controller_examples.png', dpi=300, bbox_inches='tight')
    print("✓ Example plots saved as 'statespace_controller_examples.png'")
    
    return fig


def run_all_examples():
    """Run all StateSpaceController examples."""
    print("STATE-SPACE CONTROLLER EXAMPLES")
    print("Advanced MIMO control for chemical processes")
    print()
    
    try:
        # Run all examples
        example_reactor_network()
        example_heat_exchanger_network()
        example_distillation_column()
        example_observer_based_control()
        
        print("\n" + "=" * 60)
        print("✓ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Example failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run all examples
    success = run_all_examples()
    
    if success:
        # Generate plots if examples complete successfully
        try:
            plot_all_examples()
        except ImportError:
            print("Note: matplotlib not available for plotting")
        except Exception as e:
            print(f"Note: plotting failed with {e}")
    
    exit(0 if success else 1)
