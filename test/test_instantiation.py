#!/usr/bin/env python3
"""
Test script to verify the refactored SPROCLIB modules can be instantiated.
"""

import sys
import os
import numpy as np

# Add the process_control directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_instantiation():
    """Test instantiating all refactored modules."""
    
    print("Testing refactored SPROCLIB module instantiation...")
    print("=" * 50)
    
    success_count = 0
    total_tests = 0
    
    # Test Pump modules
    try:
        from unit.pump.base import Pump
        pump = Pump(eta=0.8, rho=1200.0, name="TestPump")
        print(f"✓ Pump instantiated: {pump.name}")
        success_count += 1
    except Exception as e:
        print(f"✗ Pump instantiation failed: {e}")
    total_tests += 1
    
    try:
        from unit.pump.centrifugal import CentrifugalPump
        cpump = CentrifugalPump(H0=60.0, K=25.0, name="TestCentrifugalPump")
        print(f"✓ CentrifugalPump instantiated: {cpump.name}")
        success_count += 1
    except Exception as e:
        print(f"✗ CentrifugalPump instantiation failed: {e}")
    total_tests += 1
    
    try:
        from unit.pump.positive_displacement import PositiveDisplacementPump
        pdpump = PositiveDisplacementPump(flow_rate=2.0, name="TestPDPump")
        print(f"✓ PositiveDisplacementPump instantiated: {pdpump.name}")
        success_count += 1
    except Exception as e:
        print(f"✗ PositiveDisplacementPump instantiation failed: {e}")
    total_tests += 1
    
    try:
        from unit.compressor import Compressor
        comp = Compressor(eta_isentropic=0.8, name="TestCompressor")
        print(f"✓ Compressor instantiated: {comp.name}")
        success_count += 1
    except Exception as e:
        print(f"✗ Compressor instantiation failed: {e}")
    total_tests += 1
    
    try:
        from unit.valve.three_way import ThreeWayValve
        valve = ThreeWayValve(Cv_max=120.0, valve_config="mixing", name="TestThreeWayValve")
        print(f"✓ ThreeWayValve instantiated: {valve.name}")
        success_count += 1
    except Exception as e:
        print(f"✗ ThreeWayValve instantiation failed: {e}")
    total_tests += 1
    
    try:
        from unit.tank.interacting import InteractingTanks
        tanks = InteractingTanks(A1=2.0, A2=1.5, name="TestInteractingTanks")
        print(f"✓ InteractingTanks instantiated: {tanks.name}")
        success_count += 1
    except Exception as e:
        print(f"✗ InteractingTanks instantiation failed: {e}")
    total_tests += 1
    
    try:
        from unit.reactor.semi_batch import SemiBatchReactor
        sbr = SemiBatchReactor(V_max=250.0, k0=1e11, name="TestSemiBatchReactor")
        print(f"✓ SemiBatchReactor instantiated: {sbr.name}")
        success_count += 1
    except Exception as e:
        print(f"✗ SemiBatchReactor instantiation failed: {e}")
    total_tests += 1
    
    try:
        from unit.reactor.fluidized_bed import FluidizedBedReactor
        fbr = FluidizedBedReactor(H=4.0, D=2.5, name="TestFluidizedBedReactor")
        print(f"✓ FluidizedBedReactor instantiated: {fbr.name}")
        success_count += 1
    except Exception as e:
        print(f"✗ FluidizedBedReactor instantiation failed: {e}")
    total_tests += 1
    
    try:
        from unit.reactor.fixed_bed import FixedBedReactor
        fixedbr = FixedBedReactor(L=6.0, D=1.2, name="TestFixedBedReactor")
        print(f"✓ FixedBedReactor instantiated: {fixedbr.name}")
        success_count += 1
    except Exception as e:
        print(f"✗ FixedBedReactor instantiation failed: {e}")
    total_tests += 1
    
    print("=" * 50)
    print(f"Instantiation test results: {success_count}/{total_tests} modules instantiated successfully")
    
    if success_count == total_tests:
        print("All modules instantiated successfully!")
        return True
    else:
        print(f"⚠️  {total_tests - success_count} modules failed to instantiate")
        return False

if __name__ == "__main__":
    test_instantiation()
