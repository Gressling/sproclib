"""
Visualization script for Compressor performance analysis
Generates engineering plots for compressor behavior and sensitivity analysis
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

import numpy as np
import matplotlib.pyplot as plt
from sproclib.unit.compressor.Compressor import Compressor

# Set professional plot style
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

# Create compressor instance
compressor = Compressor(
    eta_isentropic=0.82,
    P_suction=40e5,      # 40 bar
    T_suction=288.15,    # 15°C
    gamma=1.27,          # Natural gas
    M=0.0175,            # kg/mol
    flow_nominal=1500.0  # mol/s
)

# PLOT 1: Performance Curves
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Natural Gas Compressor Performance Analysis', fontsize=16, fontweight='bold')

# Pressure ratio vs outlet temperature and power
pressure_ratios = np.linspace(1.2, 3.5, 50)
flow_rates = [750, 1500, 2250]  # 50%, 100%, 150% of nominal
colors = ['blue', 'red', 'green']
linestyles = ['--', '-', ':']

P_suction = 40e5
T_suction = 288.15

for i, (flow, color, linestyle) in enumerate(zip(flow_rates, colors, linestyles)):
    temps = []
    powers = []
    
    for pr in pressure_ratios:
        P_discharge = P_suction * pr
        u = np.array([P_suction, T_suction, P_discharge, flow])
        T_out, Power = compressor.steady_state(u)
        temps.append(T_out - 273.15)  # Convert to °C
        powers.append(Power / 1e6)    # Convert to MW
    
    ax1.plot(pressure_ratios, temps, color=color, linestyle=linestyle, 
             linewidth=2, label=f'{flow/1500:.0%} Flow ({flow:.0f} mol/s)')
    ax2.plot(pressure_ratios, powers, color=color, linestyle=linestyle,
             linewidth=2, label=f'{flow/1500:.0%} Flow ({flow:.0f} mol/s)')

# Format subplot 1 - Temperature
ax1.set_xlabel('Pressure Ratio (P₂/P₁)', fontweight='bold')
ax1.set_ylabel('Outlet Temperature (°C)', fontweight='bold')
ax1.set_title('Outlet Temperature vs Pressure Ratio')
ax1.legend()
ax1.axhline(y=150, color='red', linestyle='--', alpha=0.7, label='Material Limit')
ax1.set_ylim(0, 200)

# Format subplot 2 - Power
ax2.set_xlabel('Pressure Ratio (P₂/P₁)', fontweight='bold')
ax2.set_ylabel('Compression Power (MW)', fontweight='bold')
ax2.set_title('Power Consumption vs Pressure Ratio')
ax2.legend()

# PLOT 3: Efficiency sensitivity
efficiencies = np.linspace(0.6, 0.95, 20)
pr_fixed = 2.0
flow_fixed = 1500

temps_eff = []
powers_eff = []

for eta in efficiencies:
    comp_temp = Compressor(eta_isentropic=eta, P_suction=P_suction, 
                          T_suction=T_suction, gamma=1.27, M=0.0175)
    P_discharge = P_suction * pr_fixed
    u = np.array([P_suction, T_suction, P_discharge, flow_fixed])
    T_out, Power = comp_temp.steady_state(u)
    temps_eff.append(T_out - 273.15)
    powers_eff.append(Power / 1e6)

ax3.plot(efficiencies * 100, temps_eff, 'bo-', linewidth=2, markersize=4)
ax3.set_xlabel('Isentropic Efficiency (%)', fontweight='bold')
ax3.set_ylabel('Outlet Temperature (°C)', fontweight='bold')
ax3.set_title(f'Efficiency Impact (PR={pr_fixed}, Flow={flow_fixed} mol/s)')
ax3.axvline(x=82, color='red', linestyle='--', alpha=0.7, label='Design Point')
ax3.legend()

# PLOT 4: Specific power vs pressure ratio
specific_powers = []
for pr in pressure_ratios:
    P_discharge = P_suction * pr
    u = np.array([P_suction, T_suction, P_discharge, 1500])
    T_out, Power = compressor.steady_state(u)
    specific_power = Power / (1500 * 0.0175 * 1000)  # kJ/kg
    specific_powers.append(specific_power)

ax4.plot(pressure_ratios, specific_powers, 'g-', linewidth=3)
ax4.set_xlabel('Pressure Ratio (P₂/P₁)', fontweight='bold')
ax4.set_ylabel('Specific Power (kJ/kg)', fontweight='bold')
ax4.set_title('Specific Energy Consumption')
ax4.axhspan(15, 25, alpha=0.2, color='green', label='Typical Range')
ax4.legend()

plt.tight_layout()
plt.savefig('/Users/macmini/Desktop/github/sproclib/sproclib/unit/compressor/Compressor_example_plots.png', 
            dpi=300, bbox_inches='tight')
plt.close()

# PLOT 2: Detailed Analysis - Operating Map and Sensitivity
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Compressor Detailed Analysis & Operating Limits', fontsize=16, fontweight='bold')

# Operating map - Temperature contours
flow_range = np.linspace(500, 3000, 30)
pr_range = np.linspace(1.2, 3.5, 30)
Flow_grid, PR_grid = np.meshgrid(flow_range, pr_range)
Temp_grid = np.zeros_like(Flow_grid)

for i, pr in enumerate(pr_range):
    for j, flow in enumerate(flow_range):
        P_discharge = P_suction * pr
        u = np.array([P_suction, T_suction, P_discharge, flow])
        T_out, _ = compressor.steady_state(u)
        Temp_grid[i, j] = T_out - 273.15

contour = ax1.contour(Flow_grid, PR_grid, Temp_grid, levels=20, colors='black', alpha=0.5)
contourf = ax1.contourf(Flow_grid, PR_grid, Temp_grid, levels=20, cmap='viridis', alpha=0.8)
ax1.clabel(contour, inline=True, fontsize=8, fmt='%1.0f°C')
cbar1 = plt.colorbar(contourf, ax=ax1)
cbar1.set_label('Outlet Temperature (°C)', fontweight='bold')

# Add operating limits
ax1.axhline(y=3.0, color='red', linestyle='--', linewidth=2, label='Max PR per stage')
ax1.axhline(y=1.5, color='orange', linestyle='--', linewidth=2, label='Min economic PR')
ax1.set_xlabel('Flow Rate (mol/s)', fontweight='bold')
ax1.set_ylabel('Pressure Ratio', fontweight='bold')
ax1.set_title('Operating Map - Temperature Contours')
ax1.legend()

# Gas property sensitivity
gammas = [1.2, 1.27, 1.3, 1.4]  # Different gas compositions
gas_labels = ['Heavy HC', 'Natural Gas', 'CO₂', 'Air']
pr_test = 2.0

for gamma, label in zip(gammas, gas_labels):
    comp_gas = Compressor(eta_isentropic=0.82, gamma=gamma, M=0.0175)
    flow_test = np.linspace(500, 2500, 20)
    temps_gas = []
    
    for flow in flow_test:
        P_discharge = P_suction * pr_test
        u = np.array([P_suction, T_suction, P_discharge, flow])
        T_out, _ = comp_gas.steady_state(u)
        temps_gas.append(T_out - 273.15)
    
    ax2.plot(flow_test, temps_gas, linewidth=2, label=f'{label} (γ={gamma})')

ax2.set_xlabel('Flow Rate (mol/s)', fontweight='bold')
ax2.set_ylabel('Outlet Temperature (°C)', fontweight='bold')
ax2.set_title(f'Gas Property Sensitivity (PR={pr_test})')
ax2.legend()

# Polytropic efficiency comparison
n_values = np.linspace(1.15, 1.35, 20)  # Polytropic exponent range
temps_poly = []
powers_poly = []

for n in n_values:
    # Calculate equivalent gamma for comparison
    gamma_equiv = n / (n - 1) * (1.27 - 1) / 1.27 + 1
    comp_poly = Compressor(eta_isentropic=0.82, gamma=gamma_equiv, M=0.0175)
    
    P_discharge = P_suction * 2.0
    u = np.array([P_suction, T_suction, P_discharge, 1500])
    T_out, Power = comp_poly.steady_state(u)
    temps_poly.append(T_out - 273.15)
    powers_poly.append(Power / 1e6)

ax3.plot(n_values, temps_poly, 'b-o', linewidth=2, markersize=4, label='Temperature')
ax3_twin = ax3.twinx()
ax3_twin.plot(n_values, powers_poly, 'r-s', linewidth=2, markersize=4, label='Power')

ax3.set_xlabel('Polytropic Exponent (n)', fontweight='bold')
ax3.set_ylabel('Outlet Temperature (°C)', color='blue', fontweight='bold')
ax3_twin.set_ylabel('Power (MW)', color='red', fontweight='bold')
ax3.set_title('Polytropic Process Comparison')
ax3.tick_params(axis='y', labelcolor='blue')
ax3_twin.tick_params(axis='y', labelcolor='red')

# Economic optimization - Cost vs efficiency
efficiencies_econ = np.linspace(0.65, 0.95, 15)
capital_costs = []
operating_costs = []
total_costs = []

electricity_price = 0.08  # $/kWh
operating_hours = 8760   # h/year
project_life = 20        # years
discount_rate = 0.08

for eta in efficiencies_econ:
    comp_econ = Compressor(eta_isentropic=eta, M=0.0175)
    P_discharge = P_suction * 2.0
    u = np.array([P_suction, T_suction, P_discharge, 1500])
    T_out, Power = comp_econ.steady_state(u)
    
    # Estimate capital cost (higher efficiency = higher cost)
    base_capital = 5e6  # $5M base cost
    capital_cost = base_capital * (1 + 2 * (eta - 0.7))  # Cost premium for efficiency
    
    # Operating cost (electricity)
    annual_energy_cost = Power / 1000 * operating_hours * electricity_price
    pv_operating_cost = annual_energy_cost * ((1 - (1 + discount_rate)**(-project_life)) / discount_rate)
    
    total_cost = capital_cost + pv_operating_cost
    
    capital_costs.append(capital_cost / 1e6)
    operating_costs.append(pv_operating_cost / 1e6)
    total_costs.append(total_cost / 1e6)

ax4.plot(efficiencies_econ * 100, capital_costs, 'b-', linewidth=2, label='Capital Cost')
ax4.plot(efficiencies_econ * 100, operating_costs, 'r-', linewidth=2, label='Operating Cost (PV)')
ax4.plot(efficiencies_econ * 100, total_costs, 'g-', linewidth=3, label='Total Cost')

# Find optimal efficiency
min_idx = np.argmin(total_costs)
optimal_eff = efficiencies_econ[min_idx] * 100
ax4.axvline(x=optimal_eff, color='black', linestyle='--', alpha=0.7, 
           label=f'Optimal: {optimal_eff:.1f}%')

ax4.set_xlabel('Isentropic Efficiency (%)', fontweight='bold')
ax4.set_ylabel('Life Cycle Cost ($M)', fontweight='bold')
ax4.set_title('Economic Optimization')
ax4.legend()

plt.tight_layout()
plt.savefig('/Users/macmini/Desktop/github/sproclib/sproclib/unit/compressor/Compressor_detailed_analysis.png', 
            dpi=300, bbox_inches='tight')
plt.close()

print("Visualization files generated successfully:")
print("- Compressor_example_plots.png")
print("- Compressor_detailed_analysis.png")
