PipeFlow Class
==============

Overview
--------

The ``PipeFlow`` class implements a comprehensive pipe flow transport model for steady-state and dynamic analysis of fluid flow through pipelines. This model is essential for process control applications involving fluid transport systems.

.. image:: PipeFlow_example_plots.png
   :width: 800px
   :align: center
   :alt: PipeFlow Analysis Plots

Class Description
-----------------

The ``PipeFlow`` class provides accurate modeling of pressure drop, temperature effects, and flow characteristics in pipeline systems. It implements the Darcy-Weisbach equation for friction factor calculations and includes thermal dynamics for temperature-dependent applications.

Key Features
~~~~~~~~~~~~

* **Pressure Drop Calculations**: Accurate pressure drop prediction using Darcy-Weisbach equation
* **Reynolds Number Analysis**: Automatic flow regime identification (laminar/turbulent)
* **Thermal Effects**: Temperature-dependent fluid properties and heat transfer
* **Elevation Changes**: Hydrostatic pressure effects for non-horizontal pipelines
* **Friction Factor Models**: Multiple correlations for different pipe roughness conditions

Mathematical Model
------------------

The pipe flow model is based on fundamental fluid mechanics principles:

**Pressure Drop Equation**:

.. math::

   \Delta P = f \cdot \frac{L}{D} \cdot \frac{\rho v^2}{2} + \rho g \Delta h

Where:
- :math:`\Delta P` = pressure drop (Pa)
- :math:`f` = Darcy friction factor (-)
- :math:`L` = pipe length (m)
- :math:`D` = pipe diameter (m)
- :math:`\rho` = fluid density (kg/m³)
- :math:`v` = flow velocity (m/s)
- :math:`g` = gravitational acceleration (9.81 m/s²)
- :math:`\Delta h` = elevation change (m)

**Reynolds Number**:

.. math::

   Re = \frac{\rho v D}{\mu}

Where :math:`\mu` is the dynamic viscosity (Pa·s).

Constructor Parameters
----------------------

.. code-block:: python

   PipeFlow(
       pipe_length=1000.0,      # Pipeline length [m]
       pipe_diameter=0.2,       # Pipeline diameter [m]
       roughness=1e-4,          # Surface roughness [m]
       elevation_change=0.0,    # Elevation change [m]
       fluid_density=1000.0,    # Fluid density [kg/m³]
       fluid_viscosity=1e-3,    # Fluid viscosity [Pa·s]
       name="PipeFlow"
   )

Methods
-------

steady_state(u)
~~~~~~~~~~~~~~~

Calculate steady-state pressure and temperature for given flow conditions.

**Input**: ``u = [P_inlet, T_inlet, flow_rate]``

**Output**: ``[P_outlet, T_outlet]``

dynamics(t, x, u)
~~~~~~~~~~~~~~~~~

Calculate dynamic derivatives for time-domain analysis.

**Input**: 
- ``t``: time (s)
- ``x``: state vector [P_outlet, T_outlet]
- ``u``: input vector [P_inlet, T_inlet, flow_rate]

**Output**: ``[dP_outlet/dt, dT_outlet/dt]``

describe()
~~~~~~~~~~

Returns comprehensive metadata about the model including algorithms, parameters, and equations.

Usage Examples
--------------

Basic Pipeline Analysis
~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: PipeFlow_example.py
   :language: python
   :lines: 1-50

The complete example demonstrates:

* Industrial pipeline design and analysis
* Pressure drop calculations across different flow rates
* Reynolds number analysis and flow regime identification
* Temperature effects in thermal transport systems
* Pipeline network optimization

Example Output
~~~~~~~~~~~~~~

.. literalinclude:: PipeFlow_example.out
   :language: text
   :lines: 1-50

Applications
------------

The ``PipeFlow`` class is widely used in:

* **Chemical Processing**: Pipeline design for chemical plants
* **Oil & Gas**: Crude oil and natural gas pipeline systems
* **Water Distribution**: Municipal water supply networks
* **HVAC Systems**: Heating and cooling fluid distribution
* **Industrial Processes**: Process fluid transport and distribution

Performance Characteristics
---------------------------

* **Accuracy**: ±2-5% for turbulent flow conditions
* **Reynolds Range**: 1 to 10⁸ (laminar to fully turbulent)
* **Pressure Range**: Up to 100 bar operating pressure
* **Temperature Range**: 0°C to 200°C fluid temperatures
* **Pipe Diameter**: 10 mm to 2 m diameter range

Visualization
-------------

The example generates comprehensive visualization plots showing:

1. **Flow Rate vs Pressure Drop**: Relationship between volumetric flow and pressure loss
2. **Reynolds Number Analysis**: Flow regime identification and transition points
3. **Temperature Response**: Thermal dynamics and heat transfer effects
4. **Pipeline Profile**: Pressure distribution along pipeline length
5. **Design Charts**: Engineering design and selection guidelines

.. image:: PipeFlow_example_plots.png
   :width: 100%
   :align: center
   :alt: Comprehensive PipeFlow Analysis

Technical References
--------------------

1. Moody, L.F. (1944). "Friction factors for pipe flow." *Transactions of the ASME*, 66(8), 671-684.
2. Colebrook, C.F. (1939). "Turbulent flow in pipes." *Journal of the Institution of Civil Engineers*, 11(4), 133-156.
3. White, F.M. (2011). *Fluid Mechanics*, 7th Edition. McGraw-Hill Education.
4. Crane Co. (2013). *Flow of Fluids Through Valves, Fittings, and Pipe*. Technical Paper No. 410.

See Also
--------

* :doc:`PeristalticFlow` - Positive displacement pump modeling
* :doc:`SlurryPipeline` - Multiphase slurry transport
* :doc:`steady_state` - Steady-state analysis functions
* :doc:`dynamics` - Dynamic modeling functions
