Semi-Batch Reactor
==================

Overview
--------

The Semi-Batch Reactor model combines batch and continuous operation with controlled feeding strategies. It is used for fed-batch processes, controlled polymerization, and crystallization where precise control of reactant addition is critical for product quality and safety.

Theory and Equations
-------------------

Material Balance
~~~~~~~~~~~~~~~~

.. math::

   \frac{dn_A}{dt} = F_{in} C_{A,in} - k(T) C_A V

Volume Balance
~~~~~~~~~~~~~~

.. math::

   \frac{dV}{dt} = F_{in}

Energy Balance
~~~~~~~~~~~~~~

.. math::

   \frac{dT}{dt} = \frac{F_{in} \rho c_p (T_{in} - T) + (-\Delta H_r) k(T) C_A V + UA(T_j - T)}{\rho c_p V}

Concentration
~~~~~~~~~~~~~

.. math::

   C_A = \frac{n_A}{V}

Key Features
-----------

- Fed-batch operation with variable volume
- Controlled addition of reactants
- Temperature and concentration control
- Optimal feeding strategies
- Safety analysis for runaway prevention

Usage Example
-------------

.. code-block:: python

   from unit.reactor.SemiBatchReactor import SemiBatchReactor
   
   # Create Semi-Batch Reactor instance
   reactor = SemiBatchReactor(
       V_max=200.0,         # Maximum volume [L]
       k0=7.2e10,          # Pre-exponential factor [1/min]
       Ea=72750.0          # Activation energy [J/mol]
   )

Example Output
--------------

.. code-block:: text

   Semi-Batch Reactor Example
   ==================================================
   Reactor: Fed-Batch Reactor
   Maximum Volume: 200.0 L
   Activation Energy: 72.8 kJ/mol
   Heat of Reaction: -52.0 kJ/mol

   Initial Conditions:
   Initial moles: 20.0 mol
   Initial temperature: 300.0 K
   Initial volume: 50.0 L
   Initial concentration: 0.40 mol/L

   Final Results:
   Time: 120.0 min
   Moles: 22.62 mol
   Temperature: 306.0 K
   Volume: 125.0 L
   Concentration: 0.181 mol/L
   Conversion: -13.1%

Performance Plots
----------------

**Dynamic Response (semi_batch_reactor_example_plots.png)**

.. image:: semi_batch_reactor_example_plots.png
   :width: 600px
   :align: center
   :alt: Semi-batch reactor dynamics and feeding strategies

**Detailed Analysis (semi_batch_reactor_detailed_analysis.png)**

.. image:: semi_batch_reactor_detailed_analysis.png
   :width: 600px
   :align: center
   :alt: Semi-batch reactor control strategies

Applications
-----------

- Fine chemical manufacturing
- Controlled polymerization
- Crystallization processes
- Biochemical fermentation
- Pharmaceutical synthesis

See Also
--------

- :doc:`batch_reactor` - Batch reactor model
- :doc:`cstr` - Continuous stirred tank reactor
