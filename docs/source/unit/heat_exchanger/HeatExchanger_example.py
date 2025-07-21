"""
Industrial Example: Crude Oil Preheat Train Heat Exchanger
Typical refinery application with realistic plant conditions and scale

This example demonstrates a shell-and-tube heat exchanger used in crude oil preheating,
a common application in petroleum refineries for energy integration and efficiency.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the parent directory to the Python path to import HeatExchanger
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from sproclib.unit.heat_exchanger.HeatExchanger import HeatExchanger

# =============================================================================
# Process Conditions (Typical Industrial Scale - Crude Oil Preheat Train)
# =============================================================================

print("=" * 80)
print("INDUSTRIAL HEAT EXCHANGER EXAMPLE")
print("Application: Crude Oil Preheat Train in Petroleum Refinery")
print("Configuration: Counter-current Shell-and-Tube Heat Exchanger")
print("=" * 80)

# Heat Exchanger Design Parameters
U = 180.0               # W/m²·K - Overall heat transfer coefficient (crude oil/gas oil)
A = 450.0              # m² - Heat transfer area (typical industrial size)
m_hot = 25.0           # kg/s - Hot gas oil flow rate (90 m³/h @ 0.85 kg/L)
m_cold = 30.0          # kg/s - Cold crude oil flow rate (108 m³/h @ 0.92 kg/L)

# Fluid Properties
cp_hot = 2400.0        # J/kg·K - Gas oil specific heat capacity
cp_cold = 2100.0       # J/kg·K - Crude oil specific heat capacity
V_hot = 8.5            # m³ - Hot side volume (shell side)
V_cold = 6.2           # m³ - Cold side volume (tube side)
rho_hot = 850.0        # kg/m³ - Gas oil density at operating temperature
rho_cold = 920.0       # kg/m³ - Crude oil density at operating temperature

print(f"\nDESIGN PARAMETERS:")
print(f"Overall Heat Transfer Coefficient (U): {U:.1f} W/m²·K")
print(f"Heat Transfer Area (A): {A:.1f} m²")
print(f"Hot Side Flow Rate (Gas Oil): {m_hot:.1f} kg/s ({m_hot*3.6/rho_hot*1000:.1f} m³/h)")
print(f"Cold Side Flow Rate (Crude Oil): {m_cold:.1f} kg/s ({m_cold*3.6/rho_cold*1000:.1f} m³/h)")

# Create heat exchanger instance
hx = HeatExchanger(
    U=U, A=A,
    m_hot=m_hot, m_cold=m_cold,
    cp_hot=cp_hot, cp_cold=cp_cold,
    V_hot=V_hot, V_cold=V_cold,
    rho_hot=rho_hot, rho_cold=rho_cold,
    name="CrudeOilPreheater"
)

# =============================================================================
# Operating Conditions Analysis
# =============================================================================

# Typical operating temperatures (K)
T_hot_in = 473.15      # 200°C - Hot gas oil inlet temperature
T_cold_in = 313.15     # 40°C - Cold crude oil inlet temperature

print(f"\nOPERATING CONDITIONS:")
print(f"Hot Gas Oil Inlet Temperature: {T_hot_in-273.15:.1f}°C ({T_hot_in:.1f} K)")
print(f"Cold Crude Oil Inlet Temperature: {T_cold_in-273.15:.1f}°C ({T_cold_in:.1f} K)")
print(f"Operating Pressure: 15 bar (typical crude unit pressure)")

# Calculate steady-state performance
u_design = np.array([T_hot_in, T_cold_in])
T_outlets = hx.steady_state(u_design)
T_hot_out, T_cold_out = T_outlets

print(f"\nSTEADY-STATE RESULTS:")
print(f"Hot Gas Oil Outlet Temperature: {T_hot_out-273.15:.1f}°C ({T_hot_out:.1f} K)")
print(f"Cold Crude Oil Outlet Temperature: {T_cold_out-273.15:.1f}°C ({T_cold_out:.1f} K)")

# =============================================================================
# Heat Transfer Analysis
# =============================================================================

# Calculate heat transfer performance
Q = hx.calculate_heat_transfer_rate(T_hot_in, T_cold_in, T_hot_out, T_cold_out)
lmtd = hx.calculate_lmtd(T_hot_in, T_cold_in, T_hot_out, T_cold_out)

print(f"\nHEAT TRANSFER PERFORMANCE:")
print(f"Heat Transfer Rate (Q): {Q/1e6:.2f} MW")
print(f"Log Mean Temperature Difference (LMTD): {lmtd:.1f} K")
print(f"Heat Exchanger Effectiveness: {hx.effectiveness:.3f}")
print(f"Number of Transfer Units (NTU): {hx.NTU:.2f}")

# Dimensionless groups
C_hot = hx.C_hot
C_cold = hx.C_cold
C_min = min(C_hot, C_cold)
C_max = max(C_hot, C_cold)
C_ratio = C_min / C_max

print(f"\nDIMENSIONLESS ANALYSIS:")
print(f"Hot Side Heat Capacity Rate (C_hot): {C_hot/1e3:.1f} kW/K")
print(f"Cold Side Heat Capacity Rate (C_cold): {C_cold/1e3:.1f} kW/K")
print(f"Heat Capacity Rate Ratio (Cr): {C_ratio:.3f}")

# =============================================================================
# Energy Integration Analysis
# =============================================================================

# Calculate energy savings compared to no heat integration
Q_max_theoretical = C_min * (T_hot_in - T_cold_in)
energy_recovery_efficiency = Q / Q_max_theoretical

# Economic impact (rough estimate)
fuel_heating_value = 42e6  # J/kg - typical fuel oil heating value
fuel_cost = 0.8  # $/kg - typical fuel cost
hours_per_year = 8000  # operating hours per year
furnace_efficiency = 0.85  # typical furnace efficiency

fuel_savings_kg_h = Q / (fuel_heating_value * furnace_efficiency)  # kg/h fuel saved
annual_fuel_savings = fuel_savings_kg_h * hours_per_year * fuel_cost  # $/year

print(f"\nENERGY INTEGRATION BENEFITS:")
print(f"Maximum Theoretical Heat Transfer: {Q_max_theoretical/1e6:.2f} MW")
print(f"Energy Recovery Efficiency: {energy_recovery_efficiency:.1%}")
print(f"Fuel Savings: {fuel_savings_kg_h:.1f} kg/h")
print(f"Annual Cost Savings: ${annual_fuel_savings/1e3:.1f}k/year")

# =============================================================================
# Process Sensitivity Analysis
# =============================================================================

print(f"\nSENSITIVITY ANALYSIS:")

# Flow rate sensitivity
flow_ratios = np.linspace(0.5, 1.5, 11)
effectiveness_vs_flow = []
Q_vs_flow = []

for ratio in flow_ratios:
    m_hot_var = m_hot * ratio
    m_cold_var = m_cold * ratio
    
    # Create temporary heat exchanger with varied flow rates
    hx_temp = HeatExchanger(
        U=U, A=A,
        m_hot=m_hot_var, m_cold=m_cold_var,
        cp_hot=cp_hot, cp_cold=cp_cold,
        V_hot=V_hot, V_cold=V_cold,
        rho_hot=rho_hot, rho_cold=rho_cold
    )
    
    effectiveness_vs_flow.append(hx_temp.effectiveness)
    
    # Calculate heat transfer at design conditions
    T_out_temp = hx_temp.steady_state(u_design)
    Q_temp = hx_temp.calculate_heat_transfer_rate(T_hot_in, T_cold_in, T_out_temp[0], T_out_temp[1])
    Q_vs_flow.append(Q_temp / 1e6)  # MW

print(f"Flow Rate Sensitivity (±50% of design):")
print(f"  50% Flow: Effectiveness = {effectiveness_vs_flow[0]:.3f}, Q = {Q_vs_flow[0]:.2f} MW")
print(f"  Design Flow: Effectiveness = {effectiveness_vs_flow[5]:.3f}, Q = {Q_vs_flow[5]:.2f} MW")
print(f"  150% Flow: Effectiveness = {effectiveness_vs_flow[10]:.3f}, Q = {Q_vs_flow[10]:.2f} MW")

# Temperature sensitivity
T_hot_variations = np.array([450, 460, 470, 480, 490]) + 273.15  # K
Q_vs_temp = []

for T_hot_var in T_hot_variations:
    u_temp = np.array([T_hot_var, T_cold_in])
    T_out_temp = hx.steady_state(u_temp)
    Q_temp = hx.calculate_heat_transfer_rate(T_hot_var, T_cold_in, T_out_temp[0], T_out_temp[1])
    Q_vs_temp.append(Q_temp / 1e6)

print(f"\nHot Inlet Temperature Sensitivity:")
for i, T_hot_var in enumerate(T_hot_variations):
    print(f"  {T_hot_var-273.15:.0f}°C: Q = {Q_vs_temp[i]:.2f} MW")

# =============================================================================
# Comparison with Perry's Handbook Correlations
# =============================================================================

print(f"\nCOMPARISON WITH HANDBOOK CORRELATIONS:")

# Calculate heat transfer coefficient from empirical correlations
# (Simplified Dittus-Boelter for turbulent flow in tubes)

# Assume tube diameter and properties for Reynolds number calculation
D_tube = 0.025  # m - typical tube diameter
mu_hot = 0.001  # Pa·s - gas oil viscosity at operating temperature
mu_cold = 0.005  # Pa·s - crude oil viscosity at operating temperature

# Velocity calculation (simplified)
A_cross_tube = np.pi * (D_tube/2)**2  # m²
n_tubes = 200  # estimated number of tubes
v_cold = m_cold / (rho_cold * n_tubes * A_cross_tube)  # m/s

# Reynolds number for cold side (crude oil in tubes)
Re_cold = rho_cold * v_cold * D_tube / mu_cold

print(f"Estimated Tube Side Velocity: {v_cold:.2f} m/s")
print(f"Tube Side Reynolds Number: {Re_cold:.0f}")

# Thermal boundary layer considerations
Pr_cold = mu_cold * cp_cold / 0.14  # Prandtl number (k = 0.14 W/m·K for crude oil)
print(f"Tube Side Prandtl Number: {Pr_cold:.1f}")

if Re_cold > 2300:
    print("Flow Regime: Turbulent (typical for industrial heat exchangers)")
else:
    print("Flow Regime: Laminar (unusual for industrial scale)")

# =============================================================================
# Scale-up Considerations
# =============================================================================

print(f"\nSCALE-UP CONSIDERATIONS:")
print(f"Current Heat Duty: {Q/1e6:.1f} MW")
print(f"Heat Flux: {Q/A:.0f} W/m² (within typical range: 5,000-50,000 W/m²)")
print(f"Area Density: {A/V_hot:.1f} m²/m³ (shell side)")

# Fouling considerations
fouling_factor = 0.0002  # m²·K/W - typical for crude oil service
U_clean = 1 / (1/U - fouling_factor)
print(f"Clean Overall HTC (U_clean): {U_clean:.0f} W/m²·K")
print(f"Design U with Fouling: {U:.0f} W/m²·K")
print(f"Fouling Margin: {(U_clean - U)/U_clean:.1%}")

# =============================================================================
# Performance Monitoring Recommendations
# =============================================================================

print(f"\nPERFORMANCE MONITORING RECOMMENDATIONS:")
print(f"Key Process Variables to Monitor:")
print(f"  • Inlet/Outlet temperatures (±2°C accuracy)")
print(f"  • Flow rates (±5% accuracy)")
print(f"  • Pressure drop across exchanger (<20 kPa typical)")
print(f"  • Fouling rate (effectiveness degradation)")

print(f"\nMaintenance Indicators:")
print(f"  • Effectiveness drop below {hx.effectiveness*0.9:.3f} indicates fouling")
print(f"  • LMTD increase above {lmtd*1.2:.1f} K suggests performance degradation")

print(f"\nExample completed successfully!")
print(f"Results demonstrate typical industrial heat exchanger performance")
print(f"with realistic crude oil processing conditions and scale.")
print("=" * 80)
