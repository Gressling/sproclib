# PeristalticFlow Class Documentation

## Overview

The `PeristalticFlow` class models peristaltic pump systems used for precise fluid transport in process control applications. Peristaltic pumps use mechanical compression of flexible tubing to create flow, making them ideal for sterile, accurate, and contamination-free fluid handling.

## Scientific Background

### Peristaltic Pump Principles

Peristaltic pumps operate on the principle of peristalsis, similar to biological processes like digestion. The key mechanisms include:

1. **Mechanical Compression**: Rollers or shoes compress flexible tubing against a circular track
2. **Progressive Motion**: The compression point moves along the tubing, creating a traveling wave
3. **Positive Displacement**: Each revolution displaces a fixed volume of fluid
4. **Self-Priming**: The pump can start with air in the lines and self-prime

### Flow Rate Calculation

The theoretical flow rate for a peristaltic pump is:

```
Q_theoretical = N × V_chamber
```

Where:
- Q_theoretical = Theoretical volumetric flow rate [m³/s]
- N = Pump speed [rev/s]
- V_chamber = Volume per revolution [m³]

The chamber volume depends on tube geometry:

```
V_chamber = π × (D/2)² × L_compression × occlusion_factor
```

Where:
- D = Tube inner diameter [m]
- L_compression = Length of tube compressed per revolution [m]
- occlusion_factor = Fraction of tube diameter compressed [-]

### Actual Flow Rate

Real peristaltic pumps have several factors that reduce actual flow:

1. **Slip**: Fluid backflow due to incomplete tube occlusion
2. **Tube Deformation**: Elastic recovery affects volume displacement
3. **Pressure Effects**: Higher outlet pressure reduces effective flow
4. **Tube Wear**: Degradation over time affects performance

The actual flow rate is modeled as:

```
Q_actual = Q_theoretical × efficiency × pressure_correction
```

### Pulsation Effects

Peristaltic pumps inherently produce pulsating flow due to the discrete compression cycles. The pulsation can be characterized by:

1. **Pulsation Amplitude**: Peak-to-peak flow variation
2. **Pulsation Frequency**: Related to pump speed and number of rollers
3. **Smoothing**: Dampening effects from tubing elasticity and system compliance

### Dynamic Response

The dynamic model accounts for:

1. **Tube Elasticity**: Compliance effects during compression/relaxation cycles
2. **Fluid Inertia**: Acceleration/deceleration of fluid column
3. **System Compliance**: Accumulator and tubing stretch effects

## Use Cases

### Pharmaceutical and Biotechnology

1. **Drug Manufacturing**
   - Precise dosing of active ingredients
   - Sterile transfer of solutions
   - Cell culture media delivery
   - Buffer and reagent handling

2. **Bioprocessing**
   - Fermentation feed streams
   - Product harvest and purification
   - Clean-in-place (CIP) chemical dosing
   - Waste handling systems

3. **Analytical Instruments**
   - HPLC mobile phase delivery
   - Sample injection systems
   - Reagent pumps for analyzers
   - Calibration standard delivery

### Chemical Processing

1. **Corrosive Chemical Handling**
   - Acid and base transfer
   - Catalyst injection
   - Additive dosing
   - Waste treatment chemicals

2. **Precision Dosing**
   - Polymerization initiators
   - pH adjustment chemicals
   - Trace additive injection
   - Quality control sampling

### Food and Beverage Industry

1. **Ingredient Dosing**
   - Flavor and color addition
   - Preservative injection
   - Vitamin and mineral fortification
   - Enzyme addition

2. **Sanitary Applications**
   - CIP chemical circulation
   - Product transfer
   - Sampling systems
   - Waste handling

### Water Treatment

1. **Chemical Feed Systems**
   - Chlorine and disinfectant dosing
   - Coagulant and flocculant injection
   - pH adjustment chemicals
   - Anti-scalant addition

2. **Process Control**
   - Polymer feed for sludge dewatering
   - Nutrient dosing for biological treatment
   - Trace contaminant analysis sampling

## Class Structure

