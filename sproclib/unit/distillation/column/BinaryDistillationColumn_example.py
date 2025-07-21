"""
Industrial Example: Binary Distillation Column
Ethanol-Water Separation for Bioethanol Production
"""

import numpy as np
import matplotlib.pyplot as plt
from sproclib.unit.distillation.column import BinaryDistillationColumn

# Industrial bioethanol production parameters
# Typical industrial scale ethanol distillation
pressure = 1.01325e5  # Pa (1 atm)
temperature_range = [78.3, 100.0]  # °C (ethanol bp to water bp)
relative_volatility = 8.0  # Ethanol/water at 1 atm (average)

# Industrial column specifications
N_trays = 35          # Typical for ethanol purification
feed_tray = 18        # Optimal feed location (~50% from bottom)
column_diameter = 3.5  # m (typical industrial scale)
tray_spacing = 0.6    # m (typical)

print("=== BIOETHANOL DISTILLATION COLUMN ANALYSIS ===")
print(f"Operating Pressure: {pressure/1e5:.2f} bar")
print(f"Temperature Range: {temperature_range[0]:.1f} - {temperature_range[1]:.1f}°C")
print(f"Relative Volatility (Ethanol/Water): {relative_volatility:.1f}")
print(f"Number of Trays: {N_trays}")
print(f"Feed Tray Location: {feed_tray}")
print(f"Column Diameter: {column_diameter:.1f} m")
print()

# Create binary distillation column model
column = BinaryDistillationColumn(
    N_trays=N_trays,
    feed_tray=feed_tray,
    alpha=relative_volatility,
    tray_holdup=4.0,  # kmol per tray (industrial scale)
    reflux_drum_holdup=25.0,  # kmol
    reboiler_holdup=40.0,  # kmol
    feed_flow=500.0,  # kmol/min (large bioethanol plant)
    feed_composition=0.12,  # 12% ethanol (typical fermentation)
    name="BioethanolColumn"
)

# Industrial operating conditions
reflux_ratio = 4.5    # High reflux for high purity ethanol
reboiler_duty = 12000  # kW (energy input)
distillate_flow = 55.0  # kmol/min (targeting 95% ethanol)
bottoms_flow = 445.0   # kmol/min (stillage)

print("=== PROCESS OPERATING CONDITIONS ===")
print(f"Feed Flow Rate: {column.feed_flow:.1f} kmol/min ({column.feed_flow*60:.0f} kmol/h)")
print(f"Feed Composition: {column.feed_composition:.3f} mole fraction ethanol")
print(f"Reflux Ratio: {reflux_ratio:.1f}")
print(f"Reboiler Duty: {reboiler_duty:.0f} kW")
print(f"Distillate Flow: {distillate_flow:.1f} kmol/min")
print(f"Bottoms Flow: {bottoms_flow:.1f} kmol/min")
print()

# Calculate minimum reflux ratio
R_min = column.calculate_minimum_reflux()
print(f"Minimum Reflux Ratio: {R_min:.2f}")
print(f"Operating Reflux Ratio: {reflux_ratio:.2f}")
print(f"Reflux Ratio Factor: {reflux_ratio/R_min:.2f} × R_min")
print()

# Steady-state operation
print("=== STEADY-STATE OPERATION ===")
u_operating = np.array([reflux_ratio, reboiler_duty, distillate_flow, bottoms_flow])
x_steady = column.steady_state(u_operating)

# Extract key compositions
x_distillate = x_steady[N_trays]      # Reflux drum composition
x_bottoms = x_steady[N_trays + 1]     # Reboiler composition
x_feed_tray = x_steady[feed_tray - 1] # Feed tray composition

print(f"Distillate Composition: {x_distillate:.4f} mole fraction ethanol ({x_distillate*100:.1f}%)")
print(f"Bottoms Composition: {x_bottoms:.4f} mole fraction ethanol ({x_bottoms*100:.2f}%)")
print(f"Feed Tray Composition: {x_feed_tray:.4f} mole fraction ethanol ({x_feed_tray*100:.1f}%)")
print()

