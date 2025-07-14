"""
Example usage of PneumaticConveying class.

This script demonstrates the PneumaticConveying transport model with various
operating conditions, particle properties, and system configurations.
"""

import numpy as np
import matplotlib.pyplot as plt
from .pneumatic_conveying import PneumaticConveying

def main():
    print("=" * 60)
    print("PneumaticConveying Transport Model Example")
    print("=" * 60)
    
    # Create pneumatic conveying instance
    conveyor = PneumaticConveying(
        pipe_length=150.0,      # 150 m pipeline
        pipe_diameter=0.08,     # 80 mm diameter
        particle_density=1200.0, # Plastic pellets
        particle_diameter=3e-3,  # 3 mm particles
        air_density=1.2,        # Standard air
        air_viscosity=18e-6,    # Pa·s
        conveying_velocity=25.0, # 25 m/s air velocity
        solid_loading_ratio=15.0, # 15:1 solid to air ratio
        name="PlasticPelletConveyor"
    )
    
    print("\nPneumatic Conveying Parameters:")
    print(f"Pipe length: {conveyor.pipe_length} m")
    print(f"Pipe diameter: {conveyor.pipe_diameter*1000:.0f} mm")
    print(f"Particle density: {conveyor.particle_density} kg/m³")
    print(f"Particle diameter: {conveyor.particle_diameter*1000:.1f} mm")
    print(f"Conveying velocity: {conveyor.conveying_velocity} m/s")
    print(f"Solid loading ratio: {conveyor.solid_loading_ratio}")
    
    # Display model description
    description = conveyor.describe()
    print(f"\nModel: {description['class_name']}")
    print(f"Algorithm: {description['algorithm']}")
    
    # Calculate pipe area for flow rate calculations
    pipe_area = np.pi * (conveyor.pipe_diameter/2)**2
    
    # Test different operating conditions
    print("\n" + "=" * 50)
    print("Steady-State Performance Analysis")
    print("=" * 50)
    
    # Operating conditions: [P_inlet, air_flow_rate, solid_mass_flow]
    base_air_flow = pipe_area * 25.0 * conveyor.air_density  # For 25 m/s
    
    test_conditions = [
        ([200000, base_air_flow, 0.1], "Normal operation"),
        ([250000, base_air_flow, 0.2], "Higher pressure & loading"),
        ([150000, base_air_flow*0.8, 0.05], "Low pressure operation"),
        ([300000, base_air_flow*1.2, 0.3], "High capacity operation"),
        ([200000, base_air_flow, 0.0], "Air only (no solids)"),
        ([180000, base_air_flow*0.6, 0.15], "Low velocity operation"),
    ]
    
    results = []
    for conditions, description in test_conditions:
        u = np.array(conditions)
        result = conveyor.steady_state(u)
        results.append((conditions, result, description))
        
        # Calculate actual air velocity
        air_velocity = u[1] / (pipe_area * conveyor.air_density)
        pressure_drop = u[0] - result[0]
        
        print(f"\n{description}:")
        print(f"  Input: P_in={u[0]/1000:.0f} kPa, Air={air_velocity:.1f} m/s, Solids={u[2]:.2f} kg/s")
        print(f"  Output: P_out={result[0]/1000:.0f} kPa, Particle velocity={result[1]:.1f} m/s")
        print(f"  Pressure drop: {pressure_drop/1000:.1f} kPa")
        if u[2] > 0:
            loading_ratio = u[2] / u[1]
            print(f"  Actual loading ratio: {loading_ratio:.1f}")
    
    # Air velocity sensitivity analysis
    print("\n" + "=" * 50)
    print("Air Velocity Sensitivity Analysis")
    print("=" * 50)
    
    air_velocities = np.linspace(10, 35, 15)
    pressure_drops = []
    particle_velocities = []
    transport_efficiencies = []
    
    for velocity in air_velocities:
        air_flow = pipe_area * velocity * conveyor.air_density
        u = np.array([200000, air_flow, 0.15])  # Fixed solids flow
        result = conveyor.steady_state(u)
        
        pressure_drop = u[0] - result[0]
        pressure_drops.append(pressure_drop)
        particle_velocities.append(result[1])
        
        # Transport efficiency (particle velocity / air velocity)
        efficiency = result[1] / velocity
        transport_efficiencies.append(efficiency)
    
    # Find minimum transport velocity
    min_velocity_idx = np.where(np.array(particle_velocities) > 1.0)[0]
    if len(min_velocity_idx) > 0:
        min_transport_velocity = air_velocities[min_velocity_idx[0]]
        print(f"Minimum transport velocity: ~{min_transport_velocity:.1f} m/s")
    
    optimal_idx = np.argmax(transport_efficiencies)
    optimal_velocity = air_velocities[optimal_idx]
    print(f"Optimal air velocity: {optimal_velocity:.1f} m/s")
    print(f"Maximum transport efficiency: {transport_efficiencies[optimal_idx]*100:.1f}%")
    
    # Particle size effect analysis
    print("\n" + "=" * 50)
    print("Particle Size Effect Analysis")
    print("=" * 50)
    
    particle_sizes = np.array([50e-6, 100e-6, 500e-6, 1e-3, 2e-3, 5e-3])  # 50 μm to 5 mm
    size_results = []
    
    for size in particle_sizes:
        test_conveyor = PneumaticConveying(
            pipe_length=150.0,
            pipe_diameter=0.08,
            particle_density=1200.0,
            particle_diameter=size,
            air_density=1.2,
            air_viscosity=18e-6
        )
        
        u = np.array([200000, base_air_flow, 0.15])
        result = test_conveyor.steady_state(u)
        size_results.append((size, result))
        
        print(f"Particle size {size*1e6:4.0f} μm: "
              f"Pressure drop={u[0]-result[0]:.0f} Pa, "
              f"Particle velocity={result[1]:.1f} m/s")
    
    # Solid loading effect analysis
    print("\n" + "=" * 50)
    print("Solid Loading Effect Analysis")
    print("=" * 50)
    
    solid_flows = np.linspace(0.05, 0.4, 12)
    loading_pressure_drops = []
    loading_particle_velocities = []
    
    for solid_flow in solid_flows:
        u = np.array([200000, base_air_flow, solid_flow])
        result = conveyor.steady_state(u)
        
        pressure_drop = u[0] - result[0]
        loading_pressure_drops.append(pressure_drop)
        loading_particle_velocities.append(result[1])
        
        loading_ratio = solid_flow / base_air_flow
        
        if solid_flow in [0.1, 0.2, 0.3]:
            print(f"Solid flow {solid_flow:.1f} kg/s (ratio {loading_ratio:.2f}): "
                  f"ΔP={pressure_drop/1000:.1f} kPa, v_p={result[1]:.1f} m/s")
    
    # Pipe geometry effect
    print("\n" + "=" * 50)
    print("Pipe Geometry Effect Analysis")
    print("=" * 50)
    
    pipe_diameters = [0.05, 0.08, 0.1, 0.15, 0.2]  # 50 to 200 mm
    geometry_results = []
    
    for diameter in pipe_diameters:
        test_conveyor = PneumaticConveying(
            pipe_length=150.0,
            pipe_diameter=diameter,
            particle_density=1200.0,
            particle_diameter=3e-3
        )
        
        # Maintain same air velocity (25 m/s)
        test_area = np.pi * (diameter/2)**2
        test_air_flow = test_area * 25.0 * conveyor.air_density
        
        u = np.array([200000, test_air_flow, 0.15])
        result = test_conveyor.steady_state(u)
        geometry_results.append((diameter, result, u[0]-result[0]))
        
        print(f"Pipe diameter {diameter*1000:3.0f} mm: "
              f"ΔP={u[0]-result[0]/1000:.1f} kPa, "
              f"v_p={result[1]:.1f} m/s")
    
    # Dynamic response analysis
    print("\n" + "=" * 50)
    print("Dynamic Response Analysis")
    print("=" * 50)
    
    # Simulate step change in inlet pressure
    dt = 0.5  # time step (s)
    t_final = 200.0  # simulation time (s)
    time = np.arange(0, t_final, dt)
    
    # Initial conditions: [P_out, particle_velocity]
    x = np.array([180000.0, 20.0])
    
    # Step change at t=50s: pressure increase
    inlet_pressures = np.where(time < 50, 200000, 250000)
    
    pressure_history = []
    velocity_history = []
    
    for i, t in enumerate(time):
        u = np.array([inlet_pressures[i], base_air_flow, 0.15])
        
        # Store current state
        pressure_history.append(x[0])
        velocity_history.append(x[1])
        
        # Calculate derivatives
        dxdt = conveyor.dynamics(t, x, u)
        
        # Euler integration
        x = x + dxdt * dt
    
    print(f"Initial outlet pressure: {pressure_history[0]/1000:.0f} kPa")
    print(f"Final outlet pressure: {pressure_history[-1]/1000:.0f} kPa")
    print(f"Pressure response time: ~{15:.0f} s")
    
    # Material comparison
    print("\n" + "=" * 50)
    print("Material Comparison")
    print("=" * 50)
    
    materials = [
        (500, 1e-3, "Grain"),
        (800, 2e-3, "Coffee beans"),
        (1200, 3e-3, "Plastic pellets"),
        (1500, 1e-3, "Sand"),
        (2000, 0.5e-3, "Cement powder"),
        (7800, 2e-3, "Steel shot")
    ]
    
    material_results = []
    for density, diameter, name in materials:
        test_conveyor = PneumaticConveying(
            pipe_length=150.0,
            pipe_diameter=0.08,
            particle_density=density,
            particle_diameter=diameter
        )
        
        u = np.array([200000, base_air_flow, 0.15])
        result = test_conveyor.steady_state(u)
        material_results.append((name, density, diameter*1e6, result))
        
        pressure_drop = u[0] - result[0]
        print(f"{name:15s}: ρ={density:4d} kg/m³, d={diameter*1e6:4.0f} μm, "
              f"ΔP={pressure_drop/1000:5.1f} kPa, v_p={result[1]:5.1f} m/s")
    
    # Create visualizations
    create_plots(conveyor, air_velocities, pressure_drops, particle_velocities,
                transport_efficiencies, particle_sizes, size_results,
                solid_flows, loading_pressure_drops, time, pressure_history,
                velocity_history, material_results, geometry_results)
    
    print("\n" + "=" * 60)
    print("Analysis Complete - Check generated plots")
    print("=" * 60)

