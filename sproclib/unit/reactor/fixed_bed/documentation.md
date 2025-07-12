# Fixed Bed Reactor Model

## Use Case

The Fixed Bed Reactor model simulates packed bed catalytic reactors with solid catalyst particles. It is commonly used in petrochemical industry for hydrogenation, oxidation, steam reforming, and environmental catalysis applications. The model accounts for bed porosity, catalyst loading, axial concentration and temperature profiles, and pressure drop effects.

## Algorithm

The Fixed Bed Reactor model implements a heterogeneous catalytic system with axial discretization:

### Material Balance (per segment)
```
dCA/dt = -u*dCA/dz - k(T)*CA*W_cat/V_void
```

### Energy Balance (per segment)
```
dT/dt = -u*dT/dz + (-ΔH*r*W_cat)/(ρ*cp*V_void) + UA(Tw-T)/(ρ*cp*V_void)
```

### Reaction Kinetics
```
k(T) = k0 * exp(-Ea/(R*T))
r = k(T) * CA  [mol/kg_cat/s]
```

### Bed Properties
- Void volume: V_void = ε * V_total
- Catalyst mass per segment: W_cat = ρ_cat * (1-ε) * A_cross * dz
- Pressure drop: ΔP = f(Re, ε, dp, L)

## Parameters

### Reactor Design Parameters
- **L**: Bed length [m] (typical range: 0.1-20)
- **D**: Bed diameter [m] (typical range: 0.1-5)
- **ε**: Bed porosity [-] (typical range: 0.2-0.8)
- **ρ_cat**: Catalyst density [kg/m³] (typical range: 500-2000)
- **dp**: Particle diameter [m] (typical range: 0.001-0.01)

### Kinetic Parameters
- **k0**: Pre-exponential factor [m³/kg·s] (typical range: 1e3-1e8)
- **Ea**: Activation energy [J/mol] (typical range: 40000-150000)

### Physical Properties
- **rho**: Fluid density [kg/m³] (typical range: 0.1-1000)
- **cp**: Heat capacity [J/kg·K] (typical range: 1000-5000)
- **delta_H**: Heat of reaction [J/mol] (typical range: -200000 to -10000)

### Operating Variables
- **u**: Superficial velocity [m/s] (typical range: 0.001-1.0)
- **CAi**: Inlet concentration [mol/m³] (typical range: 10-10000)
- **Ti**: Inlet temperature [K] (typical range: 300-800)
- **Tw**: Wall temperature [K] (typical range: 300-1000)

## Equations

1. **Reaction Rate**: r = k(T) * CA [mol/kg_cat/s]
2. **Conversion**: X = (CAi - CAe) / CAi
3. **Space Velocity**: SV = u / L [1/s]
4. **Residence Time**: τ = ε * L / u [s]

## Usage

The Fixed Bed Reactor model is suitable for:
- Catalytic processes in petrochemical industry
- Steam reforming and synthesis gas production
- Hydrogenation and dehydrogenation reactions
- Environmental catalysis (SCR, oxidation)
- Ammonia synthesis and other gas-phase reactions

## Acceptable Working Ranges

### Temperature Ranges
- **Operating**: 300-1000 K
- **Optimal for most catalysts**: 400-700 K
- **High-temperature processes**: 700-1000 K

### Pressure Ranges
- **Low pressure**: 1-10 bar
- **Medium pressure**: 10-50 bar
- **High pressure**: 50-300 bar

### Flow Rate Ranges
- **Superficial velocity**: 0.001-1.0 m/s
- **Space velocity**: 0.1-100 h⁻¹
- **Reynolds number**: 0.1-1000

### Bed Design Ranges
- **L/D ratio**: 1-20 (typical 3-10)
- **Bed porosity**: 0.2-0.8 (typical 0.4-0.6)
- **Particle size**: 1-10 mm

## Literature References

1. Froment, G.F., Bischoff, K.B., and De Wilde, J. (2010). "Chemical Reactor Analysis and Design", 3rd Edition, John Wiley & Sons.
2. Fogler, H.S. (2016). "Elements of Chemical Reaction Engineering", 5th Edition, Prentice Hall.
3. Rase, H.F. (1977). "Chemical Reactor Design for Process Plants", John Wiley & Sons.
4. Sie, S.T. (1996). "Reaction engineering aspects of catalytic processes in fixed beds", Applied Catalysis A: General, 146, 1-26.
5. Dudukovic, M.P. (2010). "Reaction engineering: Status and future challenges", Chemical Engineering Science, 65, 3-11.
