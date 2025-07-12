Fixed Bed Reactor
=================

Overview
--------

The Fixed Bed Reactor model simulates packed bed catalytic reactors with solid catalyst particles. It accounts for bed porosity, catalyst loading, axial profiles, and pressure drop effects. It is widely used in petrochemical industry for hydrogenation, oxidation, steam reforming, and environmental catalysis applications.

Theory and Equations
-------------------

Material Balance (per segment)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \frac{dC_A}{dt} = -u \frac{dC_A}{dz} - \frac{k(T) C_A W_{cat}}{V_{void}}

Energy Balance (per segment)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \frac{dT}{dt} = -u \frac{dT}{dz} + \frac{(-\Delta H_r) k(T) C_A W_{cat}}{\rho c_p V_{void}} + \frac{UA(T_w - T)}{\rho c_p V_{void}}

Bed Properties
~~~~~~~~~~~~~~

- Void volume per segment: :math:`V_{void} = \epsilon A_{cross} \Delta z`
- Catalyst mass per segment: :math:`W_{cat} = \rho_{cat} (1-\epsilon) A_{cross} \Delta z`
- Heat transfer area per segment: :math:`A_{heat} = \pi D \Delta z`

Key Features
-----------

- Heterogeneous catalysis modeling
- Bed porosity and catalyst density effects
- Axial temperature and concentration profiles
- Heat transfer to reactor walls
- Pressure drop calculations

Parameters
----------

- **L**: Bed length [m] (0.1-20 m)
- **D**: Bed diameter [m]
- **epsilon**: Bed porosity [-] (0.2-0.8)
- **rho_cat**: Catalyst density [kg/m³] (500-2000)
- **dp**: Particle diameter [m] (0.001-0.01)

Usage Example
-------------

.. code-block:: python

   from unit.reactor.FixedBedReactor import FixedBedReactor
   
   # Create Fixed Bed Reactor instance
   reactor = FixedBedReactor(
       L=5.0,               # Bed length [m]
       D=1.0,               # Bed diameter [m]
       epsilon=0.4,         # Bed porosity [-]
       rho_cat=1500.0,      # Catalyst density [kg/m³]
       n_segments=20        # Number of segments
   )

Example Output
--------------

.. code-block:: text

   ============================================================
   FixedBedReactor Example
   ============================================================
   Reactor: Example_FixedBed
   Bed length: 5.0 m
   Bed diameter: 1.0 m
   Bed porosity: 0.4
   Catalyst density: 1500.0 kg/m³
   Particle diameter: 5.0 mm
   Total bed volume: 3.927 m³
   Void volume: 1.571 m³

   Operating Conditions:
     u: 0.1 m/s
     CAi: 1000.0 mol/m³
     Ti: 450.0 K
     Tw: 430.0 K

   Steady-State Analysis:
   ------------------------------
   Overall conversion: 0.0%
   Residence time: 0.33 min
   Space velocity: 72.0 h⁻¹

Applications
-----------

- Catalytic processes in petrochemical industry
- Hydrogenation and oxidation reactions
- Environmental catalysis
- Steam reforming
- Ammonia synthesis

Visualization
-------------

Example Plots
~~~~~~~~~~~~~

.. figure:: fixed_bed_reactor_example_plots.png
   :width: 800px
   :align: center
   :alt: Fixed Bed Reactor Example Plots

   Comprehensive analysis showing concentration, temperature, conversion, and reaction rate profiles along the fixed bed reactor.

.. figure:: fixed_bed_reactor_detailed_analysis.png
   :width: 600px
   :align: center
   :alt: Fixed Bed Reactor Detailed Analysis

   Detailed axial profiles showing concentration and temperature distributions with key performance metrics.

See Also
--------

- :doc:`plug_flow_reactor` - Plug flow reactor
- :doc:`fluidized_bed_reactor` - Fluidized bed reactor
