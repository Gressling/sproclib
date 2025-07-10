Semantic Plant Design
=====================

SPROCLIB provides a semantic API for chemical plant design that uses familiar
patterns from machine learning frameworks like TensorFlow and Keras.

API Design Philosophy
---------------------

The semantic API implements consistent patterns across all process units:

**Plant Definition**
    Similar to keras.Sequential(), define a plant container

**Unit Addition**
    Add process units like neural network layers with model.add()

**Connection Specification**
    Connect units with explicit stream definitions

**Compilation**
    Configure optimization objectives and constraints

**Optimization**
    Solve for optimal operating conditions

Basic Usage
-----------

.. code-block:: python

    from unit.plant import ChemicalPlant
    from unit.reactor.cstr import CSTR
    from unit.pump import CentrifugalPump
    
    # Define plant
    plant = ChemicalPlant(name="Process Plant")
    
    # Add units
    plant.add(CentrifugalPump(H0=50.0, eta=0.75), name="feed_pump")
    plant.add(CSTR(V=150.0, k0=7.2e10), name="reactor")
    
    # Connect units
    plant.connect("feed_pump", "reactor", "feed_stream")
    
    # Configure optimization
    plant.compile(
        optimizer="economic",
        loss="total_cost", 
        metrics=["profit", "conversion"]
    )
    
    # Optimize operations
    plant.optimize(target_production=1000.0)
    
    # Display results
    plant.summary()

Hyperparameter Optimization Analogy
------------------------------------

Just as machine learning models require hyperparameter tuning to achieve optimal performance, 
chemical plants require unit operation parameter optimization to maximize efficiency, profit, 
and safety. SPROCLIB makes this analogy explicit through its design.

Neural Network vs Chemical Plant Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Neural Network Layer Configuration:**

.. code-block:: python

    # Keras neural network hyperparameters
    model = keras.Sequential()
    model.add(Dense(units=128, activation='relu'))      # Layer size
    model.add(Dropout(rate=0.3))                        # Regularization
    model.add(Dense(units=64, activation='relu'))       # Hidden layer size
    model.add(Dense(units=10, activation='softmax'))    # Output classes

**Chemical Plant Unit Configuration:**

.. code-block:: python

    # SPROCLIB plant unit parameters
    plant = ChemicalPlant("Production Plant")
    plant.add(PipeFlow(length=200.0, diameter=0.15), name="pipeline1")      # Physical dimensions
    plant.add(CSTR(V=150.0, k0=7.2e10, Ea=72750), name="reactor1")         # Reaction kinetics
    plant.add(DistillationColumn(N_trays=20, reflux_ratio=3.5), name="col1") # Separation efficiency
    plant.add(ControlValve(Cv_max=15.0, response_time=2.0), name="valve1")   # Control characteristics

Parameter Categories and Analogies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Hyperparameter Optimization Analogy
   :widths: 33 33 34
   :header-rows: 1

   * - **Aspect**
     - **Neural Networks**
     - **Chemical Plants**
   * - **Architecture**
     - Layer types, connections
     - Unit types, stream connections
   * - **Capacity**
     - Number of neurons, layer width
     - Reactor volume, pipe diameter
   * - **Performance**
     - Activation functions, dropout rates
     - Reaction kinetics, efficiency factors
   * - **Control**
     - Learning rate, batch size
     - Control valve settings, flow rates
   * - **Regularization**
     - Dropout, weight decay
     - Safety margins, constraint limits

**Physical Design Parameters (Architecture Hyperparameters):**

.. code-block:: python

    # Equipment sizing - analogous to layer architecture
    plant.add(CSTR(
        V=150.0,           # Reactor volume (like layer width)
        A_heat=25.0,       # Heat transfer area (like connections)
        height=3.0         # Physical geometry (like network depth)
    ), name="reactor")
    
    plant.add(PipeFlow(
        length=200.0,      # Transport capacity (like layer size)
        diameter=0.15,     # Flow capacity (like neuron count)
        roughness=0.045    # Efficiency factor (like activation)
    ), name="pipeline")

**Operating Parameters (Training Hyperparameters):**