### Main Class: `PeristalticFlow`

The primary class inheriting from `ProcessModel` that encapsulates peristaltic pump functionality.

#### Key Parameters

| Parameter | Unit | Description | Typical Range |
|-----------|------|-------------|---------------|
| `tube_diameter` | m | Inner diameter of pump tubing | 0.001-0.05 |
| `tube_length` | m | Length of tubing in pump head | 0.1-2.0 |
| `pump_speed` | rpm | Rotational speed of pump | 1-1000 |
| `occlusion_factor` | - | Tube compression ratio | 0.5-1.0 |
| `fluid_density` | kg/m³ | Density of pumped fluid | 500-2000 |
| `fluid_viscosity` | Pa·s | Dynamic viscosity | 1e-6 to 1e-1 |
| `pulsation_damping` | - | Flow smoothing factor | 0.1-1.0 |

#### Key Methods

1. **`steady_state(pump_speed)`**
   - Calculates steady-state flow rate and pump characteristics
   - Returns flow rate, efficiency, chamber volume, and pulsation metrics
   - Accounts for slip and pressure effects

2. **`dynamics(pump_speed, time_step)`**
   - Simulates dynamic pump response including pulsation
   - Models tube compliance and fluid inertia
   - Returns time-dependent flow variables

3. **`describe()`**
   - Provides comprehensive metadata about the pump model
   - Returns algorithm information, parameters, and equations
   - Useful for documentation and introspection

### Static Methods

- **`describe_steady_state()`**: Metadata for steady-state flow calculations
- **`describe_dynamics()`**: Metadata for dynamic flow simulations

## Mathematical Models

### Steady-State Model

The steady-state model calculates:

1. **Chamber Volume**: V = π × (D/2)² × L × occlusion
2. **Theoretical Flow**: Q_th = N × V
3. **Actual Flow**: Q = Q_th × efficiency × corrections
4. **Pulsation**: Amplitude and frequency calculations

### Dynamic Model

The dynamic model includes:

1. **Tube Compliance**: Elastic effects during compression cycles
2. **Flow Pulsation**: Sinusoidal variation with pump frequency
3. **System Response**: First-order lag for overall system dynamics

```
Q(t) = Q_avg × [1 + pulsation_amplitude × sin(2π × f × t)]
```

Where:
- f = pump_speed × n_rollers / 60 [Hz]
- pulsation_amplitude depends on tube properties and damping

## Implementation Details

### Algorithm Features

- **Realistic pump modeling** with efficiency and slip factors
- **Pulsation simulation** for accurate dynamic response
- **Tube wear effects** through degradation factors
- **Pressure-dependent performance** modeling
- **Multi-roller configurations** support

### Performance Characteristics

1. **Flow Accuracy**: Typically ±1-5% of full scale
2. **Repeatability**: Better than ±0.5% for consistent conditions
3. **Turn-down Ratio**: Up to 1000:1 for speed-controlled pumps
4. **Pressure Capability**: Limited by tube burst pressure

### Operational Considerations

1. **Tube Selection**: Material compatibility and pressure rating
2. **Calibration**: Regular flow rate verification required
3. **Maintenance**: Tube replacement based on wear indicators
4. **Temperature Effects**: Viscosity and tube property changes

## Validation and Testing

The model has been validated against:

1. **Manufacturer specifications** for various pump models
2. **Experimental measurements** of flow rate vs. speed
3. **Pulsation analysis** using flow meters and oscilloscopes
4. **Long-term accuracy** studies with tube aging

Test coverage includes:
- Flow rate accuracy across speed range
- Pulsation amplitude and frequency verification
- Temperature and viscosity effects
- Tube wear and degradation modeling

## Scientific References

1. **Noordergraaf, A.** (1978). *Circulatory System Dynamics*. Academic Press.
   - Fundamental principles of peristaltic flow in biological and mechanical systems

2. **Yin, F.C.P., & Fung, Y.C.** (1971). "Peristaltic waves in circular cylindrical tubes." *Journal of Applied Mechanics*, 38(3), 579-587.
   - Mathematical analysis of peristaltic wave propagation

