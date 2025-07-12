Fluidized Bed Reactor
=====================

Overview
--------

The Fluidized Bed Reactor model simulates two-phase fluidized systems with bubble and emulsion phases. It is used for catalytic cracking, combustion, and polymerization processes where excellent heat and mass transfer characteristics are required.

Theory and Equations
-------------------

Two-Phase Model
~~~~~~~~~~~~~~~

**Bubble Phase:**

.. math::

   \frac{dC_b}{dt} = K_{bc}(C_e - C_b) - u_b \frac{dC_b}{dz}

**Emulsion Phase:**

.. math::

   \frac{dC_e}{dt} = K_{bc} \frac{\delta_b}{1-\delta_b}(C_b - C_e) - k C_e \frac{\rho_{cat}(1-\epsilon_{mf})}{1-\delta_b}

Fluidization Properties
~~~~~~~~~~~~~~~~~~~~~~

- **Minimum fluidization velocity**: :math:`U_{mf}`
- **Bubble velocity**: :math:`u_b = u_g - U_{mf} + u_{br}`
- **Bubble fraction**: :math:`\delta_b = f(u_g, U_{mf}, geometry)`

Key Features
-----------

- Two-phase (bubble and emulsion) modeling
- Fluidization regime characterization
- Heat and mass transfer between phases
- Catalyst circulation effects
- Gas-solid contact modeling

Usage Example
-------------

.. code-block:: python

   from unit.reactor.FluidizedBedReactor import FluidizedBedReactor
   
   # Create Fluidized Bed Reactor instance
   reactor = FluidizedBedReactor(
       H=3.0,               # Bed height [m]
       D=2.0,               # Bed diameter [m]
       U_mf=0.1,           # Minimum fluidization velocity [m/s]
       rho_cat=1500.0      # Catalyst density [kg/m³]
   )

Example Output
--------------

.. code-block:: text

   Fluidized Bed Reactor Example
   ==================================================
   Reactor: Fluidized Bed Reactor
   Bed Height: 3.0 m
   Bed Diameter: 2.0 m
   Minimum Fluidization Velocity: 0.1 m/s
   Catalyst Density: 1500.0 kg/m³
   Particle Diameter: 0.50 mm
   Activation Energy: 60.0 kJ/mol

   Operating Conditions:
   Inlet concentration: 100.0 mol/m³
   Inlet temperature: 700.0 K (426.9 °C)
   Superficial gas velocity: 0.3 m/s
   Coolant temperature: 650.0 K (376.9 °C)

   Reactor is fluidized (U_g > U_mf)
   Excess velocity: 0.200 m/s

   Fluidization Properties:
   Bubble velocity: 0.250 m/s
   Bubble fraction: 0.801
   Emulsion fraction: 0.199

Performance Plots
----------------

**Dynamic Response (fluidized_bed_reactor_example_plots.png)**

.. image:: fluidized_bed_reactor_example_plots.png
   :width: 600px
   :align: center
   :alt: Fluidized bed reactor bubble and emulsion phase dynamics

Applications
-----------

- Fluid catalytic cracking (FCC)
- Coal combustion and gasification
- Polymerization processes
- Roasting and calcination
- Waste treatment

See Also
--------

- :doc:`fixed_bed_reactor` - Fixed bed reactor
- :doc:`cstr` - Continuous stirred tank reactor