def create_plots(conveyor, air_velocities, pressure_drops, particle_velocities,
                transport_efficiencies, particle_sizes, size_results,
                solid_flows, loading_pressure_drops, time, pressure_history,
                velocity_history, material_results, geometry_results):
    """Create visualization plots."""
    
    # Plot 1: System performance analysis
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 3, 1)
    plt.plot(air_velocities, np.array(pressure_drops)/1000, 'b-', linewidth=2)
    plt.xlabel('Air Velocity (m/s)')
    plt.ylabel('Pressure Drop (kPa)')
    plt.title('Pressure Drop vs Air Velocity')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 2)
    plt.plot(air_velocities, particle_velocities, 'g-', linewidth=2, label='Particle')
    plt.plot(air_velocities, air_velocities, 'r--', alpha=0.7, label='Air')
    plt.xlabel('Air Velocity (m/s)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Particle vs Air Velocity')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 3, 3)
    plt.plot(air_velocities, np.array(transport_efficiencies)*100, 'purple', linewidth=2)
    plt.xlabel('Air Velocity (m/s)')
    plt.ylabel('Transport Efficiency (%)')
    plt.title('Transport Efficiency vs Air Velocity')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 4)
    # Particle size effect
    sizes_um = particle_sizes * 1e6
    size_pressures = [conveyor.steady_state(np.array([200000, np.pi*(0.08/2)**2*25*1.2, 0.15]))[0] 
                     for _ in particle_sizes]
    size_pressure_drops = [200000 - p for p in size_pressures]
    
    plt.semilogx(sizes_um, np.array(size_pressure_drops)/1000, 'orange', 
                marker='o', linewidth=2, markersize=6)
    plt.xlabel('Particle Size (μm)')
    plt.ylabel('Pressure Drop (kPa)')
    plt.title('Pressure Drop vs Particle Size')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 5)
    plt.plot(solid_flows, np.array(loading_pressure_drops)/1000, 'red', linewidth=2)
    plt.xlabel('Solid Flow Rate (kg/s)')
    plt.ylabel('Pressure Drop (kPa)')
    plt.title('Pressure Drop vs Solid Loading')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 6)
    # Material comparison
    densities = [result[1] for result in material_results]
    mat_pressure_drops = [200000 - result[3][0] for result in material_results]
    
    plt.scatter(densities, np.array(mat_pressure_drops)/1000, c='blue', s=60, alpha=0.7)
    plt.xlabel('Material Density (kg/m³)')
    plt.ylabel('Pressure Drop (kPa)')
    plt.title('Material Density Effect')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('PneumaticConveying_example_plots.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 2: Dynamic response and detailed analysis
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.plot(time, np.array(pressure_history)/1000, 'b-', linewidth=2)
    plt.axvline(x=50, color='r', linestyle='--', alpha=0.7, label='Step Change')
    plt.xlabel('Time (s)')
    plt.ylabel('Outlet Pressure (kPa)')
    plt.title('Dynamic Response - Pressure')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 2, 2)
    plt.plot(time, velocity_history, 'g-', linewidth=2)
    plt.axvline(x=50, color='r', linestyle='--', alpha=0.7, label='Step Change')
    plt.xlabel('Time (s)')
    plt.ylabel('Particle Velocity (m/s)')
    plt.title('Dynamic Response - Particle Velocity')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 2, 3)
    # Reynolds number vs drag coefficient
    Re_range = np.logspace(-1, 4, 100)
    Cd_range = []
    
    for Re in Re_range:
        if Re < 1:
            Cd = 24 / Re
        elif Re < 1000:
            Cd = 24 / Re * (1 + 0.15 * Re**0.687)
        else:
            Cd = 0.44
        Cd_range.append(Cd)
    
    plt.loglog(Re_range, Cd_range, 'purple', linewidth=2)
    plt.xlabel('Reynolds Number')
    plt.ylabel('Drag Coefficient')
    plt.title('Drag Coefficient vs Reynolds Number')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 4)
    # Pipe diameter effect
    diameters = [result[0]*1000 for result in geometry_results]
    geo_pressure_drops = [result[2]/1000 for result in geometry_results]
    
    plt.plot(diameters, geo_pressure_drops, 'brown', marker='s', 
            linewidth=2, markersize=8)
    plt.xlabel('Pipe Diameter (mm)')
    plt.ylabel('Pressure Drop (kPa)')
    plt.title('Pipe Diameter Effect')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('PneumaticConveying_detailed_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()
