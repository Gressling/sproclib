CSTR describe() Method Documentation
=====================================

Overview
--------

The ``describe()`` method is a core introspection feature of the CSTR (Continuous Stirred Tank Reactor) class that provides comprehensive metadata about the reactor model. This method returns a structured dictionary containing all essential information about the reactor's algorithms, parameters, variables, operating ranges, and limitations.

Method Signature
----------------

.. code-block:: python

   def describe(self) -> dict

Purpose and Usage
-----------------

The ``describe()`` method serves multiple purposes:

* **Model Documentation**: Provides self-documenting capability for the reactor model
* **Algorithm Discovery**: Lists all implemented algorithms and equations
* **Parameter Inspection**: Shows current parameter values with units and descriptions
* **Validation Support**: Provides valid operating ranges for safety and optimization
* **Educational Tool**: Offers comprehensive information for learning and teaching

Basic Usage Examples
--------------------

**Example 1: Using with Plant Instance**

.. code-block:: python

   from sproclib.unit.plant import ChemicalPlant
   from sproclib.unit.reactor.cstr import CSTR
   
   # Create plant and add CSTR
   plant = ChemicalPlant(name="Process Plant")
   plant.add(CSTR(V=150.0, k0=7.2e10), name="reactor")
   
   # Get reactor instance from plant and describe
   reactor_instance = plant.units[1]  # CSTR is the second unit
   metadata = reactor_instance.describe()

**Example 2: Using with Direct Instance**

.. code-block:: python

   from sproclib.unit.reactor.cstr import CSTR
   
   # Create CSTR instance with default parameters
   reactor = CSTR()
   metadata = reactor.describe()

Return Value Structure
----------------------

The ``describe()`` method returns a dictionary with the following structure:

Basic Information
~~~~~~~~~~~~~~~~~

.. code-block:: python

   {
       'type': 'CSTR',
       'description': 'Continuous Stirred Tank Reactor with Arrhenius kinetics and energy balance',
       'category': 'reactor'
   }

**Fields:**

* ``type``: Model type identifier
* ``description``: Human-readable description of the reactor model
* ``category``: Classification category (always 'reactor' for CSTR)

Algorithms
~~~~~~~~~~

.. code-block:: python

   'algorithms': {
       'reaction_kinetics': 'Arrhenius equation: k = k0 * exp(-Ea/RT)',
       'material_balance': 'dCA/dt = q/V*(CAi - CA) - k(T)*CA',
       'energy_balance': 'dT/dt = q/V*(Ti - T) + (-dHr)*k(T)*CA/(rho*Cp) + UA*(Tc - T)/(V*rho*Cp)',
       'steady_state': 'Numerical solution using scipy.optimize.fsolve'
   }

**Mathematical Models Implemented:**

* **Reaction Kinetics**: Arrhenius temperature dependence
* **Material Balance**: Component mass balance with reaction consumption
* **Energy Balance**: Temperature dynamics with reaction heat and cooling
* **Steady State**: Numerical solution for equilibrium conditions

Parameters
~~~~~~~~~~

.. code-block:: python

   'parameters': {
       'V': {'value': 100.0, 'units': 'L', 'description': 'Reactor volume'},
       'k0': {'value': 7.2e10, 'units': '1/min', 'description': 'Arrhenius pre-exponential factor'},
       'Ea': {'value': 72750.0, 'units': 'J/gmol', 'description': 'Activation energy'},
       'R': {'value': 8.314, 'units': 'J/gmol/K', 'description': 'Gas constant'},
       'rho': {'value': 1000.0, 'units': 'g/L', 'description': 'Density'},
       'Cp': {'value': 0.239, 'units': 'J/g/K', 'description': 'Heat capacity'},
       'dHr': {'value': -50000.0, 'units': 'J/gmol', 'description': 'Heat of reaction'},
       'UA': {'value': 50000.0, 'units': 'J/min/K', 'description': 'Heat transfer coefficient'}
   }

**Parameter Categories:**

* **Reactor Design**: Volume (V)
* **Kinetic Parameters**: Pre-exponential factor (k0), Activation energy (Ea)
* **Physical Properties**: Density (rho), Heat capacity (Cp)
* **Thermodynamic**: Heat of reaction (dHr), Gas constant (R)
* **Heat Transfer**: Overall heat transfer coefficient (UA)

State Variables
~~~~~~~~~~~~~~~

.. code-block:: python

   'state_variables': {
       'CA': 'Concentration [mol/L]',
       'T': 'Temperature [K]'
   }

**State Variables:**

* **CA**: Reactant concentration in the reactor
* **T**: Reactor temperature

Input Variables
~~~~~~~~~~~~~~~

.. code-block:: python

   'inputs': {
       'q': 'Flow rate [L/min]',
       'CAi': 'Inlet concentration [mol/L]',
       'Ti': 'Inlet temperature [K]',
       'Tc': 'Coolant temperature [K]'
   }

**Input Variables:**

* **q**: Volumetric flow rate through the reactor
* **CAi**: Concentration of reactant in the feed stream
* **Ti**: Temperature of the incoming feed stream
* **Tc**: Coolant temperature for heat removal

Output Variables
~~~~~~~~~~~~~~~~

