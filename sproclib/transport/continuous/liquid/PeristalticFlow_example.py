#!/usr/bin/env python3
"""
PeristalticFlow Example Usage - Comprehensive Demonstration

This example demonstrates the capabilities of the PeristalticFlow class for modeling
peristaltic pump systems. It covers dosing accuracy, pulsation analysis, calibration,
and control system applications.

Based on: PeristalticFlow_documentation.md
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from PeristalticFlow import PeristalticFlow
except ImportError:
    print("Error: Could not import PeristalticFlow. Make sure PeristalticFlow.py is in the current directory.")
    sys.exit(1)

def example_1_pharmaceutical_dosing():
    """
    Example 1: Pharmaceutical dosing system for drug manufacturing
    
    Scenario: Precise dosing of active pharmaceutical ingredient (API)
    - High accuracy requirement (±1%)
    - Low flow rates (mL/min range)
    - Sterile fluid path
    """
    print("=" * 60)
    print("EXAMPLE 1: Pharmaceutical API Dosing System")
    print("=" * 60)
    
    # Create peristaltic pump for pharmaceutical dosing
    api_pump = PeristalticFlow(
        tube_diameter=0.003,        # 3 mm ID tubing (small for precision)
        tube_length=0.25,           # 25 cm in pump head
        pump_speed=50.0,            # 50 RPM (moderate speed)
        occlusion_factor=0.95,      # 95% compression (excellent seal)
        fluid_density=1050.0,       # API solution density
        fluid_viscosity=1.5e-3,     # Slightly viscous solution
        pulsation_damping=0.9,      # High damping (compliance chamber)
        name="PharmaceuticalDosingPump"
    )
    
    # Display model information
    print("\nPump Configuration:")
    info = api_pump.describe()
    print(f"Application: {info['typical_applications'][0]}")
    print(f"Tube Diameter: {api_pump.tube_diameter*1000:.1f} mm")
    print(f"Occlusion Factor: {api_pump.occlusion_factor*100:.1f}%")
    print(f"Pulsation Damping: {api_pump.pulsation_damping*100:.1f}%")
    
    # Calibration curve generation
    speeds = np.array([10, 20, 30, 50, 80, 100, 150, 200])  # RPM
    
    print("\nCalibration Curve:")
    print("Speed | Flow Rate | Accuracy | Pulsation | Chamber")
    print("(RPM) | (mL/min)  | (%)      | (%)       | Vol(uL)")
    print("-" * 55)
    
    calibration_data = []
    for speed in speeds:
        # steady_state expects [P_inlet, pump_speed, occlusion_level]
        inputs = np.array([101325.0, speed, 1.0])  # Atmospheric pressure, speed, full occlusion
        result = api_pump.steady_state(inputs)
        
        flow_rate = result[0]  # m³/s
        p_outlet = result[1]   # Pa
        
        flow_ml_min = flow_rate * 60 * 1e6  # Convert to mL/min
        # Calculate simple metrics for display
        efficiency = min(95.0, 90.0 + speed/100.0)  # Simple efficiency model
        pulsation = max(1.0, 10.0 - api_pump.pulsation_damping * 10)  # Pulsation based on damping
        chamber_ul = (flow_rate / speed) * 1e9 if speed > 0 else 0  # Stroke volume estimate
        
        print(f"{speed:5.0f} | {flow_ml_min:8.2f}  | {efficiency:7.1f}  | {pulsation:8.1f}  | {chamber_ul:6.1f}")
        
        calibration_data.append({
            'speed': speed,
            'flow_rate': flow_rate,
            'flow_ml_min': flow_ml_min,
            'efficiency': efficiency,
            'pulsation': pulsation
        })
    
    # Dosing precision analysis
    target_dose = 5.0  # mL/min target
    best_match = min(calibration_data, key=lambda x: abs(x['flow_ml_min'] - target_dose))
    
    print(f"\nDosing Analysis for {target_dose} mL/min:")
    print(f"Optimal Speed: {best_match['speed']:.0f} RPM")
    print(f"Actual Flow: {best_match['flow_ml_min']:.3f} mL/min")
    print(f"Dosing Error: {abs(best_match['flow_ml_min'] - target_dose)/target_dose*100:.2f}%")
    print(f"Pulsation: ±{best_match['pulsation']:.1f}%")
    
    return calibration_data

def example_2_analytical_instrument():
    """
    Example 2: HPLC mobile phase delivery system
    
    Scenario: High-performance liquid chromatography pump
    - Consistent flow for accurate retention times
    - Low pulsation for detector stability
    - Wide flow range capability
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: HPLC Mobile Phase Delivery")
    print("=" * 60)
    
    # HPLC pump configuration
    hplc_pump = PeristalticFlow(
        tube_diameter=0.006,        # 6 mm ID tubing
        tube_length=0.4,            # 40 cm pump head
        pump_speed=100.0,           # 100 RPM baseline
        occlusion_factor=0.88,      # 88% compression (good balance)
        fluid_density=780.0,        # Acetonitrile/water mixture
        fluid_viscosity=0.4e-3,     # Low viscosity mobile phase
        pulsation_damping=0.95,     # Very high damping (critical for HPLC)
        name="HPLCMobilePhasePump"
    )
    
    print("\nHPLC System Requirements:")
    print(f"Mobile Phase: Acetonitrile/Water (80/20)")
    print(f"Density: {hplc_pump.fluid_density} kg/m³")
    print(f"Viscosity: {hplc_pump.fluid_viscosity*1000:.1f} mPa·s")
    print(f"Required Stability: < ±0.1% flow variation")
    
    # Flow rate range analysis
    speed_range = np.linspace(20, 300, 15)  # 20-300 RPM
    flow_performance = []
    
    print("\nFlow Rate Performance Map:")
    print("Speed | Flow Rate | Pulsation | Stability | Suitable")
    print("(RPM) | (mL/min)  | (%)       | Rating    | for HPLC")
    print("-" * 55)
    
    for speed in speed_range:
        inputs = np.array([101325.0, speed, 1.0])  # Atmospheric pressure, speed, full occlusion
        result = hplc_pump.steady_state(inputs)
        
        flow_rate = result[0]  # m³/s
        p_outlet = result[1]   # Pa
        
        flow_ml_min = flow_rate * 60 * 1e6  # mL/min
        pulsation = max(1.0, 10.0 - hplc_pump.pulsation_damping * 10)  # Estimated pulsation
        
        # Stability rating based on pulsation
        if pulsation < 2.0:
            stability = "Excellent"
            suitable = "Yes"
        elif pulsation < 5.0:
            stability = "Good"
            suitable = "Yes"
        elif pulsation < 10.0:
            stability = "Fair"
            suitable = "Maybe"
        else:
            stability = "Poor"
            suitable = "No"
        
        if speed % 40 < 20:  # Print subset for readability
            print(f"{speed:5.0f} | {flow_ml_min:8.2f}  | {pulsation:8.2f}  | {stability:8s}  | {suitable}")
        
        flow_performance.append({
            'speed': speed,
            'flow_rate': flow_rate,
            'flow_ml_min': flow_ml_min,
            'pulsation': pulsation,
            'stability': stability,
            'suitable': suitable
        })
    
    # Optimal operating window
    suitable_points = [p for p in flow_performance if p['suitable'] == 'Yes']
    min_flow = min(p['flow_ml_min'] for p in suitable_points)
    max_flow = max(p['flow_ml_min'] for p in suitable_points)
    
    print(f"\nOptimal Operating Window:")
    print(f"Flow Range: {min_flow:.1f} - {max_flow:.1f} mL/min")
    print(f"Turn-down Ratio: {max_flow/min_flow:.1f}:1")
    print(f"Recommended for HPLC: {len(suitable_points)}/{len(flow_performance)} operating points")
    
    return flow_performance

