Quick Start Guide
================

Get up and running with SPROCLIB transport modeling in minutes.

Your First Transport Model
--------------------------

Create a simple pipeline model::

    from transport.continuous.liquid import PipeFlow
    
    # Create a water pipeline
    pipeline = PipeFlow(
        pipe_length=1000.0,    # 1 km
        pipe_diameter=0.2,     # 20 cm
        name="My First Pipeline"
    )
    
    # Calculate pressure drop
    result = pipeline.steady_state([300000, 293.15, 0.05])
    print(f"Outlet pressure: {result[0]/1000:.1f} kPa")

Essential Workflows
------------------

**1. Steady-State Analysis**

::

    # Define operating conditions
    inlet_pressure = 300000  # Pa
    inlet_temperature = 293.15  # K
    flow_rate = 0.05  # m³/s
    
    # Calculate steady-state
    result = pipeline.steady_state([inlet_pressure, inlet_temperature, flow_rate])
    outlet_pressure, outlet_temperature = result

**2. Dynamic Analysis**

::

    import numpy as np
    from scipy.integrate import solve_ivp
    
    # Define system dynamics
    def system_dynamics(t, x):
        u = [300000, 293.15, 0.05]  # Constant inputs
        return pipeline.dynamics(t, x, u)
    
    # Initial conditions
    x0 = [250000, 293.15]  # Initial state
    
    # Solve ODE
    solution = solve_ivp(system_dynamics, [0, 100], x0, dense_output=True)

**3. Parameter Studies**

::

    import matplotlib.pyplot as plt
    
    # Study pressure drop vs flow rate
    flow_rates = np.linspace(0.01, 0.1, 20)
    pressure_drops = []
    
    for Q in flow_rates:
        result = pipeline.steady_state([300000, 293.15, Q])
        pressure_drop = 300000 - result[0]
        pressure_drops.append(pressure_drop)
    
    # Plot results
    plt.plot(flow_rates * 1000, np.array(pressure_drops) / 1000)
    plt.xlabel('Flow Rate (L/s)')
    plt.ylabel('Pressure Drop (kPa)')
    plt.show()

Common Tasks
------------

**Model Configuration**

::

    # Update model parameters
    pipeline.pipe_diameter = 0.25  # Change diameter
    pipeline.roughness = 5e-5      # Change roughness
    
    # Update fluid properties
    pipeline.fluid_density = 850   # Different fluid
    pipeline.fluid_viscosity = 2e-3

**Error Handling**

::

    try:
        result = pipeline.steady_state([inlet_pressure, inlet_temperature, flow_rate])
    except ValueError as e:
        print(f"Invalid operating conditions: {e}")
    except RuntimeError as e:
        print(f"Calculation failed: {e}")

**Model Validation**

::

    # Get model information
    model_info = pipeline.describe()
    print(model_info)
    
    # Check operating envelope
    max_velocity = 4.0  # m/s
    max_flow = max_velocity * np.pi * (pipeline.pipe_diameter/2)**2
    print(f"Maximum recommended flow: {max_flow*1000:.0f} L/s")

Next Steps
----------

* Explore :doc:`transport_overview` for comprehensive modeling
* Learn :doc:`pipeline_transport` for advanced techniques
* Try :doc:`examples/transport_examples` for practical applications
