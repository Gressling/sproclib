"""
Create visualization plots for heat exchanger analysis
Focus on chemical engineering insights with professional engineering plot style
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the parent directory to the Python path to import HeatExchanger
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from sproclib.unit.heat_exchanger.HeatExchanger import HeatExchanger

# Set professional plotting style
plt.style.use('default')
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

# Base case parameters (crude oil preheat train)
U_base = 180.0
A_base = 450.0
m_hot_base = 25.0
m_cold_base = 30.0
cp_hot = 2400.0
cp_cold = 2100.0
V_hot = 8.5
V_cold = 6.2
rho_hot = 850.0
rho_cold = 920.0

# Create base heat exchanger
hx_base = HeatExchanger(
    U=U_base, A=A_base,
    m_hot=m_hot_base, m_cold=m_cold_base,
    cp_hot=cp_hot, cp_cold=cp_cold,
    V_hot=V_hot, V_cold=V_cold,
    rho_hot=rho_hot, rho_cold=rho_cold
)

# Operating conditions
T_hot_in = 473.15  # K (200°C)
T_cold_in = 313.15  # K (40°C)

# =============================================================================
# Figure 1: Process Behavior and Performance Curves
# =============================================================================

fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
fig1.suptitle('Heat Exchanger Process Behavior - Industrial Crude Oil Preheat Train', 
              fontsize=16, fontweight='bold')

# Subplot 1: Effectiveness vs NTU for different heat capacity ratios
NTU_range = np.linspace(0.1, 5.0, 100)
C_ratios = [0.25, 0.5, 0.75, 1.0]
colors = ['blue', 'green', 'orange', 'red']

for i, Cr in enumerate(C_ratios):
    effectiveness = []
    for NTU in NTU_range:
        if abs(Cr - 1.0) < 1e-6:
            eff = NTU / (1 + NTU)
        else:
            exp_term = np.exp(-NTU * (1 - Cr))
            eff = (1 - exp_term) / (1 - Cr * exp_term)
        effectiveness.append(eff)
    
    ax1.plot(NTU_range, effectiveness, color=colors[i], linewidth=2, 
             label=f'Cr = {Cr}')

# Mark operating point
ax1.plot(hx_base.NTU, hx_base.effectiveness, 'ko', markersize=8, 
         label=f'Operating Point\n(NTU={hx_base.NTU:.2f}, ε={hx_base.effectiveness:.3f})')

ax1.set_xlabel('Number of Transfer Units (NTU) [-]')
ax1.set_ylabel('Effectiveness (ε) [-]')
ax1.set_title('Effectiveness-NTU Relationship\n(Counter-current Configuration)')
ax1.grid(True, alpha=0.3)
ax1.legend()
ax1.set_xlim(0, 5)
ax1.set_ylim(0, 1)

# Subplot 2: Heat transfer rate vs flow rate
flow_multipliers = np.linspace(0.3, 2.0, 50)
Q_vs_flow = []
effectiveness_vs_flow = []

for mult in flow_multipliers:
    hx_temp = HeatExchanger(
        U=U_base, A=A_base,
        m_hot=m_hot_base * mult, m_cold=m_cold_base * mult,
        cp_hot=cp_hot, cp_cold=cp_cold,
        V_hot=V_hot, V_cold=V_cold,
        rho_hot=rho_hot, rho_cold=rho_cold
    )
    
    u = np.array([T_hot_in, T_cold_in])
    T_out = hx_temp.steady_state(u)
    Q = hx_temp.calculate_heat_transfer_rate(T_hot_in, T_cold_in, T_out[0], T_out[1])
    
    Q_vs_flow.append(Q / 1e6)  # MW
    effectiveness_vs_flow.append(hx_temp.effectiveness)

flow_rates = flow_multipliers * m_hot_base

ax2.plot(flow_rates, Q_vs_flow, 'b-', linewidth=2, label='Heat Transfer Rate')
ax2.axvline(x=m_hot_base, color='red', linestyle='--', alpha=0.7, label='Design Point')
ax2.set_xlabel('Hot Side Flow Rate [kg/s]')
ax2.set_ylabel('Heat Transfer Rate [MW]')
ax2.set_title('Heat Transfer vs Flow Rate\n(Cold side flow scaled proportionally)')
ax2.grid(True, alpha=0.3)
ax2.legend()

# Add effectiveness on secondary y-axis
ax2_twin = ax2.twinx()
ax2_twin.plot(flow_rates, effectiveness_vs_flow, 'g--', linewidth=2, alpha=0.7)
ax2_twin.set_ylabel('Effectiveness [-]', color='green')
ax2_twin.tick_params(axis='y', labelcolor='green')

# Subplot 3: Temperature profiles
# Calculate temperature along the length (simplified 1D approximation)
length_fraction = np.linspace(0, 1, 20)
T_hot_profile = []
T_cold_profile = []

u_base = np.array([T_hot_in, T_cold_in])
T_out_base = hx_base.steady_state(u_base)

for x in length_fraction:
    # Linear approximation for temperature profile
    T_hot = T_hot_in - x * (T_hot_in - T_out_base[0])
    T_cold = T_cold_in + x * (T_out_base[1] - T_cold_in)
    T_hot_profile.append(T_hot - 273.15)  # Convert to °C
    T_cold_profile.append(T_cold - 273.15)

ax3.plot(length_fraction, T_hot_profile, 'r-', linewidth=3, label='Hot Side (Gas Oil)')
ax3.plot(length_fraction, T_cold_profile, 'b-', linewidth=3, label='Cold Side (Crude Oil)')
ax3.fill_between(length_fraction, T_hot_profile, T_cold_profile, alpha=0.2, color='yellow', label='ΔT Zone')
ax3.set_xlabel('Normalized Length [-]')
ax3.set_ylabel('Temperature [°C]')
ax3.set_title('Temperature Profiles\n(Counter-current Flow)')
ax3.grid(True, alpha=0.3)
ax3.legend()

# Subplot 4: Operating window (pressure-temperature limits)
T_hot_range = np.linspace(150, 250, 20) + 273.15  # K
pressure_range = np.linspace(5, 25, 20)  # bar

# Create operating envelope
T_mesh, P_mesh = np.meshgrid(T_hot_range - 273.15, pressure_range)
Q_mesh = np.zeros_like(T_mesh)

for i, P in enumerate(pressure_range):
    for j, T in enumerate(T_hot_range):
        u_temp = np.array([T, T_cold_in])
        T_out_temp = hx_base.steady_state(u_temp)
        Q_temp = hx_base.calculate_heat_transfer_rate(T, T_cold_in, T_out_temp[0], T_out_temp[1])
        Q_mesh[i, j] = Q_temp / 1e6  # MW

contour = ax4.contour(T_mesh, P_mesh, Q_mesh, levels=10, colors='black', alpha=0.5)
ax4.clabel(contour, inline=True, fontsize=8, fmt='%.1f MW')
contour_filled = ax4.contourf(T_mesh, P_mesh, Q_mesh, levels=20, cmap='viridis', alpha=0.7)

# Mark operating point
ax4.plot(T_hot_in - 273.15, 15, 'ro', markersize=10, label='Design Operating Point')

# Add safe operating limits
ax4.axhline(y=20, color='red', linestyle='--', alpha=0.8, label='Maximum Pressure')
ax4.axvline(x=220, color='orange', linestyle='--', alpha=0.8, label='Temperature Limit')

ax4.set_xlabel('Hot Inlet Temperature [°C]')
ax4.set_ylabel('Operating Pressure [bar]')
ax4.set_title('Operating Window\n(Heat Duty Contours)')
ax4.legend()

# Add colorbar
cbar = plt.colorbar(contour_filled, ax=ax4)
cbar.set_label('Heat Transfer Rate [MW]')

plt.tight_layout()
plt.savefig('/Users/macmini/Desktop/github/sproclib/sproclib/unit/heat_exchanger/HeatExchanger_example_plots.png', 
            bbox_inches='tight', dpi=300)
plt.close()

# =============================================================================
# Figure 2: Detailed Analysis - Parameter Sensitivity and Design Optimization
# =============================================================================

fig2, ((ax5, ax6), (ax7, ax8)) = plt.subplots(2, 2, figsize=(14, 10))
fig2.suptitle('Heat Exchanger Detailed Analysis - Parameter Sensitivity & Design Optimization', 
              fontsize=16, fontweight='bold')

# Subplot 5: Area vs Heat Transfer Coefficient sensitivity
U_range = np.linspace(50, 500, 30)
A_range = np.linspace(100, 800, 30)
U_mesh, A_mesh = np.meshgrid(U_range, A_range)
Q_sensitivity = np.zeros_like(U_mesh)

for i, A in enumerate(A_range):
    for j, U in enumerate(U_range):
        hx_temp = HeatExchanger(
            U=U, A=A,
            m_hot=m_hot_base, m_cold=m_cold_base,
            cp_hot=cp_hot, cp_cold=cp_cold,
            V_hot=V_hot, V_cold=V_cold,
            rho_hot=rho_hot, rho_cold=rho_cold
        )
        u = np.array([T_hot_in, T_cold_in])
        T_out = hx_temp.steady_state(u)
        Q = hx_temp.calculate_heat_transfer_rate(T_hot_in, T_cold_in, T_out[0], T_out[1])
        Q_sensitivity[i, j] = Q / 1e6  # MW

contour5 = ax5.contour(U_mesh, A_mesh, Q_sensitivity, levels=15, colors='black', alpha=0.6)
ax5.clabel(contour5, inline=True, fontsize=8, fmt='%.1f MW')
contour5_filled = ax5.contourf(U_mesh, A_mesh, Q_sensitivity, levels=20, cmap='plasma', alpha=0.8)

# Mark design point
ax5.plot(U_base, A_base, 'wo', markersize=10, markeredgecolor='black', markeredgewidth=2, 
         label=f'Design Point\n(U={U_base} W/m²·K, A={A_base} m²)')

ax5.set_xlabel('Overall Heat Transfer Coefficient [W/m²·K]')
ax5.set_ylabel('Heat Transfer Area [m²]')
ax5.set_title('Heat Duty Sensitivity\n(U vs A Design Space)')
ax5.legend()

# Add colorbar
cbar5 = plt.colorbar(contour5_filled, ax=ax5)
cbar5.set_label('Heat Transfer Rate [MW]')

# Subplot 6: Effectiveness vs Reynolds number (approximate)
Re_range = np.logspace(3, 6, 50)  # Reynolds number range
effectiveness_Re = []

# Approximate relationship: U ∝ Re^0.8 for turbulent flow
U_base_ref = U_base
Re_base = 5000  # Reference Reynolds number

for Re in Re_range:
    U_approx = U_base_ref * (Re / Re_base) ** 0.8
    # Limit U to realistic values
    U_approx = min(U_approx, 2000)
    
    hx_temp = HeatExchanger(
        U=U_approx, A=A_base,
        m_hot=m_hot_base, m_cold=m_cold_base,
        cp_hot=cp_hot, cp_cold=cp_cold,
        V_hot=V_hot, V_cold=V_cold,
        rho_hot=rho_hot, rho_cold=rho_cold
    )
    effectiveness_Re.append(hx_temp.effectiveness)

ax6.semilogx(Re_range, effectiveness_Re, 'b-', linewidth=2)
ax6.axvline(x=5000, color='red', linestyle='--', alpha=0.7, label='Estimated Operating Re')
ax6.axhline(y=0.9, color='green', linestyle=':', alpha=0.7, label='High Effectiveness Target')
ax6.set_xlabel('Reynolds Number [-]')
ax6.set_ylabel('Effectiveness [-]')
ax6.set_title('Effectiveness vs Reynolds Number\n(Approximate U ∝ Re^0.8 correlation)')
ax6.grid(True, alpha=0.3)
ax6.legend()
ax6.set_ylim(0, 1)

# Subplot 7: Economic optimization (Cost vs Area)
area_design_range = np.linspace(200, 1000, 50)
capital_cost = []
operating_cost = []
total_cost = []

# Cost correlations (simplified)
area_cost_factor = 2000  # $/m²
energy_cost_factor = 0.08  # $/kWh
operating_hours = 8000  # h/year

for A in area_design_range:
    # Capital cost (proportional to area)
    cap_cost = A * area_cost_factor
    
    # Operating cost (energy savings)
    hx_temp = HeatExchanger(
        U=U_base, A=A,
        m_hot=m_hot_base, m_cold=m_cold_base,
        cp_hot=cp_hot, cp_cold=cp_cold,
        V_hot=V_hot, V_cold=V_cold,
        rho_hot=rho_hot, rho_cold=rho_cold
    )
    
    u = np.array([T_hot_in, T_cold_in])
    T_out = hx_temp.steady_state(u)
    Q = hx_temp.calculate_heat_transfer_rate(T_hot_in, T_cold_in, T_out[0], T_out[1])
    
    # Annual energy savings (negative cost)
    annual_savings = Q * operating_hours * energy_cost_factor / 1000  # $/year
    
    # Present value of 10-year savings
    op_cost = -annual_savings * 8  # Simplified 10-year PV
    
    capital_cost.append(cap_cost / 1000)  # k$
    operating_cost.append(op_cost / 1000)  # k$
    total_cost.append((cap_cost + op_cost) / 1000)  # k$

ax7.plot(area_design_range, capital_cost, 'r-', linewidth=2, label='Capital Cost')
ax7.plot(area_design_range, operating_cost, 'g-', linewidth=2, label='Operating Cost (Savings)')
ax7.plot(area_design_range, total_cost, 'b-', linewidth=3, label='Total Cost')

# Find optimal area
optimal_idx = np.argmin(total_cost)
optimal_area = area_design_range[optimal_idx]
ax7.axvline(x=optimal_area, color='purple', linestyle='--', alpha=0.8, 
           label=f'Economic Optimum\n(A = {optimal_area:.0f} m²)')
ax7.axvline(x=A_base, color='orange', linestyle=':', alpha=0.8, 
           label=f'Design Point\n(A = {A_base:.0f} m²)')

ax7.set_xlabel('Heat Transfer Area [m²]')
ax7.set_ylabel('Cost [k$]')
ax7.set_title('Economic Optimization\n(10-year NPV Analysis)')
ax7.grid(True, alpha=0.3)
ax7.legend()

# Subplot 8: Fouling impact analysis
time_years = np.linspace(0, 5, 50)
fouling_resistance = 0.0001 * time_years  # m²·K/W - fouling builds up over time
Q_fouling = []
effectiveness_fouling = []

for Rf in fouling_resistance:
    U_fouled = 1 / (1/U_base + Rf)
    
    hx_fouled = HeatExchanger(
        U=U_fouled, A=A_base,
        m_hot=m_hot_base, m_cold=m_cold_base,
        cp_hot=cp_hot, cp_cold=cp_cold,
        V_hot=V_hot, V_cold=V_cold,
        rho_hot=rho_hot, rho_cold=rho_cold
    )
    
    u = np.array([T_hot_in, T_cold_in])
    T_out = hx_fouled.steady_state(u)
    Q = hx_fouled.calculate_heat_transfer_rate(T_hot_in, T_cold_in, T_out[0], T_out[1])
    
    Q_fouling.append(Q / 1e6)  # MW
    effectiveness_fouling.append(hx_fouled.effectiveness)

ax8.plot(time_years, Q_fouling, 'r-', linewidth=2, label='Heat Transfer Rate')
ax8.axhline(y=Q_fouling[0] * 0.9, color='orange', linestyle='--', alpha=0.7, 
           label='90% Performance Threshold')

ax8_twin = ax8.twinx()
ax8_twin.plot(time_years, effectiveness_fouling, 'b--', linewidth=2, alpha=0.7, label='Effectiveness')
ax8_twin.set_ylabel('Effectiveness [-]', color='blue')
ax8_twin.tick_params(axis='y', labelcolor='blue')

ax8.set_xlabel('Operating Time [years]')
ax8.set_ylabel('Heat Transfer Rate [MW]')
ax8.set_title('Fouling Impact Analysis\n(Performance Degradation)')
ax8.grid(True, alpha=0.3)
ax8.legend(loc='upper right')

plt.tight_layout()
plt.savefig('/Users/macmini/Desktop/github/sproclib/sproclib/unit/heat_exchanger/HeatExchanger_detailed_analysis.png', 
            bbox_inches='tight', dpi=300)
plt.close()

print("Heat exchanger visualization plots created successfully!")
print("Files generated:")
print("  - HeatExchanger_example_plots.png: Process behavior and performance curves")
print("  - HeatExchanger_detailed_analysis.png: Parameter sensitivity and design optimization")
