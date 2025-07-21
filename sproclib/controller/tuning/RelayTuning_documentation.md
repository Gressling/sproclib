# RelayTuning Documentation

The RelayTuning class implements relay-based auto-tuning methods for PID controllers in chemical process systems. This approach uses relay feedback to automatically identify critical process characteristics and calculate optimal PID parameters without requiring manual step tests or process models.

## Theory and Applications

Relay auto-tuning, pioneered by Åström and Hägglund in 1984, revolutionized industrial controller tuning by providing:

- **Automated parameter identification** without operator intervention
- **Continuous operation** during tuning process
- **Robust identification** even with process noise and disturbances
- **Safety through controlled oscillation** with bounded amplitude

The method is particularly valuable in chemical engineering where:

- **Manual tuning is time-consuming** and requires skilled operators
- **Process models are unavailable** or uncertain
- **Safety requirements** prevent large process upsets
- **Continuous operation** must be maintained during tuning

### Mathematical Foundation

**Relay Feedback Principle**

The relay creates controlled oscillations by switching the controller output between two levels based on the process variable:

u(t) = u₀ + d × sign(e(t))

Where:
- u₀ = Bias level (typically current operating point)
- d = Relay amplitude (tuning parameter)
- e(t) = Error signal (setpoint - measurement)

**Critical Point Identification**

From the sustained oscillation:
- Ultimate gain: Ku = 4d/(π×a)
- Ultimate period: Pu = oscillation period
- Ultimate frequency: ωu = 2π/Pu

Where 'a' is the amplitude of process variable oscillation.

**PID Parameter Calculation**

Using Ziegler-Nichols equivalent relationships:
- Kc = 0.6 × Ku (proportional gain)
- τI = 0.5 × Pu (integral time)
- τD = 0.125 × Pu (derivative time)

### Advanced Relay Methods

**Asymmetric Relay**

For processes with asymmetric behavior:

u(t) = u₀ + d₁ (when e(t) > 0)
u(t) = u₀ - d₂ (when e(t) < 0)

**Relay with Hysteresis**

To reduce noise sensitivity:

Switch up when e(t) > +ε
Switch down when e(t) < -ε

Where ε is the hysteresis band.

**Relay with Dead Zone**

For noisy processes:

u(t) = u₀ + d × sign(e(t)) when |e(t)| > δ
u(t) = u₀ when |e(t)| ≤ δ

## Industrial Applications

### CSTR Temperature Control

For continuous stirred tank reactor with exothermic reaction:

**Process Characteristics:**
- Temperature range: 320-380 K
- Control via cooling water flow
- Safety-critical (thermal runaway risk)

**Relay Test Configuration:**
- Relay amplitude: ±2 L/min (5% of maximum flow)
- Hysteresis: ±0.5 K (noise reduction)
- Test duration: 3-4 oscillation cycles

**Typical Results:**
- Ultimate gain: Ku = 8.5 (L/min)/K
- Ultimate period: Pu = 12 minutes
- PID parameters: Kc = 5.1, τI = 6.0 min, τD = 1.5 min

**Safety Benefits:**
- Controlled oscillation amplitude (±3 K)
- Automatic termination if bounds exceeded
- Continuous monitoring of reaction conditions

### Distillation Column Composition Control

For top composition control via reflux ratio:

**Process Challenges:**
- Long dead times (5-15 minutes)
- Measurement noise from gas chromatograph
- Strong interaction with bottom composition loop

**Relay Configuration:**
- Asymmetric relay (composition control is directional)
- d₁ = +0.2 reflux ratio increase
- d₂ = -0.1 reflux ratio decrease
- Hysteresis: ±0.2 mol% (GC noise tolerance)

**Identification Results:**
- Ku = 12.3 (reflux ratio change per mol%)
- Pu = 25 minutes (includes analyzer delay)
- Modified tuning for robustness: Kc = 0.4×Ku = 4.9

**Performance Improvements:**
- 40% faster disturbance rejection vs. manual tuning
- Reduced composition variance by 60%
- Improved separation efficiency

### Heat Exchanger Network Control

For multi-pass heat exchanger outlet temperature:

**System Complexity:**
- Multiple thermal time constants
- Steam flow valve nonlinearities  
- Interaction with upstream processes

**Relay Test Setup:**
- Pretest: Valve characterization
- Relay amplitude: 8% valve position
- Dead zone: ±1 °C (thermal noise)
- Multiple tests at different operating points

**Adaptive Features:**
- Gain scheduling for different loads
- Seasonal adjustment for ambient conditions
- Automatic retuning on significant process changes

## Design Guidelines

### Test Configuration

**Relay Amplitude Selection:**

For temperature processes:
- d = 2-5% of normal operating range
- Ensure valve/actuator can respond
- Consider downstream equipment limits

