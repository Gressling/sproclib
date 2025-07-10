DrumBinTransfer
================

.. automodule:: sproclib.transport.batch.solid.DrumBinTransfer
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The DrumBinTransfer class models batch solid material transfer operations using drums or bins with conveyor-based discharge systems. This model is commonly used in pharmaceutical, food, and chemical processing industries for transferring powders, granules, and other solid materials between process units.

Use Case
--------

The drum/bin transfer system is employed when:

* Batch processing requires controlled material handling
* Materials need to be transferred between different elevation levels
* Dust containment is important
* Process requires intermediate storage capacity
* Materials have varying flowability characteristics

Mathematical Model
------------------

Steady-State Model
~~~~~~~~~~~~~~~~~~

The steady-state calculation determines the actual transfer rate and batch completion time based on:

1. **Available Material Mass**: Calculated from container fill level and material density
2. **Effective Discharge Rate**: Considers flowability factor and discharge efficiency
3. **Transfer Rate Limiting**: Accounts for material availability and discharge capacity
4. **Batch Time Calculation**: Includes discharge, transport, and handling times

Key equations:

.. math::

   \text{flowability\_factor} = 0.5 + 0.5 \times \text{flowability}

.. math::

   \text{max\_effective\_rate} = \text{transfer\_rate\_max} \times \text{flowability\_factor} \times \text{discharge\_efficiency}

.. math::

   \text{actual\_rate} = \min(\text{rate\_setpoint}, \text{max\_effective\_rate})

.. math::

   \text{total\_time} = \frac{\text{available\_mass}}{\text{actual\_rate}/60} + \frac{\text{transfer\_distance}}{\text{conveyor\_speed}} + \text{handling\_time}

Dynamic Model
~~~~~~~~~~~~~

The dynamic model tracks:

* Transfer rate response with first-order dynamics
* Container level changes based on mass balance
* System stops when container is empty

State equations:

.. math::

   \frac{d(\text{transfer\_rate})}{dt} = \frac{\text{rate\_ss} - \text{transfer\_rate}}{\tau_{\text{rate}}}

.. math::

   \frac{d(\text{fill\_level})}{dt} = -\frac{\text{volume\_flow\_rate}}{\text{container\_capacity}}

where :math:`\tau_{\text{rate}} = 10.0` s is the discharge rate response time constant.

Parameters
----------

.. list-table:: Model Parameters
   :widths: 20 15 15 50
   :header-rows: 1

   * - Parameter
     - Range
     - Unit
     - Description
   * - container_capacity
     - 0.1 - 2.0
     - m³
     - Container volume capacity
   * - transfer_rate_max
     - 10.0 - 500.0
     - kg/min
     - Maximum discharge rate
   * - material_density
     - 200.0 - 2000.0
     - kg/m³
     - Bulk density of material
   * - discharge_efficiency
     - 0.5 - 1.0
     - -
     - Discharge mechanism efficiency
   * - handling_time
     - 60.0 - 300.0
     - s
     - Setup and handling time per batch
   * - conveyor_speed
     - 0.1 - 2.0
     - m/s
     - Conveyor belt speed
   * - transfer_distance
     - 1.0 - 50.0
     - m
     - Transfer distance

Examples
--------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from transport.batch.solid.DrumBinTransfer import DrumBinTransfer
   import numpy as np

   # Create pharmaceutical transfer system
   pharma_transfer = DrumBinTransfer(
       container_capacity=0.3,      # 300 L container
       transfer_rate_max=80.0,      # 80 kg/min max rate
       material_density=600.0,      # Pharmaceutical powder density
       discharge_efficiency=0.9,    # Good discharge efficiency
       handling_time=90.0,          # 1.5 min handling time
       conveyor_speed=0.4,          # 0.4 m/s conveyor speed
       transfer_distance=8.0        # 8 m transfer distance
   )

   # Steady-state calculation
   u = np.array([0.8, 70.0, 0.7])  # [fill_level, setpoint, flowability]
   result = pharma_transfer.steady_state(u)
   transfer_rate, batch_time = result
   print(f"Transfer rate: {transfer_rate:.1f} kg/min")
   print(f"Batch time: {batch_time:.1f} s")

Dynamic Simulation
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Dynamic simulation
   import matplotlib.pyplot as plt

   time_span = np.linspace(0, 600, 301)  # 10 minutes
   dt = time_span[1] - time_span[0]

   # Initial conditions
   x = np.array([0.0, 1.0])  # [transfer_rate=0, fill_level=1.0]
   u = np.array([1.0, 70.0, 0.8])  # [target_fill, setpoint, flowability]

   # Storage for results
   transfer_rates = []
   fill_levels = []

   # Euler integration
   for t in time_span:
       transfer_rates.append(x[0])
       fill_levels.append(x[1])
       
       if x[1] > 0:  # Continue only if material remains
           dx_dt = pharma_transfer.dynamics(t, x, u)
           x = x + dx_dt * dt
           x[1] = max(0.0, x[1])  # Prevent negative fill level
       else:
           break

   # Plot results
   plt.figure(figsize=(10, 6))
   plt.subplot(2, 1, 1)
   plt.plot(time_span[:len(transfer_rates)]/60, transfer_rates)
   plt.ylabel('Transfer Rate (kg/min)')
   plt.title('DrumBinTransfer Dynamic Response')

   plt.subplot(2, 1, 2)
   plt.plot(time_span[:len(fill_levels)]/60, np.array(fill_levels)*100)
   plt.xlabel('Time (min)')
   plt.ylabel('Fill Level (%)')
   plt.show()

Visualization Results
---------------------

Dynamic Response
~~~~~~~~~~~~~~~~

.. figure:: DrumBinTransfer_example_plots.png
   :align: center
   :width: 80%

   Dynamic response showing transfer rate and container fill level during batch operation.

Detailed Analysis
~~~~~~~~~~~~~~~~~

.. figure:: DrumBinTransfer_detailed_analysis.png
   :align: center
   :width: 90%

   Detailed analysis showing flowability effects, fill level impacts, setpoint tracking, and batch time calculations.

Example Output
--------------

.. literalinclude:: DrumBinTransfer_example.out
   :language: text
   :caption: Complete example output

Literature References
---------------------

1. Perry, R.H., Green, D.W. (2019). "Perry's Chemical Engineers' Handbook", 9th Edition, McGraw-Hill, Chapter 21: Solid-Solid Operations.

2. Schulze, D. (2008). "Powders and Bulk Solids: Behavior, Characterization, Storage and Flow", Springer, ISBN: 978-3-540-73768-1.

3. Marinelli, J., Carson, J.W. (1992). "Solve solids flow problems in bins, hoppers, and feeders", Chemical Engineering Progress, 88(5), 22-28.

4. Jenike, A.W. (1964). "Storage and Flow of Solids", Bulletin No. 123, University of Utah Engineering Experiment Station.

5. BMHB (2003). "The Design of Hoppers, Silos and Bunkers", Institution of Chemical Engineers, Rugby, UK.

6. Roberts, A.W. (2001). "Particle Technology - Storage and Flow of Particulate Solids", TUNRA Bulk Solids Research Associates, University of Newcastle.
