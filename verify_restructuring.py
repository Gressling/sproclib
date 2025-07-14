#!/usr/bin/env python3
"""
Verification script for the restructured solid transport package.

This script tests that all classes can be imported and instantiated correctly
after the package restructuring.
"""

def test_imports():
    """Test all imports work correctly."""
    print("Testing imports...")
    
    # Test main package imports
    from sproclib.transport.continuous.solid import (
        ConveyorBelt, GravityChute, PneumaticConveying, ScrewFeeder
    )
    print("✓ Main package imports successful")
    
    # Test direct subpackage imports
    from sproclib.transport.continuous.solid.conveyor_belt import ConveyorBelt as CB
    from sproclib.transport.continuous.solid.gravity_chute import GravityChute as GC
    from sproclib.transport.continuous.solid.pneumatic_conveying import PneumaticConveying as PC
    from sproclib.transport.continuous.solid.screw_feeder import ScrewFeeder as SF
    print("✓ Direct subpackage imports successful")
    
    return {
        'ConveyorBelt': ConveyorBelt,
        'GravityChute': GravityChute, 
        'PneumaticConveying': PneumaticConveying,
        'ScrewFeeder': ScrewFeeder
    }

def test_instantiation(classes):
    """Test all classes can be instantiated."""
    print("\nTesting class instantiation...")
    
    instances = {}
    
    # ConveyorBelt
    cb = classes['ConveyorBelt'](belt_length=50.0, belt_speed=1.5)
    instances['ConveyorBelt'] = cb
    print(f"✓ ConveyorBelt: {cb.name} (length: {cb.belt_length}m, speed: {cb.belt_speed}m/s)")
    
    # GravityChute
    gc = classes['GravityChute'](chute_length=30.0, chute_angle=0.5)
    instances['GravityChute'] = gc
    print(f"✓ GravityChute: {gc.name} (length: {gc.chute_length}m, angle: {gc.chute_angle}rad)")
    
    # PneumaticConveying
    pc = classes['PneumaticConveying'](pipe_length=100.0, conveying_velocity=25.0)
    instances['PneumaticConveying'] = pc
    print(f"✓ PneumaticConveying: {pc.name} (length: {pc.pipe_length}m, velocity: {pc.conveying_velocity}m/s)")
    
    # ScrewFeeder
    sf = classes['ScrewFeeder'](screw_length=5.0, screw_speed=60.0)
    instances['ScrewFeeder'] = sf
    print(f"✓ ScrewFeeder: {sf.name} (length: {sf.screw_length}m, speed: {sf.screw_speed}rpm)")
    
    return instances

def test_functionality(instances):
    """Test basic functionality of each class."""
    print("\nTesting basic functionality...")
    
    # Test that classes have the expected methods from ProcessModel
    for name, instance in instances.items():
        # Test basic attributes
        assert hasattr(instance, 'name'), f"{name} missing 'name' attribute"
        assert hasattr(instance, 'inputs'), f"{name} missing 'inputs' attribute"
        assert hasattr(instance, 'outputs'), f"{name} missing 'outputs' attribute"
        print(f"✓ {name} has expected base attributes")

def main():
    """Main verification function."""
    print("=" * 60)
    print("SOLID TRANSPORT PACKAGE RESTRUCTURING VERIFICATION")
    print("=" * 60)
    
    try:
        # Test imports
        classes = test_imports()
        
        # Test instantiation
        instances = test_instantiation(classes)
        
        # Test functionality
        test_functionality(instances)
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED - RESTRUCTURING SUCCESSFUL!")
        print("=" * 60)
        
        # Display final structure summary
        print(f"\nRestructured Package Summary:")
        print(f"├── conveyor_belt/")
        print(f"│   ├── __init__.py")
        print(f"│   ├── conveyor_belt.py (ConveyorBelt class)")
        print(f"│   ├── test_conveyor_belt.py")
        print(f"│   ├── example.py")
        print(f"│   ├── documentation.md")
        print(f"│   └── plots/")
        print(f"├── gravity_chute/")
        print(f"│   └── ... (similar structure)")
        print(f"├── pneumatic_conveying/")
        print(f"│   └── ... (similar structure)")
        print(f"└── screw_feeder/")
        print(f"    └── ... (similar structure)")
        
    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {e}")
        raise

if __name__ == "__main__":
    main()