def example_3_pulsation_analysis():
    """
    Example 3: Detailed pulsation analysis for process control
    
    Scenario: Chemical dosing with pulsation dampening
    - Time-domain analysis of flow pulsation
    - Effect of damping on flow smoothness
    - Control system implications
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Pulsation Analysis and Damping")
    print("=" * 60)
    
    # Chemical dosing pump
    chem_pump = PeristalticFlow(
        tube_diameter=0.008,        # 8 mm ID tubing
        tube_length=0.3,            # 30 cm pump head
        pump_speed=120.0,           # 120 RPM
        occlusion_factor=0.85,      # 85% compression
        fluid_density=1200.0,       # Dense chemical solution
        fluid_viscosity=2.0e-3,     # Viscous chemical
        pulsation_damping=0.7,      # Moderate damping
        name="ChemicalDosingPump"
    )
    
    print("\nPulsation Analysis Setup:")
    print(f"Pump Speed: {chem_pump.pump_speed} RPM")
    print(f"Number of Rollers: 3 (typical)")
    
    # Time-domain simulation
    dt = 0.01  # 10 ms time steps
    t_total = 2.0  # 2 seconds simulation
    time_points = np.arange(0, t_total, dt)
    n_points = len(time_points)
    
    # Calculate pulsation characteristics
    base_inputs = np.array([101325.0, chem_pump.pump_speed, 1.0])
    base_result = chem_pump.steady_state(base_inputs)
    avg_flow = base_result[0]  # m³/s
    pulsation_freq = chem_pump.pump_speed / 60.0  # Hz (simplified)
    
    print(f"Base Flow Rate: {avg_flow*60*1e6:.1f} mL/min")
    print(f"Pulsation Frequency: {pulsation_freq:.1f} Hz")
    pulsation_amplitude = max(1.0, 10.0 - chem_pump.pulsation_damping * 10) / 100.0  # As fraction
    print(f"Pulsation Amplitude: ±{pulsation_amplitude*100:.1f}%")
    
    # Generate pulsating flow profile
    flow_history = np.zeros(n_points)
    pressure_history = np.zeros(n_points)
    
    for i, t in enumerate(time_points):
        # Simulate pulsating flow profile
        pulsation_component = pulsation_amplitude * np.sin(2 * np.pi * pulsation_freq * t)
        flow_history[i] = (avg_flow + avg_flow * pulsation_component) * 60 * 1e6  # mL/min
        # Approximate pressure fluctuation
        pressure_history[i] = 101.325 + 2.0 * np.sin(2 * np.pi * pulsation_freq * t)  # kPa
    
    # Statistical analysis of pulsation
    mean_flow = np.mean(flow_history)
    std_flow = np.std(flow_history)
    min_flow = np.min(flow_history)
    max_flow = np.max(flow_history)
    
    print(f"\nPulsation Statistics:")
    print(f"Mean Flow: {mean_flow:.2f} mL/min")
    print(f"Standard Deviation: {std_flow:.3f} mL/min ({std_flow/mean_flow*100:.2f}%)")
    print(f"Flow Range: {min_flow:.2f} - {max_flow:.2f} mL/min")
    print(f"Peak-to-Peak Variation: {(max_flow-min_flow)/mean_flow*100:.1f}%")
    
    # Compare different damping levels
    damping_levels = [0.3, 0.5, 0.7, 0.9]
    
    print(f"\nDamping Comparison:")
    print("Damping | Pulsation | Flow Stability")
    print("Factor  | Amplitude | Rating")
    print("-" * 35)
    
    damping_data = []
    for damping in damping_levels:
        test_pump = PeristalticFlow(
            tube_diameter=chem_pump.tube_diameter,
            tube_length=chem_pump.tube_length,
            pump_speed=chem_pump.pump_speed,
            occlusion_factor=chem_pump.occlusion_factor,
            fluid_density=chem_pump.fluid_density,
            fluid_viscosity=chem_pump.fluid_viscosity,
            pulsation_damping=damping
        )
        
        test_inputs = np.array([101325.0, test_pump.pump_speed, 1.0])
        result = test_pump.steady_state(test_inputs)
        flow_rate = result[0]
        pulsation = max(1.0, 10.0 - damping * 10)  # Estimated pulsation based on damping
        
        if pulsation < 1:
            stability = "Excellent"
        elif pulsation < 3:
            stability = "Good"
        elif pulsation < 8:
            stability = "Fair"
        else:
            stability = "Poor"
        
        print(f"{damping:6.1f}  | {pulsation:8.1f}%  | {stability}")
        
        damping_data.append({
            'damping': damping,
            'pulsation': pulsation,
            'stability': stability
        })
    
    return {
        'time': time_points,
        'flow_history': flow_history,
        'pressure_history': pressure_history,
        'damping_data': damping_data,
        'base_result': base_result,
        'pulsation_frequency': pulsation_freq,
        'avg_flow': avg_flow,
        'pulsation_amplitude': pulsation_amplitude
    }

def example_4_tube_wear_analysis():
    """
    Example 4: Tube wear and replacement analysis
    
    Scenario: Predictive maintenance for industrial dosing
    - Model tube degradation over time
    - Performance impact assessment
    - Replacement scheduling optimization
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Tube Wear and Maintenance Analysis")
    print("=" * 60)
    
    # Industrial dosing pump
    industrial_pump = PeristalticFlow(
        tube_diameter=0.012,        # 12 mm ID tubing (industrial size)
        tube_length=0.5,            # 50 cm pump head
        pump_speed=150.0,           # 150 RPM continuous operation
        occlusion_factor=0.90,      # 90% compression (new tube)
        fluid_density=1100.0,       # Industrial chemical
        fluid_viscosity=3.0e-3,     # Moderately viscous
        pulsation_damping=0.6,      # Industrial damping
        name="IndustrialDosingPump"
    )
    
    print("\nTube Wear Analysis:")
    print(f"Initial Tube Diameter: {industrial_pump.tube_diameter*1000:.1f} mm")
    print(f"Operating Speed: {industrial_pump.pump_speed} RPM")
    print(f"Continuous Operation: 24/7")
    
    # Simulate tube wear over time (months of operation)
    months = np.array([0, 1, 2, 3, 6, 9, 12, 15, 18])  # Months of operation
    
    print(f"\nWear Progression Analysis:")
    print("Months | Occlusion | Flow Rate | Accuracy | Replacement")
    print("       | Factor    | (L/h)     | Loss (%) | Required")
    print("-" * 55)
    
    wear_data = []
    for month in months:
        # Model occlusion degradation (exponential decay)
        degradation_factor = np.exp(-month / 15)  # 15-month time constant
        current_occlusion = 0.90 * degradation_factor + 0.60 * (1 - degradation_factor)
        
        # Create pump with degraded tube
        worn_pump = PeristalticFlow(
            tube_diameter=industrial_pump.tube_diameter,
            tube_length=industrial_pump.tube_length,
            pump_speed=industrial_pump.pump_speed,
            occlusion_factor=current_occlusion,
            fluid_density=industrial_pump.fluid_density,
            fluid_viscosity=industrial_pump.fluid_viscosity,
            pulsation_damping=industrial_pump.pulsation_damping
        )
        
        worn_inputs = np.array([101325.0, worn_pump.pump_speed, 1.0])
        result = worn_pump.steady_state(worn_inputs)
        flow_rate = result[0]  # m³/s
        flow_lh = flow_rate * 3600  # L/h
        
        # Calculate accuracy loss compared to new tube
        if month == 0:
            reference_flow = flow_lh
        
        accuracy_loss = (1 - flow_lh/reference_flow) * 100
        replacement_needed = "Yes" if accuracy_loss > 10 else "No"
        
        print(f"{month:6.0f} | {current_occlusion:8.2f}  | {flow_lh:8.1f}  | {accuracy_loss:7.1f}  | {replacement_needed}")
        
        wear_data.append({
            'months': month,
            'occlusion': current_occlusion,
            'flow_rate': flow_lh,
            'accuracy_loss': accuracy_loss,
            'replacement_needed': replacement_needed
        })
    
    # Maintenance scheduling analysis
    replacement_threshold = 10  # % accuracy loss
    replacement_month = None
    for data in wear_data:
        if data['accuracy_loss'] > replacement_threshold:
            replacement_month = data['months']
            break
    
    print(f"\nMaintenance Recommendations:")
    if replacement_month:
        print(f"Tube Replacement Due: Month {replacement_month}")
        print(f"Performance Threshold: {replacement_threshold}% accuracy loss")
        print(f"Annual Tube Cost: ${(12/replacement_month)*150:.0f} (assuming $150/tube)")
    else:
        print(f"Tube performance acceptable for analysis period")
    
    # Economic analysis
    tube_cost = 150  # $ per tube
    pump_efficiency_loss = 0.1  # 10% efficiency loss at replacement point
    energy_cost = 0.12  # $/kWh
    operating_power = 0.5  # kW pump motor
    
    if replacement_month:
        annual_tubes = 12 / replacement_month
        annual_tube_cost = annual_tubes * tube_cost
        annual_energy_loss = pump_efficiency_loss * operating_power * 8760 * energy_cost
        total_annual_cost = annual_tube_cost + annual_energy_loss
        
        print(f"\nEconomic Analysis:")
        print(f"Annual Tube Replacement Cost: ${annual_tube_cost:.0f}")
        print(f"Annual Energy Loss Cost: ${annual_energy_loss:.0f}")
        print(f"Total Annual Maintenance Cost: ${total_annual_cost:.0f}")
    
    return wear_data

