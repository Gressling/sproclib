#!/usr/bin/env python3
"""
Test script to verify the refactored SPROCLIB modules import correctly.
"""

import sys
import os

# Add the process_control directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_imports():
    """Test importing all refactored modules."""
    
    print("Testing refactored SPROCLIB module imports...")
    print("=" * 50)
    
    success_count = 0
    total_tests = 0
    
    # Test Pump modules
    try:
        from unit.pump.base import Pump
        print("✓ Pump (base) imported successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ Pump (base) import failed: {e}")
    total_tests += 1
    
    try:
        from unit.pump.centrifugal import CentrifugalPump
        print("✓ CentrifugalPump imported successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ CentrifugalPump import failed: {e}")
    total_tests += 1
    
    try:
        from unit.pump.positive_displacement import PositiveDisplacementPump
        print("✓ PositiveDisplacementPump imported successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ PositiveDisplacementPump import failed: {e}")
    total_tests += 1
    
    # Test Compressor
    try:
        from unit.compressor import Compressor
        print("✓ Compressor imported successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ Compressor import failed: {e}")
    total_tests += 1
    
    # Test ThreeWayValve
    try:
        from unit.valve.three_way import ThreeWayValve
        print("✓ ThreeWayValve imported successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ ThreeWayValve import failed: {e}")
    total_tests += 1
    
    # Test utilities
    try:
        from unit.utilities import LinearApproximation
        print("✓ LinearApproximation imported successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ LinearApproximation import failed: {e}")
    total_tests += 1
    
    # Test InteractingTanks
    try:
        from unit.tank.interacting import InteractingTanks
        print("✓ InteractingTanks imported successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ InteractingTanks import failed: {e}")
    total_tests += 1
    
    # Test additional reactors
    try:
        from unit.reactor.semi_batch import SemiBatchReactor
        print("✓ SemiBatchReactor imported successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ SemiBatchReactor import failed: {e}")
    total_tests += 1
    
    try:
        from unit.reactor.fluidized_bed import FluidizedBedReactor
        print("✓ FluidizedBedReactor imported successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ FluidizedBedReactor import failed: {e}")
    total_tests += 1
    
    try:
        from unit.reactor.fixed_bed import FixedBedReactor
        print("✓ FixedBedReactor imported successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ FixedBedReactor import failed: {e}")
    total_tests += 1
    
    print("=" * 50)
    print(f"Import test results: {success_count}/{total_tests} modules imported successfully")
    
    if success_count == total_tests:
        print("🎉 All modules imported successfully!")
        return True
    else:
        print(f"⚠️  {total_tests - success_count} modules failed to import")
        return False

if __name__ == "__main__":
    test_imports()
