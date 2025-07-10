dynamics Function
=================

Overview
--------

The ``dynamics`` function provides unified time-domain analysis capabilities across all transport models in the continuous liquid module. This function enables transient response analysis, control system design, and dynamic behavior characterization.

.. image:: dynamics_example_plots.png
   :width: 800px
   :align: center
   :alt: Dynamic Analysis Comparison

Function Description
--------------------

The ``dynamics`` function implements time-domain differential equations for fluid transport systems, providing time derivatives for state variables including pressure, temperature, flow rate, and concentration. Each transport model implements its specific dynamic behavior while maintaining consistent interface standards.

Key Features
~~~~~~~~~~~~

* **Time-Domain Analysis**: Transient response characterization
* **Control System Design**: Dynamic model for controller development
* **Step Response Analysis**: System response to input changes
* **Time Constant Estimation**: System response speed characterization
* **Stability Assessment**: Dynamic stability and settling behavior

Mathematical Framework
-----------------------

The dynamics analysis solves the time-dependent differential equations:

**General Form**:

.. math::

   \frac{dx}{dt} = f(t, x, u)

Where:
- :math:`t` = time (s)
- :math:`x` = state vector (system variables)
- :math:`u` = input vector (control variables)
- :math:`f` = model-specific dynamics function

**Model-Specific State Variables**:

**PipeFlow**: :math:`x = [P_{outlet}, T_{outlet}]`
**PeristalticFlow**: :math:`x = [flow\_rate, pulsation\_amplitude]`
**SlurryPipeline**: :math:`x = [P_{outlet}, concentration_{outlet}]`

Dynamic Response Characteristics
--------------------------------

Each model exhibits distinct dynamic behavior:

**First-Order Response**:

.. math::

   \tau \frac{dx}{dt} + x = K \cdot u

Where:
- :math:`\tau` = time constant (s)
- :math:`K` = steady-state gain
- :math:`u` = input step

**Time Constant Relationships**:

* **PipeFlow**: Hydraulic and thermal time constants (typically 1-10 s)
* **PeristalticFlow**: Pulsation damping and flow response (typically 0.5-5 s)
* **SlurryPipeline**: Transport delay and concentration mixing (typically 10-500 s)

State Variable Definitions
--------------------------

.. code-block:: python

   # PipeFlow State Variables
   x = [P_outlet,           # Outlet pressure [Pa]
        T_outlet]           # Outlet temperature [K]
   
   # PeristalticFlow State Variables  
   x = [flow_rate,          # Volumetric flow rate [m³/s]
        pulsation_amplitude] # Pulsation amplitude [-]
   
   # SlurryPipeline State Variables
   x = [P_outlet,           # Outlet pressure [Pa]
        c_solid_outlet]     # Outlet solid concentration [-]

Usage Examples
--------------

Time-Domain Analysis
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: dynamics_example.py
   :language: python
   :lines: 1-150

The comprehensive example demonstrates:

* **PipeFlow Step Response**: Pressure and temperature dynamics
* **PeristalticFlow Speed Changes**: Flow rate and pulsation response
* **SlurryPipeline Concentration Steps**: Transport delay effects
* **Response Time Comparison**: Time constant estimation across models

Example Output
~~~~~~~~~~~~~~

.. literalinclude:: dynamics_example.out
   :language: text

Key output sections include:

* PipeFlow pressure and temperature step responses
* PeristalticFlow speed change dynamics and pulsation effects
* SlurryPipeline concentration transport with mixing delays
* Comparative time constant analysis across all models

Dynamic Model Characteristics
-----------------------------

**Response Speed Ranking**:

1. **PeristalticFlow**: Fastest response (τ ≈ 0.5-5 s)
2. **PipeFlow**: Medium response (τ ≈ 1-10 s)  
3. **SlurryPipeline**: Slowest response (τ ≈ 10-500 s)

**Physical Mechanisms**:

* **Hydraulic Response**: Pressure wave propagation
* **Thermal Response**: Heat transfer and thermal capacity effects
* **Mechanical Response**: Pump dynamics and pulsation damping
* **Transport Response**: Advection and diffusion processes

Integration Methods
-------------------

The dynamics function supports various integration schemes:

**Explicit Methods**:

.. code-block:: python

   # Euler Integration
   x_new = x_old + dt * dynamics(t, x_old, u)
   
   # Runge-Kutta 4th Order
   k1 = dt * dynamics(t, x, u)
   k2 = dt * dynamics(t + dt/2, x + k1/2, u)
   k3 = dt * dynamics(t + dt/2, x + k2/2, u)
   k4 = dt * dynamics(t + dt, x + k3, u)
   x_new = x + (k1 + 2*k2 + 2*k3 + k4)/6