.. code-block:: python

    # Process conditions - analogous to training parameters
    plant.add(DistillationColumn(
        N_trays=20,           # Separation stages (like epochs)
        reflux_ratio=3.5,     # Internal recycle (like learning rate)
        feed_tray=10          # Input location (like batch strategy)
    ), name="column")
    
    plant.add(ControlValve(
        Cv_max=15.0,          # Maximum capacity (like max learning rate)
        response_time=2.0,    # Control speed (like optimizer momentum)
        dead_time=0.5         # System lag (like gradient delay)
    ), name="valve")

Optimization Strategies Comparison
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Neural Network Hyperparameter Search:**

.. code-block:: python

    # Grid search for neural network
    param_grid = {
        'layers': [[64, 32], [128, 64], [256, 128, 64]],
        'dropout': [0.2, 0.3, 0.5],
        'learning_rate': [0.001, 0.01, 0.1],
        'batch_size': [32, 64, 128]
    }
    
    best_model = grid_search(param_grid, validation_data)

**Chemical Plant Parameter Optimization:**

.. code-block:: python

    # Grid search for plant design
    param_grid = {
        'reactor_volume': [100.0, 150.0, 200.0],          # Physical sizing
        'pipe_diameter': [0.10, 0.15, 0.20],              # Transport capacity  
        'column_trays': [15, 20, 25],                      # Separation stages
        'reflux_ratio': [2.5, 3.5, 4.5]                   # Operating conditions
    }
    
    best_plant = plant.optimize_parameters(param_grid, economic_objective)

**Automated Hyperparameter Optimization:**

.. code-block:: python

    # Neural network auto-tuning
    tuner = keras_tuner.RandomSearch(
        build_model,
        objective='val_accuracy',
        max_trials=50
    )
    
    # Plant parameter auto-tuning  
    plant_tuner = PlantParameterOptimizer(
        build_plant,
        objective='profit_per_hour',
        max_trials=50,
        constraints={'safety_margin': 0.2}
    )
    
    # Both follow similar optimization patterns
    best_hyperparams = tuner.get_best_hyperparameters()
    best_plant_params = plant_tuner.get_best_parameters()

Parameter Sensitivity and Design Trade-offs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Neural Network Trade-offs:**

.. code-block:: python

    # Larger networks: better capacity but slower training
    model.add(Dense(512))  # vs Dense(64) - capacity vs speed
    
    # Higher dropout: less overfitting but slower convergence  
    model.add(Dropout(0.5))  # vs Dropout(0.2) - generalization vs training

**Chemical Plant Trade-offs:**

.. code-block:: python

    # Larger equipment: better performance but higher cost
    plant.add(CSTR(V=300.0))  # vs V=150.0 - conversion vs capital cost
    
    # Tighter control: better performance but higher complexity
    plant.add(ControlValve(response_time=0.5))  # vs 2.0 - control vs stability

**Sensitivity Analysis (analogous to hyperparameter importance):**

.. code-block:: python

    # Neural network parameter sensitivity
    sensitivity = analyze_hyperparameter_importance(model, validation_data)
    # Output: learning_rate=0.8, dropout=0.6, layer_size=0.4
    
    # Plant parameter sensitivity  
    sensitivity = plant.analyze_parameter_sensitivity(economic_objective)
    # Output: reactor_volume=0.9, pipe_diameter=0.7, reflux_ratio=0.5

Practical Design Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^

**1. Initial Design (Default Hyperparameters):**

.. code-block:: python

    # Start with reasonable defaults (like pre-trained models)
    plant = ChemicalPlant("Initial Design")
    plant.add(CSTR(V=150.0), name="reactor")        # Standard reactor size
    plant.add(PipeFlow(diameter=0.15), name="pipe") # Standard pipe size
    plant.add(DistillationColumn(N_trays=20), name="column") # Standard column

**2. Parameter Screening (Coarse Grid Search):**

.. code-block:: python

    # Quick screening of major parameters
    results = plant.parameter_sweep({
        'reactor.V': [100, 150, 200],           # ±33% variation
        'pipe.diameter': [0.10, 0.15, 0.20],   # ±33% variation  
        'column.N_trays': [15, 20, 25]         # ±25% variation
    })

**3. Fine-tuning (Local Optimization):**

.. code-block:: python

    # Refine around best configuration
    best_config = results.get_best_configuration()
    optimized_plant = plant.fine_tune_parameters(
        base_config=best_config,
        tolerance=0.05,  # ±5% variation
        objective='maximize_profit'
    )

