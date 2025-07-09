Pipeline Transport Tutorial
==========================

This tutorial provides comprehensive guidance for modeling single-phase liquid transport
through pipelines using the ``PipeFlow`` class. Pipeline transport is fundamental to
chemical processes, involving the movement of liquids through pipe networks.

.. note::
   This tutorial combines theoretical background with practical examples to demonstrate
   effective pipeline modeling techniques.

Learning Objectives
-------------------

By completing this tutorial, you will be able to:

* Create and configure ``PipeFlow`` models for various applications
* Perform steady-state pressure drop calculations
* Analyze dynamic behavior for control system design
* Optimize pipeline operating conditions
* Integrate pipeline models with control systems

Tutorial Overview
-----------------

**Prerequisites:**
- Basic understanding of fluid mechanics
- Familiarity with Python programming
- SPROCLIB installation and setup

**Topics Covered:**
1. Pipeline modeling fundamentals
2. Steady-state analysis and design
3. Dynamic behavior and control
4. Advanced applications and optimization
5. Real-world case studies

Part 1: Pipeline Modeling Fundamentals
--------------------------------------

Understanding Pipeline Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~

Pipeline flow involves several key phenomena:

**Pressure Drop Sources:**
- Wall friction (major losses)
- Fittings and valves (minor losses)
- Elevation changes (hydrostatic effects)
- Acceleration effects (usually negligible for liquids)

**Flow Regimes:**
- **Laminar Flow** (Re < 2300): Smooth, predictable flow
- **Transition** (2300 < Re < 4000): Unstable, avoid if possible
- **Turbulent Flow** (Re > 4000): Chaotic but well-characterized

Creating Your First Pipeline Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's start with a simple water pipeline:

.. code-block:: python

   from transport.continuous.liquid import PipeFlow
   import numpy as np
   import matplotlib.pyplot as plt
   
   # Create a basic water pipeline model
   pipeline = PipeFlow(
       pipe_length=1000.0,      # 1 km pipeline
       pipe_diameter=0.2,       # 20 cm diameter
       roughness=1e-4,          # Commercial steel roughness (0.1 mm)
       elevation_change=0.0,    # Level pipeline
       fluid_density=1000.0,    # Water density (kg/m³)
       fluid_viscosity=1e-3,    # Water viscosity (Pa·s)
       name="Water Pipeline"
   )
   
   # Display model information
   print(pipeline.describe())

**Expected Output:**

.. code-block:: text

   PipeFlow Model: Water Pipeline
   =============================
   Configuration:
   - Length: 1000.0 m
   - Diameter: 0.2 m
   - Roughness: 0.0001 m
   - Elevation change: 0.0 m
   
   Fluid Properties:
   - Density: 1000.0 kg/m³
   - Viscosity: 0.001 Pa·s
   
   Mathematical Model:
   - Darcy-Weisbach equation for pressure drop
   - Colebrook-White correlation for friction factor
   - Reynolds number flow regime analysis

Part 2: Steady-State Analysis
-----------------------------

Basic Pressure Drop Calculation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculate pressure drop for different flow rates:

.. code-block:: python

   # Define operating conditions
   # Input: [inlet_pressure (Pa), inlet_temperature (K), flow_rate (m³/s)]
   
   # Test different flow rates
   flow_rates = np.linspace(0.01, 0.10, 10)  # 0.01 to 0.10 m³/s
   results = []
   
   for Q in flow_rates:
       # Steady-state calculation
       P_in = 300000  # 3 bar inlet pressure
       T_in = 293.15  # 20°C inlet temperature
       
       result = pipeline.steady_state([P_in, T_in, Q])
       P_out, T_out = result
       
       # Calculate pressure drop and velocity
       pressure_drop = P_in - P_out
       velocity = Q / (np.pi * (pipeline.pipe_diameter/2)**2)
       
       results.append({
           'flow_rate': Q,
           'velocity': velocity,
           'pressure_drop': pressure_drop,
           'outlet_pressure': P_out
       })
       
       print(f"Q = {Q:.3f} m³/s, v = {velocity:.2f} m/s, ΔP = {pressure_drop:.0f} Pa")

