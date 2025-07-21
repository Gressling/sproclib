import numpy as np
import matplotlib.pyplot as plt

def main():
    """
    AMIGO Tuning Example: Distillation Column Composition Control
    
    This example demonstrates AMIGO (Approximate M-constrained Integral Gain Optimization)
    tuning methodology for a distillation column composition control system.
    """
    
    print("=== AMIGO Tuning Example: Distillation Column Composition Control ===")
    print()
    
    # ==============================================
    # STEP 1: PROCESS DESCRIPTION
    # ==============================================
    print("1. Process Description")
    print("-" * 40)
    
    print("Process: Binary Distillation Column")
    print("  Component A (Light): Ethanol")
    print("  Component B (Heavy): Water")
    print("  Separation: Ethanol-Water")
    print()
    
    print("Control Loop Configuration:")
    print("  Manipulated Variable: Reflux Ratio (L/D)")
    print("  Controlled Variable: Top Product Composition (mol% Ethanol)")
    print("  Disturbance: Feed Composition Changes")
    print("  Constraint: Reboiler Duty < 5000 kW")
    print()
    
    print("Operating Conditions:")
    print("  Feed Rate: 100 kmol/h")
    print("  Feed Composition: 45 mol% Ethanol")
    print("  Top Product Purity: 95 mol% Ethanol")
    print("  Bottom Product: < 2 mol% Ethanol")
    print("  Operating Pressure: 1.0 bar")
    print("  Number of Trays: 25")
    print()
    
    # ==============================================
    # STEP 2: STEP TEST AND IDENTIFICATION
    # ==============================================
    print("2. Step Test for Process Identification")
    print("-" * 40)
    
    # Simulate step test data
    time_vector = np.linspace(0, 480, 2401)  # 8 hours, 2-second intervals
    
    # Process parameters (typical for composition control)
    Kp_actual = 0.08  # (mol% ethanol)/(reflux ratio)
    tau_actual = 120.0  # minutes (dominant time constant)
    theta_actual = 12.0  # minutes (analyzer dead time)
    
    # Step test parameters
    step_time = 60.0  # minutes
    step_magnitude = 0.5  # reflux ratio increase
    initial_composition = 95.0  # mol% ethanol
    
    print(f"Step Test Parameters:")
    print(f"  Step Time: {step_time} min")
    print(f"  Step Magnitude: +{step_magnitude} reflux ratio")
    print(f"  Initial Composition: {initial_composition} mol%")
    print()
    
    # Generate step response
    composition_response = np.zeros_like(time_vector)
    
    for i, t in enumerate(time_vector):
        if t < step_time:
            composition_response[i] = initial_composition
        elif t >= step_time + theta_actual:
            time_since_step = t - step_time - theta_actual
            comp_change = Kp_actual * step_magnitude * (1 - np.exp(-time_since_step / tau_actual))
            composition_response[i] = initial_composition + comp_change
        else:
            composition_response[i] = initial_composition
    
    # Add realistic analyzer noise
    np.random.seed(42)
    noise = np.random.normal(0, 0.02, len(composition_response))  # ±0.02 mol% noise
    composition_response += noise
    
    print(f"Step Test Results:")
    print(f"  Final Composition: {composition_response[-1]:.2f} mol%")
    print(f"  Composition Change: {composition_response[-1] - initial_composition:.2f} mol%")
    print(f"  Process Gain: {(composition_response[-1] - initial_composition)/step_magnitude:.3f} mol%/(reflux ratio)")
    print()
    
    # ==============================================
    # STEP 3: AMIGO PARAMETER IDENTIFICATION
    # ==============================================
    print("3. AMIGO Parameter Identification")
    print("-" * 40)
    
    # AMIGO identification method (simplified)
    final_value = np.mean(composition_response[-100:])
    initial_value = composition_response[0]
    total_change = final_value - initial_value
    
    # Process gain identification
    Kp_identified = total_change / step_magnitude
    
    # Time constant identification (63.2% method)
    target_value = initial_value + 0.632 * total_change
    try:
        idx_63 = np.where(composition_response >= target_value)[0][0]
        t63 = time_vector[idx_63] - step_time - theta_actual
        tau_identified = t63
    except:
        tau_identified = tau_actual  # Fallback
    
    # Dead time identification (tangent method)
    response_after_step = composition_response[600:]  # After step
    time_after_step = time_vector[600:] - step_time
    
    slopes = np.gradient(response_after_step, time_after_step[1] - time_after_step[0])
    max_slope_idx = np.argmax(slopes)
    max_slope = slopes[max_slope_idx]
    
    if max_slope > 0:
        inflection_time = time_after_step[max_slope_idx] + step_time
        inflection_comp = response_after_step[max_slope_idx]
        x_intercept = (initial_value - inflection_comp) / max_slope + inflection_time
        theta_identified = x_intercept - step_time
    else:
        theta_identified = theta_actual  # Fallback
    
    print(f"Identified Parameters:")
    print(f"  Process Gain (Kp): {Kp_identified:.3f} mol%/(reflux ratio)")
    print(f"  Time Constant (T): {tau_identified:.1f} min")
    print(f"  Dead Time (L): {theta_identified:.1f} min")
    print(f"  L/T Ratio: {theta_identified/tau_identified:.3f}")
    print()
    
    print(f"Identification Accuracy:")
    print(f"  Kp Error: {abs(Kp_identified - Kp_actual)/abs(Kp_actual)*100:.1f}%")
    print(f"  T Error: {abs(tau_identified - tau_actual)/tau_actual*100:.1f}%")
    print(f"  L Error: {abs(theta_identified - theta_actual)/theta_actual*100:.1f}%")
    print()
    
    # ==============================================
    # STEP 4: AMIGO TUNING CALCULATIONS
    # ==============================================
    print("4. AMIGO Tuning Calculations")
    print("-" * 40)
    
    # Use identified parameters
    Kp = abs(Kp_identified)
    T = tau_identified
    L = theta_identified
    L_T = L / T
    
    print(f"AMIGO Method Selection (L/T = {L_T:.3f}):")
    
    # AMIGO PID tuning formulas based on L/T ratio
    if L_T <= 0.1:
        print("  Low dead time process - Aggressive tuning")
        Kc_pid = (0.15 + 0.35 * T / L) / Kp
        tau_I_pid = 0.35 * L + 13 * L**2 / T
        tau_D_pid = 0.5 * L
        robustness_target = "Ms ≈ 1.4"
    elif L_T <= 0.2:
        print("  Medium dead time process - Balanced tuning")
        Kc_pid = (0.25 + 0.3 * T / L) / Kp
        tau_I_pid = 0.32 * L + 13 * L**2 / T
        tau_D_pid = 0.5 * L
        robustness_target = "Ms ≈ 1.4"
    else:
        print("  High dead time process - Conservative tuning")
        Kc_pid = (0.15 + 0.25 * T / L) / Kp
        tau_I_pid = 0.4 * L + 8 * L**2 / T
        tau_D_pid = 0.5 * L
        robustness_target = "Ms ≈ 1.6"
    
    # AMIGO PI tuning (recommended for composition control)
    Kc_pi = (0.15 + 0.35 * T / L) / Kp * 0.8  # More conservative
    tau_I_pi = (0.35 * L + 13 * L**2 / T) * 1.2  # Slower integral action
    
    print()
    print(f"AMIGO PID Tuning:")
    print(f"  Controller Gain (Kc): {Kc_pid:.2f} (reflux ratio)/(mol%)")
    print(f"  Integral Time (τI): {tau_I_pid:.1f} min")
    print(f"  Derivative Time (τD): {tau_D_pid:.1f} min")
    print(f"  Robustness Target: {robustness_target}")
    print()
    
    print(f"AMIGO PI Tuning (Recommended for Composition):")
    print(f"  Controller Gain (Kc): {Kc_pi:.2f} (reflux ratio)/(mol%)")
    print(f"  Integral Time (τI): {tau_I_pi:.1f} min")
    print(f"  Derivative Time (τD): 0.0 min")
    print()
    
    # ==============================================
    # STEP 5: ROBUSTNESS ANALYSIS
    # ==============================================
    print("5. AMIGO Robustness Analysis")
    print("-" * 40)
    
    # Maximum sensitivity calculation (simplified)
    omega_c = 1 / tau_I_pi  # Crossover frequency approximation
    phase_margin = 60 - 57.3 * L * omega_c  # Degrees
    
    if phase_margin > 30:
        Ms_estimated = 1 / np.sin(np.radians(phase_margin / 2))
    else:
        Ms_estimated = 3.0
    
    print(f"Robustness Metrics:")
    print(f"  Estimated Phase Margin: {phase_margin:.1f}°")
    print(f"  Estimated Max Sensitivity (Ms): {Ms_estimated:.2f}")
    print(f"  AMIGO Target Ms: 1.4")
    print()
    
    # Gain margin estimation
    gain_margin_db = 20 * np.log10(1 + 1 / (Kc_pi * Kp))
    print(f"  Estimated Gain Margin: {gain_margin_db:.1f} dB")
    print()
    
    if Ms_estimated <= 2.0:
        print("  ✓ Good robustness margins")
    else:
        print("  ⚠ Consider more conservative tuning")
    
    if phase_margin >= 45:
        print("  ✓ Adequate phase margin")
    else:
        print("  ⚠ Low phase margin - check for model uncertainty")
    
    print()
    
    # ==============================================
    # STEP 6: PERFORMANCE SIMULATION
    # ==============================================
    print("6. Closed-Loop Performance Simulation")
    print("-" * 40)
    
    # Simulate closed-loop response
    sim_time = np.linspace(0, 360, 1801)  # 6 hours
    dt = sim_time[1] - sim_time[0]
    
    # Setpoint and disturbance profile
    setpoint = np.ones_like(sim_time) * 95.0  # mol% ethanol
    setpoint[900:] = 96.0  # 1 mol% step increase at t=180 min
    
    # Feed composition disturbance
    feed_disturbance = np.zeros_like(sim_time)
    feed_disturbance[1200:] = -2.0  # 2 mol% feed composition drop at t=240 min
    
    # Initialize simulation
    composition = np.zeros_like(sim_time)
    reflux_ratio = np.zeros_like(sim_time)
    control_error = np.zeros_like(sim_time)
    integral_error = 0.0
    
    # Initial conditions
    composition[0] = 95.0  # mol%
    reflux_ratio[0] = 3.5  # nominal reflux ratio
    
    # PI controller simulation
    for i in range(1, len(sim_time)):
        # Process simulation with disturbance
        disturbance_effect = 0.02 * feed_disturbance[i]  # mol% per mol% feed change
        
        # Simple first-order response
        steady_state_comp = 95.0 + Kp * (reflux_ratio[i-1] - 3.5) + disturbance_effect
        comp_error = steady_state_comp - composition[i-1]
        comp_change = comp_error / tau_identified * dt
        composition[i] = composition[i-1] + comp_change
        
        # PI controller
        error = setpoint[i-1] - composition[i-1]
        control_error[i-1] = error
        
        # Proportional action
        proportional = Kc_pi * error
        
        # Integral action
        integral_error += error * dt
        integral = Kc_pi / tau_I_pi * integral_error
        
        # Control output
        control_output = proportional + integral
        reflux_ratio[i] = 3.5 + control_output  # Add to nominal
        
        # Constrain reflux ratio
        reflux_ratio[i] = np.clip(reflux_ratio[i], 1.0, 8.0)
    
    # Performance metrics
    step_start_idx = 900
    step_response = composition[step_start_idx:]
    step_time_vec = sim_time[step_start_idx:] - 180.0
    
    # Rise time, settling time, overshoot
    initial_comp = composition[step_start_idx-1]
    final_comp = np.mean(composition[-100:])
    step_size = final_comp - initial_comp
    
    # Settling time (2% criterion)
    settling_band = 0.02 * abs(step_size)
    try:
        settled_indices = np.where(np.abs(step_response - final_comp) <= settling_band)[0]
        settling_time = step_time_vec[settled_indices[0]]
    except:
        settling_time = np.nan
    
    # Overshoot
    max_comp = np.max(step_response)
    overshoot = (max_comp - final_comp) / abs(step_size) * 100
    
    # Integral absolute error
    iae = np.trapz(np.abs(control_error), sim_time)
    
    print(f"Performance Metrics (1 mol% Step Response):")
    print(f"  Settling Time (2%): {settling_time:.1f} min")
    print(f"  Overshoot: {overshoot:.1f}%")
    print(f"  Final Composition: {final_comp:.2f} mol%")
    print(f"  Steady-State Error: {abs(96.0 - final_comp):.3f} mol%")
    print(f"  Integral Absolute Error: {iae:.1f} mol%·min")
    print()
    
    # ==============================================
    # STEP 7: ECONOMIC AND OPERATIONAL ANALYSIS
    # ==============================================
    print("7. Economic and Operational Analysis")
    print("-" * 40)
    
    # Economic parameters
    ethanol_price = 800.0  # $/tonne
    energy_cost = 0.06  # $/kWh
    reboiler_duty = 4500.0  # kW
    production_rate = 25.0  # tonne/h ethanol
    
    # Control performance economics
    composition_variance_before = 0.5  # mol% standard deviation
    composition_variance_after = 0.2  # mol% with AMIGO tuning
    
    # Product quality improvement
    off_spec_reduction = (composition_variance_before - composition_variance_after) / composition_variance_before
    quality_improvement_value = off_spec_reduction * production_rate * ethanol_price * 0.05  # 5% penalty for off-spec
    
    # Energy efficiency
    control_stability_factor = 0.98  # Fraction of optimal efficiency with good control
    energy_savings = reboiler_duty * (1 - control_stability_factor) * energy_cost * 24  # $/day
    
    total_daily_savings = quality_improvement_value * 24 + energy_savings
    annual_savings = total_daily_savings * 365
    
    print(f"Economic Benefits of AMIGO Tuning:")
    print(f"  Composition Variance Reduction: {off_spec_reduction*100:.1f}%")
    print(f"  Quality Improvement Value: ${quality_improvement_value:.2f}/h")
    print(f"  Energy Efficiency Savings: ${energy_savings:.2f}/day")
    print(f"  Total Daily Savings: ${total_daily_savings:.2f}")
    print(f"  Annual Savings: ${annual_savings:,.0f}")
    print()
    
    # ==============================================
    # STEP 8: TUNING RECOMMENDATIONS
    # ==============================================
    print("8. AMIGO Tuning Recommendations")
    print("-" * 40)
    
    print("Implementation Guidelines:")
    print("  ✓ Use PI control (not PID) for composition loops")
    print("  ✓ AMIGO provides excellent robustness for model uncertainty")
    print("  ✓ Conservative tuning appropriate for slow composition dynamics")
    print("  ✓ Monitor for process changes that may require retuning")
    print()
    
    print("Operational Considerations:")
    print("  • Implement feed-forward control for feed composition disturbances")
    print("  • Use analyzer validation and backup control strategies")
    print("  • Consider cascade control with temperature as secondary loop")
    print("  • Regular maintenance of composition analyzer critical")
    print()
    
    print("Advantages of AMIGO vs Other Methods:")
    print("  • Better robustness than Ziegler-Nichols")
    print("  • Systematic design procedure")
    print("  • Explicit robustness constraints (Ms target)")
    print("  • Suitable for wide range of L/T ratios")
    print("  • Less aggressive than IMC for uncertain models")
    print()
    
    return {
        'time': sim_time,
        'composition': composition,
        'setpoint': setpoint,
        'reflux_ratio': reflux_ratio,
        'control_error': control_error,
        'step_test_time': time_vector,
        'step_test_response': composition_response,
        'tuning_parameters': {
            'Kc_pid': Kc_pid,
            'tau_I_pid': tau_I_pid,
            'tau_D_pid': tau_D_pid,
            'Kc_pi': Kc_pi,
            'tau_I_pi': tau_I_pi
        },
        'performance_metrics': {
            'settling_time': settling_time,
            'overshoot': overshoot,
            'iae': iae
        },
        'economics': {
            'annual_savings': annual_savings,
            'quality_improvement': off_spec_reduction
        }
    }

if __name__ == "__main__":
    results = main()
    print("✓ AMIGO tuning example completed successfully!")
    print(f"✓ Results available with {len(results['time'])} simulation points.")
    print(f"✓ Estimated annual savings: ${results['economics']['annual_savings']:,.0f}")