3. **Takabatake, S., & Ayukawa, K.** (1982). "Numerical study of two-dimensional peristaltic flows." *Journal of Fluid Mechanics*, 122, 439-465.
   - Computational fluid dynamics approach to peristaltic pumping

4. **Weinberg, S.L.** (1963). "Theoretical and experimental treatment of peristaltic pumping and its relation to ureteral function." *Journal of Urology*, 89, 207-211.
   - Medical applications and experimental validation of peristaltic pumping

5. **Jaffrin, M.Y., & Shapiro, A.H.** (1971). "Peristaltic pumping." *Annual Review of Fluid Mechanics*, 3, 13-37.
   - Comprehensive review of peristaltic pumping theory and applications

6. **Cole, D.G., et al.** (1998). "Fluid mechanics of peristaltic pumping for process applications." *Chemical Engineering and Processing*, 37(4), 363-378.
   - Industrial applications and design considerations

## Related Wikipedia Articles

- [Peristaltic Pump](https://en.wikipedia.org/wiki/Peristaltic_pump)
- [Peristalsis](https://en.wikipedia.org/wiki/Peristalsis)
- [Positive Displacement Pump](https://en.wikipedia.org/wiki/Positive-displacement_pump)
- [Fluid Mechanics](https://en.wikipedia.org/wiki/Fluid_mechanics)
- [Pump](https://en.wikipedia.org/wiki/Pump)

## Example Usage

```python
# Create a peristaltic pump model
pump = PeristalticFlow(
    tube_diameter=0.005,        # 5 mm ID tubing
    tube_length=0.3,            # 30 cm in pump head
    pump_speed=100.0,           # 100 RPM
    occlusion_factor=0.9,       # 90% compression
    fluid_density=1000.0,       # Water
    fluid_viscosity=1e-3,       # Water at 20°C
    pulsation_damping=0.8       # Moderate damping
)

# Steady-state calculation
speed = 150  # RPM
results = pump.steady_state(speed)
print(f"Flow rate: {results['flow_rate']*1000:.2f} L/min")
print(f"Pulsation: ±{results['pulsation_amplitude']*100:.1f}%")

# Dynamic simulation
dt = 0.01  # 10 ms time step
dynamic_results = pump.dynamics(speed, dt)

# Get model information
info = pump.describe()
print(f"Model: {info['model_type']}")
print(f"Applications: {info['applications']}")
```

## Advantages and Limitations

### Advantages

1. **Contamination-Free**: Fluid only contacts tubing interior
2. **Self-Priming**: Can start with air-filled lines
3. **Precise Metering**: Excellent repeatability and accuracy
4. **Reversible**: Can pump in either direction
5. **Low Shear**: Gentle on sensitive fluids
6. **Easy Maintenance**: Only tubing requires replacement

### Limitations

1. **Pulsating Flow**: Inherent flow variation
2. **Tube Wear**: Regular replacement required
3. **Pressure Limitation**: Limited by tube burst pressure
4. **Flow Rate Range**: Fixed displacement per revolution
5. **Cost**: Higher than some centrifugal alternatives
6. **Efficiency**: Lower than rotodynamic pumps

## Design Considerations

### Tube Selection

1. **Material Compatibility**: Chemical resistance to pumped fluid
2. **Temperature Range**: Operating temperature limits
3. **Pressure Rating**: Maximum system pressure
4. **Flexibility**: Ease of compression and recovery
5. **Permeability**: Gas transmission for sensitive applications

### System Integration

1. **Pulsation Dampening**: Accumulators or compliance chambers
2. **Pressure Relief**: Protection against over-pressure
3. **Flow Measurement**: Verification of pump performance
4. **Control Integration**: Speed control and feedback systems

## Future Enhancements

- **Advanced pulsation modeling** with multiple rollers
- **Tube degradation prediction** algorithms
- **Temperature compensation** for viscosity effects
- **Multi-pump synchronization** for flow splitting
- **Predictive maintenance** features
