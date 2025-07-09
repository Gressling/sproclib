# dynamics Function Documentation

## Overview

The `dynamics` functions in the liquid transport models simulate time-dependent behavior and transient responses of flow systems. These functions solve differential equations that govern unsteady flow, accounting for fluid inertia, system compliance, and time-varying conditions.

## Scientific Background

### Dynamic Flow Analysis Principles

Dynamic analysis captures the time-dependent behavior of flow systems, essential for:

1. **Control System Design:** Understanding process dynamics for controller tuning
2. **Transient Analysis:** Predicting system response to disturbances
3. **Safety Analysis:** Evaluating emergency shutdown scenarios
4. **Optimization:** Dynamic optimization of process operations
5. **Startup/Shutdown:** Modeling non-steady operations

### Mathematical Foundation

Dynamic flow systems are governed by time-dependent differential equations:

#### Momentum Conservation (Unsteady Flow)

For pipe flow, the momentum equation becomes:

```
ρL(dv/dt) = ΔP_applied - ΔP_friction - ΔP_gravity
```

Expanded form:
```
ρL(dv/dt) = P_in - P_out - f(L/D)(ρv²/2) - ρgΔh
```

#### Mass Conservation (Compressibility Effects)

For slightly compressible systems:
```
dρ/dt + ∇·(ρv) = 0
```

#### State Space Representation

The system can be represented as:
```
dx/dt = f(x, u, t)
y = g(x, u, t)
```

Where:
- x = state variables (velocities, concentrations, etc.)
- u = input variables (flow rates, pump speeds, etc.)
- y = output variables (pressures, flow rates, etc.)

### Time Scales and Dynamic Phenomena

#### Fast Dynamics (Milliseconds to Seconds)

1. **Pressure Wave Propagation:** Sound speed effects in fluids
2. **Valve Opening/Closing:** Rapid flow changes
3. **Pump Startup:** Motor acceleration dynamics

#### Medium Dynamics (Seconds to Minutes)

1. **Flow Establishment:** Momentum building in long pipelines
2. **Temperature Changes:** Thermal effects on fluid properties
3. **Control Loop Response:** Feedback control adjustments

#### Slow Dynamics (Minutes to Hours)

1. **Concentration Changes:** Mixing and transport in large systems
2. **Fouling Buildup:** Gradual performance degradation
3. **Thermal Equilibration:** Heat transfer to surroundings

## Implementation in Transport Models

### PipeFlow.dynamics()

**Purpose:** Simulates dynamic pipe flow response including fluid inertia and compressibility effects.

**Input Parameters:**
- `flow_rate` (float): Current volumetric flow rate [m³/s]
- `time_step` (float): Integration time step [s]

**Mathematical Model:**

The pipe dynamics are modeled using the unsteady momentum equation:

```python
# State variables
x[0] = velocity  # Current pipe velocity [m/s]

# Governing equation
dv_dt = (pressure_applied - pressure_friction - pressure_gravity) / (density * length)

# Friction pressure (velocity-dependent)
pressure_friction = friction_factor * (length/diameter) * (density * velocity * abs(velocity)) / 2

# Integration (Explicit Euler)
velocity_new = velocity + dv_dt * time_step
```

**Key Features:**
1. **Fluid Inertia:** Accounts for momentum changes in pipe flow
2. **Nonlinear Friction:** Quadratic velocity dependence
3. **Gravity Effects:** Elevation changes impact dynamics
4. **Stability Monitoring:** Automatic time step adjustment

**Output Dictionary:**
- `velocity`: Updated flow velocity [m/s]
- `flow_rate`: Volumetric flow rate [m³/s]
- `pressure_drop`: Instantaneous pressure loss [Pa]
- `acceleration`: Flow acceleration [m/s²]
- `time_constant`: Characteristic response time [s]

### PeristalticFlow.dynamics()

**Purpose:** Simulates peristaltic pump dynamics including pulsation effects and tube compliance.

**Input Parameters:**
- `pump_speed` (float): Current pump speed [rpm]
- `time_step` (float): Integration time step [s]

