"""
Industrial Example: Positive Displacement Pump in Chemical Injection System
High-pressure metering application with constant flow characteristics
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the sproclib directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sproclib'))

from sproclib.unit.pump.PositiveDisplacementPump import PositiveDisplacementPump

def main():
    print("=" * 75)
    print("POSITIVE DISPLACEMENT PUMP - CHEMICAL INJECTION APPLICATION")
    print("=" * 75)
    print()
    
    # Process conditions (chemical injection system)
    print("PROCESS CONDITIONS:")
    print("-" * 20)
    pressure_inlet = 1.0e5      # Pa (1.0 bar - atmospheric tank)
    pressure_system = 25.0e5    # Pa (25 bar - high pressure process)
    temperature = 298           # K (25°C)
    fluid_density = 1150        # kg/m³ (corrosion inhibitor solution)
    viscosity = 5.2e-3          # Pa·s (5.2 cP - moderate viscosity)
    
    print(f"Inlet Pressure:     {pressure_inlet/1e5:.1f} bar (atmospheric tank)")
    print(f"System Pressure:    {pressure_system/1e5:.1f} bar (process line)")
    print(f"Temperature:        {temperature-273.15:.1f} °C")
    print(f"Fluid Density:      {fluid_density:.0f} kg/m³")
    print(f"Viscosity:          {viscosity*1000:.1f} cP")
    print()
    
    # Create positive displacement pump for chemical injection
    # Typical metering pump for corrosion inhibitor injection
    pump = PositiveDisplacementPump(
        flow_rate=0.0028,               # 10 m³/h = 2.8×10⁻³ m³/s
        eta=0.85,                       # 85% efficiency (typical for PD pumps)
        rho=fluid_density,
        name="ChemicalMeteringPump"
    )
    
    # Calculate required pressure rise
    delta_P_required = pressure_system - pressure_inlet + 2.0e5  # +2 bar safety margin
    pump.delta_P_nominal = delta_P_required
    
    print("PUMP SPECIFICATIONS:")
    print("-" * 20)
    print(f"Pump Type:          Positive Displacement (Diaphragm)")
    print(f"Flow Rate:          {pump.flow_rate:.4f} m³/s ({pump.flow_rate*3600:.1f} m³/h)")
    print(f"Required ΔP:        {delta_P_required/1e5:.1f} bar")
    print(f"Efficiency:         {pump.eta:.1%}")
    print(f"Displacement:       ~47 mL/stroke (estimated)")
    print(f"Stroke Rate:        ~60 strokes/min (estimated)")
    print()
    
    # Steady-state performance at design conditions
    u_design = np.array([pressure_inlet])
    P_outlet_design, Power_design = pump.steady_state(u_design)
    
    print("DESIGN POINT PERFORMANCE:")
    print("-" * 30)
    print(f"Inlet Pressure:     {pressure_inlet/1e5:.1f} bar")
    print(f"Outlet Pressure:    {P_outlet_design/1e5:.1f} bar")
    print(f"Pressure Rise:      {(P_outlet_design-pressure_inlet)/1e5:.1f} bar")
    print(f"Hydraulic Power:    {Power_design/1000:.2f} kW")
    print(f"Brake Power:        {Power_design/(pump.eta*1000):.2f} kW")
    print(f"Motor Size:         1.5 kW (recommended with safety factor)")
    print()
    
    # Performance at different discharge pressures
    print("PRESSURE CAPABILITY ANALYSIS:")
    print("-" * 35)
    
    system_pressures = np.array([10, 15, 20, 25, 30]) * 1e5  # bar to Pa
    
    print("System P   Outlet P   ΔP      Power   Torque")
    print("(bar)      (bar)      (bar)   (kW)    (N·m)")
    print("-" * 45)
    
    pressure_performance = []
    for P_sys in system_pressures:
        # Adjust required pressure rise
        pump.delta_P_nominal = P_sys - pressure_inlet + 2.0e5  # +2 bar margin
        
        u = np.array([pressure_inlet])
        P_out, Power = pump.steady_state(u)
        
        # Estimate torque (assuming displacement pump)
        # T = (ΔP * displacement) / (2π * mechanical_efficiency)
        displacement = pump.flow_rate / (60/60)  # m³/stroke (60 strokes/min)
        eta_mech = 0.90  # Mechanical efficiency
        torque = (P_out - pressure_inlet) * displacement / (2 * np.pi * eta_mech)
        
        pressure_performance.append([P_sys/1e5, P_out/1e5, (P_out-pressure_inlet)/1e5, 
                                    Power/1000, torque])
        
        print(f"{P_sys/1e5:.0f}        {P_out/1e5:.1f}      {(P_out-pressure_inlet)/1e5:.1f}     {Power/1000:.2f}    {torque:.1f}")
    
    print()
    
    # Flow consistency analysis (key advantage of PD pumps)
    print("FLOW CONSISTENCY ANALYSIS:")
    print("-" * 30)
    
    # Test flow rate at different operating conditions
    inlet_pressures = np.array([0.5, 1.0, 1.5, 2.0]) * 1e5  # Different suction conditions
    pump.delta_P_nominal = 26.0e5  # Reset to design value
    
    print("Inlet P    Flow Rate   Deviation")
    print("(bar)      (m³/h)      (%)")
    print("-" * 30)
    
    base_flow = pump.flow_rate * 3600  # m³/h
    for P_in in inlet_pressures:
        # For PD pump, flow rate is constant regardless of pressure
        flow_actual = pump.flow_rate * 3600  # m³/h (constant)
        deviation = 100 * (flow_actual - base_flow) / base_flow
        
        print(f"{P_in/1e5:.1f}        {flow_actual:.1f}       {deviation:.1f}")
    
    print("\nNote: Flow rate remains constant - key advantage of PD pumps")
    print()
    
    # Viscosity effect analysis
    print("VISCOSITY EFFECT ANALYSIS:")
    print("-" * 30)
    
    viscosities = [1.0, 5.2, 10.0, 50.0, 100.0]  # cP
    print("Viscosity  Vol. Eff.  Flow Rate  Power")
    print("(cP)       (%)        (m³/h)     (kW)")
    print("-" * 35)
    
    for visc in viscosities:
        # Estimate volumetric efficiency vs viscosity
        # η_vol ≈ 0.95 - 0.001 * (μ - 1) for μ < 100 cP
        eta_vol = max(0.80, 0.95 - 0.001 * (visc - 1.0))
        
        # Effective flow rate
        flow_eff = pump.flow_rate * 3600 * eta_vol
        
        # Power increases with viscosity (friction losses)
        power_factor = 1.0 + 0.005 * (visc - 1.0)  # Simplified correlation
        power_visc = Power_design/1000 * power_factor
        
        print(f"{visc:.1f}        {eta_vol*100:.1f}      {flow_eff:.1f}      {power_visc:.2f}")
    
    print()
    
    # Dynamic response analysis
    print("DYNAMIC RESPONSE ANALYSIS:")
    print("-" * 30)
    
    # Simulate pressure transient (faster response than centrifugal)
    time_span = np.linspace(0, 5, 50)
    initial_pressure = P_outlet_design
    
    print("PD pumps have faster pressure response due to:")
    print("• Positive displacement mechanism")
    print("• Lower fluid inertia in chambers")
    print("• Direct mechanical coupling")
    print()
    print(f"Time Constant:      0.5 s (vs 1.0 s for centrifugal)")
    print(f"Response to 10% pressure step:")
    
    # Step response calculation
    step_magnitude = 0.1 * delta_P_required
    tau = 0.5  # Time constant for PD pump
    
    response_times = []
    for percentage in [10, 50, 90, 95]:
        # Time to reach percentage of final value
        t_response = -tau * np.log(1 - percentage/100)
        response_times.append(t_response)
        print(f"  {percentage}% response:    {t_response:.2f} s")
    
    print()
    
    # Injection rate control analysis
    print("INJECTION RATE CONTROL:")
    print("-" * 25)
    
    # Chemical dosing calculation
    process_flow = 500  # m³/h (main process stream)
    target_concentration = 25  # ppm (corrosion inhibitor)
    chemical_concentration = 50000  # ppm (50% active solution)
    
    # Required injection rate
    injection_rate = (process_flow * target_concentration) / chemical_concentration  # m³/h
    
    print(f"Process Flow:       {process_flow:.0f} m³/h")
    print(f"Target Dosage:      {target_concentration:.0f} ppm")
    print(f"Chemical Conc:      {chemical_concentration/10000:.1f}%")
    print(f"Required Injection: {injection_rate:.3f} m³/h")
    print(f"Pump Capacity:      {pump.flow_rate*3600:.1f} m³/h")
    print(f"Turndown Ratio:     {(pump.flow_rate*3600)/injection_rate:.1f}:1")
    print()
    
    # Operating cost and reliability analysis
    print("OPERATING COST & RELIABILITY:")
    print("-" * 35)
    
    operating_hours = 8760  # Continuous operation
    electricity_cost = 0.08  # $/kWh
    maintenance_factor = 1.5  # Higher maintenance for PD pumps
    
    annual_energy = Power_design/1000 * operating_hours
    annual_electricity = annual_energy * electricity_cost
    annual_maintenance = annual_electricity * maintenance_factor
    total_annual_cost = annual_electricity + annual_maintenance
    
    print(f"Annual Operating Hours: {operating_hours:,} h")
    print(f"Annual Energy:          {annual_energy:.0f} kWh")
    print(f"Electricity Cost:       ${annual_electricity:.0f}/year")
    print(f"Maintenance Cost:       ${annual_maintenance:.0f}/year")
    print(f"Total Annual Cost:      ${total_annual_cost:.0f}/year")
    print()
    
    # Comparison with centrifugal pump
    print("COMPARISON WITH CENTRIFUGAL PUMP:")
    print("-" * 40)
    print("Positive Displacement Advantages:")
    print("• Constant flow regardless of pressure")
    print("• Excellent for high-pressure applications")
    print("• Superior viscous fluid handling")
    print("• Precise metering capability")
    print("• Self-priming capability")
    print()
    print("Centrifugal Pump Advantages:")
    print("• Lower initial cost")
    print("• Lower maintenance requirements")
    print("• Smooth, pulsation-free flow")
    print("• Higher flow rates available")
    print("• Better for low-viscosity fluids")
    print()
    
    # Application guidelines
    print("APPLICATION GUIDELINES:")
    print("-" * 25)
    print("Recommended for:")
    print("• Chemical injection systems")
    print("• High-pressure applications (>10 bar)")
    print("• Viscous fluids (>10 cP)")
    print("• Precise flow control requirements")
    print("• Low flow rates (<50 m³/h)")
    print()
    print("Consider alternatives for:")
    print("• High flow, low pressure applications")
    print("• Clean, low-viscosity fluids")
    print("• Cost-sensitive applications")
    print("• Continuous high-speed operation")
    
    return pressure_performance, pump.flow_rate, delta_P_required

if __name__ == "__main__":
    perf_data, flow_rate, delta_p = main()
