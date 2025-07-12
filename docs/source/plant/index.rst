Semantic Plant Design
=====================

🎯 **The Revolutionary TensorFlow/Keras-Style API for Chemical Plant Design**

SPROCLIB introduces a groundbreaking semantic API for chemical plant design that brings the familiar, 
intuitive patterns from machine learning frameworks like TensorFlow and Keras to chemical process control.

.. toctree::
   :maxdepth: 2
   :caption: Semantic Plant Design:

   semantic_plant_design
   semantic_examples
   tensorflow_comparison
   simple_example/index

Overview
--------

The semantic plant design API represents a paradigm shift in how chemical engineers approach process design:

* **Familiar ML Syntax**: Leverage TensorFlow/Keras knowledge for chemical plant design
* **Rapid Prototyping**: Build complex plants in minutes, not hours  
* **Educational Excellence**: Perfect for teaching process control concepts
* **Professional Results**: Industrial-grade calculations with intuitive syntax

Key Features
------------

**Sequential Plant Building**
    Add units to your plant like adding layers to a neural network::

        plant = ChemicalPlant(name="Production Plant")
        plant.add(CentrifugalPump(H0=50.0, eta=0.75), name="feed_pump")
        plant.add(CSTR(V=150.0, k0=7.2e10), name="reactor")

**Functional Connections**
    Connect units with explicit stream specifications::

        plant.connect("feed_pump", "reactor", "feed_stream")

**ML-Style Compilation**
    Configure optimization objectives like compiling a model::

        plant.compile(
            optimizer="economic",
            loss="total_cost",
            metrics=["profit", "conversion"]
        )

**Training-Style Optimization**
    Optimize your plant like training a model::

        plant.optimize(target_production=1000.0)

Getting Started
---------------

1. **Quick Start**: Jump right into the :doc:`semantic_examples` for working code
2. **API Reference**: Learn the complete API in :doc:`semantic_plant_design`
3. **Comparison**: See how it compares to TensorFlow in :doc:`tensorflow_comparison`
4. **Simple Tutorial**: Follow the step-by-step guide in :doc:`simple_example/index`

Why Semantic Design?
--------------------

**Before SPROCLIB:**

.. code-block:: python

   # Traditional approach - verbose and complex
   from complex_process_library import *
   
   # Create components with complex configuration
   pump = CentrifugalPump()
   pump.set_head(50.0)
   pump.set_efficiency(0.75)
   pump.configure_performance_curve(...)
   
   reactor = CSTR()
   reactor.set_volume(150.0)
   reactor.set_kinetic_parameters(k0=7.2e10, Ea=...)
   reactor.configure_heat_transfer(...)
   
   # Complex connection management
   stream1 = ProcessStream(...)
   pump.connect_outlet(stream1)
   reactor.connect_inlet(stream1)
   
   # Manual optimization setup
   optimizer = EconomicOptimizer()
   optimizer.add_objective("minimize_cost")
   optimizer.add_constraint("production_target", 1000.0)
   # ... many more lines of configuration

**With SPROCLIB Semantic API:**

.. code-block:: python

   # Semantic approach - clean and intuitive
   from sproclib.unit.plant import ChemicalPlant
   from sproclib.unit.reactor.cstr import CSTR
   from sproclib.unit.pump import CentrifugalPump
   
   # Build plant like a neural network
   plant = ChemicalPlant(name="Production Plant")
   plant.add(CentrifugalPump(H0=50.0, eta=0.75), name="feed_pump")
   plant.add(CSTR(V=150.0, k0=7.2e10), name="reactor")
   
   # Connect with simple, clear syntax
   plant.connect("feed_pump", "reactor", "feed_stream")
   
   # Compile like a machine learning model
   plant.compile(
       optimizer="economic",
       loss="total_cost", 
       metrics=["profit", "conversion"]
   )
   
   # Optimize like training a model
   plant.optimize(target_production=1000.0)

Benefits
--------

✅ **Familiar Patterns**: Leverage existing ML/TensorFlow knowledge
✅ **Reduced Code**: 70% less code compared to traditional approaches
✅ **Better Readability**: Self-documenting, intuitive syntax
✅ **Faster Development**: Rapid prototyping and iteration
✅ **Educational Value**: Easier to learn and teach
✅ **Professional Grade**: Full industrial capabilities maintained

Applications
------------

The semantic API is perfect for:

* **Process Design**: Rapid prototyping of new plant configurations
* **Education**: Teaching chemical process control concepts
* **Research**: Quick exploration of process alternatives
* **Control System Design**: Intuitive controller development
* **Optimization Studies**: Economic and operational optimization

See Also
--------

* :doc:`../unit/index` - Complete unit operations documentation
* :doc:`../tutorials` - Step-by-step learning guides
* :doc:`../api/index` - Complete API reference
