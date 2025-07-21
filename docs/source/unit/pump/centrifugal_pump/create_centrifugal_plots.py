"""
Generate visualization plots for CentrifugalPump class
Pump curves, performance maps, and system analysis
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the sproclib directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sproclib'))

from sproclib.unit.pump.CentrifugalPump import CentrifugalPump

def create_centrifugal_plots():
    """Create comprehensive plots for centrifugal pump analysis."""
    
    fig = plt.figure(figsize=(15, 10))
    
    # Plot 1: Pump Curves (Different H0 values)
    ax1 = plt.subplot(2, 3, 1)
    
    shutoff_heads = [40, 60, 80]  # m
    K = 25.0  # Fixed K value
    colors = ['blue', 'green', 'red']
    
    for H0, color in zip(shutoff_heads, colors):
        pump = CentrifugalPump(H0=H0, K=K, eta=0.80, rho=1000.0)
        Q_max = np.sqrt(H0/K)
        flow_range = np.linspace(0, Q_max*0.95, 50)
        
        heads = []
        for Q in flow_range:
            u = np.array([100000.0, Q])  # 1 bar inlet
            P_out, _ = pump.steady_state(u)
            head = (P_out - 100000.0) / (pump.rho * 9.81)
            heads.append(head)
        
        ax1.plot(flow_range*3600, heads, color=color, linewidth=2, 
                label=f'H₀ = {H0} m')
    
    ax1.set_xlabel('Flow Rate (m³/h)')
    ax1.set_ylabel('Head (m)')
    ax1.set_title('Pump Curves (H = H₀ - K·Q²)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, None)
    ax1.set_ylim(0, None)
    
    # Plot 2: Effect of K coefficient
    ax2 = plt.subplot(2, 3, 2)
    
    H0 = 60.0  # Fixed shutoff head
    K_values = [15, 25, 40]  # Different curve steepness
    
    for K, color in zip(K_values, colors):
        pump = CentrifugalPump(H0=H0, K=K, eta=0.80, rho=1000.0)
        Q_max = np.sqrt(H0/K)
        flow_range = np.linspace(0, min(Q_max*0.95, 2.0), 50)
        
        heads = []
        for Q in flow_range:
            u = np.array([100000.0, Q])
            P_out, _ = pump.steady_state(u)
            head = (P_out - 100000.0) / (pump.rho * 9.81)
            heads.append(head)
        
        ax2.plot(flow_range*3600, heads, color=color, linewidth=2,
                label=f'K = {K} s²/m⁵')
    
    ax2.set_xlabel('Flow Rate (m³/h)')
    ax2.set_ylabel('Head (m)')
    ax2.set_title('Effect of K Coefficient\n(Curve Steepness)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, None)
    ax2.set_ylim(0, None)
    
    # Plot 3: Power Curves
    ax3 = plt.subplot(2, 3, 3)
    
    pump = CentrifugalPump(H0=80.0, K=25.0, eta=0.80, rho=1000.0)
    Q_max = np.sqrt(pump.H0/pump.K)
    flow_range = np.linspace(0.1, Q_max*0.9, 50)  # Start from 0.1 to avoid zero
    
    powers = []
    efficiencies = []
    
    for Q in flow_range:
        u = np.array([150000.0, Q])  # 1.5 bar inlet
        P_out, power = pump.steady_state(u)
        
        powers.append(power/1000)  # Convert to kW
        
        # Calculate hydraulic efficiency
        hydraulic_power = Q * (P_out - 150000.0)
        efficiency = hydraulic_power / power if power > 0 else 0
        efficiencies.append(efficiency*100)
    
    ax3_eff = ax3.twinx()
    
    line1 = ax3.plot(flow_range*3600, powers, 'b-', linewidth=2, label='Power')
    line2 = ax3_eff.plot(flow_range*3600, efficiencies, 'r--', linewidth=2, label='Efficiency')
    
    ax3.set_xlabel('Flow Rate (m³/h)')
    ax3.set_ylabel('Power (kW)', color='blue')
    ax3_eff.set_ylabel('Efficiency (%)', color='red')
    ax3.set_title('Power and Efficiency Curves')
    
    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax3.legend(lines, labels, loc='upper left')
    
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: System Curve Intersection
    ax4 = plt.subplot(2, 3, 4)
    
    pump = CentrifugalPump(H0=70.0, K=20.0, eta=0.82, rho=1000.0)
    Q_range = np.linspace(0, 2.0, 100)
    
    # Pump curve
    pump_heads = []
    for Q in Q_range:
        H = max(0, pump.H0 - pump.K * Q**2)
        pump_heads.append(H)
    
    # System curves (different static heads)
    static_heads = [20, 30, 40]  # m
    K_system = 10.0  # System resistance
    
    for H_static in static_heads:
        system_heads = H_static + K_system * Q_range**2
        ax4.plot(Q_range*3600, system_heads, '--', linewidth=2,
                label=f'System (H_s = {H_static} m)')
        
        # Find intersection
        for i, Q in enumerate(Q_range):
            if abs(pump_heads[i] - system_heads[i]) < 0.5:
                ax4.plot(Q*3600, pump_heads[i], 'ro', markersize=8)
                break
    
    ax4.plot(Q_range*3600, pump_heads, 'b-', linewidth=3, label='Pump Curve')
    
    ax4.set_xlabel('Flow Rate (m³/h)')
    ax4.set_ylabel('Head (m)')
    ax4.set_title('Pump-System Intersection')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(0, 7000)
    ax4.set_ylim(0, 80)
    
    # Plot 5: Affinity Laws
    ax5 = plt.subplot(2, 3, 5)
    
    # Base pump at 100% speed
    pump_base = CentrifugalPump(H0=60.0, K=25.0, eta=0.80, rho=1000.0)
    
    speed_ratios = [0.8, 1.0, 1.2]
    
    for speed, color in zip(speed_ratios, colors):
        # Apply affinity laws: H ∝ N², Q ∝ N
        H0_adj = pump_base.H0 * speed**2
        K_adj = pump_base.K / speed**2
        
        pump_adj = CentrifugalPump(H0=H0_adj, K=K_adj, eta=pump_base.eta, rho=pump_base.rho)
        Q_max = np.sqrt(H0_adj/K_adj)
        Q_range = np.linspace(0, Q_max*0.9, 30)
        
        heads = []
        for Q in Q_range:
            u = np.array([100000.0, Q])
            P_out, _ = pump_adj.steady_state(u)
            head = (P_out - 100000.0) / (pump_adj.rho * 9.81)
            heads.append(head)
        
        ax5.plot(Q_range*3600, heads, color=color, linewidth=2,
                label=f'{speed*100:.0f}% Speed')
    
    ax5.set_xlabel('Flow Rate (m³/h)')
    ax5.set_ylabel('Head (m)')
    ax5.set_title('Affinity Laws\n(Speed Variation)')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # Plot 6: NPSH Requirements
    ax6 = plt.subplot(2, 3, 6)
    
    # NPSH estimation using Thoma's correlation
    pump = CentrifugalPump(H0=60.0, K=25.0, eta=0.80, rho=1000.0)
    Q_bep = 0.8  # m³/s (estimated BEP)
    H_bep = pump.H0 - pump.K * Q_bep**2
    
    Q_range = np.linspace(0.2, 1.5, 50)
    npsh_req = []
    
    for Q in Q_range:
        # Simplified NPSH correlation: NPSH ∝ (Q/Q_bep)^1.5 * H_bep
        sigma = 0.15  # Thoma number (typical for centrifugal pumps)
        npsh = sigma * H_bep * (Q/Q_bep)**1.5
        npsh_req.append(npsh)
    
    ax6.plot(Q_range*3600, npsh_req, 'purple', linewidth=2, label='NPSH Required')
    
    # NPSH available (example system)
    P_atm = 101325  # Pa
    P_vapor = 2340  # Pa (water at 20°C)
    rho = 1000  # kg/m³
    g = 9.81
    
    # Static suction head and friction losses
    suction_heads = [2, 4, 6]  # m (different suction conditions)
    
    for h_s in suction_heads:
        npsh_avail = (P_atm - P_vapor)/(rho*g) - h_s - 0.5*Q_range**2  # Simplified friction
        ax6.plot(Q_range*3600, npsh_avail, '--', linewidth=2,
                label=f'NPSH Avail (h_s={h_s}m)')
    
    ax6.set_xlabel('Flow Rate (m³/h)')
    ax6.set_ylabel('NPSH (m)')
    ax6.set_title('NPSH Analysis\n(Cavitation Prevention)')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    ax6.set_ylim(0, 15)
    
    plt.tight_layout()
    plt.savefig('/Users/macmini/Desktop/github/sproclib/CentrifugalPump_example_plots.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_detailed_analysis():
    """Create detailed analysis plots for centrifugal pump characteristics."""
    
    fig = plt.figure(figsize=(12, 8))
    
    # Plot 1: Performance Map
    ax1 = plt.subplot(2, 2, 1)
    
    pump = CentrifugalPump(H0=80.0, K=25.0, eta=0.80, rho=1000.0)
    
    # Create meshgrid for performance map
    Q_range = np.linspace(0.1, 1.5, 30)
    H0_range = np.linspace(40, 100, 30)
    Q_mesh, H0_mesh = np.meshgrid(Q_range, H0_range)
    
    # Calculate efficiency map (simplified)
    K = 25.0
    efficiency_map = np.zeros_like(Q_mesh)
    
    for i in range(len(H0_range)):
        for j in range(len(Q_range)):
            Q = Q_mesh[i, j]
            H0 = H0_mesh[i, j]
            Q_bep = np.sqrt(H0/K) * 0.75  # BEP at 75% of max flow
            
            # Efficiency curve (parabolic around BEP)
            eta_max = 0.85
            eta = eta_max * (1 - 2*((Q - Q_bep)/Q_bep)**2) if abs(Q - Q_bep) < Q_bep else 0.3
            efficiency_map[i, j] = max(0.3, eta)
    
    contour = ax1.contourf(Q_mesh*3600, H0_mesh, efficiency_map*100, 
                          levels=np.linspace(30, 85, 12), cmap='viridis')
    plt.colorbar(contour, ax=ax1, label='Efficiency (%)')
    
    # Add iso-efficiency lines
    ax1.contour(Q_mesh*3600, H0_mesh, efficiency_map*100, 
               levels=[50, 60, 70, 80], colors='white', linewidths=1)
    
    ax1.set_xlabel('Flow Rate (m³/h)')
    ax1.set_ylabel('Shutoff Head (m)')
    ax1.set_title('Pump Efficiency Map')
    
    # Plot 2: Specific Speed Analysis
    ax2 = plt.subplot(2, 2, 2)
    
    # Different pump designs
    pumps_data = [
        {'H0': 100, 'K': 50, 'type': 'High Head'},
        {'H0': 60, 'K': 25, 'type': 'Medium Head'},
        {'H0': 30, 'K': 10, 'type': 'Low Head'}
    ]
    
    N = 1450  # rpm
    
    colors = ['blue', 'green', 'red']
    
    for i, pump_data in enumerate(pumps_data):
        pump = CentrifugalPump(H0=pump_data['H0'], K=pump_data['K'], eta=0.80, rho=1000.0)
        Q_bep = np.sqrt(pump.H0/pump.K) * 0.75
        H_bep = pump.H0 - pump.K * Q_bep**2
        
        # Specific speed (US units for comparison)
        Q_gpm = Q_bep * 15850
        H_ft = H_bep * 3.281
        Ns = N * np.sqrt(Q_gpm) / (H_ft**0.75)
        
        ax2.bar(pump_data['type'], Ns, color=colors[i], alpha=0.7)
        ax2.text(i, Ns + 50, f'{Ns:.0f}', ha='center', va='bottom')
    
    ax2.set_ylabel('Specific Speed (US units)')
    ax2.set_title('Specific Speed Comparison')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add classification lines
    ax2.axhline(y=1000, color='red', linestyle='--', alpha=0.7, label='Radial/Mixed')
    ax2.axhline(y=4000, color='orange', linestyle='--', alpha=0.7, label='Mixed/Axial')
    ax2.legend()
    
    # Plot 3: Operating Range Analysis
    ax3 = plt.subplot(2, 2, 3)
    
    pump = CentrifugalPump(H0=70.0, K=25.0, eta=0.82, rho=1000.0)
    Q_bep = np.sqrt(pump.H0/pump.K) * 0.75
    Q_range = np.linspace(0.1, 1.5, 50)
    
    # Calculate various parameters
    heads = []
    powers = []
    efficiencies = []
    
    for Q in Q_range:
        u = np.array([150000.0, Q])
        P_out, power = pump.steady_state(u)
        head = (P_out - 150000.0) / (pump.rho * 9.81)
        
        heads.append(head)
        powers.append(power/1000)
        
        hydraulic_power = Q * (P_out - 150000.0)
        efficiency = hydraulic_power / power if power > 0 else 0
        efficiencies.append(efficiency*100)
    
    # Define operating zones
    Q_min = 0.5 * Q_bep  # Minimum continuous flow
    Q_rated = Q_bep      # Rated flow
    Q_max = 1.2 * Q_bep  # Maximum recommended flow
    
    ax3.fill_between([Q_min*3600, Q_max*3600], 0, 100, alpha=0.2, color='green', 
                     label='Recommended Range')
    ax3.fill_between([0, Q_min*3600], 0, 100, alpha=0.2, color='red', 
                     label='Avoid (Low Flow)')
    ax3.fill_between([Q_max*3600, 5400], 0, 100, alpha=0.2, color='orange', 
                     label='Caution (High Flow)')
    
    ax3.plot(Q_range*3600, efficiencies, 'b-', linewidth=2, label='Efficiency')
    ax3.axvline(x=Q_rated*3600, color='black', linestyle='--', alpha=0.7, label='BEP')
    
    ax3.set_xlabel('Flow Rate (m³/h)')
    ax3.set_ylabel('Efficiency (%)')
    ax3.set_title('Operating Range Guidelines')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, 5400)
    ax3.set_ylim(0, 100)
    
    # Plot 4: Energy Cost Analysis
    ax4 = plt.subplot(2, 2, 4)
    
    # Annual cost vs flow rate
    operating_hours = 6000  # hours/year
    electricity_cost = 0.09  # $/kWh
    motor_efficiency = 0.94
    
    annual_costs = []
    for Q in Q_range:
        u = np.array([150000.0, Q])
        _, power = pump.steady_state(u)
        brake_power = power / motor_efficiency
        annual_cost = brake_power/1000 * operating_hours * electricity_cost
        annual_costs.append(annual_cost)
    
    ax4.plot(Q_range*3600, annual_costs, 'g-', linewidth=2, label='Annual Cost')
    
    # Find minimum cost point
    min_cost_idx = np.argmin(annual_costs)
    ax4.plot(Q_range[min_cost_idx]*3600, annual_costs[min_cost_idx], 'ro', 
             markersize=8, label='Minimum Cost')
    
    # Add BEP line
    ax4.axvline(x=Q_bep*3600, color='blue', linestyle='--', alpha=0.7, label='BEP')
    
    ax4.set_xlabel('Flow Rate (m³/h)')
    ax4.set_ylabel('Annual Cost ($/year)')
    ax4.set_title('Annual Energy Cost\n(6000 h/year, $0.09/kWh)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/Users/macmini/Desktop/github/sproclib/CentrifugalPump_detailed_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    create_centrifugal_plots()
    create_detailed_analysis()
    print("CentrifugalPump visualization plots created successfully!")
