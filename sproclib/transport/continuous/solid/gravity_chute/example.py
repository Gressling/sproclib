"""
Example usage of GravityChute class.

This script demonstrates the GravityChute transport model with various
particle properties and chute configurations.
"""

import numpy as np
import matplotlib.pyplot as plt
from .gravity_chute import GravityChute

def main():
    print("=" * 60)
    print("GravityChute Transport Model Example")
    print("=" * 60)
    
    # Create gravity chute instance
    chute = GravityChute(
        chute_length=15.0,      # 15 m chute
        chute_width=0.8,        # 0.8 m wide
        chute_angle=0.524,      # 30 degrees
        surface_roughness=0.3,  # Moderate friction
        particle_density=2200.0, # Sand density
        particle_diameter=3e-3,  # 3 mm particles
        air_resistance=0.02,
        name="SandChute"
    )
    
    print("\nGravity Chute Parameters:")
    print(f"Length: {chute.chute_length} m")
    print(f"Width: {chute.chute_width} m")
    print(f"Angle: {chute.chute_angle:.3f} rad ({np.degrees(chute.chute_angle):.1f}°)")
    print(f"Surface roughness: {chute.surface_roughness}")
    print(f"Particle density: {chute.particle_density} kg/m³")
    print(f"Particle diameter: {chute.particle_diameter*1000:.1f} mm")
    
    # Display model description
    description = chute.describe()
    print(f"\nModel: {description['class_name']}")
    print(f"Algorithm: {description['algorithm']}")
    
    # Test different operating conditions
    print("\n" + "=" * 50)
    print("Steady-State Performance Analysis")
    print("=" * 50)
    
    # Operating conditions: [feed_rate, particle_size_factor, chute_loading]
    test_conditions = [
        ([5.0, 1.0, 0.2], "Normal operation"),
        ([8.0, 1.0, 0.4], "Higher loading"),
        ([3.0, 0.5, 0.3], "Fine particles"),
        ([6.0, 2.0, 0.3], "Coarse particles"),
        ([10.0, 1.0, 0.8], "High capacity"),
        ([2.0, 1.0, 0.1], "Low loading"),
    ]
    
    results = []
    for conditions, description in test_conditions:
        u = np.array(conditions)
        result = chute.steady_state(u)
        results.append((conditions, result, description))
        
        print(f"\n{description}:")
        print(f"  Input: Feed={u[0]:.1f} kg/s, Size factor={u[1]:.1f}, Loading={u[2]:.1f}")
        print(f"  Output: Velocity={result[0]:.2f} m/s, Flow={result[1]:.2f} kg/s")
        if u[0] > 0:
            print(f"  Efficiency: {result[1]/u[0]*100:.1f}%")
    
    # Chute angle analysis
    print("\n" + "=" * 50)
    print("Chute Angle Analysis")
    print("=" * 50)
    
    angles_deg = np.linspace(10, 50, 15)
    angles_rad = np.radians(angles_deg)
    velocities = []
    flow_rates = []
    
    for angle in angles_rad:
        test_chute = GravityChute(
            chute_length=15.0,
            chute_width=0.8,
            chute_angle=angle,
            surface_roughness=0.3,
            particle_density=2200.0,
            particle_diameter=3e-3
        )
        
        u = np.array([6.0, 1.0, 0.3])
        result = test_chute.steady_state(u)
        velocities.append(result[0])
        flow_rates.append(result[1])
    
    # Find critical angle (minimum angle for flow)
    critical_idx = np.where(np.array(velocities) > 0.1)[0]
    if len(critical_idx) > 0:
        critical_angle = angles_deg[critical_idx[0]]
        print(f"Critical angle for flow: ~{critical_angle:.1f}°")
    
    optimal_idx = np.argmax(velocities)
    optimal_angle = angles_deg[optimal_idx]
    print(f"Angle for maximum velocity: {optimal_angle:.1f}°")
    print(f"Maximum velocity: {velocities[optimal_idx]:.2f} m/s")
    
    # Particle size effect analysis
    print("\n" + "=" * 50)
    print("Particle Size Effect Analysis")
    print("=" * 50)
    
    size_factors = np.linspace(0.2, 3.0, 15)
    size_velocities = []
    size_flows = []
    
    for size_factor in size_factors:
        u = np.array([6.0, size_factor, 0.3])
        result = chute.steady_state(u)
        size_velocities.append(result[0])
        size_flows.append(result[1])
    
    print("Particle Size Effects:")
    for i, factor in enumerate([0.5, 1.0, 2.0]):
        idx = np.argmin(np.abs(size_factors - factor))
        effective_size = chute.particle_diameter * factor * 1000
        print(f"  Size factor {factor:.1f} ({effective_size:.1f} mm): "
              f"Velocity={size_velocities[idx]:.2f} m/s, Flow={size_flows[idx]:.2f} kg/s")
    
    # Surface roughness effect
    print("\n" + "=" * 50)
    print("Surface Roughness Effect Analysis")
    print("=" * 50)
    
    roughness_values = np.linspace(0.1, 0.8, 10)
    roughness_velocities = []
    roughness_flows = []
    
    for roughness in roughness_values:
        test_chute = GravityChute(
            chute_length=15.0,
            chute_width=0.8,
            chute_angle=0.524,
            surface_roughness=roughness,
            particle_density=2200.0,
            particle_diameter=3e-3
        )
        
        u = np.array([6.0, 1.0, 0.3])
        result = test_chute.steady_state(u)
        roughness_velocities.append(result[0])
        roughness_flows.append(result[1])
    
    print("Surface Roughness Effects:")
    surface_types = [(0.1, "Very smooth"), (0.3, "Moderate"), (0.6, "Rough"), (0.8, "Very rough")]
    for roughness, surface_type in surface_types:
        idx = np.argmin(np.abs(roughness_values - roughness))
        print(f"  {surface_type:12s} (μ={roughness:.1f}): "
              f"Velocity={roughness_velocities[idx]:.2f} m/s")
    
    # Dynamic response analysis
    print("\n" + "=" * 50)
    print("Dynamic Response Analysis")
    print("=" * 50)
    
    # Simulate step change in feed rate
    dt = 0.2  # time step (s)
    t_final = 120.0  # simulation time (s)
    time = np.arange(0, t_final, dt)
    
    # Initial conditions: [velocity, flow_rate]
    x = np.array([2.0, 3.0])
    
    # Step change at t=30s: from 4 to 8 kg/s feed rate
    feed_rates = np.where(time < 30, 4.0, 8.0)
    
    velocity_history = []
    flow_history = []
    
    for i, t in enumerate(time):
        u = np.array([feed_rates[i], 1.0, 0.3])
        
        # Store current state
        velocity_history.append(x[0])
        flow_history.append(x[1])
        
        # Calculate derivatives
        dxdt = chute.dynamics(t, x, u)
        
        # Euler integration
        x = x + dxdt * dt
    
    print(f"Initial velocity: {velocity_history[0]:.2f} m/s")
    print(f"Final velocity: {velocity_history[-1]:.2f} m/s")
    print(f"Transport time: {chute.chute_length/velocity_history[-1]:.1f} s")
    
    # Material comparison
    print("\n" + "=" * 50)
    print("Material Comparison")
    print("=" * 50)
    
    materials = [
        (1000, 1e-3, "Fine sand"),
        (1500, 2e-3, "Coarse sand"),
        (2200, 3e-3, "Gravel"),
        (2700, 5e-3, "Crushed stone"),
        (7800, 8e-3, "Steel shot")
    ]
    
    material_results = []
    for density, diameter, name in materials:
        test_chute = GravityChute(
            chute_length=15.0,
            chute_width=0.8,
            chute_angle=0.524,
            surface_roughness=0.3,
            particle_density=density,
            particle_diameter=diameter
        )
        
        u = np.array([6.0, 1.0, 0.3])
        result = test_chute.steady_state(u)
        material_results.append((name, density, diameter*1000, result))
        
        print(f"{name:15s}: ρ={density:4d} kg/m³, d={diameter*1000:4.1f} mm, "
              f"v={result[0]:5.2f} m/s, Q={result[1]:5.2f} kg/s")
    
    # Loading effect analysis
    print("\n" + "=" * 50)
    print("Loading Effect Analysis")
    print("=" * 50)
    
    loadings = np.linspace(0.1, 0.9, 9)
    loading_velocities = []
    loading_flows = []
    
    for loading in loadings:
        u = np.array([10.0, 1.0, loading])  # High feed rate
        result = chute.steady_state(u)
        loading_velocities.append(result[0])
        loading_flows.append(result[1])
    
    print("Loading Effects (at 10 kg/s feed rate):")
    for i, loading in enumerate([0.2, 0.4, 0.6, 0.8]):
        idx = np.argmin(np.abs(loadings - loading))
        print(f"  Loading {loading*100:2.0f}%: "
              f"Velocity={loading_velocities[idx]:.2f} m/s, "
              f"Flow={loading_flows[idx]:.2f} kg/s")
    
    # Create visualizations
    create_plots(chute, angles_deg, velocities, flow_rates,
                size_factors, size_velocities, roughness_values, 
                roughness_velocities, time, velocity_history, 
                flow_history, material_results, loadings, 
                loading_velocities, loading_flows)
    
    print("\n" + "=" * 60)
    print("Analysis Complete - Check generated plots")
    print("=" * 60)

