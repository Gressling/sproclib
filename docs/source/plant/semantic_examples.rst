Complete Semantic Plant Design Examples
=======================================

🎯 **The Core of SPROCLIB: Real Chemical Plant Design**

This section contains the complete semantic plant design example that showcases
SPROCLIB's revolutionary TensorFlow/Keras-style API for chemical plant construction.

.. note::
   **This is the heart of SPROCLIB** - These examples demonstrate why the semantic
   plant design API is revolutionary for chemical process control.

Complete Working Example
------------------------

The following is the complete semantic plant design example from 
``examples/semantic_plant_example.py``:

.. literalinclude:: ../../examples/semantic_plant_example.py
   :language: python
   :caption: Complete Semantic Plant Design Example
   :name: semantic-plant-complete

Running the Example
-------------------

To run this example::

    cd examples
    python semantic_plant_example.py

Expected Output
--------------

.. code-block:: text

    SPROCLIB Semantic Plant Design Examples
    ==================================================
    === Semantic Chemical Plant Design Example ===
    Using TensorFlow/Keras-style API for process plant design
    
    Step 3: Added 7 process units to the plant
    Step 4: Created 6 process connections
    Step 5: Plant compiled for economic optimization
    
    ============================================================
    Chemical Plant: Demo Chemical Plant
    ============================================================
    Configuration:
      Operating hours: 8,000 h/year
      Electricity cost: $0.120/kWh
      Steam cost: $18.00/ton
      Cooling water cost: $0.080/m³
    
    Process Units (7 total):
    Unit Name            Type                    Parameters
    ----------------------------------------------------------------------
    feed_pump            CentrifugalPump         H0=50.0m
    feed_pipeline        PipeFlow                L=200.0m
    main_reactor         CSTR                    V=150.0L
    reactor_outlet_pipe  PipeFlow                L=50.0m
    separation_column    BinaryDistillationColumn  Trays=12
    reflux_control_valve ControlValve            Cv_max=15.0
    product_pump         CentrifugalPump         H0=35.0m
    
    Connections (6 total):
      feed_pump → feed_pipeline (feed_stream)
      feed_pipeline → main_reactor (reactor_feed)
      main_reactor → reactor_outlet_pipe (reactor_effluent)
      reactor_outlet_pipe → separation_column (column_feed)
      separation_column → reflux_control_valve (reflux_stream)
      reflux_control_valve → product_pump (product_stream)
    
    Optimization:
      Optimizer: economic
      Loss function: total_cost
      Metrics: profit, energy_consumption, conversion, efficiency
    ============================================================
    
    Step 7: Running plant optimization...
    Optimization Results:
      Success: True
      Optimal Cost: $523.45/h
      Message: Optimization terminated successfully
    
    Step 8: Running dynamic plant simulation...
    Simulation completed for 49 time points
    
    Step 9: Plant Performance Evaluation:
      Overall efficiency: 80.0%
      Total energy consumption: 1500 kW
      Production rate: 1000 kg/h
      Profit rate: $500.00/h

Key Example Sections
-------------------

**1. Plant Configuration**
  
   Setting up plant-wide parameters like operating costs and schedules

**2. Sequential Unit Addition**
  
   Adding process equipment using the intuitive ``plant.add()`` method

**3. Stream Connections**
  
   Connecting units with the ``plant.connect()`` method

**4. Plant Compilation**
  
   Configuring optimization strategy with ``plant.compile()``

**5. Plant Optimization**
  
   Running economic optimization with ``plant.optimize()``

**6. Dynamic Simulation**
  
   Time-based plant simulation with ``plant.simulate()``

**7. Performance Evaluation**
  
   Steady-state analysis with ``plant.evaluate()``

**8. Plant Summary**
  
   Comprehensive overview with ``plant.summary()``

Syntax Comparison Highlight
---------------------------

The example demonstrates the revolutionary syntax comparison:

**TensorFlow/Keras Neural Network**:

