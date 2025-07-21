"""
Industrial Example: Natural Gas Pipeline Compression Station
Typical plant conditions and scale for transmission pipeline applications
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

import numpy as np
import matplotlib.pyplot as plt
from sproclib.unit.compressor.Compressor import Compressor

print("="*60)
print("NATURAL GAS PIPELINE COMPRESSION STATION ANALYSIS")
print("="*60)

# Process conditions (typical transmission pipeline)
print("\n1. DESIGN CONDITIONS")
print("-" * 20)
P_suction = 40e5      # Pa (40 bar) - typical pipeline pressure
P_discharge = 80e5    # Pa (80 bar) - boosted pressure  
T_suction = 288.15    # K (15°C) - ground temperature
eta_isentropic = 0.82 # Typical for centrifugal compressor
gamma = 1.27          # Natural gas (mostly methane)
M_gas = 0.0175        # kg/mol (natural gas mixture)
flow_rate = 1500.0    # mol/s (equivalent to ~40,000 Nm³/h)

print(f"Suction Pressure:    {P_suction/1e5:.1f} bar")
print(f"Discharge Pressure:  {P_discharge/1e5:.1f} bar") 
print(f"Pressure Ratio:      {P_discharge/P_suction:.2f}")
print(f"Suction Temperature: {T_suction-273.15:.1f}°C")
print(f"Isentropic Efficiency: {eta_isentropic:.1%}")
print(f"Gas Flow Rate:       {flow_rate*22.4/1000:.1f} kNm³/h (at STP)")

# Create compressor model
compressor = Compressor(
    eta_isentropic=eta_isentropic,
    P_suction=P_suction,
    P_discharge=P_discharge, 
    T_suction=T_suction,
    gamma=gamma,
    M=M_gas,
    flow_nominal=flow_rate
)

# Calculate steady-state performance
u_design = np.array([P_suction, T_suction, P_discharge, flow_rate])
T_out, Power = compressor.steady_state(u_design)

print(f"\n2. COMPRESSION PERFORMANCE")
print("-" * 30)
print(f"Outlet Temperature:   {T_out-273.15:.1f}°C")
print(f"Temperature Rise:     {T_out-T_suction:.1f} K")
print(f"Compression Power:    {Power/1e6:.2f} MW")
print(f"Specific Power:       {Power/(flow_rate*M_gas*1000):.0f} kJ/kg")

# Compare with Perry's Handbook correlation (isentropic)
T_isentropic = T_suction * (P_discharge/P_suction)**((gamma-1)/gamma)
Power_isentropic = flow_rate * compressor.R * (T_isentropic - T_suction) / M_gas

print(f"\n3. COMPARISON WITH IDEAL ISENTROPIC")
print("-" * 40)
print(f"Ideal Outlet Temperature: {T_isentropic-273.15:.1f}°C")
print(f"Ideal Power:             {Power_isentropic/1e6:.2f} MW")
print(f"Efficiency Impact:       {(Power-Power_isentropic)/Power_isentropic:.1%} power increase")

# Dimensionless analysis
print(f"\n4. DIMENSIONLESS GROUPS")
print("-" * 25)
print(f"Pressure Ratio (P₂/P₁):     {P_discharge/P_suction:.2f}")
print(f"Temperature Ratio (T₂/T₁):  {T_out/T_suction:.3f}")
print(f"Efficiency Factor:          {eta_isentropic:.3f}")

# Operating envelope analysis
print(f"\n5. OPERATING ENVELOPE ANALYSIS") 
print("-" * 35)

# Vary pressure ratio from 1.5 to 3.0
pressure_ratios = np.linspace(1.5, 3.0, 10)
flow_rates = np.array([0.5, 1.0, 1.5]) * flow_rate  # 50%, 100%, 150% flow

results = {}
results['PR'] = pressure_ratios
results['flows'] = flow_rates

for i, flow in enumerate(flow_rates):
    temps = []
    powers = []
    
    for pr in pressure_ratios:
        P_dis = P_suction * pr
        u = np.array([P_suction, T_suction, P_dis, flow])
        T_out_calc, Power_calc = compressor.steady_state(u)
        temps.append(T_out_calc - 273.15)  # Convert to °C
        powers.append(Power_calc / 1e6)    # Convert to MW
    
    results[f'T_out_{int(flow/flow_rate*100)}%'] = temps
    results[f'Power_{int(flow/flow_rate*100)}%'] = powers
    
    print(f"\nFlow = {flow/flow_rate:.0%} of design:")
    for j, pr in enumerate(pressure_ratios[::2]):  # Show every other point
        print(f"  PR={pr:.1f}: T_out={temps[j*2]:.0f}°C, Power={powers[j*2]:.1f}MW")

# Scale-up considerations
print(f"\n6. SCALE-UP CONSIDERATIONS")
print("-" * 30)
print("Mechanical limits:")
print(f"  - Max tip speed: ~250-300 m/s (centrifugal)")
print(f"  - Max outlet temp: 150°C (material limits)")
print(f"  - Surge margin: 15-20% above surge line")
print(f"  - Current outlet temp: {T_out-273.15:.0f}°C ({'OK' if T_out-273.15 < 150 else 'HIGH'})")

# Economic analysis
print(f"\n7. ECONOMIC IMPACT")
print("-" * 20)
electricity_cost = 0.08  # $/kWh
operating_hours = 8760   # hours/year
annual_energy_cost = Power/1000 * operating_hours * electricity_cost

print(f"Annual electricity cost: ${annual_energy_cost/1e6:.2f}M")
print(f"Cost per Nm³ compressed: ${annual_energy_cost/(flow_rate*22.4*operating_hours/1000)*1000:.3f}/kNm³")

# Safety considerations  
print(f"\n8. SAFETY & OPERATIONAL LIMITS")
print("-" * 35)
max_temp_rise = 100  # K, typical limit
current_temp_rise = T_out - T_suction

print(f"Temperature rise limit: {max_temp_rise} K")
print(f"Current temperature rise: {current_temp_rise:.1f} K")
print(f"Safety margin: {(max_temp_rise - current_temp_rise)/max_temp_rise:.1%}")

if current_temp_rise > max_temp_rise:
    print("WARNING: Exceeds temperature rise limit!")
else:
    print("Within safe operating limits")

print(f"\n9. COMPARISON WITH INDUSTRY STANDARDS")
print("-" * 40)
print("Typical pipeline compressor performance:")
print("  - Efficiency: 80-85% (current: {:.1%})".format(eta_isentropic))
print("  - Pressure ratio: 1.5-2.5 per stage (current: {:.1f})".format(P_discharge/P_suction))
print("  - Specific power: 15-25 kJ/kg (current: {:.0f} kJ/kg)".format(Power/(flow_rate*M_gas*1000)))

# Display metadata
print(f"\n10. MODEL METADATA")
print("-" * 20)
metadata = compressor.describe()
print(f"Model type: {metadata['type']}")
print(f"Category: {metadata['category']}")
print("Key applications:")
for app in metadata['applications'][:3]:
    print(f"  - {app}")
print("Main limitations:")
for lim in metadata['limitations'][:3]:
    print(f"  - {lim}")

print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
