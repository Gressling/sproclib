"""
Test Suite for StateSpaceController - SPROCLIB Process Control Library

This module provides tests for the StateSpaceController implementation,
including LQR control, pole placement, observer design, and MIMO system control.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
import sys
import os

# Add the process_control directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sproclib.controller.state_space.StateSpaceController import StateSpaceController, StateSpaceModel


def test_state_space_model():
    """Test StateSpaceModel creation and basic functionality."""
    print("Testing StateSpaceModel...")
    
    # Create a simple 2x2 system (two tank system)
    A = np.array([[-0.1, 0.05],
                  [0.05, -0.15]])
    B = np.array([[1.0, 0.0],
                  [0.0, 1.0]])
    C = np.array([[1.0, 0.0],
                  [0.0, 1.0]])
    
    model = StateSpaceModel(
        A=A, B=B, C=C,
        state_names=['Tank1_Level', 'Tank2_Level'],
        input_names=['Pump1_Flow', 'Pump2_Flow'],
        output_names=['Level1_Sensor', 'Level2_Sensor']
    )
    
    # Test model properties
    assert model.n_states == 2
    assert model.n_inputs == 2
    assert model.n_outputs == 2
    assert model.is_controllable()
    assert model.is_observable()
    
    print("✓ StateSpaceModel basic functionality tests passed")
    return model


def test_lqr_controller():
    """Test LQR controller design and performance."""
    print("\nTesting LQR Controller...")
    
    # Create model
    model = test_state_space_model()
    
    # Create controller
    controller = StateSpaceController(model)
    
    # Design LQR controller
    Q = np.eye(2)  # State penalty
    R = np.eye(2)  # Input penalty
    K = controller.design_lqr_controller(Q, R)
    
    # Check dimensions
    assert K.shape == (2, 2)
    
    # Calculate closed-loop poles
    A_cl = model.A - model.B @ K
    poles = np.linalg.eigvals(A_cl)
    
    # Check stability (all poles should have negative real parts)
    assert all(np.real(pole) < 0 for pole in poles)
    
    print(f"✓ LQR gain matrix K:\n{K}")
    print(f"✓ Closed-loop poles: {poles}")
    print("✓ LQR controller design tests passed")
    
    return controller, K


def test_pole_placement():
    """Test pole placement controller design."""
    print("\nTesting Pole Placement Controller...")
    
    # Create model
    model = test_state_space_model()
    controller = StateSpaceController(model)
    
    # Specify desired poles
    desired_poles = [-0.5, -0.8]
    K = controller.design_pole_placement_controller(desired_poles)
    
    # Verify pole placement
    A_cl = model.A - model.B @ K
    actual_poles = np.linalg.eigvals(A_cl)
    
    # Check if poles are approximately correct
    np.testing.assert_allclose(np.sort(actual_poles), np.sort(desired_poles), rtol=1e-6)
    
    print(f"✓ Desired poles: {desired_poles}")
    print(f"✓ Actual poles: {actual_poles}")
    print("✓ Pole placement tests passed")
    
    return K


def test_observer_design():
    """Test observer design functionality."""
    print("\nTesting Observer Design...")
    
    # Create model
    model = test_state_space_model()
    controller = StateSpaceController(model)
    
    # Design observer
    desired_observer_poles = [-1.0, -1.2]
    L = controller.design_observer(desired_observer_poles)
    
    # Verify observer pole placement
    A_obs = model.A - L @ model.C
    actual_poles = np.linalg.eigvals(A_obs)
    
    # Check if poles are approximately correct
    np.testing.assert_allclose(np.sort(actual_poles), np.sort(desired_observer_poles), rtol=1e-6)
    
    print(f"✓ Observer gain matrix L:\n{L}")
    print(f"✓ Observer poles: {actual_poles}")
    print("✓ Observer design tests passed")
    
    return L


def test_mimo_system_simulation():
    """Test MIMO system control simulation."""
    print("\nTesting MIMO System Simulation...")
    
    # Create a more complex 3x2 system (3 states, 2 inputs)
    A = np.array([[-0.1, 0.05, 0.0],
                  [0.05, -0.15, 0.1],
                  [0.0, 0.1, -0.2]])
    B = np.array([[1.0, 0.0],
                  [0.5, 0.5],
                  [0.0, 1.0]])
    C = np.array([[1.0, 0.0, 0.0],
                  [0.0, 1.0, 0.0],
                  [0.0, 0.0, 1.0]])
    
    model = StateSpaceModel(A=A, B=B, C=C)
    controller = StateSpaceController(model)
    
    # Design LQR controller
    Q = np.diag([1.0, 1.0, 1.0])
    R = np.diag([0.1, 0.1])
    K = controller.design_lqr_controller(Q, R)
    
    # Simulate system response
    x0 = np.array([1.0, 0.5, 0.2])  # Initial state
    setpoint = np.array([0.0, 0.0, 0.0])  # Target state
    
    time_points = np.linspace(0, 10, 100)
    
    # Simple forward Euler simulation
    x = x0.copy()
    dt = time_points[1] - time_points[0]
    states = np.zeros((len(time_points), model.n_states))
    inputs = np.zeros((len(time_points), model.n_inputs))
    outputs = np.zeros((len(time_points), model.n_outputs))
    
    for i, t in enumerate(time_points):
        # Store current state
        states[i, :] = x
        outputs[i, :] = model.C @ x
        
        # Calculate control input (state feedback)
        u = -K @ (x - setpoint)
        inputs[i, :] = u
        
        # Simple Euler integration
        if i < len(time_points) - 1:
            x_dot = model.A @ x + model.B @ u
            x = x + dt * x_dot
    
    # Check simulation results
    assert states.shape == (100, 3)
    assert inputs.shape == (100, 2)
    assert outputs.shape == (100, 3)
    
    # Check final state convergence (should be close to setpoint)
    final_state = states[-1, :]
    np.testing.assert_allclose(final_state, setpoint, atol=0.1)
    
    print(f"✓ Initial state: {x0}")
    print(f"✓ Final state: {final_state}")
    print(f"✓ Setpoint: {setpoint}")
    print("✓ MIMO simulation tests passed")
    
    return time_points, states, inputs, outputs


def test_reactor_network_example():
    """Test state-space control for a reactor network."""
    print("\nTesting Reactor Network Example...")
    
    # 3-reactor network with interconnections
    # States: [CA1, CA2, CA3] (concentrations)
    # Inputs: [F1, F2] (feed flows to reactors 1 and 2)
    
    # System matrices for reactor network
    k1, k2, k3 = 0.1, 0.15, 0.2  # Reaction rate constants
    V1, V2, V3 = 1.0, 1.5, 2.0   # Reactor volumes
    F12, F23 = 0.5, 0.3          # Interconnection flows
    
    A = np.array([
        [-(k1 + F12/V1), 0, 0],
        [F12/V2, -(k2 + F23/V2), 0],
        [0, F23/V3, -k3]
    ])
    
    B = np.array([
        [1/V1, 0],
        [0, 1/V2],
        [0, 0]
    ])
    
    C = np.eye(3)  # All concentrations measured
    
    model = StateSpaceModel(
        A=A, B=B, C=C,
        state_names=['CA1', 'CA2', 'CA3'],
        input_names=['Feed_F1', 'Feed_F2'],
        output_names=['Sensor_CA1', 'Sensor_CA2', 'Sensor_CA3']
    )
    
    controller = StateSpaceController(model)
    
    # Design LQR controller for concentration regulation
    Q = np.diag([10.0, 10.0, 5.0])  # Higher penalty on CA1, CA2
    R = np.diag([1.0, 1.0])         # Input penalty
    K = controller.design_lqr_controller(Q, R)
    
    # Calculate closed-loop poles
    A_cl = model.A - model.B @ K
    poles = np.linalg.eigvals(A_cl)
    
    # Simulate disturbance rejection
    x0 = np.array([0.8, 0.6, 0.4])  # Initial concentrations
    setpoint = np.array([0.5, 0.3, 0.2])  # Target concentrations
    
    time_points = np.linspace(0, 20, 200)
    
    # Simple simulation
    x = x0.copy()
    dt = time_points[1] - time_points[0]
    states = np.zeros((len(time_points), model.n_states))
    inputs = np.zeros((len(time_points), model.n_inputs))
    
    for i, t in enumerate(time_points):
        states[i, :] = x
        u = -K @ (x - setpoint)
        inputs[i, :] = u
        if i < len(time_points) - 1:
            x_dot = model.A @ x + model.B @ u
            x = x + dt * x_dot
    
    # Check system controllability and observability
    assert model.is_controllable()
    assert model.is_observable()
    
    # Check stability
    assert all(np.real(pole) < 0 for pole in poles)
    
    print(f"✓ System is controllable: {model.is_controllable()}")
    print(f"✓ System is observable: {model.is_observable()}")
    print(f"✓ Closed-loop poles: {poles}")
    print("✓ Reactor network example tests passed")
    
    return model, controller, time_points, states, inputs


def run_all_tests():
    """Run all StateSpaceController tests."""
    print("=" * 60)
    print("STATESPACE CONTROLLER TEST SUITE")
    print("=" * 60)
    
    try:
        # Run individual tests
        test_state_space_model()
        test_lqr_controller()
        test_pole_placement()
        test_observer_design()
        test_mimo_system_simulation()
        test_reactor_network_example()
        
        print("\n" + "=" * 60)
        print("✓ ALL STATESPACE CONTROLLER TESTS PASSED!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def plot_simulation_results():
    """Create plots showing controller performance."""
    print("\nGenerating simulation plots...")
    
    # Run reactor network simulation
    model, controller, time, states, inputs = test_reactor_network_example()
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Plot states (concentrations)
    ax1.plot(time, states[:, 0], 'b-', label='CA1', linewidth=2)
    ax1.plot(time, states[:, 1], 'r-', label='CA2', linewidth=2)
    ax1.plot(time, states[:, 2], 'g-', label='CA3', linewidth=2)
    ax1.axhline(y=0.5, color='b', linestyle='--', alpha=0.7, label='Setpoint CA1')
    ax1.axhline(y=0.3, color='r', linestyle='--', alpha=0.7, label='Setpoint CA2')
    ax1.axhline(y=0.2, color='g', linestyle='--', alpha=0.7, label='Setpoint CA3')
    ax1.set_xlabel('Time (min)')
    ax1.set_ylabel('Concentration (mol/L)')
    ax1.set_title('State-Space Control: Reactor Network Concentrations')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot inputs (feed flows)
    ax2.plot(time, inputs[:, 0], 'b-', label='Feed F1', linewidth=2)
    ax2.plot(time, inputs[:, 1], 'r-', label='Feed F2', linewidth=2)
    ax2.set_xlabel('Time (min)')
    ax2.set_ylabel('Feed Flow (L/min)')
    ax2.set_title('State-Space Control: Manipulated Variables')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('statespace_controller_performance.png', dpi=300, bbox_inches='tight')
    print("✓ Simulation plots saved as 'statespace_controller_performance.png'")
    
    return fig


if __name__ == "__main__":
    # Run all tests
    success = run_all_tests()
    
    if success:
        # Generate plots if tests pass
        try:
            plot_simulation_results()
        except ImportError:
            print("Note: matplotlib not available for plotting")
        except Exception as e:
            print(f"Note: plotting failed with {e}")
    
    exit(0 if success else 1)