.. code-block:: python

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

**SPROCLIB Chemical Plant (Equivalent Syntax)**:

.. code-block:: python

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

Advanced Examples
----------------

**Multi-Objective Optimization**:

.. code-block:: python

    # Economic + Environmental optimization
    plant.compile(
        optimizer="hybrid",
        loss=["total_cost", "emissions"],
        loss_weights=[0.7, 0.3],  # 70% economic, 30% environmental
        metrics=["profit", "carbon_footprint", "energy_efficiency"]
    )

**Dynamic Process Control**:

.. code-block:: python

    # Add controllers to the plant
    from unit.controller import PIDController
    
    temp_controller = PIDController(Kp=2.0, Ki=0.5, Kd=0.1)
    plant.add_controller(temp_controller, 
                        controlled_unit="main_reactor",
                        controlled_variable="temperature",
                        manipulated_variable="coolant_flow")

**Real-time Optimization**:

.. code-block:: python

    # Continuous optimization with disturbances
    disturbances = {
        "feed_composition": lambda t: 0.8 + 0.1*np.sin(0.1*t),
        "market_price": lambda t: 2.5 + 0.3*np.random.normal()
    }
    
    results = plant.optimize_realtime(
        duration=24.0,
        reoptimize_interval=1.0,  # Re-optimize every hour
        disturbances=disturbances
    )

Educational Value
----------------

**Why This Example is Perfect for Teaching**:

✅ **Familiar Syntax** - Students already know TensorFlow/Keras
✅ **Progressive Complexity** - Builds from simple to advanced concepts
✅ **Real Engineering** - Uses actual chemical engineering principles
✅ **Immediate Feedback** - Visual results and clear outputs
✅ **Extensible** - Easy to modify and experiment with

**Learning Objectives Demonstrated**:

1. **Plant Design** - How to structure chemical processes
2. **Process Control** - PID control and optimization
3. **Economic Analysis** - Cost optimization and profitability
4. **System Integration** - How units work together
5. **Dynamic Simulation** - Time-based process behavior

Extending the Example
--------------------

**Add More Equipment**:

.. code-block:: python

    # Add heat integration
    plant.add(HeatExchanger(U=500, A=10), name="preheater")
    plant.add(HeatExchanger(U=600, A=8), name="cooler")
    
    # Add safety systems
    plant.add(ReliefValve(set_pressure=12e5), name="safety_valve")
    plant.add(EmergencyShutdown(), name="esd_system")

**Custom Optimization Objectives**:

.. code-block:: python

    def custom_objective(plant_state):
        """Custom multi-criteria optimization"""
        profit = calculate_profit(plant_state)
        safety = calculate_safety_margin(plant_state)
        sustainability = calculate_sustainability_index(plant_state)
        
        return 0.5*profit + 0.3*safety + 0.2*sustainability
    
    plant.compile(optimizer=custom_objective, loss="custom")

**Integration with External Systems**:

.. code-block:: python

    # Connect to real-time data
    plant.connect_realtime_data(
        data_source="plant_historian",
        update_frequency=60  # seconds
    )
    
    # Export to process simulators
    plant.export_to_aspen_plus("plant_model.apw")
    plant.export_to_hysys("plant_model.hsc")

Why This Example Matters
------------------------

**🏆 Industry First**: First semantic API for chemical plant design
**🎓 Educational Revolution**: Makes process control accessible to everyone  
**🚀 Rapid Prototyping**: Design plants in minutes instead of hours
**🔬 Research Platform**: Perfect for advanced control research
**🌍 Open Source**: Community-driven development and improvement

This example demonstrates that complex chemical plant design can be as intuitive
and accessible as machine learning model development.

See Also
--------
- :doc:`semantic_plant_design` - Complete API documentation
- :doc:`tensorflow_comparison` - Detailed syntax comparisons
- :doc:`plant_optimization` - Advanced optimization techniques
- :doc:`examples/process_units` - Individual unit examples