**Stability Requirements**:

* Time step selection based on fastest time constant
* Courant-Friedrichs-Lewy (CFL) condition for transport
* Adaptive step size for stiff systems

Visualization
-------------

The dynamic analysis generates comprehensive visualization including:

1. **Step Response Plots**: Time-domain response to input changes
2. **Phase Portraits**: State variable relationships
3. **Time Constant Comparison**: Response speed characterization
4. **Settling Time Analysis**: System stabilization assessment

.. image:: dynamics_example_plots.png
   :width: 100%
   :align: center
   :alt: Comprehensive Dynamic Analysis

Control System Applications
---------------------------

**Controller Design**:

* **PID Tuning**: Time constant and gain information
* **Model Predictive Control**: Dynamic model for prediction
* **Feedforward Control**: Disturbance compensation
* **Adaptive Control**: Parameter estimation and adjustment

**Stability Analysis**:

* **Root Locus**: Pole-zero analysis
* **Bode Plots**: Frequency response characterization
* **Nyquist Criteria**: Stability margins assessment
* **Robustness**: Parameter sensitivity analysis

Dynamic Performance Metrics
----------------------------

.. list-table:: Dynamic Response Characteristics
   :header-rows: 1
   :widths: 25 25 25 25

   * - Metric
     - PipeFlow
     - PeristalticFlow
     - SlurryPipeline
   * - Time Constant
     - 1-10 s
     - 0.5-5 s
     - 10-500 s
   * - Settling Time
     - 4-40 s
     - 2-20 s
     - 40-2000 s
   * - Overshoot
     - < 5%
     - < 10%
     - None
   * - Damping
     - High
     - Variable
     - Overdamped

Applications
------------

The ``dynamics`` function is used for:

* **Process Control**: Controller design and tuning
* **System Analysis**: Transient behavior characterization
* **Simulation**: Time-domain system simulation
* **Optimization**: Dynamic performance optimization
* **Safety Analysis**: Response to emergency conditions

Computational Implementation
----------------------------

**Numerical Methods**:

.. code-block:: python

   def dynamics(model, t, x, u):
       """
       Calculate time derivatives for transport model
       
       Parameters:
       -----------
       model : TransportModel
           Transport model instance
       t : float
           Current time [s]
       x : array_like
           State vector
       u : array_like
           Input vector
           
       Returns:
       --------
       dx_dt : array_like
           Time derivatives of state variables
       """
       
       # Validate state and inputs
       x = validate_state(model, x)
       u = validate_inputs(model, u)
       
       # Calculate derivatives
       dx_dt = model.dynamics(t, x, u)
       
       # Apply physical constraints
       dx_dt = apply_constraints(model, x, dx_dt)
       
       return dx_dt

**Performance Optimization**:

* **Vectorized Operations**: Efficient array computations
* **Memory Management**: Minimal allocation during integration
* **Parallel Processing**: Multiple simulation scenarios
* **Adaptive Stepping**: Variable time step for efficiency

Best Practices
--------------

**Time Step Selection**:

.. math::

   \Delta t \leq \frac{\tau_{min}}{10}

Where :math:`\tau_{min}` is the smallest time constant in the system.

**Initial Conditions**:

* Use steady-state values for baseline
* Check physical consistency
* Consider measurement uncertainties

**Integration Monitoring**:

* Monitor conservation laws
* Check for numerical instabilities
* Validate against analytical solutions

Technical References
--------------------

1. Stephanopoulos, G. (1984). *Chemical Process Control: An Introduction to Theory and Practice*. Prentice Hall.
2. Seborg, D.E., Edgar, T.F. & Mellichamp, D.A. (2010). *Process Dynamics and Control*, 3rd Edition. John Wiley & Sons.
3. Bequette, B.W. (2003). *Process Control: Modeling, Design, and Simulation*. Prentice Hall.
4. Ogunnaike, B.A. & Ray, W.H. (1994). *Process Dynamics, Modeling, and Control*. Oxford University Press.

See Also
--------

* :doc:`PipeFlow` - Pipeline transport modeling
* :doc:`PeristalticFlow` - Peristaltic pump modeling
* :doc:`SlurryPipeline` - Multiphase slurry transport
* :doc:`steady_state` - Steady-state analysis functions