**4. Validation and Robustness (like model validation):**

.. code-block:: python

    # Test performance under different conditions
    validation_scenarios = [
        {'feed_rate': 0.8 * nominal_feed},    # Low throughput
        {'feed_rate': 1.2 * nominal_feed},    # High throughput
        {'ambient_temp': 5.0},                # Winter conditions
        {'ambient_temp': 35.0}                # Summer conditions
    ]
    
    robustness = optimized_plant.validate_design(validation_scenarios)

This analogy helps engineers familiar with machine learning quickly understand chemical 
plant optimization, while showing chemical engineers how modern ML optimization 
techniques can be applied to process design.

**Complete Semantic API Reference**
-------------------------------------

Plant Construction
^^^^^^^^^^^^^^^^^^

**Create Plant (like keras.Sequential):**

.. code-block:: python

    from unit.plant import ChemicalPlant, PlantConfiguration
    
    # Basic plant
    plant = ChemicalPlant("My Plant")
    
    # Plant with configuration
    config = PlantConfiguration(
        operating_hours=8000.0,
        electricity_cost=0.12,
        steam_cost=18.0
    )
    plant = ChemicalPlant("Advanced Plant", config=config)

**Add Units (like model.add(layers)):**

.. code-block:: python

    # Sequential addition
    plant.add(CentrifugalPump(H0=50.0, eta=0.75), name="pump1")
    plant.add(PipeFlow(length=200.0, diameter=0.15), name="pipeline1") 
    plant.add(CSTR(V=150.0, k0=7.2e10), name="reactor1")
    plant.add(DistillationColumn(N_trays=12), name="column1")
    
    # Chaining (fluent interface)
    plant.add(Pump(...), name="pump1") \
         .add(Reactor(...), name="reactor1") \
         .add(Column(...), name="column1")

**Connect Units (functional API):**

.. code-block:: python

    # Simple connections
    plant.connect("pump1", "pipeline1", "feed_stream")
    plant.connect("pipeline1", "reactor1", "reactor_feed")
    plant.connect("reactor1", "column1", "reactor_effluent")
    
    # Complex networks
    plant.connect("column1", "pump2", "distillate")
    plant.connect("column1", "pump3", "bottoms")
    plant.connect("pump2", "mixer1", "recycle_stream")

Plant Compilation
^^^^^^^^^^^^^^^^^

**Compile for Optimization (like model.compile):**

.. code-block:: python

    # Economic optimization
    plant.compile(
        optimizer="economic",           # Strategy
        loss="total_cost",             # Minimize total cost
        metrics=["profit", "efficiency"] # Track these metrics
    )
    
    # Environmental optimization
    plant.compile(
        optimizer="environmental",
        loss="carbon_footprint",
        metrics=["emissions", "energy_use"]
    )
    
    # Safety optimization
    plant.compile(
        optimizer="safety",
        loss="risk_index",
        metrics=["safety_margin", "hazard_level"]
    )

**Available Optimizers:**
- ``economic`` - Minimize costs, maximize profit
- ``environmental`` - Minimize environmental impact
- ``safety`` - Maximize safety margins
- ``energy`` - Minimize energy consumption
- ``custom`` - Define your own objective function

Plant Operations
^^^^^^^^^^^^^^^^

**Optimize Plant (like model.fit):**

.. code-block:: python

    # Basic optimization
    results = plant.optimize(target_production=1000.0)
    
    # Optimization with constraints
    results = plant.optimize(
        target_production=1000.0,
        constraints={
            "max_pressure": 10e5,      # 10 bar max
            "min_conversion": 0.85,    # 85% min conversion
            "max_temperature": 400.0,  # 400 K max temp
            "energy_limit": 5000.0     # 5 MW max energy
        }
    )
    
    # Multi-objective optimization
    results = plant.optimize(
        objectives=["minimize_cost", "maximize_safety"],
        weights=[0.7, 0.3]  # 70% cost, 30% safety
    )

**Simulate Plant Dynamics (like model.predict):**

