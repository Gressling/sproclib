Continuous Stirred Tank Reactor (CSTR)
========================================

Overview
--------

The Continuous Stirred Tank Reactor (CSTR) model simulates a well-mixed reactor with continuous feed and discharge streams. The model incorporates Arrhenius reaction kinetics, material balance, energy balance, and heat transfer with jacket cooling. It is widely used in chemical process engineering for reactor design, control system development, and process optimization.

Theory and Equations
-------------------

Material Balance
~~~~~~~~~~~~~~~~

The material balance for a first-order reaction in a CSTR is:

.. math::

   \frac{dC_A}{dt} = \frac{q}{V}(C_{A,i} - C_A) - k(T) \cdot C_A

where:
- :math:`C_A` = concentration in reactor [mol/L]
- :math:`C_{A,i}` = inlet concentration [mol/L]  
- :math:`q` = volumetric flow rate [L/min]
- :math:`V` = reactor volume [L]
- :math:`k(T)` = temperature-dependent rate constant [1/min]

Energy Balance  
~~~~~~~~~~~~~~

The energy balance accounts for sensible heat, reaction heat, and jacket heat transfer:

.. math::

   \frac{dT}{dt} = \frac{q}{V}(T_i - T) + \frac{(-\Delta H_r) k(T) C_A}{\rho C_p} + \frac{UA(T_c - T)}{V \rho C_p}

where:
- :math:`T` = reactor temperature [K]
- :math:`T_i` = inlet temperature [K]
- :math:`T_c` = coolant temperature [K]
- :math:`\Delta H_r` = heat of reaction [J/mol]
- :math:`\rho` = density [g/L]
- :math:`C_p` = heat capacity [J/g/K]
- :math:`UA` = overall heat transfer coefficient [J/min/K]

Reaction Kinetics
~~~~~~~~~~~~~~~~~

The reaction rate follows the Arrhenius equation:

.. math::

   k(T) = k_0 \exp\left(\frac{-E_a}{RT}\right)

where:
- :math:`k_0` = pre-exponential factor [1/min]
- :math:`E_a` = activation energy [J/mol]
- :math:`R` = gas constant (8.314 J/mol/K)

Parameters
----------

Design Parameters
~~~~~~~~~~~~~~~~~

- **V**: Reactor volume [L]
  
  - Typical range: 10-10,000 L
  - Laboratory scale: 1-10 L
  - Industrial scale: 1,000-10,000 L

- **UA**: Heat transfer coefficient [J/min/K]
  
  - Typical range: 1,000-100,000 J/min/K
  - Depends on jacket design and heat transfer area

Kinetic Parameters
~~~~~~~~~~~~~~~~~~

- **k₀**: Pre-exponential factor [1/min]
  
  - Typical range: 10⁶-10¹² 1/min
  - Reaction-specific parameter

- **Eₐ**: Activation energy [J/mol]
  
  - Typical range: 40,000-100,000 J/mol
  - Higher values indicate stronger temperature dependence

Physical Properties
~~~~~~~~~~~~~~~~~~~

- **ρ**: Density [g/L]
  
  - Typical range: 800-1,200 g/L
  - Temperature-dependent (assumed constant)

- **Cₚ**: Heat capacity [J/g/K]
  
  - Typical range: 0.1-0.5 J/g/K  
  - Composition and temperature dependent

- **ΔHᵣ**: Heat of reaction [J/mol]
  
  - Exothermic reactions: negative values
  - Typical range: -100,000 to -10,000 J/mol

Operating Ranges
---------------

Safe Operating Window
~~~~~~~~~~~~~~~~~~~~

**Temperature Control:**

- Operating range: 250-600 K
- Optimal range: 300-500 K  
- Safety limit: <600 K to prevent thermal runaway

**Concentration Ranges:**

- Feed concentration: 0.1-10 mol/L
- Target conversion: 10-95%
- Maximum concentration: <100 mol/L

**Flow Rate Ranges:**

- Minimum: 0.1 L/min (continuous operation)
- Maximum: 1,000 L/min (mixing limitations)
- Optimal: 1-100 L/min for most applications

Usage Example
-------------

Basic Implementation
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from unit.reactor.cstr import CSTR
   import numpy as np
   
   # Create CSTR instance
   reactor = CSTR(
       V=100.0,           # Reactor volume [L]
       k0=7.2e10,         # Pre-exponential factor [1/min]
       Ea=72750.0,        # Activation energy [J/mol]
       dHr=-50000.0,      # Heat of reaction [J/mol]
       UA=50000.0         # Heat transfer coefficient [J/min/K]
   )
   
   # Define operating conditions
   u = np.array([10.0, 1.0, 350.0, 300.0])  # [q, CAi, Ti, Tc]
   
   # Calculate steady state
   x_ss = reactor.steady_state(u)
   print(f"Steady-state concentration: {x_ss[0]:.4f} mol/L")
   print(f"Steady-state temperature: {x_ss[1]:.2f} K")

Dynamic Simulation
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from scipy.integrate import solve_ivp
   
   # Initial conditions
   x0 = np.array([1.0, 350.0])  # [CA0, T0]
   
   # Time span
   t_span = (0, 60)  # 0 to 60 minutes
   t_eval = np.linspace(0, 60, 300)
   
   # Solve ODE
   def cstr_ode(t, x):
       return reactor.dynamics(t, x, u)
   
   sol = solve_ivp(cstr_ode, t_span, x0, t_eval=t_eval, method='RK45')

Example Output
--------------

Running the complete example produces the following results:

.. code-block:: text

   ============================================================
   CSTR (Continuous Stirred Tank Reactor) Example
   ============================================================
   Reactor: Example_CSTR
   Volume: 100.0 L
   Heat transfer coefficient: 50000.0 J/min/K

   Operating Conditions:
     q: 10.0 L/min
     CAi: 1.0 mol/L
     Ti: 350.0 K
     Tc: 300.0 K

   Steady State Analysis:
   ------------------------------
   Steady-state concentration: 0.8140 mol/L
   Steady-state temperature: 304.06 K
   Conversion: 18.6%
   Residence time: 10.00 min
   Reaction rate constant: 2.29e-02 1/min
   Heat generation: 93014 J/min
   Productivity: 8.140 mol/min

   Dynamic Simulation:
   ------------------------------
   Dynamic simulation completed successfully
   Final concentration: 0.8135 mol/L
   Final temperature: 304.06 K
   Final conversion: 18.6%
   Time to 95% of steady state: 24.7 min

   Step Response Analysis:
   ------------------------------
   Temperature change after step: -66.54 K
   Concentration change after step: -0.0276 mol/L

Performance Plots
----------------

The example generates two visualization files:

**Dynamic Response (cstr_example_plots.png)**

.. image:: cstr_example_plots.png
   :width: 600px
   :align: center
   :alt: CSTR dynamic response plots

Shows concentration, temperature, conversion, and phase portrait during startup.

**Step Response Analysis (cstr_detailed_analysis.png)**

.. image:: cstr_detailed_analysis.png  
   :width: 500px
   :align: center
   :alt: CSTR step response analysis

Shows reactor response to coolant temperature step change.

Applications
-----------

The CSTR model is applicable for:

- **Process Design**: Reactor sizing and configuration
- **Control System Design**: Controller tuning and testing  
- **Process Optimization**: Operating condition optimization
- **Safety Analysis**: Thermal runaway and stability analysis
- **Educational Purposes**: Teaching reaction engineering concepts

Limitations
-----------

Model assumptions and limitations:

- **Perfect Mixing**: Assumes instantaneous mixing throughout reactor
- **Single Reaction**: Limited to first-order reaction kinetics
- **Constant Properties**: Physical properties assumed temperature-independent
- **No Mass Transfer**: Ignores mass transfer limitations
- **Ideal Behavior**: No catalyst deactivation or side reactions

Literature References
--------------------

1. Fogler, H.S. (2016). *Elements of Chemical Reaction Engineering*, 5th Edition, Prentice Hall.

2. Levenspiel, O. (1999). *Chemical Reaction Engineering*, 3rd Edition, John Wiley & Sons.

3. Rawlings, J.B. and Ekerdt, J.G. (2002). *Chemical Reactor Analysis and Design Fundamentals*, Nob Hill Publishing.

4. Schmidt, L.D. (2005). *The Engineering of Chemical Reactions*, 2nd Edition, Oxford University Press.

5. Davis, M.E. and Davis, R.J. (2003). *Fundamentals of Chemical Reaction Engineering*, McGraw-Hill.

See Also
--------

- :doc:`batch_reactor` - Batch reactor model
- :doc:`plug_flow_reactor` - Plug flow reactor model  
- :doc:`fixed_bed_reactor` - Fixed bed catalytic reactor model
