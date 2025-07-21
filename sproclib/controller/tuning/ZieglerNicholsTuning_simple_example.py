import numpy as np
import matplotlib.pyplot as plt

def main():
    """
    Ziegler-Nichols Tuning Example: CSTR Temperature Control
    
    This example demonstrates Ziegler-Nichols tuning methodology for a continuous
    stirred tank reactor (CSTR) temperature control system using cooling water flow.
    """
    
    print("=== Ziegler-Nichols Tuning Example: CSTR Temperature Control ===")
    print()
    
    # ==============================================
    # STEP 1: PROCESS STEP TESTING
    # ==============================================
    print("1. Process Step Test")
    print("-" * 40)
    
    # Simulate step test data
    time_vector = np.linspace(0, 60, 301)
    
    # CSTR process parameters (actual)
    Kp_actual = -2.5  # K per L/min cooling water (negative gain for cooling)
    tau_actual = 12.0  # minutes (thermal time constant)
    theta_actual = 0.8  # minutes (sensor + valve delays)
    
    print(f"Process Characteristics:")
    print(f"  Process Type: Exothermic CSTR with cooling")
    print(f"  Manipulated Variable: Cooling water flow (L/min)")
    print(f"  Controlled Variable: Reactor temperature (K)")
    print(f"  Operating Temperature: 350 K")
    print(f"  Step Test: +2 L/min cooling water at t=5 min")
    print()
    
    # Generate step response
    step_magnitude = 2.0  # L/min increase in cooling
    temperature_response = np.zeros_like(time_vector)
    initial_temp = 350.0  # K
    
    for i, t in enumerate(time_vector):
        if t < 5.0:
            temperature_response[i] = initial_temp
        elif t >= 5.0 + theta_actual:
            # First-order response with dead time
            time_since_step = t - 5.0 - theta_actual
            temp_change = Kp_actual * step_magnitude * (1 - np.exp(-time_since_step / tau_actual))
            temperature_response[i] = initial_temp + temp_change
        else:
            # Dead time period
            temperature_response[i] = initial_temp
    
    # Add realistic measurement noise
    np.random.seed(42)
    noise = np.random.normal(0, 0.1, len(temperature_response))
    temperature_response += noise
    
    print(f"Step Test Results:")
    print(f"  Initial Temperature: {initial_temp:.1f} K")
    print(f"  Final Temperature: {temperature_response[-1]:.1f} K")
    print(f"  Temperature Change: {temperature_response[-1] - initial_temp:.1f} K")
    print(f"  Step Magnitude: {step_magnitude} L/min")
    print()
    
    # ==============================================
    # STEP 2: PARAMETER IDENTIFICATION
    # ==============================================
    print("2. Parameter Identification (Tangent Line Method)")
    print("-" * 40)
    
    # Identify parameters using tangent line method
    final_value = np.mean(temperature_response[-20:])
    initial_value = temperature_response[0]
    total_change = final_value - initial_value
    
    # Find inflection point (maximum slope)
    # For first-order system, this occurs at t = θ + τ*ln(τ/(τ-θ)) ≈ θ + 0.63*τ
    response_after_step = temperature_response[50:]  # After step at t=5
    time_after_step = time_vector[50:] - 5.0
    
    # Calculate slopes
    slopes = np.gradient(response_after_step, time_after_step[1] - time_after_step[0])
    max_slope_idx = np.argmax(np.abs(slopes))
    max_slope = slopes[max_slope_idx]
    inflection_time = time_after_step[max_slope_idx] + 5.0
    inflection_temp = response_after_step[max_slope_idx]
    
    # Tangent line intercepts
    # y = mx + b, solve for x-intercept when y = initial_value
    x_intercept = (initial_value - inflection_temp) / max_slope + inflection_time
    dead_time_identified = x_intercept - 5.0  # Subtract step time
    
    # Solve for when tangent line reaches final value
    x_final = (final_value - inflection_temp) / max_slope + inflection_time
    time_constant_identified = x_final - x_intercept
    
    # Process gain
    process_gain_identified = total_change / step_magnitude
    
    print(f"Identified Parameters:")
    print(f"  Process Gain (Kp): {process_gain_identified:.2f} K/(L/min)")
    print(f"  Time Constant (T): {time_constant_identified:.1f} min")
    print(f"  Dead Time (L): {dead_time_identified:.1f} min")
    print(f"  Normalized Dead Time (L/T): {dead_time_identified/time_constant_identified:.3f}")
    print()
    
    print(f"Identification Accuracy:")
    print(f"  Kp Error: {abs(process_gain_identified - Kp_actual)/abs(Kp_actual)*100:.1f}%")
    print(f"  T Error: {abs(time_constant_identified - tau_actual)/tau_actual*100:.1f}%")
    print(f"  L Error: {abs(dead_time_identified - theta_actual)/theta_actual*100:.1f}%")
    print()
    
    # ==============================================
    # STEP 3: ZIEGLER-NICHOLS TUNING
    # ==============================================
    print("3. Ziegler-Nichols Tuning Calculations")
    print("-" * 40)
    
    # Use identified parameters for tuning
    Kp = abs(process_gain_identified)  # Use absolute value for calculations
    T = time_constant_identified
    L = dead_time_identified
    
    # ZN PID tuning formulas
    Kc_pid = 1.2 * T / (Kp * L)
    tau_I_pid = 2 * L
    tau_D_pid = 0.5 * L
    
    # ZN PI tuning formulas (often preferred for temperature control)
    Kc_pi = 0.9 * T / (Kp * L)
    tau_I_pi = 3.3 * L
    
    print(f"Ziegler-Nichols PID Tuning:")
    print(f"  Proportional Gain (Kc): {Kc_pid:.2f} (L/min)/K")
    print(f"  Integral Time (τI): {tau_I_pid:.1f} min")
    print(f"  Derivative Time (τD): {tau_D_pid:.1f} min")
    print()
    
    print(f"Ziegler-Nichols PI Tuning (Recommended for Temperature):")
    print(f"  Proportional Gain (Kc): {Kc_pi:.2f} (L/min)/K")
    print(f"  Integral Time (τI): {tau_I_pi:.1f} min")
    print(f"  Derivative Time (τD): 0.0 min")
    print()
    
    # ==============================================
    # STEP 4: PERFORMANCE SIMULATION
    # ==============================================
    print("4. Closed-Loop Performance Simulation")
    print("-" * 40)
    
    # Simulate closed-loop response
    sim_time = np.linspace(0, 100, 501)
    dt = sim_time[1] - sim_time[0]
    
    # Setpoint profile
    setpoint = np.ones_like(sim_time) * 350.0  # K
    setpoint[250:] = 355.0  # 5K step increase at t=50 min
    
    # Initialize simulation variables
    temperature = np.zeros_like(sim_time)
    cooling_flow = np.zeros_like(sim_time)
    control_error = np.zeros_like(sim_time)
    integral_error = 0.0
    previous_error = 0.0
    
    # Initial conditions
    temperature[0] = 350.0  # K
    cooling_flow[0] = 20.0  # L/min (nominal)
    
    # PID controller simulation (simplified)
    for i in range(1, len(sim_time)):
        # Current error
        error = setpoint[i-1] - temperature[i-1]
        control_error[i-1] = error
        
        # PID calculation (using ZN PI tuning)
        proportional = Kc_pi * error
        
        # Integral term (trapezoidal integration)
        integral_error += error * dt
        integral = Kc_pi / tau_I_pi * integral_error
        
        # Derivative term (not used for PI)
        derivative = 0.0
        
        # Control output
        control_output = proportional + integral + derivative
        cooling_flow[i] = 20.0 + control_output  # Add to nominal flow
        
        # Constrain cooling flow (realistic limits)
        cooling_flow[i] = np.clip(cooling_flow[i], 5.0, 50.0)
        
        # Process simulation (first-order with dead time, simplified)
        flow_change = cooling_flow[i] - 20.0  # Change from nominal
        
        # Simple first-order response (ignoring dead time for simplicity)
        steady_state_temp = 350.0 + Kp_actual * flow_change
        temp_error = steady_state_temp - temperature[i-1]
        temp_change = temp_error / tau_actual * dt
        
        temperature[i] = temperature[i-1] + temp_change
    
    # Calculate performance metrics
    step_start_idx = 250
    step_response = temperature[step_start_idx:]
    step_time = sim_time[step_start_idx:] - 50.0
    
    # Rise time (10% to 90% of step)
    initial_temp = temperature[step_start_idx-1]
    final_temp = np.mean(temperature[-50:])
    step_size = final_temp - initial_temp
    
    temp_10 = initial_temp + 0.1 * step_size
    temp_90 = initial_temp + 0.9 * step_size
    
    try:
        idx_10 = np.where(step_response >= temp_10)[0][0]
        idx_90 = np.where(step_response >= temp_90)[0][0]
        rise_time = step_time[idx_90] - step_time[idx_10]
    except:
        rise_time = np.nan
    
    # Settling time (within 2% of final value)
    settling_band = 0.02 * abs(step_size)
    try:
        settled_indices = np.where(np.abs(step_response - final_temp) <= settling_band)[0]
        settling_time = step_time[settled_indices[0]]
    except:
        settling_time = np.nan
    
    # Overshoot
    max_temp = np.max(step_response)
    overshoot = (max_temp - final_temp) / abs(step_size) * 100
    
    # Integral Absolute Error
    iae = np.trapz(np.abs(control_error), sim_time)
    
    print(f"Performance Metrics (5K Step Response):")
    print(f"  Rise Time (10%-90%): {rise_time:.1f} min")
    print(f"  Settling Time (2%): {settling_time:.1f} min")
    print(f"  Overshoot: {overshoot:.1f}%")
    print(f"  Final Temperature: {final_temp:.1f} K")
    print(f"  Steady-State Error: {abs(355.0 - final_temp):.2f} K")
    print(f"  Integral Absolute Error: {iae:.1f} K·min")
    print()
    
    # ==============================================
    # STEP 5: TUNING RECOMMENDATIONS
    # ==============================================
    print("5. Tuning Recommendations")
    print("-" * 40)
    
    print("Standard ZN Tuning Assessment:")
    if overshoot > 20:
        print("  ⚠ High overshoot detected - consider conservative tuning")
        print("  ⚠ Reduce Kc by 20-30% for smoother response")
    elif overshoot < 5:
        print("  ✓ Conservative response - acceptable for temperature control")
    else:
        print("  ✓ Moderate overshoot - good balance of speed and stability")
    
    if settling_time > 20:
        print("  ⚠ Slow settling - consider increasing Kc or decreasing τI")
    else:
        print("  ✓ Acceptable settling time for thermal process")
    
    print()
    print("Process-Specific Recommendations:")
    print("  • Use PI control (not PID) for temperature loops to avoid derivative kick")
    print("  • Consider conservative tuning (Kc × 0.8) for safety-critical processes")  
    print("  • Implement anti-windup protection for valve saturation")
    print("  • Monitor for process changes that may require retuning")
    print()
    
    # ==============================================
    # STEP 6: ECONOMIC ANALYSIS
    # ==============================================
    print("6. Economic Impact Analysis")
    print("-" * 40)
    
    # Economic parameters
    cooling_cost = 0.02  # $/L cooling water
    off_spec_cost = 5.0  # $/K·min temperature deviation
    production_rate = 1000  # kg/h
    
    # Calculate costs
    cooling_usage = np.trapz(cooling_flow - 20.0, sim_time) / 60  # L (convert min to h)
    cooling_cost_total = abs(cooling_usage) * cooling_cost
    
    temp_deviation = np.abs(temperature - setpoint)
    off_spec_cost_total = np.trapz(temp_deviation, sim_time) * off_spec_cost / 60
    
    total_cost = cooling_cost_total + off_spec_cost_total
    
    print(f"Operating Costs (100-minute simulation):")
    print(f"  Cooling Water Cost: ${cooling_cost_total:.2f}")
    print(f"  Off-Specification Cost: ${off_spec_cost_total:.2f}")
    print(f"  Total Cost: ${total_cost:.2f}")
    print()
    
    # Compare with manual control
    manual_deviation = 3.0  # K average deviation with manual control
    manual_cost = manual_deviation * 100 * off_spec_cost / 60
    savings = manual_cost - off_spec_cost_total
    
    print(f"Manual Control Comparison:")
    print(f"  Manual Control Cost: ${manual_cost:.2f}")
    print(f"  ZN Tuning Savings: ${savings:.2f} ({savings/manual_cost*100:.1f}%)")
    print()
    
    return {
        'time': sim_time,
        'temperature': temperature,
        'setpoint': setpoint,
        'cooling_flow': cooling_flow,
        'control_error': control_error,
        'step_test_time': time_vector,
        'step_test_response': temperature_response,
        'tuning_parameters': {
            'Kc_pid': Kc_pid,
            'tau_I_pid': tau_I_pid,
            'tau_D_pid': tau_D_pid,
            'Kc_pi': Kc_pi,
            'tau_I_pi': tau_I_pi
        },
        'performance_metrics': {
            'rise_time': rise_time,
            'settling_time': settling_time,
            'overshoot': overshoot,
            'iae': iae
        }
    }

if __name__ == "__main__":
    results = main()
    print("✓ Ziegler-Nichols tuning example completed successfully!")
    print(f"✓ Results available with {len(results['time'])} simulation points.")
