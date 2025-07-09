#!/usr/bin/env python3
"""
Test script to verify the legacy package works correctly.
"""
import sys
import warnings
warnings.filterwarnings('ignore')  # Suppress deprecation warnings for test

def test_legacy_package():
    """Test that the legacy package imports work correctly."""
    try:
        # Test legacy package imports
        from legacy import TransferFunction, step_response, tune_pid
        print("✅ Legacy package imports work")
        
        # Test legacy submodule imports
        from legacy.functions import fit_fopdt
        from legacy.analysis import Simulation
        print("✅ Legacy submodule imports work")
        
        # Test basic functionality
        tf = TransferFunction([1], [1, 1])
        print("✅ Legacy TransferFunction creation works")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing legacy package...")
    success = test_legacy_package()
    if success:
        print("Legacy package works correctly!")
    else:
        print("❌ Legacy package has issues")
    sys.exit(0 if success else 1)
