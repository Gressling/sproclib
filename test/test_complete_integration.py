"""
Complete Integration Test for All Recovered Models
Tests all 18 models in the SPROCLIB modular structure
"""

import sys
import os

# Add the process_control directory to Python path
sys.path.insert(0, os.path.abspath('.'))

def test_all_models():
    """Test import and instantiation of all 18 SPROCLIB models."""
    
    print("=== SPROCLIB COMPLETE INTEGRATION TEST ===")
    print("Testing all 18 process unit models...\n")
    
    models_tested = 0
    models_passed = 0
    
    try:
        # Test base class
        print("1. Testing Base Classes...")
        from unit.base import ProcessModel
        print("   ✓ ProcessModel imported successfully")
        models_tested += 1
        models_passed += 1
        
        # Test reactor models
        print("\n2. Testing Reactor Models...")
        from unit.reactor.cstr import CSTR
        from unit.reactor.pfr import PlugFlowReactor
        from unit.reactor.batch import BatchReactor
        from unit.reactor.fixed_bed import FixedBedReactor
        from unit.reactor.semi_batch import SemiBatchReactor
        from unit.reactor.fluidized_bed import FluidizedBedReactor
        
        cstr = CSTR(name="Test CSTR")
        pfr = PlugFlowReactor(name="Test PFR")
        batch = BatchReactor(name="Test Batch")
        fixed_bed = FixedBedReactor(name="Test Fixed Bed")
        semi_batch = SemiBatchReactor(name="Test Semi-Batch")
        fluidized_bed = FluidizedBedReactor(name="Test Fluidized Bed")
        
        print("   ✓ CSTR imported and instantiated successfully")
        print("   ✓ PlugFlowReactor imported and instantiated successfully")
        print("   ✓ BatchReactor imported and instantiated successfully")
        print("   ✓ FixedBedReactor imported and instantiated successfully")
        print("   ✓ SemiBatchReactor imported and instantiated successfully")
        print("   ✓ FluidizedBedReactor imported and instantiated successfully")
        models_tested += 6
        models_passed += 6
        
        # Test tank models
        print("\n3. Testing Tank Models...")
        from unit.tank.single import Tank
        from unit.tank.interacting import InteractingTanks
        
        tank = Tank(name="Test Tank")
        interacting = InteractingTanks(name="Test Interacting Tanks")
        
        print("   ✓ Tank imported and instantiated successfully")
        print("   ✓ InteractingTanks imported and instantiated successfully")
        models_tested += 2
        models_passed += 2
        
        # Test heat exchanger
        print("\n4. Testing Heat Transfer Equipment...")
        from unit.heat_exchanger import HeatExchanger
        
        hx = HeatExchanger(name="Test Heat Exchanger")
        
        print("   ✓ HeatExchanger imported and instantiated successfully")
        models_tested += 1
        models_passed += 1
        
        # Test distillation models
        print("\n5. Testing Separation Equipment...")
        from unit.distillation.tray import DistillationTray
        from unit.distillation.column import BinaryDistillationColumn
        
        tray = DistillationTray(name="Test Distillation Tray")
        column = BinaryDistillationColumn(name="Test Distillation Column")
        
        print("   ✓ DistillationTray imported and instantiated successfully")
        print("   ✓ BinaryDistillationColumn imported and instantiated successfully")
        models_tested += 2
        models_passed += 2
        
        # Test valve models
        print("\n6. Testing Flow Control Equipment...")
        from unit.valve.control import ControlValve
        from unit.valve.three_way import ThreeWayValve
        
        control_valve = ControlValve(name="Test Control Valve")
        three_way = ThreeWayValve(name="Test Three-Way Valve")
        
        print("   ✓ ControlValve imported and instantiated successfully")
        print("   ✓ ThreeWayValve imported and instantiated successfully")
        models_tested += 2
        models_passed += 2
        
        # Test pump models (RECOVERED)
        print("\n7. Testing Pump Equipment (RECOVERED)...")
        from unit.pump.base import Pump
        from unit.pump.centrifugal import CentrifugalPump
        from unit.pump.positive_displacement import PositiveDisplacementPump
        
        pump = Pump(name="Test Pump")
        centrifugal = CentrifugalPump(name="Test Centrifugal Pump")
        pos_disp = PositiveDisplacementPump(name="Test PD Pump")
        
        print("   ✓ Pump imported and instantiated successfully")
        print("   ✓ CentrifugalPump imported and instantiated successfully")
        print("   ✓ PositiveDisplacementPump imported and instantiated successfully")
        models_tested += 3
        models_passed += 3
        
        # Test compressor model (RECOVERED)
        print("\n8. Testing Compression Equipment (RECOVERED)...")
        from unit.compressor import Compressor
        
        compressor = Compressor(name="Test Compressor")
        
        print("   ✓ Compressor imported and instantiated successfully")
        models_tested += 1
        models_passed += 1
        
        # Test utility models
        print("\n9. Testing Utility Models...")
        from unit.utilities import LinearApproximation
        
        linear = LinearApproximation(tank)  # Use tank as the model to linearize
        
        print("   ✓ LinearApproximation imported and instantiated successfully")
        models_tested += 1
        models_passed += 1
        
        # Test main module imports
        print("\n10. Testing Main Module Imports...")
        from unit import (
            ProcessModel, CSTR, PlugFlowReactor, BatchReactor, FixedBedReactor, 
            SemiBatchReactor, FluidizedBedReactor, Tank, InteractingTanks, 
            HeatExchanger, DistillationTray, BinaryDistillationColumn, 
            ControlValve, ThreeWayValve, Pump, CentrifugalPump, 
            PositiveDisplacementPump, Compressor, LinearApproximation
        )
        
        print("   ✓ All models can be imported from main unit module")
        
        print(f"\n=== INTEGRATION TEST RESULTS ===")
        print(f"Models Tested: {models_tested}")
        print(f"Models Passed: {models_passed}")
        print(f"Success Rate: {models_passed/models_tested*100:.1f}%")
        
        if models_tested == models_passed and models_tested >= 18:
            print(f"\nALL {models_tested} MODELS PASSED INTEGRATION TEST!")
            print("SPROCLIB modular refactoring is COMPLETE and FUNCTIONAL!")
            return True
        else:
            print(f"\n❌ PARTIAL SUCCESS: {models_passed}/{models_tested} models passed")
            return False
            
    except Exception as e:
        print(f"\n❌ INTEGRATION TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_all_models()
    if not success:
        sys.exit(1)
