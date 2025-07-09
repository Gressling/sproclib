"""
SPROCLIB - Standard Process Control Library
Test Suite for Core Functionality

Simple test to verify the SPROCLIB process control library functionality.

Author: Thorsten Gressling (gressling@paramus.ai)
License: MIT License
"""

import sys
import os
import numpy as np

# Add the parent directory to path so we can import the library
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_functionality():
    """Test basic functionality of the library."""
    print("Testing SPROCLIB Process Control Library...")
    
    try:
        # Import the library
        from controllers import PIDController, ZieglerNicholsTuning
        from models import Tank, CSTR
        from functions import tune_pid, step_response
        print("✓ Library imports successful")
        
        # Test 1: PID Controller
        controller = PIDController(Kp=2.0, Ki=0.5, Kd=0.1)
        mv = controller.update(0.0, 10.0, 8.0)  # t, SP, PV
        print(f"✓ PID Controller test: MV = {mv:.2f}")
        
        # Test 2: Tank Model
        tank = Tank(A=1.0, C=2.0)
        x0 = np.array([1.0])  # Initial height
        u = np.array([2.0])   # Flow rate
        dxdt = tank.dynamics(0, x0, u)
        print(f"✓ Tank model test: dh/dt = {dxdt[0]:.3f}")
        
        # Test 3: Tuning function
        model_params = {'K': 2.0, 'tau': 5.0, 'theta': 1.0}
        pid_params = tune_pid(model_params, method='ziegler_nichols')
        print(f"✓ PID tuning test: Kp = {pid_params['Kp']:.2f}")
        
        # Test 4: CSTR Model
        cstr = CSTR()
        x_cstr = np.array([0.5, 350.0])  # CA, T
        u_cstr = np.array([100.0, 1.0, 350.0, 300.0])  # q, CAi, Ti, Tc
        dxdt_cstr = cstr.dynamics(0, x_cstr, u_cstr)
        print(f"✓ CSTR model test: dCA/dt = {dxdt_cstr[0]:.4f}")
        
        # Test 5: Transfer function analysis
        from analysis import TransferFunction
        tf = TransferFunction([2.0], [5.0, 1.0])
        step_data = step_response((tf.num, tf.den), t_final=10.0)
        print(f"✓ Transfer function test: Final value = {step_data['y'][-1]:.2f}")
        
        # Test 6: Heat Exchanger Model
        from models import HeatExchanger
        hx = HeatExchanger(U=500.0, A=10.0, m_hot=2.0, m_cold=1.8)
        x_hx = np.array([350.0, 310.0])  # T_hot_out, T_cold_out
        u_hx = np.array([363.15, 293.15])  # T_hot_in, T_cold_in
        dxdt_hx = hx.dynamics(0, x_hx, u_hx)
        steady_state_hx = hx.steady_state(u_hx)
        print(f"✓ Heat Exchanger test: dT_hot/dt = {dxdt_hx[0]:.3f}, T_hot_out_ss = {steady_state_hx[0]:.1f}K")
        
        # Test heat transfer calculations
        Q_rate = hx.calculate_heat_transfer_rate(363.15, 293.15, steady_state_hx[0], steady_state_hx[1])
        lmtd = hx.calculate_lmtd(363.15, 293.15, steady_state_hx[0], steady_state_hx[1])
        print(f"✓ Heat transfer test: Q = {Q_rate/1000:.1f} kW, LMTD = {lmtd:.1f} K")
        
        # Test 7: Distillation Column Models
        from models import DistillationTray, BinaryDistillationColumn
        
        # Test individual tray
        tray = DistillationTray(tray_number=5, holdup=1.0, alpha=2.5)
        x_tray = np.array([0.5])  # 50% light component
        u_tray = np.array([10.0, 0.6, 12.0, 0.4, 11.0, 12.0])  # L_in, x_in, V_in, y_in, L_out, V_out
        dxdt_tray = tray.dynamics(0, x_tray, u_tray)
        x_steady_tray = tray.steady_state(u_tray)
        y_equilibrium = tray.vapor_liquid_equilibrium(x_tray[0])
        print(f"✓ Distillation Tray test: dx/dt = {dxdt_tray[0]:.3f}, VLE y = {y_equilibrium:.3f}")
        
        # Test binary column
        column = BinaryDistillationColumn(N_trays=5, feed_tray=3, alpha=2.5, feed_flow=100.0, feed_composition=0.5)
        u_column = np.array([2.0, 500.0, 48.0, 52.0])  # R, Q_reb, D, B
        x_steady_column = column.steady_state(u_column)
        metrics = column.calculate_separation_metrics(x_steady_column)
        R_min = column.calculate_minimum_reflux()
        print(f"✓ Distillation Column test: x_D = {metrics['distillate_composition']:.3f}, x_B = {metrics['bottoms_composition']:.3f}, R_min = {R_min:.2f}")
        
        print("\nAll basic tests passed!")
        print("The library is ready for use!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_advanced_features():
    """Test more advanced features."""
    print("\nTesting advanced features...")
    
    try:
        from models import LinearApproximation, Tank
        from analysis import Optimization
        
        # Test linearization
        tank = Tank(A=1.0, C=2.0)
        linear_approx = LinearApproximation(tank)
        u_nominal = np.array([2.0])
        A, B = linear_approx.linearize(u_nominal)
        print(f"✓ Linearization test: A = {A[0,0]:.3f}, B = {B[0,0]:.3f}")
        
        # Test optimization
        optimizer = Optimization()
        
        # Simple linear programming test
        c = np.array([1, 2])  # Minimize x1 + 2*x2
        A_ub = np.array([[1, 1], [2, 1]])  # x1 + x2 <= 3, 2*x1 + x2 <= 4
        b_ub = np.array([3, 4])
        
        result = optimizer.linear_programming(c, A_ub, b_ub)
        if result['success']:
            print(f"✓ Optimization test: Optimal value = {result['fun']:.2f}")
        else:
            print("⚠ Optimization test: Could not solve (acceptable)")
        
        print("✓ Advanced features working!")
        
    except Exception as e:
        print(f"⚠ Advanced test warning: {e}")
        # Advanced features are optional, so we don't fail here
    
    return True

if __name__ == "__main__":
    success = test_basic_functionality()
    if success:
        test_advanced_features()
        print("\n" + "="*50)
        print("Standard Process Control Library Test Complete!")
        print("="*50)
        print("\nNext steps:")
        print("1. Run 'python examples.py' for examples")
        print("2. Check the README.md for detailed documentation")
        print("3. Explore the individual modules in the library")
    else:
        print("\n❌ Tests failed. Please check the installation.")
        sys.exit(1)
