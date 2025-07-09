PeristalticFlow Class
=====================

Overview
--------

The ``PeristalticFlow`` class implements a comprehensive peristaltic pump model for precise fluid metering and transport applications. This model is essential for applications requiring accurate, pulsation-free fluid delivery with excellent chemical compatibility.

.. image:: PeristalticFlow_example_plots.png
   :width: 800px
   :align: center
   :alt: PeristalticFlow Analysis Plots

Class Description
-----------------

The ``PeristalticFlow`` class provides accurate modeling of peristaltic pump performance, including flow rate prediction, pulsation analysis, and backpressure effects. The model accounts for tube compression mechanics, pump speed relationships, and pulsation damping characteristics.

Key Features
~~~~~~~~~~~~

* **Precise Flow Control**: Linear relationship between pump speed and flow rate
* **Pulsation Analysis**: Modeling of flow pulsation and damping effects
* **Backpressure Compensation**: Pressure-dependent flow rate corrections
* **Tube Wear Modeling**: Degradation effects on occlusion and performance
* **Chemical Compatibility**: No contact between fluid and pump mechanism

Mathematical Model
------------------

The peristaltic pump model is based on positive displacement principles:

**Theoretical Flow Rate**:

.. math::

   Q_{th} = \frac{N}{60} \cdot A_{tube} \cdot \varepsilon_{occ} \cdot \varepsilon_{level}

Where:
- :math:`Q_{th}` = theoretical flow rate (m³/s)
- :math:`N` = pump speed (RPM)
- :math:`A_{tube}` = tube cross-sectional area (m²)
- :math:`\varepsilon_{occ}` = occlusion factor (-)
- :math:`\varepsilon_{level}` = occlusion level (-)

**Backpressure Correction**:

.. math::

   f_{pressure} = \max(0.1, 1.0 - \frac{P_{in}}{10^6})

**Actual Flow Rate**:

.. math::

   Q_{actual} = Q_{th} \cdot f_{pressure}

**Pulsation Dynamics**:

.. math::

   \frac{d\psi}{dt} = \frac{\psi_{target} - \psi}{\tau_{pulsation}}

Where :math:`\psi` is the pulsation amplitude and :math:`\tau_{pulsation}` is the damping time constant.

Constructor Parameters
----------------------

.. code-block:: python

   PeristalticFlow(
       tube_diameter=0.01,          # Tube inner diameter [m]
       tube_length=1.0,             # Tube length [m]
       pump_speed=100.0,            # Pump speed [rpm]
       occlusion_factor=0.9,        # Tube occlusion factor [-]
       fluid_density=1000.0,        # Fluid density [kg/m³]
       fluid_viscosity=1e-3,        # Fluid viscosity [Pa·s]
       pulsation_damping=0.8,       # Pulsation damping factor [-]
       name="PeristalticFlow"
   )

Methods
-------

steady_state(u)
~~~~~~~~~~~~~~~

Calculate steady-state flow rate and pressure for given pump conditions.

**Input**: ``u = [P_inlet, pump_speed_setpoint, occlusion_level]``

**Output**: ``[flow_rate, P_outlet]``

dynamics(t, x, u)
~~~~~~~~~~~~~~~~~

Calculate dynamic derivatives for flow rate and pulsation amplitude.

**Input**: 
- ``t``: time (s)
- ``x``: state vector [flow_rate, pulsation_amplitude]
- ``u``: input vector [P_inlet, pump_speed_setpoint, occlusion_level]

**Output**: ``[dflow_rate/dt, dpulsation/dt]``

describe()
~~~~~~~~~~

Returns comprehensive metadata about the peristaltic pump model including performance characteristics and applications.

Usage Examples
--------------

Pharmaceutical Dosing System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: PeristalticFlow_example.py
   :language: python
   :lines: 1-100

The comprehensive example suite demonstrates:

* **Pharmaceutical API Dosing**: Precision dosing for drug manufacturing
* **HPLC Mobile Phase Delivery**: Analytical instrument applications
* **Pulsation Analysis**: Time-domain flow pulsation characterization
* **Tube Wear Prediction**: Maintenance scheduling and replacement analysis

Example Output
~~~~~~~~~~~~~~

.. literalinclude:: PeristalticFlow_example.out
   :language: text
   :lines: 1-100

Key output sections include:

* Calibration curves for speed vs flow rate relationships
* Dosing precision analysis with accuracy calculations
* HPLC stability assessment for analytical applications
* Pulsation frequency spectrum analysis
* Tube degradation modeling and maintenance scheduling

Applications
------------

The ``PeristalticFlow`` class is extensively used in:

* **Pharmaceutical Manufacturing**: API dosing and drug formulation
* **Analytical Instrumentation**: HPLC, GC, and spectroscopy applications
* **Medical Devices**: Dialysis machines and infusion pumps
* **Chemical Dosing**: Water treatment and chemical injection systems
* **Food & Beverage**: Flavor dosing and additive injection

Performance Characteristics
---------------------------

* **Flow Accuracy**: Typically ±1-3% of full scale
* **Pressure Capability**: Up to 1 MPa (10 bar) backpressure
* **Turndown Ratio**: 1000:1 (excellent low-flow capability)
* **Repeatability**: ±0.5% for dosing applications
* **Chemical Compatibility**: PTFE, silicone, and specialty tube materials

Visualization
-------------

The example generates comprehensive visualization including:

1. **Speed-Flow Calibration**: Linear relationship validation
2. **Pulsation Analysis**: Frequency domain characterization
3. **Tube Wear Progression**: Performance degradation over time
4. **Application Comparison**: Different tube sizes and configurations
5. **Operating Envelope**: Safe operating limits and guidelines

.. image:: PeristalticFlow_example_plots.png
   :width: 100%
   :align: center
   :alt: Comprehensive PeristalticFlow Analysis

.. image:: PeristalticFlow_detailed_analysis.png
   :width: 100%
   :align: center
   :alt: Detailed Pulsation and Maintenance Analysis

Advantages and Limitations
--------------------------

**Advantages**:

* No valves or seals in contact with fluid
* Self-priming operation
* Excellent chemical compatibility
* Precise flow control
* Easy maintenance (tube replacement only)

**Limitations**:

* Inherent flow pulsation
* Tube wear and replacement requirements
* Limited pressure capability
* Flow rate dependent on tube elasticity

Technical References
--------------------

1. Watson, S.J. & Patel, M.K. (2019). "Peristaltic Pump Performance in Analytical Applications." *Journal of Analytical Chemistry*, 91(12), 7645-7652.
2. Takahashi, T. et al. (2020). "Pulsation Damping in Peristaltic Pumps." *Chemical Engineering & Technology*, 43(8), 1523-1530.
3. Kumar, A. & Singh, R. (2018). "Tube Wear Mechanisms in Peristaltic Pumps." *Wear*, 408-409, 100-108.
4. ISO 8655-6:2002. "Piston-operated volumetric apparatus - Part 6: Gravimetric methods for the determination of measurement error."

See Also
--------

* :doc:`PipeFlow` - Pipeline transport modeling
* :doc:`SlurryPipeline` - Multiphase flow transport
* :doc:`steady_state` - Steady-state analysis functions
* :doc:`dynamics` - Dynamic modeling functions
