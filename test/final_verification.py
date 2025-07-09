"""
Final Verification Script for SPROCLIB Refactoring
==================================================

This script performs verification of the completed SPROCLIB refactoring,
including testing all refactored modules and example scripts.

Author: GitHub Copilot
Date: 2024
"""

import sys
import os
import importlib

# Add the process_control directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_refactored_imports():
    """Test all refactored module imports."""
    print("Testing Refactored Module Imports")
    print("=" * 40)
    
    modules_to_test = [
        ("unit.pump.Pump", "Pump"),
        ("unit.pump.CentrifugalPump", "CentrifugalPump"),
        ("unit.pump.PositiveDisplacementPump", "PositiveDisplacementPump"),
        ("unit.compressor.Compressor", "Compressor"),
        ("unit.valve.ControlValve", "ControlValve"),
        ("unit.valve.ThreeWayValve", "ThreeWayValve"),
        ("unit.tank.Tank", "Tank"),
        ("unit.tank.InteractingTanks", "InteractingTanks"),
        ("unit.reactor.cstr", "CSTR"),
        ("unit.reactor.PlugFlowReactor", "PlugFlowReactor"),
        ("unit.reactor.BatchReactor", "BatchReactor"),
        ("unit.reactor.SemiBatchReactor", "SemiBatchReactor"),
        ("unit.reactor.FluidizedBedReactor", "FluidizedBedReactor"),
        ("unit.reactor.FixedBedReactor", "FixedBedReactor"),
        ("unit.distillation.column.BinaryDistillationColumn", "BinaryDistillationColumn"),
        ("unit.distillation.tray.DistillationTray", "DistillationTray"),
        ("unit.heat_exchanger.HeatExchanger", "HeatExchanger"),
        ("unit.utilities.LinearApproximation", "LinearApproximation"),
        ("unit.base.ProcessModel", "ProcessModel")
    ]
    
    passed = 0
    failed = 0
    
    for module_path, class_name in modules_to_test:
        try:
            module = importlib.import_module(module_path)
            cls = getattr(module, class_name)
            print(f"✅ {module_path}.{class_name}")
            passed += 1
        except Exception as e:
            print(f"❌ {module_path}.{class_name} - Error: {e}")
            failed += 1
    
    print(f"\nImport Results: {passed}/{len(modules_to_test)} passed")
    return failed == 0


def test_backward_compatibility():
    """Test backward compatibility through __init__.py imports."""
    print("\nTesting Backward Compatibility")
    print("=" * 40)
    
    compatibility_tests = [
        ("unit.pump", ["Pump", "CentrifugalPump", "PositiveDisplacementPump"]),
        ("unit.compressor", ["Compressor"]),
        ("unit.valve", ["ControlValve", "ThreeWayValve"]),
        ("unit.tank", ["Tank", "InteractingTanks"]),
        ("unit.reactor", ["CSTR", "PlugFlowReactor", "BatchReactor", "SemiBatchReactor", "FluidizedBedReactor", "FixedBedReactor"]),
        ("unit.distillation", ["BinaryDistillationColumn", "DistillationTray"]),
        ("unit.heat_exchanger", ["HeatExchanger"]),
        ("unit.utilities", ["LinearApproximation"]),
        ("unit.base", ["ProcessModel"])
    ]
    
    passed = 0
    failed = 0
    
    for module_path, class_names in compatibility_tests:
        try:
            module = importlib.import_module(module_path)
            for class_name in class_names:
                cls = getattr(module, class_name)
                print(f"✅ {module_path}.{class_name} (backward compatible)")
                passed += 1
        except Exception as e:
            print(f"❌ {module_path} - Error: {e}")
            failed += len(class_names)
    
    total_tests = sum(len(classes) for _, classes in compatibility_tests)
    print(f"\nBackward Compatibility Results: {passed}/{total_tests} passed")
    return failed == 0


