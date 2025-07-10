Analysis Legacy Package
=======================

.. note::
   This documentation covers the legacy analysis interface.
   
   **For new projects, use the modular analysis package instead:**
   :doc:`analysis_package` - Modern modular analysis structure
   
   The legacy interface is maintained for backward compatibility via the legacy package.

The analysis module provides essential tools for process control system analysis, including transfer functions, simulation capabilities, optimization algorithms, and batch scheduling.

.. note::
   The analysis module contains core mathematical and simulation tools that complement the physical process units. These tools work together with the modular unit structure to provide complete process control capabilities.
   
   For examples of analysis tools integrated with process units, see:
   
   * :doc:`../examples` - Comprehensive examples showing analysis integration
   * :doc:`units_package` - Process units that work with analysis tools

Analysis Documentation
----------------------

.. automodule:: sproclib.analysis
   :members:
   :undoc-members:
   :show-inheritance:

Detailed Documentation

The analysis module provides tools for system analysis, simulation, optimization, and batch scheduling.

Classes
-------

.. automodule:: sproclib.analysis
   :members:
   :undoc-members:
   :show-inheritance:

TransferFunction
~~~~~~~~~~~~~~~~

.. autoclass:: sproclib.analysis.TransferFunction
   :members:
   :special-members: __init__
   :show-inheritance:

The TransferFunction class provides comprehensive frequency domain analysis capabilities.

**Mathematical Foundation:**

A transfer function represents the relationship between input and output in the Laplace domain:

.. math::
   G(s) = \\frac{Y(s)}{U(s)} = \\frac{b_n s^n + b_{n-1} s^{n-1} + \\ldots + b_1 s + b_0}{a_m s^m + a_{m-1} s^{m-1} + \\ldots + a_1 s + a_0}

Common forms include:

* **First Order Plus Dead Time (FOPDT):** :math:`G(s) = \\frac{K e^{-\\theta s}}{\\tau s + 1}`
* **Second Order:** :math:`G(s) = \\frac{K \\omega_n^2}{s^2 + 2\\zeta\\omega_n s + \\omega_n^2}`

Example Usage::

    from analysis import TransferFunction
    
    # Create FOPDT transfer function
    tf = TransferFunction.first_order_plus_dead_time(
        K=2.0, tau=5.0, theta=1.0, name="Process"
    )
    
    # Frequency domain analysis
    bode_data = tf.bode_plot(plot=True)
    
    # Stability analysis
    stability = tf.stability_analysis()
    print(f"Stable: {stability['stable']}")
    print(f"Gain margin: {stability['gain_margin_db']:.1f} dB")

Simulation
~~~~~~~~~~

.. autoclass:: analysis.Simulation
   :members:
   :special-members: __init__
   :show-inheritance:

The Simulation class provides ODE integration capabilities for process models.

**Integration Methods:**

Supports multiple integration algorithms:

* **RK45** - Runge-Kutta 4(5) method (default, adaptive)
* **RK23** - Runge-Kutta 2(3) method (faster, less accurate)
* **BDF** - Backward Differentiation Formula (for stiff systems)
* **LSODA** - Automatic stiffness detection

Example Usage::

    from analysis import Simulation
    from models import Tank
    
    # Create model and simulator
    tank = Tank(A=1.0, C=2.0)
    sim = Simulation(tank)
    
    # Define simulation parameters
    time_span = (0, 20)
    initial_state = [1.0]  # h0 = 1.0 m
    
    def input_function(t):
        return [2.0 + 0.5 * np.sin(0.1 * t)]  # Sinusoidal input
    
    # Run simulation
    result = sim.simulate(time_span, initial_state, input_function)
    
    # Plot results
    plt.plot(result.t, result.y[0])
    plt.xlabel('Time (min)')
    plt.ylabel('Height (m)')

Optimization
~~~~~~~~~~~~

.. autoclass:: analysis.Optimization
   :members:
   :special-members: __init__
   :show-inheritance:

The Optimization class provides linear and nonlinear optimization capabilities.

**Problem Types:**

* **Linear Programming** - Optimize linear objectives subject to linear constraints
* **Nonlinear Programming** - General constrained optimization
* **Parameter Estimation** - Fit model parameters to data

Example Usage::

    from analysis import Optimization
    import numpy as np
    
    # Create optimizer
    optimizer = Optimization()
    
    # Linear programming example
    c = np.array([1, 2])  # Minimize x1 + 2*x2
    A_ub = np.array([[1, 1], [2, 1]])  # Constraints
    b_ub = np.array([3, 4])
    
    result = optimizer.linear_programming(c, A_ub, b_ub)
    print(f"Optimal solution: x = {result['x']}")
    print(f"Optimal value: {result['fun']:.2f}")
    
    # Nonlinear optimization example
    def objective(x):
        return x[0]**2 + x[1]**2
    
    def constraint(x):
        return x[0] + x[1] - 1
    
    x0 = [0.5, 0.5]
    constraints = {'type': 'eq', 'fun': constraint}
    
    result = optimizer.nonlinear_programming(objective, x0, constraints=constraints)

