"""
Complete Process Examples - SPROCLIB
====================================

This module contains comprehensive examples demonstrating the integration of multiple
SPROCLIB units in complete process simulations.

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

from unit.pump.CentrifugalPump import CentrifugalPump
from unit.tank.Tank import Tank
from unit.reactor.cstr import CSTR
from unit.heat_exchanger.HeatExchanger import HeatExchanger
from unit.valve.ControlValve import ControlValve
from unit.compressor.Compressor import Compressor
from unit.distillation.column.BinaryDistillationColumn import BinaryDistillationColumn


def simple_integrated_process():
    """
    Simple integrated process example.
    
    Process: Tank → Pump → Reactor → Heat Exchanger
    """
    print("=== Simple Integrated Process ===")
    print("Process Flow: Feed Tank → Pump → CSTR → Heat Exchanger → Product")
    
    # Create process units
    feed_tank = Tank(name="Feed Tank")
    process_pump = CentrifugalPump(name="Process Pump")
    reactor = CSTR(name="Main Reactor")
    cooler = HeatExchanger(name="Product Cooler")
    
    print(f"\nProcess units created:")
    print(f"1. {feed_tank.name} ({type(feed_tank).__name__})")
    print(f"2. {process_pump.name} ({type(process_pump).__name__})")
    print(f"3. {reactor.name} ({type(reactor).__name__})")
    print(f"4. {cooler.name} ({type(cooler).__name__})")
    
    # Process conditions
    feed_flow = 1200.0  # kg/h
    feed_concentration = 2.5  # mol/L
    reactor_temperature = 80.0  # °C
    product_temperature = 40.0  # °C
    
    print(f"\nProcess conditions:")
    print(f"Feed flow rate: {feed_flow} kg/h")
    print(f"Feed concentration: {feed_concentration} mol/L")
    print(f"Reactor temperature: {reactor_temperature}°C")
    print(f"Target product temperature: {product_temperature}°C")
    
    # Tank sizing
    tank_volume = feed_flow * 4 / 1000  # 4 hours residence time, m³
    tank_level = 75.0  # %
    current_volume = tank_volume * tank_level / 100
    
    print(f"\nFeed tank:")
    print(f"Volume: {tank_volume:.1f} m³")
    print(f"Current level: {tank_level}%")
    print(f"Current volume: {current_volume:.1f} m³")
    print(f"Available residence time: {current_volume * 1000 / feed_flow:.1f} hours")
    
    # Pump sizing
    pump_head = 25.0  # m
    pump_efficiency = 0.75
    fluid_density = 1000.0  # kg/m³
    
    power_hydraulic = feed_flow * pump_head * 9.81 / (3600 * 1000)  # kW
    power_brake = power_hydraulic / pump_efficiency
    
    print(f"\nPump performance:")
    print(f"Head: {pump_head} m")
    print(f"Efficiency: {pump_efficiency*100:.0f}%")
    print(f"Hydraulic power: {power_hydraulic:.2f} kW")
    print(f"Brake power: {power_brake:.2f} kW")
    
    # Reactor design
    reactor_volume = 2.5  # m³
    residence_time = reactor_volume * 1000 / feed_flow  # hours
    reaction_rate_constant = 0.8  # h⁻¹
    
    # CSTR conversion calculation
    conversion = reaction_rate_constant * residence_time / (1 + reaction_rate_constant * residence_time)
    outlet_concentration = feed_concentration * (1 - conversion)
    
    print(f"\nReactor performance:")
    print(f"Volume: {reactor_volume} m³")
    print(f"Residence time: {residence_time:.2f} hours")
    print(f"Rate constant: {reaction_rate_constant} h⁻¹")
    print(f"Conversion: {conversion*100:.1f}%")
    print(f"Outlet concentration: {outlet_concentration:.2f} mol/L")
    
    # Heat exchanger design
    cp = 4.18  # kJ/kg·K
    cooling_duty = feed_flow * cp * (reactor_temperature - product_temperature) / 3600  # kW
    cooling_water_flow = 2000.0  # kg/h
    cooling_water_inlet = 20.0  # °C
    cooling_water_outlet = cooling_water_inlet + cooling_duty * 3600 / (cooling_water_flow * cp)
    
    print(f"\nHeat exchanger performance:")
    print(f"Cooling duty: {cooling_duty:.1f} kW")
    print(f"Cooling water flow: {cooling_water_flow} kg/h")
    print(f"Cooling water inlet: {cooling_water_inlet}°C")
    print(f"Cooling water outlet: {cooling_water_outlet:.1f}°C")
    
    # Overall process summary
    print(f"\nProcess summary:")
    print(f"Feed rate: {feed_flow} kg/h at {feed_concentration} mol/L")
    print(f"Product rate: {feed_flow} kg/h at {outlet_concentration:.2f} mol/L")
    print(f"Overall conversion: {conversion*100:.1f}%")
    print(f"Energy consumption: {power_brake:.2f} kW (pumping) + {cooling_duty:.1f} kW (cooling)")
    
    print("\nSimple integrated process example completed successfully!")


def comprehensive_chemical_plant():
    """
    Comprehensive chemical plant simulation.
    
    Process: Multi-stage reaction with separation and recycle
    """
    print("\n=== Comprehensive Chemical Plant ===")
    print("Process: Feed Preparation → Reaction → Separation → Product Recovery")
    
    # Create all process units
    units = {
        "feed_tank": Tank(name="Feed Storage Tank"),
        "feed_pump": CentrifugalPump(name="Feed Pump"),
        "preheater": HeatExchanger(name="Feed Preheater"),
        "reactor_1": CSTR(name="Primary Reactor"),
        "reactor_2": CSTR(name="Secondary Reactor"),
        "cooler": HeatExchanger(name="Reactor Effluent Cooler"),
        "compressor": Compressor(name="Vapor Compressor"),
        "separator": Tank(name="Flash Separator"),
        "distillation": BinaryDistillationColumn(name="Product Distillation"),
        "recycle_pump": CentrifugalPump(name="Recycle Pump"),
        "control_valve": ControlValve(name="Flow Control Valve")
    }
    
    print(f"\nProcess units ({len(units)} total):")
    for i, (key, unit) in enumerate(units.items(), 1):
        print(f"{i:2d}. {unit.name} ({type(unit).__name__})")
    
    # Process flow rates and compositions
    fresh_feed = 5000.0  # kg/h
    recycle_ratio = 0.3  # Recycle to fresh feed ratio
    total_feed = fresh_feed * (1 + recycle_ratio)
    
    print(f"\nFlow rates:")
    print(f"Fresh feed: {fresh_feed} kg/h")
    print(f"Recycle ratio: {recycle_ratio}")
    print(f"Total reactor feed: {total_feed:.0f} kg/h")
    
    # Feed preparation section
    print(f"\n--- Feed Preparation Section ---")
    
    # Tank sizing (8 hours storage)
    tank_volume = fresh_feed * 8 / 1000  # m³
    tank_turnover = fresh_feed / (tank_volume * 1000)  # h⁻¹
    
    print(f"Feed tank volume: {tank_volume:.1f} m³")
    print(f"Turnover rate: {tank_turnover:.3f} h⁻¹")
    
    # Pump sizing
    feed_pump_head = 45.0  # m
    feed_pump_efficiency = 0.78
    feed_pump_power = total_feed * feed_pump_head * 9.81 / (3600 * 1000 * feed_pump_efficiency)
    
    print(f"Feed pump power: {feed_pump_power:.2f} kW")
    
    # Preheating
    feed_temp_in = 25.0  # °C
    feed_temp_out = 120.0  # °C
    preheat_duty = total_feed * 4.18 * (feed_temp_out - feed_temp_in) / 3600  # kW
    
    print(f"Preheating duty: {preheat_duty:.1f} kW")
    
    # Reaction section
    print(f"\n--- Reaction Section ---")
    
    # Two CSTRs in series
    reactor_volumes = [8.0, 6.0]  # m³
    rate_constants = [1.2, 0.8]  # h⁻¹ (different due to temperature)
    
    concentrations = [2.0]  # Starting concentration, mol/L
    conversions = []
    
    for i, (volume, k) in enumerate(zip(reactor_volumes, rate_constants)):
        residence_time = volume * 1000 / total_feed  # hours
        conversion_stage = k * residence_time / (1 + k * residence_time)
        
        # Overall conversion
        inlet_conc = concentrations[-1]
        outlet_conc = inlet_conc * (1 - conversion_stage)
        concentrations.append(outlet_conc)
        conversions.append(conversion_stage)
        
        print(f"Reactor {i+1}:")
        print(f"  Volume: {volume} m³")
        print(f"  Residence time: {residence_time:.2f} hours")
        print(f"  Stage conversion: {conversion_stage*100:.1f}%")
        print(f"  Outlet concentration: {outlet_conc:.2f} mol/L")
    
    overall_conversion = (concentrations[0] - concentrations[-1]) / concentrations[0]
    print(f"Overall conversion: {overall_conversion*100:.1f}%")
    
    # Heat of reaction (exothermic)
    heat_of_reaction = -50.0  # kJ/mol
    moles_reacted = total_feed / 60 * (concentrations[0] - concentrations[-1])  # mol/h (assuming MW=60)
    heat_generated = moles_reacted * abs(heat_of_reaction) / 3600  # kW
    
    print(f"Heat generated: {heat_generated:.1f} kW")
    
    # Cooling requirement
    reactor_temp = 140.0  # °C
    cooler_outlet_temp = 60.0  # °C
    cooling_duty = total_feed * 4.18 * (reactor_temp - cooler_outlet_temp) / 3600  # kW
    
    print(f"Cooling duty required: {cooling_duty:.1f} kW")
    
    # Separation section
    print(f"\n--- Separation Section ---")
    
    # Flash separation
    flash_temp = 80.0  # °C
    flash_pressure = 2.0  # bar
    vapor_fraction = 0.25  # 25% vaporized
    
    vapor_flow = total_feed * vapor_fraction
    liquid_flow = total_feed * (1 - vapor_fraction)
    
    print(f"Flash separator:")
    print(f"  Temperature: {flash_temp}°C")
    print(f"  Pressure: {flash_pressure} bar")
    print(f"  Vapor flow: {vapor_flow:.0f} kg/h")
    print(f"  Liquid flow: {liquid_flow:.0f} kg/h")
    
    # Vapor compression
    compressor_ratio = 3.0  # Compression ratio
    compressor_efficiency = 0.75
    
    # Simplified compressor power calculation
    compressor_power = vapor_flow * 0.5 * np.log(compressor_ratio) / compressor_efficiency  # kW (simplified)
    
    print(f"Compressor power: {compressor_power:.1f} kW")
    
    # Distillation column
    distillation_feed = liquid_flow
    distillate_rate = distillation_feed * 0.6  # 60% overhead
    bottoms_rate = distillation_feed * 0.4  # 40% bottoms
    
    reflux_ratio = 3.5
    reboiler_duty = distillate_rate * 2500 / 3600  # kW (simplified, 2500 kJ/kmol)
    condenser_duty = reboiler_duty * 1.1  # 10% more for condenser
    
    print(f"Distillation column:")
    print(f"  Feed rate: {distillation_feed:.0f} kg/h")
    print(f"  Distillate rate: {distillate_rate:.0f} kg/h")
    print(f"  Bottoms rate: {bottoms_rate:.0f} kg/h")
    print(f"  Reflux ratio: {reflux_ratio}")
    print(f"  Reboiler duty: {reboiler_duty:.1f} kW")
    print(f"  Condenser duty: {condenser_duty:.1f} kW")
    
    # Recycle system
    print(f"\n--- Recycle System ---")
    
    recycle_flow = fresh_feed * recycle_ratio
    recycle_concentration = concentrations[-1] * 0.8  # Some concentration in recycle
    
    recycle_pump_power = recycle_flow * 30 * 9.81 / (3600 * 1000 * 0.75)  # kW
    
    print(f"Recycle flow: {recycle_flow:.0f} kg/h")
    print(f"Recycle concentration: {recycle_concentration:.2f} mol/L")
    print(f"Recycle pump power: {recycle_pump_power:.2f} kW")
    
    # Control system
    control_valve_dp = 5.0  # bar pressure drop
    valve_cv = recycle_flow / 100  # Simplified Cv calculation
    
    print(f"Control valve ΔP: {control_valve_dp} bar")
    print(f"Required Cv: {valve_cv:.1f}")
    
    # Overall plant summary
    print(f"\n--- Overall Plant Summary ---")
    
    total_power = (feed_pump_power + compressor_power + recycle_pump_power + 
                  reboiler_duty + condenser_duty + cooling_duty + preheat_duty)
    
    product_rate = distillate_rate
    specific_energy = total_power / product_rate * 1000  # kWh/tonne
    
    print(f"Total energy consumption: {total_power:.1f} kW")
    print(f"Product rate: {product_rate:.0f} kg/h")
    print(f"Specific energy consumption: {specific_energy:.1f} kWh/tonne")
    print(f"Overall process efficiency: {overall_conversion*100:.1f}%")
    
    # Economic analysis (simplified)
    print(f"\n--- Economic Analysis ---")
    
    electricity_cost = 0.10  # $/kWh
    operating_hours = 8000  # hours/year
    
    annual_energy_cost = total_power * operating_hours * electricity_cost / 1000  # k$/year
    annual_production = product_rate * operating_hours / 1000  # tonnes/year
    energy_cost_per_tonne = annual_energy_cost * 1000 / annual_production  # $/tonne
    
    print(f"Annual energy cost: ${annual_energy_cost:.0f}k/year")
    print(f"Annual production: {annual_production:.0f} tonnes/year")
    print(f"Energy cost per tonne: ${energy_cost_per_tonne:.2f}/tonne")
    
    # Equipment count summary
    print(f"\n--- Equipment Summary ---")
    equipment_types = {}
    for unit in units.values():
        unit_type = type(unit).__name__
        equipment_types[unit_type] = equipment_types.get(unit_type, 0) + 1
    
    for equipment, count in equipment_types.items():
        print(f"{equipment}: {count}")
    
    print("\nComprehensive chemical plant example completed successfully!")


def main():
    """
    Main function to run all integrated process examples.
    """
    print("SPROCLIB Complete Process Examples")
    print("=" * 50)
    
    try:
        # Run simple integrated process
        simple_integrated_process()
        
        # Run comprehensive chemical plant
        comprehensive_chemical_plant()
        
        print("\n" + "=" * 50)
        print("All complete process examples completed successfully!")
        
        print(f"\nNote: These examples demonstrate the integration of refactored SPROCLIB units.")
        print(f"Each unit class is now in its own file, improving modularity and maintainability.")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
