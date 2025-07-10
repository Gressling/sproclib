#!/usr/bin/env python3
"""
PipeFlow Example Usage - Comprehensive Demonstration

This example demonstrates the capabilities of the PipeFlow class for modeling
single-phase liquid flow in pipes. It covers both steady-state and dynamic
analysis with various scenarios and parameter studies.

Based on: PipeFlow_documentation.md
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from PipeFlow import PipeFlow
except ImportError:
    print("Error: Could not import PipeFlow. Make sure PipeFlow.py is in the current directory.")
    sys.exit(1)

def example_1_basic_pipe_flow():
    """
    Example 1: Basic pipe flow calculation for a water supply line
    
    Scenario: Water supply line from storage tank to treatment plant
    - 500m long pipeline
    - 15cm diameter steel pipe
    - Water at 20°C
    """
    print("=" * 60)
    print("EXAMPLE 1: Basic Water Supply Pipeline")
    print("=" * 60)
    
    # Create pipe flow model
    water_pipe = PipeFlow(
        pipe_length=500.0,          # 500 m pipeline
        pipe_diameter=0.15,         # 15 cm diameter
        roughness=0.046e-3,         # Commercial steel roughness
        fluid_density=1000.0,       # Water density at 20°C
        fluid_viscosity=1.002e-3,   # Water viscosity at 20°C
        elevation_change=25.0,      # 25 m elevation gain
        name="WaterSupplyPipe"
    )
    
    # Display model information
    print("\nModel Configuration:")
    info = water_pipe.describe()
    print(f"Model Type: {info['model_type']}")
    print(f"Pipe Length: {water_pipe.pipe_length} m")
    print(f"Pipe Diameter: {water_pipe.pipe_diameter*1000} mm")
    print(f"Elevation Change: {water_pipe.elevation_change} m")
    
    # Steady-state analysis for different flow rates
    flow_rates = [0.01, 0.05, 0.1, 0.15, 0.2]  # m³/s
    
    print("\nSteady-State Analysis:")
    print("Flow Rate | Velocity | Reynolds | Friction | Pressure | Flow")
    print("(L/s)     | (m/s)    | Number   | Factor   | Drop(kPa)| Regime")
    print("-" * 70)
    
    results_data = []
    for flow in flow_rates:
        # steady_state expects [P_inlet, T_inlet, flow_rate]
        u = np.array([101325.0, 293.15, flow])  # 1 atm, 20°C, flow_rate
        result_array = water_pipe.steady_state(u)
        
        # For examples, we need to call the individual calculation
        # Let's create a helper method to get the detailed results
        velocity = flow / (np.pi * (water_pipe.pipe_diameter/2)**2)
        Re = water_pipe.fluid_density * velocity * water_pipe.pipe_diameter / water_pipe.fluid_viscosity
        
        # Calculate friction factor
        if Re < 2300:
            friction_factor = 64 / Re
            regime = "laminar"
        elif Re > 4000:
            # Colebrook-White approximation (Swamee-Jain)
            friction_factor = 0.25 / (np.log10(water_pipe.roughness/(3.7*water_pipe.pipe_diameter) + 5.74/(Re**0.9)))**2
            regime = "turbulent"
        else:
            # Transition region - interpolate
            f_lam = 64 / Re
            f_turb = 0.25 / (np.log10(water_pipe.roughness/(3.7*water_pipe.pipe_diameter) + 5.74/(Re**0.9)))**2
            friction_factor = f_lam + (f_turb - f_lam) * (Re - 2300) / (4000 - 2300)
            regime = "transition"
        
        # Calculate pressure loss
        pressure_loss = friction_factor * (water_pipe.pipe_length/water_pipe.pipe_diameter) * (water_pipe.fluid_density * velocity**2)/2
        pressure_loss += water_pipe.fluid_density * 9.81 * water_pipe.elevation_change  # Add elevation
        
        result = {
            'velocity': velocity,
            'reynolds_number': Re,
            'friction_factor': friction_factor,
            'pressure_loss': pressure_loss,
            'flow_regime': regime
        }
        
        flow_ls = flow * 1000  # Convert to L/s
        velocity = result['velocity']
        reynolds = result['reynolds_number']
        friction = result['friction_factor']
        pressure_kpa = result['pressure_loss'] / 1000  # Convert to kPa
        regime = result['flow_regime']
        
        print(f"{flow_ls:8.0f}  | {velocity:7.3f}  | {reynolds:8.0f} | {friction:8.5f} | {pressure_kpa:8.1f} | {regime}")
        
        results_data.append({
            'flow_rate': flow,
            'velocity': velocity,
            'reynolds': reynolds,
            'pressure_loss': result['pressure_loss'],
            'regime': regime
        })
    
    return results_data

def example_2_pump_sizing():
    """
    Example 2: Pump sizing calculation for a chemical transfer system
    
    Scenario: Acid transfer line in chemical plant
    - 200m horizontal pipe
    - 10cm diameter lined pipe
    - Sulfuric acid solution
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Chemical Transfer System - Pump Sizing")
    print("=" * 60)
    
    # Sulfuric acid properties (20% solution at 25°C)
    acid_pipe = PipeFlow(
        pipe_length=200.0,          # 200 m transfer line
        pipe_diameter=0.10,         # 10 cm diameter
        roughness=0.015e-3,         # Smooth lined pipe
        fluid_density=1140.0,       # 20% H2SO4 density
        fluid_viscosity=1.32e-3,    # 20% H2SO4 viscosity
        elevation_change=0.0,       # Horizontal transfer
        name="AcidTransferPipe"
    )
    
    print("\nChemical Properties:")
    print(f"Fluid: 20% Sulfuric Acid Solution")
    print(f"Density: {acid_pipe.fluid_density} kg/m³")
    print(f"Viscosity: {acid_pipe.fluid_viscosity*1000:.2f} mPa·s")
    
    # Calculate system curve (pressure vs flow)
    flow_range = np.linspace(0.005, 0.08, 20)  # 5 to 80 L/s
    system_curve = []
    
    print("\nSystem Curve Generation:")
    print("Flow Rate | Pressure Loss | Total Head")
    print("(L/s)     | (kPa)         | (m)")
    print("-" * 35)
    
    for flow in flow_range:
        # Calculate using helper function
        velocity = flow / (np.pi * (acid_pipe.pipe_diameter/2)**2)
        Re = acid_pipe.fluid_density * velocity * acid_pipe.pipe_diameter / acid_pipe.fluid_viscosity
        
        if Re < 2300:
            friction_factor = 64 / Re
        else:
            friction_factor = 0.25 / (np.log10(acid_pipe.roughness/(3.7*acid_pipe.pipe_diameter) + 5.74/(Re**0.9)))**2
        
        pressure_loss = friction_factor * (acid_pipe.pipe_length/acid_pipe.pipe_diameter) * (acid_pipe.fluid_density * velocity**2)/2
        head_loss = pressure_loss / (acid_pipe.fluid_density * 9.81)
        
        flow_ls = flow * 1000
        pressure_kpa = pressure_loss / 1000
        
        if flow_ls % 10 < 1:  # Print every ~10 L/s
            print(f"{flow_ls:8.1f}  | {pressure_kpa:11.1f}   | {head_loss:8.2f}")
        
        system_curve.append({'flow': flow, 'pressure': pressure_loss, 'head': head_loss})
    
    # Find operating point for specific flow requirement
    target_flow = 0.03  # 30 L/s requirement
    
    # Calculate for target flow
    velocity = target_flow / (np.pi * (acid_pipe.pipe_diameter/2)**2)
    Re = acid_pipe.fluid_density * velocity * acid_pipe.pipe_diameter / acid_pipe.fluid_viscosity
    friction_factor = 0.25 / (np.log10(acid_pipe.roughness/(3.7*acid_pipe.pipe_diameter) + 5.74/(Re**0.9)))**2
    pressure_loss = friction_factor * (acid_pipe.pipe_length/acid_pipe.pipe_diameter) * (acid_pipe.fluid_density * velocity**2)/2
    
    result = {'pressure_loss': pressure_loss}
    
    print(f"\nDesign Point Analysis (30 L/s):")
    print(f"Required Flow Rate: {target_flow*1000:.0f} L/s")
    print(f"Pipe Pressure Loss: {result['pressure_loss']/1000:.1f} kPa")
    print(f"Pump Head Required: {result['pressure_loss']/(acid_pipe.fluid_density*9.81):.1f} m")
    print(f"Pump Power (75% eff): {(result['pressure_loss']*target_flow/0.75/1000):.1f} kW")
    
    return system_curve

