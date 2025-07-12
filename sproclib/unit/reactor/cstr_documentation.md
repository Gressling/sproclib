# Continuous Stirred Tank Reactor (CSTR) Model

## Use Case

The CSTR model simulates a continuous stirred tank reactor with Arrhenius kinetics and energy balance. It is used for analyzing chemical reactions in well-mixed conditions with continuous feed and discharge streams. The model incorporates reaction kinetics, heat generation, and heat transfer with a jacket cooling system.

## Algorithm

The CSTR model implements a dynamic system based on material and energy balances:

### Material Balance
```
dCA/dt = q/V*(CAi - CA) - k(T)*CA
```

### Energy Balance  
```
dT/dt = q/V*(Ti - T) + (-dHr)*k(T)*CA/(rho*Cp) + UA*(Tc - T)/(V*rho*Cp)
```

### Reaction Kinetics
The reaction rate follows the Arrhenius equation:
```
k(T) = k0 * exp(-Ea/(R*T))
```

### Steady State Solution
Steady-state conditions are found by solving:
```
dCA/dt = 0 and dT/dt = 0
```
using numerical methods (scipy.optimize.fsolve).

## Parameters

### Reactor Design Parameters
- **V**: Reactor volume [L] (typical range: 10-10000)
- **UA**: Heat transfer coefficient [J/min/K] (typical range: 1000-100000)

### Kinetic Parameters
- **k0**: Pre-exponential factor [1/min] (typical range: 1e6-1e12)
- **Ea**: Activation energy [J/gmol] (typical range: 40000-100000)
- **R**: Gas constant [J/gmol/K] = 8.314

### Physical Properties
- **rho**: Density [g/L] (typical range: 800-1200)
- **Cp**: Heat capacity [J/g/K] (typical range: 0.1-0.5)
- **dHr**: Heat of reaction [J/gmol] (typical range: -100000 to -10000)

### Operating Variables
- **q**: Flow rate [L/min] (typical range: 1-1000)
- **CAi**: Inlet concentration [mol/L] (typical range: 0.1-10)
- **Ti**: Inlet temperature [K] (typical range: 280-400)
- **Tc**: Coolant temperature [K] (typical range: 250-350)

## Equations

1. **Reaction Rate**: r = k(T) * CA [mol/L/min]
2. **Conversion**: X = (CAi - CA) / CAi
3. **Residence Time**: τ = V / q [min]
4. **Heat Generation**: Qgen = (-dHr) * r * V [J/min]

## Usage

The CSTR model is suitable for:
- Continuous reaction processes
- Process control design and tuning
- Reactor optimization studies
- Safety and operability analysis
- Educational purposes

## Acceptable Working Ranges

### Temperature Ranges
- **Operating**: 250-600 K
- **Optimal**: 300-500 K
- **Safety limit**: <600 K to prevent degradation

### Concentration Ranges
- **Feed concentration**: 0.1-10 mol/L
- **Operating conversion**: 0.1-0.95
- **Maximum concentration**: <100 mol/L

### Flow Rate Ranges
- **Minimum**: 0.1 L/min (to maintain continuous operation)
- **Maximum**: 1000 L/min (limited by mixing effectiveness)
- **Optimal**: 1-100 L/min for most applications

### Volume Ranges
- **Laboratory scale**: 1-10 L
- **Pilot scale**: 10-1000 L
- **Industrial scale**: 1000-10000 L

## Literature References

1. Fogler, H.S. (2016). "Elements of Chemical Reaction Engineering", 5th Edition, Prentice Hall.
2. Levenspiel, O. (1999). "Chemical Reaction Engineering", 3rd Edition, John Wiley & Sons.
3. Rawlings, J.B. and Ekerdt, J.G. (2002). "Chemical Reactor Analysis and Design Fundamentals", Nob Hill Publishing.
4. Schmidt, L.D. (2005). "The Engineering of Chemical Reactions", 2nd Edition, Oxford University Press.
5. Davis, M.E. and Davis, R.J. (2003). "Fundamentals of Chemical Reaction Engineering", McGraw-Hill.
