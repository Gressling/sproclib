InteractingTanks Model
====================

.. currentmodule:: unit.tank.InteractingTanks

Overview
--------

The InteractingTanks class implements a two-tank system in series where the outlet of the first tank feeds the second tank. This configuration is widely used in process control education and industrial applications to study multi-variable dynamics and control strategies.

This model represents a common configuration in chemical processing where multiple tanks are connected in series for sequential processing or storage.

Algorithm Description
--------------------

The interacting tanks model consists of two coupled material balance equations:

**Tank 1:**

.. math::
   
   A_1 \frac{dh_1}{dt} = q_{in} - q_{12}

**Tank 2:**

.. math::
   
   A_2 \frac{dh_2}{dt} = q_{12} - q_{out}

Where the inter-tank flow and outlet flow follow Torricelli's law:

.. math::
   
   q_{12} = C_1 \sqrt{h_1}
   
   q_{out} = C_2 \sqrt{h_2}

Mathematical Model
-----------------

State Variables
~~~~~~~~~~~~~~

- **h1**: Tank 1 height [m]
- **h2**: Tank 2 height [m]

Input Variables
~~~~~~~~~~~~~~

- **q_in**: Inlet flow rate to tank 1 [m³/min]

Parameters
~~~~~~~~~

- **A1**: Tank 1 cross-sectional area [m²]
- **A2**: Tank 2 cross-sectional area [m²]
- **C1**: Tank 1 discharge coefficient [m²/min]
- **C2**: Tank 2 discharge coefficient [m²/min]

Governing Equations
~~~~~~~~~~~~~~~~~~

**Tank 1 dynamics:**

.. math::
   
   \frac{dh_1}{dt} = \frac{q_{in} - C_1\sqrt{h_1}}{A_1}

**Tank 2 dynamics:**

.. math::
   
   \frac{dh_2}{dt} = \frac{C_1\sqrt{h_1} - C_2\sqrt{h_2}}{A_2}

**Inter-tank flow:**

.. math::
   
   q_{12} = C_1\sqrt{h_1}

**Outlet flow:**

.. math::
   
   q_{out} = C_2\sqrt{h_2}

**Steady-state heights:**

.. math::
   
   h_{1,ss} = \left(\frac{q_{in}}{C_1}\right)^2
   
   h_{2,ss} = \left(\frac{q_{in}}{C_2}\right)^2

Transfer Function Analysis
-------------------------

For small perturbations around steady-state, the system can be linearized:

**Tank 1 time constant:**

.. math::
   
   \tau_1 = \frac{2A_1\sqrt{h_{1,ss}}}{C_1}

**Tank 2 time constant:**

.. math::
   
   \tau_2 = \frac{2A_2\sqrt{h_{2,ss}}}{C_2}

**Overall transfer function (h2/q_in):**

.. math::
   
   G(s) = \frac{K}{(\tau_1 s + 1)(\tau_2 s + 1)}

Where K is the overall process gain.

Parameters and Working Ranges
----------------------------

Cross-sectional Areas (A1, A2)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Range**: 0.1 - 10 m²
- **Typical**: 1.0 m²
- **Effect**: Larger areas increase time constants

Discharge Coefficients (C1, C2)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Range**: 0.01 - 1.0 m²/min
- **Typical**: 0.1 - 0.5 m²/min
- **Effect**: Higher values decrease time constants

Operating Ranges
~~~~~~~~~~~~~~~

- **Heights**: 0 - 10 m
- **Flow rates**: 0 - 5 m³/min
- **Time constants**: 2 - 200 min (typical)

System Characteristics
---------------------

Process Gain
~~~~~~~~~~~

The steady-state gain from inlet flow to tank 2 level:

.. math::
   
   K = \frac{4h_{2,ss}}{q_{in,ss}} = \frac{4}{C_2^2}

Time Constants
~~~~~~~~~~~~~

- **Fast tank**: min(τ1, τ2)
- **Slow tank**: max(τ1, τ2)
- **Dominant pole**: Usually the slower tank

Interaction Effects
~~~~~~~~~~~~~~~~~

- Strong interaction when τ1 ≈ τ2
- Weak interaction when τ1 >> τ2 or τ1 << τ2

Physical Assumptions
-------------------

- Incompressible fluid
- Constant cross-sectional areas
- Gravity-driven discharge
- Perfect mixing in each tank
- Negligible pipe dynamics between tanks
- Turbulent flow through outlets

Limitations
----------

- Cannot model negative tank heights
- Assumes constant discharge coefficients
- Does not account for pipe pressure drops
- Neglects fluid acceleration effects