For composition processes:
- d = 0.1-0.5% of specification range
- Account for analyzer measurement delays
- Minimize impact on product quality

For pressure/flow processes:
- d = 1-3% of operating range
- Faster dynamics allow smaller amplitudes
- Consider system pressure ratings

**Hysteresis Selection:**

General rule: ε = 2-3 × measurement noise level

Temperature: ε = 0.5-2 °C
Composition: ε = 0.1-0.5 mol%
Pressure: ε = 0.02-0.1 bar
Flow: ε = 1-3% of range

### Safety Protocols

**Pre-Test Verification:**
- Confirm process at steady state
- Check all safety interlocks active
- Verify manual control capability
- Set emergency stop conditions

**Test Monitoring:**
- Continuous operator oversight
- Automatic amplitude limiting
- Oscillation bounds checking
- Emergency termination triggers

**Post-Test Validation:**
- Parameter reasonableness check
- Simulation before implementation
- Gradual transition to auto mode
- Performance monitoring

## Implementation Procedures

### Automated Relay Test

```python
class RelayAutoTuner:
    def __init__(self, process_interface):
        self.process = process_interface
        self.relay_amplitude = 0.0
        self.hysteresis = 0.0
        self.test_active = False
        
    def configure_test(self, amplitude_pct, hysteresis_units):
        """Configure relay test parameters"""
        operating_range = self.process.get_operating_range()
        self.relay_amplitude = operating_range * amplitude_pct / 100
        self.hysteresis = hysteresis_units
        
    def execute_relay_test(self, duration_cycles=4):
        """Execute automated relay test"""
        # Initialize
        start_output = self.process.get_current_output()
        setpoint = self.process.get_setpoint()
        
        # Data collection
        time_data = []
        pv_data = []
        output_data = []
        
        # Test execution
        self.test_active = True
        cycle_count = 0
        
        while cycle_count < duration_cycles and self.test_active:
            # Read process variable
            pv = self.process.read_measurement()
            error = setpoint - pv
            
            # Relay logic with hysteresis
            if error > self.hysteresis:
                output = start_output + self.relay_amplitude
            elif error < -self.hysteresis:
                output = start_output - self.relay_amplitude
            else:
                output = start_output  # Dead zone
                
            # Apply output
            self.process.set_output(output)
            
            # Log data
            time_data.append(time.time())
            pv_data.append(pv)
            output_data.append(output)
            
            # Safety checks
            if self.check_safety_limits(pv, output):
                self.terminate_test("Safety limit exceeded")
                break
                
            # Cycle counting (detect zero crossings)
            cycle_count = self.count_oscillation_cycles(pv_data)
            
            time.sleep(self.process.sample_time)
            
        return {
            'time': time_data,
            'pv': pv_data, 
            'output': output_data,
            'cycles_completed': cycle_count
        }
```

### Parameter Calculation

```python
def calculate_pid_from_relay(test_data):
    """Calculate PID parameters from relay test data"""
    
    # Extract oscillation characteristics
    pv_signal = np.array(test_data['pv'])
    output_signal = np.array(test_data['output'])
    time_vector = np.array(test_data['time'])
    
    # Find oscillation amplitude
    pv_max = np.max(pv_signal[-len(pv_signal)//2:])  # Last half of test
    pv_min = np.min(pv_signal[-len(pv_signal)//2:])
    oscillation_amplitude = (pv_max - pv_min) / 2
    
    # Find ultimate period from zero crossings
    mean_pv = np.mean(pv_signal[-len(pv_signal)//2:])
    zero_crossings = find_zero_crossings(pv_signal - mean_pv)
    
    if len(zero_crossings) >= 4:
        # Calculate period from multiple cycles
        periods = []
        for i in range(len(zero_crossings)-2):
            period = 2 * (time_vector[zero_crossings[i+2]] - 
                         time_vector[zero_crossings[i]])
            periods.append(period)
        ultimate_period = np.mean(periods)
    else:
        raise ValueError("Insufficient oscillation cycles for identification")
    
    # Calculate ultimate gain
    relay_amplitude = np.mean(np.abs(output_signal - np.mean(output_signal)))
    ultimate_gain = (4 * relay_amplitude) / (np.pi * oscillation_amplitude)
    
    # Calculate PID parameters (Ziegler-Nichols equivalent)
    pid_params = {
        'Kc': 0.6 * ultimate_gain,
        'tau_I': 0.5 * ultimate_period,
        'tau_D': 0.125 * ultimate_period,
        'ultimate_gain': ultimate_gain,
        'ultimate_period': ultimate_period
    }
    
    return pid_params
```

## Performance Optimization

### Modified Relay Methods

**Bias Compensation:**

For processes with load disturbances during testing:

```python
def bias_compensated_relay(error, previous_outputs, compensation_factor=0.1):
    """Relay with automatic bias compensation"""
    
    # Calculate bias drift
    recent_outputs = previous_outputs[-10:]  # Last 10 samples
    bias_drift = np.mean(recent_outputs) - previous_outputs[0]
    
    # Compensate relay center point
    bias_compensation = compensation_factor * bias_drift
    
    # Standard relay logic with compensation
    if error > hysteresis:
        output = nominal_output + relay_amplitude - bias_compensation
    elif error < -hysteresis:
        output = nominal_output - relay_amplitude - bias_compensation
    else:
        output = nominal_output - bias_compensation
        
    return output
```

**Frequency Response Enhancement:**

For better frequency domain identification:

```python
def multisine_relay_test(frequencies, amplitudes):
    """Multi-frequency relay test for enhanced identification"""
    
    test_signal = 0
    for freq, amp in zip(frequencies, amplitudes):
        test_signal += amp * np.sin(2 * np.pi * freq * time)
    
    # Apply through relay mechanism
    relay_output = relay_amplitude * np.sign(test_signal)
    
    return relay_output
```

### Robustness Enhancements

**Adaptive Amplitude:**

```python
def adaptive_relay_amplitude(error_history, target_oscillation=5.0):
    """Automatically adjust relay amplitude for target oscillation"""
    
    current_oscillation = np.std(error_history[-50:])  # Recent standard deviation
    
    if current_oscillation < 0.8 * target_oscillation:
        # Increase amplitude for larger oscillation
        amplitude_adjustment = 1.2
    elif current_oscillation > 1.2 * target_oscillation:
        # Decrease amplitude for smaller oscillation
        amplitude_adjustment = 0.8
    else:
        amplitude_adjustment = 1.0
        
    return amplitude_adjustment
```

## Economic Benefits

### Quantified Improvements

**Tuning Time Reduction:**
- Manual tuning: 4-8 hours per loop
- Relay auto-tuning: 20-60 minutes per loop
- Time savings: 80-90% reduction

**Performance Improvements:**
- Settling time: 20-40% faster
- Overshoot: 30-50% reduction
- Energy consumption: 5-15% decrease
- Product quality variance: 25-60% reduction

**Maintenance Benefits:**
- Consistent tuning across all loops
- Reduced operator training requirements
- Automatic retuning capability
- Documentation of tuning parameters

### Return on Investment

**Typical Chemical Plant (100 control loops):**

Implementation costs:
- Software integration: $50,000
- Engineering time: $30,000
- Commissioning: $20,000
- Total: $100,000

Annual benefits:
- Energy savings: $200,000
- Quality improvements: $300,000
- Maintenance reduction: $100,000
- Operator productivity: $150,000
- Total: $750,000

**ROI: 650% first year**

## Advanced Applications

### Multivariable Relay Tuning

For interacting control loops:

```python
def sequential_relay_tuning(loop_list, interaction_matrix):
    """Sequential relay tuning for interacting loops"""
    
    tuned_parameters = {}
    
    for loop in loop_list:
        # Identify interaction effects
        interaction_level = calculate_interaction_strength(loop, interaction_matrix)
        
        # Adjust relay parameters for interaction
        adjusted_amplitude = base_amplitude * (1 - 0.3 * interaction_level)
        
        # Perform relay test
        test_results = execute_relay_test(loop, adjusted_amplitude)
        
        # Calculate detuned parameters
        raw_params = calculate_pid_from_relay(test_results)
        detuned_params = apply_interaction_detuning(raw_params, interaction_level)
        
        tuned_parameters[loop.name] = detuned_params
        
    return tuned_parameters
```

### Adaptive Relay Tuning

For time-varying processes:

```python
class AdaptiveRelayTuner:
    def __init__(self, retune_threshold=0.3):
        self.retune_threshold = retune_threshold
        self.last_tune_params = None
        self.performance_monitor = PerformanceMonitor()
        
    def monitor_and_retune(self, controller, process):
        """Monitor performance and retune when needed"""
        
        # Calculate current performance metrics
        current_performance = self.performance_monitor.assess(controller)
        
        # Check if retuning is needed
        if self.needs_retuning(current_performance):
            print("Performance degradation detected. Initiating relay retune...")
            
            # Execute new relay test
            new_params = self.execute_relay_test(process)
            
            # Smooth parameter transition
            smoothed_params = self.smooth_parameter_transition(
                self.last_tune_params, new_params)
            
            # Update controller
            controller.update_parameters(smoothed_params)
            self.last_tune_params = smoothed_params
            
            return True
        
        return False
```

Relay auto-tuning represents a significant advancement in automatic controller tuning technology, providing chemical process engineers with a powerful tool for achieving optimal control performance while maintaining operational safety and minimizing process disruption.
