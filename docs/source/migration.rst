Migration Guide
===============

This guide helps you migrate from the legacy SPROCLIB structure to the modern modular architecture.

Why Migrate?
------------

The new modular structure provides:

* **Better Organization**: Functions grouped by purpose (analysis, simulation, optimization, etc.)
* **Improved Performance**: Import only what you need
* **Enhanced Documentation**: Module-specific documentation and examples
* **Future Support**: New features will be added to modular packages
* **Type Safety**: Better IDE support with type hints
* **Maintainability**: Easier to understand and extend

Migration Steps
---------------

1. **Identify Legacy Imports**
   
   Look for these patterns in your code::
   
       from analysis import TransferFunction, Simulation
       from functions import step_response, tune_pid
       import analysis
       import functions

2. **Replace with Modern Imports**
   
   Update to the new modular structure:
   
   .. code-block:: python
   
       # OLD (legacy)
       from analysis import TransferFunction
       from functions import step_response, tune_pid
       
       # NEW (modern)
       from analysis.transfer_function import TransferFunction
       from analysis.system_analysis import step_response
       from utilities.control_utils import tune_pid

3. **Update Function Calls**
   
   Most function calls remain the same, but some may have enhanced APIs:
   
   .. code-block:: python
   
       # Function calls typically don't change
       tf = TransferFunction([1], [1, 1])
       response = step_response(tf)
       params = tune_pid(model_params)

Common Migration Patterns
-------------------------

Analysis Module
~~~~~~~~~~~~~~~

**Legacy:**

.. code-block:: python

    from analysis import TransferFunction, Simulation, Optimization

**Modern:**

.. code-block:: python

    from analysis.transfer_function import TransferFunction
    from simulation.process_simulation import ProcessSimulation
    from optimization.economic_optimization import EconomicOptimization

Functions Module
~~~~~~~~~~~~~~~~

**Legacy:**

.. code-block:: python

    from functions import (
        step_response, bode_plot, tune_pid, 
        simulate_process, optimize_operation, fit_fopdt
    )

**Modern:**

.. code-block:: python

    from analysis.system_analysis import step_response, bode_plot
    from utilities.control_utils import tune_pid, simulate_process
    from optimization.economic_optimization import optimize_operation
    from analysis.model_identification import fit_fopdt

Complete Migration Example
--------------------------

**Legacy Code:**

.. code-block:: python

    # Old imports
    from analysis import TransferFunction, Simulation
    from functions import step_response, tune_pid, fit_fopdt
    
    # Create transfer function
    tf = TransferFunction([2], [5, 1])
    
    # Analyze step response
    response = step_response(tf)
    
    # Tune PID controller
    model_params = {'K': 2.0, 'tau': 5.0, 'theta': 1.0}
    pid_params = tune_pid(model_params)
    
    # Fit FOPDT model to data
    result = fit_fopdt(t_data, y_data)

**Modern Code:**

.. code-block:: python

    # New modular imports
    from analysis.transfer_function import TransferFunction
    from analysis.system_analysis import step_response
    from utilities.control_utils import tune_pid
    from analysis.model_identification import fit_fopdt
    
    # Create transfer function (same API)
    tf = TransferFunction([2], [5, 1])
    
    # Analyze step response (same API)
    response = step_response(tf)
    
    # Tune PID controller (same API)
    model_params = {'K': 2.0, 'tau': 5.0, 'theta': 1.0}
    pid_params = tune_pid(model_params)
    
    # Fit FOPDT model to data (same API)
    result = fit_fopdt(t_data, y_data)

Gradual Migration Strategy
--------------------------

You don't need to migrate everything at once:

1. **Start with New Code**: Use modern imports for all new development
2. **Update Imports Gradually**: Replace legacy imports file by file
3. **Use Legacy Bridge**: Keep legacy imports temporarily where needed
4. **Test Thoroughly**: Ensure functionality remains the same

Compatibility Period
--------------------

* **Current Status**: Legacy imports work with deprecation warnings
* **Deprecation Timeline**: Legacy support will be maintained for several versions
* **Future Removal**: Legacy modules will eventually be removed (with advance notice)

Getting Help
------------

If you encounter issues during migration:

* Check the :doc:`api/legacy` documentation for mapping details
* Review :doc:`examples` for modern usage patterns
* Compare legacy and modern code side-by-side
* The APIs are designed to be nearly identical for easy migration

.. tip::
   **Pro Tip**: Start by updating your imports first, then test your code.
   Most function calls will work exactly the same way!
