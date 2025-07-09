#!/usr/bin/env python3
"""
Test script for controller refactoring.
"""

def test_modular_imports():
    """Test new modular imports."""
    try:
        from controller.pid.PIDController import PIDController
        from controller.tuning.ZieglerNicholsTuning import ZieglerNicholsTuning
        from controller.tuning.AMIGOTuning import AMIGOTuning
        from controller.tuning.RelayTuning import RelayTuning
        from controller.base.TuningRule import TuningRule
        print("✓ All modular imports successful")
        return True
    except ImportError as e:
        print(f"✗ Modular import failed: {e}")
        return False

def test_legacy_imports():
    """Test backward compatibility imports."""
    try:
        from controllers import PIDController, ZieglerNicholsTuning, AMIGOTuning, RelayTuning, TuningRule
        print("✓ Legacy imports successful")
        return True
    except ImportError as e:
        print(f"✗ Legacy import failed: {e}")
        return False

def test_controller_functionality():
    """Test that the controllers work correctly."""
    try:
        # Test PID controller
        from controller.pid.PIDController import PIDController
        pid = PIDController(Kp=1.0, Ki=0.1, Kd=0.05)
        output = pid.update(t=1.0, SP=50.0, PV=45.0)
        print(f"✓ PID controller test: output = {output}")
        
        # Test tuning rule
        from controller.tuning.ZieglerNicholsTuning import ZieglerNicholsTuning
        tuner = ZieglerNicholsTuning(controller_type="PID")
        params = tuner.calculate_parameters({'K': 2.0, 'tau': 5.0, 'theta': 1.0})
        print(f"✓ Tuning rule test: {params}")
        
        return True
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Controller Refactoring...")
    print("=" * 40)
    
    modular_ok = test_modular_imports()
    legacy_ok = test_legacy_imports()
    functionality_ok = test_controller_functionality()
    
    print("=" * 40)
    if modular_ok and legacy_ok and functionality_ok:
        print("All tests passed! Controller refactoring successful.")
    else:
        print("❌ Some tests failed. Check the imports and structure.")