.. code-block:: python

   'outputs': {
       'CA': 'Outlet concentration [mol/L]',
       'T': 'Outlet temperature [K]',
       'reaction_rate': 'Reaction rate [mol/L/min]',
       'heat_generation': 'Heat generation [J/min]'
   }

**Output Variables:**

* **CA**: Outlet concentration (same as state variable)
* **T**: Outlet temperature (same as state variable)
* **reaction_rate**: Current reaction rate
* **heat_generation**: Heat generated by the reaction

Valid Operating Ranges
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   'valid_ranges': {
       'V': {'min': 1.0, 'max': 10000.0, 'units': 'L'},
       'T': {'min': 250.0, 'max': 600.0, 'units': 'K'},
       'CA': {'min': 0.0, 'max': 100.0, 'units': 'mol/L'},
       'q': {'min': 0.1, 'max': 1000.0, 'units': 'L/min'}
   }

**Safety and Operational Limits:**

* **Volume**: 1-10,000 L (laboratory to industrial scale)
* **Temperature**: 250-600 K (to prevent degradation)
* **Concentration**: 0-100 mol/L (physical constraints)
* **Flow Rate**: 0.1-1000 L/min (mixing and operational limits)

Applications
~~~~~~~~~~~~

.. code-block:: python

   'applications': [
       'Chemical reaction engineering',
       'Process control design',
       'Reactor optimization',
       'Safety analysis'
   ]

**Typical Use Cases:**

* **Chemical Reaction Engineering**: Reactor design and analysis
* **Process Control Design**: Controller development and tuning
* **Reactor Optimization**: Operating condition optimization
* **Safety Analysis**: Risk assessment and safety system design

Model Limitations
~~~~~~~~~~~~~~~~~

.. code-block:: python

   'limitations': [
       'Perfect mixing assumption',
       'Single reaction assumed',
       'Constant physical properties',
       'No mass transfer limitations'
   ]

**Model Assumptions and Constraints:**

* **Perfect Mixing**: Uniform concentration and temperature throughout reactor
* **Single Reaction**: Only one chemical reaction considered
* **Constant Properties**: Physical properties don't vary with composition/temperature
* **No Mass Transfer**: Reaction kinetics not limited by mass transfer

Parameter Differences Between Instances
---------------------------------------

The ``describe()`` method shows the actual parameter values for the specific reactor instance. Different instances will have different parameter values:

**Plant Instance (V=150.0 L)**:

.. code-block:: python

   # From plant reactor with custom volume
   reactor_instance = plant.units[1]  # V=150.0 L
   metadata = reactor_instance.describe()
   print(metadata['parameters']['V'])  # {'value': 150.0, 'units': 'L', ...}

**Default Instance (V=100.0 L)**:

.. code-block:: python

   # Default CSTR instance
   basic_cstr = CSTR()  # V=100.0 L (default)
   metadata = basic_cstr.describe()
   print(metadata['parameters']['V'])  # {'value': 100.0, 'units': 'L', ...}

Practical Applications
----------------------

**1. Model Validation**

.. code-block:: python

   # Check if reactor parameters are within valid ranges
   metadata = reactor.describe()
   V_current = metadata['parameters']['V']['value']
   V_range = metadata['valid_ranges']['V']
   
   if V_range['min'] <= V_current <= V_range['max']:
       print("Reactor volume within valid range")

**2. Algorithm Discovery**

.. code-block:: python

   # Find available algorithms
   metadata = reactor.describe()
   print("Available algorithms:")
   for name, equation in metadata['algorithms'].items():
       print(f"  {name}: {equation}")

**3. Documentation Generation**

.. code-block:: python

   # Generate parameter table for documentation
   metadata = reactor.describe()
   print("| Parameter | Value | Units | Description |")
   print("|-----------|-------|-------|-------------|")
   for param, info in metadata['parameters'].items():
       print(f"| {param} | {info['value']} | {info['units']} | {info['description']} |")

**4. Model Comparison**

.. code-block:: python

   # Compare two reactor configurations
   reactor1 = CSTR(V=100.0)
   reactor2 = CSTR(V=200.0)
   
   meta1 = reactor1.describe()
   meta2 = reactor2.describe()
   
   print(f"Reactor 1 volume: {meta1['parameters']['V']['value']} L")
   print(f"Reactor 2 volume: {meta2['parameters']['V']['value']} L")

Integration with SProcLib
-------------------------

The ``describe()`` method is part of SProcLib's introspection and self-documentation framework. It enables:

* **Dynamic Documentation**: Models can document themselves
* **Interactive Exploration**: Users can discover model capabilities programmatically
* **Validation Support**: Operating ranges help prevent invalid configurations
* **Educational Use**: Comprehensive information for learning chemical engineering

See Also
--------

* :doc:`cstr` - Complete CSTR documentation
* :doc:`../plant` - Chemical plant integration
* :doc:`../optimization` - Optimization with CSTR models
* :doc:`../examples/cstr_examples` - CSTR usage examples

Notes
-----

.. note::
   The ``describe()`` method is an instance method that requires a CSTR object to be created first. The returned parameter values reflect the specific configuration of that instance.

.. warning::
   Always validate parameter values against the ``valid_ranges`` before using the reactor in simulations to ensure safe and realistic operating conditions.

.. tip::
   Use the ``describe()`` method during model development to verify that your reactor configuration matches your design intentions.
