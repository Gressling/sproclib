#!/usr/bin/env python3
"""
steady_state Function Example
=============================
Demonstration of the steady_state function for process control transport models.

This example shows how to use the steady_state function with different transport models
including PipeFlow, PeristalticFlow, and SlurryPipeline.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from PipeFlow import PipeFlow
from PeristalticFlow import PeristalticFlow
from SlurryPipeline import SlurryPipeline

def main():
    """Main function demonstrating steady_state function usage"""
    print("steady_state Function Example")
    print("=============================")
    print("Demonstration of steady_state function across transport models")
    print("Timestamp: 2025-07-09")
    print("=" * 60)
    
    # Example 1: PipeFlow steady_state
    print("\nEXAMPLE 1: PipeFlow steady_state Function")
    print("-" * 45)
    
    pipe = PipeFlow(
        pipe_length=1000.0,      # 1 km
        pipe_diameter=0.2,       # 20 cm
        roughness=1e-4,          # Steel pipe
        fluid_density=1000.0,    # Water
        fluid_viscosity=1e-3,    # Water viscosity
        name="SteadyStatePipe"
    )
    
    print(f"Model: {pipe.name}")
    print(f"Pipe: {pipe.pipe_length/1000:.1f} km x {pipe.pipe_diameter*100:.0f} cm")
    print(f"Material: Steel (roughness = {pipe.roughness:.0e} m)")
    
    # steady_state expects [P_inlet, T_inlet, flow_rate]
    inlet_pressures = np.array([200000, 300000, 400000, 500000])  # Pa
    inlet_temperature = 293.15  # K (20°C)
    flow_rate = 0.05  # m³/s
    
    print(f"\nSteady-State Analysis for {flow_rate:.3f} m³/s:")
    print("Inlet P | Outlet P | Pressure Drop | Velocity | Reynolds")
    print("(kPa)   | (kPa)    | (kPa)         | (m/s)    | Number")
    print("-" * 60)
    
    pipe_results = []
    for p_in in inlet_pressures:
        inputs = np.array([p_in, inlet_temperature, flow_rate])
        result = pipe.steady_state(inputs)
        
        p_out = result[0]
        t_out = result[1]
        
        # Calculate velocity and Reynolds number for display
        velocity = flow_rate / (np.pi * (pipe.pipe_diameter/2)**2)
        reynolds = pipe.fluid_density * velocity * pipe.pipe_diameter / pipe.fluid_viscosity
        pressure_drop = p_in - p_out
        
        print(f"{p_in/1000:7.0f} | {p_out/1000:8.0f} | {pressure_drop/1000:12.0f}  | {velocity:7.2f}  | {reynolds:8.0f}")
        
        pipe_results.append({
            'p_in': p_in, 'p_out': p_out, 'velocity': velocity, 'reynolds': reynolds
        })
    
    # Example 2: PeristalticFlow steady_state
    print("\n\nEXAMPLE 2: PeristalticFlow steady_state Function")
    print("-" * 50)
    
    pump = PeristalticFlow(
        tube_diameter=0.01,      # 10 mm tube
        tube_length=0.5,         # 50 cm in pump head
        pump_speed=100.0,        # 100 RPM
        occlusion_factor=0.9,    # 90% occlusion
        fluid_density=1000.0,    # Water
        name="SteadyStatePump"
    )
    
    print(f"Model: {pump.name}")
    print(f"Tube: {pump.tube_diameter*1000:.0f} mm ID x {pump.tube_length*100:.0f} cm")
    print(f"Speed: {pump.pump_speed:.0f} RPM, Occlusion: {pump.occlusion_factor*100:.0f}%")
    
    # steady_state expects [P_inlet, pump_speed, occlusion_level]
    pump_speeds = np.array([50, 75, 100, 125, 150])  # RPM
    inlet_pressure = 101325.0  # Atmospheric
    occlusion_level = 1.0  # Full occlusion
    
    print(f"\nSteady-State Analysis at {inlet_pressure/1000:.0f} kPa inlet:")
    print("Speed | Flow Rate | Outlet P | Backpressure")
    print("(RPM) | (mL/min)  | (kPa)    | Effect")
    print("-" * 40)
    
    pump_results = []
    for speed in pump_speeds:
        inputs = np.array([inlet_pressure, speed, occlusion_level])
        result = pump.steady_state(inputs)
        
        flow_rate = result[0]  # m³/s
        p_out = result[1]      # Pa
        
        flow_ml_min = flow_rate * 60 * 1e6  # Convert to mL/min
        backpressure_effect = (p_out - inlet_pressure) / inlet_pressure * 100
        
        print(f"{speed:5.0f} | {flow_ml_min:8.1f}  | {p_out/1000:7.0f}  | {backpressure_effect:+8.2f}%")
        
        pump_results.append({
            'speed': speed, 'flow_rate': flow_rate, 'p_out': p_out
        })
    
    # Example 3: SlurryPipeline steady_state
    print("\n\nEXAMPLE 3: SlurryPipeline steady_state Function")
    print("-" * 48)
    
    slurry = SlurryPipeline(
        pipe_length=5000.0,      # 5 km
        pipe_diameter=0.4,       # 40 cm
        solid_concentration=0.25, # 25% solids
        particle_diameter=200e-6, # 200 microns
        solid_density=2500.0,    # Sand
        name="SteadyStateSlurry"
    )
    
    print(f"Model: {slurry.name}")
    print(f"Pipeline: {slurry.pipe_length/1000:.0f} km x {slurry.pipe_diameter*100:.0f} cm")
    print(f"Solids: {slurry.solid_concentration*100:.0f}% vol, {slurry.particle_diameter*1e6:.0f} micron particles")
    
    # steady_state expects [P_inlet, flow_rate, c_solid_in]
    flow_rates = np.array([0.1, 0.2, 0.3, 0.4, 0.5])  # m³/s
    inlet_pressure = 600000.0  # 600 kPa
    solid_conc_in = slurry.solid_concentration
    
    print(f"\nSteady-State Analysis at {inlet_pressure/1000:.0f} kPa inlet:")
    print("Flow   | Velocity | Outlet P | Solids Out | Settling")
    print("(m³/s) | (m/s)    | (kPa)    | (%)        | Effect")
    print("-" * 50)
    
    slurry_results = []
    for flow in flow_rates:
        inputs = np.array([inlet_pressure, flow, solid_conc_in])
        result = slurry.steady_state(inputs)
        
        p_out = result[0]
        c_solid_out = result[1]
        
        velocity = flow / (np.pi * (slurry.pipe_diameter/2)**2)
        settling_effect = (solid_conc_in - c_solid_out) / solid_conc_in * 100
        
        print(f"{flow:6.1f} | {velocity:7.2f}  | {p_out/1000:7.0f}  | {c_solid_out*100:9.1f}  | {settling_effect:+7.1f}%")
        
        slurry_results.append({
            'flow': flow, 'velocity': velocity, 'p_out': p_out, 'c_solid_out': c_solid_out
        })
    
    # Example 4: Comparative Analysis
    print("\n\nEXAMPLE 4: Comparative Model Analysis")
    print("-" * 37)
    
    print("Model Comparison at Standard Conditions:")
    print("Model           | Input Format                     | Output Format")
    print("-" * 75)
    print("PipeFlow        | [P_inlet, T_inlet, flow_rate]    | [P_outlet, T_outlet]")
    print("PeristalticFlow | [P_inlet, speed, occlusion]      | [flow_rate, P_outlet]")
    print("SlurryPipeline  | [P_inlet, flow, c_solid]         | [P_outlet, c_solid_out]")
    
    # Create comprehensive visualization
    create_steady_state_plots(pipe_results, pump_results, slurry_results)
    
    print(f"\n\nExample completed successfully!")
    print(f"Generated: steady_state_example_plots.png")
    
    return {
        'pipe_results': pipe_results,
        'pump_results': pump_results,
        'slurry_results': slurry_results
    }

def create_steady_state_plots(pipe_results, pump_results, slurry_results):
    """Create comprehensive steady_state function visualization"""
    
    fig = plt.figure(figsize=(15, 10))
    
    # Plot 1: PipeFlow - Pressure Drop vs Inlet Pressure
    ax1 = plt.subplot(2, 3, 1)
    pressures_in = [r['p_in']/1000 for r in pipe_results]
    pressure_drops = [(r['p_in'] - r['p_out'])/1000 for r in pipe_results]
    
    plt.plot(pressures_in, pressure_drops, 'b-', marker='o', linewidth=2, markersize=6)
    plt.xlabel('Inlet Pressure (kPa)')
    plt.ylabel('Pressure Drop (kPa)')
    plt.title('PipeFlow: Pressure Drop Analysis\\n(1 km Steel Pipe)')
    plt.grid(True, alpha=0.3)
    
    # Plot 2: PipeFlow - Reynolds Number
    ax2 = plt.subplot(2, 3, 2)
    reynolds_numbers = [r['reynolds'] for r in pipe_results]
    
    plt.plot(pressures_in, reynolds_numbers, 'g-', marker='s', linewidth=2, markersize=6)
    plt.xlabel('Inlet Pressure (kPa)')
    plt.ylabel('Reynolds Number')
    plt.title('PipeFlow: Reynolds Number\\n(Flow Regime Analysis)')
    plt.grid(True, alpha=0.3)
    
    # Add flow regime indicators
    plt.axhline(y=2300, color='red', linestyle='--', label='Laminar/Turbulent')
    plt.legend()
    
    # Plot 3: PeristalticFlow - Flow Rate vs Speed
    ax3 = plt.subplot(2, 3, 3)
    speeds = [r['speed'] for r in pump_results]
    flow_rates_ml = [r['flow_rate']*60*1e6 for r in pump_results]
    
    plt.plot(speeds, flow_rates_ml, 'purple', marker='^', linewidth=2, markersize=6)
    plt.xlabel('Pump Speed (RPM)')
    plt.ylabel('Flow Rate (mL/min)')
    plt.title('PeristalticFlow: Speed-Flow Relationship\\n(10 mm Tube)')
    plt.grid(True, alpha=0.3)
    
    # Plot 4: SlurryPipeline - Velocity vs Settling
    ax4 = plt.subplot(2, 3, 4)
    velocities = [r['velocity'] for r in slurry_results]
    concentrations_out = [r['c_solid_out']*100 for r in slurry_results]
    
    plt.plot(velocities, concentrations_out, 'orange', marker='d', linewidth=2, markersize=6)
    plt.xlabel('Flow Velocity (m/s)')
    plt.ylabel('Outlet Solids Concentration (%)')
    plt.title('SlurryPipeline: Settling Effect\\n(5 km Pipeline)')
    plt.grid(True, alpha=0.3)
    
    # Plot 5: Pressure Drop Comparison
    ax5 = plt.subplot(2, 3, 5)
    
    # Normalize to common basis for comparison
    pipe_drops = pressure_drops
    slurry_drops = [(600 - r['p_out']/1000) for r in slurry_results]
    
    # Make sure both arrays have the same length
    min_length = min(len(pipe_drops), len(slurry_drops))
    x_pos = np.arange(min_length)
    
    plt.bar(x_pos - 0.2, pipe_drops[:min_length], 0.4, label='PipeFlow (Clean)', color='blue', alpha=0.7)
    plt.bar(x_pos + 0.2, slurry_drops[:min_length], 0.4, label='SlurryPipeline (25% solids)', color='orange', alpha=0.7)
    
    plt.xlabel('Test Condition')
    plt.ylabel('Pressure Drop (kPa)')
    plt.title('Pressure Drop Comparison\\n(Clean vs Slurry Flow)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 6: Model Application Summary
    ax6 = plt.subplot(2, 3, 6)
    
    # Create summary comparison
    models = ['PipeFlow', 'PeristalticFlow', 'SlurryPipeline']
    complexities = [1, 2, 3]  # Relative complexity
    applications = [3, 2, 1]  # Relative number of applications
    
    x_pos = np.arange(len(models))
    
    plt.bar(x_pos - 0.2, complexities, 0.4, label='Model Complexity', color='lightblue', alpha=0.7)
    plt.bar(x_pos + 0.2, applications, 0.4, label='Application Scope', color='lightgreen', alpha=0.7)
    
    plt.xlabel('Transport Model')
    plt.ylabel('Relative Scale (1-3)')
    plt.title('Model Characteristics\\n(Complexity vs Applications)')
    plt.xticks(x_pos, models, rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('steady_state_example_plots.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()
