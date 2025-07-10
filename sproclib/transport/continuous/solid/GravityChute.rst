GravityChute
============

Overview
--------

The GravityChute class models gravitational solid transport through inclined chutes and slides. Gravity chutes are simple, energy-efficient systems used in material handling where materials flow under gravitational force along inclined surfaces.

.. figure:: GravityChute_example_plots.png
   :width: 800px
   :align: center
   :alt: GravityChute Example Analysis
   
   GravityChute system behavior showing flow rate response, velocity profiles, pressure buildup, and flow efficiency.

Algorithm and Theory
--------------------

Gravity chutes operate based on gravitational acceleration and friction forces. The flow behavior depends on material properties, chute geometry, and inclination angle.

**Key Equations:**

- **Flow Velocity**: :math:`v = \sqrt{2gh \cdot \sin(\theta) \cdot (1 - \mu \cos(\theta))}`
- **Mass Flow Rate**: :math:`Q_m = \rho_b \cdot A \cdot v \cdot \phi`
- **Acceleration**: :math:`a = g(\sin(\theta) - \mu \cos(\theta))`
- **Flow Depth**: :math:`h = (Q_m / (\rho_b \cdot w \cdot v))^{2/3}`

Where:
- :math:`g` = Gravitational acceleration (9.81 m/s²)
- :math:`h` = Flow depth or height (m)
- :math:`\theta` = Chute inclination angle (rad)
- :math:`\mu` = Friction coefficient between material and chute
- :math:`\rho_b` = Bulk density (kg/m³)
- :math:`A` = Cross-sectional flow area (m²)
- :math:`\phi` = Flow factor (dimensionless)
- :math:`w` = Chute width (m)

Use Cases
---------

- **Mining Operations**: Ore and coal transport from storage to processing
- **Cement Industry**: Limestone and clinker handling
- **Food Processing**: Grain and bulk ingredient transfer
- **Chemical Plants**: Granular chemical transport
- **Waste Management**: Sorting and disposal operations
- **Agriculture**: Grain elevator and silo discharge

Parameters
----------

Essential Parameters:
~~~~~~~~~~~~~~~~~~~~~

- **chute_width** (float): Chute width in meters [0.2-5.0 m]
- **chute_length** (float): Total chute length in meters [2-100 m]
- **inclination_angle** (float): Chute inclination in degrees [15°-60°]
- **material_density** (float): Bulk density of material in kg/m³ [300-3000 kg/m³]
- **friction_coefficient** (float): Material-chute friction [0.1-0.8]

Optional Parameters:
~~~~~~~~~~~~~~~~~~~

- **flow_factor** (float): Flow efficiency factor [0.5-1.0]
- **roughness** (float): Surface roughness factor [0.001-0.01 m]
- **side_wall_height** (float): Chute side wall height [0.1-2.0 m]
- **discharge_coefficient** (float): Discharge efficiency [0.6-0.9]

Working Ranges and Limitations
-------------------------------

**Operating Ranges:**

- Inclination Angle: 15°-60° (optimal: 30°-45° for most materials)
- Flow Velocity: 1-15 m/s (depends on inclination and material)
- Capacity: 10-5000 t/h (depends on chute size and material)
- Material Size: 0.1-300 mm (fine powders to coarse aggregates)

**Limitations:**

- Requires sufficient inclination for flow initiation
- Material degradation due to impact and abrasion
- Dust generation with fine materials
- Limited control over flow rate
- Potential for blockages with cohesive materials
- Noise generation at high velocities

.. figure:: GravityChute_detailed_analysis.png
   :width: 800px
   :align: center
   :alt: GravityChute Detailed Analysis
   
   Detailed analysis showing velocity vs inclination, flow capacity, friction effects, and operating envelope.

Code Example
------------

.. literalinclude:: GravityChute_example.py
   :language: python
   :caption: GravityChute usage example

Example Output
--------------

.. literalinclude:: GravityChute_example.out
   :caption: Example execution output

Literature References
----------------------

1. **Brown, R.L. and Richards, J.C.**. "Principles of Powder Mechanics," Pergamon Press, 1970.

2. **Cleary, P.W.**. "DEM prediction of industrial and geophysical particle flows," Particuology, 8(2), 106-118, 2010.

3. **Schulze, D.**. "Powders and Bulk Solids: Behavior, Characterization, Storage and Flow," Springer, 2007.

4. **Marinelli, J. and Carson, J.W.**. "Solve solids flow problems in bins, hoppers, and feeders," Chemical Engineering Progress, 88(5), 1992.

5. **Jenike, A.W.**. "Storage and Flow of Solids," Bulletin No. 123, University of Utah Engineering Experiment Station, 1964.

6. **Roberts, A.W.**. "Chute performance and design for rapid flow conditions," Chemical Engineering and Technology, 26(2), 163-170, 2003.

API Reference
-------------

.. autoclass:: transport.continuous.solid.GravityChute.GravityChute
   :members:
   :undoc-members:
   :show-inheritance:
