import numpy as np
import matplotlib.pyplot as plt

def main():
    """
    Relay Auto-Tuning Example: Shell-and-Tube Heat Exchanger Temperature Control
    
    This example demonstrates relay auto-tuning methodology for automatically
    identifying process dynamics and calculating controller parameters.
    """
    
    print("=== Relay Auto-Tuning Example: Heat Exchanger Temperature Control ===")
    print()
    
    # ==============================================
    # STEP 1: PROCESS SETUP
    # ==============================================
    print("1. Process Setup and Configuration")
    print("-" * 40)
    
    print("Process: Shell-and-Tube Heat Exchanger")
    print("  Type: Counter-current flow")
    print("  Shell Side: Process fluid (to be heated)")
    print("  Tube Side: Steam (heating medium)")
    print("  Heat Transfer Area: 150 m²")
    print("  Design Heat Duty: 2.5 MW")
    print()
    
    print("Control Configuration:")
    print("  Manipulated Variable: Steam Control Valve Position (%)")
    print("  Controlled Variable: Process Outlet Temperature (K)")
    print("  Measurement: RTD with 4-20 mA transmitter")
    print("  Control Valve: Equal percentage, Cv=50")
    print()
    
    print("Operating Conditions:")
    print("  Process Inlet Temperature: 298 K (25°C)")
    print("  Process Outlet Setpoint: 348 K (75°C)")
    print("  Process Flow Rate: 50 m³/h")
    print("  Steam Pressure: 6 bar (158°C)")
    print("  Typical Valve Position: 45%")
    print()
    
    # ==============================================
    # STEP 2: RELAY TEST DESIGN
    # ==============================================
    print("2. Relay Test Design Parameters")
    print("-" * 40)
    
    # Relay test parameters
    relay_amplitude = 12.0  # % valve position
    hysteresis = 0.8  # K temperature band
    test_duration = 180.0  # minutes (3 hours)
    sampling_time = 0.5  # minutes (30 seconds)
    
    print(f"Relay Test Configuration:")
    print(f"  Relay Amplitude: ±{relay_amplitude} % valve position")
    print(f"  Hysteresis Band: ±{hysteresis/2} K around setpoint")
    print(f"  Test Duration: {test_duration} minutes")
    print(f"  Sampling Rate: {sampling_time} minutes ({sampling_time*60} seconds)")
    print(f"  Safety Limits: 320-370 K")
    print()
    
    # Safety validation
    nominal_valve = 45.0  # %
    max_valve = nominal_valve + relay_amplitude
    min_valve = nominal_valve - relay_amplitude
    
    print(f"Safety Check:")
    print(f"  Valve Range: {min_valve}% to {max_valve}%")
    assert 0 <= min_valve and max_valve <= 100, "Valve limits exceeded"
    print(f"  ✓ Valve position within safe limits (0-100%)")
    print()
    
    # ==============================================
    # STEP 3: RELAY TEST EXECUTION SIMULATION
    # ==============================================
    print("3. Relay Test Execution")
    print("-" * 40)
    
    # Time vector
    time_vector = np.arange(0, test_duration + sampling_time, sampling_time)
    n_points = len(time_vector)
    
    # Process parameters (actual, unknown during test)
    Kp_actual = 2.2  # K/% valve position
    tau_actual = 18.0  # minutes (thermal time constant)
    theta_actual = 3.0  # minutes (dead time)
    
    # Initialize arrays
    valve_position = np.zeros(n_points)
    temperature = np.zeros(n_points)
    relay_output = np.zeros(n_points)
    temperature_setpoint = 348.0  # K
    
    # Initial conditions
    temperature[0] = temperature_setpoint
    valve_position[0] = nominal_valve
    relay_state = 1  # Start with positive relay output
    
    print(f"Starting relay test at t=10 minutes...")
    print(f"Initial temperature: {temperature[0]:.1f} K")
    print(f"Initial valve position: {valve_position[0]:.1f}%")
    print()
    
    # Relay test simulation
    for i in range(1, n_points):
        t = time_vector[i]
        
        if t >= 10.0:  # Start relay test after 10 minutes
            # Relay logic with hysteresis
            error = temperature_setpoint - temperature[i-1]
            
            if relay_state == 1 and error <= -hysteresis/2:
                relay_state = -1
                print(f"  t={t:.1f} min: Relay switched to LOW (temp > setpoint)")
            elif relay_state == -1 and error >= hysteresis/2:
                relay_state = 1
                print(f"  t={t:.1f} min: Relay switched to HIGH (temp < setpoint)")
            
            # Relay output
            relay_output[i] = relay_state * relay_amplitude
            valve_position[i] = nominal_valve + relay_output[i]
        else:
            # Before relay test - maintain nominal valve position
            valve_position[i] = nominal_valve
            relay_output[i] = 0
        
        # Process response simulation (first-order with dead time)
        if i >= int(theta_actual / sampling_time):  # Account for dead time
            # Input considering dead time
            delayed_input = valve_position[i - int(theta_actual / sampling_time)]
            
            # First-order response
            steady_state_temp = temperature_setpoint + Kp_actual * (delayed_input - nominal_valve)
            temp_error = steady_state_temp - temperature[i-1]
            temp_change = temp_error * sampling_time / tau_actual
            temperature[i] = temperature[i-1] + temp_change
        else:
            # During dead time - no response to input changes
            temperature[i] = temperature[i-1]
        
        # Add measurement noise
        np.random.seed(42 + i)
        noise = np.random.normal(0, 0.1)  # 0.1 K noise
        temperature[i] += noise
    
    # ==============================================
    # STEP 4: OSCILLATION ANALYSIS
    # ==============================================
    print()
    print("4. Oscillation Analysis and Parameter Extraction")
    print("-" * 40)
    
    # Analyze oscillation after initial transient (skip first 30 minutes)
    analysis_start = int(30 / sampling_time)
    temp_analysis = temperature[analysis_start:]
    time_analysis = time_vector[analysis_start:]
    valve_analysis = valve_position[analysis_start:]
    
    # Find peaks and valleys for period calculation
    peaks = []
    valleys = []
    
    for i in range(1, len(temp_analysis) - 1):
        if temp_analysis[i] > temp_analysis[i-1] and temp_analysis[i] > temp_analysis[i+1]:
            if temp_analysis[i] > temperature_setpoint:  # Only significant peaks
                peaks.append(i)
        elif temp_analysis[i] < temp_analysis[i-1] and temp_analysis[i] < temp_analysis[i+1]:
            if temp_analysis[i] < temperature_setpoint:  # Only significant valleys
                valleys.append(i)
    
    # Calculate ultimate period
    if len(peaks) >= 3:
        peak_times = time_analysis[peaks]
        periods = np.diff(peak_times)
        Tu_identified = np.mean(periods)
        period_std = np.std(periods)
        
        print(f"Period Analysis:")
        print(f"  Number of peaks detected: {len(peaks)}")
        print(f"  Individual periods: {periods}")
        print(f"  Ultimate Period (Tu): {Tu_identified:.1f} ± {period_std:.1f} min")
    else:
        Tu_identified = 20.0  # Estimate if detection fails
        print(f"  Warning: Insufficient peaks for reliable period calculation")
        print(f"  Using estimated period: {Tu_identified:.1f} min")
    
    # Calculate oscillation amplitude
    if len(peaks) > 0 and len(valleys) > 0:
        peak_values = temp_analysis[peaks]
        valley_values = temp_analysis[valleys]
        amplitude_temp = (np.mean(peak_values) - np.mean(valley_values)) / 2
        
        print(f"  Peak temperatures: {peak_values}")
        print(f"  Valley temperatures: {valley_values}")
        print(f"  Oscillation amplitude (a): {amplitude_temp:.2f} K")
    else:
        amplitude_temp = 2.5  # Estimate
        print(f"  Using estimated amplitude: {amplitude_temp:.2f} K")
    
    print()
    
    # ==============================================
    # STEP 5: ULTIMATE GAIN CALCULATION
    # ==============================================
    print("5. Ultimate Gain Calculation")
    print("-" * 40)
    
    # Describing function method for ultimate gain
    # For ideal relay: N(A) = 4h/(πa)
    # where h = relay amplitude, a = oscillation amplitude
    
    describing_function = 4 * relay_amplitude / (np.pi * amplitude_temp)
    Ku_identified = 1 / describing_function  # Ultimate gain is inverse of describing function
    
    print(f"Describing Function Analysis:")
    print(f"  Relay amplitude (h): {relay_amplitude} %")
    print(f"  Oscillation amplitude (a): {amplitude_temp:.2f} K")
    print(f"  Describing function N(A): {describing_function:.4f} %/K")
    print(f"  Ultimate Gain (Ku): {Ku_identified:.3f} %/K")
    print()
    
    # Validation check
    print(f"Parameter Identification Accuracy:")
    Ku_actual = 1.0 / (Kp_actual * np.pi / 4)  # Theoretical for comparison
    Tu_actual = 2 * np.pi * np.sqrt(tau_actual * theta_actual)  # Approximate
    
    Ku_error = abs(Ku_identified - Ku_actual) / Ku_actual * 100
    Tu_error = abs(Tu_identified - Tu_actual) / Tu_actual * 100
    
    print(f"  Ku Error: {Ku_error:.1f}%")
    print(f"  Tu Error: {Tu_error:.1f}%")
    print()
    
    # ==============================================
    # STEP 6: CONTROLLER TUNING FROM RELAY TEST
    # ==============================================
    print("6. Controller Tuning from Relay Test Results")
    print("-" * 40)
    
    # Multiple tuning methods based on relay test results
    
    # 1. Ziegler-Nichols from relay test
    Kc_zn = 0.6 * Ku_identified
    tau_I_zn = 0.5 * Tu_identified
    tau_D_zn = 0.125 * Tu_identified
    
    # 2. Tyreus-Luyben (more conservative)
    Kc_tl = Ku_identified / 3.2
    tau_I_tl = 2.2 * Tu_identified
    tau_D_tl = Tu_identified / 6.3
    
    # 3. AMIGO-based from relay test
    Kc_amigo = 0.45 * Ku_identified
    tau_I_amigo = 0.85 * Tu_identified
    tau_D_amigo = 0.1 * Tu_identified
    
    # 4. PI tuning (recommended for temperature control)
    Kc_pi = 0.45 * Ku_identified
    tau_I_pi = 0.83 * Tu_identified
    
    print(f"Tuning Method Comparison:")
    print(f"  Method          | Kc      | τI      | τD    ")
    print(f"  ----------------+---------+---------+-------")
    print(f"  Ziegler-Nichols | {Kc_zn:7.3f} | {tau_I_zn:7.1f} | {tau_D_zn:5.1f}")
    print(f"  Tyreus-Luyben  | {Kc_tl:7.3f} | {tau_I_tl:7.1f} | {tau_D_tl:5.1f}")
    print(f"  AMIGO-based    | {Kc_amigo:7.3f} | {tau_I_amigo:7.1f} | {tau_D_amigo:5.1f}")
    print(f"  PI Control     | {Kc_pi:7.3f} | {tau_I_pi:7.1f} |   0.0")
    print()
    
    print(f"Recommended Tuning (PI Control for Temperature):")
    print(f"  Controller Gain (Kc): {Kc_pi:.3f} %/K")
    print(f"  Integral Time (τI): {tau_I_pi:.1f} min")
    print(f"  Derivative Time (τD): 0.0 min (not recommended for temperature)")
    print()
    
    # ==============================================
    # STEP 7: PERFORMANCE VALIDATION
    # ==============================================
    print("7. Performance Validation Simulation")
    print("-" * 40)
    
    # Simulate closed-loop performance with PI tuning
    sim_time = np.linspace(0, 120, 601)  # 2 hours after tuning
    dt = sim_time[1] - sim_time[0]
    
    # Setpoint profile
    setpoint_sim = np.ones_like(sim_time) * 348.0  # K
    setpoint_sim[300:] = 353.0  # 5K step at t=60 min
    
    # Initialize simulation
    temp_sim = np.zeros_like(sim_time)
    valve_sim = np.zeros_like(sim_time)
    error_sim = np.zeros_like(sim_time)
    integral_error = 0.0
    
    temp_sim[0] = 348.0  # K
    valve_sim[0] = nominal_valve  # %
    
    # PI controller simulation
    for i in range(1, len(sim_time)):
        # Process simulation (simplified)
        valve_change = valve_sim[i-1] - nominal_valve
        steady_state_temp = 348.0 + Kp_actual * valve_change
        temp_error = steady_state_temp - temp_sim[i-1]
        temp_change = temp_error / tau_actual * dt
        temp_sim[i] = temp_sim[i-1] + temp_change
        
        # Add small disturbance
        if 200 <= i <= 220:  # Brief cooling disturbance
            temp_sim[i] -= 1.0
        
        # PI controller
        error = setpoint_sim[i-1] - temp_sim[i-1]
        error_sim[i-1] = error
        
        # Proportional action
        proportional = Kc_pi * error
        
        # Integral action
        integral_error += error * dt
        integral = Kc_pi / tau_I_pi * integral_error
        
        # Control output
        control_output = proportional + integral
        valve_sim[i] = nominal_valve + control_output
        
        # Valve constraints
        valve_sim[i] = np.clip(valve_sim[i], 0, 100)
    
    # Performance metrics
    step_start = 300
    step_response = temp_sim[step_start:]
    step_time_vec = sim_time[step_start:] - 60.0
    
    # Rise time and settling time
    initial_temp = temp_sim[step_start-1]
    final_temp = np.mean(temp_sim[-50:])
    step_size = final_temp - initial_temp
    
    # 10% to 90% rise time
    temp_10 = initial_temp + 0.1 * step_size
    temp_90 = initial_temp + 0.9 * step_size
    
    try:
        idx_10 = np.where(step_response >= temp_10)[0][0]
        idx_90 = np.where(step_response >= temp_90)[0][0]
        rise_time = step_time_vec[idx_90] - step_time_vec[idx_10]
    except:
        rise_time = np.nan
    
    # Overshoot
    max_temp = np.max(step_response)
    overshoot = (max_temp - final_temp) / abs(step_size) * 100
    
    # Settling time (2% band)
    settling_band = 0.02 * abs(step_size)
    try:
        settled_indices = np.where(np.abs(step_response - final_temp) <= settling_band)[0]
        settling_time = step_time_vec[settled_indices[0]]
    except:
        settling_time = np.nan
    
    print(f"Closed-Loop Performance (5K Step Response):")
    print(f"  Rise Time (10%-90%): {rise_time:.1f} min")
    print(f"  Settling Time (2%): {settling_time:.1f} min")
    print(f"  Overshoot: {overshoot:.1f}%")
    print(f"  Final Temperature: {final_temp:.1f} K")
    print(f"  Steady-State Error: {abs(353.0 - final_temp):.2f} K")
    print()
    
    # ==============================================
    # STEP 8: ECONOMIC BENEFITS
    # ==============================================
    print("8. Economic Benefits of Relay Auto-Tuning")
    print("-" * 40)
    
    # Economic analysis
    steam_cost = 25.0  # $/tonne
    energy_efficiency_improvement = 0.05  # 5% better efficiency
    production_rate = 100.0  # tonne/h of heated product
    
    # Annual savings calculation
    steam_consumption = 5.0  # tonne/h
    annual_steam_cost = steam_consumption * 8760 * steam_cost  # $/year
    annual_energy_savings = annual_steam_cost * energy_efficiency_improvement
    
    # Reduced variability benefits
    temperature_variance_reduction = 0.6  # 60% reduction in temperature variance
    quality_improvement_value = production_rate * 8760 * 2.0 * temperature_variance_reduction  # $/year
    
    # Relay test cost
    test_duration_hours = test_duration / 60
    test_cost = test_duration_hours * 50.0  # $/hour operational cost
    
    total_annual_savings = annual_energy_savings + quality_improvement_value
    payback_time = test_cost / (total_annual_savings / 365)  # days
    
    print(f"Economic Analysis:")
    print(f"  Relay Test Cost: ${test_cost:.0f}")
    print(f"  Annual Energy Savings: ${annual_energy_savings:,.0f}")
    print(f"  Annual Quality Benefits: ${quality_improvement_value:,.0f}")
    print(f"  Total Annual Savings: ${total_annual_savings:,.0f}")
    print(f"  Payback Time: {payback_time:.1f} days")
    print()
    
    # ==============================================
    # STEP 9: IMPLEMENTATION RECOMMENDATIONS
    # ==============================================
    print("9. Implementation Recommendations")
    print("-" * 40)
    
    print("Relay Auto-Tuning Advantages:")
    print("  ✓ No prior process knowledge required")
    print("  ✓ Automatic identification of process dynamics")
    print("  ✓ Multiple tuning options from single test")
    print("  ✓ Fast and cost-effective")
    print("  ✓ Can be repeated easily for retuning")
    print()
    
    print("Best Practices:")
    print("  • Perform during steady-state operation")
    print("  • Ensure adequate safety margins")
    print("  • Use appropriate relay amplitude (5-15% of range)")
    print("  • Monitor process throughout test")
    print("  • Validate tuning with small setpoint changes")
    print()
    
    print("When to Use Relay Tuning:")
    print("  • New control loops without process models")
    print("  • Retuning existing loops with poor performance")
    print("  • Process changes requiring controller adjustment")
    print("  • Validation of model-based tuning methods")
    print()
    
    return {
        'relay_test': {
            'time': time_vector,
            'temperature': temperature,
            'valve_position': valve_position,
            'relay_output': relay_output
        },
        'performance_test': {
            'time': sim_time,
            'temperature': temp_sim,
            'setpoint': setpoint_sim,
            'valve_position': valve_sim,
            'error': error_sim
        },
        'identification_results': {
            'Ku': Ku_identified,
            'Tu': Tu_identified,
            'amplitude': amplitude_temp
        },
        'tuning_parameters': {
            'Kc_pi': Kc_pi,
            'tau_I_pi': tau_I_pi,
            'Kc_zn': Kc_zn,
            'tau_I_zn': tau_I_zn,
            'tau_D_zn': tau_D_zn
        },
        'performance_metrics': {
            'rise_time': rise_time,
            'settling_time': settling_time,
            'overshoot': overshoot
        },
        'economics': {
            'annual_savings': total_annual_savings,
            'payback_days': payback_time
        }
    }

if __name__ == "__main__":
    results = main()
    print("✓ Relay auto-tuning example completed successfully!")
    print(f"✓ Ultimate gain identified: {results['identification_results']['Ku']:.3f}")
    print(f"✓ Ultimate period identified: {results['identification_results']['Tu']:.1f} min")
    print(f"✓ Recommended PI tuning: Kc={results['tuning_parameters']['Kc_pi']:.3f}, τI={results['tuning_parameters']['tau_I_pi']:.1f} min")
    print(f"✓ Estimated annual savings: ${results['economics']['annual_savings']:,.0f}")
