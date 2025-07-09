#!/usr/bin/env python3
"""
Test script to verify that backward compatibility works before cleanup.
"""
import sys
import warnings
warnings.filterwarnings('ignore')  # Suppress deprecation warnings for test

def test_wrappers():
    """Test that current backward compatibility wrappers work correctly."""
    try:
        # Test functions wrapper
        from functions import step_response, tune_pid, fit_fopdt
        print("✓ functions wrapper works")
        
        # Test analysis wrapper  
        from analysis import TransferFunction
        tf = TransferFunction([1], [1, 1])
        print("✓ analysis wrapper works")
        
        print("All backward compatibility wrappers are functional")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_wrappers()
    sys.exit(0 if success else 1)
