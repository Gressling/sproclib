#!/usr/bin/env python3
"""
Industrial Example: Process Optimization for Chemical Plant Operations

This example demonstrates process optimization for typical chemical engineering
applications including reactor design, heat exchanger networks, and operating
condition optimization.

Typical plant conditions and industrial scale operations.
"""

import numpy as np
import matplotlib.pyplot as plt
from .process_optimization import ProcessOptimization

def main():
    print("=" * 70)
    print("PROCESS OPTIMIZATION - INDUSTRIAL CHEMICAL ENGINEERING EXAMPLES")
    print("=" * 70)
    
    # Create optimization instance
    optimizer = ProcessOptimization("Chemical Plant Optimization")
    
    print(f"\nOptimizer: {optimizer.name}")
    print(f"Capabilities: {len(optimizer.describe()['applications'])} application areas")
    
    # Example 1: CSTR Reactor Volume Optimization
    print("\n" + "="*50)
    print("EXAMPLE 1: CSTR REACTOR VOLUME OPTIMIZATION")
    print("="*50)
    
    # Process conditions (typical industrial scale)
    flow_rate = 0.5  # m³/s (1800 m³/h)
    concentration_feed = 2.0  # kmol/m³
    conversion_target = 0.85  # 85% conversion
    k_reaction = 0.1  # s⁻¹ (first order reaction rate constant)
    
    print(f"Feed flow rate: {flow_rate} m³/s ({flow_rate*3600:.0f} m³/h)")
    print(f"Feed concentration: {concentration_feed} kmol/m³")
    print(f"Target conversion: {conversion_target*100:.1f}%")
    print(f"Reaction rate constant: {k_reaction} s⁻¹")
    
    def reactor_total_cost(x):
        """
        Total cost function for CSTR reactor.
        Capital cost scales with V^0.6, operating cost inversely with residence time.
        """
        volume = x[0]  # m³
        if volume <= 0:
            return 1e10  # Invalid volume penalty
        
        # Residence time for CSTR
        tau = volume / flow_rate  # s
        
        # Conversion for first-order reaction in CSTR: X = k*tau / (1 + k*tau)
        conversion = (k_reaction * tau) / (1 + k_reaction * tau)
        
        if conversion < conversion_target:
            return 1e10  # Penalty for not meeting conversion target
        
        # Cost components (typical industrial scaling)
        capital_cost = 50000 * (volume ** 0.6)  # $ (equipment cost scaling)
        operating_cost_annual = 10000 * volume  # $/year (utilities, maintenance)
        
        # Convert to total cost (capital + 10 years operating)
        total_cost = capital_cost + 10 * operating_cost_annual
        
        return total_cost
    
    # Optimization bounds: 1 m³ to 50 m³ (industrial range)
    from scipy.optimize import Bounds
    bounds = Bounds([1.0], [50.0])
    
    # Initial guess: 10 m³
    x0 = [10.0]
    
    result = optimizer.optimize(reactor_total_cost, x0, bounds=bounds)
    
    if result['success']:
        optimal_volume = result['x'][0]
        optimal_cost = result['fun']
        tau_optimal = optimal_volume / flow_rate
        conversion_achieved = (k_reaction * tau_optimal) / (1 + k_reaction * tau_optimal)
        
        print(f"\nOptimal reactor volume: {optimal_volume:.2f} m³")
        print(f"Residence time: {tau_optimal:.1f} s ({tau_optimal/60:.2f} min)")
        print(f"Conversion achieved: {conversion_achieved*100:.2f}%")
        print(f"Total cost (10-year): ${optimal_cost:,.0f}")
        
        # Economic analysis
        capital = 50000 * (optimal_volume ** 0.6)
        operating_annual = 10000 * optimal_volume
        print(f"Capital cost: ${capital:,.0f}")
        print(f"Annual operating cost: ${operating_annual:,.0f}/year")
    
    # Example 2: Heat Exchanger Network Optimization
    print("\n" + "="*50)
    print("EXAMPLE 2: SHELL-AND-TUBE HEAT EXCHANGER OPTIMIZATION")
    print("="*50)
    
    # Heat exchanger design parameters
    Q_duty = 5e6  # W (5 MW heat duty)
    T_hot_in = 180 + 273.15  # K (180°C)
    T_hot_out = 80 + 273.15  # K (80°C)
    T_cold_in = 25 + 273.15  # K (25°C)
    T_cold_out = 120 + 273.15  # K (120°C)
    
    # Calculate LMTD
    delta_T1 = T_hot_in - T_cold_out  # K
    delta_T2 = T_hot_out - T_cold_in  # K
    LMTD = (delta_T1 - delta_T2) / np.log(delta_T1 / delta_T2)  # K
    
    print(f"Heat duty: {Q_duty/1e6:.1f} MW")
    print(f"Hot fluid: {T_hot_in-273.15:.0f}°C → {T_hot_out-273.15:.0f}°C")
    print(f"Cold fluid: {T_cold_in-273.15:.0f}°C → {T_cold_out-273.15:.0f}°C")
    print(f"LMTD: {LMTD:.1f} K")
    
    def heat_exchanger_cost(x):
        """
        Heat exchanger total cost optimization.
        Trade-off between area (capital) and pressure drop (pumping).
        """
        area = x[0]  # m²
        if area <= 0:
            return 1e10
        
        # Overall heat transfer coefficient (typical for liquid-liquid)
        U = 800  # W/m²/K
        
        # Check if area is sufficient for heat duty
        Q_possible = U * area * LMTD
        if Q_possible < Q_duty:
            return 1e10  # Insufficient area penalty
        
        # Capital cost (shell-and-tube heat exchanger)
        capital_cost = 15000 + 500 * area  # $ (base cost + area cost)
        
        # Pressure drop cost (simplified - inversely proportional to area)
        # Larger area → lower velocity → lower pressure drop → lower pumping cost
        pressure_drop_annual_cost = 20000 / (area / 100)  # $/year
        
        # Total cost (capital + 15 years pumping)
        total_cost = capital_cost + 15 * pressure_drop_annual_cost
        
        return total_cost
    
    # Bounds: 50 m² to 2000 m² (practical industrial range)
    bounds_hx = Bounds([50.0], [2000.0])
    x0_hx = [300.0]  # Initial guess: 300 m²
    
    result_hx = optimizer.optimize(heat_exchanger_cost, x0_hx, bounds=bounds_hx)
    
    if result_hx['success']:
        optimal_area = result_hx['x'][0]
        optimal_cost_hx = result_hx['fun']
        
        # Performance calculations
        U = 800  # W/m²/K
        Q_actual = U * optimal_area * LMTD
        area_safety_factor = Q_actual / Q_duty
        
        print(f"\nOptimal heat transfer area: {optimal_area:.0f} m²")
        print(f"Safety factor: {area_safety_factor:.2f}")
        print(f"Total cost (15-year): ${optimal_cost_hx:,.0f}")
        
        # Cost breakdown
        capital = 15000 + 500 * optimal_area
        pumping_annual = 20000 / (optimal_area / 100)
        print(f"Capital cost: ${capital:,.0f}")
        print(f"Annual pumping cost: ${pumping_annual:,.0f}/year")
    
    # Example 3: Multi-variable Process Optimization
    print("\n" + "="*50)
    print("EXAMPLE 3: DISTILLATION COLUMN OPTIMIZATION")
    print("="*50)
    
    # Distillation column design parameters
    feed_rate = 100  # kmol/h
    feed_composition = 0.4  # mole fraction light component
    distillate_purity = 0.95  # required purity
    bottoms_purity = 0.05  # maximum light component in bottoms
    
    print(f"Feed rate: {feed_rate} kmol/h")
    print(f"Feed composition: {feed_composition:.2f} mole fraction")
    print(f"Distillate purity target: {distillate_purity:.3f}")
    print(f"Bottoms purity limit: {bottoms_purity:.3f}")
    
    def distillation_cost(x):
        """
        Distillation column optimization: reflux ratio and number of stages.
        """
        reflux_ratio = x[0]  # dimensionless
        num_stages = x[1]  # number of theoretical stages
        
        if reflux_ratio < 1.2 or num_stages < 5:  # Minimum feasible values
            return 1e10
        
        # Simplified column design equations (Fenske-Underwood-Gilliland)
        # For demonstration - in practice, use rigorous simulation
        
        # Minimum stages (Fenske equation approximation)
        alpha = 2.5  # relative volatility (typical for similar components)
        N_min = np.log((distillate_purity/(1-distillate_purity)) * 
                      ((1-bottoms_purity)/bottoms_purity)) / np.log(alpha)
        
        if num_stages < N_min:
            return 1e10
        
        # Column diameter (from vapor load)
        vapor_rate = reflux_ratio * feed_rate * feed_composition  # kmol/h (simplified)
        # Typical vapor velocity and density for sizing
        column_diameter = 0.1 * np.sqrt(vapor_rate)  # m (simplified correlation)
        
        # Capital costs
        column_cost = 50000 + 10000 * num_stages + 5000 * (column_diameter ** 2)
        reboiler_cost = 20000 + 1000 * vapor_rate
        condenser_cost = 15000 + 800 * vapor_rate
        
        # Operating costs (energy)
        reboiler_duty = vapor_rate * 35000  # kJ/h (latent heat)
        steam_cost_annual = reboiler_duty * 0.02 * 8760  # $/year
        cooling_cost_annual = vapor_rate * 100 * 8760  # $/year
        
        total_cost = (column_cost + reboiler_cost + condenser_cost + 
                     10 * (steam_cost_annual + cooling_cost_annual))
        
        return total_cost
    
    # Bounds: reflux ratio 1.2-5.0, stages 5-50
    bounds_dist = Bounds([1.2, 5], [5.0, 50])
    x0_dist = [2.0, 20]  # Initial guess
    
    result_dist = optimizer.optimize(distillation_cost, x0_dist, bounds=bounds_dist)
    
    if result_dist['success']:
        optimal_reflux = result_dist['x'][0]
        optimal_stages = int(result_dist['x'][1])
        optimal_cost_dist = result_dist['fun']
        
        print(f"\nOptimal reflux ratio: {optimal_reflux:.2f}")
        print(f"Optimal number of stages: {optimal_stages}")
        print(f"Total cost (10-year): ${optimal_cost_dist:,.0f}")
        
        # Performance metrics
        vapor_rate = optimal_reflux * feed_rate * feed_composition
        print(f"Vapor rate: {vapor_rate:.1f} kmol/h")
        print(f"Energy efficiency: {1/optimal_reflux:.3f} (higher is better)")
    
    # Summary
    print("\n" + "="*70)
    print("OPTIMIZATION SUMMARY")
    print("="*70)
    print("✓ CSTR reactor volume optimized for minimum total cost")
    print("✓ Heat exchanger area optimized balancing capital vs operating costs")
    print("✓ Distillation column design optimized for energy efficiency")
    print("\nAll optimizations consider:")
    print("- Industrial scale parameters")
    print("- Realistic cost correlations")
    print("- Engineering constraints")
    print("- Economic trade-offs")

if __name__ == "__main__":
    main()
