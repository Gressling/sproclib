Scheduling Package
==================

The scheduling package provides batch process scheduling tools including
State-Task Networks for production scheduling optimization.

.. note::
   This is part of the modern modular structure of SPROCLIB. For legacy compatibility,
   see :doc:`legacy`.

Submodules
----------

State-Task Network
~~~~~~~~~~~~~~~~~~

.. automodule:: sproclib.scheduling.state_task_network
   :members:
   :undoc-members:
   :show-inheritance:

Quick Usage
-----------

Batch Process Scheduling::

    from scheduling.state_task_network import StateTaskNetwork
    
    # Create State-Task Network
    stn = StateTaskNetwork("Batch Plant")
    
    # Add states (materials)
    stn.add_state("Raw_A", capacity=1000, initial_amount=500, price=10)
    stn.add_state("Raw_B", capacity=800, initial_amount=300, price=15)
    stn.add_state("Product", capacity=500, initial_amount=0, price=50)
    
    # Add tasks (operations)
    stn.add_task(
        name="React",
        duration=2.0,
        inputs={"Raw_A": 2.0, "Raw_B": 1.0},
        outputs={"Product": 1.0},
        suitable_units=["Reactor1", "Reactor2"]
    )
    
    # Add units (equipment)
    stn.add_unit("Reactor1", capacity=100, unit_cost=50)
    stn.add_unit("Reactor2", capacity=150, unit_cost=75)
    
    # Optimize schedule
    result = stn.optimize_schedule(
        time_horizon=24,
        objective='profit',
        demand={"Product": 200}
    )
    
    # Visualize schedule
    stn.plot_schedule()
    
    print(f"Total profit: ${result['profit']:.2f}")
    print(f"Schedule feasible: {result['feasible']}")
