# Semi-Batch Reactor Model

## Use Case

The Semi-Batch Reactor model simulates fed-batch operation combining batch and continuous modes. It is commonly used in fine chemical manufacturing, controlled polymerization, crystallization processes, and biochemical fermentation where controlled addition of reactants is crucial for product quality and safety.

## Algorithm

The Semi-Batch Reactor model implements variable volume operation with controlled feeding:

### Material Balance
```
dnA/dt = F_in*CA_in - k(T)*CA*V
```

### Volume Balance
```
dV/dt = F_in
```

### Energy Balance
```
dT/dt = (F_in*ρ*cp*(T_in - T) + (-ΔH)*r*V + UA*(Tj - T))/(ρ*cp*V)
```

### Concentration Calculation
```
CA = nA/V
```

### Reaction Kinetics
```
k(T) = k0 * exp(-Ea/(R*T))
r = k(T) * CA  [mol/L/min]
```

## Parameters

### Reactor Design Parameters
- **V_max**: Maximum reactor volume [L] (typical range: 100-50000)
- **U**: Heat transfer coefficient [W/m²·K] (typical range: 100-1000)
- **A_heat**: Heat transfer area [m²] (typical range: 1-100)

### Kinetic Parameters
- **k0**: Pre-exponential factor [1/min] (typical range: 1e6-1e12)
- **Ea**: Activation energy [J/mol] (typical range: 40000-120000)

### Physical Properties
- **rho**: Density [kg/m³] (typical range: 800-1200)
- **cp**: Heat capacity [J/kg·K] (typical range: 2000-5000)
- **delta_H**: Heat of reaction [J/mol] (typical range: -100000 to -10000)

### Operating Variables
- **F_in**: Feed flow rate [L/min] (typical range: 0.1-100)
- **CA_in**: Feed concentration [mol/L] (typical range: 0.1-10)
- **T_in**: Feed temperature [K] (typical range: 280-400)
- **Tj**: Jacket temperature [K] (typical range: 250-400)

## Equations

1. **Instantaneous Conversion**: X = (n_A0 - n_A) / n_A0
2. **Overall Conversion**: X_overall = (n_A0 + ∫F_in*CA_in dt - n_A) / (n_A0 + ∫F_in*CA_in dt)
3. **Space-Time Yield**: STY = productivity / V_avg
4. **Dilution Rate**: D = F_in / V

## Usage

The Semi-Batch Reactor model is suitable for:
- Fine chemical and pharmaceutical manufacturing
- Controlled polymerization reactions
- Crystallization and precipitation processes
- Fed-batch fermentation
- Safety-critical reactions requiring controlled heat release

## Acceptable Working Ranges

### Volume Ranges
- **Initial volume**: 10-50% of V_max
- **Final volume**: 80-95% of V_max
- **Fill ratio**: V_final/V_initial = 2-10

### Feed Rate Ranges
- **Slow feeding**: 0.1-1 L/min
- **Medium feeding**: 1-10 L/min
- **Fast feeding**: 10-100 L/min

### Temperature Control
- **Operating range**: 250-500 K
- **Temperature rise control**: <5 K/min
- **Safety limit**: Heat removal capacity > heat generation

### Batch Time Ranges
- **Fast reactions**: 1-6 hours
- **Medium reactions**: 6-24 hours
- **Slow reactions**: 24-72 hours

## Literature References

1. Fogler, H.S. (2016). "Elements of Chemical Reaction Engineering", 5th Edition, Prentice Hall.
2. Nauman, E.B. (2008). "Chemical Reactor Design, Optimization, and Scaleup", 2nd Edition, McGraw-Hill.
3. Salmi, T., Mikkola, J.P., and Wärnå, J. (2019). "Chemical Reaction Engineering and Reactor Technology", 2nd Edition, CRC Press.
4. Levenspiel, O. (1999). "Chemical Reaction Engineering", 3rd Edition, John Wiley & Sons.
5. Rase, H.F. (1977). "Chemical Reactor Design for Process Plants", John Wiley & Sons.
