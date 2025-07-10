Process Control Package API Documentation
==========================================

Complete API documentation for the Standard Process Control Library (SPROCLIB).

.. note::
   **Recommended for New Development**: Use the modern modular packages listed below.
   Legacy modules are maintained for backward compatibility but should be avoided
   for new projects.

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

Legacy Compatibility
~~~~~~~~~~~~~~~~~~~~

For backward compatibility with existing code:

.. toctree::
   :maxdepth: 2

   units_package
   controllers_package
   legacy

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

**Legacy Support**
  * ``legacy/`` - Deprecated interfaces with migration guidance

Migration Guide
---------------

**From Legacy to Modern API:**

Old (still works with warnings)::

    from process_control import TransferFunction, tune_pid
    from analysis import step_response

New (recommended)::

    from sproclib.analysis.transfer_function import TransferFunction
    from sproclib.utilities.control_utils import tune_pid
    from sproclib.analysis.system_analysis import step_response

**Benefits of Modern API:**
- Faster import times (import only what you need)
- Better organization and discoverability
- Enhanced type hints and documentation
- Improved testing and reliability
- Future-proof design for new features

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
1. Review :doc:`../migration` for upgrading from legacy code
2. Explore :doc:`optimization_package` for advanced features
3. Consult :doc:`utilities_package` for specialized tools

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
