#!/usr/bin/env python3
"""
SlurryPipeline Simple Example
============================
Simplified demonstration of SlurryPipeline class for robust output generation.

This example provides essential SlurryPipeline functionality demonstrations
without complex error-prone dependencies.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from SlurryPipeline import SlurryPipeline

def main():
    """Main function demonstrating SlurryPipeline capabilities"""
    print("SlurryPipeline Simple Example")
    print("=============================")
    print("Basic demonstration of SlurryPipeline class")
    print("Timestamp: 2025-07-09")
    print("=" * 50)
    
    # Example 1: Mining Ore Transport
    print("\nEXAMPLE 1: Mining Ore Transport Pipeline")
    print("-" * 45)
    
    # Create mining ore pipeline
    ore_pipeline = SlurryPipeline(
        pipe_length=50000.0,      # 50 km pipeline
        pipe_diameter=0.6,        # 60 cm diameter
        solid_concentration=0.35, # 35% solids by volume
        particle_diameter=150e-6, # 150 micron particles
        fluid_density=1000.0,     # Water
        solid_density=2700.0,     # Ore density
        fluid_viscosity=1e-3,     # Water viscosity
        flow_nominal=0.5,         # 0.5 m³/s nominal flow
        name="MiningOrePipeline"
    )
    
    print(f"Pipeline: {ore_pipeline.name}")
    print(f"Length: {ore_pipeline.pipe_length/1000:.0f} km")
    print(f"Diameter: {ore_pipeline.pipe_diameter*100:.0f} cm")
    print(f"Solids: {ore_pipeline.solid_concentration*100:.0f}% by volume")
    print(f"Particle Size: {ore_pipeline.particle_diameter*1e6:.0f} microns")
    
    # Calculate steady-state conditions
    # steady_state expects [P_inlet, flow_rate, c_solid_in]
    inlet_pressure = 800000.0  # 800 kPa (8 bar)
    flow_rate = ore_pipeline.flow_nominal
    solid_conc = ore_pipeline.solid_concentration
    
    inputs = np.array([inlet_pressure, flow_rate, solid_conc])
    result = ore_pipeline.steady_state(inputs)
    
    outlet_pressure = result[0]
    outlet_solid_conc = result[1]
    
    # Calculate derived properties
    velocity = flow_rate / (np.pi * (ore_pipeline.pipe_diameter/2)**2)
    mixture_density = (ore_pipeline.fluid_density * (1 - solid_conc) + 
                      ore_pipeline.solid_density * solid_conc)
    pressure_drop = inlet_pressure - outlet_pressure
    
    print(f"\nOperating Conditions:")
    print(f"Inlet Pressure: {inlet_pressure/1000:.0f} kPa")
    print(f"Outlet Pressure: {outlet_pressure/1000:.0f} kPa")
    print(f"Pressure Drop: {pressure_drop/1000:.0f} kPa")
    print(f"Flow Velocity: {velocity:.2f} m/s")
    print(f"Mixture Density: {mixture_density:.0f} kg/m³")
    print(f"Outlet Solids: {outlet_solid_conc*100:.1f}% (settling effect)")
    
    # Critical velocity calculation (Durand equation)
    g = 9.81  # m/s²
    density_ratio = ore_pipeline.solid_density / ore_pipeline.fluid_density
    critical_velocity = 1.5 * np.sqrt(2 * g * ore_pipeline.particle_diameter * (density_ratio - 1))
    
    print(f"\nCritical Velocity Analysis:")
    print(f"Critical Velocity: {critical_velocity:.2f} m/s")
    print(f"Design Velocity: {velocity:.2f} m/s")
    print(f"Safety Factor: {velocity/critical_velocity:.2f}")
    
    if velocity > critical_velocity:
        print("OK Adequate velocity - particles suspended")
    else:
        print("WARNING Low velocity - risk of settling")
    
    # Example 2: Flow Rate Variations
    print("\n\nEXAMPLE 2: Flow Rate Performance Analysis")
    print("-" * 45)
    
    flow_rates = np.linspace(0.1, 1.0, 10)  # 0.1 to 1.0 m³/s
    velocities = []
    pressure_drops = []
    outlet_concentrations = []
    
    print("Flow Rate | Velocity | Pressure Drop | Outlet Solids")
    print("(m³/s)    | (m/s)    | (kPa)         | (%)")
    print("-" * 50)
    
    for flow in flow_rates:
        inputs = np.array([inlet_pressure, flow, solid_conc])
        result = ore_pipeline.steady_state(inputs)
        
        vel = flow / (np.pi * (ore_pipeline.pipe_diameter/2)**2)
        p_drop = inlet_pressure - result[0]
        out_conc = result[1]
        
        velocities.append(vel)
        pressure_drops.append(p_drop)
        outlet_concentrations.append(out_conc)
        
        print(f"{flow:8.2f}  | {vel:7.2f}  | {p_drop/1000:12.0f}  | {out_conc*100:8.1f}")
    
    # Example 3: Particle Size Effects
    print("\n\nEXAMPLE 3: Particle Size Effects")
    print("-" * 35)
    
    particle_sizes = np.array([50, 100, 150, 200, 300, 500]) * 1e-6  # microns to meters
    critical_vels = []
    
    print("Particle Size | Critical Velocity")
    print("(microns)     | (m/s)")
    print("-" * 30)
    
    for size in particle_sizes:
        v_crit = 1.5 * np.sqrt(2 * g * size * (density_ratio - 1))
        critical_vels.append(v_crit)
        print(f"{size*1e6:12.0f}  | {v_crit:14.2f}")
    
    # Create visualization
    create_slurry_plots(flow_rates, velocities, pressure_drops, outlet_concentrations,
                       particle_sizes, critical_vels, ore_pipeline)
    
    print(f"\n\nExample completed successfully!")
    print(f"Generated: SlurryPipeline_example_plots.png")
    
    return {
        'ore_pipeline': ore_pipeline,
        'flow_data': {
            'flow_rates': flow_rates,
            'velocities': velocities,
            'pressure_drops': pressure_drops,
            'outlet_concentrations': outlet_concentrations
        },
        'particle_data': {
            'sizes': particle_sizes,
            'critical_velocities': critical_vels
        }
    }

def create_slurry_plots(flow_rates, velocities, pressure_drops, outlet_concentrations,
                       particle_sizes, critical_vels, pipeline):
    """Create comprehensive SlurryPipeline visualization plots"""
    
    fig = plt.figure(figsize=(15, 10))
    
    # Plot 1: Flow Rate vs Velocity
    ax1 = plt.subplot(2, 3, 1)
    plt.plot(flow_rates, velocities, 'b-', marker='o', linewidth=2, markersize=6)
    plt.xlabel('Flow Rate (m³/s)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Flow Rate vs Velocity\n(60 cm Diameter Pipeline)')
    plt.grid(True, alpha=0.3)
    
    # Add critical velocity line
    critical_v = 1.5 * np.sqrt(2 * 9.81 * pipeline.particle_diameter * 
                              (pipeline.solid_density/pipeline.fluid_density - 1))
    plt.axhline(y=critical_v, color='red', linestyle='--', 
                label=f'Critical Velocity: {critical_v:.2f} m/s')
    plt.legend()
    
    # Plot 2: Flow Rate vs Pressure Drop
    ax2 = plt.subplot(2, 3, 2)
    plt.plot(flow_rates, np.array(pressure_drops)/1000, 'g-', marker='s', linewidth=2, markersize=6)
    plt.xlabel('Flow Rate (m³/s)')
    plt.ylabel('Pressure Drop (kPa)')
    plt.title('Flow Rate vs Pressure Drop\n(50 km Pipeline)')
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Flow Rate vs Outlet Concentration
    ax3 = plt.subplot(2, 3, 3)
    plt.plot(flow_rates, np.array(outlet_concentrations)*100, 'purple', marker='^', linewidth=2, markersize=6)
    plt.xlabel('Flow Rate (m³/s)')
    plt.ylabel('Outlet Solids Concentration (%)')
    plt.title('Settling Effect vs Flow Rate\n(Particle Transport)')
    plt.grid(True, alpha=0.3)
    
    # Plot 4: Particle Size vs Critical Velocity
    ax4 = plt.subplot(2, 3, 4)
    plt.plot(particle_sizes*1e6, critical_vels, 'orange', marker='d', linewidth=2, markersize=6)
    plt.xlabel('Particle Size (microns)')
    plt.ylabel('Critical Velocity (m/s)')
    plt.title('Particle Size Effect\n(Durand Equation)')
    plt.grid(True, alpha=0.3)
    
    # Plot 5: Pipeline Profile
    ax5 = plt.subplot(2, 3, 5)
    x_profile = np.linspace(0, pipeline.pipe_length/1000, 100)  # km
    # Simplified pressure profile (linear drop)
    p_profile = 800 - (400 * x_profile / (pipeline.pipe_length/1000))  # kPa
    
    plt.plot(x_profile, p_profile, 'darkblue', linewidth=3)
    plt.fill_between(x_profile, 0, p_profile, alpha=0.3, color='lightblue')
    plt.xlabel('Distance (km)')
    plt.ylabel('Pressure (kPa)')
    plt.title('Pipeline Pressure Profile\n(Mining Ore Transport)')
    plt.grid(True, alpha=0.3)
    
    # Plot 6: Operating Map
    ax6 = plt.subplot(2, 3, 6)
    
    # Create operating envelope
    flow_envelope = np.linspace(0.1, 1.2, 50)
    vel_envelope = flow_envelope / (np.pi * (pipeline.pipe_diameter/2)**2)
    
    # Safe operating region
    safe_region = vel_envelope >= critical_v
    
    plt.plot(flow_envelope, vel_envelope, 'b-', linewidth=2, label='Operating Line')
    plt.fill_between(flow_envelope, critical_v, vel_envelope, 
                    where=safe_region, alpha=0.3, color='green', label='Safe Operation')
    plt.fill_between(flow_envelope, 0, critical_v, alpha=0.3, color='red', label='Settling Risk')
    
    plt.axhline(y=critical_v, color='red', linestyle='--', linewidth=2)
    plt.xlabel('Flow Rate (m³/s)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Operating Envelope\n(Safe vs Risk Zones)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('SlurryPipeline_example_plots.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()
