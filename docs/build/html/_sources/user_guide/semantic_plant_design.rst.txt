Semantic Plant Design API
=========================

SPROCLIB now provides a semantic plant design API similar to TensorFlow/Keras
for intuitive chemical plant construction, optimization, and simulation.

Overview
--------

The semantic API allows you to build complex chemical plants using familiar
patterns from machine learning frameworks::

    from unit.plant import ChemicalPlant
    from unit.reactor.cstr import CSTR
    from unit.pump import CentrifugalPump
    
    # Define plant (similar to keras.Sequential)
    plant = ChemicalPlant(name="Demo Plant")
    
    # Add units sequentially (similar to model.add(layers))
    plant.add(CentrifugalPump(H0=50.0, eta=0.75), name="feed_pump")
    plant.add(CSTR(V=150.0, k0=7.2e10), name="reactor")
    
    # Connect units
    plant.connect("feed_pump", "reactor", "feed_stream")
    
    # Compile for optimization (similar to model.compile)
    plant.compile(
        optimizer="economic",
        loss="total_cost", 
        metrics=["profit", "conversion"]
    )
    
    # Optimize plant (similar to model.fit)
    plant.optimize(target_production=1000.0)
    
    # Display summary (similar to model.summary)
    plant.summary()

Building Plants
---------------

**Sequential Design**

Build plants by adding units in sequence::

    plant = ChemicalPlant("My Plant")
    plant.add(Pump(...), name="pump1")
    plant.add(Reactor(...), name="reactor1") 
    plant.add(Distillation(...), name="column1")

**Functional Connections**

Connect units with named streams::

    plant.connect("pump1", "reactor1", "feed_stream")
    plant.connect("reactor1", "column1", "reactor_effluent")

**Plant Configuration**

Set plant-wide parameters::

    config = PlantConfiguration(
        operating_hours=8000.0,
        electricity_cost=0.12,
        steam_cost=18.0
    )
    plant = ChemicalPlant("Plant", config=config)

Compilation and Optimization
----------------------------

**Compile Plant**

Prepare plant for optimization::

    plant.compile(
        optimizer="economic",           # Strategy
        loss="total_cost",             # Objective
        metrics=["profit", "efficiency"] # Track metrics
    )

**Optimization Strategies**
- ``economic``: Minimize operating costs, maximize profit
- ``environmental``: Minimize emissions and waste
- ``safety``: Maximize safety margins

**Run Optimization**

Optimize plant operations::

    results = plant.optimize(
        target_production=1000.0,
        constraints={
            "max_pressure": 10e5,
            "min_conversion": 0.85
        }
    )

Simulation and Analysis
----------------------

**Dynamic Simulation**

Run time-based simulations::

    results = plant.simulate(
        duration=24.0,    # hours
        time_step=0.5     # time step
    )

**Performance Evaluation**

Evaluate at operating conditions::

    performance = plant.evaluate({
        "feed_flow": 1200.0,
        "temperature": 85.0
    })

**Plant Summary**

Get comprehensive overview::

    plant.summary()  # Similar to model.summary()

Complete Example
---------------

**TensorFlow/Keras Neural Network**::

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
    
    # Train and evaluate
    model.fit(x_train, y_train, epochs=100)
    model.summary()

**SPROCLIB Chemical Plant (Equivalent)**::

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
    
    # Optimize and evaluate
    plant.optimize(target_production=1000.0)
    plant.summary()

Key Benefits
-----------

**Familiar Syntax**
- TensorFlow/Keras-inspired API
- Sequential and functional design patterns
- Consistent method naming

**Intuitive Workflow**
- Add units like neural network layers
- Connect with named streams
- Compile for optimization objectives
- Optimize like model training

**Comprehensive Analysis**
- Plant-wide optimization
- Dynamic simulation
- Economic evaluation
- Performance metrics

**Extensible Design**
- Easy to add new unit types
- Plugin architecture for optimizers
- Custom metrics and objectives

See Also
--------
- :doc:`examples/semantic_plant_example` - Complete usage examples
- :doc:`api/plant_package` - API reference
- :doc:`optimization` - Optimization strategies
