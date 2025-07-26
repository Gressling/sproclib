Migration Guide
==============

Guide for migrating from older versions of SPROCLIB to the current modular architecture.

Overview
--------

This guide helps users migrate from previous versions of SPROCLIB to the new
modular architecture introduced in version 2.0+.

.. note::
   This migration guide is currently under development. Complete migration details
   will be available in a future release.

Breaking Changes
---------------

Key changes that may affect existing code:

* Reorganized package structure
* Updated API interfaces
* New naming conventions
* Deprecated legacy functions

Migration Steps
--------------

1. **Update Import Statements**
   
   .. code-block:: python
   
      # Old (deprecated)
      from sproclib.legacy import Tank
      
      # New (recommended)
      from sproclib.unit.tank import Tank

2. **Update Configuration Syntax**

   Details on new configuration options and syntax changes.

3. **Update Control System Integration**

   Changes to controller interfaces and integration patterns.

Compatibility Layer
------------------

The legacy package provides backward compatibility for most common use cases
during the transition period.

Getting Help
-----------

If you encounter issues during migration:

* Check the changelog for detailed changes
* Review updated examples in the documentation
* Contact support for specific migration questions
