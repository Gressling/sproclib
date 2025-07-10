Tank Unit Operations
===================

This module provides models for tank unit operations commonly used in chemical engineering processes. Tank systems are fundamental building blocks for level control, storage, and sequential processing applications.

The tank models implement gravity-drained systems based on material balance principles and Torricelli's law, providing realistic dynamics for process control studies and industrial applications.

Available Models
---------------

.. toctree::
   :maxdepth: 2
   
   Tank
   InteractingTanks

Tank Model
----------

The single tank model represents a gravity-drained tank with inlet flow control. This is the most basic level control system and serves as a foundation for understanding tank dynamics. The model exhibits first-order nonlinear behavior due to the square root relationship between liquid height and outlet flow rate.

**Key Features:**
- First-order nonlinear dynamics
- Variable time constant based on operating point
- Suitable for level control applications
- Educational tool for process control fundamentals

**Typical Applications:**
- Storage tanks
- Buffer vessels
- Process reactors
- Level control systems

InteractingTanks Model
---------------------

The interacting tanks model represents two tanks connected in series, where the outlet of the first tank feeds the second tank. This configuration is widely used for studying multi-variable dynamics and demonstrates the cascading effects in process systems.

**Key Features:**
- Second-order coupled nonlinear dynamics
- Multiple time constants and interaction effects
- Realistic representation of tank cascades
- Suitable for advanced control studies

**Typical Applications:**
- Tank cascades in water treatment
- Sequential reactor systems
- Multi-stage separation processes
- Educational demonstrations of interaction effects

Chemical Engineering Perspective
-------------------------------

From a chemical engineering standpoint, tank systems are critical unit operations that serve multiple purposes:

**Material Balance and Storage**
- Provide inventory control and buffering capacity
- Enable continuous operation despite batch upstream/downstream processes
- Allow for residence time control in reactive systems

**Process Control**
- Level control maintains safe operating conditions
- Flow regulation provides smooth operation
- Cascade systems enable staged processing

**Design Considerations**
- Tank sizing affects system dynamics and control performance
- Discharge coefficient selection impacts operating point
- Area ratios in cascade systems determine interaction strength

**Scale-up Implications**
- Time constants scale with tank size and operating conditions
- Control strategies must account for varying dynamics
- Safety considerations become more critical at larger scales

The models provided in this module capture the essential dynamics while maintaining computational efficiency suitable for control system design and educational purposes.