def example_3_dynamic_response():
    """
    Example 3: Dynamic response analysis for control system design
    
    Scenario: Feed line to reactor with flow control
    - Analyze step response for controller tuning
    - Study startup transients
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Dynamic Response Analysis")
    print("=" * 60)
    
    # Reactor feed line
    feed_pipe = PipeFlow(
        pipe_length=150.0,          # 150 m feed line
        pipe_diameter=0.08,         # 8 cm diameter
        roughness=0.025e-3,         # Electropolished stainless steel
        fluid_density=950.0,        # Organic solvent
        fluid_viscosity=0.8e-3,     # Low viscosity solvent
        elevation_change=5.0,       # Slight elevation change
        name="ReactorFeedPipe"
    )
    
    print("\nDynamic Analysis Setup:")
    print(f"Pipe Length: {feed_pipe.pipe_length} m")
    print(f"Expected Time Constant: ~{feed_pipe.pipe_length/10:.0f} seconds")
    
    # Step response simulation
    dt = 0.5  # Time step: 0.5 seconds
    t_final = 120  # Total time: 2 minutes
    time_points = np.arange(0, t_final, dt)
    n_points = len(time_points)
    
    # Step change at t = 30s: 0.015 → 0.025 m³/s
    flow_input = np.zeros(n_points)
    flow_input[0:60] = 0.015    # First 30 seconds
    flow_input[60:] = 0.025     # Step to higher flow
    
    # Initialize arrays for results
    velocity_history = np.zeros(n_points)
    pressure_history = np.zeros(n_points)
    flow_output = np.zeros(n_points)
    
    # Initial steady state
    initial_result = feed_pipe.steady_state(flow_input[0])
    current_velocity = initial_result['velocity']
    
    print(f"\nSimulating step response...")
    print(f"Initial flow: {flow_input[0]*1000:.1f} L/s")
    print(f"Final flow: {flow_input[-1]*1000:.1f} L/s")
    
    # Time integration
    for i, t in enumerate(time_points):
        # Dynamic simulation step
        result = feed_pipe.dynamics(flow_input[i], dt)
        
        # Store results
        velocity_history[i] = result['velocity']
        pressure_history[i] = result['pressure_drop']
        flow_output[i] = result['flow_rate']
        
        # Update current state
        current_velocity = result['velocity']
    
    # Analysis of step response
    step_start_idx = 60
    step_response = flow_output[step_start_idx:]
    final_value = flow_input[-1]
    
    # Find 63% response time (time constant)
    target_63 = flow_input[0] + 0.63 * (final_value - flow_input[0])
    tau_idx = np.where(flow_output >= target_63)[0]
    time_constant = time_points[tau_idx[0]] - time_points[step_start_idx] if len(tau_idx) > 0 else 0
    
    print(f"\nStep Response Analysis:")
    print(f"Time Constant (τ): {time_constant:.1f} seconds")
    print(f"Settling Time (4τ): {4*time_constant:.1f} seconds")
    print(f"Final Pressure: {pressure_history[-1]/1000:.1f} kPa")
    
    return {
        'time': time_points,
        'flow_input': flow_input,
        'flow_output': flow_output,
        'velocity': velocity_history,
        'pressure': pressure_history,
        'time_constant': time_constant
    }

def example_4_parametric_study():
    """
    Example 4: Parametric study of pipe roughness effects
    
    Scenario: Study effect of pipe aging on system performance
    - Compare new vs aged pipes
    - Quantify fouling impact
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Pipe Roughness Parametric Study")
    print("=" * 60)
    
    # Base pipe configuration
    base_params = {
        'pipe_length': 300.0,
        'pipe_diameter': 0.12,
        'fluid_density': 1000.0,
        'fluid_viscosity': 1e-3,
        'elevation_change': 0.0
    }
    
    # Different pipe conditions
    pipe_conditions = [
        {'name': 'New Stainless Steel', 'roughness': 0.015e-3},
        {'name': 'Used Stainless Steel', 'roughness': 0.030e-3},
        {'name': 'New Carbon Steel', 'roughness': 0.046e-3},
        {'name': 'Aged Carbon Steel', 'roughness': 0.150e-3},
        {'name': 'Heavily Fouled', 'roughness': 0.500e-3}
    ]
    
    flow_rate = 0.05  # 50 L/s test flow
    
    print(f"\nRoughness Impact Analysis (Flow = {flow_rate*1000:.0f} L/s):")
    print("Pipe Condition        | Roughness | Pressure | Friction | Power")
    print("                      | (μm)      | Loss(kPa)| Factor   | (kW)")
    print("-" * 65)
    
    roughness_data = []
    for condition in pipe_conditions:
        pipe = PipeFlow(
            roughness=condition['roughness'],
            **base_params
        )
        
        result = pipe.steady_state(flow_rate)
        
        roughness_um = condition['roughness'] * 1e6  # Convert to micrometers
        pressure_kpa = result['pressure_loss'] / 1000
        friction_factor = result['friction_factor']
        power_kw = result['pressure_loss'] * flow_rate / 1000  # Hydraulic power
        
        print(f"{condition['name']:20s} | {roughness_um:8.0f}  | {pressure_kpa:8.1f} | {friction_factor:8.5f} | {power_kw:6.2f}")
        
        roughness_data.append({
            'name': condition['name'],
            'roughness': condition['roughness'],
            'pressure_loss': result['pressure_loss'],
            'friction_factor': friction_factor,
            'power': power_kw
        })
    
    # Calculate fouling impact
    new_pressure = roughness_data[0]['pressure_loss']
    fouled_pressure = roughness_data[-1]['pressure_loss']
    fouling_factor = fouled_pressure / new_pressure
    
    print(f"\nFouling Impact Analysis:")
    print(f"New pipe pressure loss: {new_pressure/1000:.1f} kPa")
    print(f"Fouled pipe pressure loss: {fouled_pressure/1000:.1f} kPa")
    print(f"Fouling factor: {fouling_factor:.2f}x")
    print(f"Additional pumping power: {((fouled_pressure-new_pressure)*flow_rate/1000):.2f} kW")
    
    return roughness_data

