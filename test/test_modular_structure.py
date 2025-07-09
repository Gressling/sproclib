"""
Final validation test for the modular SPROCLIB structure.
This script verifies that all process units have been successfully migrated.
"""

import sys
import traceback

def test_imports():
    """Test all process unit imports."""
    units = {
        'ProcessModel': 'unit.base',
        'CSTR': 'unit.reactor.cstr',
        'PlugFlowReactor': 'unit.reactor.pfr',
        'BatchReactor': 'unit.reactor.batch',
        'FixedBedReactor': 'unit.reactor.fixed_bed', 
        'SemiBatchReactor': 'unit.reactor.semi_batch',
        'Tank': 'unit.tank.single',
        'InteractingTanks': 'unit.tank.interacting',
        'HeatExchanger': 'unit.heat_exchanger',
        'DistillationTray': 'unit.distillation.tray',
        'BinaryDistillationColumn': 'unit.distillation.column',
        'ControlValve': 'unit.valve.control',
        'ThreeWayValve': 'unit.valve.three_way',
        'LinearApproximation': 'unit.utilities'
    }
    
    print("🔍 Testing SPROCLIB Modular Structure")
    print("=" * 50)
    
    success_count = 0
    total_count = len(units)
    
    for class_name, module_path in units.items():
        try:
            module = __import__(module_path, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✅ {class_name:20} -> {module_path}")
            success_count += 1
        except Exception as e:
            print(f"❌ {class_name:20} -> {module_path} (Error: {str(e)})")
    
    print("=" * 50)
    print(f"📊 Results: {success_count}/{total_count} units imported successfully")
    
    if success_count == total_count:
        print("🎉 MODULAR REFACTORING COMPLETE!")
        print("   All 14 process units successfully migrated to modular structure.")
        return True
    else:
        print(f"⚠️  {total_count - success_count} units failed to import.")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
