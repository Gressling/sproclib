PneumaticConveying
==================

Overview
--------

The PneumaticConveying class models solid transport using gas (typically air) as the conveying medium. Pneumatic conveying systems use pressure differentials and gas flow to transport bulk solids through pipelines, offering flexible routing and enclosed transport.

.. figure:: PneumaticConveying_example_plots.png
   :width: 800px
   :align: center
   :alt: PneumaticConveying Example Analysis
   
   PneumaticConveying system behavior showing pressure drop response, flow rate dynamics, air and particle velocities, and operating envelope.

Algorithm and Theory
--------------------

Pneumatic conveying systems operate in two main modes: dilute phase (high velocity, low pressure) and dense phase (low velocity, high pressure). The system behavior is governed by gas-solid flow dynamics.

**Key Equations:**

- **Minimum Transport Velocity**: :math:`v_{min} = F_r \sqrt{gd_p(\rho_p - \rho_g)/\rho_g}`
- **Pressure Drop**: :math:`\Delta P = \Delta P_{gas} + \Delta P_{solid} + \Delta P_{acceleration}`
- **Solid Loading Ratio**: :math:`\mu = Q_m / Q_{gas}`
- **Saltation Velocity**: :math:`v_{salt} = 4.0 \sqrt{gd_p(\rho_p - \rho_g)/\rho_g}`

Where:
- :math:`F_r` = Froude number factor (typically 3-5)
- :math:`g` = Gravitational acceleration (9.81 m/s²)
- :math:`d_p` = Particle diameter (m)
- :math:`\rho_p` = Particle density (kg/m³)
- :math:`\rho_g` = Gas density (kg/m³)
- :math:`Q_m` = Mass flow rate of solids (kg/s)
- :math:`Q_{gas}` = Mass flow rate of gas (kg/s)

Use Cases
---------

- **Chemical Processing**: Catalyst, polymer pellet, and powder transport
- **Food Industry**: Flour, sugar, and grain pneumatic conveying
- **Pharmaceutical**: Active ingredient and excipient handling
- **Power Generation**: Coal and biomass fuel transport
- **Cement Industry**: Cement powder and raw material transport
- **Plastics Industry**: Resin pellet and additive conveying

Parameters
----------

Essential Parameters:
~~~~~~~~~~~~~~~~~~~~~

- **pipe_diameter** (float): Conveying pipe diameter in meters [0.05-0.5 m]
- **pipe_length** (float): Total pipeline length in meters [10-1000 m]
- **air_velocity** (float): Superficial air velocity in m/s [15-40 m/s]
- **particle_density** (float): Particle density in kg/m³ [500-5000 kg/m³]
- **particle_size** (float): Mean particle diameter in meters [10⁻⁶-0.01 m]

Optional Parameters:
~~~~~~~~~~~~~~~~~~~

- **solid_loading** (float): Solid-to-air mass ratio [0.1-50]
- **air_density** (float): Air density in kg/m³ [1.0-1.5 kg/m³]
- **friction_factor** (float): Pipe friction factor [0.001-0.01]
- **bend_pressure_loss** (float): Additional losses at bends [0.1-2.0]
- **pickup_velocity** (float): Material pickup velocity [5-25 m/s]

Working Ranges and Limitations
-------------------------------

**Operating Ranges:**

- **Dilute Phase**: Air velocity 15-40 m/s, solid loading 0.1-15
- **Dense Phase**: Air velocity 3-15 m/s, solid loading 15-50
- Pressure Drop: 10-100 kPa (dilute), 100-700 kPa (dense)
- Transport Distance: 10-1000 m (horizontal equivalent)
- Capacity: 0.1-100 t/h (depends on system size)

**Limitations:**

- Particle degradation due to high velocities and impacts
- High energy consumption compared to mechanical conveyors
- Sensitivity to particle size distribution
- Moisture content limitations
- Electrostatic charge buildup
- Wear on pipeline components

.. figure:: PneumaticConveying_detailed_analysis.png
   :width: 800px
   :align: center
   :alt: PneumaticConveying Detailed Analysis
   
   Detailed analysis showing pressure drop vs air velocity, minimum transport velocity, conveying capacity, and operating regions.

Code Example
------------

.. literalinclude:: PneumaticConveying_example.py
   :language: python
   :caption: PneumaticConveying usage example

Example Output
--------------

.. literalinclude:: PneumaticConveying_example.out
   :caption: Example execution output

Literature References
----------------------

1. **Wypych, P.W.**. "Pneumatic Conveying of Bulk Solids," Elsevier, 2019.

2. **Mills, D.**. "Pneumatic Conveying Design Guide," 3rd Edition, Butterworth-Heinemann, 2016.

3. **Klinzing, G.E.**. "Pneumatic Conveying of Solids: A Theoretical and Practical Approach," 3rd Edition, Springer, 2010.

4. **Levy, A. and Kalman, H.**. "Handbook of Conveying and Handling of Particulate Solids," Elsevier, 2001.

5. **Jones, M.G. and Mills, D.**. "Pneumatic conveying of solids," Chapman & Hall, 1991.

6. **Muschelknautz, E.**. "Design and calculation of pneumatic conveying installations," Bulk Solids Handling, 2(4), 1982.

7. **Zenz, F.A.**. "Two-phase fluid-solid flow," Industrial and Engineering Chemistry, 41(12), 2801-2806, 1949.

API Reference
-------------

.. autoclass:: transport.continuous.solid.PneumaticConveying.PneumaticConveying
   :members:
   :undoc-members:
   :show-inheritance:
