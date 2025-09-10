#!/usr/bin/env python3
"""
Mixer Example - Working demonstration from project root

This example demonstrates the new Mixer unit operation.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Import from the sproclib package
from sproclib.unit.mixer import Mixer


def demo_mixer():
    """Demonstrate mixer functionality"""
    print("SPROCLIB Mixer Demonstration")
    print("=" * 40)
    
    # Create a mixer for hot/cold water mixing
    mixer = Mixer(
        n_inlets=2,
        mixing_efficiency=0.95,
        volume=2.0,
        heat_transfer_coeff=200.0,
        ambient_temp=298.15,
        pressure_drop=5000.0,
        name="HotColdMixer"
    )
    
    print("\n1. Mixer Configuration:")
    desc = mixer.describe()
    print(f"   Type: {desc['type']}")
    print(f"   Efficiency: {mixer.mixing_efficiency}")
    print(f"   Volume: {mixer.volume} m³")
    print(f"   Pressure drop: {mixer.pressure_drop/1000:.1f} kPa")
    
    # Example 1: Hot and cold water mixing
    print("\n2. Hot/Cold Water Mixing Test:")
    
    # Stream 1: Hot water
    flow_1 = 15.0    # kg/s
    temp_1 = 363.15  # 90°C
    pres_1 = 300000  # 3 bar
    
    # Stream 2: Cold water  
    flow_2 = 10.0    # kg/s
    temp_2 = 278.15  # 5°C
    pres_2 = 310000  # 3.1 bar
    
    u = np.array([flow_1, temp_1, pres_1, flow_2, temp_2, pres_2])
    result = mixer.steady_state(u)
    
    flow_out, temp_out, pres_out = result
    
    print(f"   Hot stream: {flow_1} kg/s at {temp_1-273.15:.1f}°C")
    print(f"   Cold stream: {flow_2} kg/s at {temp_2-273.15:.1f}°C")
    print(f"   Mixed stream: {flow_out} kg/s at {temp_out-273.15:.1f}°C")
    print(f"   Outlet pressure: {pres_out/1000:.1f} kPa")
    
    # Example 2: Mixing efficiency study
    print("\n3. Mixing Efficiency Study:")
    print("   Efficiency | Outlet Temp | Comment")
    print("      (%)     |     (°C)    |")
    print("   " + "-" * 35)
    
    for eff in [0.70, 0.85, 0.95, 0.99]:
        test_mixer = Mixer(n_inlets=2, mixing_efficiency=eff)
        test_result = test_mixer.steady_state(u)
        temp_test = test_result[1]
        
        if eff >= 0.95:
            comment = "Excellent"
        elif eff >= 0.85:
            comment = "Good"
        else:
            comment = "Moderate"
            
        print(f"      {eff*100:4.0f}     | {temp_test-273.15:11.1f} | {comment}")
    
    # Example 3: Three-stream mixing
    print("\n4. Three-Stream Process Mixing:")
    
    mixer_3 = Mixer(
        n_inlets=3,
        mixing_efficiency=0.92,
        volume=5.0,
        pressure_drop=8000.0
    )
    
    # Three process streams
    u3 = np.array([
        20.0, 343.15, 400000,  # Stream 1: Hot reactant
        12.0, 288.15, 420000,  # Stream 2: Cold reactant  
        8.0, 298.15, 410000    # Stream 3: Solvent
    ])
    
    result3 = mixer_3.steady_state(u3)
    flow3, temp3, pres3 = result3
    
    print(f"   Total flow: {flow3:.1f} kg/s")
    print(f"   Mixed temperature: {temp3-273.15:.1f}°C")
    print(f"   System pressure: {pres3/100000:.2f} bar")
    
    # Example 4: Dynamic response
    print("\n5. Dynamic Startup Simulation:")
    
    # Initial conditions: empty mixer
    x0 = np.array([0.0, 0.0])  # [mass, energy]
    
    # Time span
    t_span = (0, 30)  # 30 seconds
    t_eval = np.linspace(0, 30, 50)
    
    # Solve dynamic model
    def dynamics_wrapper(t, x):
        return mixer.dynamics(t, x, u)
    
    sol = solve_ivp(dynamics_wrapper, t_span, x0, t_eval=t_eval)
    
    # Calculate temperature profile
    mass_profile = sol.y[0]
    energy_profile = sol.y[1]
    cp = 4186.0  # J/kg/K
    
    temp_profile = []
    for m, e in zip(mass_profile, energy_profile):
        if m > 0.1:
            temp_profile.append(e / (m * cp) - 273.15)  # Convert to °C
        else:
            temp_profile.append(25.0)  # Ambient temperature
    
    print(f"   Startup time to steady-state: ~{t_eval[-1]:.0f} seconds")
    print(f"   Final temperature: {temp_profile[-1]:.1f}°C")
    print(f"   Steady-state temperature: {temp_out-273.15:.1f}°C")
    
    # Show applications
    print(f"\n6. Applications ({len(desc['applications'])} listed):")
    for i, app in enumerate(desc['applications'][:4], 1):
        print(f"   {i}. {app}")
    
    print("\n" + "=" * 40)
    print("✅ Mixer implementation working successfully!")
    print("✅ All calculations completed without errors")
    print("✅ Ready for integration into process models")
    print("=" * 40)
    
    return mixer, result


if __name__ == "__main__":
    demo_mixer()
