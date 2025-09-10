#!/usr/bin/env python3
"""
Mixer Example - Demonstration of Stream Mixing Operations

This example demonstrates various mixer configurations and applications.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from Mixer import Mixer


def example_1_hot_cold_mixing():
    """Example 1: Hot and cold water mixing"""
    print("=" * 60)
    print("Example 1: Hot and Cold Water Mixing")
    print("=" * 60)
    
    # Create mixer for 2 streams
    mixer = Mixer(
        n_inlets=2,
        mixing_efficiency=0.98,
        volume=1.5,
        heat_transfer_coeff=200.0,
        ambient_temp=298.15,
        pressure_drop=3000.0,
        name="HotColdMixer"
    )
    
    # Test different mixing ratios
    print("\nMixing Ratio Analysis:")
    print("Hot Flow | Cold Flow | Outlet Temp | Energy Balance")
    print("(kg/s)   | (kg/s)    | (°C)        | Check")
    print("-" * 50)
    
    hot_temp = 363.15  # 90°C
    cold_temp = 278.15  # 5°C
    pressure = 250000   # 2.5 bar
    
    results = []
    for hot_flow in [2, 5, 8, 10, 12]:
        cold_flow = 15 - hot_flow  # Total flow = 15 kg/s
        
        u = np.array([hot_flow, hot_temp, pressure,
                      cold_flow, cold_temp, pressure])
        
        result = mixer.steady_state(u)
        flow_out, temp_out, pres_out = result
        
        # Energy balance check
        cp = 4186.0
        energy_in = hot_flow * cp * hot_temp + cold_flow * cp * cold_temp
        energy_out = flow_out * cp * temp_out
        energy_balance = abs(energy_in - energy_out) / energy_in
        
        print(f"{hot_flow:8.1f} | {cold_flow:9.1f} | {temp_out-273.15:11.1f} | {energy_balance:10.4f}")
        
        results.append({
            'hot_flow': hot_flow,
            'cold_flow': cold_flow,
            'temp_out': temp_out,
            'flow_out': flow_out
        })
    
    return results


def example_2_three_stream_mixing():
    """Example 2: Three-stream chemical mixing"""
    print("\n" + "=" * 60)
    print("Example 2: Three-Stream Chemical Process Mixing")
    print("=" * 60)
    
    # Create mixer for chemical process
    mixer = Mixer(
        n_inlets=3,
        mixing_efficiency=0.92,
        volume=5.0,
        heat_transfer_coeff=800.0,
        ambient_temp=295.15,
        pressure_drop=8000.0,
        name="ChemicalMixer"
    )
    
    # Define process streams
    print("\nProcess Stream Conditions:")
    print("Stream | Flow Rate | Temperature | Pressure | Description")
    print("       | (kg/s)    | (°C)        | (bar)    |")
    print("-" * 65)
    
    # Stream 1: Main reactant (hot)
    flow_1, temp_1, pres_1 = 25.0, 343.15, 400000
    print(f"  1    | {flow_1:9.1f} | {temp_1-273.15:11.1f} | {pres_1/100000:8.1f} | Main reactant")
    
    # Stream 2: Secondary reactant (cold)
    flow_2, temp_2, pres_2 = 15.0, 288.15, 420000
    print(f"  2    | {flow_2:9.1f} | {temp_2-273.15:11.1f} | {pres_2/100000:8.1f} | Secondary reactant")
    
    # Stream 3: Solvent (ambient)
    flow_3, temp_3, pres_3 = 10.0, 298.15, 410000
    print(f"  3    | {flow_3:9.1f} | {temp_3-273.15:11.1f} | {pres_3/100000:8.1f} | Solvent")
    
    u = np.array([flow_1, temp_1, pres_1,
                  flow_2, temp_2, pres_2,
                  flow_3, temp_3, pres_3])
    
    # Calculate steady-state results
    result = mixer.steady_state(u)
    flow_out, temp_out, pres_out = result
    
    print(f"\nMixer Outlet Conditions:")
    print(f"Total flow rate: {flow_out:.1f} kg/s")
    print(f"Outlet temperature: {temp_out:.1f} K ({temp_out-273.15:.1f}°C)")
    print(f"Outlet pressure: {pres_out/100000:.1f} bar")
    print(f"Pressure drop: {(min([pres_1, pres_2, pres_3]) - pres_out)/1000:.1f} kPa")
    
    return result


def example_3_dynamic_startup():
    """Example 3: Dynamic mixer startup"""
    print("\n" + "=" * 60)
    print("Example 3: Dynamic Mixer Startup")
    print("=" * 60)
    
    # Create mixer for startup analysis
    mixer = Mixer(
        n_inlets=2,
        mixing_efficiency=0.95,
        volume=3.0,
        heat_transfer_coeff=400.0,
        ambient_temp=298.15,
        pressure_drop=5000.0,
        name="StartupMixer"
    )
    
    # Startup conditions
    flow_hot = 12.0
    temp_hot = 353.15  # 80°C
    flow_cold = 8.0
    temp_cold = 283.15  # 10°C
    pressure = 300000   # 3 bar
    
    u = np.array([flow_hot, temp_hot, pressure,
                  flow_cold, temp_cold, pressure])
    
    # Initial conditions: empty mixer
    x0 = np.array([0.0, 0.0])  # [mass, energy]
    
    # Time span for startup
    t_span = (0, 120)  # 2 minutes
    t_eval = np.linspace(0, 120, 200)
    
    # Solve dynamic model
    def dynamics_wrapper(t, x):
        return mixer.dynamics(t, x, u)
    
    print("\nSimulating mixer startup...")
    sol = solve_ivp(dynamics_wrapper, t_span, x0, t_eval=t_eval, 
                    method='RK45', rtol=1e-6)
    
    # Calculate profiles
    mass_profile = sol.y[0]
    energy_profile = sol.y[1]
    cp = 4186.0
    
    temp_profile = np.zeros_like(mass_profile)
    for i, (m, e) in enumerate(zip(mass_profile, energy_profile)):
        if m > 0.1:  # Avoid division by very small numbers
            temp_profile[i] = e / (m * cp)
        else:
            temp_profile[i] = mixer.ambient_temp
    
    # Calculate steady-state reference
    ss_result = mixer.steady_state(u)
    ss_temp = ss_result[1]
    
    print(f"\nStartup Analysis Results:")
    print(f"Steady-state temperature: {ss_temp:.1f} K ({ss_temp-273.15:.1f}°C)")
    print(f"Time to 95% of steady-state: {find_settling_time(t_eval, temp_profile, ss_temp):.1f} s")
    print(f"Final mixer mass: {mass_profile[-1]:.1f} kg")
    
    return t_eval, temp_profile, mass_profile, ss_temp


def example_4_parametric_study():
    """Example 4: Parametric study of mixing efficiency"""
    print("\n" + "=" * 60)
    print("Example 4: Mixing Efficiency Parametric Study")
    print("=" * 60)
    
    # Base mixer configuration
    base_mixer = Mixer(
        n_inlets=2,
        volume=2.0,
        heat_transfer_coeff=300.0,
        ambient_temp=298.15,
        pressure_drop=4000.0
    )
    
    # Stream conditions
    flow_1, temp_1, pres_1 = 10.0, 373.15, 300000  # Hot stream
    flow_2, temp_2, pres_2 = 10.0, 273.15, 300000  # Cold stream
    
    u = np.array([flow_1, temp_1, pres_1,
                  flow_2, temp_2, pres_2])
    
    # Theoretical mixed temperature (perfect mixing)
    theoretical_temp = (flow_1 * temp_1 + flow_2 * temp_2) / (flow_1 + flow_2)
    
    print(f"\nMixing Efficiency Analysis:")
    print(f"Hot stream: {flow_1} kg/s at {temp_1-273.15:.1f}°C")
    print(f"Cold stream: {flow_2} kg/s at {temp_2-273.15:.1f}°C")
    print(f"Theoretical mixed temperature: {theoretical_temp-273.15:.1f}°C")
    print()
    print("Efficiency | Outlet Temp | Deviation | Comment")
    print("    (-)    |     (°C)    |   (°C)    |")
    print("-" * 50)
    
    efficiencies = [0.70, 0.80, 0.85, 0.90, 0.95, 0.98, 1.00]
    results = []
    
    for eff in efficiencies:
        mixer = Mixer(
            n_inlets=2,
            mixing_efficiency=eff,
            volume=2.0,
            heat_transfer_coeff=300.0,
            ambient_temp=298.15,
            pressure_drop=4000.0
        )
        
        result = mixer.steady_state(u)
        temp_out = result[1]
        deviation = abs(temp_out - theoretical_temp)
        
        if eff >= 0.95:
            comment = "Excellent"
        elif eff >= 0.90:
            comment = "Good"
        elif eff >= 0.80:
            comment = "Moderate"
        else:
            comment = "Poor"
        
        print(f"{eff:10.2f} | {temp_out-273.15:11.1f} | {deviation:9.2f} | {comment}")
        
        results.append({
            'efficiency': eff,
            'temp_out': temp_out,
            'deviation': deviation
        })
    
    return results


def find_settling_time(time, signal, steady_state_value, tolerance=0.05):
    """Find settling time to within tolerance of steady-state value"""
    target = steady_state_value * (1 - tolerance)
    
    # Find last time signal crosses the target
    for i in range(len(signal)-1, 0, -1):
        if abs(signal[i] - steady_state_value) > abs(steady_state_value * tolerance):
            return time[i+1] if i+1 < len(time) else time[-1]
    
    return time[0]


def create_visualizations():
    """Create visualization plots for all examples"""
    print("\n" + "=" * 60)
    print("Creating Visualization Plots")
    print("=" * 60)
    
    # Run examples to get data
    results_1 = example_1_hot_cold_mixing()
    results_4 = example_4_parametric_study()
    t_eval, temp_profile, mass_profile, ss_temp = example_3_dynamic_startup()
    
    # Create plots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Mixing ratio vs outlet temperature
    hot_flows = [r['hot_flow'] for r in results_1]
    temps_out = [r['temp_out'] - 273.15 for r in results_1]
    
    ax1.plot(hot_flows, temps_out, 'bo-', linewidth=2, markersize=8)
    ax1.set_xlabel('Hot Water Flow Rate (kg/s)')
    ax1.set_ylabel('Outlet Temperature (°C)')
    ax1.set_title('Effect of Flow Ratio on Outlet Temperature')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Mixing efficiency effect
    efficiencies = [r['efficiency'] for r in results_4]
    deviations = [r['deviation'] for r in results_4]
    
    ax2.plot(efficiencies, deviations, 'ro-', linewidth=2, markersize=8)
    ax2.set_xlabel('Mixing Efficiency (-)')
    ax2.set_ylabel('Temperature Deviation (K)')
    ax2.set_title('Effect of Mixing Efficiency')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Dynamic startup - temperature
    ax3.plot(t_eval, temp_profile - 273.15, 'g-', linewidth=2, label='Mixer Temperature')
    ax3.axhline(y=ss_temp - 273.15, color='r', linestyle='--', 
               label=f'Steady State ({ss_temp-273.15:.1f}°C)')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Temperature (°C)')
    ax3.set_title('Dynamic Mixer Startup')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Dynamic startup - mass accumulation
    ax4.plot(t_eval, mass_profile, 'b-', linewidth=2)
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Mass in Mixer (kg)')
    ax4.set_title('Mass Accumulation During Startup')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('Mixer_example_plots.png', dpi=300, bbox_inches='tight')
    print("Plots saved as 'Mixer_example_plots.png'")
    
    return fig


def main():
    """Main function to run all examples"""
    print("SPROCLIB Mixer Model Examples")
    print("=" * 60)
    print("Demonstrating stream mixing operations and analysis")
    
    # Run all examples
    example_1_hot_cold_mixing()
    example_2_three_stream_mixing()
    example_3_dynamic_startup()
    example_4_parametric_study()
    
    # Create visualizations
    create_visualizations()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
