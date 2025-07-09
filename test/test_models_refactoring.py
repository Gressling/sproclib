#!/usr/bin/env python3
"""
Test script for models refactoring to use unit package.
"""

def test_modular_imports():
    """Test new modular imports."""
    try:
        from unit.base import ProcessModel
        from unit.reactor.cstr import CSTR
        from unit.tank.single import Tank
        from unit.heat_exchanger import HeatExchanger
        from unit.utilities import LinearApproximation
        print("✓ All modular imports successful")
        return True
    except ImportError as e:
        print(f"✗ Modular import failed: {e}")
        return False

def test_legacy_imports():
    """Test backward compatibility imports."""
    try:
        from models import ProcessModel, CSTR, Tank, HeatExchanger, LinearApproximation
        print("✓ Legacy imports successful")
        return True
    except ImportError as e:
        print(f"✗ Legacy import failed: {e}")
        return False

def test_model_functionality():
    """Test that the models work correctly."""
    try:
        # Test Tank model
        from unit.tank.single import Tank
        tank = Tank(A=2.0, C=1.5)
        
        import numpy as np
        u = np.array([10.0])  # inlet flow
        x_ss = tank.steady_state(u)
        print(f"✓ Tank model test: steady-state height = {x_ss[0]:.2f}")
        
        # Test CSTR model
        from unit.reactor.cstr import CSTR
        cstr = CSTR()
        u_cstr = np.array([100.0, 1.0, 350.0, 300.0])  # q, CAi, Ti, Tc
        x_cstr_ss = cstr.steady_state(u_cstr)
        print(f"✓ CSTR model test: steady-state CA = {x_cstr_ss[0]:.4f}, T = {x_cstr_ss[1]:.1f}")
        
        return True
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Models Refactoring...")
    print("=" * 40)
    
    modular_ok = test_modular_imports()
    legacy_ok = test_legacy_imports()
    functionality_ok = test_model_functionality()
    
    print("=" * 40)
    if modular_ok and legacy_ok and functionality_ok:
        print("All tests passed! Models refactoring successful.")
    else:
        print("❌ Some tests failed. Check the imports and structure.")
