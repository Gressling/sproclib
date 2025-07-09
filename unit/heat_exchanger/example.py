"""
Example usage of the HeatExchanger class for SPROCLIB.

This example demonstrates how to simulate a counter-current heat exchanger
with varying inlet conditions.
"""

import numpy as np
import matplotlib.pyplot as plt
from paramus.chemistry.process_control.unit.heat_exchanger import HeatExchanger


def main():
    """Demonstrate heat exchanger simulation."""
    
    # Create heat exchanger
    hx = HeatExchanger(
        area=10.0,           # Heat transfer area (m²)
        U=500.0,             # Overall heat transfer coefficient (W/m²·K)
        mc_hot=2000.0,       # Hot side thermal capacity (J/K)
        mc_cold=1500.0,      # Cold side thermal capacity (J/K)
        name="CounterCurrentHX"
    )
    
    print(f"Heat Exchanger: {hx.name}")
    print(f"Area: {hx.area} m²")
    print(f"U: {hx.U} W/m²·K")
    print(f"Hot side thermal capacity: {hx.mc_hot} J/K")
    print(f"Cold side thermal capacity: {hx.mc_cold} J/K")
    
    # Set up simulation
    t_span = (0, 3600)  # 1 hour simulation
    t_eval = np.linspace(0, 3600, 300)
    
    # Initial conditions: [T_hot, T_cold]
    x0 = np.array([90.0, 20.0])  # °C
    
    # Define varying inlet conditions
    def input_function(t):
        """
        Time-varying inlet conditions.
        Returns: [T_hot_in, T_cold_in, m_dot_hot, m_dot_cold]
        """
        T_hot_in = 100.0 + 10.0 * np.sin(2 * np.pi * t / 1800)  # Varying hot inlet
        T_cold_in = 15.0   # Constant cold inlet
        m_dot_hot = 2.0    # Hot side flow rate (kg/s)
        m_dot_cold = 1.5   # Cold side flow rate (kg/s)
        
        return np.array([T_hot_in, T_cold_in, m_dot_hot, m_dot_cold])
    
    # Simulate
    print("\\nRunning simulation...")
    result = hx.simulate(
        t_span=t_span,
        x0=x0,
        input_func=input_function,
        t_eval=t_eval
    )
    
    # Extract results
    T_hot = result.y[0]
    T_cold = result.y[1]
    
    # Get inlet temperatures for plotting
    T_hot_in = [input_function(t)[0] for t in result.t]
    T_cold_in = [input_function(t)[1] for t in result.t]
    
    # Calculate heat duty
    cp = 4184  # Water specific heat (J/kg·K)
    m_dot_hot = 2.0
    m_dot_cold = 1.5
    
    Q_hot = m_dot_hot * cp * (np.array(T_hot_in) - T_hot)
    Q_cold = m_dot_cold * cp * (T_cold - T_cold_in[0])
    
    # Plot results
    plt.figure(figsize=(12, 10))
    
    # Temperature profiles
    plt.subplot(3, 1, 1)
    plt.plot(result.t/60, T_hot_in, 'r--', label='Hot inlet', linewidth=2)
    plt.plot(result.t/60, T_hot, 'r-', label='Hot outlet', linewidth=2)
    plt.plot(result.t/60, T_cold_in, 'b--', label='Cold inlet', linewidth=2)
    plt.plot(result.t/60, T_cold, 'b-', label='Cold outlet', linewidth=2)
    plt.ylabel('Temperature (°C)')
    plt.title('Heat Exchanger Temperature Profiles')
    plt.legend()
    plt.grid(True)
    
    # Heat duty
    plt.subplot(3, 1, 2)
    plt.plot(result.t/60, Q_hot/1000, 'r-', label='Hot side duty', linewidth=2)
    plt.plot(result.t/60, Q_cold/1000, 'b-', label='Cold side duty', linewidth=2)
    plt.ylabel('Heat Duty (kW)')
    plt.title('Heat Transfer Rates')
    plt.legend()
    plt.grid(True)
    
    # Temperature difference
    plt.subplot(3, 1, 3)
    delta_T = T_hot - T_cold
    plt.plot(result.t/60, delta_T, 'g-', linewidth=2)
    plt.xlabel('Time (min)')
    plt.ylabel('ΔT (°C)')
    plt.title('Temperature Difference (Hot - Cold)')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # Print final results
    print(f"\\nFinal Results:")
    print(f"Hot outlet temperature: {T_hot[-1]:.1f} °C")
    print(f"Cold outlet temperature: {T_cold[-1]:.1f} °C")
    print(f"Final heat duty: {Q_hot[-1]/1000:.1f} kW")
    print(f"Average effectiveness: {np.mean(Q_hot/(m_dot_hot * cp * (np.array(T_hot_in) - T_cold_in[0]))):.3f}")


if __name__ == "__main__":
    main()
