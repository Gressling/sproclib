Pipeline Flow Examples
======================

This section provides practical examples of pipeline flow analysis and modeling using the transport module.

Overview
--------

Pipeline flow is fundamental to many chemical processes. These examples demonstrate:

- Basic pipeline flow calculations
- Pressure drop analysis
- Flow rate optimization
- Multi-phase flow considerations

Basic Pipeline Flow
-------------------

Example 1: Single-Phase Liquid Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import numpy as np
    from transport.continuous.liquid import PipeFlow
    
    # Create a pipeline system
    pipeline = PipeFlow(
        diameter=0.1,  # 10 cm diameter
        length=100,    # 100 m length
        roughness=0.00015  # Steel pipe roughness
    )
    
    # Set fluid properties
    pipeline.set_fluid_properties(
        density=1000,      # kg/m³
        viscosity=0.001,   # Pa·s
        temperature=20     # °C
    )
    
    # Calculate pressure drop for given flow rate
    flow_rate = 0.01  # m³/s
    pressure_drop = pipeline.calculate_pressure_drop(flow_rate)
    
    print(f"Pressure drop: {pressure_drop:.2f} Pa")

Example 2: Flow Rate Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import matplotlib.pyplot as plt
    
    # Analyze flow rates vs pressure drop
    flow_rates = np.linspace(0.001, 0.02, 50)
    pressure_drops = [pipeline.calculate_pressure_drop(q) for q in flow_rates]
    
    # Plot the relationship
    plt.figure(figsize=(10, 6))
    plt.plot(flow_rates, pressure_drops)
    plt.xlabel('Flow Rate (m³/s)')
    plt.ylabel('Pressure Drop (Pa)')
    plt.title('Pipeline Flow Rate vs Pressure Drop')
    plt.grid(True)
    plt.show()

Advanced Pipeline Systems
-------------------------

Example 3: Pipeline Network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from transport.continuous.liquid import PipelineNetwork
    
    # Create a network of connected pipes
    network = PipelineNetwork()
    
    # Add pipeline segments
    network.add_pipe('segment1', diameter=0.1, length=50, roughness=0.00015)
    network.add_pipe('segment2', diameter=0.08, length=75, roughness=0.00015)
    network.add_pipe('segment3', diameter=0.12, length=30, roughness=0.00015)
    
    # Connect pipes in series
    network.connect_series(['segment1', 'segment2', 'segment3'])
    
    # Calculate total system pressure drop
    total_pressure_drop = network.calculate_system_pressure_drop(flow_rate=0.01)
    
    print(f"Total system pressure drop: {total_pressure_drop:.2f} Pa")

Example 4: Pipe Sizing Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from scipy.optimize import minimize_scalar
    
    def cost_function(diameter):
        """Total cost function including pumping and pipe costs"""
        # Create pipeline with given diameter
        pipe = PipeFlow(diameter=diameter, length=100, roughness=0.00015)
        pipe.set_fluid_properties(density=1000, viscosity=0.001)
        
        # Calculate pressure drop
        pressure_drop = pipe.calculate_pressure_drop(0.01)
        
        # Calculate costs (simplified model)
        pipe_cost = 1000 * diameter**2  # Material cost
        pumping_cost = pressure_drop * 0.001  # Pumping cost
        
        return pipe_cost + pumping_cost
    
    # Optimize pipe diameter
    result = minimize_scalar(cost_function, bounds=(0.05, 0.3), method='bounded')
    optimal_diameter = result.x
    
    print(f"Optimal pipe diameter: {optimal_diameter:.3f} m")

Troubleshooting
---------------

Common Issues and Solutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **High Pressure Drop**
   - Check for pipe blockages
   - Verify fluid properties
   - Consider pipe diameter increase

2. **Flow Instabilities**
   - Ensure adequate NPSHa for pumps
   - Check for cavitation conditions
   - Verify system design margins

3. **Accuracy Issues**
   - Use appropriate friction factor correlations
   - Account for pipe fittings and valves
   - Consider non-Newtonian fluid behavior

See Also
--------

- :doc:`peristaltic_pump_examples`
- :doc:`slurry_transport_examples`
- :doc:`../pump_systems`
- :doc:`../../api/transport_package`
