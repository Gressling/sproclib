"""
Semantic Plant Design Example - SPROCLIB
========================================

This example demonstrates the semantic plant design API similar to TensorFlow/Keras
for intuitive chemical plant construction, optimization, and simulation.

Requirements:
- NumPy
- SciPy  
- All SPROCLIB units
"""

import numpy as np
import sys
import os

# Add the process_control directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unit.plant import ChemicalPlant, PlantConfiguration
from unit.reactor.cstr import CSTR
from unit.distillation.column.BinaryDistillationColumn import BinaryDistillationColumn
from unit.pump.CentrifugalPump import CentrifugalPump
from unit.valve.ControlValve import ControlValve
from transport.continuous.liquid.PipeFlow import PipeFlow


def semantic_plant_example():
    """
    Demonstrate semantic plant design API similar to TensorFlow/Keras.
    
    This example creates a small chemistry plant with reactor, distillation,
    pumps, valves and pipes using intuitive semantic syntax.
    """
    print("=== Semantic Chemical Plant Design Example ===")
    print("Using TensorFlow/Keras-style API for process plant design")
    
    # Step 1: Configure plant-wide parameters (similar to setting up ML environment)
    config = PlantConfiguration(
        name="Demo Chemical Plant",
        operating_hours=8000.0,
        electricity_cost=0.12,  # $/kWh
        steam_cost=18.0,        # $/ton
        cooling_water_cost=0.08 # $/m³
    )
    
    # Step 2: Define plant architecture (similar to keras.Sequential)
    plant = ChemicalPlant(name="Demo Chemical Plant", config=config)
    
    # Step 3: Add process units sequentially (similar to model.add(layers.Dense(...)))
    plant.add(CentrifugalPump(
        H0=50.0,          # 50 m shutoff head
        K=20.0,           # Head-flow coefficient  
        eta=0.75          # 75% efficiency
    ), name="feed_pump")
    
    plant.add(PipeFlow(
        length=200.0,     # 200 m pipeline
        diameter=0.15,    # 15 cm diameter
        roughness=4.6e-5  # Steel pipe roughness
    ), name="feed_pipeline")
    
    plant.add(CSTR(
        V=150.0,          # 150 L volume
        k0=7.2e10,        # Pre-exponential factor
        Ea=72750.0        # Activation energy
    ), name="main_reactor")
    
    plant.add(PipeFlow(
        length=50.0,      # 50 m pipeline
        diameter=0.12,    # 12 cm diameter
        roughness=4.6e-5
    ), name="reactor_outlet_pipe")
    
    plant.add(BinaryDistillationColumn(
        N_trays=12,       # 12 trays
        feed_tray=6,      # Feed on tray 6
        alpha=2.2,        # Relative volatility
        feed_flow=120.0   # Feed flow rate
    ), name="separation_column")
    
    plant.add(ControlValve(
        Cv_max=15.0,      # Maximum flow coefficient
        time_constant=3.0, # Response time constant
        dead_time=0.5     # Dead time
    ), name="reflux_control_valve")
    
    plant.add(CentrifugalPump(
        H0=35.0,          # 35 m shutoff head
        K=12.0,           # Head-flow coefficient
        eta=0.72          # 72% efficiency
    ), name="product_pump")
    
    print(f"\nStep 3: Added {len(plant.units)} process units to the plant")
    
    # Step 4: Connect units with streams (similar to functional API connections)
    plant.connect("feed_pump", "feed_pipeline", "feed_stream")
    plant.connect("feed_pipeline", "main_reactor", "reactor_feed")
    plant.connect("main_reactor", "reactor_outlet_pipe", "reactor_effluent")
    plant.connect("reactor_outlet_pipe", "separation_column", "column_feed")
    plant.connect("separation_column", "reflux_control_valve", "reflux_stream")
    plant.connect("reflux_control_valve", "product_pump", "product_stream")
    
    print(f"Step 4: Created {len(plant.connections)} process connections")
    
    # Step 5: Compile plant for optimization (similar to model.compile())
    plant.compile(
        optimizer="economic",           # Optimization strategy
        loss="total_cost",             # Loss function to minimize
        metrics=["profit", "energy_consumption", "conversion", "efficiency"]
    )
    
    print("Step 5: Plant compiled for economic optimization")
    
    # Step 6: Display plant summary (similar to model.summary())
    plant.summary()
    
    # Step 7: Optimize plant operations (similar to model.fit())
    print("Step 7: Running plant optimization...")
    
    optimization_results = plant.optimize(
        target_production=1000.0,  # kg/h target production
        constraints={
            "max_pressure": 10e5,   # 10 bar maximum pressure
            "min_conversion": 0.85,  # 85% minimum conversion
            "max_temperature": 400.0 # 400 K maximum temperature
        }
    )
    
    print(f"Optimization Results:")
    print(f"  Success: {optimization_results['success']}")
    print(f"  Optimal Cost: ${optimization_results['optimal_cost']:.2f}/h")
    print(f"  Message: {optimization_results['message']}")
    
    # Step 8: Simulate plant dynamics (similar to model.predict())
    print("\nStep 8: Running dynamic plant simulation...")
    
    simulation_results = plant.simulate(
        duration=24.0,    # 24 hours simulation
        time_step=0.5     # 30 minute time steps
    )
    
    print(f"Simulation completed for {len(simulation_results['time'])} time points")
    
    # Step 9: Evaluate plant performance at operating conditions
    operating_conditions = {
        "feed_flow": 1200.0,      # kg/h
        "feed_temperature": 25.0,  # °C
        "reactor_temperature": 85.0, # °C
        "column_reflux_ratio": 3.5
    }
    
    performance = plant.evaluate(operating_conditions)
    print(f"\nStep 9: Plant Performance Evaluation:")
    print(f"  Overall efficiency: {performance['plant']['overall_efficiency']:.1%}")
    print(f"  Total energy consumption: {performance['plant']['total_energy']:.0f} kW")
    print(f"  Production rate: {performance['plant']['production_rate']:.0f} kg/h")
    print(f"  Profit rate: ${performance['plant']['profit_rate']:.2f}/h")
    
    return plant


