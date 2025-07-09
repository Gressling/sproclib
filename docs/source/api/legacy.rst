Legacy Package
==============

The legacy package provides backward compatibility for existing SPROCLIB code.
It contains wrapper modules that maintain the old API while internally using
the new modular structure.

.. warning::
   The legacy package is deprecated and will be removed in a future version.
   Please migrate to the modern modular packages:
   
   * :doc:`analysis_package` - Analysis tools
   * :doc:`simulation_package` - Simulation capabilities  
   * :doc:`optimization_package` - Optimization algorithms
   * :doc:`scheduling_package` - Batch scheduling
   * :doc:`utilities_package` - Control utilities

Migration Guide
---------------

The legacy modules provide the same functionality as before, but with deprecation warnings.
Here's how to migrate your code:

Legacy Analysis Module
~~~~~~~~~~~~~~~~~~~~~~

**Old way (deprecated):**

.. code-block:: python

    from legacy.analysis import TransferFunction, Simulation
    from legacy.functions import step_response, tune_pid

**New way (recommended):**

.. code-block:: python

    from analysis.transfer_function import TransferFunction
    from simulation.process_simulation import ProcessSimulation
    from analysis.system_analysis import step_response
    from utilities.control_utils import tune_pid

Legacy Functions Module
~~~~~~~~~~~~~~~~~~~~~~~

**Old way (deprecated):**

.. code-block:: python

    from legacy.functions import (
        step_response, bode_plot, tune_pid, 
        simulate_process, optimize_operation
    )

**New way (recommended):**

.. code-block:: python

    from analysis.system_analysis import step_response, bode_plot
    from utilities.control_utils import tune_pid, simulate_process
    from optimization.economic_optimization import optimize_operation

Benefits of Migration
---------------------

Migrating to the new modular structure provides:

* **Better Organization**: Functions grouped by purpose
* **Improved Performance**: Only import what you need
* **Enhanced Documentation**: Module-specific documentation
* **Future Support**: New features added to modular packages
* **Type Safety**: Better IDE support and type hints

Legacy Modules Reference
------------------------

.. note::
   These modules are provided for backward compatibility only.
   All new development should use the modern modular packages.

For detailed documentation of legacy interfaces, see:

.. toctree::
   :maxdepth: 1
   :caption: Legacy Interface Documentation

   analysis_legacy_package
   controllers_legacy_package
   functions_legacy_package
   models_legacy_package

Legacy Package API
~~~~~~~~~~~~~~~~~~

.. automodule:: legacy
   :members:
   :undoc-members:
   :show-inheritance:
