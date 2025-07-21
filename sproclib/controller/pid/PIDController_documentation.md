# PID Controller Documentation

## Overview and Use Case
Three-term controller providing proportional, integral, and derivative control action for process regulation. Standard feedback controller for single-input single-output (SISO) systems in chemical process control.

## Physical/Chemical Principles
**Control Equation**: u(t) = Kp·e(t) + Ki·∫e(t)dt + Kd·de(t)/dt

Where:
- e(t) = setpoint - process_variable (control error)
- Kp = proportional gain [output_units/input_units]
- Ki = integral gain [output_units/(input_units·s)]
- Kd = derivative gain [output_units·s/input_units]

**Transfer Function**: C(s) = Kp + Ki/s + Kd·s

**Physical Actions**:
- Proportional: Immediate response proportional to current error
- Integral: Eliminates steady-state offset, responds to error history
- Derivative: Anticipatory action based on error rate of change

## Process Parameters
| Parameter | Typical Range | Units | Description |
|-----------|---------------|-------|-------------|
| Kp | 0.1 - 10 | process dependent | Proportional gain |
| Ki | 0.01 - 5 | 1/s | Integral gain |
| Kd | 0 - 60 | s | Derivative gain |
| Output limits | ±100% | % or engineering units | Actuator constraints |
| Sample time | 0.1 - 10 | s | Control execution frequency |

## Operating Conditions
- **Temperature control**: 50-500°C, response times 1-30 minutes
- **Flow control**: 0.1-1000 m³/h, response times 1-60 seconds  
- **Pressure control**: 1-50 bar, response times 5-300 seconds
- **Level control**: 10-90% tank capacity, response times 2-60 minutes

## Industrial Applications
- **Reactor temperature control**: Jacket cooling/heating systems
- **Distillation column control**: Reflux ratio, reboiler duty regulation
- **Heat exchanger control**: Outlet temperature via bypass or utility flow
- **Pump flow control**: Variable speed drives or control valve manipulation
- **Pressure vessel control**: Vent valve or compressor speed regulation

## Limitations and Assumptions
- Linear process behavior around operating point
- Constant process parameters (gain, time constants)
- Single-input single-output systems only
- Derivative action sensitive to measurement noise
- Integral windup during actuator saturation
- Cannot handle pure dead time effectively

## Key References
1. Åström, K.J. & Hägglund, T. (2006). *Advanced PID Control*. ISA Press.
2. Stephanopoulos, G. (1984). *Chemical Process Control*. Prentice Hall.
3. Seborg, D.E. et al. (2016). *Process Dynamics and Control*, 4th Edition. Wiley.
