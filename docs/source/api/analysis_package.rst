Analysis Package
================

The analysis package provides comprehensive tools for process control system analysis,
including transfer functions, system analysis, and model identification.

.. note::
   This is part of the modern modular structure of SPROCLIB.

Submodules
----------

Transfer Function
~~~~~~~~~~~~~~~~~

.. automodule:: sproclib.analysis.transfer_function
   :members:
   :undoc-members:
   :show-inheritance:

System Analysis
~~~~~~~~~~~~~~~

.. automodule:: sproclib.analysis.system_analysis
   :members:
   :undoc-members:
   :show-inheritance:

Model Identification
~~~~~~~~~~~~~~~~~~~~

.. automodule:: sproclib.analysis.model_identification
   :members:
   :undoc-members:
   :show-inheritance:

Quick Usage
-----------

Transfer Function Analysis::

    from analysis.transfer_function import TransferFunction
    from analysis.system_analysis import step_response, bode_plot
    
    # Create a transfer function
    tf = TransferFunction([1], [1, 1], name="First Order")
    
    # Analyze step response
    response = step_response(tf)
    
    # Generate Bode plot
    bode_data = bode_plot(tf, plot=True)

Model Identification::

    from analysis.model_identification import fit_fopdt
    import numpy as np
    
    # Generate sample data
    t = np.linspace(0, 20, 100)
    y = 2 * (1 - np.exp(-t/3))  # FOPDT response
    
    # Fit FOPDT model
    result = fit_fopdt(t, y)
    print(f"K={result['K']:.2f}, tau={result['tau']:.2f}")
