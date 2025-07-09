#!/usr/bin/env python3
"""
IMC Controller Examples for SPROCLIB

This script demonstrates the use of Internal Model Control (IMC) for various
chemical process applications including continuous reactors, pH control, 
and heat exchangers.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def continuous_reactor_example():
    """
    Example: IMC control of a continuous reactor temperature.
    
    Process: CSTR with first-order kinetics
    Model: G(s) = 1.8*exp(-0.8s)/(12s+1)
    """
    print("=" * 60)
    print("IMC CONTROLLER EXAMPLE: CONTINUOUS REACTOR")
    print("=" * 60)
    
    # Import IMC components
    from controller.model_based.IMCController import IMCController, FOPDTModel, tune_imc_lambda
    
    # Process model: Reactor temperature response to coolant flow
    # K = 1.8 K/(L/min), tau = 12 min, theta = 0.8 min (sensor delay)
    reactor_model = FOPDTModel(K=1.8, tau=12.0, theta=0.8)
    
    print(f"Reactor Model: G(s) = {reactor_model.K}*exp(-{reactor_model.theta}s)/({reactor_model.tau}s+1)")
    
    # Tune IMC for good performance (settling time ~30 min)
    lambda_c = tune_imc_lambda(reactor_model, desired_settling_time=30.0, overshoot_limit=0.02)
    
    # Create IMC controller
    imc = IMCController(reactor_model, filter_time_constant=lambda_c, name="Reactor_IMC")
    imc.set_output_limits(0, 20)  # Coolant flow limits: 0-20 L/min
    
    # Display tuning parameters
    params = imc.get_tuning_parameters()
    print(f"IMC Tuning: λ = {params['lambda_c']:.2f} min")
    print(f"Equivalent PID: Kp = {params['equivalent_Kp']:.3f}, Ki = {params['equivalent_Ki']:.4f}, Kd = {params['equivalent_Kd']:.3f}")
    
    # Simulation setup
    dt = 0.2  # 0.2 min time step
    t_final = 60.0  # 1 hour simulation
    t = np.arange(0, t_final, dt)
    
    # Setpoint changes: step changes in reactor temperature
    setpoint = np.ones_like(t) * 300.0  # 300°C base temperature
    setpoint[(t >= 10) & (t < 30)] = 310.0  # +10°C step at t=10min
    setpoint[t >= 40] = 295.0  # -5°C step at t=40min
    
    # Add disturbance (feed temperature change)
    disturbance = np.zeros_like(t)
    disturbance[(t >= 20) & (t < 35)] = -3.0  # -3°C feed temp disturbance
    
    # Initialize simulation arrays
    temperature = np.full_like(t, 300.0)  # Start at 300°C
    coolant_flow = np.zeros_like(t)
    
    print("\nSimulating reactor temperature control...")
    
    # Simulation loop
    for i in range(1, len(t)):
        # IMC controller update
        coolant_flow[i] = imc.update(t[i], setpoint[i], temperature[i-1])
        
        # Simple reactor dynamics (first-order + dead time approximation)
        if t[i] > reactor_model.theta:
            # Temperature response to coolant flow + disturbance
            tau_eff = reactor_model.tau
            K_eff = reactor_model.K
            temp_change = dt * (K_eff * coolant_flow[i-1] + disturbance[i] - temperature[i-1] + 300.0) / tau_eff
            temperature[i] = temperature[i-1] + temp_change
        else:
            temperature[i] = temperature[i-1] + disturbance[i] * 0.1  # Small direct effect
    
    # Performance analysis
    settling_indices = []
    for step_time in [10, 40]:
        step_idx = int(step_time / dt)
        if step_idx < len(t) - 50:
            final_temp = temperature[step_idx + 50:].mean()
            target_temp = setpoint[step_idx + 10]
            error_threshold = 0.02 * abs(target_temp - temperature[step_idx])
            
            for j in range(step_idx + 5, len(t)):
                if abs(temperature[j] - final_temp) <= error_threshold:
                    settling_time = t[j] - t[step_idx]
                    settling_indices.append((step_time, settling_time))
                    break
    
    print(f"\nPerformance Results:")
    for step_time, settling_time in settling_indices:
        print(f"  Step at {step_time} min: Settling time = {settling_time:.1f} min")
    
    print(f"  Final steady-state error: {abs(temperature[-1] - setpoint[-1]):.2f}°C")
    print(f"  Max coolant flow used: {coolant_flow.max():.1f} L/min")
    
    return t, temperature, setpoint, coolant_flow, disturbance


def ph_control_example():
    """
    Example: IMC control of pH in a neutralization process.
    
    pH control is highly nonlinear, but can be approximated with FOPDT around operating point.
    """
    print("\n" + "=" * 60)
    print("IMC CONTROLLER EXAMPLE: pH CONTROL")
    print("=" * 60)
    
    from controller.model_based.IMCController import IMCController, FOPDTModel, tune_imc_lambda
    
    # Linearized pH model around pH 7 (acid addition response)
    # K = -0.8 pH/(mL/min), tau = 2.5 min, theta = 0.3 min (mixing delay)
    ph_model = FOPDTModel(K=-0.8, tau=2.5, theta=0.3)
    
    print(f"pH Model (linearized): G(s) = {ph_model.K}*exp(-{ph_model.theta}s)/({ph_model.tau}s+1)")
    
    # Aggressive tuning for fast pH control (settling time ~8 min)
    lambda_c = tune_imc_lambda(ph_model, desired_settling_time=8.0, overshoot_limit=0.01)
    
    # Create IMC controller  
    ph_imc = IMCController(ph_model, filter_time_constant=lambda_c, name="pH_IMC")
    ph_imc.set_output_limits(0, 50)  # Acid dosing: 0-50 mL/min
    
    params = ph_imc.get_tuning_parameters()
    print(f"IMC Tuning: λ = {params['lambda_c']:.2f} min")
    print(f"Equivalent PID: Kp = {params['equivalent_Kp']:.3f}, Ki = {params['equivalent_Ki']:.4f}")
    
    # Simulation
    dt = 0.1
    t_final = 30.0
    t = np.arange(0, t_final, dt)
    
    # pH setpoint profile
    ph_setpoint = np.full_like(t, 7.0)  # Target pH 7
    ph_setpoint[(t >= 5) & (t < 15)] = 6.8  # Lower pH period
    ph_setpoint[t >= 20] = 7.2  # Higher pH period
    
    # Disturbances (base solution addition)
    base_disturbance = np.zeros_like(t)
    base_disturbance[(t >= 10) & (t < 12)] = 0.3  # pH increase disturbance
    
    # Initialize
    ph = np.full_like(t, 7.0)
    acid_flow = np.zeros_like(t)
    
    print("\nSimulating pH control...")
    
    # Simulation loop
    for i in range(1, len(t)):
        acid_flow[i] = ph_imc.update(t[i], ph_setpoint[i], ph[i-1])
        
        # pH dynamics (simplified)
        if t[i] > ph_model.theta:
            ph_change = dt * (ph_model.K * acid_flow[i-1] + base_disturbance[i] - (ph[i-1] - 7.0)) / ph_model.tau
            ph[i] = ph[i-1] + ph_change
        else:
            ph[i] = ph[i-1] + base_disturbance[i] * 0.05
    
    print(f"\nPH Control Results:")
    print(f"  Max pH deviation: ±{max(abs(ph - ph_setpoint)):.3f} pH units")
    print(f"  Average acid consumption: {acid_flow.mean():.1f} mL/min")
    print(f"  Max acid flow: {acid_flow.max():.1f} mL/min")
    
    return t, ph, ph_setpoint, acid_flow


def heat_exchanger_example():
    """
    Example: IMC control of heat exchanger outlet temperature.
    
    Controlling hot fluid outlet temperature by manipulating coolant flow.
    """
    print("\n" + "=" * 60)
    print("IMC CONTROLLER EXAMPLE: HEAT EXCHANGER")
    print("=" * 60)
    
    from controller.model_based.IMCController import IMCController, SOPDTModel
    
    # Heat exchanger model: Second-order response due to thermal masses
    # G(s) = -2.5*exp(-1.2s)/((8s+1)(3s+1))
    # Negative gain: increased coolant flow decreases hot outlet temperature
    hx_model = SOPDTModel(K=-2.5, tau1=8.0, tau2=3.0, theta=1.2)
    
    print(f"Heat Exchanger Model: G(s) = {hx_model.K}*exp(-{hx_model.theta}s)/")
    print(f"                            (({hx_model.tau1}s+1)({hx_model.tau2}s+1))")
    
    # Conservative tuning for stable operation
    lambda_c = 6.0  # Manual selection for heat exchanger
    
    hx_imc = IMCController(hx_model, filter_time_constant=lambda_c, 
                          filter_order=2, name="HeatExchanger_IMC")
    hx_imc.set_output_limits(10, 100)  # Coolant flow: 10-100 L/min
    
    params = hx_imc.get_tuning_parameters()
    print(f"IMC Tuning: λ = {params['lambda_c']:.1f} min, Filter Order = 2")
    print(f"Equivalent PID: Kp = {params['equivalent_Kp']:.3f}, Ki = {params['equivalent_Ki']:.4f}")
    
    # Simulation
    dt = 0.2
    t_final = 80.0
    t = np.arange(0, t_final, dt)
    
    # Temperature setpoint changes
    temp_setpoint = np.full_like(t, 180.0)  # 180°C target
    temp_setpoint[t >= 25] = 175.0  # Reduce to 175°C
    temp_setpoint[t >= 50] = 185.0  # Increase to 185°C
    
    # Hot inlet temperature disturbances
    inlet_temp_disturbance = np.zeros_like(t)
    inlet_temp_disturbance[(t >= 15) & (t < 30)] = 5.0  # +5°C inlet temp
    inlet_temp_disturbance[(t >= 60) & (t < 70)] = -8.0  # -8°C inlet temp
    
    # Initialize
    hot_outlet_temp = np.full_like(t, 180.0)
    coolant_flow = np.full_like(t, 45.0)  # Start at 45 L/min
    
    print("\nSimulating heat exchanger temperature control...")
    
    # Simulation loop  
    for i in range(1, len(t)):
        coolant_flow[i] = hx_imc.update(t[i], temp_setpoint[i], hot_outlet_temp[i-1])
        
        # Heat exchanger dynamics (second-order approximation)
        if t[i] > hx_model.theta:
            # Combined time constant for second-order system
            tau_eq = hx_model.tau1 + hx_model.tau2
            temp_change = dt * (hx_model.K * coolant_flow[i-1] + 
                              inlet_temp_disturbance[i] * 0.8 +  # Inlet temp effect
                              (180.0 - hot_outlet_temp[i-1])) / tau_eq
            hot_outlet_temp[i] = hot_outlet_temp[i-1] + temp_change
        else:
            hot_outlet_temp[i] = hot_outlet_temp[i-1] + inlet_temp_disturbance[i] * 0.1
    
    print(f"\nHeat Exchanger Control Results:")
    print(f"  Max temperature deviation: ±{max(abs(hot_outlet_temp - temp_setpoint)):.2f}°C")
    print(f"  Coolant flow range: {coolant_flow.min():.1f} - {coolant_flow.max():.1f} L/min")
    print(f"  Average coolant consumption: {coolant_flow.mean():.1f} L/min")
    
    return t, hot_outlet_temp, temp_setpoint, coolant_flow


if __name__ == "__main__":
    print("IMC CONTROLLER APPLICATION EXAMPLES")
    print("Demonstrating Internal Model Control for Chemical Processes")
    
    try:
        # Run examples
        reactor_results = continuous_reactor_example()
        ph_results = ph_control_example()  
        hx_results = heat_exchanger_example()
        
        print("\n" + "=" * 60)
        print("ALL IMC EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nKey Benefits of IMC Demonstrated:")
        print("✓ Excellent setpoint tracking")
        print("✓ Good disturbance rejection")  
        print("✓ Systematic tuning based on process model")
        print("✓ Suitable for processes with dead time")
        print("✓ Equivalent PID parameters for implementation")
        
        print("\nApplications Covered:")
        print("• Continuous Reactor Temperature Control")
        print("• pH Control in Neutralization Process")
        print("• Heat Exchanger Temperature Control")
        
    except Exception as e:
        print(f"\nError running IMC examples: {e}")
        import traceback
        traceback.print_exc()
