#!/usr/bin/env python3
"""
dynamics Function Example
=========================
Demonstration of the dynamics function for process control transport models.

This example shows how to use the dynamics function for time-domain analysis
with different transport models including PipeFlow, PeristalticFlow, and SlurryPipeline.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from PipeFlow import PipeFlow
from PeristalticFlow import PeristalticFlow
from SlurryPipeline import SlurryPipeline

def main():
    """Main function demonstrating dynamics function usage"""
    print("dynamics Function Example")
    print("=========================")
    print("Demonstration of dynamics function for time-domain analysis")
    print("Timestamp: 2025-07-09")
    print("=" * 60)
    
    # Example 1: PipeFlow dynamics
    print("\nEXAMPLE 1: PipeFlow dynamics Function")
    print("-" * 40)
    
    pipe = PipeFlow(
        pipe_length=500.0,       # 500 m
        pipe_diameter=0.15,      # 15 cm
        roughness=5e-5,          # Smooth steel
        fluid_density=1000.0,    # Water
        fluid_viscosity=1e-3,    # Water viscosity
        name="DynamicPipe"
    )
    
    print(f"Model: {pipe.name}")
    print(f"Pipe: {pipe.pipe_length:.0f} m x {pipe.pipe_diameter*100:.0f} cm")
    print(f"Material: Smooth steel")
    
    # Simulate step response
    dt = 0.1  # 0.1 second time steps
    t_final = 10.0  # 10 seconds
    time_points = np.arange(0, t_final, dt)
    n_points = len(time_points)
    
    # Initial conditions: [P_outlet, T_outlet]
    x0 = np.array([200000.0, 293.15])  # 200 kPa, 20°C
    
    # Input step: [P_inlet, T_inlet, flow_rate]
    u_step = np.array([300000.0, 298.15, 0.03])  # Step to 300 kPa, 25°C, 0.03 m³/s
    
    print(f"\nStep Response Analysis:")
    print(f"Initial State: P={x0[0]/1000:.0f} kPa, T={x0[1]-273.15:.1f}°C")
    print(f"Input Step: P={u_step[0]/1000:.0f} kPa, T={u_step[1]-273.15:.1f}°C, Q={u_step[2]:.3f} m³/s")
    
    # Simulate dynamics using simple Euler integration
    x_history = np.zeros((n_points, 2))
    x_history[0, :] = x0
    x_current = x0.copy()
    
    print(f"\nTime Domain Response (first 5 seconds):")
    print("Time | P_outlet | T_outlet | dP/dt  | dT/dt")
    print("(s)  | (kPa)    | (°C)     | (kPa/s)| (°C/s)")
    print("-" * 45)
    
    for i in range(1, n_points):
        t = time_points[i]
        
        # Calculate derivatives using dynamics function
        dx_dt = pipe.dynamics(t, x_current, u_step)
        
        # Simple Euler integration
        x_current = x_current + dx_dt * dt
        x_history[i, :] = x_current
        
        # Print first few steps
        if i <= 50:  # First 5 seconds
            if i % 10 == 0:  # Every second
                print(f"{t:4.1f} | {x_current[0]/1000:7.0f}  | {x_current[1]-273.15:7.1f}  | {dx_dt[0]/1000:6.1f} | {dx_dt[1]:6.2f}")
    
    pipe_results = {
        'time': time_points,
        'pressure': x_history[:, 0],
        'temperature': x_history[:, 1]
    }
    
    # Example 2: PeristalticFlow dynamics
    print("\n\nEXAMPLE 2: PeristalticFlow dynamics Function")
    print("-" * 45)
    
    pump = PeristalticFlow(
        tube_diameter=0.008,     # 8 mm tube
        tube_length=0.3,         # 30 cm
        pump_speed=80.0,         # 80 RPM
        occlusion_factor=0.85,   # 85% occlusion
        pulsation_damping=0.7,   # 70% damping
        name="DynamicPump"
    )
    
    print(f"Model: {pump.name}")
    print(f"Tube: {pump.tube_diameter*1000:.0f} mm x {pump.tube_length*100:.0f} cm")
    print(f"Base Speed: {pump.pump_speed:.0f} RPM")
    
    # Simulate speed change response
    dt = 0.05  # 50 ms time steps
    t_final = 5.0  # 5 seconds
    time_points = np.arange(0, t_final, dt)
    n_points = len(time_points)
    
    # Initial conditions: [flow_rate, pulsation_amplitude]
    x0 = np.array([5e-6, 0.01])  # 5 mL/min, 1% pulsation
    
    # Input: [P_inlet, pump_speed, occlusion_level]
    u_base = np.array([101325.0, 80.0, 1.0])
    u_step = np.array([101325.0, 120.0, 1.0])  # Speed step to 120 RPM
    
    print(f"\nSpeed Step Response:")
    print(f"Initial Speed: {u_base[1]:.0f} RPM")
    print(f"Step to: {u_step[1]:.0f} RPM at t=2s")
    
    x_history = np.zeros((n_points, 2))
    x_history[0, :] = x0
    x_current = x0.copy()
    
    print(f"\nPump Response (key time points):")
    print("Time | Speed | Flow Rate | Pulsation")
    print("(s)  | (RPM) | (mL/min)  | (%)")
    print("-" * 35)
    
    for i in range(1, n_points):
        t = time_points[i]
        
        # Switch input at t=2s
        u_current = u_step if t >= 2.0 else u_base
        
        # Calculate derivatives
        dx_dt = pump.dynamics(t, x_current, u_current)
        
        # Euler integration
        x_current = x_current + dx_dt * dt
        x_history[i, :] = x_current
        
        # Print key points
        if i % 20 == 0 or (t >= 1.8 and t <= 2.2 and i % 4 == 0):
            flow_ml_min = x_current[0] * 60 * 1e6
            pulsation_pct = x_current[1] * 100
            print(f"{t:4.1f} | {u_current[1]:5.0f} | {flow_ml_min:8.2f}  | {pulsation_pct:6.2f}")
    
    pump_results = {
        'time': time_points,
        'flow_rate': x_history[:, 0],
        'pulsation': x_history[:, 1]
    }
    
    # Example 3: SlurryPipeline dynamics  
    print("\n\nEXAMPLE 3: SlurryPipeline dynamics Function")
    print("-" * 44)
    
    slurry = SlurryPipeline(
        pipe_length=2000.0,      # 2 km
        pipe_diameter=0.3,       # 30 cm
        solid_concentration=0.2, # 20% solids
        particle_diameter=100e-6, # 100 microns
        name="DynamicSlurry"
    )
    
    print(f"Model: {slurry.name}")
    print(f"Pipeline: {slurry.pipe_length/1000:.0f} km x {slurry.pipe_diameter*100:.0f} cm")
    print(f"Solids: {slurry.solid_concentration*100:.0f}% vol")
    
    # Simulate concentration change response
    dt = 1.0  # 1 second time steps
    t_final = 100.0  # 100 seconds
    time_points = np.arange(0, t_final, dt)
    n_points = len(time_points)
    
    # Initial conditions: [P_outlet, c_solid_outlet]
    x0 = np.array([450000.0, 0.18])  # 450 kPa, 18% solids out
    
    # Input: [P_inlet, flow_rate, c_solid_inlet]
    u_base = np.array([500000.0, 0.2, 0.20])
    u_step = np.array([500000.0, 0.2, 0.30])  # Concentration step to 30%
    
    print(f"\nConcentration Step Response:")
    print(f"Initial Inlet Concentration: {u_base[2]*100:.0f}%")
    print(f"Step to: {u_step[2]*100:.0f}% at t=30s")
    
    x_history = np.zeros((n_points, 2))
    x_history[0, :] = x0
    x_current = x0.copy()
    
    print(f"\nSlurry Response (every 10 seconds):")
    print("Time | C_in | P_out | C_out | Transport")
    print("(s)  | (%)  | (kPa) | (%)   | Delay")
    print("-" * 40)
    
    for i in range(1, n_points):
        t = time_points[i]
        
        # Switch input at t=30s
        u_current = u_step if t >= 30.0 else u_base
        
        # Calculate derivatives
        dx_dt = slurry.dynamics(t, x_current, u_current)
        
        # Euler integration
        x_current = x_current + dx_dt * dt
        x_history[i, :] = x_current
        
        # Print every 10 seconds
        if i % 10 == 0:
            delay_s = abs(u_current[2] - x_current[1]) / 0.01 * 10  # Rough delay estimate
            print(f"{t:4.0f} | {u_current[2]*100:4.0f} | {x_current[0]/1000:5.0f} | {x_current[1]*100:5.1f} | {delay_s:6.0f}s")
    
    slurry_results = {
        'time': time_points,
        'pressure': x_history[:, 0],
        'concentration': x_history[:, 1]
    }
    
    # Example 4: Comparative Dynamics Analysis
    print("\n\nEXAMPLE 4: Dynamic Response Comparison")
    print("-" * 38)
    
    print("Model Response Characteristics:")
    print("Model           | Time Constant | Settling Time | Overshoot")
    print("-" * 60)
    
    # Simple response analysis
    pipe_tau = estimate_time_constant(pipe_results['time'], pipe_results['pressure'])
    pump_tau = estimate_time_constant(pump_results['time'], pump_results['flow_rate'])
    slurry_tau = estimate_time_constant(slurry_results['time'], slurry_results['concentration'])
    
    print(f"PipeFlow        | {pipe_tau:11.1f}s | {pipe_tau*4:11.1f}s | Low")
    print(f"PeristalticFlow | {pump_tau:11.1f}s | {pump_tau*4:11.1f}s | Low")
    print(f"SlurryPipeline  | {slurry_tau:11.1f}s | {slurry_tau*4:11.1f}s | None")
    
    # Create comprehensive visualization
    create_dynamics_plots(pipe_results, pump_results, slurry_results)
    
    print(f"\n\nExample completed successfully!")
    print(f"Generated: dynamics_example_plots.png")
    
    return {
        'pipe_results': pipe_results,
        'pump_results': pump_results,
        'slurry_results': slurry_results
    }

def estimate_time_constant(time, response):
    """Estimate time constant from step response"""
    # Find 63% of final value
    final_value = response[-1]
    initial_value = response[0]
    target_value = initial_value + 0.63 * (final_value - initial_value)
    
    # Find time when response reaches 63% of final value
    idx = np.argmin(np.abs(response - target_value))
    time_constant = time[idx] - time[0]
    
    return max(0.1, time_constant)  # Minimum 0.1s

def create_dynamics_plots(pipe_results, pump_results, slurry_results):
    """Create comprehensive dynamics function visualization"""
    
    fig = plt.figure(figsize=(15, 12))
    
    # Plot 1: PipeFlow Pressure Response
    ax1 = plt.subplot(3, 2, 1)
    plt.plot(pipe_results['time'], pipe_results['pressure']/1000, 'b-', linewidth=2)
    plt.axhline(y=300, color='red', linestyle='--', alpha=0.7, label='Target (300 kPa)')
    plt.xlabel('Time (s)')
    plt.ylabel('Outlet Pressure (kPa)')
    plt.title('PipeFlow: Pressure Step Response\\n(500m x 15cm pipe)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(0, 10)
    
    # Plot 2: PipeFlow Temperature Response
    ax2 = plt.subplot(3, 2, 2)
    plt.plot(pipe_results['time'], pipe_results['temperature']-273.15, 'g-', linewidth=2)
    plt.axhline(y=25, color='red', linestyle='--', alpha=0.7, label='Target (25°C)')
    plt.xlabel('Time (s)')
    plt.ylabel('Outlet Temperature (°C)')
    plt.title('PipeFlow: Temperature Step Response\\n(Thermal Dynamics)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(0, 10)
    
    # Plot 3: PeristalticFlow Flow Rate Response
    ax3 = plt.subplot(3, 2, 3)
    flow_ml_min = pump_results['flow_rate'] * 60 * 1e6
    plt.plot(pump_results['time'], flow_ml_min, 'purple', linewidth=2)
    plt.axvline(x=2.0, color='orange', linestyle='--', alpha=0.7, label='Speed Step (t=2s)')
    plt.xlabel('Time (s)')
    plt.ylabel('Flow Rate (mL/min)')
    plt.title('PeristalticFlow: Speed Step Response\\n(80→120 RPM)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(0, 5)
    
    # Plot 4: PeristalticFlow Pulsation Response
    ax4 = plt.subplot(3, 2, 4)
    pulsation_pct = pump_results['pulsation'] * 100
    plt.plot(pump_results['time'], pulsation_pct, 'orange', linewidth=2)
    plt.axvline(x=2.0, color='purple', linestyle='--', alpha=0.7, label='Speed Step (t=2s)')
    plt.xlabel('Time (s)')
    plt.ylabel('Pulsation Amplitude (%)')
    plt.title('PeristalticFlow: Pulsation Dynamics\\n(Speed Change Effect)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(0, 5)
    
    # Plot 5: SlurryPipeline Concentration Response
    ax5 = plt.subplot(3, 2, 5)
    conc_pct = slurry_results['concentration'] * 100
    plt.plot(slurry_results['time'], conc_pct, 'brown', linewidth=2)
    plt.axvline(x=30.0, color='red', linestyle='--', alpha=0.7, label='Conc. Step (t=30s)')
    plt.axhline(y=30, color='red', linestyle=':', alpha=0.7, label='Target (30%)')
    plt.xlabel('Time (s)')
    plt.ylabel('Outlet Concentration (%)')
    plt.title('SlurryPipeline: Concentration Step\\n(20%→30% solids)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(0, 100)
    
    # Plot 6: Comparative Response Times
    ax6 = plt.subplot(3, 2, 6)
    
    models = ['PipeFlow\\n(Pressure)', 'PipeFlow\\n(Temperature)', 'PeristalticFlow\\n(Flow)', 'SlurryPipeline\\n(Concentration)']
    time_constants = [
        estimate_time_constant(pipe_results['time'], pipe_results['pressure']),
        estimate_time_constant(pipe_results['time'], pipe_results['temperature']),
        estimate_time_constant(pump_results['time'], pump_results['flow_rate']),
        estimate_time_constant(slurry_results['time'], slurry_results['concentration'])
    ]
    
    colors = ['blue', 'green', 'purple', 'brown']
    bars = plt.bar(range(len(models)), time_constants, color=colors, alpha=0.7)
    
    plt.xlabel('System Response')
    plt.ylabel('Time Constant (s)')
    plt.title('Dynamic Response Comparison\\n(63% Response Time)')
    plt.xticks(range(len(models)), models, rotation=45, ha='right')
    plt.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, tc in zip(bars, time_constants):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'{tc:.1f}s', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('dynamics_example_plots.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    main()
