SlurryPipeline Class
====================

Overview
--------

The ``SlurryPipeline`` class implements a comprehensive multiphase transport model for solid-liquid slurry systems. This model is essential for mining, dredging, and industrial applications involving the transport of particulate matter in liquid carriers.

.. image:: SlurryPipeline_example_plots.png
   :width: 800px
   :align: center
   :alt: SlurryPipeline Analysis Plots

Class Description
-----------------

The ``SlurryPipeline`` class provides accurate modeling of slurry transport phenomena, including critical velocity calculations, particle settling effects, pressure drop predictions, and concentration variations. The model accounts for multiphase flow dynamics and particle-fluid interactions.

Key Features
~~~~~~~~~~~~

* **Critical Velocity Prediction**: Durand equation implementation for minimum transport velocity
* **Particle Settling Analysis**: Concentration changes due to gravitational settling
* **Multiphase Pressure Drop**: Enhanced friction factors for solid-liquid mixtures
* **Concentration Tracking**: Inlet and outlet solid concentration modeling
* **Operating Envelope**: Safe transport velocity determination

Mathematical Model
------------------

The slurry pipeline model incorporates multiphase flow mechanics:

**Critical Velocity (Durand Equation)**:

.. math::

   V_{critical} = 1.5 \sqrt{2g d_p \left(\frac{\rho_s}{\rho_f} - 1\right)}

Where:
- :math:`V_{critical}` = critical transport velocity (m/s)
- :math:`g` = gravitational acceleration (9.81 m/s²)
- :math:`d_p` = particle diameter (m)
- :math:`\rho_s` = solid density (kg/m³)
- :math:`\rho_f` = fluid density (kg/m³)

**Mixture Density**:

.. math::

   \rho_m = \rho_f (1 - C_v) + \rho_s C_v

Where :math:`C_v` is the volumetric concentration of solids.

**Effective Viscosity (Einstein Relation)**:

.. math::

   \mu_{eff} = \mu_f (1 + 2.5 C_v + 10.05 C_v^2)

**Enhanced Pressure Drop**:

.. math::

   \Delta P = f \cdot \frac{L}{D} \cdot \frac{\rho_m v^2}{2} \cdot (1 + 3 C_v)

Constructor Parameters
----------------------

.. code-block:: python

   SlurryPipeline(
       pipe_length=500.0,           # Pipeline length [m]
       pipe_diameter=0.2,           # Pipeline diameter [m]
       solid_concentration=0.3,     # Volume fraction of solids [-]
       particle_diameter=1e-3,      # Average particle diameter [m]
       fluid_density=1000.0,        # Carrier fluid density [kg/m³]
       solid_density=2500.0,        # Solid particle density [kg/m³]
       fluid_viscosity=1e-3,        # Carrier fluid viscosity [Pa·s]
       flow_nominal=0.05,           # Nominal volumetric flow [m³/s]
       name="SlurryPipeline"
   )

Methods
-------

steady_state(u)
~~~~~~~~~~~~~~~

Calculate steady-state pressure drop and solid concentration for given flow.

**Input**: ``u = [P_inlet, flow_rate, inlet_solid_concentration]``

**Output**: ``[P_outlet, outlet_solid_concentration]``

dynamics(t, x, u)
~~~~~~~~~~~~~~~~~

Calculate dynamic derivatives for pressure and concentration transport.

**Input**: 
- ``t``: time (s)
- ``x``: state vector [P_outlet, outlet_solid_concentration]
- ``u``: input vector [P_inlet, flow_rate, inlet_solid_concentration]

**Output**: ``[dP_outlet/dt, dconcentration/dt]``

describe()
~~~~~~~~~~

Returns comprehensive metadata about the slurry transport model including particle mechanics and flow regimes.

Usage Examples
--------------

Mining Ore Transport System
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: SlurryPipeline_simple_example.py
   :language: python
   :lines: 1-100

The comprehensive example demonstrates:

* **Mining Ore Transport**: Long-distance pipeline for mineral transport
* **Critical Velocity Analysis**: Ensuring adequate particle suspension
* **Flow Rate Performance**: Velocity and pressure drop relationships
* **Particle Size Effects**: Impact of particle diameter on transport
* **Operating Envelope**: Safe vs risk zone identification

Example Output
~~~~~~~~~~~~~~

.. literalinclude:: SlurryPipeline_example.out
   :language: text
   :lines: 1-80

Key output sections include:

* Pipeline configuration and mixture properties
* Critical velocity analysis with safety factors
* Flow rate performance mapping
* Particle size effect characterization
* Operating envelope determination

Applications
------------

The ``SlurryPipeline`` class is widely used in:

* **Mining Industry**: Ore concentrate and tailings transport
* **Dredging Operations**: Sediment and sand transport systems
* **Wastewater Treatment**: Sludge transport and dewatering
* **Coal Preparation**: Coal slurry pipeline systems
* **Industrial Processes**: Catalyst and solid waste transport

Performance Characteristics
---------------------------

* **Concentration Range**: 5% to 60% solids by volume
* **Particle Size Range**: 10 μm to 10 mm diameter
* **Velocity Range**: 0.5 to 8 m/s transport velocities
* **Pressure Rating**: Up to 50 bar operating pressure
* **Pipeline Length**: Up to 100 km transport distance

Visualization
-------------

The example generates comprehensive visualization including:

1. **Flow Rate vs Velocity**: Operating line and critical velocity relationship
2. **Pressure Drop Analysis**: Flow rate dependent pressure losses
3. **Settling Effect**: Concentration changes with flow velocity
4. **Particle Size Impact**: Critical velocity variations
5. **Operating Map**: Safe operation envelope definition

.. image:: SlurryPipeline_example_plots.png
   :width: 100%
   :align: center
   :alt: Comprehensive SlurryPipeline Analysis

Transport Phenomena
-------------------

**Particle Suspension Mechanisms**:

* **Turbulent Diffusion**: Particles suspended by turbulent eddies
* **Saltation**: Intermittent particle jumping along pipeline bottom
* **Heterogeneous Flow**: Non-uniform concentration distribution
* **Homogeneous Flow**: Well-mixed solid-liquid suspension

**Critical Design Considerations**:

* Minimum transport velocity to prevent settling
* Pipeline slope and elevation changes
* Pump selection and system hydraulics
* Erosion and wear protection measures

Engineering Guidelines
----------------------

**Design Velocity**:

.. math::

   V_{design} = (1.2 \text{ to } 2.0) \times V_{critical}

**Recommended Operating Conditions**:

* Maintain velocity > 120% of critical velocity
* Monitor concentration variations continuously
* Design for worst-case particle size distribution
* Include settling velocity safety margins

Technical References
--------------------

1. Durand, R. & Condolios, E. (1952). "The hydraulic transport of coal and solid materials in pipes." *Proceedings of Colloquium on Hydraulic Transport*, National Coal Board, London.
2. Wilson, K.C. et al. (2006). *Slurry Transport Using Centrifugal Pumps*, 3rd Edition. Springer Science & Business Media.
3. Wasp, E.J., Kenny, J.P. & Gandhi, R.L. (1977). *Solid-Liquid Flow: Slurry Pipeline Transportation*. Trans Tech Publications.
4. Matousek, V. (2009). "Research developments in pipeline transport of settling slurries." *Powder Technology*, 196(3), 280-291.

See Also
--------

* :doc:`PipeFlow` - Single-phase pipeline transport
* :doc:`PeristalticFlow` - Positive displacement pumping
* :doc:`steady_state` - Steady-state analysis functions
* :doc:`dynamics` - Dynamic modeling functions
