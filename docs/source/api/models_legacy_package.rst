Models Legacy Package (Deprecated)
===================================

.. warning::
   This documentation refers to the legacy monolithic models.py module.
   
   **Please use the new modular unit structure instead:**
   
   * :doc:`units_package` - Complete documentation for all process units
   * :doc:`../examples` - Comprehensive examples for all units
   
   The legacy models.py module is maintained for backward compatibility only.

Migration Guide
---------------

The classes from the legacy models.py module have been refactored into the modular unit structure:

**Legacy Location** → **New Location**

* ``models.ProcessModel`` → ``unit.base.ProcessModel``
* ``models.Tank`` → ``unit.tank.Tank``
* ``models.InteractingTanks`` → ``unit.tank.InteractingTanks``
* ``models.CSTR`` → ``unit.reactor.cstr.CSTR``
* ``models.PlugFlowReactor`` → ``unit.reactor.PlugFlowReactor``
* ``models.BatchReactor`` → ``unit.reactor.BatchReactor``
* ``models.SemiBatchReactor`` → ``unit.reactor.SemiBatchReactor``
* ``models.FixedBedReactor`` → ``unit.reactor.FixedBedReactor``
* ``models.HeatExchanger`` → ``unit.heat_exchanger.HeatExchanger``
* ``models.DistillationTray`` → ``unit.distillation.tray.DistillationTray``
* ``models.BinaryDistillationColumn`` → ``unit.distillation.column.BinaryDistillationColumn``
* ``models.ControlValve`` → ``unit.valve.ControlValve``
* ``models.ThreeWayValve`` → ``unit.valve.ThreeWayValve``
* ``models.LinearApproximation`` → ``unit.utilities.LinearApproximation``

Benefits of New Structure
~~~~~~~~~~~~~~~~~~~~~~~~~

* **Better Organization**: Classes grouped by unit type
* **Easier Maintenance**: Each class in its own file
* **Enhanced Discoverability**: Clear import paths
* **Comprehensive Examples**: Each unit has dedicated examples
* **Future-Proof**: Modular design supports easy extension

Quick Migration Example
~~~~~~~~~~~~~~~~~~~~~~~~

**Old (Deprecated):**

.. code-block:: python

   from models import Tank, CSTR, LinearApproximation

**New (Recommended):**

.. code-block:: python

   from unit.tank.Tank import Tank
   from unit.reactor.cstr import CSTR
   from unit.utilities.LinearApproximation import LinearApproximation

For complete documentation of all available units, see :doc:`units_package`.

Example Usage::

    from models import Tank
    
    # Create tank model
    tank = Tank(A=1.0, C=2.0, name="Storage Tank")
    
    # Find steady-state height for given inlet flow
    steady_state = tank.steady_state({'q_in': 4.0})
    print(f"Steady-state height: {steady_state['h']:.2f} m")
    
    # Calculate dynamics at current state
    state = [2.0]  # height = 2.0 m
    inputs = [3.0]  # q_in = 3.0 L/min
    dhdt = tank.dynamics(0, state, inputs)

CSTR
~~~~

.. autoclass:: models.CSTR
   :members:
   :special-members: __init__
   :show-inheritance:

Models a Continuous Stirred Tank Reactor with Arrhenius kinetics.

**Physical Model:**

The CSTR is described by material and energy balances:

.. math::
   V \\frac{dC_A}{dt} = q(C_{A,in} - C_A) - Vk_0 e^{-E/RT} C_A

.. math::
   V\\rho C_p \\frac{dT}{dt} = q\\rho C_p(T_{in} - T) + (-\\Delta H_r)Vk_0 e^{-E/RT} C_A + UA(T_{cool} - T)

Where:
- :math:`C_A` = Reactant concentration (mol/L)
- :math:`T` = Temperature (K)
- :math:`k_0` = Pre-exponential factor (1/min)
- :math:`E` = Activation energy (K)
- :math:`\\Delta H_r` = Heat of reaction (J/mol)

