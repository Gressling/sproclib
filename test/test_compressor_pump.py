#!/usr/bin/env python3
"""
SPROCLIB - Standard Process Control Library
Test Script for Compressor and Pump Models

Author: Thorsten Gressling (gressling@paramus.ai)
License: MIT License
"""

import numpy as np
from models import Compressor, Pump, CentrifugalPump, PositiveDisplacementPump

def test_compressor():
    """Test gas compressor model."""
    print("Testing Compressor Model:")
    print("-" * 30)
    
    # Create compressor
    compressor = Compressor(
        eta_isentropic=0.75,
        P_suction=1e5,      # 1 bar
        P_discharge=5e5,    # 5 bar  
        T_suction=288.15,   # 15°C
        name="TestCompressor"
    )
    
    # Test steady-state calculation
    u = np.array([1e5, 300.0, 5e5, 10.0])  # [P_suc, T_suc, P_dis, flow]
    result = compressor.steady_state(u)
    
    print(f"✓ Compressor created: {compressor.name}")
    print(f"  Pressure ratio: {compressor.P_discharge/compressor.P_suction:.1f}")
    print(f"  Efficiency: {compressor.eta_isentropic:.1%}")
    print(f"  Outlet temperature: {result[0]-273.15:.1f} °C")
    print(f"  Power required: {result[1]/1000:.1f} kW")
    
    # Test dynamics
    x0 = np.array([result[0]])
    dx_dt = compressor.dynamics(0, x0, u)
    print(f"  Dynamic test: dT/dt = {dx_dt[0]:.3f} K/s")
    

def test_pumps():
    """Test pump models."""
    print("\nTesting Pump Models:")
    print("-" * 30)
    
    # Generic pump
    pump = Pump(eta=0.7, name="GenericPump")
    u = np.array([1e5, 0.01])  # [P_inlet, flow]
    result = pump.steady_state(u)
    print(f"✓ Generic Pump: P_out = {result[0]/1e5:.2f} bar, Power = {result[1]/1000:.1f} kW")
    
    # Centrifugal pump
    cent_pump = CentrifugalPump(H0=50.0, K=20.0, eta=0.72, name="CentrifugalPump")
    result = cent_pump.steady_state(u)
    print(f"✓ Centrifugal Pump: P_out = {result[0]/1e5:.2f} bar, Power = {result[1]/1000:.1f} kW")
    
    # Positive displacement pump
    pd_pump = PositiveDisplacementPump(flow_rate=0.008, eta=0.85, name="PDPump")
    u_pd = np.array([1e5])  # [P_inlet]
    result = pd_pump.steady_state(u_pd)
    print(f"✓ PD Pump: P_out = {result[0]/1e5:.2f} bar, Power = {result[1]/1000:.1f} kW")
    
    # Test dynamics
    x0 = np.array([result[0]])
    dx_dt = pd_pump.dynamics(0, x0, u_pd)
    print(f"  Dynamic test: dP/dt = {dx_dt[0]/1000:.1f} bar/s")


def test_performance_curves():
    """Test pump performance curves."""
    print("\nTesting Performance Curves:")
    print("-" * 30)
    
    cent_pump = CentrifugalPump(H0=60.0, K=15.0, eta=0.75)
    
    print("Flow [L/s]  Head [m]  Power [kW]")
    print("-" * 35)
    
    for flow in np.linspace(0.005, 0.018, 6):
        u = np.array([1e5, flow])
        result = cent_pump.steady_state(u)
        
        # Calculate head
        g = 9.81
        head = (result[0] - 1e5) / (cent_pump.rho * g)
        power = result[1] / 1000
        
        print(f"{flow*1000:8.1f}  {head:7.1f}  {power:8.2f}")


if __name__ == "__main__":
    try:
        test_compressor()
        test_pumps()
        test_performance_curves()
        print("\n✓ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
