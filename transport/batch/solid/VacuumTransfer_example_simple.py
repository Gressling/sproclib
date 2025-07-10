"""
Simple example runner for VacuumTransfer class
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the project root to the path
project_root = os.path.join(os.path.dirname(__file__), '../../..')
sys.path.insert(0, project_root)

# Import ProcessModel directly
from unit.base.ProcessModel import ProcessModel

# Now import our class with corrected import
exec(open(os.path.join(os.path.dirname(__file__), 'VacuumTransfer.py')).read())

def main():
    """Main function demonstrating VacuumTransfer operations."""
    
    print("=== VacuumTransfer Example ===")
    print()
    
    # Create VacuumTransfer instances for different scenarios
    print("1. Creating VacuumTransfer instances:")
    print("-" * 38)
    
    # Pharmaceutical fine powder transfer
    pharma_vacuum = VacuumTransfer(
        vacuum_pump_capacity=80.0,      # 80 m³/h pump
        transfer_line_diameter=0.04,    # 40 mm diameter line
        transfer_line_length=12.0,      # 12 m transfer line
        powder_density=500.0,           # Light pharmaceutical powder
        particle_size=50e-6,            # 50 micron particles
        cyclone_efficiency=0.95,        # High efficiency cyclone
        vacuum_level_max=-75000.0,      # -75 kPa max vacuum
        filter_resistance=1500.0,       # Higher filter resistance
        name="PharmaVacuumTransfer"
    )
    
    # Food ingredient transfer
    food_vacuum = VacuumTransfer(
        vacuum_pump_capacity=200.0,     # 200 m³/h pump
        transfer_line_diameter=0.08,    # 80 mm diameter line
        transfer_line_length=25.0,      # 25 m transfer line
        powder_density=700.0,           # Food powder density
        particle_size=150e-6,           # 150 micron particles
        cyclone_efficiency=0.98,        # Very high efficiency cyclone
        vacuum_level_max=-90000.0,      # -90 kPa max vacuum
        filter_resistance=800.0,        # Lower filter resistance
        name="FoodVacuumTransfer"
    )
    
    # Chemical powder transfer
    chemical_vacuum = VacuumTransfer(
        vacuum_pump_capacity=150.0,     # 150 m³/h pump
        transfer_line_diameter=0.06,    # 60 mm diameter line
        transfer_line_length=8.0,       # 8 m transfer line
        powder_density=900.0,           # Dense chemical powder
        particle_size=100e-6,           # 100 micron particles
        cyclone_efficiency=0.92,        # Good efficiency cyclone
        vacuum_level_max=-85000.0,      # -85 kPa max vacuum
        filter_resistance=1200.0,       # Moderate filter resistance
        name="ChemicalVacuumTransfer"
    )
    
    print(f"Pharmaceutical vacuum: {pharma_vacuum.name}")
    print(f"  Pump capacity: {pharma_vacuum.vacuum_pump_capacity} m³/h")
    print(f"  Particle size: {pharma_vacuum.particle_size*1e6:.0f} μm")
    print()
    
    print(f"Food vacuum: {food_vacuum.name}")
    print(f"  Pump capacity: {food_vacuum.vacuum_pump_capacity} m³/h")
    print(f"  Particle size: {food_vacuum.particle_size*1e6:.0f} μm")
    print()
    
    print(f"Chemical vacuum: {chemical_vacuum.name}")
    print(f"  Pump capacity: {chemical_vacuum.vacuum_pump_capacity} m³/h")
    print(f"  Particle size: {chemical_vacuum.particle_size*1e6:.0f} μm")
    print()
    
    # 2. Steady-state analysis
    print("2. Steady-state analysis:")
    print("-" * 25)
    
    # Test different operating conditions
    conditions = [
        {"name": "High source, low vacuum", "powder": 0.8, "vacuum": -30000.0, "filter": 0.1},
        {"name": "Medium source, medium vacuum", "powder": 0.5, "vacuum": -50000.0, "filter": 0.3},
        {"name": "Low source, high vacuum", "powder": 0.2, "vacuum": -70000.0, "filter": 0.5},
        {"name": "Full source, max vacuum", "powder": 1.0, "vacuum": -80000.0, "filter": 0.8}
    ]
    
    print("Pharmaceutical vacuum results:")
    for condition in conditions:
        u = np.array([condition["powder"], condition["vacuum"], condition["filter"]])
        result = pharma_vacuum.steady_state(u)
        powder_rate, vacuum_level = result
        
        print(f"  {condition['name']}:")
        print(f"    Powder rate: {powder_rate:.2f} kg/s")
        print(f"    Vacuum level: {vacuum_level/1000:.1f} kPa")
        print()
    
    # 3. Dynamic simulation
    print("3. Dynamic simulation:")
    print("-" * 20)
    
    # Simulate vacuum system startup and operation
    time_span = np.linspace(0, 120, 241)  # 2 minutes
    dt = time_span[1] - time_span[0]
    
    # Initial conditions
    x = np.array([0.0, 0.0])  # [powder_rate=0, vacuum_level=0]
    u = np.array([0.7, -60000.0, 0.2])  # [powder_level, vacuum_setpoint, filter_loading]
    
    # Storage for results
    powder_rates = []
    vacuum_levels = []
    times = []
    
    print("Simulating vacuum system startup with food_vacuum:")
    print(f"Initial conditions: rate=0 kg/s, vacuum=0 Pa")
    print(f"Setpoint: {u[1]/1000:.0f} kPa, powder level: {u[0]*100:.0f}%")
    print()
    
    # Euler integration
    for t in time_span:
        # Store current state
        powder_rates.append(x[0])
        vacuum_levels.append(x[1]/1000)  # Convert to kPa
        times.append(t)
        
        # Calculate derivatives
        dx_dt = food_vacuum.dynamics(t, x, u)
        # Update state
        x = x + dx_dt * dt
    
    # Convert to numpy arrays
    powder_rates = np.array(powder_rates)
    vacuum_levels = np.array(vacuum_levels)
    times = np.array(times)
    
    # Print key results
    print("Dynamic simulation results:")
    print(f"  Final powder rate: {powder_rates[-1]:.2f} kg/s")
    print(f"  Final vacuum level: {vacuum_levels[-1]:.1f} kPa")
    
    # Find steady-state time (95% of final value)
    final_rate = powder_rates[-1]
    if final_rate > 0:
        steady_indices = np.where(powder_rates > 0.95 * final_rate)[0]
        if len(steady_indices) > 0:
            steady_time = times[steady_indices[0]]
            print(f"  Steady-state time: ~{steady_time:.0f} s")
    print()
    
    # 4. Particle size sensitivity analysis
    print("4. Particle size sensitivity analysis:")
    print("-" * 38)
    
    particle_sizes = np.array([20, 50, 100, 200, 300, 400]) * 1e-6  # microns
    transfer_rates = []
    
    for particle_size in particle_sizes:
        # Temporarily modify particle size
        original_size = chemical_vacuum.particle_size
        chemical_vacuum.particle_size = particle_size
        
        u_test = np.array([0.6, -70000.0, 0.3])
        result = chemical_vacuum.steady_state(u_test)
        transfer_rates.append(result[0])
        
        # Restore original size
        chemical_vacuum.particle_size = original_size
    
    transfer_rates = np.array(transfer_rates)
    
    print("Chemical vacuum particle size sensitivity (60% powder, -70 kPa):")
    for i, (size, rate) in enumerate(zip(particle_sizes*1e6, transfer_rates)):
        print(f"  {size:.0f} μm: {rate:.2f} kg/s")
    
    print()
    
    # 5. Filter loading effects
    print("5. Filter loading effects:")
    print("-" * 24)
    
    filter_loadings = np.linspace(0.0, 1.0, 11)
    vacuum_performance = []
    
    for loading in filter_loadings:
        u_test = np.array([0.8, -80000.0, loading])
        result = pharma_vacuum.steady_state(u_test)
        vacuum_performance.append(abs(result[1]))
    
    vacuum_performance = np.array(vacuum_performance)
    
    print("Pharma vacuum filter loading effects (80% powder, -80 kPa setpoint):")
    for i, (loading, vacuum) in enumerate(zip(filter_loadings, vacuum_performance)):
        print(f"  {loading:.1f} loading: {vacuum/1000:.1f} kPa actual")
    
    print()
    
    # 6. Model introspection
    print("6. Model introspection:")
    print("-" * 20)
    
    metadata = pharma_vacuum.describe()
    print(f"Model type: {metadata['model_type']}")
    print(f"Description: {metadata['description']}")
    print()
    print("Key parameters:")
    for param, info in list(metadata['parameters'].items())[:5]:  # First 5 parameters
        print(f"  {param}: {info['value']} {info['unit']} - {info['description']}")
    print()
    
    print("Key equations:")
    for eq_name, equation in metadata['equations'].items():
        print(f"  {eq_name}: {equation}")
    print()
    
    # 7. Comparative analysis
    print("7. Comparative analysis:")
    print("-" * 23)
    
    # Compare all three systems under same conditions
    test_condition = np.array([0.7, -60000.0, 0.3])
    
    systems = [
        ("Pharmaceutical", pharma_vacuum),
        ("Food", food_vacuum),
        ("Chemical", chemical_vacuum)
    ]
    
    print("System comparison (70% powder, -60 kPa, 30% filter loading):")
    for name, system in systems:
        result = system.steady_state(test_condition)
        print(f"  {name:15s}: {result[0]:.3f} kg/s, {result[1]/1000:.1f} kPa")
    
    print()
    
    # 8. Create visualization plots
    print("8. Creating visualization plots...")
    create_plots(times, powder_rates, vacuum_levels, particle_sizes, transfer_rates, 
                filter_loadings, vacuum_performance, systems, test_condition)
    print("Plots saved as VacuumTransfer_example_plots.png and VacuumTransfer_detailed_analysis.png")
    print()
    
    print("=== Example completed successfully ===")


def create_plots(times, powder_rates, vacuum_levels, particle_sizes, transfer_rates,
                filter_loadings, vacuum_performance, systems, test_condition):
    """Create visualization plots for the VacuumTransfer example."""
    
    # Plot 1: Dynamic simulation results
    fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Powder transfer rate vs time
    ax1.plot(times, powder_rates, 'b-', linewidth=2, label='Powder Rate')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Powder Rate (kg/s)')
    ax1.set_title('VacuumTransfer Dynamic Response - Food System')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Vacuum level vs time
    ax2.plot(times, vacuum_levels, 'r-', linewidth=2, label='Vacuum Level')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Vacuum Level (kPa)')
    ax2.set_title('Vacuum Level Development')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('VacuumTransfer_example_plots.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 2: Detailed analysis
    fig2, ((ax3, ax4), (ax5, ax6)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Particle size sensitivity
    ax3.plot(particle_sizes*1e6, transfer_rates, 'go-', linewidth=2, markersize=6)
    ax3.set_xlabel('Particle Size (μm)')
    ax3.set_ylabel('Transfer Rate (kg/s)')
    ax3.set_title('Particle Size Effect on Transfer Rate')
    ax3.grid(True, alpha=0.3)
    
    # Filter loading effects
    ax4.plot(filter_loadings*100, vacuum_performance/1000, 'mo-', linewidth=2, markersize=4)
    ax4.set_xlabel('Filter Loading (%)')
    ax4.set_ylabel('Actual Vacuum (kPa)')
    ax4.set_title('Filter Loading Effect on Vacuum')
    ax4.grid(True, alpha=0.3)
    
    # System comparison
    system_names = [name for name, _ in systems]
    system_rates = []
    system_vacuums = []
    
    for name, system in systems:
        result = system.steady_state(test_condition)
        system_rates.append(result[0])
        system_vacuums.append(abs(result[1])/1000)
    
    x_pos = np.arange(len(system_names))
    ax5.bar(x_pos, system_rates, color=['blue', 'red', 'green'], alpha=0.7)
    ax5.set_xlabel('System Type')
    ax5.set_ylabel('Transfer Rate (kg/s)')
    ax5.set_title('System Performance Comparison')
    ax5.set_xticks(x_pos)
    ax5.set_xticklabels(system_names)
    ax5.grid(True, alpha=0.3, axis='y')
    
    # Vacuum setpoint vs actual performance
    vacuum_setpoints = np.linspace(-20000, -90000, 15)
    actual_vacuums = []
    powder_rates_vs_vacuum = []
    
    # Use pharma_vacuum for this analysis
    pharma_vacuum = systems[0][1]
    for setpoint in vacuum_setpoints:
        u_test = np.array([0.6, setpoint, 0.3])
        result = pharma_vacuum.steady_state(u_test)
        powder_rates_vs_vacuum.append(result[0])
        actual_vacuums.append(abs(result[1]))
    
    ax6.plot(abs(vacuum_setpoints)/1000, np.array(actual_vacuums)/1000, 'ko-', markersize=4, label='Actual')
    ax6.plot(abs(vacuum_setpoints)/1000, abs(vacuum_setpoints)/1000, 'k--', alpha=0.5, label='Ideal')
    ax6.set_xlabel('Vacuum Setpoint (kPa)')
    ax6.set_ylabel('Actual Vacuum (kPa)')
    ax6.set_title('Vacuum Performance vs Setpoint')
    ax6.grid(True, alpha=0.3)
    ax6.legend()
    
    plt.tight_layout()
    plt.savefig('VacuumTransfer_detailed_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    main()
