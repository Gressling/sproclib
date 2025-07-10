Simulation Package
==================

The simulation package provides dynamic simulation capabilities for process control systems
with integrated control loops, disturbances, and performance monitoring.

.. note::
   This is part of the modern modular structure of SPROCLIB. For legacy compatibility,
   see :doc:`legacy`.

Submodules
----------

Process Simulation
~~~~~~~~~~~~~~~~~~

.. automodule:: sproclib.simulation.process_simulation
   :members:
   :undoc-members:
   :show-inheritance:

Quick Usage
-----------

Basic Process Simulation::

    from simulation.process_simulation import ProcessSimulation
    import numpy as np
    
    # Define a simple process model
    def tank_model(t, x, u):
        # Tank dynamics: dh/dt = (Fin - Fout)/A
        h = x[0]
        Fin = u[0]
        Fout = 2.0 * np.sqrt(h) if h > 0 else 0
        return [(Fin - Fout) / 1.0]  # Area = 1.0
    
    # Create simulation
    sim = ProcessSimulation(tank_model, name="Tank Simulation")
    
    # Define input profile
    def input_profile(t):
        return [3.0]  # Constant inlet flow
    
    # Run simulation
    results = sim.run_open_loop(
        t_span=(0, 20),
        x0=[1.0],  # Initial height
        u_profile=input_profile
    )
    
    # Plot results
    sim.plot_results()
