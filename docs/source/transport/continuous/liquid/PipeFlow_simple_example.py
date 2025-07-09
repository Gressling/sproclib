#!/usr/bin/env python3
"""
PipeFlow Simple Example - Standalone Demonstration

This example demonstrates basic PipeFlow calculations without relying on 
the complex steady_state API. It shows the fundamental pipe flow calculations
using the Darcy-Weisbach equation and friction factor correlations.
"""

import numpy as np
import matplotlib.pyplot as plt

def calculate_pipe_flow(pipe_length, pipe_diameter, roughness, 
                       fluid_density, fluid_viscosity, elevation_change, flow_rate):
    """
    Calculate pipe flow characteristics using Darcy-Weisbach equation
    """
    # Calculate velocity
    area = np.pi * (pipe_diameter/2)**2
    velocity = flow_rate / area
    
    # Calculate Reynolds number
    Re = fluid_density * velocity * pipe_diameter / fluid_viscosity
    
    # Calculate friction factor
    if Re < 2300:
        friction_factor = 64 / Re
        regime = "laminar"
    elif Re > 4000:
        # Swamee-Jain approximation to Colebrook-White
        friction_factor = 0.25 / (np.log10(roughness/(3.7*pipe_diameter) + 5.74/(Re**0.9)))**2
        regime = "turbulent"
    else:
        # Transition region
        f_lam = 64 / Re
        f_turb = 0.25 / (np.log10(roughness/(3.7*pipe_diameter) + 5.74/(Re**0.9)))**2
        friction_factor = f_lam + (f_turb - f_lam) * (Re - 2300) / (4000 - 2300)
        regime = "transition"
    
    # Calculate pressure loss
    friction_loss = friction_factor * (pipe_length/pipe_diameter) * (fluid_density * velocity**2)/2
    elevation_loss = fluid_density * 9.81 * elevation_change
    total_pressure_loss = friction_loss + elevation_loss
    
    return {
        'velocity': velocity,
        'reynolds_number': Re,
        'friction_factor': friction_factor,
        'pressure_loss': total_pressure_loss,
        'friction_loss': friction_loss,
        'elevation_loss': elevation_loss,
        'flow_regime': regime
    }

def example_1_water_supply():
    """Example 1: Water supply pipeline"""
    print("=" * 60)
    print("EXAMPLE 1: Water Supply Pipeline Analysis")
    print("=" * 60)
    
    # Pipeline parameters
    pipe_length = 500.0      # m
    pipe_diameter = 0.15     # m (15 cm)
    roughness = 0.046e-3     # m (commercial steel)
    fluid_density = 1000.0   # kg/m³ (water)
    fluid_viscosity = 1.002e-3  # Pa·s (water at 20°C)
    elevation_change = 25.0  # m
    
    print(f"Pipeline Configuration:")
    print(f"Length: {pipe_length} m")
    print(f"Diameter: {pipe_diameter*1000:.0f} mm")
    print(f"Roughness: {roughness*1e6:.0f} microns")
    print(f"Elevation Rise: {elevation_change} m")
    
    # Flow rate analysis
    flow_rates = [0.01, 0.05, 0.1, 0.15, 0.2]  # m³/s
    
    print(f"\nFlow Rate Analysis:")
    print("Flow Rate | Velocity | Reynolds | Friction | Pressure | Flow")
    print("(L/s)     | (m/s)    | Number   | Factor   | Drop(kPa)| Regime")
    print("-" * 70)
    
    results = []
    for flow in flow_rates:
        result = calculate_pipe_flow(pipe_length, pipe_diameter, roughness,
                                   fluid_density, fluid_viscosity, elevation_change, flow)
        
        flow_ls = flow * 1000
        velocity = result['velocity']
        reynolds = result['reynolds_number']
        friction = result['friction_factor']
        pressure_kpa = result['pressure_loss'] / 1000
        regime = result['flow_regime']
        
        print(f"{flow_ls:8.0f}  | {velocity:7.3f}  | {reynolds:8.0f} | {friction:8.5f} | {pressure_kpa:8.1f} | {regime}")
        results.append(result)
    
    return results

