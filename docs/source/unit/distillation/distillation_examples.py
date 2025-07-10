"""
Distillation Examples - SPROCLIB
================================

This module contains examples demonstrating the usage of distillation units in SPROCLIB.
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

from unit.distillation.column.BinaryDistillationColumn import BinaryDistillationColumn
from unit.distillation.tray.DistillationTray import DistillationTray


def simple_distillation_examples():
    """
    Simple examples of using distillation units.
    
    This example demonstrates basic distillation operations.
    """
    print("=== Simple Distillation Examples ===")
    
    # Binary Distillation Column
    print("\n--- Binary Distillation Column ---")
    column = BinaryDistillationColumn(name="Basic Binary Column")
    
    print(f"Distillation column created: {column.name}")
    print(f"Type: {type(column).__name__}")
    
    # Set basic parameters
    feed_rate = 1000.0  # kmol/h
    feed_composition = 0.4  # mole fraction of light component
    distillate_rate = 400.0  # kmol/h
    bottoms_rate = 600.0  # kmol/h
    reflux_ratio = 2.5
    
    print(f"\nColumn specifications:")
    print(f"Feed rate: {feed_rate} kmol/h")
    print(f"Feed composition (light): {feed_composition:.2f}")
    print(f"Distillate rate: {distillate_rate} kmol/h")
    print(f"Bottoms rate: {bottoms_rate} kmol/h")
    print(f"Reflux ratio: {reflux_ratio}")
    
    # Material balance
    light_in_feed = feed_rate * feed_composition
    heavy_in_feed = feed_rate * (1 - feed_composition)
    
    print(f"\nMaterial balance:")
    print(f"Light component in feed: {light_in_feed:.1f} kmol/h")
    print(f"Heavy component in feed: {heavy_in_feed:.1f} kmol/h")
    
    # Assume separation specifications
    distillate_purity = 0.95  # 95% light component
    bottoms_purity = 0.05  # 5% light component (95% heavy)
    
    light_in_distillate = distillate_rate * distillate_purity
    light_in_bottoms = bottoms_rate * bottoms_purity
    recovery = light_in_distillate / light_in_feed * 100
    
    print(f"\nSeparation performance:")
    print(f"Distillate purity: {distillate_purity*100:.1f}%")
    print(f"Bottoms purity (heavy): {(1-bottoms_purity)*100:.1f}%")
    print(f"Light component recovery: {recovery:.1f}%")
    
    # Single Tray Analysis
    print("\n--- Single Distillation Tray ---")
    tray = DistillationTray(name="Equilibrium Tray")
    
    print(f"Distillation tray created: {tray.name}")
    print(f"Type: {type(tray).__name__}")
    
    # Tray parameters
    liquid_flow = 2500.0  # kmol/h (L)
    vapor_flow = 3000.0  # kmol/h (V)
    liquid_composition = 0.3  # x (mole fraction light)
    
    # Relative volatility (constant)
    alpha = 2.5
    
    # Equilibrium calculation
    vapor_composition = alpha * liquid_composition / (1 + (alpha - 1) * liquid_composition)
    
    print(f"\nTray operating conditions:")
    print(f"Liquid flow rate: {liquid_flow} kmol/h")
    print(f"Vapor flow rate: {vapor_flow} kmol/h")
    print(f"Liquid composition: {liquid_composition:.3f}")
    print(f"Relative volatility: {alpha}")
    print(f"Vapor composition (equilibrium): {vapor_composition:.3f}")
    
    # Tray efficiency
    actual_vapor_composition = 0.20  # Given actual composition
    murphree_efficiency = (actual_vapor_composition - liquid_composition) / (vapor_composition - liquid_composition)
    
    print(f"Actual vapor composition: {actual_vapor_composition:.3f}")
    print(f"Murphree tray efficiency: {murphree_efficiency:.3f}")
    
    print("\nSimple distillation examples completed successfully!")


def comprehensive_distillation_examples():
    """
    Comprehensive examples demonstrating advanced distillation operations.
    
    This example includes:
    - McCabe-Thiele analysis
    - Multi-component distillation
    - Column optimization
    - Tray hydraulics
    - Energy analysis
    """
    print("\n=== Comprehensive Distillation Examples ===")
    
    # McCabe-Thiele Analysis
    print("\n--- McCabe-Thiele Method Analysis ---")
    
    column = BinaryDistillationColumn(name="McCabe-Thiele Column")
    
    # System parameters
    alpha = 2.4  # Relative volatility
    feed_composition = 0.45
    distillate_composition = 0.95
    bottoms_composition = 0.05
    
    print(f"McCabe-Thiele Analysis:")
    print(f"Relative volatility: {alpha}")
    print(f"Feed composition: {feed_composition:.2f}")
    print(f"Distillate composition: {distillate_composition:.2f}")
    print(f"Bottoms composition: {bottoms_composition:.2f}")
    
    # Calculate minimum reflux ratio
    x_values = np.linspace(0, 1, 21)
    y_eq = alpha * x_values / (1 + (alpha - 1) * x_values)
    
    # q-line (assume saturated liquid feed, q = 1)
    q = 1.0
    
    # Intersection of q-line with equilibrium curve at feed composition
    y_q_intersection = alpha * feed_composition / (1 + (alpha - 1) * feed_composition)
    
    # Minimum reflux calculation
    r_min = (distillate_composition - y_q_intersection) / (y_q_intersection - feed_composition)
    
    print(f"q-value (feed condition): {q}")
    print(f"Minimum reflux ratio: {r_min:.2f}")
    
    # Analyze different reflux ratios
    reflux_ratios = [1.2 * r_min, 1.5 * r_min, 2.0 * r_min, 3.0 * r_min]
    
    print(f"\n{'R/Rmin':<8} {'R':<8} {'Theoretical Stages':<18} {'Energy (relative)':<15}")
    print("-" * 55)
    
    for r in reflux_ratios:
        r_ratio = r / r_min
        
        # Approximate number of stages (simplified Gilliland correlation)
        y_gilliland = (r - r_min) / (r + 1)
        stages_approx = 5 + 10 * (1 - y_gilliland)  # Simplified estimate
        
        # Relative energy consumption
        energy_relative = r / r_min  # Proportional to reflux ratio
        
        print(f"{r_ratio:<8.1f} {r:<8.2f} {stages_approx:<18.1f} {energy_relative:<15.2f}")
    
    # Tray-by-Tray Calculation
    print("\n--- Tray-by-Tray Calculation ---")
    
    # Operating conditions
    operating_reflux = 1.5 * r_min
    
    print(f"Tray-by-tray calculation with R = {operating_reflux:.2f}")
    
    # Rectifying section operating line
    slope_rect = operating_reflux / (operating_reflux + 1)
    intercept_rect = distillate_composition / (operating_reflux + 1)
    
    print(f"Rectifying line: y = {slope_rect:.3f}x + {intercept_rect:.3f}")
    
    # Step-by-step calculation (simplified)
    stages = []
    x_current = distillate_composition
    stage_count = 0
    
    print(f"\n{'Stage':<6} {'x_liquid':<10} {'y_vapor':<10} {'y_operating':<12}")
    print("-" * 45)
    
    while x_current > bottoms_composition and stage_count < 15:
        stage_count += 1
        
        # Equilibrium
        y_eq_current = alpha * x_current / (1 + (alpha - 1) * x_current)
        
        # Operating line
        if x_current > feed_composition:
            # Rectifying section
            y_operating = slope_rect * x_current + intercept_rect
        else:
            # Stripping section (simplified)
            slope_strip = 1.2  # Simplified
            y_operating = slope_strip * x_current - 0.1
        
        stages.append([stage_count, x_current, y_eq_current, y_operating])
        print(f"{stage_count:<6} {x_current:<10.3f} {y_eq_current:<10.3f} {y_operating:<12.3f}")
        
        # Next liquid composition (from operating line)
        x_current = (y_eq_current - intercept_rect) / slope_rect if y_eq_current > intercept_rect else bottoms_composition
        
        if x_current <= bottoms_composition:
            break
    
    print(f"Total theoretical stages: {stage_count}")
    
    # Multi-Component Analysis
    print("\n--- Multi-Component Distillation ---")
    
    # Three-component system (simplified)
    components = ["Light", "Medium", "Heavy"]
    feed_compositions = [0.3, 0.4, 0.3]  # Mole fractions
    relative_volatilities = [4.0, 2.0, 1.0]  # Relative to heavy component
    
    print("Multi-component system:")
    print(f"{'Component':<10} {'Feed (mol%)':<12} {'Rel. Volatility':<15}")
    print("-" * 40)
    
    for i, comp in enumerate(components):
        print(f"{comp:<10} {feed_compositions[i]*100:<12.1f} {relative_volatilities[i]:<15.1f}")
    
    # Simplified flash calculation at different temperatures
    temperatures = [80, 100, 120, 140]  # °C
    
    print(f"\nFlash vaporization at different temperatures:")
    print(f"{'Temp (°C)':<10} {'Vapor Fraction':<15} {'Light in Vapor':<15} {'Heavy in Liquid':<15}")
    print("-" * 65)
    
    for temp in temperatures:
        # Simplified K-values (temperature dependent)
        k_values = [rel_vol * np.exp(1000 * (1/373 - 1/(temp + 273))) for rel_vol in relative_volatilities]
        
        # Rachford-Rice equation (simplified for equal molar case)
        vapor_fraction = 0.5  # Simplified assumption
        
        # Vapor phase compositions
        vapor_comps = [feed_compositions[i] * k_values[i] / (1 + vapor_fraction * (k_values[i] - 1)) for i in range(3)]
        liquid_comps = [feed_compositions[i] / (1 + vapor_fraction * (k_values[i] - 1)) for i in range(3)]
        
        # Normalize
        vapor_sum = sum(vapor_comps)
        liquid_sum = sum(liquid_comps)
        vapor_comps = [v/vapor_sum for v in vapor_comps]
        liquid_comps = [l/liquid_sum for l in liquid_comps]
        
        print(f"{temp:<10} {vapor_fraction:<15.2f} {vapor_comps[0]:<15.3f} {liquid_comps[2]:<15.3f}")
    
    # Tray Hydraulics Analysis
    print("\n--- Tray Hydraulics ---")
    
    tray = DistillationTray(name="Sieve Tray")
    
    # Tray design parameters
    tray_diameter = 3.0  # m
    tray_area = np.pi * (tray_diameter/2)**2
    active_area = 0.85 * tray_area  # 85% active area
    hole_area = 0.10 * active_area  # 10% hole area
    weir_height = 0.05  # m
    
    print(f"Sieve Tray Design:")
    print(f"Tray diameter: {tray_diameter} m")
    print(f"Active area: {active_area:.2f} m²")
    print(f"Hole area: {hole_area:.2f} m²")
    print(f"Weir height: {weir_height} m")
    
    # Operating conditions for hydraulics
    liquid_rates = [50, 100, 150, 200, 250]  # m³/h
    vapor_rates = [2000, 4000, 6000, 8000, 10000]  # m³/h
    
    print(f"\n{'Liquid Rate':<12} {'Vapor Rate':<12} {'Weep Rate':<12} {'Pressure Drop':<15} {'Flooding %':<12}")
    print("-" * 75)
    
    for i, (liq_rate, vap_rate) in enumerate(zip(liquid_rates, vapor_rates)):
        # Liquid velocity over weir
        weir_length = 0.7 * tray_diameter  # Simplified
        liquid_velocity = liq_rate / weir_length
        
        # Vapor velocity through holes
        vapor_velocity = vap_rate / (hole_area * 3600)  # m/s
        
        # Pressure drop (simplified)
        pressure_drop = 0.5 * 1.2 * vapor_velocity**2 / 1000  # kPa (simplified)
        
        # Weeping check (simplified)
        weep_rate = max(0, 20 - vapor_velocity * 10)  # % (very simplified)
        
        # Flooding percentage (simplified)
        flooding_percent = vapor_velocity / 3.0 * 100  # Assuming 3 m/s is flood point
        
        print(f"{liq_rate:<12.0f} {vap_rate:<12.0f} {weep_rate:<12.1f} {pressure_drop:<15.2f} {flooding_percent:<12.1f}")
    
    # Energy Analysis
    print("\n--- Energy Analysis ---")
    
    # Energy requirements for different separations
    separations = [
        {"name": "Easy", "alpha": 3.0, "recovery": 95},
        {"name": "Moderate", "alpha": 2.0, "recovery": 95},
        {"name": "Difficult", "alpha": 1.5, "recovery": 95},
        {"name": "Very Difficult", "alpha": 1.2, "recovery": 90}
    ]
    
    print("Energy requirements for different separations:")
    print(f"{'Separation':<15} {'Alpha':<8} {'Recovery (%)':<12} {'Min Stages':<12} {'Energy Index':<12}")
    print("-" * 70)
    
    for sep in separations:
        # Simplified minimum stages (Fenske equation approximation)
        min_stages = np.log((distillate_composition/(1-distillate_composition)) * ((1-bottoms_composition)/bottoms_composition)) / np.log(sep["alpha"])
        
        # Energy index (relative)
        energy_index = min_stages / sep["alpha"]  # Simplified metric
        
        print(f"{sep['name']:<15} {sep['alpha']:<8.1f} {sep['recovery']:<12} {min_stages:<12.1f} {energy_index:<12.2f}")
    
    print("\nComprehensive distillation examples completed successfully!")


def main():
    """
    Main function to run all distillation examples.
    """
    print("SPROCLIB Distillation Examples")
    print("=" * 50)
    
    try:
        # Run simple examples
        simple_distillation_examples()
        
        # Run comprehensive examples
        comprehensive_distillation_examples()
        
        print("\n" + "=" * 50)
        print("All distillation examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
