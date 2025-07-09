#!/usr/bin/env python3
"""
Test script to validate Read the Docs configuration
"""

import sys
import os

def test_imports():
    """Test that basic imports work"""
    try:
        import sphinx
        print(f"✓ Sphinx version: {sphinx.__version__}")
    except ImportError as e:
        print(f"✗ Sphinx import failed: {e}")
        return False
    
    try:
        import sphinx_rtd_theme
        print(f"✓ RTD theme available")
    except ImportError as e:
        print(f"✗ RTD theme import failed: {e}")
        return False
    
    return True

def test_config():
    """Test that configuration loads"""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))
    
    try:
        import conf
        print(f"✓ Configuration loads successfully")
        print(f"  Project: {conf.project}")
        print(f"  Version: {conf.version}")
        print(f"  Extensions: {len(conf.extensions)} loaded")
        return True
    except Exception as e:
        print(f"✗ Configuration failed: {e}")
        return False

def main():
    """Main test function"""
    print("=== Read the Docs Configuration Test ===")
    
    all_passed = True
    all_passed &= test_imports()
    all_passed &= test_config()
    
    if all_passed:
        print("\n✓ All tests passed! Ready for Read the Docs")
        return 0
    else:
        print("\n✗ Some tests failed. Check configuration.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
