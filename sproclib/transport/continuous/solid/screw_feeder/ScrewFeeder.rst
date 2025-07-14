ScrewFeeder
===========

Overview
--------

The ScrewFeeder class models continuous solid transport using rotating screw mechanisms. Screw feeders (also known as screw conveyors or augers) provide controlled, metered feeding of bulk solids with excellent flow control and minimal segregation.

.. figure:: ScrewFeeder_example_plots.png
   :width: 800px
   :align: center
   :alt: ScrewFeeder Example Analysis
   
   ScrewFeeder system behavior showing flow rate response, power consumption, drive torque, and volumetric efficiency.

Algorithm and Theory
--------------------

Screw feeders operate by rotating a helical screw within a trough or tube, advancing material along the screw axis. The transport mechanism combines the screw geometry with material properties.

**Key Equations:**

- **Theoretical Flow Rate**: :math:`Q_t = \frac{\pi D^2 S N}{4} \cdot \phi`
- **Actual Flow Rate**: :math:`Q_a = Q_t \cdot \eta_v \cdot \rho_b`
- **Power Requirement**: :math:`P = \frac{T \cdot \omega}{\eta_m}`
- **Screw Torque**: :math:`T = \mu \cdot W \cdot r + T_{friction}`

Where:
- :math:`D` = Screw diameter (m)
- :math:`S` = Screw pitch (m)
- :math:`N` = Rotational speed (rpm)
- :math:`\phi` = Fill factor (dimensionless)
- :math:`\eta_v` = Volumetric efficiency (dimensionless)
- :math:`\rho_b` = Bulk density (kg/m³)
- :math:`T` = Torque (Nm)
- :math:`\omega` = Angular velocity (rad/s)
- :math:`\eta_m` = Mechanical efficiency (dimensionless)
- :math:`\mu` = Friction coefficient
- :math:`W` = Material weight (N)
- :math:`r` = Screw radius (m)

Use Cases
---------

- **Chemical Processing**: Catalyst feeding, additive metering
- **Food Industry**: Flour, sugar, and ingredient dosing
- **Pharmaceutical**: Powder blending and tablet feeding
- **Plastics Industry**: Resin and additive feeding to extruders
- **Agriculture**: Grain handling and feed distribution
- **Cement Industry**: Raw material and cement feeding
- **Mining**: Ore and coal feeding to processing equipment

Parameters
----------

Essential Parameters:
~~~~~~~~~~~~~~~~~~~~~

- **screw_diameter** (float): Outer screw diameter in meters [0.05-1.0 m]
- **screw_pitch** (float): Axial distance between flights in meters [0.8-1.2 × diameter]
- **screw_length** (float): Total screw length in meters [1-20 m]
- **rpm** (float): Rotational speed in revolutions per minute [1-200 rpm]
- **material_density** (float): Bulk density of material in kg/m³ [200-3000 kg/m³]

Optional Parameters:
~~~~~~~~~~~~~~~~~~~

- **fill_factor** (float): Trough fill level [0.15-0.45]
- **efficiency** (float): Overall mechanical efficiency [0.7-0.9]
- **friction_coefficient** (float): Material-screw friction [0.2-0.8]
- **inclination_angle** (float): Screw inclination angle [0°-45°]
- **shaft_diameter** (float): Central shaft diameter [0.1-0.3 × screw diameter]

Working Ranges and Limitations
-------------------------------

**Operating Ranges:**

- Rotational Speed: 1-200 rpm (typical: 20-100 rpm for bulk solids)
- Inclination: 0°-45° (horizontal to inclined applications)
- Capacity: 0.1-500 t/h (depends on screw size and material)
- Power: 0.5-100 kW (depends on capacity and material properties)
- Fill Factor: 15%-45% (optimal: 30%-40%)

**Limitations:**

- Material degradation with friable materials
- Segregation potential with mixed particle sizes
- Limited to relatively short distances
- Wear on screw flights and trough
- Not suitable for very sticky or cohesive materials
- Power consumption increases significantly with inclination

.. figure:: ScrewFeeder_detailed_analysis.png
   :width: 800px
   :align: center
   :alt: ScrewFeeder Detailed Analysis
   
   Detailed analysis showing flow rate vs RPM, power consumption, efficiency vs fill ratio, and operating envelope.

Code Example
------------

.. literalinclude:: ScrewFeeder_example.py
   :language: python
   :caption: ScrewFeeder usage example

Example Output
--------------

.. literalinclude:: ScrewFeeder_example.out
   :caption: Example execution output

Literature References
----------------------

1. **Roberts, A.W.**. "Bulk Solids: Flow Dynamics and Conveyor Design," Trans Tech Publications, 2015.

2. **CEMA (Conveyor Equipment Manufacturers Association)**. "Screw Conveyors for Bulk Materials," 5th Edition, 2005.

3. **Owen, P.J. and Cleary, P.W.**. "Screw conveyor performance: comparison of discrete element modelling with laboratory experiments," Progress in Industrial Mathematics at ECMI 2004, 2006.

4. **Colijn, H.**. "Mechanical Conveyors for Bulk Solids," Elsevier, 1985.

5. **Schulze, D.**. "Powders and Bulk Solids: Behavior, Characterization, Storage and Flow," Springer, 2007.

6. **FEM (Fédération Européenne de la Manutention)**. "Rules for the Design of Screw Conveyors," 1998.

7. **ISO 7119:1981**. "Continuous mechanical handling equipment - Screw conveyors - Calculation of power."

API Reference
-------------

.. autoclass:: transport.continuous.solid.ScrewFeeder.ScrewFeeder
   :members:
   :undoc-members:
   :show-inheritance:
