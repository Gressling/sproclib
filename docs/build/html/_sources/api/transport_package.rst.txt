Transport (Pipes, Drums)Package
=================

The transport package provides comprehensive modeling capabilities for fluid and material transport
systems in process control applications. This package contains models for continuous and batch
transport operations across different phases and flow regimes.

.. note::
   This is part of the modern modular structure of SPROCLIB. The transport package includes
   advanced physics-based models for process engineering applications.

Package Structure
-----------------

The transport package is organized by operational mode and phase:

* **Continuous Transport** - Steady-state and dynamic transport operations
  
  * **Liquid Transport** - PipeFlow, PeristalticFlow, SlurryPipeline
  * **Solid Transport** - PneumaticConveying, ConveyorBelt, GravityChute, ScrewFeeder

* **Batch Transport** - Discrete material handling and transfer operations
  
  * **Liquid Transport** - BatchTransferPumping
  * **Solid Transport** - DrumBinTransfer, VacuumTransfer

All transport models inherit from the ProcessModel base class and provide both steady-state and dynamic analysis capabilities.

Continuous Liquid Transport
---------------------------

The continuous liquid transport module provides three specialized models for different
transport applications. These models are fully documented with examples and validation data.

.. toctree::
   :maxdepth: 2
   :caption: Liquid Transport Models:

   ../transport/continuous/liquid/index

Submodules
----------

Single-Phase Pipeline Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~

See detailed documentation: :doc:`../transport/continuous/liquid/PipeFlow`

The ``PipeFlow`` class implements comprehensive pipeline transport modeling for clean
liquids using the Darcy-Weisbach equation and friction factor correlations.

**Key Features:**

* Pressure drop calculations for laminar and turbulent flow
* Reynolds number analysis and flow regime identification  
* Temperature-dependent fluid properties
* Elevation change effects
* Multiple friction factor correlations

Positive Displacement Pumping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See detailed documentation: :doc:`../transport/continuous/liquid/PeristalticFlow`

The ``PeristalticFlow`` class models peristaltic pump systems for precise fluid
metering and chemical transfer applications.

**Key Features:**

* Precise flow rate control and prediction
* Pulsation analysis and damping effects
* Backpressure compensation
* Tube wear and occlusion modeling
* Chemical compatibility considerations

Multiphase Slurry Transport
~~~~~~~~~~~~~~~~~~~~~~~~~~~

See detailed documentation: :doc:`../transport/continuous/liquid/SlurryPipeline`

The ``SlurryPipeline`` class provides multiphase transport modeling for solid-liquid
slurry systems in mining, dredging, and industrial applications.

**Key Features:**

* Critical velocity prediction using Durand equation
* Particle settling and concentration effects
* Multiphase pressure drop calculations
* Operating envelope determination
* Concentration tracking

Continuous Solid Transport
---------------------------

The continuous solid transport module provides four specialized models for different
solid handling applications in process systems.

Pneumatic Conveying
~~~~~~~~~~~~~~~~~~~

The ``PneumaticConveying`` class models pneumatic transport systems for bulk solids
using air or gas as the carrier medium.

**Key Features:**

* Dilute and dense phase conveying analysis
* Pressure drop calculations for particle-gas flow
* Minimum transport velocity prediction
* Material degradation assessment
* Power consumption optimization

Conveyor Belt Systems
~~~~~~~~~~~~~~~~~~~~~

The ``ConveyorBelt`` class provides mechanical conveying analysis for continuous
solid transport using belt conveyors.

**Key Features:**

* Belt tension and power calculations
* Inclined conveyor analysis
* Material flow rate control
* Belt speed optimization
* Loading and discharge dynamics

Gravity Chute Transport
~~~~~~~~~~~~~~~~~~~~~~~

The ``GravityChute`` class models gravity-driven solid transport through chutes
and hoppers with flow control considerations.

**Key Features:**

* Flow rate prediction for bulk solids
* Angle of repose and flow characteristics
* Choking and bridging analysis
* Discharge control and flow regulation
* Particle size distribution effects

Screw Feeder Systems
~~~~~~~~~~~~~~~~~~~~

The ``ScrewFeeder`` class provides analysis for screw conveyors and feeders
used in controlled solid transport applications.

**Key Features:**

* Volumetric and gravimetric feeding control
* Screw geometry optimization
* Fill factor and efficiency analysis
* Power requirement calculations
* Material handling characteristics

Batch Transport Operations
--------------------------

The batch transport module provides models for discrete material transfer operations
commonly used in batch processing and discrete manufacturing.

Batch Liquid Transfer
~~~~~~~~~~~~~~~~~~~~~

The ``BatchTransferPumping`` class models batch liquid transfer operations including
pump-based transfer systems for precise volume control.

**Key Features:**

* Batch volume accuracy and control
* Transfer time optimization
* Pump priming and cavitation analysis
* Level control integration
* Contamination prevention strategies

Batch Solid Transfer
~~~~~~~~~~~~~~~~~~~~

**Drum and Bin Transfer**

The ``DrumBinTransfer`` class models solid transfer between containers including
drums, bins, and hoppers for batch operations.

**Key Features:**

* Discharge rate modeling
* Flow control and metering
* Container design optimization
* Material handling safety
* Batch accuracy and repeatability

**Vacuum Transfer Systems**

The ``VacuumTransfer`` class provides analysis for pneumatic vacuum transfer
of bulk solids in batch operations.

**Key Features:**

* Vacuum system design and sizing
* Material pickup and transport
* Filter system integration
* Energy efficiency optimization
* Dust control and containment

Analysis Functions
------------------

Steady-State Analysis
~~~~~~~~~~~~~~~~~~~~~

See detailed documentation: :doc:`../transport/continuous/liquid/steady_state`

Comprehensive steady-state analysis tools for equilibrium transport calculations.

Dynamic Analysis
~~~~~~~~~~~~~~~~

See detailed documentation: :doc:`../transport/continuous/liquid/dynamics`

Dynamic analysis capabilities for transient transport phenomena and control system design.

Quick Usage Examples
--------------------

Continuous Liquid Transport
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pipeline Flow Analysis::

    from transport.continuous.liquid import PipeFlow
    import numpy as np
    
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

Peristaltic Pump Control::

    from transport.continuous.liquid import PeristalticFlow
    
    # Create peristaltic pump model
    pump = PeristalticFlow(
        tube_diameter=0.01,      # 10 mm tube
        pump_speed=100,          # 100 RPM
        n_rollers=3,             # 3-roller head
        tube_length=0.5          # 50 cm tube
    )
    
    # Flow rate calculation
    result = pump.steady_state([101325, 100, 0.95])  # [P_in, speed, occlusion]
    flow_rate, pulsation = result

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

Continuous Solid Transport
~~~~~~~~~~~~~~~~~~~~~~~~~~

Pneumatic Conveying Analysis::

    from transport.continuous.solid import PneumaticConveying
    
    # Create pneumatic conveying model
    conveyor = PneumaticConveying(
        pipe_length=200.0,       # 200 m transport line
        pipe_diameter=0.15,      # 15 cm diameter
        particle_diameter=3e-3,  # 3 mm particles
        particle_density=1200.0, # Plastic pellets
        gas_density=1.2          # Air at standard conditions
    )
    
    # Minimum transport velocity
    result = conveyor.steady_state([150000, 15.0, 0.5])  # [P_in, v_gas, C_solid]
    P_out, v_min, power_required = result

Conveyor Belt Operations::

    from transport.continuous.solid import ConveyorBelt
    
    # Create belt conveyor model
    belt = ConveyorBelt(
        belt_length=100.0,       # 100 m conveyor
        belt_width=1.2,          # 1.2 m width
        inclination_angle=15.0,  # 15 degree incline
        material_density=800.0   # Bulk density
    )
    
    # Belt design analysis
    result = belt.steady_state([10.0, 2.0, 0.8])  # [capacity, speed, load_factor]
    tension, power, efficiency = result

Batch Transport Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    from transport.continuous.solid import ConveyorBelt
    from transport.batch.liquid import BatchTransferPumping
    
    # Multi-phase process with different transport mechanisms
    class IntegratedProcess:
        def __init__(self):
            # Liquid transport pipeline
            self.liquid_line = PipeFlow(pipe_length=500, pipe_diameter=0.2)
            
            # Solid handling conveyor
            self.solid_conveyor = ConveyorBelt(belt_length=200, belt_width=1.0)
            
            # Batch transfer system
            self.batch_transfer = BatchTransferPumping(tank_volume=5.0, transfer_volume=1.0)
        
        def process_cycle(self, liquid_flow, solid_rate, batch_volume):
            # Coordinate all transport operations
            liquid_result = self.liquid_line.steady_state([200000, 293.15, liquid_flow])
            solid_result = self.solid_conveyor.steady_state([solid_rate, 1.5, 0.9])
            batch_result = self.batch_transfer.steady_state([batch_volume, 101325, 293.15])
            
            return {
                'liquid_pressure_drop': liquid_result[0] - 200000,
                'solid_power_required': solid_result[1],
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

Optimization and Design
~~~~~~~~~~~~~~~~~~~~~~~

Multi-objective transport system optimization::

    from transport.continuous.solid import PneumaticConveying
    from optimization.parameter_estimation import optimize_design
    
    # Define multi-objective design problem
    def transport_optimization(params):
        pipe_diameter, gas_velocity, particle_loading = params
        
        # Create conveying system
        conveyor = PneumaticConveying(
            pipe_length=300, 
            pipe_diameter=pipe_diameter,
            particle_diameter=2e-3
        )
        
        result = conveyor.steady_state([180000, gas_velocity, particle_loading])
        
        # Multi-objective: minimize power, maximize capacity
        power_consumption = result[2]
        transport_capacity = particle_loading * gas_velocity * (pipe_diameter**2)
        
        return power_consumption / transport_capacity  # Power per unit capacity
    
    # Optimize system design
    optimal_design = optimize_design(
        transport_optimization,
        bounds=[(0.1, 0.4), (10.0, 30.0), (0.1, 2.0)],  # [diameter, velocity, loading]
        constraints={'min_transport_velocity': 15.0}
    )

See Also
--------

* :doc:`simulation_package` - Process simulation with transport models
* :doc:`optimization_package` - Transport system optimization  
* :doc:`utilities_package` - Control design utilities
* :doc:`../user_guide/examples/transport_examples` - Comprehensive usage examples
