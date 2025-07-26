#!/usr/bin/env python3
"""
SPROCLIB Comprehensive Examples Collection

This module contains a collection of examples demonstrating various
features of the SPROCLIB semantic plant design API.
"""

import numpy as np
import matplotlib.pyplot as plt
from process_control.unit.plant import ChemicalPlant, PlantConfiguration
from process_control.unit.pump.centrifugal import CentrifugalPump
from process_control.unit.reactor.cstr import CSTR
from process_control.unit.distillation.column import BinaryDistillationColumn
from process_control.unit.heat_exchanger import HeatExchanger
from process_control.unit.valve.control import ControlValve
from process_control.transport.continuous.liquid import PipeFlow
from process_control.controller.pid import PIDController


def basic_plant_example():
    """
    Basic plant example demonstrating fundamental concepts.
    
    This example shows:
    - Plant creation
    - Adding units
    - Basic connections
    - Simple optimization
    """
    print("=" * 60)
    print("Basic Plant Example")
    print("=" * 60)
    
    # Create basic plant
    plant = ChemicalPlant("Basic Plant")
    
    # Add units
    plant.add(CentrifugalPump(H0=30.0, eta=0.75), name="pump")
    plant.add(CSTR(V=100.0, k0=1e8), name="reactor")
    
    # Connect units
    plant.connect("pump", "reactor", "feed_stream")
    
    # Compile and optimize
    plant.compile(optimizer="economic", loss="total_cost")
    results = plant.optimize(target_production=500.0)
    
    # Display results
    plant.summary()
    print(f"Optimization successful: {results['success']}")
    
    return plant


def advanced_plant_example():
    """
    Advanced plant example with multiple units and complex connections.
    
    This example demonstrates:
    - Complex plant architecture
    - Multiple process units
    - Recycle streams
    - Advanced optimization
    - Dynamic simulation
    """
    print("=" * 60)
    print("Advanced Plant Example")
    print("=" * 60)
    
    # Create plant with configuration
    config = PlantConfiguration(
        operating_hours=8000,
        electricity_cost=0.12,
        steam_cost=18.0,
        cooling_water_cost=0.08
    )
    
    plant = ChemicalPlant("Advanced Production Plant", config=config)
    
    # Add all process units
    plant.add(CentrifugalPump(H0=50.0, eta=0.78), name="feed_pump")
    plant.add(PipeFlow(length=200.0, diameter=0.15), name="feed_line")
    plant.add(CSTR(V=150.0, k0=7.2e10, Ea=72750), name="main_reactor")
    plant.add(PipeFlow(length=100.0, diameter=0.12), name="reactor_outlet")
    plant.add(HeatExchanger(U=500.0, A=25.0), name="product_cooler")
    plant.add(BinaryDistillationColumn(N_trays=20, alpha=2.5), name="separator")
    plant.add(ControlValve(Cv_max=15.0), name="reflux_valve")
    plant.add(CentrifugalPump(H0=25.0, eta=0.72), name="product_pump")
    plant.add(CentrifugalPump(H0=30.0, eta=0.75), name="recycle_pump")
    
    # Create flow network
    plant.connect("feed_pump", "feed_line", "raw_feed")
    plant.connect("feed_line", "main_reactor", "reactor_feed")
    plant.connect("main_reactor", "reactor_outlet", "reactor_effluent")
    plant.connect("reactor_outlet", "product_cooler", "hot_product")
    plant.connect("product_cooler", "separator", "cooled_product")
    plant.connect("separator", "reflux_valve", "distillate")
    plant.connect("reflux_valve", "product_pump", "final_product")
    plant.connect("separator", "recycle_pump", "bottoms")
    plant.connect("recycle_pump", "feed_line", "recycle_stream")  # Recycle
    
    # Add control system
    temp_controller = PIDController(Kp=2.0, Ki=0.5, Kd=0.1, setpoint=350.0)
    plant.add_controller(temp_controller, "main_reactor", "temperature")
    
    # Compile for multi-objective optimization
    plant.compile(
        optimizer="multi_objective",
        loss=["total_cost", "emissions"],
        loss_weights=[0.7, 0.3],
        metrics=["profit", "conversion", "energy_efficiency", "carbon_footprint"]
    )
    
    # Optimize with constraints
    results = plant.optimize(
        target_production=1000.0,
        constraints={
            "max_pressure": 15e5,
            "min_conversion": 0.85,
            "max_temperature": 400.0,
            "max_energy": 2000.0
        }
    )
    
    # Dynamic simulation
    simulation_results = plant.simulate(
        duration=24.0,
        time_step=0.5,
        disturbances={
            "feed_composition": lambda t: 0.8 + 0.1*np.sin(0.1*t),
            "ambient_temperature": lambda t: 25.0 + 5.0*np.sin(2*np.pi*t/24)
        }
    )
    
    # Display comprehensive results
    plant.summary()
    print(f"\nOptimization Results:")
    print(f"  Success: {results['success']}")
    print(f"  Total Cost: ${results['total_cost']:.2f}/h")
    print(f"  Production Rate: {results['production_rate']:.1f} kg/h")
    print(f"  Overall Efficiency: {results['efficiency']:.1%}")
    
    return plant, results, simulation_results


