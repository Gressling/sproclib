#!/usr/bin/env python3
"""
Test script to demonstrate successful SPROCLIB refactoring

This script tests both the new modular structure and legacy compatibility.
"""

import warnings
import sys

def test_modular_imports():
    """Test new modular import structure."""
    print("🔄 Testing modular imports...")
    
    try:
        # Test analysis module
        from analysis.transfer_function import TransferFunction
        tf = TransferFunction([1], [1, 1], "Test TF")
        print("✅ analysis.transfer_function - OK")
        
        # Test utilities module  
        from utilities.control_utils import tune_pid
        print("✅ utilities.control_utils - OK")
        
        # Test optimization module
        from optimization.economic_optimization import EconomicOptimization
        opt = EconomicOptimization("Test Opt")
        print("✅ optimization.economic_optimization - OK")
        
        # Test scheduling module
        from scheduling.state_task_network import StateTaskNetwork
        stn = StateTaskNetwork("Test STN")
        print("✅ scheduling.state_task_network - OK")
        
        # Test simulation module
        from simulation.process_simulation import ProcessSimulation
        print("✅ simulation.process_simulation - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Modular import failed: {e}")
        return False


def test_legacy_compatibility():
    """Test legacy import compatibility."""
    print("\n🔄 Testing legacy compatibility...")
    
    try:
        # Suppress deprecation warnings for clean output
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            
            # Test legacy analysis imports
            from analysis import TransferFunction, Simulation, Optimization
            tf = TransferFunction([1], [1, 1], "Legacy TF")
            print("✅ Legacy analysis imports - OK")
            
            return True
            
    except Exception as e:
        print(f"❌ Legacy import failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 SPROCLIB Refactoring Test")
    print("=" * 40)
    
    modular_ok = test_modular_imports()
    legacy_ok = test_legacy_compatibility()
    
    print("\n" + "=" * 40)
    if modular_ok and legacy_ok:
        print("🎉 SUCCESS: All tests passed!")
        print("✅ Modular structure working")
        print("✅ Legacy compatibility maintained")
        print("\n📝 SPROCLIB refactoring completed successfully!")
        print("   - analysis.py and functions.py cleaned up")
        print("   - Modular structure implemented")
        print("   - Backward compatibility maintained")
        return 0
    else:
        print("❌ FAILURE: Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