Example Usage::

    from models import CSTR
    
    # Create CSTR model
    cstr = CSTR(
        V=100,      # Volume (L)
        k0=1e10,    # Pre-exponential factor
        E=8000,     # Activation energy (K)
        dHr=-50000, # Heat of reaction (J/mol)
        rho=1000,   # Density (g/L)
        Cp=4.18,    # Heat capacity (J/g/K)
        name="Main Reactor"
    )
    
    # Operating conditions
    conditions = {
        'q_in': 10.0,
        'CA_in': 1.0,
        'T_in': 300.0,
        'T_cool': 290.0
    }
    
    # Find steady state
    ss = cstr.steady_state(conditions)

InteractingTanks
~~~~~~~~~~~~~~~~

.. autoclass:: models.InteractingTanks
   :members:
   :special-members: __init__
   :show-inheritance:

Models a system of two interacting tanks in series.

**Physical Model:**

Two tanks connected in series with the outlet of tank 1 feeding tank 2:

.. math::
   A_1 \\frac{dh_1}{dt} = q_{in} - C_1\\sqrt{h_1}

.. math::
   A_2 \\frac{dh_2}{dt} = C_1\\sqrt{h_1} - C_2\\sqrt{h_2}

This creates a second-order system useful for studying more complex dynamics.

LinearApproximation
~~~~~~~~~~~~~~~~~~~

.. autoclass:: models.LinearApproximation
   :members:
   :special-members: __init__
   :show-inheritance:

Provides linearization capabilities for nonlinear process models.

**Mathematical Background:**

For a nonlinear system :math:`\\dot{x} = f(x,u)`, the linear approximation around operating point :math:`(x_0, u_0)` is:

.. math::
   \\Delta\\dot{x} = A\\Delta x + B\\Delta u

Where:

.. math::
   A = \\left.\\frac{\\partial f}{\\partial x}\\right|_{x_0,u_0}, \\quad B = \\left.\\frac{\\partial f}{\\partial u}\\right|_{x_0,u_0}

Example Usage::

    from models import Tank, LinearApproximation
    
    # Create nonlinear tank model
    tank = Tank(A=1.0, C=2.0)
    
    # Create linearization tool
    linear_approx = LinearApproximation(tank)
    
    # Linearize around operating point
    u_nominal = [2.0]  # q_in = 2.0 L/min
    A, B = linear_approx.linearize(u_nominal)
    
    print(f"Linear model: A = {A[0,0]:.3f}, B = {B[0,0]:.3f}")

Methods
-------

Common Methods
~~~~~~~~~~~~~~

All process models implement these methods:

.. automethod:: models.ProcessModel.dynamics
.. automethod:: models.ProcessModel.steady_state  
.. automethod:: models.ProcessModel.linearize

Tank-Specific Methods
~~~~~~~~~~~~~~~~~~~~~

.. automethod:: models.Tank.steady_state_height
.. automethod:: models.Tank.time_constant

CSTR-Specific Methods  
~~~~~~~~~~~~~~~~~~~~~

.. automethod:: models.CSTR.reaction_rate
.. automethod:: models.CSTR.heat_generation

Design Guidelines
-----------------

Model Selection
~~~~~~~~~~~~~~~

Choose the appropriate model based on your application:

* **Tank** - Level control, simple dynamics
* **CSTR** - Temperature/concentration control, chemical reactions
* **InteractingTanks** - More complex dynamics, cascade control
* **Custom Models** - Inherit from ProcessModel for specialized applications

Parameterization
~~~~~~~~~~~~~~~~

Properly parameterize models:

1. **Physical Parameters** - Use realistic values from equipment specifications
2. **Operating Conditions** - Choose nominal conditions representative of normal operation  
3. **Validation** - Compare model predictions with plant data

Linearization Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~

When using linearization:

1. **Operating Point** - Choose steady-state conditions for linearization
2. **Validity Range** - Linear models are only valid near the operating point
3. **Model Order** - Higher-order models may be needed for wide operating ranges

Performance Tips
----------------

* Cache steady-state calculations for repeated use
* Use appropriate integrator settings for stiff systems (CSTR)
* Validate model parameters against plant data
* Consider model complexity vs. accuracy trade-offs

See Also
--------

* :doc:`controllers_legacy_package` - Controllers for these process models
* :doc:`analysis_legacy_package` - Analysis tools for model validation
* :doc:`../theory` - Mathematical background on process modeling