def tensorflow_comparison_example():
    """
    Example demonstrating the TensorFlow/Keras syntax comparison.
    
    This shows side-by-side how SPROCLIB mirrors TensorFlow patterns.
    """
    print("=" * 60)
    print("TensorFlow/Keras Style Chemical Plant Design")
    print("=" * 60)
    
    # TensorFlow-style plant definition
    plant = ChemicalPlant([
        CentrifugalPump(H0=50.0, eta=0.75, name="input_pump"),
        CSTR(V=150.0, k0=7.2e10, name="reaction_layer"),
        BinaryDistillationColumn(N_trays=12, name="separation_layer"),
        ControlValve(Cv_max=15.0, name="output_valve")
    ], name="TensorFlow-Style Plant")
    
    # Keras-style compilation
    plant.compile(
        optimizer="economic",
        loss="total_cost",
        metrics=["profit", "conversion", "efficiency"]
    )
    
    # ML-style training/optimization
    plant.fit(
        target_production=1000.0,
        validation_split=0.2,  # Use 20% for validation
        epochs=100,            # Optimization iterations
        batch_size=32          # Batch processing size
    )
    
    # Model-style evaluation
    test_conditions = {
        "feed_flow": 1200.0,
        "feed_temperature": 298.15,
        "feed_composition": 0.85
    }
    
    performance = plant.evaluate(test_conditions)
    predictions = plant.predict(test_conditions)
    
    # Display TensorFlow-style summary
    plant.summary()
    
    print(f"\nModel Performance:")
    print(f"  Test Accuracy: {performance['accuracy']:.1%}")
    print(f"  Validation Loss: {performance['val_loss']:.3f}")
    print(f"  Predictions: {predictions}")
    
    return plant


def economic_optimization_example():
    """
    Example focusing on economic optimization features.
    """
    print("=" * 60)
    print("Economic Optimization Example")
    print("=" * 60)
    
    # Plant with detailed economic configuration
    config = PlantConfiguration(
        operating_hours=8760,      # Full year operation
        electricity_cost=0.12,     # $/kWh
        steam_cost=18.0,           # $/ton
        cooling_water_cost=0.08,   # $/m³
        raw_material_cost=2.50,    # $/kg
        product_price=8.75,        # $/kg
        labor_cost=50.0,           # $/h
        maintenance_factor=0.03    # 3% of capital cost
    )
    
    plant = ChemicalPlant("Economic Optimization Plant", config=config)
    
    # Add units with economic parameters
    plant.add(CentrifugalPump(
        H0=50.0, eta=0.75, 
        capital_cost=15000,        # Initial investment
        maintenance_factor=0.02    # 2% annual maintenance
    ), name="feed_pump")
    
    plant.add(CSTR(
        V=150.0, k0=7.2e10,
        capital_cost=85000,
        operating_cost=125.0       # $/h operating cost
    ), name="reactor")
    
    plant.add(BinaryDistillationColumn(
        N_trays=12, alpha=2.2,
        capital_cost=125000,
        steam_consumption=2.5,     # ton/h
        electricity_consumption=45 # kW
    ), name="column")
    
    # Economic optimization
    plant.compile(
        optimizer="economic",
        loss="net_present_value",
        metrics=["roi", "payback_period", "irr"]
    )
    
    # Multi-scenario optimization
    scenarios = [
        {"name": "Base Case", "production": 1000, "price": 8.75},
        {"name": "High Demand", "production": 1500, "price": 9.50},
        {"name": "Low Market", "production": 750, "price": 7.25},
        {"name": "High Energy Cost", "production": 1000, "electricity_cost": 0.18}
    ]
    
    results = plant.optimize_scenarios(scenarios)
    
    # Economic analysis
    economics = plant.calculate_economics()
    
    print(f"\nEconomic Analysis:")
    print(f"  NPV: ${economics['npv']:,.0f}")
    print(f"  ROI: {economics['roi']:.1%}")
    print(f"  Payback Period: {economics['payback']:.1f} years")
    print(f"  IRR: {economics['irr']:.1%}")
    
    # Sensitivity analysis
    sensitivity = plant.sensitivity_analysis([
        "electricity_cost", "steam_cost", "product_price", "raw_material_cost"
    ])
    
    return plant, results, economics


