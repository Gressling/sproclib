Process Control Package API Documentation
==========================================

Complete API documentation for the Standard Process Control Library (SPROCLIB).

.. note::
   **Recommended for New Development**: Use the modern modular packages listed below.

Quick Navigation
----------------

**Most Common APIs:**

* :doc:`analysis_package` - System analysis and transfer functions
* :doc:`simulation_package` - Dynamic process simulation
* :doc:`utilities_package` - Control design and mathematical utilities
* :doc:`units_package` - Process equipment models

**Specialized APIs:**

* :doc:`optimization_package` - Economic and parameter optimization
* :doc:`transport_package` - Fluid transport and pipeline systems
* :doc:`scheduling_package` - Batch process scheduling

Package Overview
----------------

Modern Modular Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The SPROCLIB API is organized into focused packages, each serving specific purposes:

.. toctree::
   :maxdepth: 2

   analysis_package
   simulation_package
   optimization_package
   scheduling_package
   transport_package
   utilities_package
   units_package
   controllers_package

API Organization
----------------

**Core Analysis and Control**
  * ``analysis/`` - Transfer functions, frequency domain analysis, system identification
  * ``simulation/`` - Dynamic simulation, ODE solvers, control loop integration
  * ``utilities/`` - PID tuning, mathematical tools, data processing

**Process Modeling**
  * ``units/`` - Process equipment (tanks, reactors, pumps, valves)
  * ``transport/`` - Pipeline systems, fluid flow, multiphase transport
  * ``controllers/`` - Control algorithms and implementations

**Optimization and Planning**
  * ``optimization/`` - Economic optimization, parameter estimation
  * ``scheduling/`` - Batch process scheduling, State-Task Networks

Common Usage Patterns
---------------------

**Basic Control Design**::

    from sproclib.analysis import TransferFunction
    from sproclib.utilities import tune_pid, step_response
    
    # Create process model
    process = TransferFunction.first_order_plus_dead_time(K=2.0, tau=5.0, theta=1.0)
    
    # Tune controller
    params = tune_pid({'K': 2.0, 'tau': 5.0, 'theta': 1.0}, method='amigo')
    
    # Analyze performance
    response = step_response(process, time_span=30)

**Process Simulation**::

    from sproclib.units import Tank, CentrifugalPump
    from sproclib.simulation import ProcessSimulator
    
    # Create process components
    tank = Tank(A=10.0, h_max=5.0)
    pump = CentrifugalPump(H0=50.0, eta=0.75)
    
    # Simulate dynamics
    simulator = ProcessSimulator([tank, pump])
    result = simulator.run(time_span=100, dt=0.1)

**Economic Optimization**::

    from sproclib.optimization import EconomicOptimizer
    from sproclib.units import CSTR
    
    # Define process
    reactor = CSTR(V=150.0, k0=7.2e10)
    
    # Optimize operation
    optimizer = EconomicOptimizer(reactor)
    optimal_conditions = optimizer.maximize_profit(
        constraints={'conversion': 0.8, 'temperature': (300, 400)}
    )

Getting Started
---------------

**For Beginners:**
1. Start with :doc:`../user_guide` for step-by-step tutorials
2. Explore :doc:`analysis_package` for basic control concepts
3. Practice with :doc:`../examples` for hands-on learning

**For Experienced Users:**
1. Explore :doc:`optimization_package` for advanced features
2. Consult :doc:`utilities_package` for specialized tools

**For Developers:**
1. See :doc:`../contributing` for development guidelines
2. Review package source code for implementation details
3. Contribute examples and improvements via GitHub

Support and Resources
--------------------

- **Documentation**: Complete guides and examples throughout this site
- **GitHub Issues**: Bug reports and feature requests
- **Examples**: Working code in :doc:`../examples`
- **Theory**: Mathematical background in :doc:`../theory`
