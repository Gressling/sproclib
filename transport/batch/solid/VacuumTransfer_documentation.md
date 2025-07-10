# VacuumTransfer Documentation

## Overview

The `VacuumTransfer` class models pneumatic powder transfer systems using vacuum pumps and cyclone separators. This model is widely used in pharmaceutical, food, and chemical industries for transferring fine powders and granular materials through enclosed piping systems.

## Use Case

The vacuum transfer system is employed when:
- Fine powder handling requires dust containment
- Materials are sensitive to contamination
- Transfer over long distances or multiple elevation changes
- Automated material handling is required
- Clean-in-place (CIP) capabilities are needed

## Algorithm Description

### Steady-State Model

The steady-state calculation determines transfer rate and vacuum level based on:

1. **Air Flow Calculation**: Through transfer line considering pressure drop
2. **Powder Entrainment**: Based on air velocity and particle pickup velocity
3. **Cyclone Separation**: Efficiency factor for powder collection
4. **System Resistance**: Line resistance and filter loading effects

### Dynamic Model

The dynamic model tracks:
- Powder transfer rate response with entrainment dynamics
- Vacuum level response considering pump and system characteristics
- First-order time constants for both variables

## Parameters

| Parameter | Range | Unit | Description |
|-----------|-------|------|-------------|
| vacuum_pump_capacity | 10.0 - 500.0 | m³/h | Vacuum pump volumetric capacity |
| transfer_line_diameter | 0.02 - 0.15 | m | Transfer line internal diameter |
| transfer_line_length | 1.0 - 100.0 | m | Transfer line length |
| powder_density | 200.0 - 1500.0 | kg/m³ | Powder bulk density |
| particle_size | 10e-6 - 500e-6 | m | Average particle diameter |
| cyclone_efficiency | 0.8 - 0.99 | - | Cyclone separator efficiency |
| vacuum_level_max | -100000 - 0 | Pa | Maximum vacuum level (gauge) |
| filter_resistance | 100.0 - 5000.0 | Pa⋅s/m³ | Filter pressure drop resistance |

## Equations

### Air Velocity in Transfer Line
```
v_air = sqrt(2 * ΔP / ρ_air)
```

### Particle Pickup Velocity
```
v_terminal = sqrt(4 * g * d_p * ρ_p / (3 * C_d * ρ_air))
v_pickup = 2 * v_terminal
```

### Powder Transfer Rate
```
if v_air > v_pickup:
    velocity_ratio = v_air / v_pickup
    loading_ratio = min(2.0, velocity_ratio * 0.5)
    powder_rate = Q_air * ρ_air * loading_ratio * η_cyclone
```

### System Pressure Drop
```
R_line = 32 * μ_air * L / D²
R_filter_total = R_filter * (1 + filter_loading * 2)
ΔP_total = Q_pump * (R_line + R_filter_total)
```

### Air Mass Flow
```
Q_air = vacuum_pump_capacity / 3600  # m³/s
m_air = Q_air * ρ_air
```

## Acceptable Working Ranges

### Material Properties
- **Bulk Density**: 200-1500 kg/m³ (typical powder range)
- **Particle Size**: 10-500 μm (fine to coarse powders)
- **Powder Level**: 0.0-1.0 (source container fill level)

### Process Conditions
- **Vacuum Level**: 0 to -100 kPa gauge (typical vacuum range)
- **Air Velocity**: 15-30 m/s (dilute phase transport)
- **Solids Loading**: 0.1-2.0 kg solid/kg air (dilute phase)

### Equipment Parameters
- **Pump Capacity**: 10-500 m³/h (laboratory to industrial scale)
- **Line Diameter**: 20-150 mm (typical pneumatic conveying)
- **Line Length**: 1-100 m (practical transfer distances)
- **Cyclone Efficiency**: 80-99% (depends on particle size)

### Performance Limits
- **Filter Loading**: 0.0-1.0 (clean to loaded filter)
- **Transfer Rate**: 0.1-50 kg/s (depends on system size)
- **Response Time**: 3-10 s (typical pneumatic system dynamics)

## Literature References

1. Mills, D. (2004). "Pneumatic Conveying Design Guide", 2nd Edition, Butterworth-Heinemann, ISBN: 978-0750654715.

2. Klinzing, G.E., Rizk, F., Marcus, R., Leung, L.S. (2010). "Pneumatic Conveying of Solids: A Theoretical and Practical Approach", 3rd Edition, Springer, ISBN: 978-90-481-3609-4.

3. Wypych, P.W. (1999). "Handbook of Pneumatic Conveying Engineering", Marcel Dekker, ISBN: 0-8247-0249-4.

4. Bradley, D. (1965). "The Hydrocyclone", Pergamon Press, Oxford.

5. Muschelknautz, E. (1972). "Design criteria for pneumatic conveying systems", Bulk Solids Handling, 2(4), 679-684.

6. Konno, H., Saito, S. (1969). "Pneumatic conveying of solids through straight pipes", Journal of Chemical Engineering of Japan, 2(2), 211-217.

7. Weber, M. (1991). "Principles of hydraulic and pneumatic conveying in pipes", Bulk Solids Handling, 11(1), 57-63.

8. Gasterstadt, S., Mallick, S.S., Wypych, P.W. (2017). "An investigation into the effect of particle size on dense phase pneumatic conveying", Particuology, 31, 68-77.