**Mathematical Model:**

Peristaltic pump dynamics include multiple phenomena:

```python
# Pulsation modeling
pulsation_frequency = pump_speed / 60 * number_of_rollers  # Hz
pulsation_phase = 2 * π * pulsation_frequency * current_time

# Instantaneous flow rate
flow_base = steady_state_flow(pump_speed)
flow_pulsation = pulsation_amplitude * sin(pulsation_phase)
flow_instantaneous = flow_base * (1 + flow_pulsation)

# Tube compliance effects
tube_pressure = calculate_tube_pressure(flow_instantaneous)
compliance_correction = tube_compliance * d(tube_pressure)/dt

# System dynamics
flow_output = flow_instantaneous + compliance_correction
```

**Key Features:**
1. **Pulsation Modeling:** Sinusoidal flow variation with pump rotation
2. **Tube Compliance:** Elastic effects of flexible tubing
3. **Multi-Roller Effects:** Phase relationships between compression points
4. **Damping Mechanisms:** Viscous and elastic damping

**Output Dictionary:**
- `flow_rate`: Instantaneous flow rate [m³/s]
- `pulsation_amplitude`: Current pulsation magnitude [-]
- `tube_pressure`: Internal tube pressure [Pa]
- `compliance_effect`: Elastic flow contribution [m³/s]
- `phase_angle`: Current pulsation phase [rad]

### SlurryPipeline.dynamics()

**Purpose:** Simulates dynamic slurry transport including particle settling and concentration evolution.

**Input Parameters:**
- `flow_rate` (float): Current slurry flow rate [m³/s]
- `time_step` (float): Integration time step [s]

**Mathematical Model:**

Slurry dynamics involve coupled momentum and concentration equations:

```python
# State variables
x[0] = velocity          # Average flow velocity [m/s]
x[1] = concentration     # Local solid concentration [-]

# Momentum equation (similar to pipe flow but with mixture properties)
mixture_density = concentration * solid_density + (1 - concentration) * fluid_density
mixture_viscosity = calculate_mixture_viscosity(concentration)

dv_dt = (pressure_applied - pressure_friction_mixture - pressure_gravity) / (mixture_density * length)

# Concentration evolution (settling and mixing)
settling_velocity = calculate_settling_velocity(particle_diameter, densities, viscosity)
mixing_diffusivity = calculate_mixing_diffusivity(turbulence_level)

dc_dt = -settling_velocity * concentration / characteristic_height + 
        mixing_diffusivity * d²c_dx²

# Integration
velocity_new = velocity + dv_dt * time_step
concentration_new = concentration + dc_dt * time_step
```

**Key Features:**
1. **Particle Settling:** Gravitational settling with Stokes/Newton drag
2. **Concentration Evolution:** Time-dependent spatial distribution
3. **Mixture Properties:** Concentration-dependent density and viscosity
4. **Flow Regime Transitions:** Dynamic switching between transport modes

**Output Dictionary:**
- `velocity`: Current mixture velocity [m/s]
- `concentration`: Solid concentration distribution [-]
- `settling_rate`: Particle settling velocity [m/s]
- `mixture_density`: Time-varying mixture density [kg/m³]
- `transport_regime`: Current flow regime classification

## Numerical Integration Methods

### Explicit Methods

**Euler Method (First-Order):**
```python
x_new = x_old + f(x_old, t) * dt
```
- Simple implementation
- Stability limited by time step
- Used for non-stiff systems

**Runge-Kutta 4th Order:**
```python
k1 = f(x, t) * dt
k2 = f(x + k1/2, t + dt/2) * dt
k3 = f(x + k2/2, t + dt/2) * dt
k4 = f(x + k3, t + dt) * dt
x_new = x + (k1 + 2*k2 + 2*k3 + k4) / 6
```
- Higher accuracy
- Better stability properties
- Moderate computational cost

### Implicit Methods

**Backward Euler:**
```python
x_new = x_old + f(x_new, t_new) * dt
```
- Requires iterative solution
- Excellent stability for stiff systems
- Used for fast dynamics

### Adaptive Methods