# Calculate separation performance
metrics = column.calculate_separation_metrics(x_steady)
print("=== SEPARATION PERFORMANCE ===")
print(f"Distillate Purity: {metrics['distillate_purity']*100:.1f}% ethanol")
print(f"Bottoms Purity: {metrics['bottoms_purity']*100:.1f}% water")
print(f"Ethanol Recovery: {metrics['light_recovery']*100:.1f}%")
print(f"Separation Factor: {metrics['separation_factor']:.1f}")
print()

# Mass balance verification
print("=== MASS BALANCE VERIFICATION ===")
total_feed = column.feed_flow
total_products = distillate_flow + bottoms_flow
ethanol_in = total_feed * column.feed_composition
ethanol_out = distillate_flow * x_distillate + bottoms_flow * x_bottoms

print(f"Total Feed: {total_feed:.1f} kmol/min")
print(f"Total Products: {total_products:.1f} kmol/min")
print(f"Overall Balance Error: {abs(total_feed - total_products):.3f} kmol/min")
print(f"Ethanol In: {ethanol_in:.2f} kmol/min")
print(f"Ethanol Out: {ethanol_out:.2f} kmol/min")
print(f"Component Balance Error: {abs(ethanol_in - ethanol_out):.3f} kmol/min")
print()

# Production rates and economics
print("=== PRODUCTION ANALYSIS ===")
# Molecular weights
MW_ethanol = 46.07  # kg/kmol
MW_water = 18.015   # kg/kmol
MW_avg_distillate = x_distillate * MW_ethanol + (1 - x_distillate) * MW_water
MW_avg_bottoms = x_bottoms * MW_ethanol + (1 - x_bottoms) * MW_water

# Production rates
ethanol_production = distillate_flow * x_distillate * MW_ethanol / 1000  # tonne/min
water_production = bottoms_flow * (1 - x_bottoms) * MW_water / 1000     # tonne/min

# Daily production
daily_ethanol = ethanol_production * 60 * 24  # tonne/day
daily_water = water_production * 60 * 24      # tonne/day

print(f"Ethanol Production: {ethanol_production:.3f} tonne/min ({daily_ethanol:.1f} tonne/day)")
print(f"Water Production: {water_production:.3f} tonne/min ({daily_water:.1f} tonne/day)")
print(f"Distillate Density: {MW_avg_distillate:.1f} kg/kmol")
print(f"Bottoms Density: {MW_avg_bottoms:.1f} kg/kmol")
print()

# Energy analysis
print("=== ENERGY ANALYSIS ===")
# Energy requirements (typical values)
latent_heat_ethanol = 38.56  # kJ/mol
latent_heat_water = 40.66    # kJ/mol
specific_energy = reboiler_duty / (distillate_flow * 60)  # kJ/kmol distillate

print(f"Reboiler Duty: {reboiler_duty:.0f} kW")
print(f"Specific Energy: {specific_energy:.0f} kJ/kmol distillate")
print(f"Energy per kg Ethanol: {specific_energy/MW_ethanol:.0f} kJ/kg")
print(f"Daily Energy Consumption: {reboiler_duty*24:.0f} kWh/day")
print()

# Column profile analysis
print("=== COLUMN PROFILE ANALYSIS ===")
print("Tray | Composition | Temperature | Vapor Flow | Liquid Flow")
print("     | (mol frac)  |     (°C)    |  (kmol/min) | (kmol/min)")
print("-" * 65)

# Calculate internal flows
L_rectifying = reflux_ratio * distillate_flow
V_rectifying = L_rectifying + distillate_flow
L_stripping = L_rectifying + column.feed_flow
V_stripping = V_rectifying

