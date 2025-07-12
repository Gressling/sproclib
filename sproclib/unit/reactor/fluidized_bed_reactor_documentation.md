# Fluidized Bed Reactor Model

## Use Case

The Fluidized Bed Reactor model simulates gas-solid catalytic reactors with fluidized catalyst particles. It is extensively used in petroleum refining (fluid catalytic cracking), coal combustion and gasification, polymerization processes, and waste treatment applications where excellent heat and mass transfer characteristics are required.

## Algorithm

The Fluidized Bed Reactor model implements a two-phase theory with bubble and emulsion phases:

### Bubble Phase Material Balance
```
dC_b/dt = K_bc*(C_e - C_b) - u_b*dC_b/dz
```

### Emulsion Phase Material Balance
```
dC_e/dt = K_bc*δ_b*(C_b - C_e)/(1-δ_b) - k*C_e*ρ_cat*(1-ε_mf)/(1-δ_b)
```

### Energy Balance
```
dT/dt = (heat exchange terms + reaction heat)/(total heat capacity)
```

### Fluidization Characteristics
- **Minimum fluidization velocity**: U_mf = f(ρ_p, ρ_g, dp, μ, g)
- **Bubble velocity**: u_b = u_g - U_mf + u_br
- **Bubble fraction**: δ_b = f(u_g, U_mf, reactor geometry)

### Mass Transfer Coefficients
- **Bubble-cloud**: K_bc = f(D_g, u_b, d_b)
- **Cloud-emulsion**: K_ce = f(D_g, U_mf, d_b)

## Parameters

### Reactor Design Parameters
- **H**: Bed height [m] (typical range: 1-10)
- **D**: Bed diameter [m] (typical range: 1-20)
- **U_mf**: Minimum fluidization velocity [m/s] (typical range: 0.01-1.0)

### Particle Properties
- **rho_cat**: Catalyst density [kg/m³] (typical range: 500-3000)
- **dp**: Particle diameter [m] (typical range: 50e-6 to 1000e-6)
- **epsilon_mf**: Voidage at minimum fluidization [-] (typical range: 0.4-0.7)

### Kinetic Parameters
- **k0**: Pre-exponential factor [m³/kg·s] (typical range: 1e3-1e8)
- **Ea**: Activation energy [J/mol] (typical range: 40000-150000)

### Operating Variables
- **u_g**: Superficial gas velocity [m/s] (typical range: 0.1-5.0)
- **CAi**: Inlet concentration [mol/m³] (typical range: 10-1000)
- **Ti**: Inlet temperature [K] (typical range: 500-1000)

## Equations

1. **Fluidization Regime**: U_mf < u_g < U_t (terminal velocity)
2. **Bubble Rise Velocity**: u_br = 0.711*(g*d_b)^0.5
3. **Bubble Diameter**: d_b = d_b0 + growth along height
4. **Heat Transfer**: h = f(fluidization regime, particle properties)

## Usage

The Fluidized Bed Reactor model is suitable for:
- Fluid catalytic cracking (FCC) in petroleum refining
- Coal combustion and gasification
- Catalytic polymerization (polyethylene, polypropylene)
- Roasting and calcination of ores
- Waste incineration and treatment
- Biomass gasification

## Acceptable Working Ranges

### Fluidization Regimes
- **Minimum fluidization**: u_g ≈ U_mf
- **Bubbling regime**: U_mf < u_g < 10*U_mf
- **Slugging regime**: 10*U_mf < u_g < U_t
- **Fast fluidization**: u_g > U_t

### Temperature Ranges
- **Low temperature**: 400-600 K (polymerization)
- **Medium temperature**: 600-900 K (FCC)
- **High temperature**: 900-1200 K (combustion)

### Particle Size Ranges
- **Fine particles**: 50-200 μm (Group A)
- **Medium particles**: 200-1000 μm (Group B)
- **Coarse particles**: 1000-2000 μm (Group D)

### Operating Velocity
- **u_g/U_mf ratio**: 2-20 for good fluidization
- **Superficial velocity**: 0.1-5.0 m/s
- **Gas residence time**: 1-10 seconds

## Literature References

1. Kunii, D. and Levenspiel, O. (1991). "Fluidization Engineering", 2nd Edition, Butterworth-Heinemann.
2. Grace, J.R., Avidan, A.A., and Knowlton, T.M. (1997). "Circulating Fluidized Beds", Blackie Academic & Professional.
3. Geldart, D. (1986). "Gas Fluidization Technology", John Wiley & Sons.
4. Yang, W.C. (2003). "Handbook of Fluidization and Fluid-Particle Systems", Marcel Dekker.
5. Basu, P. (2006). "Combustion and Gasification in Fluidized Beds", CRC Press.
