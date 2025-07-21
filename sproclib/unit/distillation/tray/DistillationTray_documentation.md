# DistillationTray Documentation

## Overview and Use Case
Individual theoretical tray model for binary distillation systems using vapor-liquid equilibrium relationships. Essential component for dynamic simulation and control design of distillation columns.

## Physical/Chemical Principles
The tray model assumes vapor-liquid equilibrium governed by relative volatility:
- **VLE Equation**: y = α·x / (1 + (α-1)·x)
- **Material Balance**: dN·x/dt = L_in·x_in + V_in·y_in - L_out·x_out - V_out·y_out
- **Equilibrium Stage**: Vapor leaving tray is in equilibrium with liquid on tray

Where α is relative volatility (light/heavy component), x is liquid mole fraction, and y is vapor mole fraction.

## Process Parameters
- **Tray Holdup**: 0.1 - 100 kmol (typical: 1-5 kmol for industrial columns)
- **Relative Volatility**: 1.01 - 20.0 dimensionless (typical: 1.5-4.0 for common separations)
- **Composition Range**: 0.0 - 1.0 mole fraction
- **Flow Rates**: 1-1000 kmol/min depending on column size

## Operating Conditions
- **Temperature**: Varies with column pressure and component properties
- **Pressure**: 1-50 bar (typical atmospheric to moderate pressure)
- **Liquid Flow**: 50-2000 kmol/min for industrial columns
- **Vapor Flow**: 100-3000 kmol/min for industrial columns

## Industrial Applications
- Petrochemical refineries (crude oil fractionation)
- Alcohol production and purification
- Solvent recovery systems
- Chemical plant separation units

## Limitations and Assumptions
- Binary systems only (two components)
- Constant relative volatility across composition range
- Perfect mixing on tray (no concentration gradients)
- Equilibrium stage assumption (100% efficiency)
- No entrainment or weeping effects

## Key References
- Seborg, D.E., Edgar, T.F., Mellichamp, D.A. "Process Dynamics and Control", 4th Ed., Wiley (2016)
- McCabe, W.L., Smith, J.C., Harriott, P. "Unit Operations of Chemical Engineering", 7th Ed., McGraw-Hill (2004)
- Kister, H.Z. "Distillation Design", McGraw-Hill (1992)
