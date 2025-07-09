steady_state Function
=====================

Overview
--------

The ``steady_state`` function provides unified steady-state analysis capabilities across all transport models in the continuous liquid module. This function enables comparative analysis and model selection for process control applications.

.. image:: steady_state_example_plots.png
   :width: 800px
   :align: center
   :alt: Steady-State Analysis Comparison

Function Description
--------------------

The ``steady_state`` function implements steady-state calculations for fluid transport systems, providing equilibrium solutions for pressure, temperature, flow rate, and concentration distributions. Each transport model implements its specific steady-state behavior while maintaining a consistent interface.

Key Features
~~~~~~~~~~~~

* **Model-Agnostic Interface**: Consistent input/output format across models
* **Comparative Analysis**: Side-by-side model performance evaluation
* **Parameter Sensitivity**: Analysis of input parameter effects
* **Design Point Calculation**: Operating point determination
* **Performance Mapping**: Model capability assessment

Mathematical Framework
-----------------------

The steady-state analysis solves the equilibrium equations for each transport model:

**General Form**:

.. math::

   \frac{dx}{dt} = f(x, u) = 0

Where:
- :math:`x` = state vector (pressure, temperature, concentration)
- :math:`u` = input vector (boundary conditions, flow rates)
- :math:`f` = model-specific dynamics function

**Model-Specific Implementations**:

**PipeFlow**: Darcy-Weisbach pressure drop with thermal effects
**PeristalticFlow**: Positive displacement flow with backpressure correction
**SlurryPipeline**: Multiphase pressure drop with settling effects

Input/Output Formats
--------------------

Each model has specific input and output formats optimized for its application:

.. code-block:: python

   # PipeFlow
   inputs = [P_inlet, T_inlet, flow_rate]       # [Pa, K, m³/s]
   outputs = [P_outlet, T_outlet]               # [Pa, K]
   
   # PeristalticFlow  
   inputs = [P_inlet, pump_speed, occlusion]    # [Pa, RPM, -]
   outputs = [flow_rate, P_outlet]              # [m³/s, Pa]
   
   # SlurryPipeline
   inputs = [P_inlet, flow_rate, c_solid]       # [Pa, m³/s, -]
   outputs = [P_outlet, c_solid_out]            # [Pa, -]

Usage Examples
--------------

Cross-Model Comparison
~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: steady_state_example.py
   :language: python
   :lines: 1-100

The comprehensive example demonstrates:

* **PipeFlow Analysis**: Pressure drop calculations for clean fluids
* **PeristalticFlow Mapping**: Speed-flow relationships for precision dosing
* **SlurryPipeline Assessment**: Multiphase flow with particle effects
* **Comparative Performance**: Model selection guidelines

Example Output
~~~~~~~~~~~~~~

.. literalinclude:: steady_state_example.out
   :language: text

Key output sections include:

* PipeFlow pressure drop and Reynolds number analysis
* PeristalticFlow speed calibration and backpressure effects
* SlurryPipeline concentration changes and settling effects
* Model comparison table with input/output formats

Model Selection Guidelines
--------------------------

**Use PipeFlow for**:

* Single-phase liquid transport
* Long-distance pipeline systems
* High-pressure applications
* Temperature-sensitive processes

**Use PeristalticFlow for**:

* Precise fluid dosing
* Chemical compatibility requirements
* Low-flow rate applications
* Analytical instrumentation

**Use SlurryPipeline for**:

* Solid-liquid transport
* Mining and dredging applications
* Particle suspension systems
* Concentration-critical processes

Performance Comparison
----------------------

.. list-table:: Model Performance Characteristics
   :header-rows: 1
   :widths: 25 25 25 25

   * - Characteristic
     - PipeFlow
     - PeristalticFlow
     - SlurryPipeline
   * - Accuracy
     - ±2-5%
     - ±1-3%
     - ±5-10%
   * - Pressure Range
     - 0-100 bar
     - 0-10 bar
     - 0-50 bar
   * - Flow Range
     - 0.001-10 m³/s
     - 0.1-1000 mL/min
     - 0.01-5 m³/s
   * - Application
     - General purpose
     - Precision dosing
     - Multiphase transport

Visualization
-------------

The steady-state analysis generates comprehensive visualization including:

1. **Pressure Drop Comparison**: Clean vs slurry flow pressure losses
2. **Reynolds Number Analysis**: Flow regime identification
3. **Flow Rate Relationships**: Model-specific performance curves
4. **Model Characteristics**: Complexity vs application scope comparison

.. image:: steady_state_example_plots.png
   :width: 100%
   :align: center
   :alt: Comprehensive Steady-State Analysis

Applications
------------

The ``steady_state`` function is used for:

* **Process Design**: Equipment sizing and selection
* **System Optimization**: Operating point determination
* **Model Validation**: Experimental data comparison
* **Sensitivity Analysis**: Parameter effect assessment
* **Performance Mapping**: Operating envelope definition

Computational Aspects
----------------------

**Solution Methods**:

* **Direct Calculation**: Explicit algebraic solutions where possible
* **Iterative Methods**: Newton-Raphson for implicit equations
* **Convergence Criteria**: Relative tolerance of 1e-6
* **Robustness**: Bounds checking and physical constraints

**Performance Metrics**:

* **Computation Time**: < 1 ms per evaluation (typical)
* **Memory Usage**: Minimal state storage requirements
* **Numerical Stability**: Validated across operating ranges
* **Error Handling**: Graceful degradation for edge cases

Technical Implementation
------------------------

The steady-state function implements:

.. code-block:: python

   def steady_state(model, inputs):
       """
       Calculate steady-state solution for transport model
       
       Parameters:
       -----------
       model : TransportModel
           Transport model instance (PipeFlow, PeristalticFlow, SlurryPipeline)
       inputs : array_like
           Model-specific input vector
           
       Returns:
       --------
       outputs : array_like
           Model-specific output vector
       """
       
       # Validate inputs
       inputs = validate_inputs(model, inputs)
       
       # Calculate steady-state solution
       outputs = model.steady_state(inputs)
       
       # Validate outputs
       outputs = validate_outputs(model, outputs)
       
       return outputs

Best Practices
--------------

**Input Validation**:

* Check physical bounds (positive pressures, flows)
* Verify units and dimensional consistency
* Handle edge cases (zero flow, extreme conditions)

**Output Analysis**:

* Compare results across models when applicable
* Validate against known analytical solutions
* Check conservation principles (mass, energy)

**Error Handling**:

* Provide meaningful error messages
* Implement fallback calculations
* Log convergence issues for debugging

Technical References
--------------------

1. Bird, R.B., Stewart, W.E. & Lightfoot, E.N. (2007). *Transport Phenomena*, 2nd Edition. John Wiley & Sons.
2. Welty, J.R. et al. (2007). *Fundamentals of Momentum, Heat, and Mass Transfer*, 5th Edition. John Wiley & Sons.
3. McCabe, W.L., Smith, J.C. & Harriott, P. (2004). *Unit Operations of Chemical Engineering*, 7th Edition. McGraw-Hill.
4. Perry, R.H. & Green, D.W. (2007). *Perry's Chemical Engineers' Handbook*, 8th Edition. McGraw-Hill.

See Also
--------

* :doc:`PipeFlow` - Pipeline transport modeling
* :doc:`PeristalticFlow` - Peristaltic pump modeling
* :doc:`SlurryPipeline` - Multiphase slurry transport
* :doc:`dynamics` - Dynamic modeling functions
