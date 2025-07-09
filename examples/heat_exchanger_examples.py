"""
Heat Exchanger Examples - SPROCLIB
==================================

This module contains examples demonstrating the usage of heat exchanger units in SPROCLIB.
Each example includes both simple and comprehensive use cases.

Requirements:
- NumPy
- SciPy
- Matplotlib (for plotting)
"""

import numpy as np
import sys
import os

# Add the process_control directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unit.heat_exchanger.HeatExchanger import HeatExchanger


def simple_heat_exchanger_examples():
    """
    Simple examples of using heat exchanger units.
    
    This example demonstrates basic heat exchanger operations.
    """
    print("=== Simple Heat Exchanger Examples ===")
    
    # Basic Heat Exchanger
    print("\n--- Basic Heat Exchanger ---")
    heat_exchanger = HeatExchanger(name="Basic Shell-and-Tube HX")
    
    print(f"Heat exchanger created: {heat_exchanger.name}")
    print(f"Type: {type(heat_exchanger).__name__}")
    
    # Set basic parameters
    hot_inlet_temp = 150.0  # °C
    hot_outlet_temp = 100.0  # °C
    cold_inlet_temp = 25.0  # °C
    hot_flow_rate = 5000.0  # kg/h
    cold_flow_rate = 4000.0  # kg/h
    hot_cp = 4.18  # kJ/kg·K (water)
    cold_cp = 4.18  # kJ/kg·K (water)
    
    print(f"\nOperating conditions:")
    print(f"Hot fluid inlet: {hot_inlet_temp}°C")
    print(f"Hot fluid outlet: {hot_outlet_temp}°C")
    print(f"Cold fluid inlet: {cold_inlet_temp}°C")
    print(f"Hot flow rate: {hot_flow_rate} kg/h")
    print(f"Cold flow rate: {cold_flow_rate} kg/h")
    
    # Heat duty calculation
    heat_duty = hot_flow_rate * hot_cp * (hot_inlet_temp - hot_outlet_temp) / 3600  # kW
    
    # Cold outlet temperature
    cold_outlet_temp = cold_inlet_temp + (heat_duty * 3600) / (cold_flow_rate * cold_cp)
    
    print(f"\nResults:")
    print(f"Heat duty: {heat_duty:.1f} kW")
    print(f"Cold fluid outlet: {cold_outlet_temp:.1f}°C")
    
    # Heat exchanger effectiveness
    c_hot = hot_flow_rate * hot_cp / 3600  # kW/K
    c_cold = cold_flow_rate * cold_cp / 3600  # kW/K
    c_min = min(c_hot, c_cold)
    
    max_possible_heat = c_min * (hot_inlet_temp - cold_inlet_temp)
    effectiveness = heat_duty / max_possible_heat
    
    print(f"Heat exchanger effectiveness: {effectiveness:.3f}")
    print(f"Maximum possible heat transfer: {max_possible_heat:.1f} kW")
    
    print("\nSimple heat exchanger examples completed successfully!")


