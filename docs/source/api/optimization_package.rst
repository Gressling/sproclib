Optimization Package
====================

The optimization package provides economic optimization tools, process optimization,
and parameter estimation capabilities for process control systems.

.. note::
   This is part of the modern modular structure of SPROCLIB. For legacy compatibility,
   see :doc:`legacy`.

Submodules
----------

Economic Optimization
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: sproclib.optimization.economic_optimization
   :members:
   :undoc-members:
   :show-inheritance:

Parameter Estimation
~~~~~~~~~~~~~~~~~~~~

.. automodule:: sproclib.optimization.parameter_estimation
   :members:
   :undoc-members:
   :show-inheritance:

Process Optimization
~~~~~~~~~~~~~~~~~~~~

.. automodule:: sproclib.optimization.process_optimization
   :members:
   :undoc-members:
   :show-inheritance:

Quick Usage
-----------

Economic Optimization::

    from optimization.economic_optimization import EconomicOptimization
    import numpy as np
    
    # Create optimizer
    optimizer = EconomicOptimization("Production Planning")
    
    # Define production planning problem
    costs = np.array([10, 15, 20])      # Production costs
    prices = np.array([25, 30, 35])     # Product prices
    capacity = np.array([100, 80, 60])  # Production capacities
    demand = np.array([50, 40, 30])     # Market demand
    
    # Solve optimization
    result = optimizer.production_optimization(
        costs=costs,
        prices=prices,
        capacity_constraints=capacity,
        demand_constraints=demand
    )
    
    print(f"Optimal production: {result['optimal_production']}")
    print(f"Maximum profit: ${result['max_profit']:.2f}")

Parameter Estimation::

    from optimization.parameter_estimation import ParameterEstimation
    
    # Create parameter estimator
    estimator = ParameterEstimation()
    
    # Estimate parameters from data
    result = estimator.least_squares_estimation(
        data=data,
        model=model_function,
        initial_guess=[1.0, 2.0]
    )
