"""
Industrial Example: Centrifugal Pump in Water Treatment Plant
Typical plant conditions and pump curve analysis for centrifugal pump
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the sproclib directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sproclib'))

from sproclib.unit.pump.CentrifugalPump import CentrifugalPump

def main():
    print("=" * 70)
    print("CENTRIFUGAL PUMP - WATER TREATMENT PLANT APPLICATION")
    print("=" * 70)
    print()
    
    # Process conditions (typical water treatment plant)
    print("PROCESS CONDITIONS:")
    print("-" * 20)
    pressure_inlet = 1.5e5      # Pa (1.5 bar absolute)
    temperature = 288           # K (15°C)
    fluid_density = 1000        # kg/m³ (water)
    viscosity = 1.12e-3         # Pa·s (water at 15°C)
    
    print(f"Inlet Pressure:     {pressure_inlet/1e5:.1f} bar")
    print(f"Temperature:        {temperature-273.15:.1f} °C")
    print(f"Fluid Density:      {fluid_density:.0f} kg/m³")
    print(f"Viscosity:          {viscosity*1000:.2f} cP")
    print()
    
    # Create centrifugal pump with realistic parameters
    # Based on typical high-service pump in water treatment
    pump = CentrifugalPump(
        H0=80.0,                    # 80 m shutoff head
        K=25.0,                     # Head-flow coefficient
        eta=0.82,                   # 82% efficiency (high-efficiency pump)
        rho=fluid_density,
        name="HighServicePump"
    )
    
    print("PUMP SPECIFICATIONS:")
    print("-" * 20)
    print(f"Pump Type:          Centrifugal (End Suction)")
    print(f"Shutoff Head:       {pump.H0:.1f} m")
    print(f"Head Coefficient:   {pump.K:.1f} s²/m⁵")
    print(f"Design Efficiency:  {pump.eta:.1%}")
    print(f"Impeller Diameter:  ~400 mm (estimated)")
    print(f"Speed:              1450 rpm (estimated)")
    print()
    
    # Calculate pump curve characteristics
    Q_max = np.sqrt(pump.H0 / pump.K)  # Maximum flow (H = 0)
    Q_bep = 0.75 * Q_max  # Best efficiency point (75% of max flow)
    
    print("PUMP CURVE CHARACTERISTICS:")
    print("-" * 30)
    print(f"Maximum Flow:       {Q_max:.3f} m³/s ({Q_max*3600:.0f} m³/h)")
    print(f"BEP Flow (est):     {Q_bep:.3f} m³/s ({Q_bep*3600:.0f} m³/h)")
    print(f"Operating Range:    {0.5*Q_bep:.3f} - {1.2*Q_bep:.3f} m³/s")
    print()
    
    # Detailed pump curve analysis
    print("PUMP CURVE ANALYSIS:")
    print("-" * 25)
    flow_range = np.linspace(0, Q_max*0.95, 10)
    
    print("Flow Rate   Head    ΔP      Power   Efficiency")
    print("(m³/s)      (m)     (bar)   (kW)    (%)")
    print("-" * 50)
    
    pump_curve_data = []
    for Q in flow_range:
        u = np.array([pressure_inlet, Q])
        P_outlet, Power = pump.steady_state(u)
        
        delta_P = P_outlet - pressure_inlet
        head = delta_P / (pump.rho * 9.81)
        
        # Calculate hydraulic efficiency
        hydraulic_power = Q * delta_P
        efficiency = hydraulic_power / Power if Power > 0 else 0
        
        pump_curve_data.append([Q, head, delta_P/1e5, Power/1000, efficiency*100])
        
        if Q > 0:  # Skip zero flow for cleaner output
            print(f"{Q:.3f}       {head:.1f}   {delta_P/1e5:.2f}    {Power/1000:.1f}     {efficiency*100:.1f}")
    
    print()
    
    # Operating point analysis for design flow
    design_flow = Q_bep
    u_design = np.array([pressure_inlet, design_flow])
    P_out_design, Power_design = pump.steady_state(u_design)
    head_design = (P_out_design - pressure_inlet) / (pump.rho * 9.81)
    
    print("DESIGN OPERATING POINT:")
    print("-" * 25)
    print(f"Design Flow:        {design_flow:.3f} m³/s ({design_flow*3600:.0f} m³/h)")
    print(f"Design Head:        {head_design:.1f} m")
    print(f"Design Power:       {Power_design/1000:.1f} kW")
    print(f"Outlet Pressure:    {P_out_design/1e5:.1f} bar")
    print(f"Pressure Rise:      {(P_out_design-pressure_inlet)/1e5:.1f} bar")
    print()
    
    # Affinity laws demonstration
    print("AFFINITY LAWS ANALYSIS:")
    print("-" * 25)
    
    # Different speeds (VFD operation)
    speeds = [0.8, 1.0, 1.2]  # 80%, 100%, 120% speed
    base_speed = 1450  # rpm
    
    print("Speed   Flow    Head    Power")
    print("(rpm)   (m³/s)  (m)     (kW)")
    print("-" * 30)
    
    for speed_ratio in speeds:
        # Affinity laws: Q ∝ N, H ∝ N², P ∝ N³
        Q_adj = design_flow * speed_ratio
        
        # Create adjusted pump parameters
        H0_adj = pump.H0 * speed_ratio**2
        K_adj = pump.K / speed_ratio**2
        
        adj_pump = CentrifugalPump(H0=H0_adj, K=K_adj, eta=pump.eta, rho=pump.rho)
        u_adj = np.array([pressure_inlet, Q_adj])
        P_out_adj, Power_adj = adj_pump.steady_state(u_adj)
        
        head_adj = (P_out_adj - pressure_inlet) / (pump.rho * 9.81)
        
        print(f"{base_speed*speed_ratio:.0f}    {Q_adj:.3f}   {head_adj:.1f}   {Power_adj/1000:.1f}")
    
    print()
    
    # NPSH and cavitation analysis
    print("NPSH AND CAVITATION ANALYSIS:")
    print("-" * 35)
    
    # Estimate NPSH required (typical correlation)
    # NPSH_req ≈ 0.2 * (Q/Q_bep)^1.5 * H_design
    npsh_factors = np.array([0.5, 0.75, 1.0, 1.25, 1.5])  # Flow ratios
    
    print("Flow Ratio  NPSH_req  Min Suction P")
    print("(Q/Q_bep)   (m)       (bar abs)")
    print("-" * 35)
    
    for factor in npsh_factors:
        Q_ratio = factor
        npsh_req = 0.2 * factor**1.5 * head_design  # Estimated correlation
        
        # Minimum suction pressure to avoid cavitation
        # P_suction > P_vapor + ρ*g*NPSH_req + P_friction
        P_vapor = 2300  # Pa (water vapor pressure at 15°C)
        P_friction = 5000  # Pa (estimated suction line losses)
        P_min_suction = P_vapor + pump.rho * 9.81 * npsh_req + P_friction
        
        print(f"{Q_ratio:.2f}        {npsh_req:.1f}     {P_min_suction/1e5:.2f}")
    
    print()
    
    # System curve intersection
    print("SYSTEM CURVE ANALYSIS:")
    print("-" * 25)
    
    # Typical system: static head + friction losses
    static_head = 45.0  # m (elevation + pressure)
    friction_coeff = 15.0  # s²/m⁵ (system resistance)
    
    print("System Equation: H_sys = H_static + K_sys * Q²")
    print(f"Static Head:     {static_head:.1f} m")
    print(f"System K:        {friction_coeff:.1f} s²/m⁵")
    print()
    
    # Find intersection point (pump curve = system curve)
    # H0 - K_pump*Q² = H_static + K_sys*Q²
    # Q² = (H0 - H_static) / (K_pump + K_sys)
    K_total = pump.K + friction_coeff
    Q_operating = np.sqrt((pump.H0 - static_head) / K_total)
    H_operating = pump.H0 - pump.K * Q_operating**2
    
    u_operating = np.array([pressure_inlet, Q_operating])
    P_out_op, Power_op = pump.steady_state(u_operating)
    
    print("OPERATING POINT (System Intersection):")
    print("-" * 40)
    print(f"Operating Flow:     {Q_operating:.3f} m³/s ({Q_operating*3600:.0f} m³/h)")
    print(f"Operating Head:     {H_operating:.1f} m")
    print(f"Operating Power:    {Power_op/1000:.1f} kW")
    print(f"Flow vs BEP:        {100*Q_operating/Q_bep:.0f}% of BEP")
    print()
    
    # Energy and cost analysis
    print("ENERGY AND COST ANALYSIS:")
    print("-" * 30)
    
    operating_hours = 6000  # hours/year (water treatment plant)
    electricity_cost = 0.09  # $/kWh
    motor_efficiency = 0.94  # High-efficiency motor
    
    brake_power = Power_op / motor_efficiency
    annual_energy = brake_power/1000 * operating_hours
    annual_cost = annual_energy * electricity_cost
    
    print(f"Motor Efficiency:   {motor_efficiency:.1%}")
    print(f"Brake Power:        {brake_power/1000:.1f} kW")
    print(f"Operating Hours:    {operating_hours:,} h/year")
    print(f"Annual Energy:      {annual_energy:,.0f} kWh/year")
    print(f"Annual Cost:        ${annual_cost:,.0f}/year")
    print()
    
    # Performance comparison with handbook data
    print("PERFORMANCE COMPARISON:")
    print("-" * 25)
    
    # Specific speed calculation (US units for comparison)
    # Ns = N * sqrt(Q) / H^0.75 (rpm, gpm, ft)
    Q_gpm = Q_operating * 15850  # Convert m³/s to gpm
    H_ft = H_operating * 3.281   # Convert m to ft
    N_rpm = 1450  # Assumed speed
    
    specific_speed = N_rpm * np.sqrt(Q_gpm) / (H_ft**0.75)
    
    print(f"Specific Speed:     {specific_speed:.0f} (US units)")
    print(f"Pump Classification: ", end="")
    if specific_speed < 1000:
        print("Radial flow (high head, low flow)")
    elif specific_speed < 4000:
        print("Mixed flow (medium head, medium flow)")
    else:
        print("Axial flow (low head, high flow)")
    
    print()
    print("Comparison with Pump Handbook (Karassik):")
    print(f"Expected Efficiency: 78-85% for this specific speed")
    print(f"Actual Efficiency:   {pump.eta:.1%}")
    print(f"Performance Rating:  {'Excellent' if pump.eta > 0.80 else 'Good' if pump.eta > 0.75 else 'Fair'}")
    
    return pump_curve_data, Q_operating, H_operating, Power_op

if __name__ == "__main__":
    curve_data, Q_op, H_op, P_op = main()
