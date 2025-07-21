Economic Optimization
====================

.. currentmodule:: sproclib.optimization.economic_optimization

.. autoclass:: EconomicOptimization
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The :class:`EconomicOptimization` class provides comprehensive economic optimization capabilities specifically designed for chemical engineering applications. It enables engineers to optimize production planning, utility systems, investment decisions, and implement economic model predictive control for maximum profitability and cost efficiency.

Key Features
------------

* **Linear Programming (LP)**: Efficient solution of large-scale linear optimization problems
* **Production Planning**: Multi-product manufacturing optimization with capacity and demand constraints
* **Utility Optimization**: Cost-effective scheduling of steam, electricity, and cooling systems
* **Investment Analysis**: Capital allocation optimization using NPV and ROI metrics
* **Economic MPC**: Real-time economic optimization for process control
* **Multi-objective**: Balance between cost, profit, and operational constraints

Applications
------------

Production Planning and Scheduling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Multi-product chemical plant optimization
* Resource allocation across product lines
* Capacity utilization optimization
* Demand fulfillment strategies
* Supply chain optimization

Utility System Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Steam system cost minimization
* Electrical load management
* Cooling water optimization
* Compressed air system efficiency
* Cogeneration planning

Investment Decision Making
~~~~~~~~~~~~~~~~~~~~~~~~~

* Capital project portfolio optimization
* Equipment replacement analysis
* Technology upgrade evaluations
* Expansion project prioritization
* Risk-adjusted return analysis

Economic Model Predictive Control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Real-time profit optimization
* Dynamic pricing response
* Energy cost minimization
* Production rate optimization
* Quality vs. cost trade-offs

Technical Specifications
-------------------------

Optimization Algorithms
~~~~~~~~~~~~~~~~~~~~~~~

* **Linear Programming**: HIGHS solver (default), Simplex method
* **Nonlinear Programming**: SLSQP, Interior Point methods
* **Integer Programming**: Branch and bound for discrete decisions
* **Economic MPC**: Receding horizon optimization

Economic Models
~~~~~~~~~~~~~~~

* **Net Present Value (NPV)**: Time value of money calculations
* **Internal Rate of Return (IRR)**: Profitability assessment
* **Payback Period**: Investment recovery analysis
* **Life Cycle Cost (LCC)**: Total ownership cost evaluation
* **Operating Expense (OPEX)**: Variable cost optimization
* **Capital Expense (CAPEX)**: Fixed cost planning

Financial Parameters
~~~~~~~~~~~~~~~~~~~~

* **Discount Rate**: Cost of capital (typically 8-15% for chemical industry)
* **Time Horizon**: Project evaluation period (1-30 years)
* **Tax Considerations**: Depreciation and tax effects
* **Inflation Adjustment**: Real vs. nominal cash flows
* **Risk Assessment**: Uncertainty and sensitivity analysis

Mathematical Foundation
-----------------------

Linear Programming Formulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \\text{minimize: } c^T x

.. math::

   \\text{subject to: } A_{ub} x \\leq b_{ub} \\text{ (inequality constraints)}

.. math::

   A_{eq} x = b_{eq} \\text{ (equality constraints)}

.. math::

   x_{min} \\leq x \\leq x_{max} \\text{ (bounds)}

Where:

* :math:`x`: Decision variables (production rates, utility usage, investments)
* :math:`c`: Cost coefficients (operating costs, prices, utility rates)
* :math:`A_{ub}, b_{ub}`: Inequality constraints (capacity limits, demand requirements)
* :math:`A_{eq}, b_{eq}`: Equality constraints (material balances, energy balances)

Economic Objective Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Profit Maximization
^^^^^^^^^^^^^^^^^^^^

.. math::

   \\text{maximize: } \\text{Profit} = \\text{Revenue} - \\text{Operating\\_Cost} - \\text{Fixed\\_Cost}

.. math::

   = \\sum_i (\\text{price}_i \\times \\text{production}_i) - \\sum_i (\\text{cost}_i \\times \\text{production}_i) - \\text{Fixed\\_Costs}

Cost Minimization
^^^^^^^^^^^^^^^^^

.. math::

   \\text{minimize: } \\text{Total\\_Cost} = \\text{Operating\\_Cost} + \\text{Utility\\_Cost} + \\text{Labor\\_Cost}

.. math::

   = \\sum_i (\\text{unit\\_cost}_i \\times \\text{usage}_i) + \\sum_j (\\text{utility\\_rate}_j \\times \\text{consumption}_j) + \\text{Labor}

NPV Maximization
^^^^^^^^^^^^^^^^

.. math::

   \\text{maximize: } \\text{NPV} = \\sum_t \\frac{\\text{Cash\\_Flow}_t}{(1 + r)^t} - \\text{Initial\\_Investment}

Usage Examples
--------------

Basic Production Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sproclib.optimization.economic_optimization import EconomicOptimization

   # Create optimizer
   optimizer = EconomicOptimization("Chemical Plant Production")

   # Production data
   costs = np.array([150, 200, 180])      # $/unit production cost
   prices = np.array([300, 400, 350])     # $/unit selling price
   capacities = np.array([1000, 800, 600]) # units/day capacity

   # Optimize production
   result = optimizer.production_optimization(
       production_rates=np.zeros(3),  # Initial production
       costs=costs,
       prices=prices,
       capacity_constraints=capacities
   )

   print(f"Optimal production: {result['optimal_production']}")
   print(f"Daily profit: ${result['total_profit']:,.0f}")