def create_visualizations():
    """
    Create visualization plots for the pipe flow examples
    """
    print("\n" + "=" * 60)
    print("CREATING VISUALIZATION PLOTS")
    print("=" * 60)
    
    # Run examples to get data
    basic_data = example_1_basic_pipe_flow()
    system_curve = example_2_pump_sizing()
    dynamic_data = example_3_dynamic_response()
    roughness_data = example_4_parametric_study()
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 12))
    
    # Plot 1: System Curve (Flow vs Pressure)
    ax1 = plt.subplot(2, 3, 1)
    flows = [d['flow'] for d in system_curve]
    pressures = [d['pressure']/1000 for d in system_curve]  # Convert to kPa
    
    plt.plot(np.array(flows)*1000, pressures, 'b-', linewidth=2, label='System Curve')
    plt.scatter([30], [system_curve[10]['pressure']/1000], color='red', s=100, 
                label='Design Point', zorder=5)
    plt.xlabel('Flow Rate (L/s)')
    plt.ylabel('Pressure Loss (kPa)')
    plt.title('Pipe System Curve\n(Acid Transfer Line)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Plot 2: Reynolds Number vs Friction Factor
    ax2 = plt.subplot(2, 3, 2)
    reynolds = [d['reynolds'] for d in basic_data]
    friction_factors = []
    
    # Recalculate friction factors for plotting
    water_pipe = PipeFlow(pipe_length=500.0, pipe_diameter=0.15, roughness=0.046e-3,
                         fluid_density=1000.0, fluid_viscosity=1.002e-3)
    for data in basic_data:
        result = water_pipe.steady_state(data['flow_rate'])
        friction_factors.append(result['friction_factor'])
    
    plt.loglog(reynolds, friction_factors, 'ro-', linewidth=2, markersize=8, label='Calculated Points')
    
    # Add theoretical lines
    re_laminar = np.logspace(2, 3.3, 50)
    f_laminar = 64 / re_laminar
    plt.loglog(re_laminar, f_laminar, 'g--', label='Laminar: f = 64/Re')
    
    plt.xlabel('Reynolds Number')
    plt.ylabel('Friction Factor')
    plt.title('Friction Factor vs Reynolds Number\n(Water in Steel Pipe)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Plot 3: Dynamic Step Response
    ax3 = plt.subplot(2, 3, 3)
    time_min = dynamic_data['time'] / 60  # Convert to minutes
    flow_input_ls = dynamic_data['flow_input'] * 1000  # Convert to L/s
    flow_output_ls = dynamic_data['flow_output'] * 1000
    
    plt.plot(time_min, flow_input_ls, 'r--', linewidth=2, label='Input Flow')
    plt.plot(time_min, flow_output_ls, 'b-', linewidth=2, label='Output Flow')
    plt.axhline(y=15 + 0.63*(25-15), color='gray', linestyle=':', alpha=0.7, label='63% Response')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Flow Rate (L/s)')
    plt.title('Dynamic Step Response\n(Feed Line Control)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(0, 2)
    
    # Plot 4: Roughness Impact on Pressure Loss
    ax4 = plt.subplot(2, 3, 4)
    roughness_values = [d['roughness']*1e6 for d in roughness_data]  # Convert to μm
    pressure_losses = [d['pressure_loss']/1000 for d in roughness_data]  # Convert to kPa
    
    plt.semilogx(roughness_values, pressure_losses, 'mo-', linewidth=2, markersize=8)
    plt.xlabel('Pipe Roughness (μm)')
    plt.ylabel('Pressure Loss (kPa)')
    plt.title('Effect of Pipe Roughness\n(50 L/s Flow Rate)')
    plt.grid(True, alpha=0.3)
    
    # Add condition labels
    for i, d in enumerate(roughness_data):
        if i % 2 == 0:  # Label every other point to avoid crowding
            plt.annotate(d['name'].split()[0], (roughness_values[i], pressure_losses[i]), 
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    # Plot 5: Velocity Profile Comparison
    ax5 = plt.subplot(2, 3, 5)
    flows = [d['flow_rate']*1000 for d in basic_data]  # L/s
    velocities = [d['velocity'] for d in basic_data]    # m/s
    pressures_basic = [d['pressure_loss']/1000 for d in basic_data]  # kPa
    
    ax5_twin = ax5.twinx()
    
    line1 = ax5.plot(flows, velocities, 'b-o', linewidth=2, label='Velocity')
    line2 = ax5_twin.plot(flows, pressures_basic, 'r-s', linewidth=2, label='Pressure Loss')
    
    ax5.set_xlabel('Flow Rate (L/s)')
    ax5.set_ylabel('Velocity (m/s)', color='blue')
    ax5_twin.set_ylabel('Pressure Loss (kPa)', color='red')
    ax5.set_title('Flow Rate vs Velocity & Pressure\n(Water Supply Line)')
    ax5.grid(True, alpha=0.3)
    
    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax5.legend(lines, labels, loc='upper left')
    
    # Plot 6: Flow Regime Classification
    ax6 = plt.subplot(2, 3, 6)
    regimes = [d['regime'] for d in basic_data]
    reynolds_basic = [d['reynolds'] for d in basic_data]
    flows_basic = [d['flow_rate']*1000 for d in basic_data]
    
    # Color code by regime
    colors = {'laminar': 'green', 'transition': 'orange', 'turbulent': 'red'}
    regime_colors = [colors.get(regime, 'gray') for regime in regimes]
    
    scatter = plt.scatter(flows_basic, reynolds_basic, c=regime_colors, s=100, alpha=0.7)
    plt.xlabel('Flow Rate (L/s)')
    plt.ylabel('Reynolds Number')
    plt.title('Flow Regime Classification\n(Re vs Flow Rate)')
    plt.grid(True, alpha=0.3)
    
    # Add regime boundaries
    plt.axhline(y=2300, color='orange', linestyle='--', alpha=0.7, label='Laminar/Transition')
    plt.axhline(y=4000, color='red', linestyle='--', alpha=0.7, label='Transition/Turbulent')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('PipeFlow_example_plots.png', dpi=300, bbox_inches='tight')
    print(f"Saved comprehensive plots to: PipeFlow_example_plots.png")
    
    # Create a second figure for detailed system analysis
    fig2 = plt.figure(figsize=(12, 8))
    
    # Detailed system curve with pump curve overlay
    ax1 = plt.subplot(2, 2, 1)
    flows_detailed = np.array([d['flow'] for d in system_curve]) * 1000  # L/s
    heads_detailed = [d['head'] for d in system_curve]  # m
    
    plt.plot(flows_detailed, heads_detailed, 'b-', linewidth=3, label='System Head Curve')
    
    # Add example pump curve (typical centrifugal pump)
    flow_pump = np.linspace(10, 80, 50)
    head_pump = 25 - 0.003 * flow_pump**2  # Parabolic pump curve
    plt.plot(flow_pump, head_pump, 'r-', linewidth=2, label='Example Pump Curve')
    
    # Find intersection (operating point)
    system_interp = np.interp(flow_pump, flows_detailed, heads_detailed)
    operating_idx = np.argmin(np.abs(head_pump - system_interp))
    operating_flow = flow_pump[operating_idx]
    operating_head = head_pump[operating_idx]
    
    plt.scatter([operating_flow], [operating_head], color='green', s=150, 
                label=f'Operating Point\n({operating_flow:.0f} L/s, {operating_head:.1f} m)', zorder=5)
    
    plt.xlabel('Flow Rate (L/s)')
    plt.ylabel('Head (m)')
    plt.title('System and Pump Curves\n(Acid Transfer System)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Power consumption analysis
    ax2 = plt.subplot(2, 2, 2)
    pump_power = flow_pump * operating_head * 1140 * 9.81 / (3600 * 0.75)  # kW (75% efficiency)
    system_power = flows_detailed / 1000 * np.array(heads_detailed) * 1140 * 9.81 / (1000 * 0.75)
    
    plt.plot(flows_detailed, system_power, 'b-', linewidth=2, label='System Power')
    plt.scatter([operating_flow], [system_power[operating_idx]], color='green', s=100, 
                label=f'Operating Power: {system_power[operating_idx]:.1f} kW')
    plt.xlabel('Flow Rate (L/s)')
    plt.ylabel('Power Consumption (kW)')
    plt.title('Power vs Flow Rate\n(Including 75% Pump Efficiency)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Economic analysis
    ax3 = plt.subplot(2, 2, 3)
    electricity_cost = 0.12  # $/kWh
    operating_hours = 8760   # hours/year
    annual_cost = system_power * electricity_cost * operating_hours
    
    plt.plot(flows_detailed, annual_cost, 'g-', linewidth=2)
    plt.scatter([operating_flow], [annual_cost[operating_idx]], color='red', s=100,
                label=f'Annual Cost: ${annual_cost[operating_idx]:.0f}')
    plt.xlabel('Flow Rate (L/s)')
    plt.ylabel('Annual Energy Cost ($)')
    plt.title('Annual Operating Cost\n(@ $0.12/kWh, 8760 hrs/year)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Time constant analysis
    ax4 = plt.subplot(2, 2, 4)
    pipe_lengths = np.array([50, 100, 200, 300, 500, 1000])  # m
    time_constants = pipe_lengths / 10  # Simplified estimate
    
    plt.plot(pipe_lengths, time_constants, 'purple', linewidth=2, marker='o')
    plt.xlabel('Pipe Length (m)')
    plt.ylabel('Time Constant (s)')
    plt.title('System Response Time\nvs Pipe Length')
    plt.grid(True, alpha=0.3)
    
    # Highlight example cases
    plt.scatter([500], [dynamic_data['time_constant']], color='red', s=100,
                label=f'Example: {dynamic_data["time_constant"]:.1f}s @ 150m')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('PipeFlow_system_analysis.png', dpi=300, bbox_inches='tight')
    print(f"Saved system analysis plots to: PipeFlow_system_analysis.png")
    
    return True

def main():
    """
    Main function to run all PipeFlow examples and create visualizations
    """
    print("PipeFlow Example Suite")
    print("=====================")
    print("Comprehensive demonstration of PipeFlow class capabilities")
    print(f"Timestamp: {np.datetime64('now')}")
    
    try:
        # Run all examples
        example_1_basic_pipe_flow()
        example_2_pump_sizing()
        example_3_dynamic_response()
        example_4_parametric_study()
        
        # Create visualizations
        create_visualizations()
        
        print("\n" + "=" * 60)
        print("EXAMPLE SUITE COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\nGenerated Files:")
        print("- PipeFlow_example_plots.png      : Comprehensive analysis plots")
        print("- PipeFlow_system_analysis.png    : System design and economic analysis")
        print("\nSee PipeFlow_documentation.md for detailed technical background.")
        
    except Exception as e:
        print(f"\nError during example execution: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
