Transport Package
=================

The transport package provides comprehensive modeling capabilities for fluid and material transport
systems in process control applications. This package contains models for continuous and batch
transport operations across different phases and flow regimes.

.. note::
   This is part of the modern modular structure of SPROCLIB. The transport package includes
   advanced physics-based models for process engineering applications.

.. toctree::
   :maxdepth: 2
   :caption: Transport Operations:

   ../transport/continuous/index
   ../transport/batch/index

Package Overview
----------------

The transport package is organized by operational mode and provides comprehensive modeling for:

**Continuous Transport Operations**:

* **Liquid Transport** - PipeFlow, PeristalticFlow, SlurryPipeline
* **Solid Transport** - PneumaticConveying, ConveyorBelt, GravityChute, ScrewFeeder

**Batch Transport Operations**:

* **Liquid Transfer** - BatchTransferPumping
* **Solid Handling** - DrumBinTransfer, VacuumTransfer

All transport models inherit from the ProcessModel base class and provide both steady-state and dynamic analysis capabilities for comprehensive system characterization.

Transport
---------

Continuous Liquid Transport
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   ../transport/continuous/liquid/PipeFlow
   ../transport/continuous/liquid/PeristalticFlow
   ../transport/continuous/liquid/SlurryPipeline

Continuous Solid Transport
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   ../transport/continuous/solid/PneumaticConveying
   ../transport/continuous/solid/ConveyorBelt
   ../transport/continuous/solid/GravityChute
   ../transport/continuous/solid/ScrewFeeder

Batch Liquid Transport
~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   ../transport/batch/liquid/BatchTransferPumping

Batch Solid Transport
~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   ../transport/batch/solid/DrumBinTransfer
   ../transport/batch/solid/VacuumTransfer

Analysis Functions
~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   ../transport/continuous/liquid/steady_state
   ../transport/continuous/liquid/dynamics

Detailed Model Documentation
----------------------------

Single-Phase Pipeline Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~

See detailed documentation: :doc:`../transport/continuous/liquid/PipeFlow`

The ``PipeFlow`` class implements comprehensive pipeline transport modeling for clean
liquids using the Darcy-Weisbach equation and friction factor correlations. Features include
pressure drop calculations, Reynolds number analysis, temperature-dependent properties, and
multiple friction factor correlations.

Positive Displacement Pumping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See detailed documentation: :doc:`../transport/continuous/liquid/PeristalticFlow`

The ``PeristalticFlow`` class models peristaltic pump systems for precise fluid metering and
chemical transfer applications. Features include precise flow control, pulsation analysis,
backpressure compensation, and tube wear modeling.

Multiphase Slurry Transport
~~~~~~~~~~~~~~~~~~~~~~~~~~~

See detailed documentation: :doc:`../transport/continuous/liquid/SlurryPipeline`

The ``SlurryPipeline`` class provides multiphase transport modeling for solid-liquid slurry
systems. Features include critical velocity prediction, particle settling effects, multiphase
pressure drop calculations, and operating envelope determination.

Batch Liquid Transfer
~~~~~~~~~~~~~~~~~~~~~

See detailed documentation: :doc:`../transport/batch/liquid/BatchTransferPumping`

The ``BatchTransferPumping`` class models batch liquid transfer operations using pumps with
comprehensive hydraulic analysis. Features include batch volume control, transfer time
optimization, pump performance integration, and level control capabilities.

Quick Usage Examples
--------------------

Continuous Transport
~~~~~~~~~~~~~~~~~~~~

Pipeline Flow Analysis::

    from transport.continuous.liquid import PipeFlow
    
    # Create pipeline model
    pipe = PipeFlow(
        pipe_length=1000.0,      # 1 km pipeline
        pipe_diameter=0.2,       # 20 cm diameter
        roughness=1e-4,          # Commercial steel
        elevation_change=50.0    # 50 m elevation gain
    )
    
    # Steady-state analysis
    result = pipe.steady_state([300000, 293.15, 0.05])  # [P_in, T_in, Q]
    P_out, T_out = result