def advanced_semantic_operations(plant):
    """
    Demonstrate advanced semantic operations on the plant.
    """
    print("\n=== Advanced Semantic Operations ===")
    
    # Plant configuration inspection
    config = plant.get_config()
    print(f"Plant Configuration:")
    print(f"  Units: {len(config['units'])}")
    print(f"  Connections: {len(config['connections'])}")
    print(f"  Optimizer: {config['optimizer']}")
    
    # Save plant configuration (similar to model.save())
    plant_file = "demo_plant_config.json"
    plant.save_plant(plant_file)
    
    # Unit-specific analysis
    print(f"\nUnit Analysis:")
    for unit in plant.units:
        unit_type = type(unit).__name__
        print(f"  {unit.name}: {unit_type}")
        
        # Example: Get unit-specific parameters
        if hasattr(unit, 'calculate_performance'):
            try:
                performance = unit.calculate_performance()
                print(f"    Performance: {performance}")
            except:
                print(f"    Performance: Not available")
    
    # Economic analysis
    print(f"\nEconomic Analysis:")
    annual_production = 1000 * plant.config.operating_hours  # kg/year
    annual_revenue = annual_production * 2.5  # $2.5/kg product price
    annual_operating_cost = 500 * plant.config.operating_hours  # $500/h operating cost
    annual_profit = annual_revenue - annual_operating_cost
    
    print(f"  Annual production: {annual_production:,.0f} kg/year")
    print(f"  Annual revenue: ${annual_revenue:,.0f}/year")
    print(f"  Annual operating cost: ${annual_operating_cost:,.0f}/year")
    print(f"  Annual profit: ${annual_profit:,.0f}/year")
    print(f"  ROI potential: {annual_profit/1e6*100:.1f}% (assuming $1M investment)")


def compare_with_tensorflow_syntax():
    """
    Show direct comparison with TensorFlow/Keras syntax.
    """
    print("\n=== Syntax Comparison: TensorFlow vs SPROCLIB ===")
    
    print("\nTensorFlow/Keras Neural Network:")
    print("""
from tensorflow import keras
from tensorflow.keras import layers

# Define model
model = keras.Sequential([
    layers.Dense(64, activation="relu", name="layer1"),
    layers.Dense(32, activation="relu", name="layer2"), 
    layers.Dense(1, name="output")
])

# Compile model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.01),
    loss=keras.losses.MeanSquaredError(),
    metrics=[keras.metrics.MeanAbsoluteError()]
)

# Train model
model.fit(x_train, y_train, epochs=100)
model.summary()
    """)
    
    print("\nSPROCLIB Chemical Plant (Equivalent Syntax):")
    print("""
from unit.plant import ChemicalPlant
from unit.reactor.cstr import CSTR
from unit.pump import CentrifugalPump
from unit.distillation import BinaryDistillationColumn

# Define plant
plant = ChemicalPlant([
    CentrifugalPump(H0=50.0, eta=0.75, name="pump1"),
    CSTR(V=150.0, k0=7.2e10, name="reactor1"),
    BinaryDistillationColumn(N_trays=12, name="column1")
])

# Compile plant  
plant.compile(
    optimizer="economic",
    loss="total_cost", 
    metrics=["profit", "conversion", "efficiency"]
)

# Optimize plant
plant.optimize(target_production=1000.0, constraints={...})
plant.summary()
    """)
    
    print("\nKey Similarities:")
    print("✓ Sequential adding of components (layers ↔ units)")
    print("✓ Compilation step for optimization setup")
    print("✓ Training/optimization with target objectives")
    print("✓ Summary() method for architecture overview")
    print("✓ Metrics tracking and evaluation")
    print("✓ Save/load functionality")
    print("✓ Functional API for complex connections")


def main():
    """
    Main function to run all semantic plant examples.
    """
    print("SPROCLIB Semantic Plant Design Examples")
    print("=" * 50)
    
    try:
        # Run semantic plant example
        plant = semantic_plant_example()
        
        # Run advanced operations
        advanced_semantic_operations(plant)
        
        # Compare syntax
        compare_with_tensorflow_syntax()
        
        print("\n" + "=" * 50)
        print("All semantic plant examples completed successfully!")
        
        print(f"\n🎉 SPROCLIB now supports TensorFlow/Keras-style plant design!")
        print(f"✓ Semantic API for intuitive plant construction")
        print(f"✓ Sequential and functional design patterns") 
        print(f"✓ Compilation and optimization framework")
        print(f"✓ Plant-wide simulation and analysis")
        print(f"✓ Economic and performance optimization")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
