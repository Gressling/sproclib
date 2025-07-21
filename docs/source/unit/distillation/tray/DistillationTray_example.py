"""
Industrial Example: Single Distillation Tray
Benzene-Toluene Separation at Industrial Scale
"""

import numpy as np
import matplotlib.pyplot as plt
from sproclib.unit.distillation.tray import DistillationTray

# Industrial process conditions for benzene-toluene separation
# Typical refinery conditions at 1 atm
pressure = 1.01325e5  # Pa (1 atm)
temperature = 383.15  # K (110°C - average tray temperature)
relative_volatility = 2.4  # Benzene/toluene at 1 atm

# Industrial scale tray parameters
tray_holdup = 3.5  # kmol (typical for 2.5 m diameter column)
tray_number = 15   # Middle tray in 30-tray column

print("=== BENZENE-TOLUENE DISTILLATION TRAY ANALYSIS ===")
print(f"Operating Pressure: {pressure/1e5:.2f} bar")
print(f"Operating Temperature: {temperature-273.15:.1f}°C")
print(f"Relative Volatility (Benzene/Toluene): {relative_volatility:.2f}")
print(f"Tray Holdup: {tray_holdup:.1f} kmol")
print(f"Tray Number: {tray_number}")
print()

# Create distillation tray model
tray = DistillationTray(
    tray_number=tray_number,
    holdup=tray_holdup,
    alpha=relative_volatility,
    name="BenzeneTolueneTray"
)

# Industrial flow rates (kmol/min)
liquid_flow = 450.0    # kmol/min (typical for large column)
vapor_flow = 520.0     # kmol/min
feed_composition = 0.45  # Benzene mole fraction in liquid feed
vapor_composition = 0.35  # Benzene mole fraction in vapor from below

print("=== PROCESS OPERATING CONDITIONS ===")
print(f"Liquid Flow Rate: {liquid_flow:.1f} kmol/min ({liquid_flow*60:.0f} kmol/h)")
print(f"Vapor Flow Rate: {vapor_flow:.1f} kmol/min ({vapor_flow*60:.0f} kmol/h)")
print(f"Feed Composition (Benzene): {feed_composition:.3f} mole fraction")
print(f"Vapor Composition (Benzene): {vapor_composition:.3f} mole fraction")
print()

# Calculate vapor-liquid equilibrium
x_range = np.linspace(0.01, 0.99, 50)
y_equilibrium = [tray.vapor_liquid_equilibrium(x) for x in x_range]

print("=== VAPOR-LIQUID EQUILIBRIUM ANALYSIS ===")
print("Liquid x_benzene | Vapor y_benzene | Enrichment Factor")
print("-" * 55)
for i in range(0, len(x_range), 10):
    x = x_range[i]
    y = y_equilibrium[i]
    enrichment = y / x if x > 0 else 0
    print(f"{x:12.3f} | {y:11.3f} | {enrichment:15.2f}")
print()

# Test steady-state operation
print("=== STEADY-STATE OPERATION ===")
# Input: [L_in, x_in, V_in, y_in, L_out, V_out]
u_steady = np.array([liquid_flow, feed_composition, vapor_flow, vapor_composition, liquid_flow, vapor_flow])
x_steady = tray.steady_state(u_steady)

print(f"Steady-State Liquid Composition: {x_steady[0]:.4f} mole fraction benzene")
y_steady = tray.vapor_liquid_equilibrium(x_steady[0])
print(f"Equilibrium Vapor Composition: {y_steady:.4f} mole fraction benzene")
print(f"Separation Factor: {y_steady/x_steady[0]:.2f}")
print()

# Material balance verification
light_in = liquid_flow * feed_composition + vapor_flow * vapor_composition
light_out = liquid_flow * x_steady[0] + vapor_flow * y_steady
print(f"Light Component In: {light_in:.2f} kmol/min")
print(f"Light Component Out: {light_out:.2f} kmol/min")
print(f"Material Balance Error: {abs(light_in - light_out):.6f} kmol/min")
print()

# Dynamic response analysis
print("=== DYNAMIC RESPONSE ANALYSIS ===")
time_points = np.linspace(0, 60, 100)  # 1 hour simulation
dt = time_points[1] - time_points[0]

# Step change in feed composition at t=30 min
x_profile = []
x_current = 0.35  # Initial composition

