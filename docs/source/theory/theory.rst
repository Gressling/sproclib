Theory and Background
====================

This section provides the mathematical and theoretical background for the Standard Process Control Library.

Control Theory Fundamentals
----------------------------

Transfer Functions
~~~~~~~~~~~~~~~~~~

A transfer function represents the relationship between the input and output of a linear time-invariant system in the Laplace domain::

   G(s) = Y(s)/U(s) = (b_m*s^m + ... + b_1*s + b_0)/(a_n*s^n + ... + a_1*s + a_0)

where s is the Laplace variable, Y(s) is the output, and U(s) is the input.

**Common Process Models:**

1. **First-Order Plus Dead Time (FOPDT):**

   ::

      G(s) = K * exp(-θ*s) / (τ*s + 1)
   
   Where:
   - K = Process gain
   - τ = Time constant
   - θ = Dead time

2. **Second-Order System:**

   ::

      G(s) = K * ωn² / (s² + 2*ζ*ωn*s + ωn²)
   
   Where:
   - ζ = Damping ratio
   - ωn = Natural frequency

PID Control
~~~~~~~~~~~

The PID controller implements proportional, integral, and derivative control actions:

**Time Domain:**

::

   u(t) = Kp*e(t) + Ki*∫[0 to t]e(τ)dτ + Kd*de(t)/dt

**Frequency Domain:**

::

   C(s) = Kp + Ki/s + Kd*s

**Practical PID (with derivative filter):**

::

   C(s) = Kp + Ki/s + (Kd*s)/(τd*s + 1)

where τd is the derivative time constant (typically τd = Kd/(8*Kp)).

Process Modeling
----------------

Chemical Reactor Models
~~~~~~~~~~~~~~~~~~~~~~~

**Continuous Stirred Tank Reactor (CSTR):**

The CSTR model combines material and energy balances:

*Material Balance:*

::

   V * dCA/dt = q*(CA,in - CA) - V*rA

*Energy Balance:*

::

   V*ρ*Cp * dT/dt = q*ρ*Cp*(Tin - T) + (-ΔHr)*V*rA + Q

where:
- rA = Reaction rate (typically Arrhenius: k0*exp(-E/RT)*CA^n)
- Q = Heat transfer rate: UA*(Tcool - T)

**Tank Level Control:**

For a gravity-drained tank::

   A * dh/dt = qin - Cv*√h

where:
- A = Tank cross-sectional area
- h = Liquid height
- Cv = Valve coefficient

Linearization
~~~~~~~~~~~~~

For nonlinear systems ẋ = f(x,u), linearization around operating point (x0, u0) gives::

   Δẋ = A*Δx + B*Δu

where::

   A = ∂f/∂x|_(x0,u0),    B = ∂f/∂u|_(x0,u0)

**Example - Tank Linearization:**

For the tank equation around h0, qin,0::

   A = -Cv/(2*√h0),    B = 1/Atank

Frequency Domain Analysis
-------------------------

Bode Plots
~~~~~~~~~~

Bode plots show the frequency response of a system:

**Magnitude Plot:**

::

   |G(jω)| in dB = 20*log10(|G(jω)|)

**Phase Plot:**

::

   ∠G(jω) in degrees

**Key Features:**

- **Gain crossover frequency** (ωgc): Where |G(jω)| = 1 (0 dB)
- **Phase crossover frequency** (ωpc): Where ∠G(jω) = -180°

Stability Analysis
~~~~~~~~~~~~~~~~~~

**Gain Margin (GM):**

::

   GM_dB = -20*log10(|G(jωpc)|)

**Phase Margin (PM):**

::

   PM = 180° + ∠G(jωgc)

**Stability Criteria:**

- System is stable if GM > 0 dB AND PM > 0°
- Good stability: GM > 6 dB, PM > 30°

Controller Tuning Methods
-------------------------

Ziegler-Nichols Tuning
~~~~~~~~~~~~~~~~~~~~~~

Based on process reaction curve (step response):

1. **Identify FOPDT parameters** from step response
2. **Apply tuning rules:**

   ===============  ==============  ==============  ==============
   Controller Type  Kp              Ti              Td
   ===============  ==============  ==============  ==============
   P                τ/(K*θ)         —               —
   PI               0.9*τ/(K*θ)     3.3*θ           —
   PID              1.2*τ/(K*θ)     2*θ             0.5*θ
   ===============  ==============  ==============  ==============

AMIGO Tuning
~~~~~~~~~~~~

Advanced Method for Integrating and General Oscillatory processes:

**For FOPDT processes:**

