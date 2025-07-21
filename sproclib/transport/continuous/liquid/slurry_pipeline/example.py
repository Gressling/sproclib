#!/usr/bin/env python3
"""
SlurryPipeline Example Usage - Comprehensive Demonstration

This example demonstrates the capabilities of the SlurryPipeline class for modeling
solid-liquid slurry transport systems. It covers mining applications, critical velocity
analysis, settling behavior, and operational optimization.

Based on: SlurryPipeline_documentation.md
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from .slurry_pipeline import SlurryPipeline
except ImportError:
    print("Error: Could not import SlurryPipeline. Make sure SlurryPipeline.py is in the current directory.")
    sys.exit(1)

def example_1_mining_ore_transport():
    """
    Example 1: Mining ore slurry transport system
    
    Scenario: Copper ore concentrate pipeline from processing plant to port
    - Long-distance transport (50 km)
    - High concentration slurry (35% solids)
    - Economic optimization critical
    """
    print("=" * 60)
    print("EXAMPLE 1: Mining Ore Transport Pipeline")
    print("=" * 60)
    
    # Create mining slurry pipeline
    ore_pipeline = SlurryPipeline(
        pipe_length=50000.0,        # 50 km pipeline
        pipe_diameter=0.6,          # 60 cm diameter (large industrial)
        solid_concentration=0.35,   # 35% solids by volume
        particle_diameter=0.15e-3,  # 150 micron average particles
        fluid_density=1000.0,       # Water carrier
        solid_density=4200.0,       # Copper ore density
        fluid_viscosity=1.2e-3,     # Slightly higher due to fines
        flow_nominal=0.8,           # 800 L/s design flow
        name="CopperOreTransportPipeline"
    )
    
    # Display system information
    print("\nPipeline Configuration:")
    info = ore_pipeline.describe()
    print(f"Application: Mining Ore Transport")
    print(f"Pipeline Length: {ore_pipeline.pipe_length/1000:.0f} km")
    print(f"Pipe Diameter: {ore_pipeline.pipe_diameter*100:.0f} cm")
    print(f"Solids Concentration: {ore_pipeline.solid_concentration*100:.0f}% by volume")
    print(f"Particle Size: {ore_pipeline.particle_diameter*1e6:.0f} microns")
    
    # Calculate mixture properties using proper inputs [P_inlet, flow_rate, c_solid_in]
    inputs = np.array([500000.0, ore_pipeline.flow_nominal, ore_pipeline.solid_concentration])  # 500 kPa inlet pressure
    result_nominal = ore_pipeline.steady_state(inputs)
    p_outlet = result_nominal[0]  # Pa
    c_solid_out = result_nominal[1]  # solid concentration out
    
    # Calculate derived properties
    mixture_density = ore_pipeline.fluid_density * (1 - ore_pipeline.solid_concentration) + ore_pipeline.solid_density * ore_pipeline.solid_concentration
    velocity = ore_pipeline.flow_nominal / (np.pi * (ore_pipeline.pipe_diameter/2)**2)
    
    print(f"\nMixture Properties:")
    print(f"Mixture Density: {mixture_density:.0f} kg/m³")
    print(f"Solids Loading: {ore_pipeline.solid_concentration * ore_pipeline.solid_density:.0f} kg/m³")
    print(f"Water Content: {(1-ore_pipeline.solid_concentration)*100:.0f}% by volume")
    
    # Critical velocity analysis (simplified)
    # Durand critical velocity approximation
    critical_velocity = 1.5 * np.sqrt(2 * 9.81 * ore_pipeline.particle_diameter * (ore_pipeline.solid_density/ore_pipeline.fluid_density - 1))
    design_velocity = velocity
    
    print(f"\nCritical Velocity Analysis:")
    print(f"Critical Velocity: {critical_velocity:.2f} m/s")
    print(f"Design Velocity: {design_velocity:.2f} m/s")
    print(f"Safety Factor: {design_velocity/critical_velocity:.2f}")
    flow_regime = "Turbulent" if design_velocity > critical_velocity else "Laminar"
    print(f"Flow Regime: {flow_regime}")
    
    if design_velocity > critical_velocity:
        print("✓ Design velocity exceeds critical - particles will remain suspended")
    else:
        print("⚠ WARNING: Design velocity below critical - settling may occur")
    
    # Flow rate vs pressure analysis
    flow_rates = np.linspace(0.4, 1.2, 10)  # 400-1200 L/s range
    
    print(f"\nFlow Rate Performance Analysis:")
    print("Flow Rate | Velocity | Critical | Safety | Pressure | Flow")
    print("(L/s)     | (m/s)    | Vel(m/s) | Factor | (MPa)    | Regime")
    print("-" * 70)
    
    transport_data = []
    for flow in flow_rates:
        result = ore_pipeline.steady_state(flow)
        
        flow_ls = flow * 1000
        velocity = result['velocity']
        critical_vel = result['critical_velocity']
        safety_factor = velocity / critical_vel
        pressure_mpa = result['pressure_loss'] / 1e6
        regime = result['flow_regime']
        
        print(f"{flow_ls:8.0f}  | {velocity:7.2f}  | {critical_vel:7.2f}  | {safety_factor:6.2f} | {pressure_mpa:7.1f}  | {regime}")
        
        transport_data.append({
            'flow_rate': flow,
            'velocity': velocity,
            'critical_velocity': critical_vel,
            'safety_factor': safety_factor,
            'pressure_loss': result['pressure_loss'],
            'regime': regime
        })
    
    # Economic analysis
    electricity_cost = 0.08  # $/kWh (industrial rate)
    pump_efficiency = 0.80   # 80% overall efficiency
    operating_hours = 8000   # hours per year
    
    print(f"\nEconomic Analysis (Design Flow = {ore_pipeline.flow_nominal*1000:.0f} L/s):")
    
    design_result = ore_pipeline.steady_state(ore_pipeline.flow_nominal)
    hydraulic_power = design_result['pressure_loss'] * ore_pipeline.flow_nominal / 1000  # kW
    electrical_power = hydraulic_power / pump_efficiency
    annual_energy_cost = electrical_power * electricity_cost * operating_hours
    
    print(f"Hydraulic Power Required: {hydraulic_power:.0f} kW")
    print(f"Electrical Power (80% eff): {electrical_power:.0f} kW")
    print(f"Annual Energy Cost: ${annual_energy_cost:,.0f}")
    print(f"Energy per Ton Transported: {electrical_power/(flow*mixture_density*3.6):.2f} kWh/tonne")
    
    return transport_data

def example_2_dredging_operations():
    """
    Example 2: Marine dredging slurry transport
    
    Scenario: Harbor deepening project with sand/silt transport
    - Variable particle sizes
    - High water content
    - Floating pipeline sections
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Marine Dredging Operations")
    print("=" * 60)
    
    # Dredging slurry pipeline
    dredge_pipeline = SlurryPipeline(
        pipe_length=2000.0,         # 2 km floating pipeline
        pipe_diameter=0.8,          # 80 cm diameter (large dredge)
        solid_concentration=0.15,   # 15% solids (high water content)
        particle_diameter=0.5e-3,   # 500 micron sand particles
        fluid_density=1025.0,       # Seawater carrier
        solid_density=2650.0,       # Sand/silt density
        fluid_viscosity=1.1e-3,     # Seawater viscosity
        flow_nominal=2.0,           # 2000 L/s dredge capacity
        name="DredgingSlurryPipeline"
    )
    
    print("\nDredging System Configuration:")
    print(f"Pipeline Type: Floating HDPE")
    print(f"Pipeline Length: {dredge_pipeline.pipe_length/1000:.1f} km")
    print(f"Dredge Material: Sand/Silt mixture")
    print(f"Carrier Fluid: Seawater")
    print(f"Solids Concentration: {dredge_pipeline.solid_concentration*100:.0f}% by volume")
    
    # Particle settling analysis
    result = dredge_pipeline.steady_state(dredge_pipeline.flow_nominal)
    settling_velocity = result['settling_velocity']
    
    print(f"\nSettling Analysis:")
    print(f"Particle Settling Velocity: {settling_velocity*1000:.1f} mm/s")
    print(f"Critical Velocity: {result['critical_velocity']:.2f} m/s")
    print(f"Operating Velocity: {result['velocity']:.2f} m/s")
    
    # Time to settle pipeline diameter
    settle_time = dredge_pipeline.pipe_diameter / settling_velocity
    print(f"Time to Settle Pipe Diameter: {settle_time/60:.1f} minutes")
    
    # Effect of concentration on transport
    concentrations = np.array([0.05, 0.10, 0.15, 0.20, 0.25, 0.30])  # 5-30% solids
    
    print(f"\nConcentration Effects Analysis:")
    print("Solids | Mixture | Critical | Pressure | Production")
    print("Conc(%) | Density | Vel(m/s) | Loss(kPa)| Rate(t/h)")
    print("-" * 50)
    
    concentration_data = []
    for conc in concentrations:
        test_pipeline = SlurryPipeline(
            pipe_length=dredge_pipeline.pipe_length,
            pipe_diameter=dredge_pipeline.pipe_diameter,
            solid_concentration=conc,
            particle_diameter=dredge_pipeline.particle_diameter,
            fluid_density=dredge_pipeline.fluid_density,
            solid_density=dredge_pipeline.solid_density,
            fluid_viscosity=dredge_pipeline.fluid_viscosity
        )
        
        result = test_pipeline.steady_state(dredge_pipeline.flow_nominal)
        
        conc_percent = conc * 100
        mix_density = result['mixture_density']
        critical_vel = result['critical_velocity']
        pressure_kpa = result['pressure_loss'] / 1000
        
        # Production rate (tonnes of solids per hour)
        solids_flow = dredge_pipeline.flow_nominal * conc * dredge_pipeline.solid_density  # kg/s
        production_tph = solids_flow * 3.6  # t/h
        
        print(f"{conc_percent:6.0f} | {mix_density:6.0f}  | {critical_vel:7.2f}  | {pressure_kpa:8.0f} | {production_tph:8.0f}")
        
        concentration_data.append({
            'concentration': conc,
            'mixture_density': mix_density,
            'critical_velocity': critical_vel,
            'pressure_loss': result['pressure_loss'],
            'production_rate': production_tph
        })
    
    # Optimal concentration analysis
    optimal_idx = np.argmax([d['production_rate'] for d in concentration_data])
    optimal_conc = concentration_data[optimal_idx]
    
    print(f"\nOptimal Operating Point:")
    print(f"Concentration: {optimal_conc['concentration']*100:.0f}% solids")
    print(f"Production Rate: {optimal_conc['production_rate']:.0f} tonnes/hour")
    print(f"Pressure Loss: {optimal_conc['pressure_loss']/1000:.0f} kPa")
    
    return concentration_data

