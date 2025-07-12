"""
PlugFlowReactor Example

This example demonstrates the use of the PlugFlowReactor model for simulating
tubular reactors with axial concentration and temperature profiles.

Author: SPROCLIB Development Team
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import sys
import os

# Add the parent directory to sys.path to import from unit.reactor
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from unit.reactor.PlugFlowReactor import PlugFlowReactor


def main():
    """Main function demonstrating PlugFlowReactor model usage."""
    
    print("="*60)
    print("PlugFlowReactor (PFR) Example")
    print("="*60)
    
    # Create PlugFlowReactor instance
    reactor = PlugFlowReactor(
        L=10.0,                # Reactor length [m]
        A_cross=0.1,           # Cross-sectional area [m²]
        n_segments=20,         # Number of segments
        k0=1e8,                # Pre-exponential factor [1/min]
        Ea=60000.0,            # Activation energy [J/mol]
        delta_H=-50000.0,      # Heat of reaction [J/mol]
        U=100.0,               # Heat transfer coefficient [W/m²·K]
        D_tube=0.35,           # Tube diameter [m]
        name="Example_PFR"
    )
    
    print(f"Reactor: {reactor.name}")
    print(f"Length: {reactor.L} m")
    print(f"Cross-sectional area: {reactor.A_cross} m²")
    print(f"Number of segments: {reactor.n_segments}")
    print(f"Segment length: {reactor.dz:.3f} m")
    print()
    
    # Define operating conditions
    operating_conditions = {
        'q': 50.0,             # Flow rate [L/min]
        'CAi': 2.0,            # Inlet concentration [mol/L]
        'Ti': 400.0,           # Inlet temperature [K]
        'Tw': 380.0            # Wall temperature [K]
    }
    
    print("Operating Conditions:")
    for param, value in operating_conditions.items():
        units = {'q': 'L/min', 'CAi': 'mol/L', 'Ti': 'K', 'Tw': 'K'}
        print(f"  {param}: {value} {units[param]}")
    print()
    
    # Input vector for simulation
    u = np.array([operating_conditions[key] for key in ['q', 'CAi', 'Ti', 'Tw']])
    
    # Calculate steady-state profiles
    print("Steady-State Analysis:")
    print("-" * 30)
    
    x_ss = reactor.steady_state(u)
    
    # Extract profiles
    n_seg = reactor.n_segments
    CA_profile = x_ss[:n_seg]
    T_profile = x_ss[n_seg:]
    
    # Axial positions
    z_positions = np.linspace(0, reactor.L, n_seg)
    
    # Calculate performance metrics
    conversion = reactor.calculate_conversion(x_ss)
    residence_time = reactor.V_segment * n_seg / operating_conditions['q']
    superficial_velocity = operating_conditions['q'] / (reactor.A_cross * 60 * 1000)  # m/s
    
    print(f"Overall conversion: {conversion:.1%}")
    print(f"Inlet concentration: {CA_profile[0]:.3f} mol/L")
    print(f"Outlet concentration: {CA_profile[-1]:.3f} mol/L")
    print(f"Inlet temperature: {T_profile[0]:.1f} K")
    print(f"Outlet temperature: {T_profile[-1]:.1f} K")
    print(f"Maximum temperature: {np.max(T_profile):.1f} K")
    print(f"Residence time: {residence_time:.2f} min")
    print(f"Superficial velocity: {superficial_velocity:.4f} m/s")
    print()
    
    # Parametric study - Effect of flow rate
    print("Parametric Study - Flow Rate Effect:")
    print("-" * 40)
    
    flow_rates = [10.0, 25.0, 50.0, 100.0, 200.0]
    conversions = []
    outlet_temps = []
    
    for q_study in flow_rates:
        u_study = u.copy()
        u_study[0] = q_study
        
        try:
            x_study = reactor.steady_state(u_study)
            conv_study = reactor.calculate_conversion(x_study)
            T_out_study = x_study[2*n_seg-1]  # Last temperature
            
            conversions.append(conv_study)
            outlet_temps.append(T_out_study)
            
            print(f"Flow rate: {q_study:6.1f} L/min → Conversion: {conv_study:.1%}, T_out: {T_out_study:.1f} K")
        except:
            conversions.append(0.0)
            outlet_temps.append(operating_conditions['Ti'])
            print(f"Flow rate: {q_study:6.1f} L/min → Calculation failed")
    
    print()
    
    # Parametric study - Effect of wall temperature
    print("Parametric Study - Wall Temperature Effect:")
    print("-" * 45)
    
    wall_temps = [350.0, 370.0, 390.0, 410.0, 430.0]
    wall_conversions = []
    max_temps = []
    
    for Tw_study in wall_temps:
        u_study = u.copy()
        u_study[3] = Tw_study
        
        try:
            x_study = reactor.steady_state(u_study)
            conv_study = reactor.calculate_conversion(x_study)
            T_max_study = np.max(x_study[n_seg:])
            
            wall_conversions.append(conv_study)
            max_temps.append(T_max_study)
            
            print(f"Wall temp: {Tw_study:5.1f} K → Conversion: {conv_study:.1%}, T_max: {T_max_study:.1f} K")
        except:
            wall_conversions.append(0.0)
            max_temps.append(Tw_study)
            print(f"Wall temp: {Tw_study:5.1f} K → Calculation failed")
    
    print()
    
    # Dynamic simulation (startup)
    print("Dynamic Simulation (Startup):")
    print("-" * 30)
    
    # Initial conditions (empty reactor at wall temperature)
    CA_initial = np.zeros(n_seg)
    T_initial = np.full(n_seg, operating_conditions['Tw'])
    x0 = np.concatenate([CA_initial, T_initial])
    
    # Time span for simulation
    t_span = (0, 20)  # 0 to 20 minutes
    t_eval = np.linspace(0, 20, 200)
    
    # Solve ODE
    def pfr_ode(t, x):
        return reactor.dynamics(t, x, u)
    
    sol = solve_ivp(pfr_ode, t_span, x0, t_eval=t_eval, method='RK45', rtol=1e-8)
    
    if sol.success:
        print("Dynamic simulation completed successfully")
        
        time = sol.t
        # Extract outlet conditions over time
        CA_outlet_dynamic = sol.y[n_seg-1, :]  # Last concentration segment
        T_outlet_dynamic = sol.y[2*n_seg-1, :] # Last temperature segment
        
        conversion_dynamic = [(operating_conditions['CAi'] - ca) / operating_conditions['CAi'] 
                            for ca in CA_outlet_dynamic]
        
        print(f"Final outlet concentration: {CA_outlet_dynamic[-1]:.3f} mol/L")
        print(f"Final outlet temperature: {T_outlet_dynamic[-1]:.1f} K")
        print(f"Final conversion: {conversion_dynamic[-1]:.1%}")
        print(f"Time to 95% of steady state: {find_settling_time(time, conversion_dynamic, conversion):.1f} min")
    else:
        print("Dynamic simulation failed")
        return
    
    # Display reactor metadata
    print("\nReactor Model Information:")
    print("-" * 30)
    
    try:
        metadata = reactor.describe()
        print(f"Type: {metadata['type']}")
        print(f"Description: {metadata['description']}")
        print("\nKey Equations:")
        for name, eq in metadata['algorithms'].items():
            print(f"  {name}: {eq}")
        
        print("\nValid Operating Ranges:")
        for param, range_info in metadata['valid_ranges'].items():
            print(f"  {param}: {range_info['min']}-{range_info['max']} {range_info['units']}")
    except AttributeError:
        print("describe() method not available - using basic information")
        print(f"Type: PlugFlowReactor")
        print(f"Description: Tubular reactor with axial discretization")
        print(f"Parameters: L={reactor.L}, n_segments={reactor.n_segments}")
    
    # Create plots
    create_plots(z_positions, CA_profile, T_profile, 
                flow_rates, conversions, outlet_temps,
                wall_temps, wall_conversions, max_temps,
                time, CA_outlet_dynamic, T_outlet_dynamic, conversion_dynamic,
                operating_conditions, reactor)
    
    print("\nExample completed successfully!")
    print("Plots saved as plug_flow_reactor_example_plots.png and plug_flow_reactor_detailed_analysis.png")


def find_settling_time(time, response, steady_value, tolerance=0.05):
    """Find settling time (time to reach within 5% of steady state)."""
    target = abs(steady_value)
    tolerance_band = target * tolerance
    
    for i in range(len(response)-1, 0, -1):
        if abs(response[i] - steady_value) > tolerance_band:
            return time[i+1] if i+1 < len(time) else time[-1]
    
    return time[0]


def create_plots(z_pos, CA_prof, T_prof, flow_rates, conversions, outlet_temps,
                wall_temps, wall_conversions, max_temps, time, CA_dyn, T_dyn, conv_dyn,
                conditions, reactor):
    """Create visualization plots for PlugFlowReactor example."""
    
    # Plot 1: Axial profiles and parametric studies
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Axial concentration profile
    ax1.plot(z_pos, CA_prof, 'b-', linewidth=2, marker='o', markersize=4)
    ax1.set_xlabel('Axial Position (m)')
    ax1.set_ylabel('Concentration (mol/L)')
    ax1.set_title('PFR Concentration Profile')
    ax1.grid(True, alpha=0.3)
    
    # Axial temperature profile
    ax2.plot(z_pos, T_prof, 'r-', linewidth=2, marker='s', markersize=4)
    ax2.axhline(y=conditions['Tw'], color='orange', linestyle='--', alpha=0.7, label='Wall Temp')
    ax2.set_xlabel('Axial Position (m)')
    ax2.set_ylabel('Temperature (K)')
    ax2.set_title('PFR Temperature Profile')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Flow rate effect on conversion
    ax3.plot(flow_rates, conversions, 'g-', linewidth=2, marker='o', markersize=6)
    ax3.set_xlabel('Flow Rate (L/min)')
    ax3.set_ylabel('Conversion (-)')
    ax3.set_title('Effect of Flow Rate on Conversion')
    ax3.grid(True, alpha=0.3)
    
    # Wall temperature effect
    ax4.plot(wall_temps, wall_conversions, 'purple', linewidth=2, marker='s', markersize=6)
    ax4.set_xlabel('Wall Temperature (K)')
    ax4.set_ylabel('Conversion (-)')
    ax4.set_title('Effect of Wall Temperature')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plug_flow_reactor_example_plots.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 2: Dynamic response and detailed analysis
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Dynamic outlet concentration
    ax1.plot(time, CA_dyn, 'b-', linewidth=2)
    ax1.axhline(y=CA_prof[-1], color='blue', linestyle='--', alpha=0.7, label='Steady State')
    ax1.set_xlabel('Time (min)')
    ax1.set_ylabel('Outlet Concentration (mol/L)')
    ax1.set_title('PFR Startup - Outlet Concentration')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Dynamic outlet temperature
    ax2.plot(time, T_dyn, 'r-', linewidth=2)
    ax2.axhline(y=T_prof[-1], color='red', linestyle='--', alpha=0.7, label='Steady State')
    ax2.set_xlabel('Time (min)')
    ax2.set_ylabel('Outlet Temperature (K)')
    ax2.set_title('PFR Startup - Outlet Temperature')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Dynamic conversion
    ax3.plot(time, conv_dyn, 'g-', linewidth=2)
    ax3.axhline(y=reactor.calculate_conversion(np.concatenate([CA_prof, T_prof])), 
                color='green', linestyle='--', alpha=0.7, label='Steady State')
    ax3.set_xlabel('Time (min)')
    ax3.set_ylabel('Conversion (-)')
    ax3.set_title('PFR Startup - Conversion')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # Flow rate vs outlet temperature
    ax4.plot(flow_rates, outlet_temps, 'orange', linewidth=2, marker='d', markersize=6)
    ax4.set_xlabel('Flow Rate (L/min)')
    ax4.set_ylabel('Outlet Temperature (K)')
    ax4.set_title('Flow Rate Effect on Outlet Temperature')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plug_flow_reactor_detailed_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    main()