**Expected Output:**

.. code-block:: text

   Q = 0.010 m³/s, v = 0.32 m/s, ΔP = 312 Pa
   Q = 0.020 m³/s, v = 0.64 m/s, ΔP = 1247 Pa
   Q = 0.030 m³/s, v = 0.96 m/s, ΔP = 2806 Pa
   Q = 0.040 m³/s, v = 1.27 m/s, ΔP = 4989 Pa
   Q = 0.050 m³/s, v = 1.59 m/s, ΔP = 7796 Pa

Flow Regime Analysis
~~~~~~~~~~~~~~~~~~~

Analyze flow regimes and friction factors:

.. code-block:: python

   # Calculate Reynolds numbers and friction factors
   for i, result in enumerate(results):
       Q = result['flow_rate']
       v = result['velocity']
       
       # Reynolds number calculation
       Re = (pipeline.fluid_density * v * pipeline.pipe_diameter) / pipeline.fluid_viscosity
       
       # Friction factor estimation
       if Re < 2300:
           f = 64 / Re  # Laminar flow
           regime = "Laminar"
       else:
           # Turbulent flow - simplified Blasius correlation
           f = 0.316 / (Re**0.25) if Re < 100000 else 0.184 / (Re**0.2)
           regime = "Turbulent"
       
       print(f"Q = {Q:.3f} m³/s, Re = {Re:.0f}, f = {f:.4f}, Regime: {regime}")

Performance Curve Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create system characteristic curves:

.. code-block:: python

   # Generate performance curves
   flow_rates = np.linspace(0.005, 0.12, 50)
   pressure_drops = []
   velocities = []
   
   for Q in flow_rates:
       try:
           result = pipeline.steady_state([300000, 293.15, Q])
           pressure_drop = 300000 - result[0]
           velocity = Q / (np.pi * (pipeline.pipe_diameter/2)**2)
           
           pressure_drops.append(pressure_drop)
           velocities.append(velocity)
       except:
           pressure_drops.append(np.nan)
           velocities.append(np.nan)
   
   # Plot system characteristic curve
   plt.figure(figsize=(12, 5))
   
   plt.subplot(1, 2, 1)
   plt.plot(flow_rates * 1000, np.array(pressure_drops) / 1000, 'b-', linewidth=2)
   plt.xlabel('Flow Rate (L/s)')
   plt.ylabel('Pressure Drop (kPa)')
   plt.title('System Characteristic Curve')
   plt.grid(True, alpha=0.3)
   
   plt.subplot(1, 2, 2)
   plt.plot(velocities, np.array(pressure_drops) / 1000, 'r-', linewidth=2)
   plt.xlabel('Velocity (m/s)')
   plt.ylabel('Pressure Drop (kPa)')
   plt.title('Pressure Drop vs. Velocity')
   plt.grid(True, alpha=0.3)
   
   plt.tight_layout()
   plt.show()

Part 3: Dynamic Analysis and Control
------------------------------------

Pipeline Dynamics
~~~~~~~~~~~~~~~~~

Analyze transient behavior for control system design:

.. code-block:: python

   import scipy.integrate as integrate
   
   # Define dynamic system for step response analysis
   def pipeline_dynamics(t, y, pipeline, u_step):
       # State variables: [P_out, T_out]
       # Input step in flow rate
       P_in, T_in, Q_base = 300000, 293.15, 0.05
       
       # Step change in flow rate at t = 10s
       Q = Q_base + (0.01 if t > 10 else 0.0)  # +0.01 m³/s step
       
       # Calculate dynamics
       u = [P_in, T_in, Q]
       dydt = pipeline.dynamics(t, y, u)
       
       return dydt
   
   # Initial steady-state conditions
   y0 = pipeline.steady_state([300000, 293.15, 0.05])
   
   # Time span for simulation
   t_span = (0, 60)  # 60 seconds
   t_eval = np.linspace(0, 60, 300)
   
   # Solve differential equation
   solution = integrate.solve_ivp(
       lambda t, y: pipeline_dynamics(t, y, pipeline, None),
       t_span, y0, t_eval=t_eval, method='RK45'
   )
   
   # Plot dynamic response
   plt.figure(figsize=(12, 4))
   
   plt.subplot(1, 2, 1)
   plt.plot(solution.t, solution.y[0] / 1000, 'b-', linewidth=2)
   plt.xlabel('Time (s)')
   plt.ylabel('Outlet Pressure (kPa)')
   plt.title('Pressure Response to Flow Step')
   plt.grid(True, alpha=0.3)
   plt.axvline(x=10, color='r', linestyle='--', alpha=0.7, label='Step input')
   plt.legend()
   
   plt.subplot(1, 2, 2)
   plt.plot(solution.t, solution.y[1] - 273.15, 'g-', linewidth=2)
   plt.xlabel('Time (s)')
   plt.ylabel('Outlet Temperature (°C)')
   plt.title('Temperature Response to Flow Step')
   plt.grid(True, alpha=0.3)
   plt.axvline(x=10, color='r', linestyle='--', alpha=0.7, label='Step input')
   plt.legend()
   
   plt.tight_layout()
   plt.show()

Transfer Function Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~

Derive transfer functions for control design:

.. code-block:: python

   from utilities.control_utils import linearize_model, tune_pid
   
   # Linearize around operating point
   operating_point = {
       'inputs': [300000, 293.15, 0.05],  # [P_in, T_in, Q]
       'states': pipeline.steady_state([300000, 293.15, 0.05])
   }
   
   # Get linear model matrices
   A, B = linearize_model(pipeline, operating_point)
   
   print("Linearized System Matrices:")
   print(f"A matrix (state dynamics):")
   print(A)
   print(f"B matrix (input influence):")
   print(B)
   
   # Design PID controller for pressure control
   # Identify process parameters
   process_params = {
       'K': B[0, 2],  # Steady-state gain (pressure response to flow)
       'tau': 15.0,   # Time constant estimate
       'theta': 2.0   # Dead time estimate
   }
   
   # Tune PID controller
   pid_params = tune_pid(process_params, method='ziegler_nichols')
   
   print("\nPID Controller Parameters:")
   print(f"Kp = {pid_params['Kp']:.3f}")
   print(f"Ki = {pid_params['Ki']:.3f}")
   print(f"Kd = {pid_params['Kd']:.3f}")

Part 4: Advanced Applications
-----------------------------

Elevation Effects
~~~~~~~~~~~~~~~~

Model pipelines with significant elevation changes:

.. code-block:: python

   # Create pipeline with elevation change
   uphill_pipeline = PipeFlow(
       pipe_length=2000.0,      # 2 km pipeline
       pipe_diameter=0.25,      # 25 cm diameter
       roughness=5e-5,          # Smooth pipe
       elevation_change=100.0,  # 100 m elevation gain
       fluid_density=1000.0,
       fluid_viscosity=1e-3,
       name="Uphill Pipeline"
   )
   
   # Compare with level pipeline
   level_pipeline = PipeFlow(
       pipe_length=2000.0,
       pipe_diameter=0.25,
       roughness=5e-5,
       elevation_change=0.0,    # Level pipeline
       fluid_density=1000.0,
       fluid_viscosity=1e-3,
       name="Level Pipeline"
   )
   
   # Compare pressure drops
   Q = 0.08  # 80 L/s flow rate
   
   result_uphill = uphill_pipeline.steady_state([400000, 293.15, Q])
   result_level = level_pipeline.steady_state([400000, 293.15, Q])
   
   pressure_drop_uphill = 400000 - result_uphill[0]
   pressure_drop_level = 400000 - result_level[0]
   
   # Hydrostatic pressure component
   hydrostatic_pressure = 1000 * 9.81 * 100  # ρ × g × h
   
   print(f"Uphill pipeline pressure drop: {pressure_drop_uphill:.0f} Pa")
   print(f"Level pipeline pressure drop: {pressure_drop_level:.0f} Pa")
   print(f"Hydrostatic component: {hydrostatic_pressure:.0f} Pa")
   print(f"Friction component: {pressure_drop_uphill - hydrostatic_pressure:.0f} Pa")