Utility System Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Utility cost data
   utility_costs = {
       'steam_hp': 15.0,    # $/GJ
       'electricity': 0.08,  # $/kWh
       'cooling': 0.05      # $/m³
   }

   # 24-hour demand profiles
   utility_demands = {
       'steam_hp': np.array([80, 85, 90, ...]),     # GJ/h for 24 hours
       'electricity': np.array([12000, 13000, ...]), # kWh/h
       'cooling': np.array([1500, 1600, ...])       # m³/h
   }

   # Optimize utility schedule
   result = optimizer.utility_optimization(
       utility_costs=utility_costs,
       utility_demands=utility_demands,
       utility_capacities=utility_capacities,
       time_horizon=24
   )

Investment Portfolio Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Investment options
   projects = [
       {'initial_cost': 2_000_000, 'annual_return': 400_000},  # Heat recovery
       {'initial_cost': 5_000_000, 'annual_return': 800_000},  # Process upgrade
       {'initial_cost': 1_500_000, 'annual_return': 350_000}   # Control system
   ]

   # Optimize investment portfolio
   result = optimizer.investment_optimization(
       investment_options=projects,
       budget_constraint=6_000_000,  # $6M budget
       time_horizon=15,              # 15 years
       discount_rate=0.10            # 10% discount rate
   )

   print(f"Selected projects: {result['selected_options']}")
   print(f"Total NPV: ${result['total_npv']:,.0f}")

Advanced Features
-----------------

Multi-Period Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~

Handle time-varying prices and demands:

.. code-block:: python

   # Weekly production planning with varying prices
   for week in range(52):
       weekly_prices = base_prices * price_factors[week]
       weekly_demands = base_demands * demand_factors[week]
       
       result = optimizer.production_optimization(
           production_rates=current_production,
           costs=costs,
           prices=weekly_prices,
           capacity_constraints=capacities,
           demand_constraints=weekly_demands
       )
       
       weekly_schedule.append(result['optimal_production'])

Stochastic Optimization
~~~~~~~~~~~~~~~~~~~~~~~

Incorporate uncertainty in prices and demands:

.. code-block:: python

   # Monte Carlo approach for uncertain parameters
   n_scenarios = 1000
   scenario_results = []

   for scenario in range(n_scenarios):
       # Sample uncertain parameters
       uncertain_prices = np.random.normal(base_prices, price_std)
       uncertain_demands = np.random.normal(base_demands, demand_std)
       
       result = optimizer.production_optimization(...)
       scenario_results.append(result)

   # Analyze risk metrics
   mean_profit = np.mean([r['total_profit'] for r in scenario_results])
   var_95 = np.percentile([r['total_profit'] for r in scenario_results], 5)

API Reference
-------------

.. automethod:: EconomicOptimization.__init__
.. automethod:: EconomicOptimization.linear_programming
.. automethod:: EconomicOptimization.production_optimization
.. automethod:: EconomicOptimization.utility_optimization
.. automethod:: EconomicOptimization.investment_optimization
.. automethod:: EconomicOptimization.economic_mpc
.. automethod:: EconomicOptimization.describe

Performance Benchmarks
-----------------------

Problem Size Capabilities
~~~~~~~~~~~~~~~~~~~~~~~~~

* **Small problems** (< 100 variables): < 1 second
* **Medium problems** (100-1,000 variables): 1-10 seconds
* **Large problems** (1,000-10,000 variables): 10-60 seconds
* **Very large problems** (> 10,000 variables): 1-10 minutes

Memory Requirements
~~~~~~~~~~~~~~~~~~~

* Linear scaling with problem size
* Typical: 1-10 MB for medium problems
* Large problems: 10-100 MB

Accuracy
~~~~~~~~

* Linear problems: Machine precision (1e-15)
* Nonlinear problems: User-specified tolerance (1e-6 typical)
* Economic calculations: Financial precision (1e-2)

Industry Applications
---------------------

Petrochemical Complex
~~~~~~~~~~~~~~~~~~~~~

* Ethylene/propylene production optimization
* Aromatics (BTX) production planning
* Utility system integration
* Maintenance scheduling

Pharmaceutical Manufacturing
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Multi-product batch scheduling
* Clean room utility optimization
* Equipment campaign planning
* Regulatory compliance optimization

Specialty Chemicals
~~~~~~~~~~~~~~~~~~~

* Custom product scheduling
* Just-in-time production
* Quality-cost trade-offs
* Waste minimization

Best Practices
--------------

Problem Formulation
~~~~~~~~~~~~~~~~~~~

1. **Clear Objectives**: Define economic goals explicitly
2. **Realistic Constraints**: Use engineering knowledge for bounds
3. **Data Quality**: Ensure accurate cost and price data
4. **Model Validation**: Verify optimization results make sense

Implementation
~~~~~~~~~~~~~~

1. **Incremental Deployment**: Start with simple problems
2. **Data Integration**: Connect to real-time plant data
3. **User Training**: Ensure operators understand economic drivers
4. **Continuous Improvement**: Regular model updates and calibration

See Also
--------

* :doc:`../process_optimization/process_optimization`
* :doc:`../parameter_estimation/parameter_estimation`
* :doc:`../../controller/index`
* :doc:`../../simulation/index`