::

   Kp = (1/K) * (0.15 + 0.35*τ/(τ + θ))

::

   Ti = 0.35*τ + (13*τ*θ)/(τ + 12*θ)

::

   Td = (0.5*τ*θ)/(τ + 0.5*θ)

Optimization Theory
-------------------

Linear Programming
~~~~~~~~~~~~~~~~~~

Standard form::

   min  c^T * x
    x

   subject to:  A*x ≤ b,  x ≥ 0

**Solved using:** Simplex method, Interior point methods

Nonlinear Programming
~~~~~~~~~~~~~~~~~~~~~

General form::

   min  f(x)
    x

   subject to:  gi(x) ≤ 0,  hj(x) = 0

**Solution methods:**
- Sequential Quadratic Programming (SQP)
- Interior Point Methods
- Gradient-based methods

Model Predictive Control
------------------------

MPC Formulation
~~~~~~~~~~~~~~~

At each time step, solve::

   min   Σ[i=1 to Np] ||y(k+i|k) - r(k+i)||²Q + Σ[i=0 to Nc-1] ||Δu(k+i)||²R
   Δu

Subject to::

   x(k+i+1|k) = A*x(k+i|k) + B*u(k+i)
   y(k+i|k)   = C*x(k+i|k)
   umin ≤ u(k+i) ≤ umax
   ymin ≤ y(k+i|k) ≤ ymax
   |Δu(k+i)| ≤ Δumax

where:
- Np = Prediction horizon
- Nc = Control horizon
- Q, R = Weighting matrices

Batch Process Scheduling
-------------------------

State-Task Networks
~~~~~~~~~~~~~~~~~~~

**Mathematical Model:**

*Binary variables:*
- W(i,t) = 1 if task i starts at time t

*Continuous variables:*
- B(i,t) = Batch size of task i starting at time t
- S(s,t) = Amount of state s at time t

*Objective:*

::

   max  Σs price(s)*S(s,T) - Σi,t cost(i)*B(i,t)

*Constraints:*

*Material balances:*

::

   S(s,t) = S(s,t-1) + Σi ρ(s,i)*B(i,t-τi) - Σi ρ(i,s)*B(i,t)

*Resource constraints:*

::

   Σi Σt'=max(1,t-τi+1)^t W(i,t') ≤ 1   ∀ equipment unit, t

Advanced Topics
---------------

Robust Control
~~~~~~~~~~~~~~

**Uncertainty Models:**
- Parametric uncertainty: G(s,θ) where θ ∈ Θ
- Multiplicative uncertainty: G(s) = G0(s)*(1 + W(s)*Δ(s))

**H∞ Control:**
Minimize worst-case performance over all uncertainties.

Adaptive Control
~~~~~~~~~~~~~~~~

**Model Reference Adaptive Control (MRAC):**
Adjust controller parameters to make the closed-loop system behave like a reference model.

**Self-Tuning Regulators:**
Online parameter estimation combined with controller design.

Implementation Considerations
-----------------------------

Discretization
~~~~~~~~~~~~~~

For digital implementation, continuous controllers must be discretized:

**Tustin's method (bilinear transform):**

::

   s = (2/Ts) * (z-1)/(z+1)

where Ts is the sampling period.

**Practical Guidelines:**
- Sampling period: Ts ≤ τ/10 (where τ is dominant time constant)
- Anti-aliasing filters for noisy measurements
- Integral windup protection

Real-Time Implementation
~~~~~~~~~~~~~~~~~~~~~~~~

**Key considerations:**
- Computational delay
- Measurement noise filtering
- Actuator saturation
- Communication delays in distributed systems

References
----------

1. Seborg, D.E., Edgar, T.F., Mellichamp, D.A., Doyle III, F.J. (2016). *Process Dynamics and Control*, 4th Edition.

2. Stephanopoulos, G. (1984). *Chemical Process Control: An Introduction to Theory and Practice*.

3. Bequette, B.W. (2003). *Process Control: Modeling, Design, and Simulation*.

4. Marlin, T.E. (2000). *Process Control: Designing Processes and Control Systems for Dynamic Performance*.

5. Kantor, J.C. Chemical Process Control. https://jckantor.github.io/CBE30338/

Mathematical Notation
---------------------

**Symbols:**
- s - Laplace variable
- t - Time
- ω - Frequency (rad/time)
- K - Process gain
- τ - Time constant
- θ - Dead time
- ζ - Damping ratio
- ωn - Natural frequency

**Subscripts:**
- in - Inlet/input
- out - Outlet/output
- ss - Steady state
- gc - Gain crossover
- pc - Phase crossover
