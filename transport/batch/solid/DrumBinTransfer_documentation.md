# DrumBinTransfer Documentation

## Overview

The `DrumBinTransfer` class models batch solid material transfer operations using drums or bins with conveyor-based discharge systems. This model is commonly used in pharmaceutical, food, and chemical processing industries for transferring powders, granules, and other solid materials between process units.

## Use Case

The drum/bin transfer system is employed when:
- Batch processing requires controlled material handling
- Materials need to be transferred between different elevation levels
- Dust containment is important
- Process requires intermediate storage capacity
- Materials have varying flowability characteristics

## Algorithm Description

### Steady-State Model

The steady-state calculation determines the actual transfer rate and batch completion time based on:

1. **Available Material Mass**: Calculated from container fill level and material density
2. **Effective Discharge Rate**: Considers flowability factor and discharge efficiency
3. **Transfer Rate Limiting**: Accounts for material availability and discharge capacity
4. **Batch Time Calculation**: Includes discharge, transport, and handling times

### Dynamic Model

The dynamic model tracks:
- Transfer rate response with first-order dynamics
- Container level changes based on mass balance
- System stops when container is empty

## Parameters

| Parameter | Range | Unit | Description |
|-----------|-------|------|-------------|
| container_capacity | 0.1 - 2.0 | m³ | Container volume capacity |
| transfer_rate_max | 10.0 - 500.0 | kg/min | Maximum discharge rate |
| material_density | 200.0 - 2000.0 | kg/m³ | Bulk density of material |
| discharge_efficiency | 0.5 - 1.0 | - | Discharge mechanism efficiency |
| handling_time | 60.0 - 300.0 | s | Setup and handling time per batch |
| conveyor_speed | 0.1 - 2.0 | m/s | Conveyor belt speed |
| transfer_distance | 1.0 - 50.0 | m | Transfer distance |

## Equations

### Mass Balance
```
dmass/dt = -transfer_rate
```

### Effective Discharge Rate
```
flowability_factor = 0.5 + 0.5 * flowability
max_effective_rate = transfer_rate_max * flowability_factor * discharge_efficiency
actual_rate = min(rate_setpoint, max_effective_rate)
```

### Level Factor for Low Fill
```
if fill_level < 0.1:
    level_factor = fill_level / 0.1
    actual_rate *= level_factor
```

### Total Batch Time
```
discharge_time = available_mass / (actual_rate / 60.0)
transport_time = transfer_distance / conveyor_speed
total_time = discharge_time + transport_time + handling_time
```

## Acceptable Working Ranges

### Material Properties
- **Bulk Density**: 200-2000 kg/m³ (covers most industrial powders)
- **Flowability Index**: 0.0-1.0 (0=poor, 1=excellent flow)
- **Particle Size**: 10 μm - 10 mm (fine powders to granules)

### Process Conditions
- **Fill Level**: 0.0-1.0 (0=empty, 1=full container)
- **Discharge Rate**: 10-500 kg/min (typical industrial ranges)
- **Container Size**: 0.1-2.0 m³ (laboratory to pilot scale)

### Performance Limits
- **Discharge Efficiency**: 0.5-1.0 (depends on material and equipment)
- **Conveyor Speed**: 0.1-2.0 m/s (typical belt conveyor speeds)
- **Transfer Distance**: 1-50 m (practical conveyor lengths)

## Literature References

1. Perry, R.H., Green, D.W. (2019). "Perry's Chemical Engineers' Handbook", 9th Edition, McGraw-Hill, Chapter 21: Solid-Solid Operations.

2. Schulze, D. (2008). "Powders and Bulk Solids: Behavior, Characterization, Storage and Flow", Springer, ISBN: 978-3-540-73768-1.

3. Marinelli, J., Carson, J.W. (1992). "Solve solids flow problems in bins, hoppers, and feeders", Chemical Engineering Progress, 88(5), 22-28.

4. Jenike, A.W. (1964). "Storage and Flow of Solids", Bulletin No. 123, University of Utah Engineering Experiment Station.

5. BMHB (2003). "The Design of Hoppers, Silos and Bunkers", Institution of Chemical Engineers, Rugby, UK.

6. Roberts, A.W. (2001). "Particle Technology - Storage and Flow of Particulate Solids", TUNRA Bulk Solids Research Associates, University of Newcastle.