.. code-block:: python

    # Dynamic simulation
    results = plant.simulate(
        duration=24.0,     # 24 hours
        time_step=0.5,     # 30 minute steps
        disturbances={     # Process disturbances
            "feed_flow": {"type": "step", "time": 12.0, "magnitude": 1.2},
            "ambient_temp": {"type": "ramp", "start": 25.0, "end": 35.0}
        }
    )
    
    # Scenario analysis
    scenarios = [
        {"name": "normal", "feed_rate": 1000},
        {"name": "high_demand", "feed_rate": 1500},
        {"name": "maintenance", "feed_rate": 500}
    ]
    
    for scenario in scenarios:
        result = plant.simulate(scenario=scenario)

**Evaluate Performance (like model.evaluate):**

.. code-block:: python

    # Performance at operating conditions
    performance = plant.evaluate({
        "feed_flow": 1200.0,
        "feed_temperature": 25.0,
        "reactor_temperature": 85.0,
        "column_reflux_ratio": 3.5
    })
    
    print(f"Overall efficiency: {performance['plant']['efficiency']:.1%}")
    print(f"Production rate: {performance['plant']['production']:.0f} kg/h")
    print(f"Energy consumption: {performance['plant']['energy']:.0f} kW")

Plant Analysis
^^^^^^^^^^^^^^

**Plant Summary (like model.summary):**

.. code-block:: python

    plant.summary()

**Output:**
::

    ============================================================
    Chemical Plant: Advanced Production Plant
    ============================================================
    Configuration:
      Operating hours: 8,000 h/year
      Electricity cost: $0.120/kWh
      Steam cost: $18.00/ton

    Process Units (7 total):
    Unit Name            Type                 Parameters
    ----------------------------------------------------------------------
    feed_pump            CentrifugalPump      H0=50.0m
    feed_pipeline        PipeFlow             L=200.0m
    main_reactor         CSTR                 V=150.0L
    outlet_pipe          PipeFlow             L=50.0m
    separation_column    DistillationColumn   Trays=12
    control_valve        ControlValve         Cv_max=15.0
    product_pump         CentrifugalPump      H0=35.0m

    Connections (6 total):
      feed_pump → feed_pipeline (feed_stream)
      feed_pipeline → main_reactor (reactor_feed)
      main_reactor → outlet_pipe (reactor_effluent)
      outlet_pipe → separation_column (column_feed)
      separation_column → control_valve (reflux_stream)
      control_valve → product_pump (product_stream)

    Optimization:
      Optimizer: economic
      Loss function: total_cost
      Metrics: profit, efficiency, conversion

    Performance:
      Production rate: 1,000 kg/h
      Energy consumption: 2,500 kW
      Overall efficiency: 82%
      Estimated profit: $1,250/h
    ============================================================

**Save and Load Plants (like model.save/load):**

.. code-block:: python

    # Save plant configuration
    plant.save_plant("my_plant.json")
    
    # Load plant configuration
    plant = ChemicalPlant.load_plant("my_plant.json")
    
    # Export to different formats
    plant.export("my_plant.xml")    # Process flow diagram
    plant.export("my_plant.py")     # Python code
    plant.export("my_plant.pdf")    # Documentation

**Real-World Example: Complete Chemical Plant**
-------------------------------------------------

.. literalinclude:: ../examples/semantic_plant_example.py
   :language: python
   :caption: Complete Semantic Plant Design Example
   :lines: 1-100

This example demonstrates:

* **Plant Configuration** - Setting up plant-wide parameters
* **Sequential Unit Addition** - Building the plant step by step
* **Functional Connections** - Creating process flow networks
* **Compilation** - Preparing for optimization
* **Optimization** - Finding optimal operating conditions
* **Simulation** - Dynamic plant behavior analysis
* **Economic Analysis** - Profit and cost calculations

**Learning Path: From Simple to Advanced**
--------------------------------------------

**Level 1: Basic Plant (5 minutes)**

.. code-block:: python

    plant = ChemicalPlant("Simple Plant")
    plant.add(Pump(H0=30.0), name="pump")
    plant.add(Tank(V=100.0), name="tank")
    plant.connect("pump", "tank")
    plant.compile(optimizer="economic")
    plant.optimize()
    plant.summary()

**Level 2: Process Plant (15 minutes)**

.. code-block:: python

    plant = ChemicalPlant("Process Plant")
    plant.add(Pump(...), name="feed_pump")
    plant.add(Reactor(...), name="reactor")
    plant.add(HeatExchanger(...), name="cooler")
    plant.add(Separator(...), name="separator")
    
    # Connect all units
    plant.connect("feed_pump", "reactor")
    plant.connect("reactor", "cooler")
    plant.connect("cooler", "separator")
    
    plant.compile(optimizer="economic", metrics=["profit", "conversion"])
    plant.optimize(target_production=500.0)

