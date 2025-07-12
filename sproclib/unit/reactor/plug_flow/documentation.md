# Plug Flow Reactor (PFR) Model

## Use Case

The Plug Flow Reactor (PFR) model simulates tubular reactors with axial discretization where there is no back-mixing and fluid elements move through the reactor as "plugs". It is widely used for gas-phase reactions, high-temperature processes, and situations where high conversion is required. The model incorporates axial dispersion, heat transfer to walls, and temperature effects on reaction kinetics.

## Algorithm

The PFR model implements axially discretized material and energy balances:

### Material Balance (per segment)
```
dCA/dt = -u * dCA/dz - k(T) * CA
```

### Energy Balance (per segment)
```
dT/dt = -u * dT/dz + (-ΔH * r)/(ρ * cp) + UA(Tw - T)/(ρ * cp * V_segment)
```

### Axial Discretization
The reactor is divided into n_segments, each with:
- Segment length: dz = L / n_segments
- Segment volume: V_segment = A_cross * dz
- Heat transfer area: A_heat = π * D_tube * dz

### Reaction Kinetics
```
k(T) = k0 * exp(-Ea/(R*T))
r = k(T) * CA
```

## Parameters

### Reactor Design Parameters
- **L**: Reactor length [m] (typical range: 1-100)
- **A_cross**: Cross-sectional area [m²] (typical range: 0.01-10)
- **n_segments**: Number of discretization segments (typical range: 10-200)
- **D_tube**: Tube diameter [m] (typical range: 0.05-2.0)

### Kinetic Parameters
- **k0**: Pre-exponential factor [1/min] (typical range: 1e6-1e12)
- **Ea**: Activation energy [J/mol] (typical range: 40000-120000)
- **delta_H**: Heat of reaction [J/mol] (typical range: -100000 to -10000)

### Physical Properties
- **rho**: Density [kg/m³] (typical range: 0.5-1200)
- **cp**: Heat capacity [J/kg·K] (typical range: 1000-5000)
- **U**: Heat transfer coefficient [W/m²·K] (typical range: 10-500)

### Operating Variables
- **q**: Inlet flow rate [L/min] (typical range: 1-10000)
- **CAi**: Inlet concentration [mol/L] (typical range: 0.1-50)
- **Ti**: Inlet temperature [K] (typical range: 300-800)
- **Tw**: Wall temperature [K] (typical range: 250-900)

## Equations

1. **Superficial Velocity**: u = q / A_cross [m/s]
2. **Residence Time**: τ = V_total / q [min]
3. **Conversion**: X = (CAi - CA_exit) / CAi
4. **Peclet Number**: Pe = u * L / D_axial (for dispersion effects)

## Usage

The PFR model is suitable for:
- Tubular reactors in chemical plants
- Gas-phase reactions at high temperature
- Catalytic processes in tubes
- Steam cracking and reforming
- Polymerization in continuous processes

## Acceptable Working Ranges

### Temperature Ranges
- **Operating**: 250-800 K
- **Optimal**: 400-700 K
- **High-temperature applications**: 600-800 K

### Flow Rate Ranges
- **Gas-phase**: 100-10000 L/min
- **Liquid-phase**: 1-1000 L/min
- **Minimum**: >0.1 L/min for stable operation

### Reactor Geometry
- **Length**: 1-100 m (typical industrial: 10-50 m)
- **Diameter**: 0.05-2.0 m
- **L/D ratio**: 10-1000 (typical: 50-200)

### Discretization Guidelines
- **Minimum segments**: 10 (for simple reactions)
- **Recommended**: 20-50 segments
- **High gradients**: 50-200 segments

## Literature References

1. Fogler, H.S. (2016). "Elements of Chemical Reaction Engineering", 5th Edition, Prentice Hall.
2. Levenspiel, O. (1999). "Chemical Reaction Engineering", 3rd Edition, John Wiley & Sons.
3. Froment, G.F., Bischoff, K.B., and De Wilde, J. (2010). "Chemical Reactor Analysis and Design", 3rd Edition, John Wiley & Sons.
4. Hill, C.G. (1977). "An Introduction to Chemical Engineering Kinetics and Reactor Design", John Wiley & Sons.
5. Schmidt, L.D. (2005). "The Engineering of Chemical Reactions", 2nd Edition, Oxford University Press.
