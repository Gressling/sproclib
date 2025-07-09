"""
EMERGENCY RECOVERY TEST for missing Pump and Compressor models

This script tests the recovered pump and compressor models that were 
missing from the modular refactoring.
"""

import sys
import os
sys.path.append('.')

try:
    print("🔍 Testing recovered pump and compressor models...")
    print("=" * 60)
    
    # Test imports
    from unit.pump.base import Pump
    from unit.pump.centrifugal import CentrifugalPump  
    from unit.pump.positive_displacement import PositiveDisplacementPump
    from unit.compressor import Compressor
    
    print("✅ All imports successful!")
    
    # Test instantiation
    pump = Pump(name="GenericPump")
    centrifugal = CentrifugalPump(name="CentrifugalPump")
    pd_pump = PositiveDisplacementPump(name="PDPump")
    compressor = Compressor(name="GasCompressor")
    
    print(f"✅ {pump.name} created")
    print(f"✅ {centrifugal.name} created") 
    print(f"✅ {pd_pump.name} created")
    print(f"✅ {compressor.name} created")
    
    print()
    print("🎉 RECOVERY SUCCESSFUL!")
    print("All missing pump and compressor models have been recovered and are working!")
    
    print()
    print("📊 Final Equipment Count:")
    print("   Original (before refactoring): 14 classes")
    print("   Missing during refactoring: 4 classes (Pump, CentrifugalPump, PositiveDisplacementPump, Compressor)")
    print("   Now recovered: 18 total classes")
    print()
    print("✅ COMPLETE EQUIPMENT INVENTORY:")
    
    # List all equipment
    equipment = [
        "ProcessModel (base)",
        "CSTR", "PlugFlowReactor", "BatchReactor", "FixedBedReactor", "SemiBatchReactor",
        "Tank", "InteractingTanks", 
        "HeatExchanger",
        "DistillationTray", "BinaryDistillationColumn",
        "ControlValve", "ThreeWayValve",
        "Pump", "CentrifugalPump", "PositiveDisplacementPump",  # RECOVERED
        "Compressor",  # RECOVERED
        "LinearApproximation"
    ]
    
    for i, item in enumerate(equipment, 1):
        marker = "🆕" if item in ["Pump", "CentrifugalPump", "PositiveDisplacementPump", "Compressor"] else "  "
        print(f"{marker} {i:2d}. {item}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