**Variable Time Step:**
```python
# Error estimation
error = estimate_truncation_error(x_old, x_new, dt)

# Time step adjustment
if error > tolerance:
    dt = dt * 0.5  # Reduce time step
elif error < tolerance/10:
    dt = dt * 1.5  # Increase time step
```

## Stability and Convergence

### Stability Criteria

**CFL Condition (Courant-Friedrichs-Lewy):**
```
dt ≤ dx / (|v| + c)
```
Where c is the speed of sound in the fluid.

**Diffusion Stability:**
```
dt ≤ dx² / (2 * diffusivity)
```

**Viscous Stability:**
```
dt ≤ ρ * dx² / (2 * μ)
```

### Convergence Monitoring

```python
# Convergence check
residual = |x_new - x_old| / max(|x_new|, small_number)
if residual < convergence_tolerance:
    converged = True
```

### Error Control

1. **Truncation Error:** From finite difference approximations
2. **Round-off Error:** From floating-point arithmetic
3. **Physical Bounds:** Enforcement of realistic values

## Common Dynamic Phenomena

### Water Hammer

High-frequency pressure waves in liquid systems:

```python
# Wave speed in pipe
wave_speed = sqrt(bulk_modulus / density) / sqrt(1 + (D*bulk_modulus)/(E*t))

# Pressure rise from sudden valve closure
pressure_rise = density * wave_speed * velocity_change
```

### Flow Oscillations

Self-sustained oscillations in flow systems:

```python
# Natural frequency of pipe system
natural_frequency = wave_speed / (4 * length)

# Damping ratio
damping_ratio = friction_factor / (2 * sqrt(inertia * compliance))
```

### Startup Transients

Flow establishment in initially static systems:

```python
# Time constant for momentum building
time_constant = length / sqrt(pressure_driving / (density * length))

# Exponential approach to steady state
velocity(t) = velocity_final * (1 - exp(-t / time_constant))
```

## Validation and Testing

### Analytical Solutions

For simple cases, analytical solutions exist:

```python
# Step response of first-order system
velocity_analytical = V_final * (1 - exp(-t / tau))

# Compare with numerical solution
error = abs(velocity_numerical - velocity_analytical)
```

### Experimental Validation

1. **Flow Meter Data:** Time-resolved flow measurements
2. **Pressure Transducers:** Dynamic pressure recordings
3. **PIV/LDV:** Velocity field measurements
4. **High-Speed Imaging:** Visual confirmation of phenomena

### Benchmark Problems

Standard test cases for validation:

1. **Sudden Valve Closure:** Water hammer analysis
2. **Pump Startup:** Transient flow establishment
3. **Oscillatory Flow:** Pulsating boundary conditions
4. **Multi-phase Slugging:** Complex transient behavior

## Performance Optimization

### Computational Efficiency

1. **Vectorization:** Process multiple time steps simultaneously
2. **Sparse Matrices:** Efficient storage for large systems
3. **Parallel Processing:** Multi-threaded integration
4. **GPU Acceleration:** High-performance computing

### Memory Management

```python
# Circular buffer for time history
history_buffer = np.zeros((buffer_size, n_variables))
current_index = 0

# Store current state
history_buffer[current_index % buffer_size] = current_state
current_index += 1
```

### Algorithm Selection

Choose integration method based on system characteristics:

```python
# Stiffness detection
jacobian = calculate_jacobian(f, x)
eigenvalues = np.linalg.eigvals(jacobian)
stiffness_ratio = max(real_parts) / min(real_parts)

if stiffness_ratio > 1000:
    # Use implicit method
    integrator = BackwardEuler()
else:
    # Use explicit method
    integrator = RungeKutta4()
```

## Applications in Control Systems

### Model Predictive Control (MPC)

Dynamic models enable prediction:

```python
# Predict future states
for i in range(prediction_horizon):
    x_pred[i+1] = model.dynamics(x_pred[i], u_pred[i], dt)

# Optimize control sequence
u_optimal = minimize(objective_function, u_pred, constraints)
```

### State Estimation

Use dynamic models for Kalman filtering:

```python
# Prediction step
x_pred = model.dynamics(x_est, u_measured, dt)
P_pred = F @ P_est @ F.T + Q  # Covariance prediction

# Update step (when measurements available)
K = P_pred @ H.T @ inv(H @ P_pred @ H.T + R)  # Kalman gain
x_est = x_pred + K @ (y_measured - H @ x_pred)
```

### Fault Detection

Monitor deviations from predicted behavior:

```python
# Residual generation
y_predicted = model.dynamics(x_estimated, u_actual, dt)
residual = y_measured - y_predicted

# Fault detection
if abs(residual) > threshold:
    trigger_alarm("Process deviation detected")
```

## Scientific References

1. **Wylie, E.B., & Streeter, V.L.** (1993). *Fluid Transients in Systems*. Prentice Hall.
   - Comprehensive treatment of unsteady flow dynamics

2. **Chaudhry, M.H.** (2014). *Applied Hydraulic Transients*, 3rd Edition. Springer.
   - Practical applications of dynamic flow analysis

3. **Strang, G.** (2007). *Computational Science and Engineering*. Wellesley-Cambridge Press.
   - Numerical methods for differential equations

4. **Ascher, U.M., & Petzold, L.R.** (1998). *Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations*. SIAM.
   - Advanced numerical integration techniques

5. **Butcher, J.C.** (2016). *Numerical Methods for Ordinary Differential Equations*, 3rd Edition. John Wiley & Sons.
   - Detailed treatment of ODE integration methods

## Example Usage Patterns

### Single Step Integration

```python
# Initialize state
initial_flow = 0.01  # m³/s
dt = 0.1  # seconds

# Single dynamics step
result = pipe_model.dynamics(initial_flow, dt)
new_flow = result['flow_rate']
```

### Time Series Simulation

```python
# Time series setup
t_start, t_end = 0, 100  # seconds
dt = 0.01
time_points = np.arange(t_start, t_end, dt)
n_steps = len(time_points)

# Initialize arrays
flow_history = np.zeros(n_steps)
pressure_history = np.zeros(n_steps)

# Time integration loop
current_flow = initial_flow
for i, t in enumerate(time_points):
    result = model.dynamics(current_flow, dt)
    current_flow = result['flow_rate']
    
    flow_history[i] = current_flow
    pressure_history[i] = result['pressure_drop']

# Plot results
plt.subplot(2,1,1)
plt.plot(time_points, flow_history)
plt.ylabel('Flow Rate (m³/s)')

plt.subplot(2,1,2)
plt.plot(time_points, pressure_history)
plt.ylabel('Pressure Drop (Pa)')
plt.xlabel('Time (s)')
```

### Disturbance Response

```python
# Step disturbance at t = 50s
for i, t in enumerate(time_points):
    if t < 50:
        input_flow = 0.01  # Normal operation
    else:
        input_flow = 0.015  # 50% increase
    
    result = model.dynamics(input_flow, dt)
    # Process result...
```

## Limitations and Considerations

### Model Assumptions

1. **Lumped Parameters:** Spatial variations are averaged
2. **Linear Friction:** May not hold for all flow regimes
3. **Incompressible Flow:** Limited compressibility effects
4. **Uniform Properties:** Constant fluid properties

### Numerical Limitations

1. **Time Step Restrictions:** Stability requirements
2. **Accumulation Errors:** Long-term integration drift
3. **Stiffness Issues:** Fast and slow dynamics together
4. **Boundary Conditions:** Proper specification required

### Physical Validity

1. **Conservation Laws:** Mass and momentum must be preserved
2. **Thermodynamic Consistency:** Entropy and energy constraints
3. **Causality:** Effects cannot precede causes
4. **Physical Bounds:** Realistic limits on variables

## Future Enhancements

- **Higher-order integration** methods for improved accuracy
- **Adaptive mesh refinement** for spatial resolution
- **Multi-scale modeling** for different time scales
- **Uncertainty propagation** through dynamic simulations
- **Machine learning** enhanced modeling approaches
- **Real-time optimization** integration capabilities