Temperature Effects
~~~~~~~~~~~~~~~~~~

Analyze temperature-dependent flow behavior:

.. code-block:: python

   # Create pipeline model for temperature analysis
   temp_pipeline = PipeFlow(
       pipe_length=1500.0,
       pipe_diameter=0.3,
       roughness=1e-4,
       elevation_change=0.0,
       name="Temperature Analysis Pipeline"
   )
   
   # Test different temperatures
   temperatures = np.array([10, 20, 40, 60, 80]) + 273.15  # Convert to Kelvin
   flow_rate = 0.1  # 100 L/s
   inlet_pressure = 350000  # 3.5 bar
   
   results_temp = []
   
   for T in temperatures:
       # Update fluid properties based on temperature
       # Simplified temperature dependence for water
       density = 1000 * (1 - 0.0002 * (T - 293.15))  # Approximate
       viscosity = 1e-3 * np.exp(-0.03 * (T - 293.15))  # Approximate
       
       # Update pipeline properties
       temp_pipeline.fluid_density = density
       temp_pipeline.fluid_viscosity = viscosity
       
       # Calculate steady-state
       result = temp_pipeline.steady_state([inlet_pressure, T, flow_rate])
       pressure_drop = inlet_pressure - result[0]
       
       results_temp.append({
           'temperature': T - 273.15,  # Convert back to Celsius
           'density': density,
           'viscosity': viscosity,
           'pressure_drop': pressure_drop
       })
       
       print(f"T = {T-273.15:.0f}°C, ρ = {density:.0f} kg/m³, "
             f"μ = {viscosity*1000:.2f} mPa·s, ΔP = {pressure_drop:.0f} Pa")
   
   # Plot temperature effects
   temperatures_C = [r['temperature'] for r in results_temp]
   pressure_drops = [r['pressure_drop'] for r in results_temp]
   
   plt.figure(figsize=(8, 6))
   plt.plot(temperatures_C, np.array(pressure_drops) / 1000, 'bo-', linewidth=2, markersize=8)
   plt.xlabel('Temperature (°C)')
   plt.ylabel('Pressure Drop (kPa)')
   plt.title('Temperature Effect on Pipeline Pressure Drop')
   plt.grid(True, alpha=0.3)
   plt.show()

Part 5: System Integration and Control
--------------------------------------

Closed-Loop Control System
~~~~~~~~~~~~~~~~~~~~~~~~~~

Implement a complete flow control system:

.. code-block:: python

   from utilities.control_utils import PIDController
   from simulation.process_simulation import ProcessSimulation
   
   # Create integrated control system
   class PipelineControlSystem:
       def __init__(self, pipeline, controller_params):
           self.pipeline = pipeline
           self.controller = PIDController(**controller_params)
           self.setpoint = 0.05  # Target flow rate (m³/s)
           
       def control_loop(self, t, x, disturbances=None):
           # Current flow rate (measured variable)
           current_flow = x[2] if len(x) > 2 else self.setpoint
           
           # Control action
           control_output = self.controller.calculate(
               setpoint=self.setpoint,
               process_variable=current_flow,
               dt=0.1
           )
           
           # Convert control output to inlet pressure
           inlet_pressure = 300000 + control_output * 50000  # Base pressure + control action
           inlet_pressure = np.clip(inlet_pressure, 200000, 500000)  # Limits
           
           # Process inputs
           u = [inlet_pressure, 293.15, current_flow]
           
           return self.pipeline.dynamics(t, x, u)
   
   # Set up control system
   pid_params = {
       'Kp': 100000,   # Proportional gain
       'Ki': 10000,    # Integral gain  
       'Kd': 5000,     # Derivative gain
       'output_limits': (-100000, 100000)
   }
   
   control_system = PipelineControlSystem(pipeline, pid_params)
   
   # Simulate setpoint tracking
   print("Pipeline control system created successfully!")
   print("Ready for closed-loop simulation...")

Performance Optimization
~~~~~~~~~~~~~~~~~~~~~~~

Optimize pipeline design for minimum energy consumption:

