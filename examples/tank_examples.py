"""
Tank Examples - SPROCLIB
========================

This module contains examples demonstrating the usage of tank units in SPROCLIB.
Each example includes both simple and comprehensive use cases.

Requirements:
- NumPy
- SciPy
- Matplotlib (for plotting)
"""

import numpy as np
import sys
import os

# Add the process_control directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unit.tank.Tank import Tank
from unit.tank.InteractingTanks import InteractingTanks


def simple_tank_examples():
    """
    Simple examples of using tank units.
    
    This example demonstrates basic tank operations with constant conditions.
    """
    print("=== Simple Tank Examples ===")
    
    # Single Tank Example
    print("\n--- Single Tank ---")
    tank = Tank(name="Basic Storage Tank")
    
    print(f"Tank created: {tank.name}")
    print(f"Type: {type(tank).__name__}")
    
    # Set tank parameters
    volume = 1000.0  # L
    initial_level = 50.0  # %
    inlet_flow = 10.0  # L/min
    outlet_flow = 8.0  # L/min
    
    print(f"\nTank specifications:")
    print(f"Total volume: {volume} L")
    print(f"Initial level: {initial_level}%")
    print(f"Initial volume: {volume * initial_level / 100.0} L")
    
    print(f"\nFlow rates:")
    print(f"Inlet flow: {inlet_flow} L/min")
    print(f"Outlet flow: {outlet_flow} L/min")
    print(f"Net flow: {inlet_flow - outlet_flow} L/min")
    
    # Calculate time to fill/empty
    current_volume = volume * initial_level / 100.0
    if inlet_flow > outlet_flow:
        remaining_volume = volume - current_volume
        time_to_full = remaining_volume / (inlet_flow - outlet_flow)
        print(f"Time to fill: {time_to_full:.1f} minutes")
    else:
        time_to_empty = current_volume / (outlet_flow - inlet_flow)
        print(f"Time to empty: {time_to_empty:.1f} minutes")
    
    # Interacting Tanks Example
    print("\n--- Interacting Tanks ---")
    tank_system = InteractingTanks(name="Two Tank System")
    
    print(f"Tank system created: {tank_system.name}")
    print(f"Type: {type(tank_system).__name__}")
    
    # Set system parameters
    tank1_volume = 800.0  # L
    tank2_volume = 1200.0  # L
    tank1_level = 70.0  # %
    tank2_level = 30.0  # %
    connection_flow = 5.0  # L/min
    
    print(f"\nSystem specifications:")
    print(f"Tank 1 volume: {tank1_volume} L (Level: {tank1_level}%)")
    print(f"Tank 2 volume: {tank2_volume} L (Level: {tank2_level}%)")
    print(f"Connection flow: {connection_flow} L/min")
    
    # Calculate initial volumes
    tank1_current = tank1_volume * tank1_level / 100.0
    tank2_current = tank2_volume * tank2_level / 100.0
    total_volume = tank1_current + tank2_current
    
    print(f"\nCurrent volumes:")
    print(f"Tank 1: {tank1_current:.1f} L")
    print(f"Tank 2: {tank2_current:.1f} L")
    print(f"Total liquid: {total_volume:.1f} L")
    
    print("\nSimple tank examples completed successfully!")


