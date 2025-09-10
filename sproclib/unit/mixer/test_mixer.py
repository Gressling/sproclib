#!/usr/bin/env python3
"""
Simple test to verify the Mixer implementation works correctly.
"""

import numpy as np
import sys
import os

# Add the mixer directory to the path
sys.path.append(os.path.dirname(__file__))

from Mixer import Mixer


def test_mixer_basic():
    """Test basic mixer functionality"""
    print("Testing Mixer Implementation")
    print("=" * 40)
    
    # Create a simple 2-stream mixer
    mixer = Mixer(
        n_inlets=2,
        mixing_efficiency=0.95,
        volume=2.0,
        heat_transfer_coeff=100.0,
        ambient_temp=298.15,
        pressure_drop=5000.0,
        name="TestMixer"
    )
    
    # Test steady-state calculation
    print("\n1. Testing steady-state calculation:")
    
    # Two streams: hot and cold water
    flow_1 = 10.0    # kg/s
    temp_1 = 353.15  # 80°C  
    pres_1 = 300000  # 3 bar
    
    flow_2 = 10.0    # kg/s
    temp_2 = 273.15  # 0°C
    pres_2 = 310000  # 3.1 bar
    
    u = np.array([flow_1, temp_1, pres_1, flow_2, temp_2, pres_2])
    
    result = mixer.steady_state(u)
    flow_out, temp_out, pres_out = result
    
    print(f"   Input stream 1: {flow_1} kg/s at {temp_1-273.15:.1f}°C, {pres_1/1000:.0f} kPa")
    print(f"   Input stream 2: {flow_2} kg/s at {temp_2-273.15:.1f}°C, {pres_2/1000:.0f} kPa")
    print(f"   Output: {flow_out} kg/s at {temp_out-273.15:.1f}°C, {pres_out/1000:.0f} kPa")
    
    # Verify mass balance
    mass_balance_error = abs(flow_out - (flow_1 + flow_2))
    print(f"   Mass balance error: {mass_balance_error:.6f} kg/s")
    
    # Expected temperature (theoretical perfect mixing)
    expected_temp = (flow_1 * temp_1 + flow_2 * temp_2) / (flow_1 + flow_2)
    temp_error = abs(temp_out - expected_temp)
    print(f"   Temperature error vs. perfect mixing: {temp_error:.2f} K")
    
    # Test pressure calculation
    expected_pressure = min(pres_1, pres_2) - mixer.pressure_drop
    pressure_error = abs(pres_out - expected_pressure)
    print(f"   Pressure error: {pressure_error:.0f} Pa")
    
    print("\n2. Testing describe() method:")
    description = mixer.describe()
    print(f"   Type: {description['type']}")
    print(f"   Category: {description['category']}")
    print(f"   Parameters: {len(description['parameters'])} defined")
    print(f"   Applications: {len(description['applications'])} listed")
    
    # Test dynamic model (basic check)
    print("\n3. Testing dynamic model:")
    x = np.array([5.0, 5.0 * 4186.0 * 298.15])  # 5 kg at ambient temperature
    dx_dt = mixer.dynamics(0.0, x, u)
    print(f"   Initial state: {x}")
    print(f"   Derivatives: {dx_dt}")
    print(f"   Mass rate of change: {dx_dt[0]:.3f} kg/s")
    print(f"   Energy rate of change: {dx_dt[1]:.0f} J/s")
    
    # Basic validation checks
    print("\n4. Validation checks:")
    
    checks_passed = 0
    total_checks = 5
    
    # Check 1: Mass balance
    if mass_balance_error < 1e-10:
        print("   ✓ Mass balance: PASSED")
        checks_passed += 1
    else:
        print("   ✗ Mass balance: FAILED")
    
    # Check 2: Temperature reasonableness
    if min(temp_1, temp_2) <= temp_out <= max(temp_1, temp_2):
        print("   ✓ Temperature bounds: PASSED")
        checks_passed += 1
    else:
        print("   ✗ Temperature bounds: FAILED")
    
    # Check 3: Pressure calculation
    if pressure_error < 1000:  # Within 1 kPa
        print("   ✓ Pressure calculation: PASSED")
        checks_passed += 1
    else:
        print("   ✗ Pressure calculation: FAILED")
    
    # Check 4: Describe method completeness
    required_keys = ['type', 'description', 'parameters', 'applications']
    if all(key in description for key in required_keys):
        print("   ✓ Describe method: PASSED")
        checks_passed += 1
    else:
        print("   ✗ Describe method: FAILED")
    
    # Check 5: Dynamic model returns correct shape
    if len(dx_dt) == 2:
        print("   ✓ Dynamic model shape: PASSED")
        checks_passed += 1
    else:
        print("   ✗ Dynamic model shape: FAILED")
    
    print(f"\nOverall: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("🎉 All tests PASSED! Mixer implementation is working correctly.")
        return True
    else:
        print("❌ Some tests FAILED. Please check the implementation.")
        return False


if __name__ == "__main__":
    test_mixer_basic()
