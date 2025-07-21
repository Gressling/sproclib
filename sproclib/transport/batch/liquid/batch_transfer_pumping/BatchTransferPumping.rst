BatchTransferPumping
===================

.. currentmodule:: transport.batch.liquid

.. autoclass:: BatchTransferPumping
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The ``BatchTransferPumping`` class models batch liquid transfer operations using pumps, incorporating pump characteristics, system hydraulics, and fluid dynamics. This model is essential for batch processing operations where liquids need to be transferred from one tank to another in discrete quantities.

Use Cases
---------

Batch transfer pumping is commonly used in:

* Chemical batch processing plants
* Pharmaceutical manufacturing
* Food and beverage production  
* Water treatment facilities
* Laboratory-scale operations

The model helps predict transfer times, optimize pump sizing, and ensure proper system design for efficient batch operations.

Algorithm Description
---------------------

The model implements two main calculation modes:

Steady-State Algorithm
~~~~~~~~~~~~~~~~~~~~~~

1. **Hydraulic Head Calculation**: Determines static head based on level difference
2. **Flow Rate Estimation**: Uses pump curve with speed and efficiency factors
3. **System Resistance**: Calculates friction losses using Darcy-Weisbach equation
4. **Flow Rate Adjustment**: Reduces flow if pump head is insufficient
5. **Transfer Time Prediction**: Estimates remaining transfer time based on volume and flow rate

Dynamic Algorithm
~~~~~~~~~~~~~~~~~

1. **Pump Response Dynamics**: Models pump startup/shutdown with time constant
2. **Tank Level Dynamics**: Implements mass balance for source tank
3. **Flow Rate Evolution**: Tracks flow rate changes over time
4. **System Constraints**: Enforces physical limits (empty tank stops flow)

Parameters
----------

.. list-table:: Model Parameters
   :widths: 20 10 20 50
   :header-rows: 1

   * - Parameter
     - Unit
     - Range
     - Description
   * - pump_capacity
     - m³/s
     - 0.001 - 0.1
     - Maximum pump flow capacity at rated conditions
   * - pump_head_max
     - m
     - 10 - 100
     - Maximum pump head at zero flow
   * - tank_volume
     - m³
     - 0.1 - 10
     - Source tank volume for batch calculations
   * - pipe_length
     - m
     - 1 - 100
     - Transfer line length affecting friction
   * - pipe_diameter
     - m
     - 0.01 - 0.2
     - Transfer line internal diameter
   * - fluid_density
     - kg/m³
     - 500 - 2000
     - Fluid density at operating temperature
   * - fluid_viscosity
     - Pa·s
     - 1e-6 - 1e-1
     - Dynamic viscosity at operating temperature
   * - transfer_efficiency
     - -
     - 0.5 - 0.95
     - Overall pump transfer efficiency

Mathematical Equations
----------------------

Reynolds Number
~~~~~~~~~~~~~~~

.. math::

   Re = \\frac{\\rho v D}{\\mu}

Where:

* :math:`\\rho` = fluid density [kg/m³]
* :math:`v` = fluid velocity [m/s]
* :math:`D` = pipe diameter [m]
* :math:`\\mu` = dynamic viscosity [Pa·s]

Friction Factor
~~~~~~~~~~~~~~~

For laminar flow (Re < 2300):

.. math::

   f = \\frac{64}{Re}

For turbulent flow (Re ≥ 2300):

.. math::

   f = \\frac{0.316}{Re^{0.25}}

Friction Head Loss
~~~~~~~~~~~~~~~~~~

.. math::

   h_f = f \\cdot \\frac{L}{D} \\cdot \\frac{v^2}{2g}

Where:

* :math:`L` = pipe length [m]
* :math:`g` = gravitational acceleration [m/s²]

Total Head Required
~~~~~~~~~~~~~~~~~~~

.. math::

   H_{total} = H_{static} + H_{friction}

Mass Balance (Dynamic)
~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \\frac{dV}{dt} = Q_{in} - Q_{out}

Pump Characteristic
~~~~~~~~~~~~~~~~~~~

.. math::

   Q = Q_{max} \\cdot speed_{fraction} \\cdot efficiency

Working Ranges
--------------

Flow Conditions
~~~~~~~~~~~~~~~

* **Reynolds Number**: 10 - 100,000 (laminar to turbulent)
* **Velocity**: 0.1 - 5 m/s (typical industrial range)
* **Flow Rate**: 10% - 100% of pump capacity

System Pressures
~~~~~~~~~~~~~~~~