def create_visualizations():
    """
    Create comprehensive visualization plots for peristaltic flow examples
    """
    print("\n" + "=" * 60)
    print("CREATING VISUALIZATION PLOTS")
    print("=" * 60)
    
    # Run examples to get data
    pharma_data = example_1_pharmaceutical_dosing()
    hplc_data = example_2_analytical_instrument()
    pulsation_data = example_3_pulsation_analysis()
    wear_data = example_4_tube_wear_analysis()
    
    # Create comprehensive figure
    fig = plt.figure(figsize=(16, 12))
    
    # Plot 1: Calibration Curve (Speed vs Flow Rate)
    ax1 = plt.subplot(2, 3, 1)
    speeds = [d['speed'] for d in pharma_data]
    flows = [d['flow_ml_min'] for d in pharma_data]
    
    plt.plot(speeds, flows, 'bo-', linewidth=2, markersize=8, label='Measured Points')
    
    # Linear fit for calibration
    coeffs = np.polyfit(speeds, flows, 1)
    speed_fit = np.linspace(min(speeds), max(speeds), 100)
    flow_fit = np.polyval(coeffs, speed_fit)
    plt.plot(speed_fit, flow_fit, 'r--', alpha=0.7, label=f'Linear Fit: {coeffs[0]:.3f}*RPM + {coeffs[1]:.2f}')
    
    plt.xlabel('Pump Speed (RPM)')
    plt.ylabel('Flow Rate (mL/min)')
    plt.title('Pharmaceutical Dosing\nCalibration Curve')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Plot 2: Pulsation vs Speed
    ax2 = plt.subplot(2, 3, 2)
    hplc_speeds = [d['speed'] for d in hplc_data]
    hplc_pulsation = [d['pulsation'] for d in hplc_data]
    
    # Color code by suitability
    colors = ['green' if d['suitable'] == 'Yes' else 'orange' if d['suitable'] == 'Maybe' else 'red' 
              for d in hplc_data]
    
    scatter = plt.scatter(hplc_speeds, hplc_pulsation, c=colors, s=60, alpha=0.7)
    plt.axhline(y=0.1, color='green', linestyle='--', alpha=0.7, label='Excellent Threshold')
    plt.axhline(y=0.5, color='orange', linestyle='--', alpha=0.7, label='Good Threshold')
    plt.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Acceptable Limit')
    
    plt.xlabel('Pump Speed (RPM)')
    plt.ylabel('Pulsation Amplitude (%)')
    plt.title('HPLC Flow Stability\nvs Pump Speed')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.yscale('log')
    
    # Plot 3: Time-Domain Pulsation
    ax3 = plt.subplot(2, 3, 3)
    time_ms = pulsation_data['time'] * 1000  # Convert to milliseconds
    flow_profile = pulsation_data['flow_history']
    
    plt.plot(time_ms, flow_profile, 'b-', linewidth=1.5, label='Instantaneous Flow')
    mean_flow = np.mean(flow_profile)
    plt.axhline(y=mean_flow, color='red', linestyle='--', alpha=0.7, label=f'Mean: {mean_flow:.1f} mL/min')
    
    plt.xlabel('Time (ms)')
    plt.ylabel('Flow Rate (mL/min)')
    plt.title('Flow Pulsation Profile\n(Chemical Dosing)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(0, 500)  # Show first 500 ms
    
    # Plot 4: Damping Effect
    ax4 = plt.subplot(2, 3, 4)
    damping_factors = [d['damping'] for d in pulsation_data['damping_data']]
    damping_pulsation = [d['pulsation'] for d in pulsation_data['damping_data']]
    
    plt.plot(damping_factors, damping_pulsation, 'mo-', linewidth=2, markersize=8)
    plt.xlabel('Damping Factor')
    plt.ylabel('Pulsation Amplitude (%)')
    plt.title('Effect of Pulsation Damping\non Flow Stability')
    plt.grid(True, alpha=0.3)
    
    # Add performance zones
    plt.axhspan(0, 1, alpha=0.2, color='green', label='Excellent')
    plt.axhspan(1, 3, alpha=0.2, color='yellow', label='Good')
    plt.axhspan(3, 8, alpha=0.2, color='orange', label='Fair')
    plt.legend()
    
    # Plot 5: Tube Wear Analysis
    ax5 = plt.subplot(2, 3, 5)
    months = [d['months'] for d in wear_data]
    accuracy_loss = [d['accuracy_loss'] for d in wear_data]
    
    plt.plot(months, accuracy_loss, 'ro-', linewidth=2, markersize=6)
    plt.axhline(y=10, color='red', linestyle='--', alpha=0.7, label='Replacement Threshold')
    plt.fill_between(months, 0, accuracy_loss, alpha=0.3, color='red')
    
    plt.xlabel('Operating Time (months)')
    plt.ylabel('Accuracy Loss (%)')
    plt.title('Tube Wear Progression\n(Industrial Application)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Plot 6: Flow Range Comparison
    ax6 = plt.subplot(2, 3, 6)
    
    # Compare different applications
    applications = ['Pharmaceutical\n(3mm tube)', 'HPLC\n(6mm tube)', 'Chemical\n(8mm tube)', 'Industrial\n(12mm tube)']
    tube_sizes = [3, 6, 8, 12]  # mm
    max_flows = [max([d['flow_ml_min'] for d in pharma_data]),
                 max([d['flow_ml_min'] for d in hplc_data]),
                 120,  # Estimated for 8mm
                 300]  # Estimated for 12mm
    
    colors_app = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral']
    bars = plt.bar(applications, max_flows, color=colors_app, alpha=0.7, edgecolor='black')
    
    # Add tube size labels on bars
    for i, (bar, size) in enumerate(zip(bars, tube_sizes)):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{size}mm', ha='center', va='bottom', fontweight='bold')
    
    plt.ylabel('Maximum Flow Rate (mL/min)')
    plt.title('Flow Capacity by Application\n(Tube Size Impact)')
    plt.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('PeristalticFlow_example_plots.png', dpi=300, bbox_inches='tight')
    print(f"Saved comprehensive plots to: PeristalticFlow_example_plots.png")
    
    # Create detailed pulsation analysis figure
    fig2 = plt.figure(figsize=(14, 10))
    
    # Detailed pulsation waveform
    ax1 = plt.subplot(2, 2, 1)
    time_detailed = pulsation_data['time'][:200]  # First 2 seconds
    flow_detailed = pulsation_data['flow_history'][:200]
    
    plt.plot(time_detailed, flow_detailed, 'b-', linewidth=1.5)
    plt.fill_between(time_detailed, flow_detailed, alpha=0.3, color='blue')
    
    # Mark pulsation peaks
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(flow_detailed, height=np.mean(flow_detailed))
    if len(peaks) > 0:
        plt.scatter(time_detailed[peaks], flow_detailed[peaks], color='red', s=50, zorder=5)
    
    plt.xlabel('Time (s)')
    plt.ylabel('Flow Rate (mL/min)')
    plt.title('Detailed Pulsation Waveform\n(First 2 Seconds)')
    plt.grid(True, alpha=0.3)
    
    # Frequency analysis
    ax2 = plt.subplot(2, 2, 2)
    from scipy.fft import fft, fftfreq
    
    # FFT of flow signal
    dt = pulsation_data['time'][1] - pulsation_data['time'][0]
    n_samples = len(pulsation_data['flow_history'])
    frequencies = fftfreq(n_samples, dt)[:n_samples//2]
    fft_magnitude = np.abs(fft(pulsation_data['flow_history']))[:n_samples//2]
    
    # Get pulsation frequency from the returned data
    pulsation_freq = pulsation_data['pulsation_frequency']
    
    plt.semilogy(frequencies, fft_magnitude, 'g-', linewidth=2)
    plt.axvline(x=pulsation_freq, 
                color='red', linestyle='--', label=f"Fundamental: {pulsation_freq:.1f} Hz")
    
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.title('Flow Pulsation Frequency Spectrum')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(0, 20)  # Focus on low frequencies
    
    # Tube degradation model
    ax3 = plt.subplot(2, 2, 3)
    months_detailed = np.linspace(0, 24, 100)
    degradation_detailed = np.exp(-months_detailed / 15)
    occlusion_detailed = 0.90 * degradation_detailed + 0.60 * (1 - degradation_detailed)
    
    plt.plot(months_detailed, occlusion_detailed * 100, 'purple', linewidth=2)
    plt.scatter([d['months'] for d in wear_data], 
                [d['occlusion']*100 for d in wear_data], 
                color='red', s=50, zorder=5, label='Analysis Points')
    
    plt.xlabel('Operating Time (months)')
    plt.ylabel('Occlusion Factor (%)')
    plt.title('Tube Degradation Model\n(Exponential Decay)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Economic optimization
    ax4 = plt.subplot(2, 2, 4)
    replacement_intervals = np.array([3, 6, 9, 12, 15, 18])  # months
    tube_cost = 150
    annual_tube_costs = (12 / replacement_intervals) * tube_cost
    
    # Energy loss cost (assuming efficiency degrades linearly)
    energy_loss_fractions = replacement_intervals / 24  # Normalized degradation
    annual_energy_costs = energy_loss_fractions * 0.5 * 8760 * 0.12  # 0.5kW, $0.12/kWh
    total_costs = annual_tube_costs + annual_energy_costs
    
    plt.plot(replacement_intervals, annual_tube_costs, 'b-o', label='Tube Costs')
    plt.plot(replacement_intervals, annual_energy_costs, 'r-s', label='Energy Loss Costs')
    plt.plot(replacement_intervals, total_costs, 'g-^', linewidth=2, label='Total Costs')
    
    # Find optimal point
    optimal_idx = np.argmin(total_costs)
    optimal_interval = replacement_intervals[optimal_idx]
    optimal_cost = total_costs[optimal_idx]
    
    plt.scatter([optimal_interval], [optimal_cost], color='orange', s=150, 
                label=f'Optimal: {optimal_interval} months', zorder=5)
    
    plt.xlabel('Replacement Interval (months)')
    plt.ylabel('Annual Cost ($)')
    plt.title('Maintenance Cost Optimization')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('PeristalticFlow_detailed_analysis.png', dpi=300, bbox_inches='tight')
    print(f"Saved detailed analysis plots to: PeristalticFlow_detailed_analysis.png")
    
    return True

def main():
    """
    Main function to run all PeristalticFlow examples and create visualizations
    """
    print("PeristalticFlow Example Suite")
    print("============================")
    print("Comprehensive demonstration of PeristalticFlow class capabilities")
    print(f"Timestamp: {np.datetime64('now')}")
    
    try:
        # Run all examples
        example_1_pharmaceutical_dosing()
        example_2_analytical_instrument()
        example_3_pulsation_analysis()
        example_4_tube_wear_analysis()
        
        # Create visualizations
        create_visualizations()
        
        print("\n" + "=" * 60)
        print("EXAMPLE SUITE COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\nGenerated Files:")
        print("- PeristalticFlow_example_plots.png      : Comprehensive analysis plots")
        print("- PeristalticFlow_detailed_analysis.png  : Detailed pulsation and maintenance analysis")
        print("\nSee PeristalticFlow_documentation.md for detailed technical background.")
        
    except Exception as e:
        print(f"\nError during example execution: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
