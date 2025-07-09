# Compressor and Pump Models - Usage Guide

## Overview

**SPROCLIB** (Standard Process Control Library) includes comprehensive models for compressors and pumps, essential for fluid handling systems in chemical processes. These models provide both steady-state and dynamic behavior for control system design and process simulation.

**Created by:** Thorsten Gressling (gressling@paramus.ai)

## Available Models

### Compressor Models
- **Compressor**: Generic gas compressor with isentropic efficiency
- Features: Thermodynamic calculations, power consumption, dynamic response

### Pump Models  
- **Pump**: Generic liquid pump base class
- **CentrifugalPump**: Pump with quadratic head-flow characteristic
- **PositiveDisplacementPump**: Constant flow pump with variable pressure

## Quick Start Examples

### 1. Gas Compressor Example

```python
from process_control import Compressor
import numpy as np

# Create compressor
compressor = Compressor(
    eta_isentropic=0.75,         # 75% efficiency
    P_suction=1e5,               # 1 bar suction
    P_discharge=5e5,             # 5 bar discharge
    T_suction=288.15,            # 15°C inlet
    gamma=1.4,                   # Air properties
    name="ProcessCompressor"
)

# Operating point
u = np.array([1.2e5, 293.15, 6e5, 10.0])  # P_suc, T_suc, P_dis, flow

# Calculate performance
result = compressor.steady_state(u)
T_out = result[0]               # Outlet temperature [K]
Power = result[1]               # Power required [W]

print(f"Outlet: {T_out-273.15:.1f}°C, Power: {Power/1000:.1f} kW")
```

### 2. Centrifugal Pump Example

```python
from process_control import CentrifugalPump

# Create pump with performance curve
pump = CentrifugalPump(
    H0=60.0,                     # 60 m shutoff head
    K=15.0,                      # Head coefficient
    eta=0.75,                    # 75% efficiency
    name="ProcessPump"
)

# Performance analysis
flows = [0.005, 0.010, 0.015]   # Flow rates [m³/s]

for Q in flows:
    u = np.array([1e5, Q])       # Inlet pressure, flow
    result = pump.steady_state(u)
    
    P_out = result[0]            # Outlet pressure [Pa]
    Power = result[1]            # Power [W]
    
    # Calculate head
    head = (P_out - 1e5) / (1000 * 9.81)  # Convert to meters
    
    print(f"Flow: {Q*1000:.1f} L/s, Head: {head:.1f} m, Power: {Power/1000:.1f} kW")
```

### 3. System Integration Example

```python
from process_control import Compressor, CentrifugalPump

# Create system components
compressor = Compressor(eta_isentropic=0.78, name="SystemCompressor")
pump = CentrifugalPump(H0=80.0, K=25.0, eta=0.75, name="SystemPump")

# System analysis
scenarios = [
    {"comp_flow": 12.0, "pump_flow": 0.012, "name": "Normal"},
    {"comp_flow": 15.0, "pump_flow": 0.015, "name": "Peak"},
    {"comp_flow": 8.0,  "pump_flow": 0.008,  "name": "Minimum"}
]

print("Scenario    Comp Power [kW]  Pump Power [kW]  Total [kW]")
for scenario in scenarios:
    # Compressor calculation
    u_comp = np.array([1e5, 298.15, 8e5, scenario["comp_flow"]])
    comp_power = compressor.steady_state(u_comp)[1] / 1000
    
    # Pump calculation  
    u_pump = np.array([1e5, scenario["pump_flow"]])
    pump_power = pump.steady_state(u_pump)[1] / 1000
    
    total = comp_power + pump_power
    print(f"{scenario['name']:<10}  {comp_power:12.1f}  {pump_power:12.1f}  {total:9.1f}")
```

## Control System Design

### Linearization for Control

```python
from process_control import LinearApproximation, tune_pid, PIDController

# Linearize pump around operating point
pump = CentrifugalPump(H0=50.0, K=20.0, eta=0.72)
linear_approx = LinearApproximation(pump)

u_nominal = np.array([1e5, 0.01])  # Operating point
x_steady = pump.steady_state(u_nominal)

# Get linear model
A, B = linear_approx.linearize(u_nominal, x_steady)

# Step response for controller design
step_data = linear_approx.step_response(
    input_idx=1,      # Flow input
    step_size=0.002,  # 2 L/s step
    t_final=10.0
)

# Tune PI controller
from process_control import fit_fopdt
fopdt_params = fit_fopdt(step_data['t'], step_data['x'][0, :], step_magnitude=0.002)
pid_params = tune_pid(fopdt_params, method='amigo', controller_type='PI')

# Create controller
controller = PIDController(
    Kp=pid_params['Kp'],
    Ki=pid_params['Ki'],
    output_limits=(0.001, 0.02),
    name="PumpController"
)
```

## Key Features

### Compressor Features
- **Thermodynamic modeling**: Isentropic efficiency, temperature rise calculations
- **Power consumption**: Accurate power requirements based on flow and pressure ratio
- **Dynamic response**: First-order temperature dynamics for control studies
- **Multiple gases**: Configurable for different gas properties (γ, molecular weight)

### Pump Features  
- **Performance curves**: Head vs. flow characteristics for centrifugal pumps
- **Pump types**: Generic, centrifugal, and positive displacement models
- **Efficiency modeling**: Power consumption based on hydraulic and mechanical efficiency
- **Dynamic response**: Pressure dynamics for control system design

### Integration Capabilities
- **System modeling**: Combine with reactors, heat exchangers, separators
- **Control design**: Linearization support for PID and advanced control
- **Optimization**: Energy optimization across multiple equipment items
- **Safety systems**: Support for surge protection, cavitation prevention

## Applications

### Industrial Applications
- **Gas compression**: Pipeline, process gas, refrigeration systems
- **Liquid pumping**: Process fluids, cooling water, chemical transfer
- **Energy systems**: Power plants, renewable energy integration
- **Manufacturing**: Chemical, petrochemical, pharmaceutical processes

### Academic Use
- **Process dynamics**: Understanding fluid machinery behavior
- **Control systems**: Design and tuning of pump/compressor controllers  
- **System integration**: Multi-unit process simulation
- **Energy analysis**: Efficiency optimization studies

## Best Practices

### Model Selection
- Use **Compressor** for gas compression with known efficiency
- Use **CentrifugalPump** when head-flow curve is important
- Use **PositiveDisplacementPump** for constant flow applications
- Consider **Generic Pump** for simplified analyses

### Control Design
- Linearize around normal operating conditions
- Consider surge/cavitation limits in controller design
- Use cascade control for improved performance
- Implement safety interlocks and protection systems

### Performance Optimization
- Monitor efficiency in real-time
- Use variable speed drives for energy savings
- Implement predictive maintenance strategies
- Consider system-wide optimization

## See Also
- Process Control Examples: `examples.py` functions 15-18
- Integration Examples: Heat exchanger + pump systems
- Control Design: PID tuning for fluid machinery
- System Optimization: Multi-equipment energy minimization