def comprehensive_heat_exchanger_examples():
    """
    Comprehensive examples demonstrating advanced heat exchanger operations.
    
    This example includes:
    - Different flow configurations
    - LMTD and NTU methods
    - Fouling effects
    - Optimization studies
    - Multi-pass configurations
    """
    print("\n=== Comprehensive Heat Exchanger Examples ===")
    
    # Flow Configuration Analysis
    print("\n--- Flow Configuration Comparison ---")
    
    # Common parameters
    hot_inlet = 120.0  # °C
    cold_inlet = 20.0  # °C
    hot_flow = 3600.0  # kg/h
    cold_flow = 3600.0  # kg/h
    cp = 4.18  # kJ/kg·K
    overall_u = 500.0  # W/m²·K
    area = 50.0  # m²
    
    print(f"Common parameters:")
    print(f"Hot inlet: {hot_inlet}°C, Cold inlet: {cold_inlet}°C")
    print(f"Flow rates: {hot_flow} kg/h each")
    print(f"Overall U: {overall_u} W/m²·K")
    print(f"Heat transfer area: {area} m²")
    
    # Calculate for different configurations
    configurations = ["Parallel Flow", "Counter Flow", "Cross Flow"]
    
    print(f"\n{'Configuration':<15} {'Hot Outlet (°C)':<15} {'Cold Outlet (°C)':<16} {'Heat Duty (kW)':<15} {'LMTD (°C)':<12}")
    print("-" * 85)
    
    for config in configurations:
        if config == "Parallel Flow":
            # Parallel flow - simplified calculation
            ntu = overall_u * area / (hot_flow * cp / 3.6)  # NTU
            effectiveness = (1 - np.exp(-2 * ntu)) / 2
        elif config == "Counter Flow":
            # Counter flow
            ntu = overall_u * area / (hot_flow * cp / 3.6)
            effectiveness = ntu / (1 + ntu)  # For equal heat capacity rates
        else:  # Cross flow
            # Cross flow (both unmixed) - approximation
            ntu = overall_u * area / (hot_flow * cp / 3.6)
            effectiveness = 1 - np.exp(-ntu * (1 - np.exp(-ntu)))
        
        # Calculate outlet temperatures
        c_min = hot_flow * cp / 3.6  # kW/K
        heat_duty = effectiveness * c_min * (hot_inlet - cold_inlet)
        
        hot_outlet = hot_inlet - heat_duty / c_min
        cold_outlet = cold_inlet + heat_duty / c_min
        
        # LMTD calculation
        if config == "Parallel Flow":
            dt1 = hot_inlet - cold_inlet
            dt2 = hot_outlet - cold_outlet
        else:  # Counter flow and cross flow
            dt1 = hot_inlet - cold_outlet
            dt2 = hot_outlet - cold_inlet
        
        if dt1 != dt2 and dt1 > 0 and dt2 > 0:
            lmtd = (dt1 - dt2) / np.log(dt1 / dt2)
        else:
            lmtd = dt1  # For very small differences
        
        print(f"{config:<15} {hot_outlet:<15.1f} {cold_outlet:<16.1f} {heat_duty:<15.1f} {lmtd:<12.1f}")
    
    # NTU-Effectiveness Method Analysis
    print("\n--- NTU-Effectiveness Analysis ---")
    
    heat_exchanger = HeatExchanger(name="Design Analysis HX")
    
    # Vary heat capacity rate ratio
    c_ratios = [0.2, 0.5, 0.8, 1.0, 1.5, 2.0]
    ntu_values = np.linspace(0.5, 4.0, 8)
    
    print("Counter-flow Heat Exchanger Effectiveness:")
    print(f"{'C_ratio':<8} " + " ".join([f"{'NTU=' + str(ntu):<8}" for ntu in ntu_values]))
    print("-" * 80)
    
    for c_ratio in c_ratios:
        effectiveness_values = []
        for ntu in ntu_values:
            if c_ratio == 1.0:
                # Special case for equal heat capacity rates
                eff = ntu / (1 + ntu)
            else:
                # General case for counter flow
                eff = (1 - np.exp(-ntu * (1 - c_ratio))) / (1 - c_ratio * np.exp(-ntu * (1 - c_ratio)))
            effectiveness_values.append(eff)
        
        print(f"{c_ratio:<8.1f} " + " ".join([f"{eff:<8.3f}" for eff in effectiveness_values]))
    
    # Fouling Effects Analysis
    print("\n--- Fouling Effects Analysis ---")
    
    # Clean and fouled conditions
    clean_u = 800.0  # W/m²·K
    fouling_resistances = [0, 0.0001, 0.0003, 0.0005, 0.001, 0.002]  # m²·K/W
    
    print("Impact of Fouling on Heat Exchanger Performance:")
    print(f"Clean overall U coefficient: {clean_u} W/m²·K")
    
    print(f"\n{'Fouling Resistance':<18} {'Fouled U (W/m²·K)':<18} {'Performance Loss (%)':<20}")
    print("-" * 60)
    
    for rf in fouling_resistances:
        if rf == 0:
            fouled_u = clean_u
        else:
            # Simplified: 1/U_fouled = 1/U_clean + R_fouling
            fouled_u = 1 / (1/clean_u + rf)
        
        performance_loss = (clean_u - fouled_u) / clean_u * 100
        
        print(f"{rf:<18.4f} {fouled_u:<18.1f} {performance_loss:<20.1f}")
    
    # Multi-Pass Configuration
    print("\n--- Multi-Pass Shell-and-Tube Analysis ---")
    
    # Shell and tube parameters
    shell_passes = [1, 2, 4]
    tube_passes = [2, 4, 6, 8]
    
    print("F-factor for different pass arrangements:")
    print("(Temperature correction factor for LMTD)")
    
    print(f"{'Shell Passes':<13} " + " ".join([f"{'Tube=' + str(tp):<8}" for tp in tube_passes]))
    print("-" * 60)
    
    # Simplified F-factor calculation (approximation)
    for sp in shell_passes:
        f_factors = []
        for tp in tube_passes:
            # Simplified F-factor approximation based on pass arrangement
            if sp == 1:
                f_factor = 0.95 - 0.02 * (tp - 2)  # Decreases with more tube passes
            else:
                f_factor = 0.85 + 0.05 * sp - 0.01 * tp  # Complex interaction
            
            f_factor = max(0.7, min(1.0, f_factor))  # Realistic bounds
            f_factors.append(f_factor)
        
        print(f"{sp:<13} " + " ".join([f"{ff:<8.3f}" for ff in f_factors]))
    
    # Heat Exchanger Sizing Example
    print("\n--- Heat Exchanger Sizing ---")
    
    # Design requirements
    required_duty = 2000.0  # kW
    hot_in = 140.0  # °C
    hot_out = 90.0  # °C
    cold_in = 30.0  # °C
    cold_out = 80.0  # °C
    
    # Calculate required area for different U values
    u_values = [300, 500, 800, 1200, 1500]  # W/m²·K
    
    # LMTD for counter flow
    dt1 = hot_in - cold_out  # 140 - 80 = 60°C
    dt2 = hot_out - cold_in  # 90 - 30 = 60°C
    lmtd = (dt1 - dt2) / np.log(dt1 / dt2) if dt1 != dt2 else dt1
    lmtd = dt1  # Since dt1 = dt2
    
    print(f"Sizing for {required_duty} kW duty:")
    print(f"Hot: {hot_in}°C → {hot_out}°C")
    print(f"Cold: {cold_in}°C → {cold_out}°C")
    print(f"LMTD: {lmtd:.1f}°C")
    
    print(f"\n{'U (W/m²·K)':<12} {'Area (m²)':<12} {'Cost Factor':<12} {'Pressure Drop':<15}")
    print("-" * 60)
    
    for u in u_values:
        area = required_duty * 1000 / (u * lmtd)  # m²
        cost_factor = area * u / 1000  # Relative cost index
        
        # Simplified pressure drop estimation (higher U often means smaller channels)
        pressure_drop = 50 * (u / 500)**0.5  # kPa (rough approximation)
        
        print(f"{u:<12} {area:<12.1f} {cost_factor:<12.1f} {pressure_drop:<15.1f}")
    
    # Performance Optimization
    print("\n--- Performance Optimization Study ---")
    
    # Optimize for minimum total cost (capital + operating)
    flow_rates = np.linspace(2000, 8000, 7)  # kg/h
    base_u = 600  # W/m²·K
    
    print("Optimization study (varying flow rate):")
    print(f"Target heat duty: {required_duty} kW")
    
    print(f"\n{'Flow Rate':<12} {'Velocity':<10} {'U (W/m²·K)':<12} {'Area (m²)':<12} {'Pump Power':<12}")
    print("-" * 70)
    
    for flow in flow_rates:
        # Velocity effect on heat transfer coefficient
        velocity_factor = (flow / 4000) ** 0.8  # Typical for turbulent flow
        u_actual = base_u * velocity_factor
        
        # Required area
        area = required_duty * 1000 / (u_actual * lmtd)
        
        # Pump power (simplified)
        velocity = flow / 3600 / 0.02  # m/s (rough approximation)
        pump_power = 0.5 * velocity**3  # kW (very simplified)
        
        print(f"{flow:<12.0f} {velocity:<10.2f} {u_actual:<12.0f} {area:<12.1f} {pump_power:<12.1f}")
    
    print("\nComprehensive heat exchanger examples completed successfully!")


def main():
    """
    Main function to run all heat exchanger examples.
    """
    print("SPROCLIB Heat Exchanger Examples")
    print("=" * 50)
    
    try:
        # Run simple examples
        simple_heat_exchanger_examples()
        
        # Run comprehensive examples
        comprehensive_heat_exchanger_examples()
        
        print("\n" + "=" * 50)
        print("All heat exchanger examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
