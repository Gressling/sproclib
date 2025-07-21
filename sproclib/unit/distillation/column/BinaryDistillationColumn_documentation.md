# BinaryDistillationColumn Documentation

## Overview and Use Case
Multi-tray binary distillation column model for dynamic simulation and control design. Models complete column behavior including material balance dynamics across all trays, reflux drum, and reboiler.

## Physical/Chemical Principles
The column model integrates individual tray behavior with overall material balances:
- **Tray VLE**: y = α·x / (1 + (α-1)·x) for each tray
- **Component Balance**: dN·x/dt = accumulation of light component per tray
- **Fenske-Underwood-Gilliland**: Shortcut method for steady-state design
- **Separation Factor**: S = (x_D/(1-x_D)) / (x_B/(1-x_B))

Internal flows calculated from reflux ratio R and distillate rate D: L = R·D, V = L + D.

## Process Parameters
- **Number of Trays**: 5-100 theoretical stages (typical: 15-40 for industrial columns)
- **Feed Location**: Usually 40-60% from top (optimal feed tray)
- **Relative Volatility**: 1.01-20.0 dimensionless
- **Tray Holdup**: 0.5-10 kmol per tray
- **Reflux Ratio**: 0.1-50.0 dimensionless (typical: 1.2-5.0 × R_min)

## Operating Conditions
- **Pressure**: 1-50 bar depending on component volatility
- **Temperature**: Varies from condenser to reboiler (30-200°C typical)
- **Feed Flow**: 10-1000 kmol/min for industrial scale
- **Distillate Rate**: 10-500 kmol/min
- **Bottoms Rate**: 10-500 kmol/min

## Industrial Applications
- Crude oil atmospheric distillation (gasoline, diesel, heavy oil)
- Ethanol-water separation (bioethanol production)
- Benzene-toluene separation (petrochemical industry)
- Methanol-water separation (chemical plants)

## Limitations and Assumptions
- Binary systems only (two components)
- Constant relative volatility throughout column
- Equilibrium stages (no tray efficiency)
- Saturated liquid feed assumed
- Constant molar overflow (CMO) approximation

## Key References
- Luyben, W.L. "Distillation Design and Control Using Aspen Simulation", 2nd Ed., Wiley (2013)
- Skogestad, S. "Distillation Control", Encyclopedia of Systems and Control, Springer (2021)
- King, C.J. "Separation Processes", 2nd Ed., McGraw-Hill (1980)
