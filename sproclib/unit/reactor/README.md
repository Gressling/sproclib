# Reactor Units

This directory contains various reactor process unit models for chemical reactions.

## Contents

- `cstr/`: Continuous Stirred Tank Reactor models
- `plug_flow/`: Plug Flow Reactor models  
- `batch/`: Batch Reactor models
- `semi_batch/`: Semi-Batch Reactor models
- `fixed_bed/`: Fixed Bed Reactor models
- `fluidized_bed/`: Fluidized Bed Reactor models

## Available Reactor Types

### CSTR (`cstr/`)
- Continuous stirred tank reactor with perfect mixing
- Temperature and concentration dynamics
- Multiple reaction support
- Heat generation/removal modeling

### Plug Flow Reactor (`plug_flow/`)
- Distributed parameter reactor model
- Axial concentration and temperature profiles
- Reaction kinetics integration
- Heat transfer to jacket/environment

### Batch Reactor (`batch/`)
- Batch operation with time-varying conditions
- Temperature control through jacket
- Multiple reactions and species
- Optimal temperature trajectory tracking

### Semi-Batch Reactor (`semi_batch/`)
- Semi-batch operation with feed addition
- Fed-batch pharmaceutical applications
- Temperature and concentration control
- Feed rate optimization

### Fixed Bed Reactor (`fixed_bed/`)
- Packed bed catalytic reactor
- Catalyst deactivation modeling
- Pressure drop and heat transfer
- Axial dispersion effects

### Fluidized Bed Reactor (`fluidized_bed/`)
- Two-phase (bubble and emulsion) model
- Fluidization properties calculation
- Mass transfer between phases
- Catalytic reaction in emulsion phase

## Usage Examples

```python
# CSTR example
from paramus.chemistry.process_control.unit.reactor.cstr import CSTR

cstr = CSTR(
    volume=1.0,           # m³
    k_reaction=0.1,       # reaction rate constant
    E_activation=50000,   # activation energy
    density=1000.0        # kg/m³
)

# PFR example
from sproclib.unit.reactor.plug_flow import PlugFlowReactor

pfr = PlugFlowReactor(
    length=10.0,          # m
    diameter=0.5,         # m
    k_reaction=0.1,       # reaction rate constant
    E_activation=50000    # activation energy
)

# Fluidized Bed Reactor example
from paramus.chemistry.process_control.unit.reactor.fluidized_bed import FluidizedBedReactor

fbr = FluidizedBedReactor(
    H=3.0,                # bed height [m]
    D=2.0,                # bed diameter [m]
    U_mf=0.1,             # minimum fluidization velocity [m/s]
    rho_cat=1500.0,       # catalyst density [kg/m³]
    k0=1e5,               # pre-exponential factor
    Ea=60000.0            # activation energy [J/mol]
)
```

## For Contributors

When adding reactor models:
- Include detailed reaction kinetics
- Model heat and mass transfer limitations
- Add catalyst deactivation for heterogeneous systems
- Consider non-ideal flow patterns
- Include startup and shutdown procedures
- Add safety constraints and monitoring