* **Static Head**: -10 to +50 m (suction to discharge)
* **Friction Losses**: 0.1 - 20 m (depending on system design)
* **Pump Operating Point**: 20% - 100% of rated head

Operational Limits
~~~~~~~~~~~~~~~~~~

* **Tank Level**: 5% - 95% of tank height
* **Transfer Time**: 1 minute - 8 hours typical
* **Temperature**: 5°C - 80°C (affects fluid properties)

Usage Guidelines
----------------

1. **Parameter Selection**: Choose pump capacity 20-30% above required flow rate
2. **Pipe Sizing**: Maintain velocity between 1-3 m/s for efficiency
3. **Head Calculations**: Include safety factor of 10-20% for head requirements
4. **Dynamic Response**: Consider pump time constant for control system design

Examples
--------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from transport.batch.liquid.BatchTransferPumping import BatchTransferPumping
   import numpy as np

   # Create pump instance
   pump = BatchTransferPumping(
       pump_capacity=0.01,      # 10 L/s
       pump_head_max=50.0,      # 50 m
       tank_volume=1.0,         # 1 m³
       pipe_length=20.0,        # 20 m
       pipe_diameter=0.05       # 5 cm
   )

   # Steady-state analysis
   u = np.array([0.8, 0.2, 1.0])  # [source_level, dest_level, pump_speed]
   flow_rate, transfer_time = pump.steady_state(u)
   print(f"Flow rate: {flow_rate*1000:.1f} L/s")
   print(f"Transfer time: {transfer_time/60:.1f} minutes")

   # Dynamic simulation
   x = np.array([0.0, 0.8])  # [initial_flow, source_level]
   dxdt = pump.dynamics(0.0, x, u)
   print(f"Flow rate derivative: {dxdt[0]:.4f} m³/s²")
   print(f"Level derivative: {dxdt[1]:.4f} 1/s")

Performance Analysis
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Model introspection
   description = pump.describe()
   print(f"Model type: {description['type']}")
   print(f"Applications: {description['applications']}")

   # Parameter sensitivity analysis
   pump_speeds = [0.2, 0.5, 0.8, 1.0]
   for speed in pump_speeds:
       u = np.array([0.8, 0.2, speed])
       flow, time = pump.steady_state(u)
       print(f"Speed {speed*100:3.0f}%: {flow*1000:5.1f} L/s, {time/60:5.1f} min")

Visualization
~~~~~~~~~~~~~

The example file generates comprehensive visualizations showing:

* Flow rate evolution over time
* Tank level changes during transfer
* Steady-state performance comparison
* Pump characteristic curves
* Reynolds number evolution
* Cumulative volume transfer
* System efficiency analysis
* Head requirement analysis

.. figure:: BatchTransferPumping_example_plots.png
   :width: 800px
   :align: center
   :alt: Batch Transfer Pumping Analysis Plots

   Dynamic response and steady-state analysis for water and oil transfer systems

.. figure:: BatchTransferPumping_detailed_analysis.png
   :width: 800px
   :align: center
   :alt: Detailed Analysis Plots

   Detailed hydraulic analysis including Reynolds number evolution and system efficiency

Test Coverage
-------------

The test suite covers:

* Model initialization and parameter validation
* Steady-state calculations under various conditions
* Dynamic behavior and system constraints
* Edge cases and numerical stability
* High viscosity fluid handling
* Reynolds number regime transitions
* Mass conservation verification
* Pump head limitations

Run tests using:

.. code-block:: bash

   pytest BatchTransferPumping_test.py -v

References
----------

1. Perry, R.H., Green, D.W. (2019). "Perry's Chemical Engineers' Handbook", 9th Edition, McGraw-Hill.
2. Crane Co. (2013). "Flow of Fluids Through Valves, Fittings, and Pipe", Technical Paper 410.
3. Karassik, I.J., et al. (2008). "Pump Handbook", 4th Edition, McGraw-Hill.
4. Coulson, J.M., Richardson, J.F. (2017). "Chemical Engineering Design", Volume 6, 5th Edition.
5. Sinnott, R., Towler, G. (2019). "Chemical Engineering Design", 6th Edition, Butterworth-Heinemann.
6. White, F.M. (2016). "Fluid Mechanics", 8th Edition, McGraw-Hill.
7. Munson, B.R., et al. (2016). "Fundamentals of Fluid Mechanics", 8th Edition, Wiley.

.. note::
   This model assumes incompressible flow and single-phase operation. For two-phase flows or compressible fluids, additional models may be required.

.. warning::
   Always verify that pump specifications match system requirements. Insufficient head can result in reduced flow rates or pump cavitation.