def example_2_chemical_transfer():
    """Example 2: Chemical transfer system"""
    print(f"\n" + "=" * 60)
    print("EXAMPLE 2: Chemical Transfer System")
    print("=" * 60)
    
    # Chemical pipeline parameters
    pipe_length = 200.0      # m
    pipe_diameter = 0.10     # m (10 cm)
    roughness = 0.015e-3     # m (smooth lined)
    fluid_density = 1140.0   # kg/m³ (20% H2SO4)
    fluid_viscosity = 1.32e-3  # Pa·s
    elevation_change = 0.0   # m (horizontal)
    
    print(f"Chemical: 20% Sulfuric Acid")
    print(f"Density: {fluid_density} kg/m³")
    print(f"Viscosity: {fluid_viscosity*1000:.2f} mPa*s")
    
    # System curve
    flow_rates = np.linspace(0.005, 0.08, 15)
    
    print(f"\nSystem Curve (Pump Sizing):")
    print("Flow Rate | Pressure Loss | Head Required")
    print("(L/s)     | (kPa)         | (m)")
    print("-" * 40)
    
    system_curve = []
    for flow in flow_rates:
        result = calculate_pipe_flow(pipe_length, pipe_diameter, roughness,
                                   fluid_density, fluid_viscosity, elevation_change, flow)
        
        flow_ls = flow * 1000
        pressure_kpa = result['pressure_loss'] / 1000
        head_m = result['pressure_loss'] / (fluid_density * 9.81)
        
        if abs(flow_ls % 10) < 2:  # Print every ~10 L/s
            print(f"{flow_ls:8.1f}  | {pressure_kpa:11.1f}   | {head_m:8.2f}")
        
        system_curve.append({'flow': flow, 'pressure': result['pressure_loss'], 'head': head_m})
    
    return system_curve

def example_3_roughness_study():
    """Example 3: Effect of pipe roughness"""
    print(f"\n" + "=" * 60)
    print("EXAMPLE 3: Pipe Roughness Study")
    print("=" * 60)
    
    # Base parameters
    pipe_length = 300.0
    pipe_diameter = 0.12
    fluid_density = 1000.0
    fluid_viscosity = 1e-3
    elevation_change = 0.0
    flow_rate = 0.05  # 50 L/s
    
    # Different pipe conditions
    conditions = [
        {'name': 'New Stainless Steel', 'roughness': 0.015e-3},
        {'name': 'Used Stainless Steel', 'roughness': 0.030e-3},
        {'name': 'New Carbon Steel', 'roughness': 0.046e-3},
        {'name': 'Aged Carbon Steel', 'roughness': 0.150e-3},
        {'name': 'Heavily Fouled', 'roughness': 0.500e-3}
    ]
    
    print(f"Flow Rate: {flow_rate*1000:.0f} L/s")
    print("Pipe Condition        | Roughness | Pressure | Friction | Power")
    print("                      | (μm)      | Loss(kPa)| Factor   | (kW)")
    print("-" * 65)
    
    roughness_data = []
    for condition in conditions:
        result = calculate_pipe_flow(pipe_length, pipe_diameter, condition['roughness'],
                                   fluid_density, fluid_viscosity, elevation_change, flow_rate)
        
        roughness_um = condition['roughness'] * 1e6
        pressure_kpa = result['pressure_loss'] / 1000
        friction_factor = result['friction_factor']
        power_kw = result['pressure_loss'] * flow_rate / 1000
        
        print(f"{condition['name']:20s} | {roughness_um:8.0f}  | {pressure_kpa:8.1f} | {friction_factor:8.5f} | {power_kw:6.2f}")
        
        roughness_data.append({
            'name': condition['name'],
            'roughness': condition['roughness'],
            'pressure_loss': result['pressure_loss'],
            'friction_factor': friction_factor,
            'power': power_kw
        })
    
    return roughness_data

def create_visualizations():
    """Create visualization plots"""
    print(f"\n" + "=" * 60)
    print("CREATING VISUALIZATION PLOTS")
    print("=" * 60)
    
    # Run examples
    water_results = example_1_water_supply()
    system_curve = example_2_chemical_transfer()
    roughness_data = example_3_roughness_study()
    
    # Create plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Reynolds vs Friction Factor
    ax1 = axes[0, 0]
    reynolds = [1000, 2000, 5000, 10000, 50000, 100000]
    friction_laminar = [64/re for re in reynolds if re < 2300]
    friction_turbulent = [0.25 / (np.log10(0.046e-3/(3.7*0.15) + 5.74/(re**0.9)))**2 
                         for re in reynolds if re > 4000]
    
    re_lam = [re for re in reynolds if re < 2300]
    re_turb = [re for re in reynolds if re > 4000]
    
    ax1.loglog(re_lam, friction_laminar, 'g-', linewidth=2, label='Laminar (f=64/Re)')
    ax1.loglog(re_turb, friction_turbulent, 'r-', linewidth=2, label='Turbulent')
    
    # Add example points
    water_re = [1000, 2000, 5000, 15000, 25000]  # Example values
    water_f = []
    for re in water_re:
        if re < 2300:
            f = 64/re
        else:
            f = 0.25 / (np.log10(0.046e-3/(3.7*0.15) + 5.74/(re**0.9)))**2
        water_f.append(f)
    
    ax1.loglog(water_re, water_f, 'bo', markersize=8, label='Water Pipeline')
    
    ax1.set_xlabel('Reynolds Number')
    ax1.set_ylabel('Friction Factor')
    ax1.set_title('Friction Factor vs Reynolds Number')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot 2: System Curve
    ax2 = axes[0, 1]
    flows = [d['flow']*1000 for d in system_curve]
    heads = [d['head'] for d in system_curve]
    
    ax2.plot(flows, heads, 'b-', linewidth=2, label='System Curve')
    
    # Add example pump curve
    flow_pump = np.linspace(10, 80, 50)
    head_pump = 25 - 0.003 * flow_pump**2
    ax2.plot(flow_pump, head_pump, 'r-', linewidth=2, label='Example Pump')
    
    ax2.set_xlabel('Flow Rate (L/s)')
    ax2.set_ylabel('Head (m)')
    ax2.set_title('System and Pump Curves')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Plot 3: Roughness Effects
    ax3 = axes[1, 0]
    roughness_values = [d['roughness']*1e6 for d in roughness_data]
    pressure_losses = [d['pressure_loss']/1000 for d in roughness_data]
    
    ax3.semilogx(roughness_values, pressure_losses, 'mo-', linewidth=2, markersize=8)
    ax3.set_xlabel('Pipe Roughness (μm)')
    ax3.set_ylabel('Pressure Loss (kPa)')
    ax3.set_title('Effect of Pipe Roughness')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Flow Regime Map
    ax4 = axes[1, 1]
    
    # Create flow regime boundaries
    velocities = np.linspace(0.1, 5, 100)
    diameters = np.linspace(0.05, 0.5, 100)
    V, D = np.meshgrid(velocities, diameters)
    
    # Reynolds number for water
    rho = 1000  # kg/m³
    mu = 1e-3   # Pa·s
    Re = rho * V * D / mu
    
    # Create regime map
    regime_map = np.zeros_like(Re)
    regime_map[Re < 2300] = 1  # Laminar
    regime_map[(Re >= 2300) & (Re < 4000)] = 2  # Transition
    regime_map[Re >= 4000] = 3  # Turbulent
    
    contour = ax4.contourf(V, D*100, regime_map, levels=[0, 1, 2, 3, 4], 
                          colors=['white', 'lightgreen', 'yellow', 'lightcoral'], alpha=0.7)
    
    # Add contour lines for Reynolds numbers
    cs = ax4.contour(V, D*100, Re, levels=[2300, 4000], colors=['black'], linestyles=['--'])
    ax4.clabel(cs, inline=True, fontsize=10)
    
    ax4.set_xlabel('Velocity (m/s)')
    ax4.set_ylabel('Pipe Diameter (cm)')
    ax4.set_title('Flow Regime Map (Water)')
    
    plt.tight_layout()
    plt.savefig('PipeFlow_example_plots.png', dpi=300, bbox_inches='tight')
    print("Saved plots to: PipeFlow_example_plots.png")
    
    return True

def main():
    """Main function"""
    print("PipeFlow Simple Example Suite")
    print("============================")
    print("Basic pipe flow calculations using Darcy-Weisbach equation")
    
    try:
        example_1_water_supply()
        example_2_chemical_transfer()
        example_3_roughness_study()
        create_visualizations()
        
        print(f"\n" + "=" * 60)
        print("EXAMPLES COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("Generated: PipeFlow_example_plots.png")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    main()