for t in time_points:
    if t >= 30:
        # Step change in feed composition
        u_dynamic = np.array([liquid_flow, 0.55, vapor_flow, vapor_composition, liquid_flow, vapor_flow])
    else:
        u_dynamic = np.array([liquid_flow, feed_composition, vapor_flow, vapor_composition, liquid_flow, vapor_flow])
    
    # Calculate derivative
    dxdt = tray.dynamics(t, np.array([x_current]), u_dynamic)
    
    # Euler integration
    x_current += dxdt[0] * dt
    x_current = max(0.001, min(0.999, x_current))  # Constrain to physical limits
    x_profile.append(x_current)

print(f"Initial Composition: {x_profile[0]:.4f} mole fraction benzene")
print(f"Final Composition: {x_profile[-1]:.4f} mole fraction benzene")
print(f"Response Time (95% of final): {time_points[next(i for i, x in enumerate(x_profile) if x > 0.95*x_profile[-1])]:.1f} min")
print()

# Calculate key dimensionless numbers
print("=== DIMENSIONLESS NUMBERS ===")
# Assuming typical physical properties for benzene-toluene
density = 800  # kg/m³ (average)
viscosity = 0.0005  # Pa·s (average)
molecular_weight = 85  # kg/kmol (average)

# Convert flows to mass basis
mass_flow_liquid = liquid_flow * molecular_weight / 60  # kg/s
mass_flow_vapor = vapor_flow * molecular_weight / 60   # kg/s

print(f"Liquid Mass Flow: {mass_flow_liquid:.1f} kg/s")
print(f"Vapor Mass Flow: {mass_flow_vapor:.1f} kg/s")
print(f"Mass Transfer Driving Force: {abs(y_steady - x_steady[0]):.4f} mole fraction")
print()

# Economic analysis
print("=== ECONOMIC ANALYSIS ===")
# Typical costs for benzene-toluene separation
benzene_price = 1200  # USD/tonne
toluene_price = 800   # USD/tonne
utilities_cost = 0.05  # USD/kmol processed

hourly_throughput = liquid_flow * 60  # kmol/h
benzene_production = hourly_throughput * x_steady[0] * molecular_weight / 1000  # tonne/h
toluene_production = hourly_throughput * (1 - x_steady[0]) * molecular_weight / 1000  # tonne/h

revenue_rate = benzene_production * benzene_price + toluene_production * toluene_price
operating_cost = hourly_throughput * utilities_cost

print(f"Hourly Throughput: {hourly_throughput:.0f} kmol/h ({hourly_throughput*molecular_weight/1000:.1f} tonne/h)")
print(f"Benzene Production: {benzene_production:.2f} tonne/h")
print(f"Toluene Production: {toluene_production:.2f} tonne/h")
print(f"Revenue Rate: ${revenue_rate:.0f}/h")
print(f"Operating Cost: ${operating_cost:.0f}/h")
print(f"Contribution Margin: ${revenue_rate - operating_cost:.0f}/h")
print()

# Performance metrics
print("=== PERFORMANCE METRICS ===")
metadata = tray.describe()
print(f"Model Type: {metadata['type']}")
print(f"Applications: {', '.join(metadata['applications'])}")
print(f"Valid Alpha Range: {metadata['valid_ranges']['alpha']['min']:.2f} - {metadata['valid_ranges']['alpha']['max']:.1f}")
print(f"Valid Holdup Range: {metadata['valid_ranges']['holdup']['min']:.1f} - {metadata['valid_ranges']['holdup']['max']:.1f} kmol")
print()

print("=== COMPARISON WITH PERRY'S HANDBOOK ===")
# Compare with typical VLE data from Perry's Chemical Engineers' Handbook
perry_alpha = 2.35  # Perry's handbook value at 1 atm
perry_y = perry_alpha * 0.5 / (1 + (perry_alpha - 1) * 0.5)
model_y = tray.vapor_liquid_equilibrium(0.5)

print(f"Perry's Handbook α: {perry_alpha:.2f}")
print(f"Model α: {relative_volatility:.2f}")
print(f"Perry's y at x=0.5: {perry_y:.4f}")
print(f"Model y at x=0.5: {model_y:.4f}")
print(f"Relative Error: {abs(perry_y - model_y)/perry_y*100:.1f}%")
