"""
Generate visualization plots for Pump class
Process behavior and parameter sensitivity analysis
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the sproclib directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sproclib'))

from sproclib.unit.pump.Pump import Pump

def create_pump_plots():
    """Create comprehensive plots for pump performance analysis."""
    
    # Create figure with subplots
    fig = plt.figure(figsize=(15, 10))
    
    # Plot 1: Power vs Flow Rate
    ax1 = plt.subplot(2, 3, 1)
    
    pump = Pump(eta=0.75, rho=1000.0, flow_nominal=0.1, delta_P_nominal=300000.0)
    flow_range = np.linspace(0, 0.2, 50)
    pressures = [100000.0, 200000.0, 300000.0]  # Different inlet pressures
    
    for P_in in pressures:
        powers = []
        for Q in flow_range:
            u = np.array([P_in, Q])
            _, power = pump.steady_state(u)
            powers.append(power/1000)  # Convert to kW
        
        ax1.plot(flow_range*3600, powers, label=f'P_in = {P_in/1e5:.1f} bar')
    
    ax1.set_xlabel('Flow Rate (m³/h)')
    ax1.set_ylabel('Power (kW)')
    ax1.set_title('Power vs Flow Rate\n(Constant Pressure Rise Model)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Efficiency Impact
    ax2 = plt.subplot(2, 3, 2)
    
    efficiencies = np.linspace(0.5, 0.9, 50)
    flow_rate = 0.1  # m³/s
    P_inlet = 200000.0  # Pa
    
    powers = []
    for eta in efficiencies:
        pump_eta = Pump(eta=eta, rho=1000.0, flow_nominal=0.1, delta_P_nominal=300000.0)
        u = np.array([P_inlet, flow_rate])
        _, power = pump_eta.steady_state(u)
        powers.append(power/1000)
    
    ax2.plot(efficiencies*100, powers, 'b-', linewidth=2)
    ax2.set_xlabel('Efficiency (%)')
    ax2.set_ylabel('Power (kW)')
    ax2.set_title('Power vs Pump Efficiency\n(Q = 360 m³/h)')
    ax2.grid(True, alpha=0.3)
    
    # Add efficiency zones
    ax2.axvspan(50, 70, alpha=0.2, color='red', label='Poor')
    ax2.axvspan(70, 80, alpha=0.2, color='yellow', label='Good')
    ax2.axvspan(80, 90, alpha=0.2, color='green', label='Excellent')
    ax2.legend()
    
    # Plot 3: Dynamic Response
    ax3 = plt.subplot(2, 3, 3)
    
    # Simulate step response
    time = np.linspace(0, 10, 100)
    P_initial = 550000.0  # Initial outlet pressure
    P_final = 600000.0    # Final outlet pressure after step
    tau = 1.0  # Time constant
    
    # Step at t=2s
    response = []
    for t in time:
        if t < 2.0:
            P_out = P_initial
        else:
            P_out = P_final - (P_final - P_initial) * np.exp(-(t-2)/tau)
        response.append(P_out/1e5)  # Convert to bar
    
    ax3.plot(time, response, 'b-', linewidth=2)
    ax3.axhline(y=P_initial/1e5, color='r', linestyle='--', alpha=0.7, label='Initial')
    ax3.axhline(y=P_final/1e5, color='g', linestyle='--', alpha=0.7, label='Final')
    ax3.axvline(x=2.0, color='orange', linestyle='--', alpha=0.7, label='Step Input')
    
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Outlet Pressure (bar)')
    ax3.set_title('Dynamic Response\n(First-Order System)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Operating Envelope
    ax4 = plt.subplot(2, 3, 4)
    
    flow_range = np.linspace(0, 0.15, 50)
    delta_P_range = np.linspace(100000, 500000, 50)
    Flow, DeltaP = np.meshgrid(flow_range, delta_P_range)
    
    # Calculate power surface
    eta = 0.75
    Power_surface = Flow * DeltaP / eta / 1000  # kW
    
    contour = ax4.contourf(Flow*3600, DeltaP/1e5, Power_surface, levels=20, cmap='viridis')
    plt.colorbar(contour, ax=ax4, label='Power (kW)')
    
    # Add operating lines
    ax4.contour(Flow*3600, DeltaP/1e5, Power_surface, levels=[10, 20, 40, 80], colors='white', linewidths=1)
    
    ax4.set_xlabel('Flow Rate (m³/h)')
    ax4.set_ylabel('Pressure Rise (bar)')
    ax4.set_title('Power Contours\n(Operating Envelope)')
    
    # Plot 5: Density Effect
    ax5 = plt.subplot(2, 3, 5)
    
    densities = [700, 850, 1000, 1150, 1300]  # kg/m³
    density_names = ['Light Oil', 'Hydrocarbon', 'Water', 'Brine', 'Heavy Solution']
    
    flow_rate = 0.08  # m³/s
    powers = []
    
    for rho in densities:
        pump_rho = Pump(eta=0.75, rho=rho, flow_nominal=0.1, delta_P_nominal=300000.0)
        u = np.array([200000.0, flow_rate])
        _, power = pump_rho.steady_state(u)
        powers.append(power/1000)
    
    bars = ax5.bar(density_names, powers, color=['orange', 'blue', 'cyan', 'green', 'red'], alpha=0.7)
    ax5.set_ylabel('Power (kW)')
    ax5.set_title('Power vs Fluid Density\n(Constant ΔP Model)')
    ax5.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, power in zip(bars, powers):
        ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{power:.1f}', ha='center', va='bottom')
    
    # Plot 6: Annual Operating Cost
    ax6 = plt.subplot(2, 3, 6)
    
    flow_rates = np.linspace(0.05, 0.15, 50)  # m³/s
    electricity_cost = 0.08  # $/kWh
    operating_hours = 8760  # hours/year
    
    annual_costs = []
    for Q in flow_rates:
        u = np.array([200000.0, Q])
        _, power = pump.steady_state(u)
        annual_cost = power/1000 * operating_hours * electricity_cost
        annual_costs.append(annual_cost)
    
    ax6.plot(flow_rates*3600, annual_costs, 'g-', linewidth=2, label='Operating Cost')
    ax6.fill_between(flow_rates*3600, annual_costs, alpha=0.3, color='green')
    
    ax6.set_xlabel('Flow Rate (m³/h)')
    ax6.set_ylabel('Annual Cost ($/year)')
    ax6.set_title('Annual Operating Cost\n($0.08/kWh, 8760 h/year)')
    ax6.grid(True, alpha=0.3)
    
    # Add cost zones
    mean_cost = np.mean(annual_costs)
    ax6.axhline(y=mean_cost, color='orange', linestyle='--', alpha=0.7, 
                label=f'Average: ${mean_cost:.0f}/year')
    ax6.legend()
    
    plt.tight_layout()
    plt.savefig('/Users/macmini/Desktop/github/sproclib/Pump_example_plots.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_detailed_analysis():
    """Create detailed analysis plots for pump characteristics."""
    
    fig = plt.figure(figsize=(12, 8))
    
    # Plot 1: Sensitivity Analysis
    ax1 = plt.subplot(2, 2, 1)
    
    # Base case
    base_pump = Pump(eta=0.75, rho=1000.0, flow_nominal=0.1, delta_P_nominal=300000.0)
    flow_range = np.linspace(0.05, 0.15, 50)
    
    # Efficiency variations
    efficiencies = [0.65, 0.75, 0.85]
    colors = ['red', 'blue', 'green']
    
    for eta, color in zip(efficiencies, colors):
        powers = []
        for Q in flow_range:
            pump_var = Pump(eta=eta, rho=1000.0, flow_nominal=0.1, delta_P_nominal=300000.0)
            u = np.array([200000.0, Q])
            _, power = pump_var.steady_state(u)
            powers.append(power/1000)
        
        ax1.plot(flow_range*3600, powers, color=color, linewidth=2, 
                label=f'η = {eta:.0%}')
    
    ax1.set_xlabel('Flow Rate (m³/h)')
    ax1.set_ylabel('Power (kW)')
    ax1.set_title('Efficiency Sensitivity Analysis')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Pressure Rise Variations
    ax2 = plt.subplot(2, 2, 2)
    
    delta_Ps = [200000, 300000, 400000]  # Pa
    
    for delta_P, color in zip(delta_Ps, colors):
        powers = []
        for Q in flow_range:
            pump_var = Pump(eta=0.75, rho=1000.0, flow_nominal=0.1, delta_P_nominal=delta_P)
            u = np.array([200000.0, Q])
            _, power = pump_var.steady_state(u)
            powers.append(power/1000)
        
        ax2.plot(flow_range*3600, powers, color=color, linewidth=2,
                label=f'ΔP = {delta_P/1e5:.1f} bar')
    
    ax2.set_xlabel('Flow Rate (m³/h)')
    ax2.set_ylabel('Power (kW)')
    ax2.set_title('Pressure Rise Sensitivity')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Economic Analysis
    ax3 = plt.subplot(2, 2, 3)
    
    electricity_prices = np.linspace(0.05, 0.15, 50)  # $/kWh
    flow_rate = 0.1  # m³/s
    operating_hours = 8760
    
    u = np.array([200000.0, flow_rate])
    _, power = base_pump.steady_state(u)
    
    annual_costs = electricity_prices * power/1000 * operating_hours
    
    ax3.plot(electricity_prices*100, annual_costs, 'purple', linewidth=2)
    ax3.fill_between(electricity_prices*100, annual_costs, alpha=0.3, color='purple')
    
    ax3.set_xlabel('Electricity Price (¢/kWh)')
    ax3.set_ylabel('Annual Operating Cost ($/year)')
    ax3.set_title('Operating Cost vs Electricity Price')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Performance Map
    ax4 = plt.subplot(2, 2, 4)
    
    # Create performance map
    flows = np.linspace(0.02, 0.18, 30)
    deltas = np.linspace(100000, 500000, 30)
    F, D = np.meshgrid(flows, deltas)
    
    # Calculate efficiency zones (constant efficiency assumed)
    eta_zones = np.ones_like(F) * 0.75
    
    # Power consumption
    P_consumption = F * D / 0.75 / 1000  # kW
    
    contour = ax4.contourf(F*3600, D/1e5, P_consumption, levels=15, cmap='RdYlBu_r')
    plt.colorbar(contour, ax=ax4, label='Power (kW)')
    
    # Add iso-power lines
    ax4.contour(F*3600, D/1e5, P_consumption, levels=[20, 40, 80, 120], 
               colors='black', linewidths=1, alpha=0.7)
    
    ax4.set_xlabel('Flow Rate (m³/h)')
    ax4.set_ylabel('Pressure Rise (bar)')
    ax4.set_title('Pump Performance Map')
    
    plt.tight_layout()
    plt.savefig('/Users/macmini/Desktop/github/sproclib/Pump_detailed_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    create_pump_plots()
    create_detailed_analysis()
    print("Pump visualization plots created successfully!")