def example_3_wastewater_sludge():
    """
    Example 3: Wastewater treatment sludge transport
    
    Scenario: Thickened sludge transport from clarifiers to digesters
    - High viscosity biological sludge
    - Non-Newtonian behavior approximation
    - Shorter pipeline distances
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Wastewater Sludge Transport")
    print("=" * 60)
    
    # Sludge transport pipeline
    sludge_pipeline = SlurryPipeline(
        pipe_length=800.0,          # 800 m within treatment plant
        pipe_diameter=0.3,          # 30 cm diameter
        solid_concentration=0.08,   # 8% solids (thickened sludge)
        particle_diameter=50e-6,    # 50 micron bio-particles
        fluid_density=1000.0,       # Water-based
        solid_density=1050.0,       # Low-density biological solids
        fluid_viscosity=5e-3,       # High viscosity due to bio-polymers
        flow_nominal=0.1,           # 100 L/s
        name="SludgeTransportPipeline"
    )
    
    print("\nSludge Transport System:")
    print(f"Application: Activated Sludge WTP")
    print(f"Pipeline Route: Clarifier → Thickener → Digester")
    print(f"Sludge Type: Thickened biological sludge")
    print(f"Solids Content: {sludge_pipeline.solid_concentration*100:.0f}% by weight (approx)")
    print(f"Carrier Viscosity: {sludge_pipeline.fluid_viscosity*1000:.0f} mPa·s")
    
    # Calculate sludge properties
    result = sludge_pipeline.steady_state(sludge_pipeline.flow_nominal)
    
    print(f"\nSludge Transport Analysis:")
    print(f"Pipeline Reynolds Number: {result['reynolds_number']:.0f}")
    print(f"Flow Regime: {result['flow_regime']}")
    print(f"Mixture Density: {result['mixture_density']:.0f} kg/m³")
    
    # Due to low density difference, settling is minimal
    settling_vel = result['settling_velocity']
    print(f"Settling Velocity: {settling_vel*1e6:.1f} μm/s (very low)")
    
    # Flow rate vs pumping requirements
    flow_rates = np.linspace(0.05, 0.2, 8)  # 50-200 L/s
    
    print(f"\nPumping Requirements Analysis:")
    print("Flow Rate | Velocity | Reynolds | Pressure | Pump Power")
    print("(L/s)     | (m/s)    | Number   | (kPa)    | (kW)")
    print("-" * 55)
    
    sludge_data = []
    for flow in flow_rates:
        result = sludge_pipeline.steady_state(flow)
        
        flow_ls = flow * 1000
        velocity = result['velocity']
        reynolds = result['reynolds_number']
        pressure_kpa = result['pressure_loss'] / 1000
        
        # Pump power (assume 70% efficiency for positive displacement)
        pump_power = result['pressure_loss'] * flow / (1000 * 0.70)
        
        print(f"{flow_ls:8.0f}  | {velocity:7.2f}  | {reynolds:7.0f}  | {pressure_kpa:7.0f}  | {pump_power:8.2f}")
        
        sludge_data.append({
            'flow_rate': flow,
            'velocity': velocity,
            'reynolds': reynolds,
            'pressure_loss': result['pressure_loss'],
            'pump_power': pump_power
        })
    
    # Viscosity effects analysis
    viscosities = np.array([1e-3, 2e-3, 5e-3, 10e-3, 20e-3])  # 1-20 mPa·s
    
    print(f"\nViscosity Effects (Flow = {sludge_pipeline.flow_nominal*1000:.0f} L/s):")
    print("Viscosity | Reynolds | Friction | Pressure")
    print("(mPa·s)   | Number   | Factor   | Loss(kPa)")
    print("-" * 40)
    
    for viscosity in viscosities:
        test_pipeline = SlurryPipeline(
            pipe_length=sludge_pipeline.pipe_length,
            pipe_diameter=sludge_pipeline.pipe_diameter,
            solid_concentration=sludge_pipeline.solid_concentration,
            particle_diameter=sludge_pipeline.particle_diameter,
            fluid_density=sludge_pipeline.fluid_density,
            solid_density=sludge_pipeline.solid_density,
            fluid_viscosity=viscosity
        )
        
        result = test_pipeline.steady_state(sludge_pipeline.flow_nominal)
        
        visc_mpas = viscosity * 1000
        reynolds = result['reynolds_number']
        # Estimate friction factor from Reynolds number
        if reynolds < 2300:
            friction_factor = 64 / reynolds
        else:
            friction_factor = 0.079 / (reynolds**0.25)  # Blasius approximation
        
        pressure_kpa = result['pressure_loss'] / 1000
        
        print(f"{visc_mpas:8.0f}  | {reynolds:7.0f}  | {friction_factor:7.4f}  | {pressure_kpa:8.0f}")
    
    return sludge_data

def example_4_startup_shutdown():
    """
    Example 4: Pipeline startup and shutdown dynamics
    
    Scenario: Coal slurry pipeline startup sequence
    - Dynamic analysis of flow establishment
    - Settling prevention during transients
    - Operational procedures
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Pipeline Startup/Shutdown Dynamics")
    print("=" * 60)
    
    # Coal slurry pipeline
    coal_pipeline = SlurryPipeline(
        pipe_length=15000.0,        # 15 km coal transport
        pipe_diameter=0.4,          # 40 cm diameter
        solid_concentration=0.45,   # 45% solids (concentrated coal)
        particle_diameter=0.3e-3,   # 300 micron coal particles
        fluid_density=1000.0,       # Water carrier
        solid_density=1300.0,       # Coal density (relatively low)
        fluid_viscosity=1.8e-3,     # Higher viscosity due to coal fines
        flow_nominal=0.3,           # 300 L/s design flow
        name="CoalSlurryPipeline"
    )
    
    print("\nCoal Slurry Pipeline:")
    print(f"Application: Coal preparation plant to port")
    print(f"Pipeline Length: {coal_pipeline.pipe_length/1000:.0f} km")
    print(f"Coal Concentration: {coal_pipeline.solid_concentration*100:.0f}% by volume")
    print(f"Design Flow Rate: {coal_pipeline.flow_nominal*1000:.0f} L/s")
    
    # Startup sequence analysis
    dt = 10.0  # 10 second time steps
    t_total = 3600  # 1 hour simulation
    time_points = np.arange(0, t_total, dt)
    n_points = len(time_points)
    
    # Startup flow profile: gradual increase to prevent settling
    startup_time = 1800  # 30 minutes to reach full flow
    flow_profile = np.zeros(n_points)
    
    for i, t in enumerate(time_points):
        if t < startup_time:
            # Gradual ramp-up
            flow_profile[i] = coal_pipeline.flow_nominal * (t / startup_time)
        else:
            # Steady operation
            flow_profile[i] = coal_pipeline.flow_nominal
    
    print(f"\nStartup Sequence Analysis:")
    print(f"Startup Duration: {startup_time/60:.0f} minutes")
    
    # Critical velocity monitoring during startup
    critical_result = coal_pipeline.steady_state(coal_pipeline.flow_nominal)
    critical_velocity = critical_result['critical_velocity']
    
    print(f"Critical Velocity: {critical_velocity:.2f} m/s")
    
    # Find minimum safe flow rate
    flow_test = np.linspace(0.1, 0.5, 20)
    for flow in flow_test:
        result = coal_pipeline.steady_state(flow)
        if result['velocity'] >= critical_velocity:
            min_safe_flow = flow
            break
    
    print(f"Minimum Safe Flow: {min_safe_flow*1000:.0f} L/s")
    print(f"Minimum Safe Velocity: {coal_pipeline.steady_state(min_safe_flow)['velocity']:.2f} m/s")
    
    # Dynamic simulation
    print(f"\nDynamic Startup Simulation:")
    print("Time   | Flow Rate | Velocity | Safety | Status")
    print("(min)  | (L/s)     | (m/s)    | Factor |")
    print("-" * 45)
    
    startup_data = []
    for i, t in enumerate(time_points[::18]):  # Sample every 3 minutes
        flow = flow_profile[i*18]
        
        if flow > 0.01:  # Avoid zero flow calculations
            result = coal_pipeline.dynamics(flow, dt)
            velocity = result['velocity']
            safety_factor = velocity / critical_velocity
            
            if safety_factor >= 1.0:
                status = "Safe"
            elif safety_factor >= 0.8:
                status = "Caution"
            else:
                status = "Risk"
        else:
            velocity = 0
            safety_factor = 0
            status = "Stopped"
        
        time_min = t / 60
        flow_ls = flow * 1000
        
        print(f"{time_min:5.0f}  | {flow_ls:8.0f}  | {velocity:7.2f}  | {safety_factor:6.2f} | {status}")
        
        startup_data.append({
            'time': t,
            'flow_rate': flow,
            'velocity': velocity,
            'safety_factor': safety_factor,
            'status': status
        })
    
    # Shutdown analysis
    print(f"\nShutdown Procedure Analysis:")
    
    # Calculate pipeline volume and flush requirements
    pipe_volume = np.pi * (coal_pipeline.pipe_diameter/2)**2 * coal_pipeline.pipe_length
    slurry_volume = pipe_volume * coal_pipeline.solid_concentration
    
    print(f"Total Pipeline Volume: {pipe_volume:.0f} m³")
    print(f"Slurry Volume to Clear: {slurry_volume:.0f} m³")
    
    # Flush water requirements
    flush_velocity = critical_velocity * 1.2  # 20% above critical
    flush_flow = flush_velocity * np.pi * (coal_pipeline.pipe_diameter/2)**2
    flush_time = pipe_volume / flush_flow
    
    print(f"Recommended Flush Velocity: {flush_velocity:.2f} m/s")
    print(f"Flush Flow Rate Required: {flush_flow*1000:.0f} L/s")
    print(f"Estimated Flush Time: {flush_time/60:.0f} minutes")
    
    return startup_data