Slurry Transport Design::

    from transport.continuous.liquid import SlurryPipeline
    
    # Create slurry pipeline model
    slurry = SlurryPipeline(
        pipe_length=5000.0,      # 5 km pipeline
        pipe_diameter=0.3,       # 30 cm diameter
        particle_diameter=0.001, # 1 mm particles
        solid_density=2650.0,    # Sand particles
        fluid_density=1000.0     # Water carrier
    )
    
    # Critical velocity analysis
    result = slurry.steady_state([400000, 0.15, 2.5])  # [P_in, C_in, v]
    P_out, C_out, v_critical = result

Batch Transport
~~~~~~~~~~~~~~~

Batch Liquid Transfer::

    from transport.batch.liquid import BatchTransferPumping
    
    # Create batch transfer model
    transfer = BatchTransferPumping(
        tank_volume=2.0,         # 2 m³ source tank
        transfer_volume=0.5,     # 500 L batch size
        pump_capacity=0.01,      # 10 L/s pump
        pipe_length=50.0         # 50 m transfer line
    )
    
    # Batch transfer analysis
    result = transfer.steady_state([0.5, 101325, 293.15])  # [volume, pressure, temp]
    transfer_time, accuracy, residual_volume = result

Batch Solid Transfer::

    from transport.batch.solid import DrumBinTransfer
    
    # Create drum transfer model
    drum_transfer = DrumBinTransfer(
        drum_capacity=0.2,       # 200 L drum
        discharge_diameter=0.1,  # 10 cm outlet
        material_density=1200.0, # Bulk density
        angle_of_repose=35.0     # Material flow property
    )
    
    # Discharge analysis
    result = drum_transfer.steady_state([0.15, 0.8, 9.81])  # [fill_level, valve_opening, gravity]
    discharge_rate, empty_time, flow_pattern = result

Advanced Applications
---------------------

Integrated Transport Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Combining multiple transport models for complex process systems::

    from transport.continuous.liquid import PipeFlow
    from transport.batch.liquid import BatchTransferPumping
    
    # Multi-phase process with different transport mechanisms
    class IntegratedProcess:
        def __init__(self):
            # Continuous liquid transport
            self.liquid_line = PipeFlow(pipe_length=500, pipe_diameter=0.2)
            
            # Batch transfer system
            self.batch_transfer = BatchTransferPumping(tank_volume=5.0, transfer_volume=1.0)
        
        def process_cycle(self, liquid_flow, batch_volume):
            # Coordinate transport operations
            liquid_result = self.liquid_line.steady_state([200000, 293.15, liquid_flow])
            batch_result = self.batch_transfer.steady_state([batch_volume, 101325, 293.15])
            
            return {
                'liquid_pressure_drop': liquid_result[0] - 200000,
                'batch_transfer_time': batch_result[0]
            }

Process Control Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Transport models with control system design::

    from transport.continuous.liquid import PipeFlow
    from utilities.control_utils import tune_pid
    from simulation.process_simulation import ProcessSimulation
    
    # Create controlled transport process
    pipeline = PipeFlow(pipe_length=2000, pipe_diameter=0.25)
    
    # Design flow controller
    process_params = {'K': 1e-6, 'tau': 30.0, 'theta': 5.0}
    pid_params = tune_pid(process_params, method='ziegler_nichols')
    
    # Run closed-loop simulation
    sim = ProcessSimulation(pipeline, controller_params=pid_params)
    results = sim.run(time_span=3600)

See Also
--------

* :doc:`../transport/index` - Complete transport module documentation
* :doc:`simulation_package` - Process simulation with transport models
* :doc:`optimization_package` - Transport system optimization  
* :doc:`utilities_package` - Control design utilities
* :doc:`../user_guide/examples/transport_examples` - Comprehensive usage examples