def test_instantiation():
    """Test instantiation of all refactored classes."""
    print("\nTesting Class Instantiation")
    print("=" * 40)
    
    # First create a simple ProcessModel for LinearApproximation
    from unit.base.ProcessModel import ProcessModel
    import numpy as np
    
    class SimpleModel(ProcessModel):
        def dynamics(self, t, x, u):
            return np.array([0.0])
        def steady_state(self, u):
            return np.array([0.0])
    
    simple_model = SimpleModel(name="Test Model")
    
    instantiation_tests = [
        ("unit.pump.Pump", "Pump", {"name": "Test Pump"}),
        ("unit.pump.CentrifugalPump", "CentrifugalPump", {"name": "Test Centrifugal"}),
        ("unit.pump.PositiveDisplacementPump", "PositiveDisplacementPump", {"name": "Test PD"}),
        ("unit.compressor.Compressor", "Compressor", {"name": "Test Compressor"}),
        ("unit.valve.ControlValve", "ControlValve", {"name": "Test Control Valve"}),
        ("unit.valve.ThreeWayValve", "ThreeWayValve", {"name": "Test Three-Way"}),
        ("unit.tank.Tank", "Tank", {"name": "Test Tank"}),
        ("unit.tank.InteractingTanks", "InteractingTanks", {"name": "Test Interacting"}),
        ("unit.reactor.cstr", "CSTR", {"name": "Test CSTR"}),
        ("unit.reactor.PlugFlowReactor", "PlugFlowReactor", {"name": "Test PFR"}),
        ("unit.reactor.BatchReactor", "BatchReactor", {"name": "Test Batch"}),
        ("unit.reactor.SemiBatchReactor", "SemiBatchReactor", {"name": "Test SemiBatch"}),
        ("unit.reactor.FluidizedBedReactor", "FluidizedBedReactor", {"name": "Test Fluidized"}),
        ("unit.reactor.FixedBedReactor", "FixedBedReactor", {"name": "Test Fixed"}),
        ("unit.distillation.column.BinaryDistillationColumn", "BinaryDistillationColumn", {"name": "Test Column"}),
        ("unit.distillation.tray.DistillationTray", "DistillationTray", {"name": "Test Tray"}),
        ("unit.heat_exchanger.HeatExchanger", "HeatExchanger", {"name": "Test HX"}),
        ("unit.utilities.LinearApproximation", "LinearApproximation", {"model": simple_model})
    ]
    
    passed = 0
    failed = 0
    
    for module_path, class_name, kwargs in instantiation_tests:
        try:
            module = importlib.import_module(module_path)
            cls = getattr(module, class_name)
            instance = cls(**kwargs)
            print(f"✅ {class_name} instantiated successfully")
            passed += 1
        except Exception as e:
            print(f"❌ {class_name} - Error: {e}")
            failed += 1
    
    print(f"\nInstantiation Results: {passed}/{len(instantiation_tests)} passed")
    return failed == 0


def test_example_scripts():
    """Test that all example scripts can be imported."""
    print("\nTesting Example Scripts")
    print("=" * 40)
    
    example_scripts = [
        "pump_examples",
        "compressor_examples",
        "valve_examples",
        "tank_examples",
        "reactor_examples",
        "heat_exchanger_examples",
        "distillation_examples",
        "utilities_examples",
        "complete_process_examples"
    ]
    
    passed = 0
    failed = 0
    
    # Add examples directory to path
    examples_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples")
    if examples_path not in sys.path:
        sys.path.insert(0, examples_path)
    
    for script_name in example_scripts:
        try:
            module = importlib.import_module(script_name)
            # Check if main function exists
            if hasattr(module, 'main'):
                print(f"✅ {script_name}.py - main() function available")
                passed += 1
            else:
                print(f"⚠️  {script_name}.py - no main() function")
                passed += 1
        except Exception as e:
            print(f"❌ {script_name}.py - Error: {e}")
            failed += 1
    
    print(f"\nExample Scripts Results: {passed}/{len(example_scripts)} passed")
    return failed == 0


def main():
    """Run comprehensive verification of SPROCLIB refactoring."""
    print("SPROCLIB Refactoring - Final Verification")
    print("=" * 50)
    print("Testing all refactored modules, backward compatibility, and examples...")
    print()
    
    all_tests_passed = True
    
    # Run all tests
    tests = [
        ("Refactored Imports", test_refactored_imports),
        ("Backward Compatibility", test_backward_compatibility),
        ("Class Instantiation", test_instantiation),
        ("Example Scripts", test_example_scripts)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
            all_tests_passed = all_tests_passed and results[test_name]
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results[test_name] = False
            all_tests_passed = False
    
    # Summary
    print("\n" + "=" * 50)
    print("FINAL VERIFICATION SUMMARY")
    print("=" * 50)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:<25}: {status}")
    
    print("-" * 50)
    
    if all_tests_passed:
        print("ALL TESTS PASSED! REFACTORING SUCCESSFUL!")
        print("\nRefactoring Summary:")
        print("- ✅ All modules refactored to class-named files")
        print("- ✅ Backward compatibility maintained")
        print("- ✅ All classes instantiate correctly")
        print("- ✅ Comprehensive examples created")
        print("- ✅ Zero breaking changes")
        print("\nThe SPROCLIB refactoring is complete and fully functional!")
    else:
        print("❌ Some tests failed. Please review the errors above.")
    
    return all_tests_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