def create_plots(chute, angles_deg, velocities, flow_rates, size_factors, 
                size_velocities, roughness_values, roughness_velocities,
                time, velocity_history, flow_history, material_results,
                loadings, loading_velocities, loading_flows):
    """Create visualization plots."""
    
    # Plot 1: Parameter effects
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 3, 1)
    plt.plot(angles_deg, velocities, 'b-', linewidth=2, label='Particle Velocity')
    plt.xlabel('Chute Angle (degrees)')
    plt.ylabel('Particle Velocity (m/s)')
    plt.title('Velocity vs Chute Angle')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 3, 2)
    plt.plot(size_factors, size_velocities, 'g-', linewidth=2, label='Velocity')
    plt.xlabel('Particle Size Factor')
    plt.ylabel('Particle Velocity (m/s)')
    plt.title('Velocity vs Particle Size')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 3, 3)
    plt.plot(roughness_values, roughness_velocities, 'r-', linewidth=2, label='Velocity')
    plt.xlabel('Surface Roughness')
    plt.ylabel('Particle Velocity (m/s)')
    plt.title('Velocity vs Surface Roughness')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 3, 4)
    plt.plot(loadings*100, loading_velocities, 'purple', linewidth=2, label='Velocity')
    plt.xlabel('Chute Loading (%)')
    plt.ylabel('Particle Velocity (m/s)')
    plt.title('Velocity vs Loading')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 3, 5)
    plt.plot(loadings*100, loading_flows, 'orange', linewidth=2, label='Flow Rate')
    plt.xlabel('Chute Loading (%)')
    plt.ylabel('Flow Rate (kg/s)')
    plt.title('Flow Rate vs Loading')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 3, 6)
    # Material comparison
    densities = [result[1] for result in material_results]
    velocities_mat = [result[3][0] for result in material_results]
    plt.scatter(densities, velocities_mat, c='red', s=60, alpha=0.7)
    plt.xlabel('Material Density (kg/m³)')
    plt.ylabel('Particle Velocity (m/s)')
    plt.title('Material Density Effect')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('GravityChute_example_plots.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 2: Dynamic response and detailed analysis
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.plot(time, velocity_history, 'b-', linewidth=2, label='Particle Velocity')
    plt.axvline(x=30, color='r', linestyle='--', alpha=0.7, label='Step Change')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Dynamic Response - Velocity')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 2, 2)
    plt.plot(time, flow_history, 'g-', linewidth=2, label='Flow Rate')
    plt.axvline(x=30, color='r', linestyle='--', alpha=0.7, label='Step Change')
    plt.xlabel('Time (s)')
    plt.ylabel('Flow Rate (kg/s)')
    plt.title('Dynamic Response - Flow Rate')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 2, 3)
    # Force balance visualization
    angles_force = np.linspace(0, 60, 100)
    g = 9.81
    mu = chute.surface_roughness
    
    gravity_component = g * np.sin(np.radians(angles_force))
    friction_component = mu * g * np.cos(np.radians(angles_force))
    net_force = gravity_component - friction_component
    
    plt.plot(angles_force, gravity_component, 'b-', label='Gravity Component')
    plt.plot(angles_force, friction_component, 'r-', label='Friction Force')
    plt.plot(angles_force, net_force, 'g-', linewidth=2, label='Net Force')
    plt.axhline(y=0, color='k', linestyle=':', alpha=0.5)
    plt.axvline(x=np.degrees(chute.chute_angle), color='purple', 
                linestyle='--', alpha=0.7, label='Operating Angle')
    plt.xlabel('Chute Angle (degrees)')
    plt.ylabel('Force per unit mass (m/s²)')
    plt.title('Force Balance Analysis')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 2, 4)
    # Flow regime map
    loading_grid = np.linspace(0.1, 0.9, 10)
    angle_grid = np.linspace(15, 45, 10)
    
    flow_map = np.zeros((len(angle_grid), len(loading_grid)))
    
    for i, angle in enumerate(angle_grid):
        for j, loading in enumerate(loading_grid):
            test_chute = GravityChute(
                chute_angle=np.radians(angle),
                surface_roughness=0.3,
                particle_density=2200.0,
                particle_diameter=3e-3
            )
            u = np.array([6.0, 1.0, loading])
            result = test_chute.steady_state(u)
            flow_map[i, j] = result[0]  # velocity
    
    im = plt.imshow(flow_map, extent=[loading_grid[0]*100, loading_grid[-1]*100,
                                     angle_grid[0], angle_grid[-1]], 
                   aspect='auto', origin='lower', cmap='viridis')
    plt.colorbar(im, label='Velocity (m/s)')
    plt.xlabel('Chute Loading (%)')
    plt.ylabel('Chute Angle (degrees)')
    plt.title('Flow Velocity Map')
    
    plt.tight_layout()
    plt.savefig('GravityChute_detailed_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()
