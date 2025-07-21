"""
Generate visualization plots for PositiveDisplacementPump class
Constant flow characteristics, pressure capability, and application analysis
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the sproclib directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sproclib'))

from sproclib.unit.pump.PositiveDisplacementPump import PositiveDisplacementPump

def create_pd_pump_plots():
    """Create comprehensive plots for positive displacement pump analysis."""
    
    fig = plt.figure(figsize=(15, 10))
    
    # Plot 1: Flow vs Pressure (Constant Flow Characteristic)
    ax1 = plt.subplot(2, 3, 1)
    
    flow_rates = [0.005, 0.01, 0.02]  # m³/s
    pressure_range = np.linspace(1, 50, 20) * 1e5  # 1 to 50 bar
    colors = ['blue', 'green', 'red']
    
    for flow_rate, color in zip(flow_rates, colors):
        flow_outputs = []
        for P_system in pressure_range:
            pump = PositiveDisplacementPump(flow_rate=flow_rate, eta=0.85, rho=1000.0)
            pump.delta_P_nominal = P_system - 1e5 + 2e5  # System pressure + margin
            
            # Flow rate is constant for PD pumps
            flow_outputs.append(flow_rate * 3600)  # Convert to m³/h
        
        ax1.plot(pressure_range/1e5, flow_outputs, color=color, linewidth=2,
                label=f'{flow_rate*3600:.1f} m³/h')
    
    ax1.set_xlabel('System Pressure (bar)')
    ax1.set_ylabel('Flow Rate (m³/h)')
    ax1.set_title('PD Pump: Constant Flow vs Pressure')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Add comparison with centrifugal pump (decreasing flow)
    from sproclib.unit.pump.CentrifugalPump import CentrifugalPump
    centrifugal = CentrifugalPump(H0=400.0, K=100.0, eta=0.75, rho=1000.0)
    
    centrifugal_flows = []
    for P_system in pressure_range:
        # For centrifugal, higher pressure = lower flow
        head_required = (P_system - 1e5) / (1000 * 9.81)
        Q = np.sqrt(max(0, (centrifugal.H0 - head_required) / centrifugal.K))
        centrifugal_flows.append(Q * 3600)
    
    ax1.plot(pressure_range/1e5, centrifugal_flows, 'k--', linewidth=2, alpha=0.7,
            label='Centrifugal (comparison)')
    ax1.legend()
    
    # Plot 2: Power vs Pressure
    ax2 = plt.subplot(2, 3, 2)
    
    pump = PositiveDisplacementPump(flow_rate=0.01, eta=0.85, rho=1000.0)
    
    powers = []
    for P_system in pressure_range:
        pump.delta_P_nominal = P_system - 1e5 + 2e5
        u = np.array([1e5])  # 1 bar inlet
        _, power = pump.steady_state(u)
        powers.append(power/1000)  # Convert to kW
    
    ax2.plot(pressure_range/1e5, powers, 'purple', linewidth=2)
    ax2.fill_between(pressure_range/1e5, powers, alpha=0.3, color='purple')
    
    ax2.set_xlabel('System Pressure (bar)')
    ax2.set_ylabel('Power (kW)')
    ax2.set_title('Power vs System Pressure\n(36 m³/h constant flow)')
    ax2.grid(True, alpha=0.3)
    
    # Add power zones
    mean_power = np.mean(powers)
    ax2.axhline(y=mean_power, color='orange', linestyle='--', alpha=0.7,
                label=f'Average: {mean_power:.1f} kW')
    ax2.legend()
    
    # Plot 3: Efficiency vs Viscosity
    ax3 = plt.subplot(2, 3, 3)
    
    viscosities = np.logspace(0, 3, 50)  # 1 to 1000 cP
    volumetric_efficiencies = []
    overall_efficiencies = []
    
    for visc in viscosities:
        # Volumetric efficiency vs viscosity (typical PD pump correlation)
        eta_vol = 0.95 - 0.0001 * visc if visc < 500 else max(0.75, 0.95 - 0.0001 * visc)
        volumetric_efficiencies.append(eta_vol * 100)
        
        # Overall efficiency (volumetric × mechanical)
        eta_mech = 0.90 - 0.00005 * visc if visc < 1000 else 0.85  # Mechanical efficiency
        overall_efficiencies.append(eta_vol * eta_mech * 100)
    
    ax3.semilogx(viscosities, volumetric_efficiencies, 'b-', linewidth=2, 
                 label='Volumetric Efficiency')
    ax3.semilogx(viscosities, overall_efficiencies, 'r-', linewidth=2,
                 label='Overall Efficiency')
    
    ax3.set_xlabel('Viscosity (cP)')
    ax3.set_ylabel('Efficiency (%)')
    ax3.set_title('Efficiency vs Fluid Viscosity')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Add viscosity zones
    ax3.axvspan(1, 10, alpha=0.2, color='green', label='Water-like')
    ax3.axvspan(10, 100, alpha=0.2, color='yellow', label='Oil-like')
    ax3.axvspan(100, 1000, alpha=0.2, color='orange', label='Viscous')
    
    # Plot 4: Metering Accuracy
    ax4 = plt.subplot(2, 3, 4)
    
    # Simulate flow rate accuracy over time
    time_hours = np.linspace(0, 24, 100)  # 24 hour period
    base_flow = 10.0  # m³/h
    
    # PD pump: very stable flow
    pd_flow = base_flow + 0.02 * np.sin(2*np.pi*time_hours/12) + 0.01 * np.random.randn(len(time_hours))
    
    # Centrifugal pump: more variation with system changes
    system_variations = 0.5 * np.sin(2*np.pi*time_hours/6)  # System pressure changes
    centrifugal_flow = base_flow * (1 - 0.1 * system_variations) + 0.1 * np.random.randn(len(time_hours))
    
    ax4.plot(time_hours, pd_flow, 'b-', linewidth=1, label='PD Pump', alpha=0.8)
    ax4.plot(time_hours, centrifugal_flow, 'r-', linewidth=1, label='Centrifugal', alpha=0.8)
    
    # Add target flow line
    ax4.axhline(y=base_flow, color='green', linestyle='--', linewidth=2, 
                label='Target Flow')
    
    ax4.set_xlabel('Time (hours)')
    ax4.set_ylabel('Flow Rate (m³/h)')
    ax4.set_title('Flow Rate Stability\n(24-hour operation)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(9.0, 11.0)
    
    # Plot 5: Chemical Injection Analysis
    ax5 = plt.subplot(2, 3, 5)
    
    # Chemical dosing scenarios
    process_flows = np.linspace(100, 1000, 50)  # m³/h main process
    target_concentrations = [10, 25, 50]  # ppm
    chemical_strength = 50000  # ppm (5% solution)
    
    for conc, color in zip(target_concentrations, colors):
        injection_rates = (process_flows * conc) / chemical_strength
        ax5.plot(process_flows, injection_rates, color=color, linewidth=2,
                label=f'{conc} ppm dosage')
    
    # Add pump capacity lines
    pump_capacities = [5, 10, 20]  # m³/h
    for capacity in pump_capacities:
        ax5.axhline(y=capacity, color='gray', linestyle='--', alpha=0.5)
        ax5.text(950, capacity+0.2, f'{capacity} m³/h', fontsize=8)
    
    ax5.set_xlabel('Process Flow Rate (m³/h)')
    ax5.set_ylabel('Required Injection Rate (m³/h)')
    ax5.set_title('Chemical Injection Requirements\n(5% active solution)')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # Plot 6: Economic Comparison
    ax6 = plt.subplot(2, 3, 6)
    
    # Compare PD vs Centrifugal costs
    flow_rates = np.linspace(1, 50, 20)  # m³/h
    
    # Capital costs (simplified)
    pd_capital = 5000 + 200 * flow_rates  # Higher base cost, linear scaling
    centrifugal_capital = 2000 + 50 * flow_rates  # Lower base cost
    
    # Operating costs (per year)
    electricity_cost = 0.08  # $/kWh
    operating_hours = 8760
    
    pd_operating = []
    centrifugal_operating = []
    
    for Q in flow_rates:
        # PD pump power (high pressure assumption)
        Q_ms = Q / 3600
        delta_P = 20e5  # 20 bar
        power_pd = Q_ms * delta_P / 0.85 / 1000  # kW
        pd_op_cost = power_pd * operating_hours * electricity_cost
        pd_operating.append(pd_op_cost)
        
        # Centrifugal pump power (lower pressure)
        delta_P_cent = 5e5  # 5 bar
        power_cent = Q_ms * delta_P_cent / 0.75 / 1000  # kW
        cent_op_cost = power_cent * operating_hours * electricity_cost
        centrifugal_operating.append(cent_op_cost)
    
    ax6.plot(flow_rates, pd_capital, 'b-', linewidth=2, label='PD Capital')
    ax6.plot(flow_rates, centrifugal_capital, 'r-', linewidth=2, label='Centrifugal Capital')
    ax6.plot(flow_rates, pd_operating, 'b--', linewidth=2, label='PD Operating (annual)')
    ax6.plot(flow_rates, centrifugal_operating, 'r--', linewidth=2, label='Centrifugal Operating (annual)')
    
    ax6.set_xlabel('Flow Rate (m³/h)')
    ax6.set_ylabel('Cost ($)')
    ax6.set_title('Economic Comparison\n(Capital vs Operating)')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/Users/macmini/Desktop/github/sproclib/PositiveDisplacementPump_example_plots.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_detailed_analysis():
    """Create detailed analysis plots for PD pump characteristics."""
    
    fig = plt.figure(figsize=(12, 8))
    
    # Plot 1: Pressure Capability Analysis
    ax1 = plt.subplot(2, 2, 1)
    
    pump_types = ['Gear', 'Piston', 'Diaphragm', 'Screw']
    max_pressures = [200, 700, 100, 400]  # bar
    flow_ranges = [50, 20, 30, 100]  # m³/h max
    colors_types = ['blue', 'red', 'green', 'orange']
    
    scatter = ax1.scatter(flow_ranges, max_pressures, c=colors_types, s=200, alpha=0.7)
    
    for i, pump_type in enumerate(pump_types):
        ax1.annotate(pump_type, (flow_ranges[i], max_pressures[i]), 
                    xytext=(5, 5), textcoords='offset points', fontsize=10)
    
    ax1.set_xlabel('Typical Max Flow (m³/h)')
    ax1.set_ylabel('Max Pressure (bar)')
    ax1.set_title('PD Pump Types - Pressure/Flow Envelope')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 120)
    ax1.set_ylim(0, 800)
    
    # Plot 2: Dynamic Response Comparison
    ax2 = plt.subplot(2, 2, 2)
    
    time = np.linspace(0, 5, 100)
    
    # Step response for different pump types
    # PD pump: faster response, lower time constant
    tau_pd = 0.5
    response_pd = 1 - np.exp(-time/tau_pd)
    
    # Centrifugal pump: slower response
    tau_cent = 1.5
    response_cent = 1 - np.exp(-time/tau_cent)
    
    ax2.plot(time, response_pd * 100, 'b-', linewidth=2, label='PD Pump (τ=0.5s)')
    ax2.plot(time, response_cent * 100, 'r-', linewidth=2, label='Centrifugal (τ=1.5s)')
    
    # Add response time markers
    ax2.axhline(y=63.2, color='gray', linestyle='--', alpha=0.5, label='63% Response')
    ax2.axhline(y=95, color='gray', linestyle=':', alpha=0.5, label='95% Response')
    
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Response (%)')
    ax2.set_title('Dynamic Response Comparison\n(Step Input)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 5)
    ax2.set_ylim(0, 100)
    
    # Plot 3: Application Map
    ax3 = plt.subplot(2, 2, 3)
    
    # Create application map based on pressure and flow
    pressures = np.linspace(1, 100, 100)
    flows = np.linspace(0.1, 100, 100)
    P_mesh, Q_mesh = np.meshgrid(pressures, flows)
    
    # Define application zones
    application_map = np.zeros_like(P_mesh)
    
    for i in range(len(flows)):
        for j in range(len(pressures)):
            P = P_mesh[i, j]
            Q = Q_mesh[i, j]
            
            if P > 50 and Q < 20:
                application_map[i, j] = 4  # High pressure injection
            elif P > 20 and Q < 50:
                application_map[i, j] = 3  # Chemical metering
            elif P < 10 and Q > 50:
                application_map[i, j] = 1  # Low pressure transfer
            else:
                application_map[i, j] = 2  # General purpose
    
    contour = ax3.contourf(P_mesh, Q_mesh, application_map, 
                          levels=[0.5, 1.5, 2.5, 3.5, 4.5],
                          colors=['lightblue', 'lightgreen', 'yellow', 'orange'],
                          alpha=0.7)
    
    # Add application labels
    ax3.text(5, 75, 'Low Pressure\nTransfer', ha='center', va='center', fontsize=10, weight='bold')
    ax3.text(30, 75, 'General\nPurpose', ha='center', va='center', fontsize=10, weight='bold')
    ax3.text(35, 25, 'Chemical\nMetering', ha='center', va='center', fontsize=10, weight='bold')
    ax3.text(75, 10, 'High Pressure\nInjection', ha='center', va='center', fontsize=10, weight='bold')
    
    ax3.set_xlabel('Pressure (bar)')
    ax3.set_ylabel('Flow Rate (m³/h)')
    ax3.set_title('PD Pump Application Map')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Turndown Capability
    ax4 = plt.subplot(2, 2, 4)
    
    # Turndown ratio analysis
    pump_speeds = np.linspace(10, 100, 50)  # % of rated speed
    
    # PD pump: linear turndown
    pd_flows = pump_speeds  # Linear relationship
    pd_efficiency = np.maximum(50, 85 - 0.2 * (100 - pump_speeds))  # Efficiency drops at low speed
    
    # Centrifugal with VFD: cubic relationship
    cent_flows = pump_speeds
    cent_efficiency = 75 * (pump_speeds/100)**0.2  # Efficiency changes with speed
    
    ax4_eff = ax4.twinx()
    
    line1 = ax4.plot(pump_speeds, pd_flows, 'b-', linewidth=2, label='PD Flow')
    line2 = ax4.plot(pump_speeds, cent_flows, 'r-', linewidth=2, label='Centrifugal Flow')
    line3 = ax4_eff.plot(pump_speeds, pd_efficiency, 'b--', linewidth=2, label='PD Efficiency')
    line4 = ax4_eff.plot(pump_speeds, cent_efficiency, 'r--', linewidth=2, label='Cent Efficiency')
    
    ax4.set_xlabel('Speed (% of rated)')
    ax4.set_ylabel('Flow (% of rated)', color='black')
    ax4_eff.set_ylabel('Efficiency (%)', color='gray')
    ax4.set_title('Turndown Capability\n(Speed Control)')
    
    # Combine legends
    lines = line1 + line2 + line3 + line4
    labels = [l.get_label() for l in lines]
    ax4.legend(lines, labels, loc='center right')
    
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(10, 100)
    
    plt.tight_layout()
    plt.savefig('/Users/macmini/Desktop/github/sproclib/PositiveDisplacementPump_detailed_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    create_pd_pump_plots()
    create_detailed_analysis()
    print("PositiveDisplacementPump visualization plots created successfully!")