# Estimate temperatures using Antoine equation approximation
def estimate_temperature(x_ethanol):
    """Estimate temperature using bubble point approximation"""
    if x_ethanol < 0.001:
        return 100.0  # Pure water
    elif x_ethanol > 0.999:
        return 78.3   # Pure ethanol
    else:
        # Linear approximation for illustration
        return 100.0 - (100.0 - 78.3) * x_ethanol

# Display key trays
key_trays = [1, 5, 10, feed_tray, 20, 25, N_trays]
for tray in key_trays:
    if tray <= N_trays:
        x_tray = x_steady[tray - 1]
        temp = estimate_temperature(x_tray)
        L_flow = L_rectifying if tray < feed_tray else L_stripping
        V_flow = V_rectifying if tray < feed_tray else V_stripping
        print(f"{tray:4d} | {x_tray:10.4f} | {temp:10.1f} | {V_flow:11.1f} | {L_flow:11.1f}")

print()

# Scale-up considerations
print("=== SCALE-UP CONSIDERATIONS ===")
column_volume = np.pi * (column_diameter/2)**2 * N_trays * tray_spacing  # m³
superficial_velocity = V_rectifying * MW_avg_distillate / (3600 * 1.5)  # m/s (assuming vapor density ~1.5 kg/m³)
f_factor = superficial_velocity * np.sqrt(1.5)  # Flooding factor

print(f"Column Volume: {column_volume:.1f} m³")
print(f"Superficial Velocity: {superficial_velocity:.2f} m/s")
print(f"F-Factor: {f_factor:.2f} (should be < 3.0 for good operation)")
print(f"Capacity Factor: {(distillate_flow * 60) / (column_diameter**2):.1f} kmol/h/m²")
print()

# Economic evaluation
print("=== ECONOMIC EVALUATION ===")
ethanol_price = 600  # USD/tonne (fuel grade)
energy_cost = 0.08   # USD/kWh
maintenance_cost = 0.02  # USD/kmol feed

# Revenue and costs
daily_revenue = daily_ethanol * ethanol_price
daily_energy_cost = reboiler_duty * 24 * energy_cost
daily_maintenance = column.feed_flow * 60 * 24 * maintenance_cost

print(f"Daily Revenue: ${daily_revenue:.0f}")
print(f"Daily Energy Cost: ${daily_energy_cost:.0f}")
print(f"Daily Maintenance Cost: ${daily_maintenance:.0f}")
print(f"Daily Operating Margin: ${daily_revenue - daily_energy_cost - daily_maintenance:.0f}")
print(f"Energy Cost per kg Ethanol: ${daily_energy_cost/daily_ethanol:.2f}/kg")
print()

# Performance comparison with literature
print("=== COMPARISON WITH LITERATURE ===")
# Typical industrial ethanol column performance
typical_ethanol_purity = 0.95  # 95% ethanol
typical_energy_consumption = 2.8  # MJ/kg ethanol
model_energy_consumption = (reboiler_duty * 60) / (ethanol_production * 1000)  # MJ/kg

print(f"Typical Ethanol Purity: {typical_ethanol_purity*100:.1f}%")
print(f"Model Ethanol Purity: {x_distillate*100:.1f}%")
print(f"Typical Energy Consumption: {typical_energy_consumption:.1f} MJ/kg ethanol")
print(f"Model Energy Consumption: {model_energy_consumption:.1f} MJ/kg ethanol")
print(f"Energy Efficiency: {typical_energy_consumption/model_energy_consumption*100:.1f}% of typical")
print()

# Control implications
print("=== CONTROL IMPLICATIONS ===")
print("Key Control Variables:")
print(f"- Reflux Ratio: {reflux_ratio:.1f} (primary product quality control)")
print(f"- Reboiler Duty: {reboiler_duty:.0f} kW (energy input)")
print(f"- Distillate Flow: {distillate_flow:.1f} kmol/min (production rate)")
print()
print("Typical Control Objectives:")
print("- Maintain distillate purity > 95% ethanol")
print("- Minimize energy consumption")
print("- Maintain stable operation despite feed variations")
print("- Optimize ethanol recovery > 99%")