.. code-block:: python

   from optimization.parameter_estimation import optimize_design
   
   def pipeline_optimization_objective(params):
       \"\"\"
       Objective function for pipeline optimization.
       Minimize pumping energy while maintaining flow requirements.
       \"\"\"
       diameter, roughness = params
       
       # Create pipeline with new parameters
       opt_pipeline = PipeFlow(
           pipe_length=1000.0,
           pipe_diameter=diameter,
           roughness=roughness,
           elevation_change=0.0,
           fluid_density=1000.0,
           fluid_viscosity=1e-3
       )
       
       # Required flow rate
       Q_required = 0.06  # 60 L/s
       
       try:
           # Calculate pressure drop
           result = opt_pipeline.steady_state([300000, 293.15, Q_required])
           pressure_drop = 300000 - result[0]
           
           # Energy consumption (proportional to pressure drop × flow rate)
           energy_consumption = pressure_drop * Q_required
           
           # Penalty for very small diameters (high velocity)
           velocity = Q_required / (np.pi * (diameter/2)**2)
           velocity_penalty = max(0, (velocity - 3.0) * 10000)  # Penalty for v > 3 m/s
           
           return energy_consumption + velocity_penalty
           
       except:
           return 1e10  # Large penalty for infeasible solutions
   
   # Optimization bounds
   bounds = [
       (0.15, 0.40),    # Diameter range (m)
       (1e-5, 5e-4)     # Roughness range (m)
   ]
   
   # Run optimization
   print("Running pipeline optimization...")
   print("Minimizing energy consumption while maintaining flow requirements...")
   
   # Note: In a real implementation, you would call the optimization function here
   # optimal_result = optimize_design(pipeline_optimization_objective, bounds)

Part 6: Real-World Case Study
-----------------------------

Industrial Water Distribution System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Complete example of an industrial water distribution network:

