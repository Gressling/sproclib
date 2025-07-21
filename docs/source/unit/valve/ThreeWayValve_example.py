"""
Industrial Example: Three-Way Valve in Chemical Process
Mixing valve for reactor temperature control - Hot/Cold feed blending
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the sproclib path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from sproclib.unit.valve.ThreeWayValve import ThreeWayValve


def main():
    print("=" * 65)
    print("THREE-WAY VALVE - INDUSTRIAL EXAMPLE")
    print("Reactor Feed Temperature Control - Hot/Cold Stream Mixing")
    print("=" * 65)
    
    # Industrial mixing valve for reactor feed temperature control
    mixing_valve = ThreeWayValve(
        Cv_max=180.0,           # gpm/psi^0.5 (per path)
        valve_config="mixing",   # Two inlets, one outlet
        dead_time=1.5,          # s (pneumatic actuator)
        time_constant=3.0,      # s
        name="ReactorFeedMixer"
    )
    
    # Industrial diverting valve for product distribution
    diverting_valve = ThreeWayValve(
        Cv_max=120.0,
        valve_config="diverting",  # One inlet, two outlets
        dead_time=1.0,
        time_constant=2.5,
        name="ProductDiverter"
    )
    
    print("\nMIXING VALVE SPECIFICATIONS:")
    print("-" * 35)
    print(f"Configuration: {mixing_valve.valve_config}")
    print(f"Max Cv per path: {mixing_valve.Cv_max:.1f} gpm/psi^0.5")
    print(f"Dead Time: {mixing_valve.dead_time:.1f} s")
    print(f"Time Constant: {mixing_valve.time_constant:.1f} s")
    print(f"State Variables: {mixing_valve.state_names}")
    
    # Process conditions for mixing application
    print("\nMIXING APPLICATION - PROCESS CONDITIONS:")
    print("-" * 45)
    T_hot = 120.0      # °C (hot feed stream)
    T_cold = 25.0      # °C (cold feed stream)
    T_target = 85.0    # °C (target reactor feed temperature)
    
    P_hot = 4.5e5      # Pa (4.5 bar hot stream pressure)
    P_cold = 4.2e5     # Pa (4.2 bar cold stream pressure)
    P_mixed = 1.8e5    # Pa (1.8 bar to reactor)
    rho = 890.0        # kg/m³ (organic solvent at average temp)
    
    print(f"Hot Stream: {T_hot:.1f} °C at {P_hot/1e5:.1f} bar")
    print(f"Cold Stream: {T_cold:.1f} °C at {P_cold/1e5:.1f} bar")
    print(f"Target Mixed: {T_target:.1f} °C at {P_mixed/1e5:.1f} bar")
    print(f"Fluid Density: {rho:.1f} kg/m³")
    
    # Calculate required mixing ratio for target temperature
    mixing_ratio = (T_target - T_cold) / (T_hot - T_cold)
    required_position = 1.0 - mixing_ratio  # Position for cold stream fraction
    
    print(f"\nTEMPERATURE MIXING CALCULATION:")
    print("-" * 35)
    print(f"Required Hot Fraction: {mixing_ratio:.3f}")
    print(f"Required Cold Fraction: {1-mixing_ratio:.3f}")
    print(f"Valve Position: {required_position:.3f}")
    
    # Analyze mixing valve performance
    print("\nMIXING VALVE PERFORMANCE ANALYSIS:")
    print("-" * 40)
    
    positions = np.linspace(0, 1, 11)
    temperatures = []
    total_flows = []
    hot_flows = []
    cold_flows = []
    
    print("Position | Hot% | Cold% | Hot Flow | Cold Flow | Total | Mixed T")
    print("         |      |       | (m³/h)   | (m³/h)    | (m³/h)| (°C)")
    print("-" * 70)
    
    for pos in positions:
        # Calculate flows
        u = np.array([pos, P_hot, P_cold, P_mixed, rho])
        steady_state = mixing_valve.steady_state(u)
        _, total_flow = steady_state
        
        # Calculate individual stream flows
        Cv_A, Cv_B = mixing_valve._calculate_cv_split(pos)
        Cv_si = 6.309e-5
        
        flow_hot = Cv_A * Cv_si * np.sqrt((P_hot - P_mixed) / rho)
        flow_cold = Cv_B * Cv_si * np.sqrt((P_cold - P_mixed) / rho)
        
        # Mass-weighted temperature mixing
        mass_hot = flow_hot * rho
        mass_cold = flow_cold * rho
        total_mass = mass_hot + mass_cold
        
        if total_mass > 0:
            T_mixed = (mass_hot * T_hot + mass_cold * T_cold) / total_mass
        else:
            T_mixed = T_cold
        
        # Convert flows to m³/h
        flow_hot_m3h = flow_hot * 3600
        flow_cold_m3h = flow_cold * 3600
        total_flow_m3h = total_flow * 3600
        
        # Flow percentages
        hot_percent = (flow_hot / total_flow * 100) if total_flow > 0 else 0
        cold_percent = (flow_cold / total_flow * 100) if total_flow > 0 else 0
        
        temperatures.append(T_mixed)
        total_flows.append(total_flow_m3h)
        hot_flows.append(flow_hot_m3h)
        cold_flows.append(flow_cold_m3h)
        
        print(f"{pos:8.1f} | {hot_percent:4.0f} | {cold_percent:5.0f} | "
              f"{flow_hot_m3h:8.1f} | {flow_cold_m3h:9.1f} | "
              f"{total_flow_m3h:5.1f} | {T_mixed:7.1f}")
    
    # Diverting valve analysis
    print("\n" + "=" * 65)
    print("DIVERTING VALVE APPLICATION - PRODUCT DISTRIBUTION")
    print("=" * 65)
    
    print(f"\nDIVERTING VALVE SPECIFICATIONS:")
    print("-" * 35)
    print(f"Configuration: {diverting_valve.valve_config}")
    print(f"Max Cv per path: {diverting_valve.Cv_max:.1f} gpm/psi^0.5")
    
    # Process conditions for diverting application
    P_feed = 5.0e5        # Pa (5 bar feed pressure)
    P_product1 = 2.0e5    # Pa (2 bar to Product Tank 1)
    P_product2 = 1.5e5    # Pa (1.5 bar to Product Tank 2)
    rho_product = 950.0   # kg/m³ (product density)
    
    print(f"\nDIVERTING PROCESS CONDITIONS:")
    print("-" * 35)
    print(f"Feed Pressure: {P_feed/1e5:.1f} bar")
    print(f"Product 1 Pressure: {P_product1/1e5:.1f} bar")
    print(f"Product 2 Pressure: {P_product2/1e5:.1f} bar")
    print(f"Product Density: {rho_product:.1f} kg/m³")
    
    print("\nDIVERTING VALVE PERFORMANCE:")
    print("-" * 35)
    print("Position | Product1 | Product2 | Total  | Split Ratio")
    print("         | (m³/h)   | (m³/h)   | (m³/h) | (P1:P2)")
    print("-" * 55)
    
    product1_flows = []
    product2_flows = []
    
    for pos in positions:
        u = np.array([pos, P_feed, P_product1, P_product2, rho_product])
        steady_state = diverting_valve.steady_state(u)
        _, flow1, flow2 = steady_state
        
        flow1_m3h = flow1 * 3600
        flow2_m3h = flow2 * 3600
        total_m3h = flow1_m3h + flow2_m3h
        
        product1_flows.append(flow1_m3h)
        product2_flows.append(flow2_m3h)
        
        if flow2_m3h > 0:
            split_ratio = flow1_m3h / flow2_m3h
        else:
            split_ratio = float('inf')
        
        print(f"{pos:8.1f} | {flow1_m3h:8.1f} | {flow2_m3h:8.1f} | "
              f"{total_m3h:6.1f} | {split_ratio:8.2f}")
    
    # Engineering validation
    print("\nENGINEERING VALIDATION:")
    print("-" * 25)
    
    # Test specific operating point for mixing valve
    test_pos = required_position
    u_test = np.array([test_pos, P_hot, P_cold, P_mixed, rho])
    steady_test = mixing_valve.steady_state(u_test)
    _, flow_test = steady_test
    
    print(f"Target temperature: {T_target:.1f} °C")
    print(f"Required position: {test_pos:.3f}")
    print(f"Achieved flow: {flow_test * 3600:.1f} m³/h")
    
    # Mass balance check
    Cv_A_test, Cv_B_test = mixing_valve._calculate_cv_split(test_pos)
    flow_hot_test = Cv_A_test * 6.309e-5 * np.sqrt((P_hot - P_mixed) / rho)
    flow_cold_test = Cv_B_test * 6.309e-5 * np.sqrt((P_cold - P_mixed) / rho)
    
    mass_balance_error = abs(flow_test - (flow_hot_test + flow_cold_test))
    print(f"Mass balance error: {mass_balance_error:.2e} m³/s")
    
    # Control scenario simulation
    print("\nCONTROL SCENARIO SIMULATION:")
    print("-" * 35)
    print("Temperature control during process upset")
    
    time_sim = np.linspace(0, 7200, 721)  # 2 hours, 10s intervals
    temp_setpoint = []
    valve_position = []
    mixed_temperature = []
    
    for i, t in enumerate(time_sim):
        # Setpoint changes during operation
        if t < 1800:  # First 30 min
            setpoint = 85.0
        elif t < 3600:  # Next 30 min  
            setpoint = 90.0
        elif t < 5400:  # Next 30 min
            setpoint = 80.0
        else:  # Final 30 min
            setpoint = 85.0
        
        temp_setpoint.append(setpoint)
        
        # Calculate required position for setpoint
        required_ratio = (setpoint - T_cold) / (T_hot - T_cold)
        required_pos = 1.0 - required_ratio
        valve_position.append(required_pos)
        
        # Calculate actual mixed temperature
        u_sim = np.array([required_pos, P_hot, P_cold, P_mixed, rho])
        steady_sim = mixing_valve.steady_state(u_sim)
        _, total_flow_sim = steady_sim
        
        # Individual flows and temperature
        Cv_A_sim, Cv_B_sim = mixing_valve._calculate_cv_split(required_pos)
        flow_hot_sim = Cv_A_sim * 6.309e-5 * np.sqrt((P_hot - P_mixed) / rho)
        flow_cold_sim = Cv_B_sim * 6.309e-5 * np.sqrt((P_cold - P_mixed) / rho)
        
        mass_hot_sim = flow_hot_sim * rho
        mass_cold_sim = flow_cold_sim * rho
        total_mass_sim = mass_hot_sim + mass_cold_sim
        
        if total_mass_sim > 0:
            T_actual = (mass_hot_sim * T_hot + mass_cold_sim * T_cold) / total_mass_sim
        else:
            T_actual = T_cold
            
        mixed_temperature.append(T_actual)
    
    # Report control performance
    temp_error = np.array(mixed_temperature) - np.array(temp_setpoint)
    rms_error = np.sqrt(np.mean(temp_error**2))
    
    print(f"RMS Temperature Error: {rms_error:.2f} °C")
    print(f"Max Temperature Error: {np.max(np.abs(temp_error)):.2f} °C")
    print(f"Position Range: {np.min(valve_position):.3f} - {np.max(valve_position):.3f}")
    
    # Valve descriptions
    print("\nVALVE DESCRIPTIONS:")
    print("-" * 25)
    
    mixing_desc = mixing_valve.describe()
    print(f"Mixing Valve - Type: {mixing_desc['type']}")
    print(f"Applications: {', '.join(mixing_desc['applications'][:2])}")
    
    diverting_desc = diverting_valve.describe()
    print(f"Diverting Valve - Type: {diverting_desc['type']}")
    print(f"Applications: {', '.join(diverting_desc['applications'][:2])}")
    
    print("\n" + "=" * 65)
    print("EXAMPLE COMPLETED - Check plots for visual analysis")
    print("=" * 65)
    
    return {
        'mixing': {
            'positions': positions,
            'temperatures': temperatures,
            'total_flows': total_flows,
            'hot_flows': hot_flows,
            'cold_flows': cold_flows
        },
        'diverting': {
            'positions': positions,
            'product1_flows': product1_flows,
            'product2_flows': product2_flows
        },
        'simulation': {
            'time': time_sim,
            'setpoint': temp_setpoint,
            'valve_position': valve_position,
            'mixed_temperature': mixed_temperature
        }
    }


if __name__ == "__main__":
    data = main()
    
    # Create comprehensive plots
    plt.style.use('default')
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: Mixing valve temperature control
    ax1.plot(data['mixing']['positions'], data['mixing']['temperatures'], 
             'b-', linewidth=3, marker='o', markersize=6)
    ax1.axhline(y=85, color='r', linestyle='--', linewidth=2, label='Target (85°C)')
    ax1.set_xlabel('Valve Position (0=Hot, 1=Cold)')
    ax1.set_ylabel('Mixed Temperature (°C)')
    ax1.set_title('Mixing Valve Temperature Control\nHot (120°C) + Cold (25°C) Streams')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 1)
    
    # Plot 2: Flow distribution in mixing
    ax2.plot(data['mixing']['positions'], data['mixing']['hot_flows'], 
             'r-', linewidth=2, marker='s', label='Hot Stream')
    ax2.plot(data['mixing']['positions'], data['mixing']['cold_flows'], 
             'b-', linewidth=2, marker='^', label='Cold Stream')
    ax2.plot(data['mixing']['positions'], data['mixing']['total_flows'], 
             'k--', linewidth=2, label='Total Flow')
    ax2.set_xlabel('Valve Position')
    ax2.set_ylabel('Flow Rate (m³/h)')
    ax2.set_title('Flow Distribution - Mixing Valve')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 1)
    
    # Plot 3: Diverting valve performance
    ax3.plot(data['diverting']['positions'], data['diverting']['product1_flows'], 
             'g-', linewidth=2, marker='o', label='Product 1 (2 bar)')
    ax3.plot(data['diverting']['positions'], data['diverting']['product2_flows'], 
             'm-', linewidth=2, marker='s', label='Product 2 (1.5 bar)')
    ax3.set_xlabel('Valve Position (0=Product1, 1=Product2)')
    ax3.set_ylabel('Flow Rate (m³/h)')
    ax3.set_title('Diverting Valve Flow Distribution')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, 1)
    
    # Plot 4: Temperature control simulation
    time_hours = np.array(data['simulation']['time']) / 3600
    ax4.plot(time_hours, data['simulation']['setpoint'], 
             'r--', linewidth=2, label='Setpoint')
    ax4.plot(time_hours, data['simulation']['mixed_temperature'], 
             'b-', linewidth=2, label='Actual')
    ax4.set_xlabel('Time (hours)')
    ax4.set_ylabel('Temperature (°C)')
    ax4.set_title('Temperature Control Response\nSetpoint Changes During Operation')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(0, 2)
    
    plt.tight_layout()
    plt.savefig('/Users/macmini/Desktop/github/sproclib/sproclib/unit/valve/ThreeWayValve_example_plots.png', 
                dpi=300, bbox_inches='tight')
    
    # Additional detailed analysis
    fig2, ((ax5, ax6), (ax7, ax8)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 5: Flow coefficient splitting
    positions_fine = np.linspace(0, 1, 101)
    cv_A = [180.0 * (1 - pos) for pos in positions_fine]
    cv_B = [180.0 * pos for pos in positions_fine]
    
    ax5.plot(positions_fine, cv_A, 'r-', linewidth=2, label='Path A (Hot/Inlet)')
    ax5.plot(positions_fine, cv_B, 'b-', linewidth=2, label='Path B (Cold/Outlet)')
    ax5.plot(positions_fine, np.array(cv_A) + np.array(cv_B), 
             'k--', linewidth=2, label='Total Cv')
    ax5.set_xlabel('Valve Position')
    ax5.set_ylabel('Flow Coefficient Cv (gpm/psi^0.5)')
    ax5.set_title('Flow Coefficient Distribution')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # Plot 6: Pressure drop sensitivity
    pressure_drops = np.linspace(0.5, 5.0, 10)  # 0.5 to 5 bar
    flows_pd = []
    for dp in pressure_drops:
        flow = 180.0 * 0.5 * 6.309e-5 * np.sqrt(dp * 1e5 / 890.0) * 3600  # m³/h at 50% position
        flows_pd.append(flow)
    
    ax6.plot(pressure_drops, flows_pd, 'purple', linewidth=2, marker='d')
    ax6.set_xlabel('Pressure Drop (bar)')
    ax6.set_ylabel('Flow Rate (m³/h)')
    ax6.set_title('Flow vs Pressure Drop\n(50% Position, Single Path)')
    ax6.grid(True, alpha=0.3)
    
    # Plot 7: Valve position during control
    ax7.plot(time_hours, np.array(data['simulation']['valve_position']), 
             'orange', linewidth=2)
    ax7.set_xlabel('Time (hours)')
    ax7.set_ylabel('Valve Position')
    ax7.set_title('Valve Position During Control\n(0=Hot, 1=Cold)')
    ax7.grid(True, alpha=0.3)
    ax7.set_xlim(0, 2)
    ax7.set_ylim(0, 1)
    
    # Plot 8: Split ratio analysis for diverting valve
    split_ratios = []
    for i in range(len(data['diverting']['positions'])):
        p1 = data['diverting']['product1_flows'][i]
        p2 = data['diverting']['product2_flows'][i]
        if p2 > 0:
            ratio = p1 / p2
        else:
            ratio = 0
        split_ratios.append(ratio)
    
    ax8.semilogy(data['diverting']['positions'], split_ratios, 
                 'brown', linewidth=2, marker='*')
    ax8.set_xlabel('Valve Position')
    ax8.set_ylabel('Flow Ratio (Product1/Product2)')
    ax8.set_title('Flow Split Ratio (Log Scale)\nDiverting Valve')
    ax8.grid(True, alpha=0.3)
    ax8.set_xlim(0, 1)
    
    plt.tight_layout()
    plt.savefig('/Users/macmini/Desktop/github/sproclib/sproclib/unit/valve/ThreeWayValve_detailed_analysis.png', 
                dpi=300, bbox_inches='tight')
    
    print("\nPlots saved:")
    print("- ThreeWayValve_example_plots.png")
    print("- ThreeWayValve_detailed_analysis.png")