def control_system_example():
    """
    Example demonstrating advanced control system integration.
    """
    print("=" * 60)
    print("Advanced Control System Example")
    print("=" * 60)
    
    plant = ChemicalPlant("Control System Plant")
    
    # Add units
    plant.add(CentrifugalPump(H0=45.0), name="feed_pump")
    plant.add(CSTR(V=120.0, k0=5e9), name="reactor")
    plant.add(HeatExchanger(U=600.0, A=20.0), name="cooler")
    
    # Connect units
    plant.connect("feed_pump", "reactor", "feed")
    plant.connect("reactor", "cooler", "product")
    
    # Add multiple controllers
    
    # Temperature control
    temp_controller = PIDController(
        Kp=2.5, Ki=0.3, Kd=0.1,
        setpoint=355.0,
        output_limits=(0, 100)
    )
    plant.add_controller(temp_controller, "reactor", "temperature", "cooling_duty")
    
    # Flow control
    flow_controller = PIDController(
        Kp=1.8, Ki=0.5, Kd=0.05,
        setpoint=1000.0
    )
    plant.add_controller(flow_controller, "feed_pump", "flow_rate", "pump_speed")
    
    # Level control
    level_controller = PIDController(
        Kp=3.0, Ki=0.8, Kd=0.0,
        setpoint=75.0
    )
    plant.add_controller(level_controller, "reactor", "level", "outlet_valve")
    
    # Advanced control - Model Predictive Control
    mpc_controller = plant.add_mpc_controller(
        controlled_variables=["temperature", "level", "concentration"],
        manipulated_variables=["cooling_duty", "feed_rate", "outlet_valve"],
        prediction_horizon=20,
        control_horizon=5
    )
    
    # Control system tuning
    plant.tune_controllers(method="auto_tune", test_signal="prbs")
    
    # Disturbance rejection test
    disturbances = {
        "feed_temperature": {"type": "step", "time": 3600, "magnitude": 10.0},
        "feed_composition": {"type": "ramp", "start_time": 7200, "duration": 1800, "magnitude": 0.1}
    }
    
    control_results = plant.test_control_performance(
        duration=14400,  # 4 hours
        disturbances=disturbances
    )
    
    print(f"\nControl Performance:")
    print(f"  Temperature IAE: {control_results['temp_iae']:.2f}")
    print(f"  Level ISE: {control_results['level_ise']:.2f}")
    print(f"  Settling Time: {control_results['settling_time']:.1f} s")
    print(f"  Overshoot: {control_results['overshoot']:.1%}")
    
    return plant, control_results


def run_all_examples():
    """Run all example functions."""
    examples = [
        basic_plant_example,
        advanced_plant_example,
        tensorflow_comparison_example,
        economic_optimization_example,
        control_system_example
    ]
    
    results = {}
    
    for example_func in examples:
        print(f"\n{'='*80}")
        print(f"Running {example_func.__name__}")
        print(f"{'='*80}")
        
        try:
            result = example_func()
            results[example_func.__name__] = result
            print(f"✅ {example_func.__name__} completed successfully!")
        except Exception as e:
            print(f"❌ {example_func.__name__} failed: {str(e)}")
            results[example_func.__name__] = None
    
    print(f"\n{'='*80}")
    print("All Examples Summary")
    print(f"{'='*80}")
    
    for name, result in results.items():
        status = "✅ Success" if result is not None else "❌ Failed"
        print(f"  {name}: {status}")
    
    return results


if __name__ == "__main__":
    # Run all examples
    results = run_all_examples()
    
    print(f"\nSPROCLIB Examples completed!")
    print(f"Total examples run: {len(results)}")
    print(f"Successful: {sum(1 for r in results.values() if r is not None)}")
