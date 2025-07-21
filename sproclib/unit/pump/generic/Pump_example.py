"""
Industrial Example: Generic Pump in Chemical Process Plant
Typical plant conditions and scale for base pump model
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the sproclib directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sproclib'))

from sproclib.unit.pump.Pump import Pump

def main():
    print("=" * 60)
    print("GENERIC PUMP - INDUSTRIAL PROCESS APPLICATION")
    print("=" * 60)
    print()
    
    # Process conditions (typical industrial scale)
    print("PROCESS CONDITIONS:")
    print("-" * 20)
    pressure_inlet = 2.5e5      # Pa (2.5 bar absolute)
    temperature = 298           # K (25°C)
    flow_rate = 0.1            # m³/s (360 m³/h)
    fluid_density = 1000       # kg/m³ (water)
    
    print(f"Inlet Pressure:     {pressure_inlet/1e5:.1f} bar")
    print(f"Temperature:        {temperature-273.15:.1f} °C")
    print(f"Flow Rate:          {flow_rate:.3f} m³/s ({flow_rate*3600:.0f} m³/h)")
    print(f"Fluid Density:      {fluid_density:.0f} kg/m³")
    print()
    
    # Create pump instance with typical industrial parameters
    pump = Pump(
        eta=0.75,                    # 75% efficiency (typical for industrial pumps)
        rho=fluid_density,
        flow_nominal=flow_rate,
        delta_P_nominal=3.0e5,       # 3 bar pressure rise (300 kPa)
        name="ProcessCirculationPump"
    )
    
    print("PUMP SPECIFICATIONS:")
    print("-" * 20)
    print(f"Pump Type:          Generic Process Pump")
    print(f"Efficiency:         {pump.eta:.1%}")
    print(f"Nominal Flow:       {pump.flow_nominal:.3f} m³/s ({pump.flow_nominal*3600:.0f} m³/h)")
    print(f"Pressure Rise:      {pump.delta_P_nominal/1e5:.1f} bar ({pump.delta_P_nominal/1000:.0f} kPa)")
    print()
    
    # Steady-state performance calculation
    u_input = np.array([pressure_inlet, flow_rate])
    P_outlet, Power = pump.steady_state(u_input)
    
    print("STEADY-STATE PERFORMANCE:")
    print("-" * 30)
    print(f"Outlet Pressure:    {P_outlet/1e5:.1f} bar ({P_outlet/1000:.0f} kPa)")
    print(f"Pressure Rise:      {(P_outlet-pressure_inlet)/1e5:.1f} bar")
    print(f"Hydraulic Power:    {Power/1000:.1f} kW")
    print(f"Brake Power:        {Power/(pump.eta*1000):.1f} kW")
    print()
    
    # Calculate specific energy and head
    specific_energy = (P_outlet - pressure_inlet) / fluid_density  # J/kg
    head = specific_energy / 9.81  # m (equivalent head)
    
    print("HYDRAULIC ANALYSIS:")
    print("-" * 20)
    print(f"Specific Energy:    {specific_energy:.0f} J/kg")
    print(f"Equivalent Head:    {head:.1f} m")
    print(f"Power Density:      {Power/(flow_rate*1000):.0f} W per m³/s")
    print()
    
    # Performance at different flow rates
    print("PERFORMANCE CURVE (Constant Pressure Rise Model):")
    print("-" * 50)
    flow_range = np.linspace(0.05, 0.15, 6)  # 50% to 150% of nominal
    
    print("Flow Rate   Outlet P   Power    Efficiency")
    print("(m³/s)      (bar)      (kW)     (%)")
    print("-" * 40)
    
    performance_data = []
    for Q in flow_range:
        u = np.array([pressure_inlet, Q])
        P_out, P_power = pump.steady_state(u)
        
        # Calculate actual efficiency (hydraulic/brake power)
        hydraulic_power = Q * (P_out - pressure_inlet)
        actual_efficiency = hydraulic_power / P_power if P_power > 0 else 0
        
        performance_data.append([Q, P_out/1e5, P_power/1000, actual_efficiency*100])
        print(f"{Q:.3f}       {P_out/1e5:.1f}      {P_power/1000:.1f}      {actual_efficiency*100:.1f}")
    
    print()
    
    # Dynamic response analysis
    print("DYNAMIC RESPONSE ANALYSIS:")
    print("-" * 30)
    
    # Simulate step change in inlet pressure
    time_span = np.linspace(0, 10, 100)
    initial_state = np.array([P_outlet])  # Start at steady state
    
    # Step change: inlet pressure increases by 0.5 bar at t=2s
    responses = []
    for t in time_span:
        if t < 2.0:
            P_in = pressure_inlet
        else:
            P_in = pressure_inlet + 0.5e5  # +0.5 bar step
        
        u = np.array([P_in, flow_rate])
        
        if t == 0:
            x_current = initial_state
        else:
            # Simple Euler integration for demonstration
            dxdt = pump.dynamics(t, x_current, u)
            dt = time_span[1] - time_span[0]
            x_current = x_current + dxdt * dt
        
        responses.append(x_current[0])
    
    final_pressure = responses[-1]
    print(f"Initial Outlet Pressure: {P_outlet/1e5:.2f} bar")
    print(f"Final Outlet Pressure:   {final_pressure/1e5:.2f} bar")
    print(f"Pressure Change:         {(final_pressure-P_outlet)/1e5:.2f} bar")
    print(f"Time Constant:           1.0 s (first-order response)")
    print()
    
    # Energy efficiency analysis
    print("ENERGY EFFICIENCY ANALYSIS:")
    print("-" * 30)
    
    # Compare with handbook correlations (Pump Handbook - Karassik)
    # Typical pump efficiency vs specific speed correlation
    print("Comparison with Perry's Chemical Engineers' Handbook:")
    print(f"Modeled Efficiency:     {pump.eta:.1%}")
    print(f"Typical Range:          70-85% for process pumps")
    print(f"Best Practice:          >80% for new installations")
    print()
    
    # Operating cost analysis (annual)
    operating_hours = 8760  # hours/year
    electricity_cost = 0.08  # $/kWh
    annual_energy = Power/1000 * operating_hours
    annual_cost = annual_energy * electricity_cost
    
    print("ANNUAL OPERATING COST:")
    print("-" * 25)
    print(f"Operating Hours:        {operating_hours:,} h/year")
    print(f"Annual Energy:          {annual_energy:,.0f} kWh/year")
    print(f"Electricity Cost:       ${electricity_cost:.3f}/kWh")
    print(f"Annual Operating Cost:  ${annual_cost:,.0f}/year")
    print()
    
    # System integration considerations
    print("SYSTEM INTEGRATION NOTES:")
    print("-" * 30)
    print("• Pump curve: Constant pressure rise (simplified model)")
    print("• Applications: Process circulation, utility services")
    print("• Control: Flow control via bypass or throttling valve")
    print("• NPSH: Ensure adequate suction pressure to prevent cavitation")
    print("• Maintenance: Monitor vibration, temperature, and power consumption")
    print("• Efficiency: Consider VFD for variable flow applications")
    print()
    
    # Scale-up considerations
    print("SCALE-UP CONSIDERATIONS:")
    print("-" * 25)
    print("• Power scaling: P ∝ Q³ for similar pumps (cube law)")
    print("• Efficiency: Larger pumps typically more efficient")
    print("• Materials: Consider corrosion, erosion, temperature effects")
    print("• Redundancy: Parallel pumps for critical services")
    print("• Control philosophy: Lead-lag operation for multiple pumps")
    
    return performance_data, time_span, responses

if __name__ == "__main__":
    performance_data, time_data, pressure_response = main()
