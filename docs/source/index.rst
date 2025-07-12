.. SPROCLIB - Standard Process Control Library documentation master file

SPROCLIB - Standard Process Control Library
=========================================================

A Python library for process control in chemistry with semantic plant design and a modern modular architecture.

Created by: **Thorsten Gressling** (gressling@paramus.ai)

.. image:: https://img.shields.io/badge/Python-3.8%2B-blue
   :alt: Python Version

.. image:: https://img.shields.io/badge/License-MIT-green
   :alt: License

Overview
--------

SPROCLIB provides essential tools for process modeling, control design, optimization, and advanced control techniques used in chemical engineering. The library features a modern modular architecture with clean separation of concerns.

Quick Start
-----------

Installation::

    pip install sproclib

Usage::

      # Define plant
      plant = ChemicalPlant(name="Process Plant")

      # Add units
      plant.add(CentrifugalPump(H0=50.0, eta=0.75), name="feed_pump")
      plant.add(CSTR(V=150.0, k0=7.2e10), name="reactor")

      # Connect units
      plant.connect("feed_pump", "reactor", "feed_stream")

      # Configure optimization
      plant.compile(
         optimizer="economic",
         loss="total_cost",
         metrics=["profit", "conversion"]
      )

      # Optimize operations
      plant.optimize(target_production=1000.0)
Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   migration
   user_guide

.. toctree::
   :maxdepth: 2
   :caption: Tutorials and Examples

   tutorials
   case_studies
   best_practices

.. toctree::
   :maxdepth: 2
   :caption: Unit Operations

   unit/index

.. toctree::
   :maxdepth: 2
   :caption: Transport Systems

   transport/index

.. toctree::
   :maxdepth: 2
   :caption: Control Systems

   controller/index

.. toctree::
   :maxdepth: 2
   :caption: Semantic Plant Design

   plant/index

.. toctree::
   :maxdepth: 3
   :caption: Programming Interfaces (API)

   api/index
   api/units_package
   api/transport_package
   api/controllers_package
   api/analysis_package
   api/simulation_package
   api/optimization_package
   api/scheduling_package
   api/utilities_package

.. toctree::
   :maxdepth: 2
   :caption: Theory and Background

   theory
   mathematical_foundations
   control_theory
   process_modeling

.. toctree::
   :maxdepth: 1
   :caption: Developer Resources

   contributing
   development_guide
   testing
   documentation_guide

.. toctree::
   :maxdepth: 1
   :caption: Project Information

   changelog
   references
   license
   acknowledgments

Process Control Documentation
-----------------------------

The SPROCLIB Process Control API is organized into focused packages:

**Modern Modular Packages (Recommended):**

* **Analysis Package** - Transfer functions, system analysis, and model identification tools
* **Simulation Package** - Dynamic process simulation with control loop integration
* **Optimization Package** - Economic optimization, parameter estimation, and process optimization
* **Scheduling Package** - Batch process scheduling using State-Task Networks
* **Transport Package** - Fluid transport systems, pipeline modeling, and multiphase flow
* **Utilities Package** - Control design utilities, mathematical tools, and data processing
* **Units Package** - Physical process equipment (tanks, pumps, reactors, etc.)
* **Controllers Package** - Control algorithms and implementations

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