**Level 3: Integrated Plant (30 minutes)**

.. code-block:: python

    # Complete plant with recycle, control, and optimization
    plant = ChemicalPlant("Integrated Plant", config=PlantConfiguration(...))
    
    # Add all units with detailed parameters
    plant.add(CentrifugalPump(H0=50.0, eta=0.78), name="feed_pump")
    plant.add(PipeFlow(length=200.0, diameter=0.15), name="feed_line")
    plant.add(CSTR(V=150.0, k0=7.2e10, Ea=72750), name="reactor")
    plant.add(HeatExchanger(U=500.0, A=25.0), name="cooler")
    plant.add(BinaryDistillationColumn(N_trays=20, alpha=2.5), name="column")
    plant.add(ControlValve(Cv_max=15.0), name="reflux_valve")
    plant.add(CentrifugalPump(H0=25.0, eta=0.72), name="recycle_pump")
    
    # Create complex flow network
    # ... connections with recycle streams
    
    # Advanced optimization
    plant.compile(optimizer="multi_objective", loss=["cost", "emissions"])
    plant.optimize(target_production=1000.0, constraints={...})
    
    # Dynamic analysis
    plant.simulate(duration=168.0, scenarios=[...])

**Advanced Features**
-----------------------

**Custom Optimizers:**

.. code-block:: python

    def custom_economic_optimizer(plant_state):
        """Custom optimization function."""
        revenue = calculate_revenue(plant_state)
        costs = calculate_costs(plant_state)
        environmental_penalty = calculate_emissions(plant_state) * 100
        return -(revenue - costs - environmental_penalty)  # Maximize profit

    plant.compile(optimizer=custom_economic_optimizer)

**Dynamic Disturbances:**

.. code-block:: python

    disturbances = {
        "feed_composition": {
            "type": "random_walk",
            "mean": 0.5,
            "std": 0.05,
            "seed": 42
        },
        "ambient_temperature": {
            "type": "seasonal",
            "amplitude": 10.0,
            "period": 24.0  # hours
        }
    }
    
    plant.simulate(duration=720.0, disturbances=disturbances)

**Multi-Scenario Analysis:**

.. code-block:: python

    scenarios = [
        {"name": "Base Case", "feed_rate": 1000, "feed_temp": 25},
        {"name": "High Production", "feed_rate": 1500, "feed_temp": 25},
        {"name": "Winter Operation", "feed_rate": 1000, "feed_temp": 5},
        {"name": "Summer Operation", "feed_rate": 1000, "feed_temp": 35}
    ]
    
    results = plant.analyze_scenarios(scenarios)
    plant.compare_scenarios(results)

**Why This Matters**
----------------------

**For Students:**
- Learn process control with familiar ML syntax
- Immediate results without complex setup
- Progressive complexity as skills develop
- Real engineering problems from day one

**For Engineers:**
- Rapid prototyping of plant designs
- Economic optimization built-in
- Professional-grade results
- Easy to explain and share

**For Industry:**
- Fast concept evaluation
- No expensive licensing
- Integration with modern data tools
- Customizable for specific needs

**For Researchers:**
- Focus on algorithms, not implementation
- Easy to extend and modify
- Publication-ready results
- Community-driven development

**The Future of Chemical Engineering Software**
-------------------------------------------------

SPROCLIB's Semantic Plant Design API represents a paradigm shift in how we approach chemical engineering software:

**From Complex → Simple**
    Intuitive APIs replace complex configuration files

**From Fragmented → Unified**
    Single framework handles all aspects of plant design

**From Expensive → Free**
    Open source eliminates licensing barriers

**From Static → Dynamic**
    Real-time optimization and simulation built-in

**From Isolated → Connected**
    Integration with modern Python data science ecosystem

---

**Ready to revolutionize your chemical plant design workflow?**

**Next Steps:**
1. Try the :doc:`examples/semantic_plant_example`
2. Explore the :doc:`api/plant_package`  
3. Learn :doc:`user_guide/optimization_strategies`
4. Build your first plant in 5 minutes!

*Chemical engineering software is here.*