def create_visualizations():
    """
    Create comprehensive visualization plots for slurry pipeline examples
    """
    print("\n" + "=" * 60)
    print("CREATING VISUALIZATION PLOTS")
    print("=" * 60)
    
    # Run examples to get data
    mining_data = example_1_mining_ore_transport()
    dredging_data = example_2_dredging_operations()
    sludge_data = example_3_wastewater_sludge()
    startup_data = example_4_startup_shutdown()
    
    # Create comprehensive figure
    fig = plt.figure(figsize=(16, 12))
    
    # Plot 1: Mining Pipeline - Safety Factor vs Flow Rate
    ax1 = plt.subplot(2, 3, 1)
    flows_mining = [d['flow_rate']*1000 for d in mining_data]  # L/s
    safety_factors = [d['safety_factor'] for d in mining_data]
    
    plt.plot(flows_mining, safety_factors, 'bo-', linewidth=2, markersize=8)
    plt.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Critical Limit')
    plt.axhline(y=1.2, color='orange', linestyle='--', alpha=0.7, label='Recommended Min')
    
    # Color code safe/unsafe regions
    plt.fill_between(flows_mining, 0, 1, alpha=0.2, color='red', label='Unsafe Region')
    plt.fill_between(flows_mining, 1, 1.2, alpha=0.2, color='orange', label='Caution Zone')
    plt.fill_between(flows_mining, 1.2, max(safety_factors), alpha=0.2, color='green', label='Safe Operation')
    
    plt.xlabel('Flow Rate (L/s)')
    plt.ylabel('Safety Factor (V/V_critical)')
    plt.title('Mining Pipeline Safety Analysis\n(50 km Copper Ore Transport)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Plot 2: Dredging - Concentration vs Production Rate
    ax2 = plt.subplot(2, 3, 2)
    concentrations = [d['concentration']*100 for d in dredging_data]
    production_rates = [d['production_rate'] for d in dredging_data]
    
    plt.plot(concentrations, production_rates, 'go-', linewidth=2, markersize=8)
    
    # Find and mark optimal point
    max_idx = np.argmax(production_rates)
    plt.scatter([concentrations[max_idx]], [production_rates[max_idx]], 
                color='red', s=150, label=f'Optimal: {concentrations[max_idx]:.0f}%', zorder=5)
    
    plt.xlabel('Solids Concentration (%)')
    plt.ylabel('Production Rate (tonnes/hour)')
    plt.title('Dredging Operations\nConcentration Optimization')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Plot 3: Sludge Transport - Viscosity Effects
    ax3 = plt.subplot(2, 3, 3)
    flows_sludge = [d['flow_rate']*1000 for d in sludge_data]
    pump_powers = [d['pump_power'] for d in sludge_data]
    
    plt.plot(flows_sludge, pump_powers, 'mo-', linewidth=2, markersize=8)
    plt.xlabel('Flow Rate (L/s)')
    plt.ylabel('Pump Power (kW)')
    plt.title('Sludge Transport\nPower Requirements')
    plt.grid(True, alpha=0.3)
    
    # Add efficiency curve
    flows_array = np.array(flows_sludge)
    power_array = np.array(pump_powers)
    efficiency_curve = flows_array / power_array  # L/s per kW
    
    ax3_twin = ax3.twinx()
    ax3_twin.plot(flows_sludge, efficiency_curve, 'r--', alpha=0.7, label='Efficiency')
    ax3_twin.set_ylabel('Transport Efficiency (L/s/kW)', color='red')
    
    # Plot 4: Startup Dynamics
    ax4 = plt.subplot(2, 3, 4)
    startup_times = [d['time']/60 for d in startup_data]  # Convert to minutes
    startup_flows = [d['flow_rate']*1000 for d in startup_data]  # L/s
    startup_safety = [d['safety_factor'] for d in startup_data]
    
    ax4_flow = ax4.twinx()
    
    line1 = ax4.plot(startup_times, startup_safety, 'b-', linewidth=3, label='Safety Factor')
    line2 = ax4_flow.plot(startup_times, startup_flows, 'g-', linewidth=2, label='Flow Rate')
    
    ax4.axhline(y=1.0, color='red', linestyle='--', alpha=0.7)
    ax4.set_xlabel('Time (minutes)')
    ax4.set_ylabel('Safety Factor', color='blue')
    ax4_flow.set_ylabel('Flow Rate (L/s)', color='green')
    ax4.set_title('Coal Pipeline Startup\nDynamics')
    ax4.grid(True, alpha=0.3)
    
    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax4.legend(lines, labels, loc='center right')
    
    # Plot 5: Pressure Loss Comparison
    ax5 = plt.subplot(2, 3, 5)
    
    # Compare pressure losses for different applications
    applications = ['Mining\nOre', 'Dredging\nSand', 'Sludge\nTransport']
    
    # Calculate representative pressure losses (normalized per km)
    mining_pressure = mining_data[5]['pressure_loss'] / 50000 * 1000 / 1000  # kPa/km
    dredging_pressure = dredging_data[2]['pressure_loss'] / 2000 * 1000 / 1000  # kPa/km
    sludge_pressure = sludge_data[2]['pressure_loss'] / 800 * 1000 / 1000  # kPa/km
    
    pressures = [mining_pressure, dredging_pressure, sludge_pressure]
    colors = ['brown', 'blue', 'green']
    
    bars = plt.bar(applications, pressures, color=colors, alpha=0.7, edgecolor='black')
    
    # Add concentration labels
    concentrations_label = ['35%', '15%', '8%']
    for bar, conc in zip(bars, concentrations_label):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{conc} solids', ha='center', va='bottom', fontweight='bold')
    
    plt.ylabel('Pressure Loss (kPa/km)')
    plt.title('Pressure Loss Comparison\n(Normalized per km)')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Plot 6: Particle Size Effects
    ax6 = plt.subplot(2, 3, 6)
    
    # Simulate different particle sizes
    particle_sizes = np.array([50, 100, 200, 500, 1000, 2000])  # microns
    critical_velocities = []
    settling_velocities = []
    
    base_pipeline = SlurryPipeline(
        pipe_length=1000, pipe_diameter=0.3, solid_concentration=0.2,
        particle_diameter=100e-6, fluid_density=1000, solid_density=2500,
        fluid_viscosity=1e-3, flow_nominal=0.1
    )
    
    for size_um in particle_sizes:
        size_m = size_um * 1e-6
        test_pipeline = SlurryPipeline(
            pipe_length=base_pipeline.pipe_length,
            pipe_diameter=base_pipeline.pipe_diameter,
            solid_concentration=base_pipeline.solid_concentration,
            particle_diameter=size_m,
            fluid_density=base_pipeline.fluid_density,
            solid_density=base_pipeline.solid_density,
            fluid_viscosity=base_pipeline.fluid_viscosity
        )
        
        result = test_pipeline.steady_state(base_pipeline.flow_nominal)
        critical_velocities.append(result['critical_velocity'])
        settling_velocities.append(result['settling_velocity']*1000)  # mm/s
    
    ax6_twin = ax6.twinx()
    
    line1 = ax6.semilogx(particle_sizes, critical_velocities, 'ro-', linewidth=2, label='Critical Velocity')
    line2 = ax6_twin.semilogx(particle_sizes, settling_velocities, 'bs-', linewidth=2, label='Settling Velocity')
    
    ax6.set_xlabel('Particle Size (μm)')
    ax6.set_ylabel('Critical Velocity (m/s)', color='red')
    ax6_twin.set_ylabel('Settling Velocity (mm/s)', color='blue')
    ax6.set_title('Particle Size Effects\non Transport Properties')
    ax6.grid(True, alpha=0.3)
    
    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax6.legend(lines, labels, loc='upper left')
    
    plt.tight_layout()
    plt.savefig('SlurryPipeline_example_plots.png', dpi=300, bbox_inches='tight')
    print(f"Saved comprehensive plots to: SlurryPipeline_example_plots.png")
    
    # Create detailed analysis figure
    fig2 = plt.figure(figsize=(14, 10))
    
    # Flow regime map
    ax1 = plt.subplot(2, 2, 1)
    
    # Create flow regime map
    velocities = np.linspace(0.5, 4.0, 50)
    concentrations_map = np.linspace(0.05, 0.5, 50)
    V, C = np.meshgrid(velocities, concentrations_map)
    
    # Simplified flow regime classification
    # Critical velocity approximation: v_c ∝ √(concentration)
    critical_vel_map = 1.5 * np.sqrt(C)
    
    regime_map = np.zeros_like(V)
    regime_map[V < 0.8 * critical_vel_map] = 0  # Deposited
    regime_map[(V >= 0.8 * critical_vel_map) & (V < critical_vel_map)] = 1  # Moving bed
    regime_map[(V >= critical_vel_map) & (V < 1.5 * critical_vel_map)] = 2  # Heterogeneous
    regime_map[V >= 1.5 * critical_vel_map] = 3  # Homogeneous
    
    colors = ['red', 'orange', 'yellow', 'green']
    labels = ['Deposited', 'Moving Bed', 'Heterogeneous', 'Homogeneous']
    
    contour = plt.contourf(V, C*100, regime_map, levels=[0, 1, 2, 3, 4], colors=colors, alpha=0.7)
    
    # Add example operating points
    plt.scatter([2.5], [35], color='blue', s=100, label='Mining (Ore)', zorder=5)
    plt.scatter([3.0], [15], color='cyan', s=100, label='Dredging (Sand)', zorder=5)
    plt.scatter([1.2], [8], color='purple', s=100, label='Sludge (Bio)', zorder=5)
    
    plt.xlabel('Velocity (m/s)')
    plt.ylabel('Solids Concentration (%)')
    plt.title('Slurry Flow Regime Map')
    plt.legend()
    
    # Add colorbar for regimes
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=colors[i], label=labels[i]) for i in range(4)]
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.3, 1))
    
    # Economic optimization
    ax2 = plt.subplot(2, 2, 2)
    
    # Cost analysis for mining pipeline
    flow_rates_econ = np.linspace(400, 1200, 20)  # L/s
    pipe_diameters = [0.4, 0.5, 0.6, 0.7, 0.8]  # m
    
    total_costs = []
    for diameter in pipe_diameters:
        diameter_costs = []
        for flow_ls in flow_rates_econ:
            flow = flow_ls / 1000  # m³/s
            
            # Create pipeline with this diameter
            test_pipeline = SlurryPipeline(
                pipe_length=50000, pipe_diameter=diameter, solid_concentration=0.35,
                particle_diameter=0.15e-3, fluid_density=1000, solid_density=4200,
                fluid_viscosity=1.2e-3
            )
            
            result = test_pipeline.steady_state(flow)
            
            # Capital cost (proportional to diameter²)
            capital_cost = diameter**2 * 50000 * 1000  # $/km * km
            
            # Operating cost (energy)
            power_kw = result['pressure_loss'] * flow / (1000 * 0.8)  # 80% efficiency
            annual_energy_cost = power_kw * 0.08 * 8000  # $/kWh * h/year
            
            # Total annualized cost (capital/20 years + operating)
            total_annual_cost = capital_cost / 20 + annual_energy_cost
            diameter_costs.append(total_annual_cost / 1e6)  # M$/year
        
        total_costs.append(diameter_costs)
        plt.plot(flow_rates_econ, diameter_costs, 'o-', linewidth=2, 
                label=f'D = {diameter*100:.0f} cm')
    
    plt.xlabel('Flow Rate (L/s)')
    plt.ylabel('Total Annual Cost (M$/year)')
    plt.title('Economic Optimization\n(50 km Mining Pipeline)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Settling time analysis
    ax3 = plt.subplot(2, 2, 3)
    
    particle_sizes_detailed = np.logspace(1, 4, 50)  # 10-10000 microns
    pipe_diameters_settle = [0.2, 0.4, 0.6, 0.8, 1.0]  # m
    
    for pipe_d in pipe_diameters_settle:
        settling_times = []
        for size_um in particle_sizes_detailed:
            # Simplified Stokes settling
            size_m = size_um * 1e-6
            settling_vel = (2500 - 1000) * 9.81 * size_m**2 / (18 * 1e-3)  # m/s
            settle_time = pipe_d / settling_vel / 3600  # hours
            settling_times.append(settle_time)
        
        plt.loglog(particle_sizes_detailed, settling_times, linewidth=2, 
                  label=f'D = {pipe_d*100:.0f} cm')
    
    plt.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='1 hour')
    plt.axhline(y=24, color='orange', linestyle='--', alpha=0.7, label='1 day')
    
    plt.xlabel('Particle Size (μm)')
    plt.ylabel('Time to Settle Pipe Diameter (hours)')
    plt.title('Particle Settling Analysis\n(Time to Bottom)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Concentration profile
    ax4 = plt.subplot(2, 2, 4)
    
    # Simplified concentration profile in vertical pipe
    heights = np.linspace(0, 1, 100)  # Normalized height (0=bottom, 1=top)
    
    # Different particle sizes
    particle_sizes_profile = [50, 200, 500, 1000]  # microns
    
    for size_um in particle_sizes_profile:
        # Rouse profile approximation
        settling_vel = (2500 - 1000) * 9.81 * (size_um*1e-6)**2 / (18 * 1e-3)
        rouse_number = settling_vel / (0.4 * 0.1)  # κ * u*
        
        if rouse_number < 10:  # Avoid numerical issues
            concentration_profile = ((1 - heights) / heights)**rouse_number
            concentration_profile = concentration_profile / concentration_profile[0]  # Normalize
            plt.plot(concentration_profile, heights, linewidth=2, label=f'{size_um} μm')
    
    plt.xlabel('Relative Concentration')
    plt.ylabel('Height (normalized)')
    plt.title('Vertical Concentration Profile\n(Rouse Distribution)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('SlurryPipeline_detailed_analysis.png', dpi=300, bbox_inches='tight')
    print(f"Saved detailed analysis plots to: SlurryPipeline_detailed_analysis.png")
    
    return True

def main():
    """
    Main function to run all SlurryPipeline examples and create visualizations
    """
    print("SlurryPipeline Example Suite")
    print("===========================")
    print("Comprehensive demonstration of SlurryPipeline class capabilities")
    print(f"Timestamp: {np.datetime64('now')}")
    
    try:
        # Run all examples
        example_1_mining_ore_transport()
        example_2_dredging_operations()
        example_3_wastewater_sludge()
        example_4_startup_shutdown()
        
        # Create visualizations
        create_visualizations()
        
        print("\n" + "=" * 60)
        print("EXAMPLE SUITE COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\nGenerated Files:")
        print("- SlurryPipeline_example_plots.png      : Comprehensive analysis plots")
        print("- SlurryPipeline_detailed_analysis.png  : Flow regime and economic analysis")
        print("\nSee SlurryPipeline_documentation.md for detailed technical background.")
        
    except Exception as e:
        print(f"\nError during example execution: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