StateTaskNetwork
~~~~~~~~~~~~~~~~

.. autoclass:: analysis.StateTaskNetwork
   :members:
   :special-members: __init__
   :show-inheritance:

The StateTaskNetwork class provides batch process scheduling and optimization.

**Scheduling Framework:**

State-Task Networks (STN) model batch processes as:

* **States** - Raw materials, intermediates, products
* **Tasks** - Processing operations (reactions, separations, etc.)
* **Resources** - Equipment units, utilities

The optimization objective is typically profit maximization:

.. math::
   \\max \\sum_{i} p_i S_{i,final} - \\sum_{j,t} c_j R_{j,t}

Subject to material balances, capacity constraints, and timing constraints.

Example Usage::

    from analysis import StateTaskNetwork
    
    # Define states (materials)
    states = {
        'Raw_A': {'initial': 100, 'price': 1.0},
        'Raw_B': {'initial': 50, 'price': 1.5},
        'Product': {'initial': 0, 'price': 10.0}
    }
    
    # Define tasks (operations)
    tasks = {
        'React': {
            'inputs': {'Raw_A': 2, 'Raw_B': 1},
            'outputs': {'Product': 1},
            'duration': 4,
            'cost': 50
        }
    }
    
    # Create and solve STN
    stn = StateTaskNetwork(states, tasks)
    result = stn.optimize_schedule(horizon=24)
    
    print(f"Total profit: ${result['profit']:.2f}")
    print(f"Final inventories: {result['final_states']}")

Methods
-------

TransferFunction Methods
~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: analysis.TransferFunction.step_response
.. automethod:: analysis.TransferFunction.bode_plot
.. automethod:: analysis.TransferFunction.stability_analysis
.. automethod:: analysis.TransferFunction.first_order_plus_dead_time
.. automethod:: analysis.TransferFunction.second_order

Simulation Methods
~~~~~~~~~~~~~~~~~~

.. automethod:: analysis.Simulation.simulate
.. automethod:: analysis.Simulation.set_integration_method

Optimization Methods
~~~~~~~~~~~~~~~~~~~~

.. automethod:: analysis.Optimization.linear_programming
.. automethod:: analysis.Optimization.nonlinear_programming
.. automethod:: analysis.Optimization.parameter_estimation

StateTaskNetwork Methods
~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: analysis.StateTaskNetwork.add_state
.. automethod:: analysis.StateTaskNetwork.add_task
.. automethod:: analysis.StateTaskNetwork.optimize_schedule

Advanced Features
-----------------

Frequency Domain Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~

The TransferFunction class provides comprehensive frequency domain tools:

* **Bode Plots** - Magnitude and phase vs. frequency
* **Nyquist Plots** - Complex plane representation
* **Root Locus** - Pole locations vs. parameter variation
* **Stability Margins** - Gain and phase margins

Stiff System Integration
~~~~~~~~~~~~~~~~~~~~~~~~

For chemically reacting systems (like CSTR), use appropriate integrators::

    sim = Simulation(cstr_model)
    sim.set_integration_method('BDF')  # Better for stiff systems
    
    result = sim.simulate(
        time_span=(0, 100),
        initial_state=[0.5, 350],  # [CA, T]
        input_function=lambda t: [10, 1.0, 300, 290],  # [q, CA_in, T_in, T_cool]
        rtol=1e-6, atol=1e-9  # Tight tolerances for accuracy
    )

Multi-Objective Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For problems with multiple objectives::

    def multi_objective(x):
        profit = revenue(x) - cost(x)
        environmental_impact = emissions(x)
        return [profit, environmental_impact]  # Return list for multi-objective
    
    # Use weighted sum approach
    def weighted_objective(x, weights=[0.7, 0.3]):
        objectives = multi_objective(x)
        return -(weights[0] * objectives[0] - weights[1] * objectives[1])

Performance Considerations
--------------------------

* **Integration Tolerances** - Balance accuracy vs. computation time
* **Optimization Algorithms** - Choose appropriate solver for problem type
* **Memory Management** - Use appropriate time steps for large simulations
* **Parallel Processing** - Consider parallel evaluation for batch optimization

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Integration Failures:**
   - Try different integration methods (BDF for stiff systems)
   - Adjust tolerances (rtol, atol)
   - Check model equations for discontinuities

**Optimization Convergence:**
   - Provide good initial guesses
   - Check constraint feasibility
   - Scale variables to similar magnitudes

**Memory Issues:**
   - Reduce simulation time spans or increase time steps
   - Use sparse matrices for large optimization problems

See Also
--------

* :doc:`functions_legacy_package` - Utility functions for analysis
* :doc:`models_legacy_package` - Process models to analyze
* :doc:`../theory` - Mathematical background on control theory