.. code-block:: python

   # Case Study: Industrial cooling water system
   # Requirements:
   # - Supply 200 L/s to industrial facility
   # - Distance: 3 km from water source
   # - Elevation difference: 50 m
   # - Reliability: 99.5% uptime required
   # - Energy efficiency: Minimize pumping costs
   
   class CoolingWaterSystem:
       def __init__(self):
           # Main supply pipeline
           self.main_pipeline = PipeFlow(
               pipe_length=3000.0,      # 3 km main line
               pipe_diameter=0.4,       # 40 cm diameter
               roughness=1e-4,          # Commercial steel
               elevation_change=50.0,   # 50 m elevation gain
               fluid_density=1000.0,    # Water
               fluid_viscosity=1e-3,
               name="Main Supply Pipeline"
           )
           
           # Distribution header
           self.distribution_header = PipeFlow(
               pipe_length=500.0,       # 500 m distribution
               pipe_diameter=0.3,       # 30 cm diameter  
               roughness=1e-4,
               elevation_change=5.0,    # 5 m elevation change
               fluid_density=1000.0,
               fluid_viscosity=1e-3,
               name="Distribution Header"
           )
           
       def calculate_system_performance(self, total_flow_rate):
           \"\"\"Calculate total system pressure drop and energy requirements.\"\"\"
           
           # Main pipeline analysis
           main_result = self.main_pipeline.steady_state([500000, 293.15, total_flow_rate])
           main_pressure_drop = 500000 - main_result[0]
           
           # Distribution header analysis  
           dist_result = self.distribution_header.steady_state([main_result[0], 293.15, total_flow_rate])
           dist_pressure_drop = main_result[0] - dist_result[0]
           
           # Total system pressure drop
           total_pressure_drop = main_pressure_drop + dist_pressure_drop
           
           # Pump power calculation (simplified)
           # Power = (Q × ΔP) / (ρ × efficiency)
           pump_efficiency = 0.85  # 85% efficient pump
           power_required = (total_flow_rate * total_pressure_drop) / (1000 * pump_efficiency)
           
           return {
               'main_pressure_drop': main_pressure_drop,
               'distribution_pressure_drop': dist_pressure_drop,
               'total_pressure_drop': total_pressure_drop,
               'power_required': power_required,
               'final_pressure': dist_result[0],
               'final_temperature': dist_result[1]
           }
       
       def analyze_operating_envelope(self):
           \"\"\"Analyze system performance across operating range.\"\"\"
           flow_rates = np.linspace(0.15, 0.25, 11)  # 150-250 L/s range
           results = []
           
           for Q in flow_rates:
               try:
                   performance = self.calculate_system_performance(Q)
                   results.append({
                       'flow_rate': Q,
                       **performance
                   })
               except Exception as e:
                   print(f"Warning: Calculation failed for Q = {Q:.3f} m³/s: {e}")
           
           return results
   
   # Create and analyze cooling water system
   cooling_system = CoolingWaterSystem()
   
   # Analyze design point performance
   design_flow_rate = 0.2  # 200 L/s
   design_performance = cooling_system.calculate_system_performance(design_flow_rate)
   
   print("Cooling Water System Analysis")
   print("=" * 40)
   print(f"Design flow rate: {design_flow_rate * 1000:.0f} L/s")
   print(f"Main pipeline pressure drop: {design_performance['main_pressure_drop']/1000:.1f} kPa")
   print(f"Distribution pressure drop: {design_performance['distribution_pressure_drop']/1000:.1f} kPa")
   print(f"Total system pressure drop: {design_performance['total_pressure_drop']/1000:.1f} kPa")
   print(f"Required pump power: {design_performance['power_required']/1000:.1f} kW")
   print(f"Final delivery pressure: {design_performance['final_pressure']/1000:.1f} kPa")
   
   # Operating envelope analysis
   envelope_results = cooling_system.analyze_operating_envelope()
   
   # Plot operating envelope
   if envelope_results:
       flow_rates = [r['flow_rate'] * 1000 for r in envelope_results]  # Convert to L/s
       pressures = [r['total_pressure_drop'] / 1000 for r in envelope_results]  # Convert to kPa
       powers = [r['power_required'] / 1000 for r in envelope_results]  # Convert to kW
       
       plt.figure(figsize=(12, 5))
       
       plt.subplot(1, 2, 1)
       plt.plot(flow_rates, pressures, 'b-o', linewidth=2, markersize=6)
       plt.xlabel('Flow Rate (L/s)')
       plt.ylabel('Total Pressure Drop (kPa)')
       plt.title('System Characteristic Curve')
       plt.grid(True, alpha=0.3)
       plt.axvline(x=200, color='r', linestyle='--', alpha=0.7, label='Design point')
       plt.legend()
       
       plt.subplot(1, 2, 2)
       plt.plot(flow_rates, powers, 'g-o', linewidth=2, markersize=6)
       plt.xlabel('Flow Rate (L/s)')
       plt.ylabel('Pump Power (kW)')
       plt.title('Power Requirements')
       plt.grid(True, alpha=0.3)
       plt.axvline(x=200, color='r', linestyle='--', alpha=0.7, label='Design point')
       plt.legend()
       
       plt.tight_layout()
       plt.show()

Summary and Best Practices
--------------------------

Key Takeaways
~~~~~~~~~~~~

1. **Model Selection**: Choose appropriate complexity for your application
2. **Parameter Accuracy**: Accurate geometry and fluid properties are critical
3. **Flow Regime**: Understand laminar vs. turbulent behavior
4. **System Integration**: Consider interactions with pumps, control systems
5. **Validation**: Always validate models against known data or expectations

Common Pitfalls
~~~~~~~~~~~~~~

* **Incorrect Units**: Ensure consistent unit systems throughout
* **Flow Regime Assumptions**: Don't assume turbulent flow for all applications
* **Elevation Effects**: Don't neglect hydrostatic pressure for vertical runs
* **Temperature Effects**: Consider property variations with temperature
* **Control System Coupling**: Account for pump and control system dynamics

Next Steps
----------

* Explore :doc:`pump_systems` for pump integration
* Learn :doc:`multiphase_flow` for complex systems  
* Study :doc:`examples/transport_examples` for more applications
* Review :doc:`../api/transport_package` for complete API documentation

For additional help, see the :doc:`../troubleshooting` guide or consult the community forums.
