# GravityChute Model Documentation

## Overview

The GravityChute class models gravity-driven flow of solid particles down inclined chutes. This model is fundamental for designing particle discharge systems, hoppers, and gravity conveyors in various industrial applications.

## Use Case

Gravity chutes are employed in:
- Bulk material discharge from silos and hoppers
- Particle sorting and classification systems
- Mining material handling
- Food processing grain handling
- Pharmaceutical powder processing
- Waste material transport

## Algorithm Description

The GravityChute model implements:

1. **Force Balance Analysis**: Gravitational, friction, and air resistance forces
2. **Terminal Velocity Calculation**: Steady-state particle velocity
3. **Flow Rate Determination**: Based on chute geometry and loading
4. **Dynamic Response**: Particle acceleration and flow establishment

### Steady-State Model

The particle motion is governed by force balance:

```
F_gravity = mg × sin(θ) (driving force)
F_friction = μ × mg × cos(θ) (resistance force)
F_air = C_drag × ρ_air × v² × A_particle (air resistance)
```

Net acceleration:
```
a_net = g × (sin(θ) - μ × cos(θ)) - (C_drag × ρ_air × v²)/(2 × m_particle)
```

### Terminal Velocity

At steady state (a_net = 0):
```
v_terminal = sqrt(2 × m_particle × g × (sin(θ) - μ × cos(θ)) / (C_drag × ρ_air × A_particle))
```

### Flow Rate Calculation

Mass flow rate considering chute loading:
```
Q = A_flow × v_particle × ρ_bulk × loading_factor
```

### Dynamic Model

The dynamic response includes:
- Velocity response: `τ_velocity = v_terminal/acceleration`
- Flow response: `τ_flow = chute_length/velocity + settling_time`

## Parameters

| Parameter | Unit | Description | Typical Range |
|-----------|------|-------------|---------------|
| chute_length | m | Chute length | 1-50 |
| chute_width | m | Chute width | 0.1-5.0 |
| chute_angle | rad | Chute inclination | 0.17-0.79 (10-45°) |
| surface_roughness | - | Friction coefficient | 0.1-0.8 |
| particle_density | kg/m³ | Particle density | 1000-5000 |
| particle_diameter | m | Average particle size | 1e-3-20e-3 |
| air_resistance | - | Air resistance coefficient | 0.001-0.1 |

## Inputs and Outputs

### Inputs
- **feed_rate** (kg/s): Particle feed rate to chute
- **particle_size_factor** (-): Relative particle size factor
- **chute_loading** (-): Chute loading factor (0-1)

### Outputs
- **outlet_velocity** (m/s): Particle velocity at chute outlet
- **mass_flow_rate** (kg/s): Actual mass flow rate

## Working Ranges

- **Chute Angle**: 10-45° (steeper angles for free-flowing materials)
- **Particle Size**: 1-20 mm (model assumes uniform size distribution)
- **Particle Density**: 1000-5000 kg/m³
- **Surface Roughness**: 0.1-0.8 (smooth to very rough surfaces)

## Equations

### Force Balance
```
ma = mg sin(θ) - μmg cos(θ) - (1/2)ρ_air C_d A v²
```

### Terminal Velocity (simplified)
```
v_t = sqrt(2mg(sin(θ) - μ cos(θ)) / (ρ_air C_d A))
```

### Reynolds Number
```
Re = ρ_air × v × d_particle / μ_air
```

### Drag Coefficient
```
C_d = 24/Re (Re < 1, Stokes flow)
C_d = 24/Re × (1 + 0.15 Re^0.687) (1 < Re < 1000)
C_d = 0.44 (Re > 1000, Newton's law)
```

## Literature References

1. Brown, R.L. and Richards, J.C. "Principles of Powder Mechanics." Pergamon Press, 1970.
2. Geldart, D. "Gas Fluidization Technology." John Wiley & Sons, 1986.
3. Rhodes, M. "Introduction to Particle Technology." 2nd Edition, John Wiley & Sons, 2008.
4. Schulze, D. "Powders and Bulk Solids: Behavior, Characterization, Storage and Flow." Springer, 2008.
5. Nedderman, R.M. "Statics and Kinematics of Granular Materials." Cambridge University Press, 1992.

## Usage Guidelines

### Design Considerations
- Chute angle must exceed material's angle of repose
- Surface finish affects flow characteristics significantly
- Consider particle size distribution effects
- Account for wear and maintenance requirements
- Ensure adequate clearance for material flow

### Flow Regimes
- **Free Flow**: Particles flow without interaction (low loading)
- **Mass Flow**: Dense particle flow with interactions
- **Flooding**: Excessive loading causing flow restriction

### Applications
- Hopper discharge systems
- Conveyor transfer chutes
- Sorting and classification equipment
- Packaging and filling systems
- Mining and quarrying operations

### Limitations
- Assumes uniform particle properties
- No consideration of particle breakage
- Steady flow conditions assumed
- Limited to non-cohesive materials
- No humidity or temperature effects included
