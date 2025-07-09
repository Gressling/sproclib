#!/usr/bin/env python3
"""
Test script to verify all modules work with the refactored ProcessModel base class.
"""

import sys
import os

# Add the process_control directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_base_class_refactor():
    """Test that all modules work with refactored ProcessModel."""
    
    print("Testing ProcessModel base class refactoring...")
    print("=" * 50)
    
    success_count = 0
    total_tests = 0
    
    # Test ProcessModel import
    try:
        from unit.base import ProcessModel
        print("✓ ProcessModel imported from unit.base")
        success_count += 1
    except Exception as e:
        print(f"✗ ProcessModel import failed: {e}")
    total_tests += 1
    
    # Test ProcessModel direct import
    try:
        from unit.base.ProcessModel import ProcessModel as DirectProcessModel
        print("✓ ProcessModel imported directly from ProcessModel.py")
        success_count += 1
    except Exception as e:
        print(f"✗ ProcessModel direct import failed: {e}")
    total_tests += 1
    
    # Test that all refactored classes still inherit correctly
    try:
        from unit.pump.base import Pump
        pump = Pump()
        assert isinstance(pump, ProcessModel), "Pump should inherit from ProcessModel"
        print("✓ Pump inherits correctly from refactored ProcessModel")
        success_count += 1
    except Exception as e:
        print(f"✗ Pump inheritance test failed: {e}")
    total_tests += 1
    
    try:
        from unit.compressor import Compressor
        comp = Compressor()
        assert isinstance(comp, ProcessModel), "Compressor should inherit from ProcessModel"
        print("✓ Compressor inherits correctly from refactored ProcessModel")
        success_count += 1
    except Exception as e:
        print(f"✗ Compressor inheritance test failed: {e}")
    total_tests += 1
    
    try:
        from unit.reactor.semi_batch import SemiBatchReactor
        sbr = SemiBatchReactor()
        assert isinstance(sbr, ProcessModel), "SemiBatchReactor should inherit from ProcessModel"
        print("✓ SemiBatchReactor inherits correctly from refactored ProcessModel")
        success_count += 1
    except Exception as e:
        print(f"✗ SemiBatchReactor inheritance test failed: {e}")
    total_tests += 1
    
    # Test that all abstract methods are properly implemented
    try:
        from unit.tank.interacting import InteractingTanks
        tanks = InteractingTanks()
        # Test that required methods exist
        assert hasattr(tanks, 'dynamics'), "Should have dynamics method"
        assert hasattr(tanks, 'steady_state'), "Should have steady_state method"
        assert hasattr(tanks, 'simulate'), "Should have simulate method from base class"
        print("✓ InteractingTanks has all required methods from ProcessModel")
        success_count += 1
    except Exception as e:
        print(f"✗ InteractingTanks method test failed: {e}")
    total_tests += 1
    
    print("=" * 50)
    print(f"Base class refactor test results: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("ProcessModel base class refactoring successful!")
        return True
    else:
        print(f"⚠️  {total_tests - success_count} tests failed")
        return False

if __name__ == "__main__":
    test_base_class_refactor()
