#!/usr/bin/env python3
"""
Final verification test for the refactored SPROCLIB with legacy folder.
"""
import warnings
warnings.filterwarnings('ignore')  # Suppress deprecation warnings

def test_modern_structure():
    """Test the modern modular structure."""
    print("🔄 Testing modern modular structure...")
    
    try:
        # Test analysis package
        from analysis.transfer_function import TransferFunction
        from analysis.system_analysis import step_response
        print("✅ Analysis package - OK")
        
        # Test utilities package
        from utilities.control_utils import tune_pid
        print("✅ Utilities package - OK")
        
        # Test optimization package
        from optimization.economic_optimization import EconomicOptimization
        print("✅ Optimization package - OK")
        
        # Test basic functionality
        tf = TransferFunction([1], [1, 1])
        print("✅ TransferFunction creation - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Modern structure test failed: {e}")
        return False

def test_legacy_structure():
    """Test the legacy backward compatibility."""
    print("🔄 Testing legacy compatibility...")
    
    try:
        # Test legacy package imports
        from legacy import TransferFunction as LegacyTF
        from legacy.functions import step_response as legacy_step_response
        print("✅ Legacy package imports - OK")
        
        # Test legacy functionality
        tf = LegacyTF([1], [1, 1])
        print("✅ Legacy TransferFunction creation - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Legacy structure test failed: {e}")
        return False

def main():
    print("🚀 SPROCLIB Final Verification Test")
    print("=" * 50)
    
    modern_ok = test_modern_structure()
    legacy_ok = test_legacy_structure()
    
    print("=" * 50)
    if modern_ok and legacy_ok:
        print("🎉 SUCCESS: All tests passed!")
        print("✅ Modern modular structure working")
        print("✅ Legacy compatibility working")
        print("✅ Refactoring with /legacy/ folder complete!")
        return True
    else:
        print("❌ FAILURE: Some tests failed!")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
