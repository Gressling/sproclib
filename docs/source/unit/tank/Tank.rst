Tank Model
==========

.. currentmodule:: unit.tank.Tank

Overview
--------

The Tank class implements a gravity-drained tank model based on material balance principles and Torricelli's law. This model is fundamental in process control applications, particularly for level control systems and process dynamics studies.

The tank model represents a common unit operation in chemical engineering where liquid flows into a tank and exits through a gravity-driven outlet at the bottom.

Algorithm Description
--------------------

The tank model is based on a material balance around the tank volume:

.. math::
   
   \text{Accumulation} = \text{Inflow} - \text{Outflow}
   
   A \frac{dh}{dt} = q_{in} - q_{out}

The outlet flow follows Torricelli's law for gravity discharge:

.. math::
   
   q_{out} = C \sqrt{h}

Combining these equations yields the fundamental tank dynamics:

.. math::
   
   \frac{dh}{dt} = \frac{q_{in} - C\sqrt{h}}{A}

Mathematical Model
-----------------

State Variables
~~~~~~~~~~~~~~

- **h**: Tank height [m]

Input Variables  
~~~~~~~~~~~~~~

- **q_in**: Inlet flow rate [m³/min]

Parameters
~~~~~~~~~

- **A**: Cross-sectional area [m²]
- **C**: Discharge coefficient [m²/min]

Governing Equations
~~~~~~~~~~~~~~~~~~

**Dynamic equation:**

.. math::
   
   \frac{dh}{dt} = \frac{q_{in} - C\sqrt{h}}{A}

**Outlet flow:**

.. math::
   
   q_{out} = C\sqrt{h}

**Tank volume:**

.. math::
   
   V = A \cdot h

**Steady-state height:**

.. math::
   
   h_{ss} = \left(\frac{q_{in}}{C}\right)^2

**Linearized time constant:**

.. math::
   
   \tau = \frac{2A\sqrt{h}}{C}

Parameters and Working Ranges
----------------------------

Cross-sectional Area (A)
~~~~~~~~~~~~~~~~~~~~~~~~

- **Range**: 0.1 - 10 m²
- **Typical**: 1.0 m²
- **Effect**: Larger area reduces response speed

Discharge Coefficient (C)
~~~~~~~~~~~~~~~~~~~~~~~~

- **Range**: 0.01 - 1.0 m²/min
- **Typical**: 0.1 - 0.5 m²/min
- **Effect**: Higher values increase discharge rate and reduce steady-state height

Operating Ranges
~~~~~~~~~~~~~~~

- **Height**: 0 - 10 m
- **Flow rate**: 0 - 5 m³/min
- **Time constant**: 1 - 100 min (typical)

Physical Assumptions
-------------------

- Incompressible fluid
- Constant cross-sectional area
- Gravity-driven discharge
- Turbulent flow through outlet (Reynolds number > 4000)
- Negligible fluid acceleration effects

Limitations
----------

- Cannot model negative tank heights
- Assumes constant discharge coefficient
- Does not account for varying cross-sections
- Neglects entrance/exit losses in detail

Code Example
-----------

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt
   from scipy.integrate import solve_ivp
   from unit.tank.Tank import Tank

   # Create tank instance
   tank = Tank(A=1.5, C=0.4, name="ExampleTank")
   
   # Initial conditions
   h0 = 1.0  # Initial height [m]
   
   # Step input function
   def step_input(t, step_time=5.0, initial_flow=0.5, final_flow=0.8):
       return final_flow if t >= step_time else initial_flow
   
   # Simulate step response
   def tank_dynamics(t, x):
       u = np.array([step_input(t)])
       return tank.dynamics(t, x, u)
   
   t_span = (0, 30)
   t_eval = np.linspace(0, 30, 301)
   sol = solve_ivp(tank_dynamics, t_span, [h0], t_eval=t_eval)
   
   # Plot results
   plt.figure(figsize=(10, 6))
   plt.plot(t_eval, sol.y[0], 'b-', linewidth=2, label='Height')
   plt.xlabel('Time [min]')
   plt.ylabel('Height [m]')
   plt.title('Tank Height Response')
   plt.grid(True)
   plt.show()

Example Output
-------------

.. code-block:: text

   Tank Model Example
   ==================

   1. Creating Tank Model
   Tank Name: Tank
   Description: Gravity-drained tank model for level control applications
   Cross-sectional Area: 1.5 m²
   Discharge Coefficient: 0.4 m²/min

   2. Simulation Setup
   Initial height: 1.0 m
   Simulation time: 30 minutes

   3. Steady-State Analysis
   Initial flow rate: 0.5 m³/min
   Initial steady-state height: 1.562 m
   Final flow rate: 0.8 m³/min
   Final steady-state height: 4.000 m

   4. Time Constant Analysis
   Time constant at initial operating point: 9.38 min
   Time constant at final operating point: 15.00 min

   5. Step Response Simulation
   Simulation completed successfully
   Final height: 3.559 m
   Final outlet flow: 0.755 m³/min
   Final volume: 5.338 m³

   6. Performance Metrics
   Height: 3.559 m
   Outlet flow: 0.755 m³/min
   Volume: 5.338 m³
   Time constant: 14.15 min
   Mass balance error: 0.045425 m³/min
   Residence time: 7.07 min

   7. Response Analysis
   Time to reach 63.2% of step change: 14.90 min
   Theoretical time constant: 15.00 min
   Settling time (2% criterion): 25.00 min

Visualizations
-------------

The following plots demonstrate the tank model behavior:

**Main Response Analysis:**

.. image:: Tank_example_plots.png
   :alt: Tank response analysis showing height, flow rates, volume, and mass balance
   :width: 800px
   :align: center

**Detailed Analysis:**

.. image:: Tank_detailed_analysis.png
   :alt: Detailed tank analysis including phase portrait, time constants, and flow characteristics
   :width: 800px
   :align: center

Control System Applications
--------------------------

PID Controller Tuning
~~~~~~~~~~~~~~~~~~~~

The linearized time constant τ = 2A√h/C provides guidance for controller tuning:

- **Proportional gain**: Kc = 1/τ
- **Integral time**: Ti = τ  
- **Derivative time**: Td = τ/4

Process Characteristics
~~~~~~~~~~~~~~~~~~~~~

- **Process gain**: Kp = 2√h_ss/C
- **Dead time**: Typically negligible for well-mixed tanks
- **Nonlinearity**: Moderate due to square root relationship

Industrial Applications
----------------------

Water Treatment
~~~~~~~~~~~~~

- Clarifier tanks
- Storage tanks
- Equalization basins

Chemical Processing
~~~~~~~~~~~~~~~~~

- Reactor vessels
- Buffer tanks
- Settling tanks

Petroleum Refining
~~~~~~~~~~~~~~~~

- Surge tanks
- Product storage
- Separation vessels

References
----------

1. Seborg, D.E., Edgar, T.F., Mellichamp, D.A., & Doyle III, F.J. (2016). *Process Dynamics and Control* (4th ed.). Wiley.

2. Stephanopoulos, G. (1984). *Chemical Process Control: An Introduction to Theory and Practice*. Prentice Hall.

3. Luyben, W.L. (1990). *Process Modeling, Simulation, and Control for Chemical Engineers* (2nd ed.). McGraw-Hill.

4. Ogunnaike, B.A., & Ray, W.H. (1994). *Process Dynamics, Modeling, and Control*. Oxford University Press.

5. Bequette, B.W. (2003). *Process Control: Modeling, Design, and Simulation*. Prentice Hall.

API Reference
------------

.. autoclass:: Tank
   :members:
   :undoc-members:
   :show-inheritance:
