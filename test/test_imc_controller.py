#!/usr/bin/env python3
"""
Test script for IMC Controller implementation.
"""

import numpy as np
import matplotlib.pyplot as plt

def test_imc_imports():
    """Test IMC controller imports."""
    print("=== IMC Import Tests ===")
    
    try:
        # Test modular imports
        from controller.model_based.IMCController import IMCController, FOPDTModel, tune_imc_lambda
        print("✓ Modular IMC imports successful")
        
        # Test legacy imports
        from controllers import IMCController as LegacyIMC, FOPDTModel as LegacyFOPDT
        print("✓ Legacy IMC imports successful")
        
        return True
    except Exception as e:
        print(f"✗ IMC import failed: {e}")
        return False

def test_fopdt_model():
    """Test FOPDT model functionality."""
    print("\n=== FOPDT Model Tests ===")
    
    try:
        from controller.model_based.IMCController import FOPDTModel
        
        # Create FOPDT model: G(s) = 2*exp(-0.5s)/(3s+1)
        model = FOPDTModel(K=2.0, tau=3.0, theta=0.5)
        
        # Test transfer function at s=0 (should equal K)
        G_0 = model.transfer_function(0)
        assert abs(G_0 - 2.0) < 1e-6, f"G(0) should be 2.0, got {G_0}"
        
        # Test step response
        t = np.linspace(0, 15, 100)
        y = model.step_response(t)
        
        # At steady state (large t), response should approach K
        y_final = y[-1]
        assert abs(y_final - 2.0) < 0.1, f"Final value should be ~2.0, got {y_final}"
        
        print(f"✓ FOPDT model: K={model.K}, τ={model.tau}, θ={model.theta}")
        print(f"✓ Step response final value: {y_final:.3f}")
        
        return True
    except Exception as e:
        print(f"✗ FOPDT model test failed: {e}")
        return False

def test_imc_controller():
    """Test IMC controller functionality."""
    print("\n=== IMC Controller Tests ===")
    
    try:
        from controller.model_based.IMCController import IMCController, FOPDTModel, tune_imc_lambda
        
        # Create process model
        process = FOPDTModel(K=2.0, tau=3.0, theta=0.5)
        
        # Tune filter time constant
        lambda_c = tune_imc_lambda(process, desired_settling_time=10.0)
        print(f"✓ IMC tuning: λ = {lambda_c:.3f}")
        
        # Create IMC controller
        imc = IMCController(process, filter_time_constant=lambda_c)
        
        # Test equivalent PID parameters
        tuning_params = imc.get_tuning_parameters()
        print(f"✓ Equivalent PID: Kp={tuning_params['equivalent_Kp']:.3f}, "
              f"Ki={tuning_params['equivalent_Ki']:.3f}, Kd={tuning_params['equivalent_Kd']:.3f}")
        
        # Test controller update
        output = imc.update(t=1.0, setpoint=10.0, process_variable=5.0)
        print(f"✓ Controller output: {output:.3f}")
        
        return True
    except Exception as e:
        print(f"✗ IMC controller test failed: {e}")
        return False

def test_imc_simulation():
    """Test IMC controller in closed-loop simulation."""
    print("\n=== IMC Simulation Test ===")
    
    try:
        from controller.model_based.IMCController import IMCController, FOPDTModel, tune_imc_lambda
        
        # Process model: G(s) = 1.5*exp(-1s)/(5s+1)
        process = FOPDTModel(K=1.5, tau=5.0, theta=1.0)
        
        # Tune and create controller
        lambda_c = tune_imc_lambda(process, desired_settling_time=15.0)
        imc = IMCController(process, filter_time_constant=lambda_c)
        imc.set_output_limits(-10, 10)
        
        # Simulation parameters
        dt = 0.1
        t_final = 25.0
        t = np.arange(0, t_final, dt)
        
        # Initialize arrays
        setpoint = np.ones_like(t) * 5.0  # Step setpoint to 5
        setpoint[t < 2.0] = 0.0  # Start at 0 for first 2 seconds
        
        pv = np.zeros_like(t)  # Process variable
        mv = np.zeros_like(t)  # Manipulated variable
        
        # Simple first-order simulation (approximation)
        for i in range(1, len(t)):
            # Controller update
            mv[i] = imc.update(t[i], setpoint[i], pv[i-1])
            
            # Simple process response (first-order approximation)
            # In practice, you'd use the actual process model
            if t[i] > process.theta:  # After dead time
                pv[i] = pv[i-1] + dt * (process.K * mv[i-1] - pv[i-1]) / process.tau
            else:
                pv[i] = pv[i-1]
        
        # Check performance
        steady_state_error = abs(pv[-1] - setpoint[-1])
        print(f"✓ Simulation completed: final PV = {pv[-1]:.3f}, SP = {setpoint[-1]:.3f}")
        print(f"✓ Steady-state error: {steady_state_error:.3f}")
        
        return True
    except Exception as e:
        print(f"✗ IMC simulation test failed: {e}")
        return False

def test_frequency_response():
    """Test IMC frequency response."""
    print("\n=== IMC Frequency Response Test ===")
    
    try:
        from controller.model_based.IMCController import IMCController, FOPDTModel
        
        # Create system
        process = FOPDTModel(K=2.0, tau=3.0, theta=0.5)
        imc = IMCController(process, filter_time_constant=1.0)
        
        # Calculate frequency response
        omega = np.logspace(-2, 1, 50)  # 0.01 to 10 rad/time
        mag, phase, _ = imc.frequency_response(omega)
        
        # Basic checks
        assert len(mag) == len(omega), "Magnitude array length mismatch"
        assert len(phase) == len(omega), "Phase array length mismatch"
        assert all(mag >= 0), "Magnitude should be non-negative"
        
        print(f"✓ Frequency response calculated: {len(omega)} points")
        print(f"✓ Magnitude range: {mag.min():.3f} to {mag.max():.3f}")
        
        return True
    except Exception as e:
        print(f"✗ Frequency response test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("IMC CONTROLLER TEST SUITE")
    print("=" * 60)
    
    import_ok = test_imc_imports()
    model_ok = test_fopdt_model()
    controller_ok = test_imc_controller()
    simulation_ok = test_imc_simulation()
    frequency_ok = test_frequency_response()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"IMC imports:         {'✓ PASS' if import_ok else '✗ FAIL'}")
    print(f"FOPDT model:         {'✓ PASS' if model_ok else '✗ FAIL'}")
    print(f"IMC controller:      {'✓ PASS' if controller_ok else '✗ FAIL'}")
    print(f"IMC simulation:      {'✓ PASS' if simulation_ok else '✗ FAIL'}")
    print(f"Frequency response:  {'✓ PASS' if frequency_ok else '✗ FAIL'}")
    
    if all([import_ok, model_ok, controller_ok, simulation_ok, frequency_ok]):
        print("\nALL IMC TESTS PASSED!")
        print("IMC Controller implementation is successful!")
    else:
        print("\n❌ Some tests failed. Check the implementation.")
