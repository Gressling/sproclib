"""
Reactor Examples - SPROCLIB
===========================

This module contains examples demonstrating the usage of reactor units in SPROCLIB.
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

from unit.reactor.cstr import CSTR
from unit.reactor.PlugFlowReactor import PlugFlowReactor
from unit.reactor.BatchReactor import BatchReactor
from unit.reactor.SemiBatchReactor import SemiBatchReactor
from unit.reactor.FluidizedBedReactor import FluidizedBedReactor
from unit.reactor.FixedBedReactor import FixedBedReactor


def simple_reactor_examples():
    """
    Simple examples of using reactor units.
    
    This example demonstrates basic reactor operations with simple reactions.
    """
    print("=== Simple Reactor Examples ===")
    
    # CSTR Example
    print("\n--- Continuous Stirred Tank Reactor (CSTR) ---")
    cstr = CSTR(name="Basic CSTR")
    
    print(f"CSTR created: {cstr.name}")
    print(f"Type: {type(cstr).__name__}")
    
    # Set reactor parameters
    volume = 2.0  # m³
    flow_rate = 0.5  # m³/h
    inlet_concentration = 2.0  # mol/L
    reaction_rate_constant = 0.3  # h^-1 (first-order)
    
    print(f"\nReactor specifications:")
    print(f"Volume: {volume} m³")
    print(f"Flow rate: {flow_rate} m³/h")
    print(f"Residence time: {volume/flow_rate:.1f} hours")
    print(f"Inlet concentration: {inlet_concentration} mol/L")
    print(f"Rate constant: {reaction_rate_constant} h^-1")
    
    # Calculate outlet concentration for first-order reaction
    residence_time = volume / flow_rate
    outlet_concentration = inlet_concentration / (1 + reaction_rate_constant * residence_time)
    conversion = (inlet_concentration - outlet_concentration) / inlet_concentration * 100
    
    print(f"\nResults:")
    print(f"Outlet concentration: {outlet_concentration:.2f} mol/L")
    print(f"Conversion: {conversion:.1f}%")
    
    # Plug Flow Reactor Example
    print("\n--- Plug Flow Reactor (PFR) ---")
    pfr = PlugFlowReactor(name="Basic PFR")
    
    print(f"PFR created: {pfr.name}")
    print(f"Type: {type(pfr).__name__}")
    
    # Set reactor parameters
    length = 10.0  # m
    diameter = 0.5  # m
    pfr_volume = np.pi * (diameter/2)**2 * length
    
    print(f"\nReactor specifications:")
    print(f"Length: {length} m")
    print(f"Diameter: {diameter} m")
    print(f"Volume: {pfr_volume:.2f} m³")
    print(f"Flow rate: {flow_rate} m³/h")
    print(f"Space time: {pfr_volume/flow_rate:.1f} hours")
    
    # Calculate outlet concentration for PFR (first-order)
    space_time = pfr_volume / flow_rate
    pfr_outlet_concentration = inlet_concentration * np.exp(-reaction_rate_constant * space_time)
    pfr_conversion = (inlet_concentration - pfr_outlet_concentration) / inlet_concentration * 100
    
    print(f"\nResults:")
    print(f"Outlet concentration: {pfr_outlet_concentration:.2f} mol/L")
    print(f"Conversion: {pfr_conversion:.1f}%")
    
    # Batch Reactor Example
    print("\n--- Batch Reactor ---")
    batch_reactor = BatchReactor(name="Basic Batch Reactor")
    
    print(f"Batch reactor created: {batch_reactor.name}")
    print(f"Type: {type(batch_reactor).__name__}")
    
    # Set batch parameters
    batch_volume = 1.5  # m³
    initial_concentration = 3.0  # mol/L
    batch_time = 2.0  # hours
    
    print(f"\nBatch specifications:")
    print(f"Volume: {batch_volume} m³")
    print(f"Initial concentration: {initial_concentration} mol/L")
    print(f"Reaction time: {batch_time} hours")
    print(f"Rate constant: {reaction_rate_constant} h^-1")
    
    # Calculate final concentration
    final_concentration = initial_concentration * np.exp(-reaction_rate_constant * batch_time)
    batch_conversion = (initial_concentration - final_concentration) / initial_concentration * 100
    
    print(f"\nResults:")
    print(f"Final concentration: {final_concentration:.2f} mol/L")
    print(f"Conversion: {batch_conversion:.1f}%")
    
    print("\nSimple reactor examples completed successfully!")


def comprehensive_reactor_examples():
    """
    Comprehensive examples demonstrating advanced reactor operations.
    
    This example includes:
    - Complex reaction kinetics
    - Temperature effects
    - Multi-reactor systems
    - Optimization studies
    - Fixed and fluidized bed reactors
    """
    print("\n=== Comprehensive Reactor Examples ===")
    
    # Complex Kinetics in CSTR
    print("\n--- Complex Kinetics Analysis ---")
    
    cstr = CSTR(name="Complex Kinetics CSTR")
    
    # Parallel reactions: A  ->  B (desired), A  ->  C (undesired)
    k1 = 0.5  # h^-1 (A  ->  B)
    k2 = 0.2  # h^-1 (A  ->  C)
    ca0 = 2.0  # mol/L
    volumes = np.linspace(0.5, 5.0, 10)  # m³
    flow_rate = 1.0  # m³/h
    
    print("Parallel Reactions: A  ->  B (desired), A  ->  C (undesired)")
    print(f"k1 (A -> B): {k1} h^-1, k2 (A -> C): {k2} h^-1")
    print(f"Feed concentration: {ca0} mol/L")
    
    print(f"\n{'Volume (m³)':<12} {'tau (h)':<8} {'CA (mol/L)':<12} {'CB (mol/L)':<12} {'CC (mol/L)':<12} {'Selectivity':<12}")
    print("-" * 80)
    
    for V in volumes:
        tau = V / flow_rate
        
        # Solve for outlet concentrations
        ca = ca0 / (1 + (k1 + k2) * tau)
        cb = k1 * tau * ca0 / (1 + (k1 + k2) * tau)
        cc = k2 * tau * ca0 / (1 + (k1 + k2) * tau)
        
        selectivity = cb / (cb + cc) if (cb + cc) > 0 else 0
        
        print(f"{V:<12.1f} {tau:<8.2f} {ca:<12.3f} {cb:<12.3f} {cc:<12.3f} {selectivity:<12.3f}")
    
    # Temperature Effects
    print("\n--- Temperature Effects on Reaction ---")
    
    # Arrhenius equation: k = A * exp(-Ea/RT)
    A = 1e8  # Pre-exponential factor (h^-1)
    Ea = 50000  # Activation energy (J/mol)
    R = 8.314  # Gas constant (J/mol·K)
    
    temperatures = np.linspace(300, 400, 11)  # K (27degC to 127degC)
    
    print("Arrhenius Kinetics Analysis:")
    print(f"A = {A:.0e} h^-1, Ea = {Ea/1000:.0f} kJ/mol")
    
    print(f"\n{'Temp (degC)':<10} {'Temp (K)':<10} {'k (h^-1)':<12} {'Conversion (%)':<15} {'Rate Ratio':<12}")
    print("-" * 70)
    
    k_ref = A * np.exp(-Ea / (R * 350))  # Reference at 350 K
    
    for T in temperatures:
        k = A * np.exp(-Ea / (R * T))
        
        # Assume CSTR with tau = 1 hour
        tau = 1.0
        conversion = k * tau / (1 + k * tau) * 100
        rate_ratio = k / k_ref
        
        print(f"{T-273.15:<10.0f} {T:<10.0f} {k:<12.2f} {conversion:<15.1f} {rate_ratio:<12.2f}")
    
    # Semi-Batch Reactor Analysis
    print("\n--- Semi-Batch Reactor Operation ---")
    
    semi_batch = SemiBatchReactor(name="Semi-Batch Reactor")
    
    # Fed-batch operation
    initial_volume = 1.0  # m³
    feed_rate = 0.1  # m³/h
    feed_concentration = 5.0  # mol/L
    operation_time = 5.0  # hours
    k = 0.4  # h^-1
    
    print(f"Fed-Batch Operation:")
    print(f"Initial volume: {initial_volume} m³")
    print(f"Feed rate: {feed_rate} m³/h")
    print(f"Feed concentration: {feed_concentration} mol/L")
    print(f"Operation time: {operation_time} hours")
    
    time_points = np.linspace(0, operation_time, 11)
    
    print(f"\n{'Time (h)':<10} {'Volume (m³)':<12} {'CA (mol/L)':<12} {'Total moles':<12} {'Conversion (%)':<15}")
    print("-" * 75)
    
    for t in time_points:
        # Current volume
        current_volume = initial_volume + feed_rate * t
        
        # Simplified solution (assuming well-mixed)
        # This is a simplified approximation
        if t == 0:
            ca = 0
            total_moles = 0
            conversion = 0
        else:
            # Average concentration (simplified)
            ca = feed_concentration * feed_rate * t / current_volume * np.exp(-k * t / 2)
            total_moles = ca * current_volume
            fed_moles = feed_concentration * feed_rate * t
            conversion = (fed_moles - total_moles) / fed_moles * 100 if fed_moles > 0 else 0
        
        print(f"{t:<10.1f} {current_volume:<12.2f} {ca:<12.3f} {total_moles:<12.2f} {conversion:<15.1f}")
    
    # Fixed Bed Reactor Analysis
    print("\n--- Fixed Bed Reactor Analysis ---")
    
    fixed_bed = FixedBedReactor(name="Catalytic Fixed Bed")
    
    # Catalyst and bed properties
    bed_length = 3.0  # m
    bed_diameter = 1.0  # m
    particle_diameter = 0.005  # m (5 mm)
    bed_porosity = 0.4
    catalyst_density = 1200  # kg/m³
    
    bed_volume = np.pi * (bed_diameter/2)**2 * bed_length
    catalyst_mass = bed_volume * (1 - bed_porosity) * catalyst_density
    
    print(f"Fixed Bed Specifications:")
    print(f"Bed length: {bed_length} m")
    print(f"Bed diameter: {bed_diameter} m")
    print(f"Particle diameter: {particle_diameter*1000:.0f} mm")
    print(f"Bed porosity: {bed_porosity}")
    print(f"Catalyst mass: {catalyst_mass:.0f} kg")
    
    # Performance analysis
    superficial_velocities = np.linspace(0.1, 1.0, 10)  # m/s
    
    print(f"\n{'Velocity (m/s)':<15} {'Re':<8} {'Pressure Drop (bar)':<18} {'Contact Time (s)':<18}")
    print("-" * 65)
    
    for u in superficial_velocities:
        # Reynolds number
        fluid_density = 1000  # kg/m³
        fluid_viscosity = 0.001  # Pa·s
        Re = fluid_density * u * particle_diameter / fluid_viscosity
        
        # Pressure drop (Ergun equation - simplified)
        pressure_drop = 150 * fluid_viscosity * u * (1-bed_porosity)**2 / (particle_diameter**2 * bed_porosity**3) * bed_length / 100000  # bar
        
        # Contact time
        contact_time = bed_length * bed_porosity / u
        
        print(f"{u:<15.2f} {Re:<8.0f} {pressure_drop:<18.3f} {contact_time:<18.1f}")
    
    # Fluidized Bed Reactor Analysis
    print("\n--- Fluidized Bed Reactor Analysis ---")
    
    fluidized_bed = FluidizedBedReactor(name="Fluidized Bed Reactor")
    
    # Fluidization parameters
    particle_density = 2500  # kg/m³
    fluid_density = 1.2  # kg/m³ (gas)
    particle_size = 0.0002  # m (200 μm)
    bed_diameter = 2.0  # m
    static_bed_height = 1.0  # m
    
    print(f"Fluidized Bed Specifications:")
    print(f"Particle density: {particle_density} kg/m³")
    print(f"Fluid density: {fluid_density} kg/m³")
    print(f"Particle size: {particle_size*1e6:.0f} μm")
    print(f"Bed diameter: {bed_diameter} m")
    print(f"Static bed height: {static_bed_height} m")
    
    # Calculate minimum fluidization velocity (simplified Ergun)
    g = 9.81  # m/s²
    fluid_viscosity = 1.8e-5  # Pa·s (air)
    
    # Archimedes number
    Ar = particle_size**3 * fluid_density * (particle_density - fluid_density) * g / fluid_viscosity**2
    
    # Reynolds number at minimum fluidization (simplified correlation)
    Re_mf = np.sqrt(33.7**2 + 0.0408 * Ar) - 33.7
    
    # Minimum fluidization velocity
    u_mf = Re_mf * fluid_viscosity / (particle_size * fluid_density)
    
    print(f"\nFluidization Analysis:")
    print(f"Archimedes number: {Ar:.0f}")
    print(f"Re at min. fluidization: {Re_mf:.2f}")
    print(f"Min. fluidization velocity: {u_mf:.3f} m/s")
    
    # Operating velocities
    operating_velocities = np.array([1, 2, 3, 5, 10]) * u_mf
    
    print(f"\n{'U/Umf':<8} {'Velocity (m/s)':<15} {'Bed Height (m)':<15} {'Regime':<20}")
    print("-" * 65)
    
    for i, u in enumerate(operating_velocities):
        u_ratio = u / u_mf
        
        # Simplified bed expansion (Richardson-Zaki type)
        if u_ratio < 1:
            bed_height = static_bed_height
            regime = "Fixed bed"
        elif u_ratio < 3:
            bed_height = static_bed_height * (u_ratio)**0.2
            regime = "Bubbling fluidized"
        elif u_ratio < 10:
            bed_height = static_bed_height * (u_ratio)**0.1
            regime = "Turbulent fluidized"
        else:
            bed_height = static_bed_height * 2
            regime = "Fast fluidized"
        
        print(f"{u_ratio:<8.1f} {u:<15.3f} {bed_height:<15.2f} {regime:<20}")
    
    print("\nComprehensive reactor examples completed successfully!")


def main():
    """
    Main function to run all reactor examples.
    """
    print("SPROCLIB Reactor Examples")
    print("=" * 50)
    
    try:
        # Run simple examples
        simple_reactor_examples()
        
        # Run comprehensive examples
        comprehensive_reactor_examples()
        
        print("\n" + "=" * 50)
        print("All reactor examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