def comprehensive_tank_examples():
    """
    Comprehensive examples demonstrating advanced tank operations.
    
    This example includes:
    - Dynamic level control
    - Multi-tank cascading systems
    - Heat transfer in tanks
    - Mixing and residence time calculations
    - Safety and overflow scenarios
    """
    print("\n=== Comprehensive Tank Examples ===")
    
    # Dynamic Level Control Simulation
    print("\n--- Dynamic Level Control ---")
    
    tank = Tank(name="Level Controlled Tank")
    
    # Control system parameters
    setpoint = 60.0  # % level
    initial_level = 40.0  # %
    tank_volume = 2000.0  # L
    
    # PID controller parameters
    kp = 2.0  # Proportional gain
    ki = 0.1  # Integral gain
    kd = 0.5  # Derivative gain
    
    print(f"Level Control Simulation:")
    print(f"Setpoint: {setpoint}%")
    print(f"Initial level: {initial_level}%")
    print(f"Tank volume: {tank_volume} L")
    
    # Simulate control response
    time_points = np.linspace(0, 60, 13)  # 0 to 60 minutes
    levels = []
    errors = []
    controller_outputs = []
    
    current_level = initial_level
    integral_error = 0.0
    previous_error = 0.0
    
    print(f"\n{'Time (min)':<10} {'Level (%)':<10} {'Error':<8} {'Controller':<12} {'Flow In':<10}")
    print("-" * 60)
    
    for t in time_points:
        # Calculate error
        error = setpoint - current_level
        errors.append(error)
        
        # PID calculation
        integral_error += error * (5.0 if t > 0 else 0)  # 5-minute intervals
        derivative_error = (error - previous_error) / (5.0 if t > 0 else 1)
        
        controller_output = kp * error + ki * integral_error + kd * derivative_error
        controller_output = max(0, min(20, controller_output))  # Limit 0-20 L/min
        controller_outputs.append(controller_output)
        
        # Tank dynamics (simplified)
        outlet_flow = 8.0  # L/min (constant)
        net_flow = controller_output - outlet_flow
        level_change = net_flow * 5.0 / tank_volume * 100.0  # % change in 5 minutes
        current_level += level_change
        current_level = max(0, min(100, current_level))  # Limit 0-100%
        
        levels.append(current_level)
        previous_error = error
        
        print(f"{t:<10.0f} {current_level:<10.1f} {error:<8.1f} {controller_output:<12.1f} {controller_output:<10.1f}")
    
    # Multi-Tank Cascade System
    print("\n--- Multi-Tank Cascade System ---")
    
    # Define a 4-tank cascade system
    tank_specs = [
        {"name": "Tank 1", "volume": 500, "level": 80},
        {"name": "Tank 2", "volume": 750, "level": 60},
        {"name": "Tank 3", "volume": 1000, "level": 40},
        {"name": "Tank 4", "volume": 1250, "level": 20}
    ]
    
    print("Cascade System Configuration:")
    print("-" * 70)
    print(f"{'Tank':<8} {'Volume (L)':<12} {'Initial Level (%)':<18} {'Current Volume (L)':<18}")
    print("-" * 70)
    
    for tank_spec in tank_specs:
        current_vol = tank_spec["volume"] * tank_spec["level"] / 100.0
        print(f"{tank_spec['name']:<8} {tank_spec['volume']:<12} {tank_spec['level']:<18} {current_vol:<18.1f}")
    
    # Simulate cascade flow
    print("\nCascade Flow Simulation (steady state):")
    print("-" * 50)
    
    feed_flow = 12.0  # L/min to first tank
    flow_between_tanks = []
    
    for i, tank_spec in enumerate(tank_specs):
        if i == 0:
            inlet_flow = feed_flow
        else:
            inlet_flow = flow_between_tanks[i-1]
        
        # Simplified outlet flow calculation (function of level)
        level_factor = tank_spec["level"] / 100.0
        outlet_flow = inlet_flow * 0.95 + 2.0 * level_factor  # Some flow depends on level
        flow_between_tanks.append(outlet_flow)
        
        print(f"{tank_spec['name']}: In = {inlet_flow:.1f} L/min, Out = {outlet_flow:.1f} L/min")
    
    # Heat Transfer in Tank
    print("\n--- Heat Transfer Analysis ---")
    
    heated_tank = Tank(name="Heated Storage Tank")
    
    # Heat transfer parameters
    tank_volume_m3 = 5.0  # m³
    fluid_density = 1000.0  # kg/m³
    fluid_cp = 4180.0  # J/kg·K (water)
    initial_temp = 20.0  # °C
    heating_power = 50000.0  # W (50 kW)
    ambient_temp = 15.0  # °C
    heat_loss_coeff = 100.0  # W/K
    
    print(f"Heat Transfer Simulation:")
    print(f"Tank volume: {tank_volume_m3} m³")
    print(f"Heating power: {heating_power/1000:.0f} kW")
    print(f"Initial temperature: {initial_temp}°C")
    print(f"Ambient temperature: {ambient_temp}°C")
    
    # Calculate heating profile
    mass = tank_volume_m3 * 1000 * fluid_density  # kg
    time_hours = np.linspace(0, 4, 9)  # 0 to 4 hours
    
    print(f"\n{'Time (h)':<10} {'Temp (°C)':<12} {'Heat Loss (kW)':<15} {'Net Heat (kW)':<15}")
    print("-" * 60)
    
    current_temp = initial_temp
    for t in time_hours:
        heat_loss = heat_loss_coeff * (current_temp - ambient_temp) / 1000.0  # kW
        net_heating = heating_power/1000.0 - heat_loss  # kW
        
        print(f"{t:<10.1f} {current_temp:<12.1f} {heat_loss:<15.1f} {net_heating:<15.1f}")
        
        # Update temperature (simplified)
        if t > 0:
            time_step = 0.5 * 3600  # 0.5 hour in seconds
            temp_rise = (net_heating * 1000 * time_step) / (mass * fluid_cp)
            current_temp += temp_rise
    
    # Mixing and Residence Time
    print("\n--- Mixing and Residence Time Analysis ---")
    
    mixing_tank = Tank(name="Continuous Mixing Tank")
    
    # Mixing parameters
    working_volume = 3000.0  # L
    flow_rate = 150.0  # L/min
    mixing_efficiency = 0.85
    
    # Calculate residence time
    residence_time = working_volume / flow_rate  # minutes
    turnover_rate = flow_rate / working_volume  # min⁻¹
    
    print(f"Mixing Tank Analysis:")
    print(f"Working volume: {working_volume} L")
    print(f"Flow rate: {flow_rate} L/min")
    print(f"Residence time: {residence_time:.1f} minutes")
    print(f"Turnover rate: {turnover_rate:.3f} min⁻¹")
    print(f"Mixing efficiency: {mixing_efficiency*100:.0f}%")
    
    # RTD (Residence Time Distribution) simulation
    print(f"\nRTD Analysis (step response):")
    print(f"{'Time/τ':<8} {'C/C₀ (Perfect Mix)':<18} {'C/C₀ (Real Mix)':<18}")
    print("-" * 50)
    
    time_ratios = np.linspace(0, 3, 7)
    for t_ratio in time_ratios:
        # Perfect mixing (CSTR)
        c_perfect = 1 - np.exp(-t_ratio)
        
        # Real mixing (with some dead volume)
        effective_ratio = t_ratio * mixing_efficiency
        c_real = 1 - np.exp(-effective_ratio)
        
        print(f"{t_ratio:<8.1f} {c_perfect:<18.3f} {c_real:<18.3f}")
    
    print("\nComprehensive tank examples completed successfully!")


def main():
    """
    Main function to run all tank examples.
    """
    print("SPROCLIB Tank Examples")
    print("=" * 50)
    
    try:
        # Run simple examples
        simple_tank_examples()
        
        # Run comprehensive examples
        comprehensive_tank_examples()
        
        print("\n" + "=" * 50)
        print("All tank examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