Code Example
-----------

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt
   from scipy.integrate import solve_ivp
   from unit.tank.InteractingTanks import InteractingTanks

   # Create interacting tanks instance
   tanks = InteractingTanks(A1=1.2, A2=0.8, C1=0.3, C2=0.25, name="ExampleTanks")
   
   # Initial conditions
   h1_0, h2_0 = 1.5, 0.8  # Initial heights [m]
   
   # Step input function
   def step_input(t, step_time=10.0, initial_flow=0.4, final_flow=0.7):
       return final_flow if t >= step_time else initial_flow
   
   # Simulate step response
   def tanks_dynamics(t, x):
       u = np.array([step_input(t)])
       return tanks.dynamics(t, x, u)
   
   t_span = (0, 60)
   t_eval = np.linspace(0, 60, 601)
   sol = solve_ivp(tanks_dynamics, t_span, [h1_0, h2_0], t_eval=t_eval)
   
   # Plot results
   plt.figure(figsize=(10, 6))
   plt.plot(t_eval, sol.y[0], 'b-', linewidth=2, label='Tank 1 Height')
   plt.plot(t_eval, sol.y[1], 'r-', linewidth=2, label='Tank 2 Height')
   plt.xlabel('Time [min]')
   plt.ylabel('Height [m]')
   plt.title('Interacting Tanks Response')
   plt.legend()
   plt.grid(True)
   plt.show()

Example Output
-------------

.. code-block:: text

   InteractingTanks Model Example
   ==============================

   1. Creating InteractingTanks Model
   System Name: InteractingTanks
   Description: Two interacting tanks in series for process dynamics studies
   Tank 1 - Area: 1.2 m², Discharge: 0.3 m²/min
   Tank 2 - Area: 0.8 m², Discharge: 0.25 m²/min

   2. Simulation Setup
   Initial heights: Tank 1 = 1.5 m, Tank 2 = 0.8 m
   Simulation time: 60 minutes

   3. Steady-State Analysis
   Initial flow rate: 0.4 m³/min
   Initial steady-state heights: Tank 1 = 1.778 m, Tank 2 = 2.560 m
   Final flow rate: 0.7 m³/min
   Final steady-state heights: Tank 1 = 5.444 m, Tank 2 = 7.840 m

   4. Linearized Time Constants
   Tank 1 time constant: 18.67 min
   Tank 2 time constant: 17.92 min

   5. Step Response Simulation
   Simulation completed successfully
   Final heights: Tank 1 = 5.229 m, Tank 2 = 6.782 m
   Final inter-tank flow: 0.686 m³/min
   Final outlet flow: 0.651 m³/min

   6. Response Analysis
   Tank 2 - Time to reach 63.2% of step change: 34.90 min
   Tank 2 - Settling time (2% criterion): 50.00 min

   7. Mass Balance Verification
   Maximum mass balance error: 5.55e-17 m³/min
   Mass balance verification: PASSED

Visualizations
-------------

The following plots demonstrate the interacting tanks model behavior:

**Main Response Analysis:**

.. image:: InteractingTanks_example_plots.png
   :alt: Interacting tanks response analysis showing heights, flow rates, volumes, and mass balance
   :width: 800px
   :align: center

**Detailed Analysis:**

.. image:: InteractingTanks_detailed_analysis.png
   :alt: Detailed analysis including phase portrait, interaction strength, and flow characteristics
   :width: 800px
   :align: center

Control System Design
--------------------

SISO Control
~~~~~~~~~~~

- **Primary**: Control h2 with q_in
- **Secondary**: Control h1 with intermediate manipulator

MIMO Control
~~~~~~~~~~~

- **Inputs**: [q_in, q_intermediate] (if available)
- **Outputs**: [h1, h2]
- **Coupling**: Moderate to strong depending on time constant ratio

Controller Tuning Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~~

For h2 control with q_in input:

- **Proportional gain**: Kc = 1/(K*(τ1 + τ2))
- **Integral time**: Ti = τ1 + τ2
- **Derivative time**: Td = τ1*τ2/(τ1 + τ2)

Industrial Applications
----------------------

Water Treatment
~~~~~~~~~~~~~

- Multi-stage clarifiers
- Sequential treatment tanks
- pH neutralization systems

Chemical Processing
~~~~~~~~~~~~~~~~~

- Reactor cascades
- Crystallization trains
- Separation sequences

Wastewater Treatment
~~~~~~~~~~~~~~~~~~

- Aeration basins
- Settling tank sequences
- Biological treatment stages

Advanced Topics
--------------

Optimal Design
~~~~~~~~~~~~~

- Tank sizing for desired dynamics
- Discharge coefficient selection
- Area ratio optimization

Nonlinear Control
~~~~~~~~~~~~~~~

- Feedback linearization
- Model predictive control
- Adaptive control strategies

References
----------

1. Seborg, D.E., Edgar, T.F., Mellichamp, D.A., & Doyle III, F.J. (2016). *Process Dynamics and Control* (4th ed.). Wiley.

2. Stephanopoulos, G. (1984). *Chemical Process Control: An Introduction to Theory and Practice*. Prentice Hall.

3. Astrom, K.J., & Hagglund, T. (2006). *Advanced PID Control*. ISA Press.

4. Luyben, W.L. (1990). *Process Modeling, Simulation, and Control for Chemical Engineers* (2nd ed.). McGraw-Hill.

5. Marlin, T.E. (2000). *Process Control: Designing Processes and Control Systems for Dynamic Performance* (2nd ed.). McGraw-Hill.

API Reference
------------

.. autoclass:: InteractingTanks
   :members:
   :undoc-members:
   :show-inheritance:
