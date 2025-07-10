ConveyorBelt
============

Overview
--------

The ConveyorBelt class models continuous solid transport using belt conveyor systems. Belt conveyors are widely used in chemical processing, mining, and material handling operations for moving bulk solids horizontally, at an incline, or decline.

.. figure:: ConveyorBelt_example_plots.png
   :width: 800px
   :align: center
   :alt: ConveyorBelt Example Analysis
   
   ConveyorBelt system behavior showing belt speed response, material flow rate, power consumption, and load distribution.

Algorithm and Theory
--------------------

Belt conveyors operate on the principle of frictional forces between the belt surface and transported material. The system includes:

**Key Equations:**

- **Volumetric Flow Rate**: :math:`Q_v = A \cdot v \cdot \phi`
- **Mass Flow Rate**: :math:`Q_m = Q_v \cdot \rho_b`
- **Power Requirements**: :math:`P = F \cdot v / \eta`
- **Belt Tension**: :math:`T = T_0 + \mu \cdot W \cdot L / 1000`

Where:
- :math:`A` = Cross-sectional area of material (m²)
- :math:`v` = Belt speed (m/s)
- :math:`\phi` = Load factor (dimensionless)
- :math:`\rho_b` = Bulk density (kg/m³)
- :math:`F` = Total resistance force (N)
- :math:`\eta` = Drive efficiency (dimensionless)
- :math:`T_0` = Empty belt tension (N)
- :math:`\mu` = Friction coefficient
- :math:`W` = Material weight per unit length (N/m)
- :math:`L` = Belt length (m)

Use Cases
---------

- **Mining Operations**: Coal, ore, and aggregate transport
- **Chemical Processing**: Bulk chemical and powder handling
- **Food Industry**: Grain, sugar, and ingredient transport
- **Manufacturing**: Parts and assembly line movement
- **Waste Management**: Refuse and recycling material handling

Parameters
----------

Essential Parameters:
~~~~~~~~~~~~~~~~~~~~~

- **belt_width** (float): Belt width in meters [0.3-3.0 m]
- **belt_length** (float): Total belt length in meters [10-2000 m]
- **belt_speed** (float): Belt operating speed in m/s [0.1-6.0 m/s]
- **inclination_angle** (float): Belt inclination in degrees [-18° to +18°]
- **material_density** (float): Bulk density of material in kg/m³ [300-3000 kg/m³]

Optional Parameters:
~~~~~~~~~~~~~~~~~~~

- **load_factor** (float): Belt loading factor [0.1-0.9]
- **friction_coefficient** (float): Belt-material friction [0.1-0.8]
- **drive_efficiency** (float): Motor and drive efficiency [0.75-0.95]
- **surcharge_angle** (float): Material surcharge angle [0°-30°]

Working Ranges and Limitations
-------------------------------

**Operating Ranges:**

- Belt Speed: 0.1-6.0 m/s (typical: 1-3 m/s for bulk solids)
- Inclination: -18° to +18° (depends on material properties)
- Capacity: 1-10,000 t/h (depends on belt width and speed)
- Power: 1-1000 kW (depends on capacity and belt length)

**Limitations:**

- Maximum inclination limited by material properties
- Belt wear increases with abrasive materials
- Weather sensitivity for outdoor installations
- Spillage concerns at transfer points
- Limited flexibility in routing

.. figure:: ConveyorBelt_detailed_analysis.png
   :width: 800px
   :align: center
   :alt: ConveyorBelt Detailed Analysis
   
   Detailed analysis showing capacity vs belt speed, power consumption, inclination effects, and operating envelope.

Code Example
------------

.. literalinclude:: ConveyorBelt_example.py
   :language: python
   :caption: ConveyorBelt usage example

Example Output
--------------

.. literalinclude:: ConveyorBelt_example.out
   :caption: Example execution output

Literature References
----------------------

1. **CEMA (Conveyor Equipment Manufacturers Association)**. "Belt Conveyors for Bulk Materials," 7th Edition, 2014.

2. **Wypych, P.W.**. "Pneumatic Conveying of Bulk Solids," Elsevier, 2019.

3. **Roberts, A.W.**. "Bulk Solids: Flow Dynamics and Conveyor Design," Trans Tech Publications, 2015.

4. **Colijn, H.**. "Mechanical Conveyors for Bulk Solids," Elsevier, 1985.

5. **FEM (Fédération Européenne de la Manutention)**. "Rules for the Design of Belt Conveyors," 2001.

6. **ISO 5048:1989**. "Continuous mechanical handling equipment - Belt conveyors with carrying idlers - Calculation of operating power and tensile forces."

API Reference
-------------

.. autoclass:: transport.continuous.solid.ConveyorBelt.ConveyorBelt
   :members:
   :undoc-members:
   :show-inheritance:
