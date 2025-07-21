Pump Models - Fluid Transport Equipment
======================================

.. toctree::
   :maxdepth: 2
   
   generic/Pump
   centrifugal_pump/CentrifugalPump
   positive_displacement_pump/PositiveDisplacementPump

Process Models Overview
----------------------

**Pump**: Generic liquid pump model for constant pressure rise applications, 
suitable for process circulation loops, utility services, and general fluid transport. 
Provides fundamental hydraulic behavior with first-order dynamic response.

**CentrifugalPump**: Dynamic pump with quadratic head-flow characteristics following 
pump affinity laws. Ideal for variable flow applications in water treatment, 
chemical processing, and HVAC systems where system curves determine operating points.

**PositiveDisplacementPump**: Constant flow pump for precise metering and high-pressure 
applications. Essential for chemical injection systems, hydraulic power units, 
and viscous fluid handling where flow accuracy is critical.

Unit Operations Context
----------------------
These pump models support fundamental unit operations in chemical engineering:

**Fluid Mechanics**: Models incorporate Bernoulli's equation, friction losses, 
and momentum transfer principles. Pump curves represent energy addition to fluid streams.

**Mass Transfer**: Circulation pumps in absorption, distillation, and extraction 
processes. Flow rate control affects mass transfer coefficients and column efficiency.

**Heat Transfer**: Cooling water circulation, heat exchanger feed pumps, and 
thermal fluid loops. Pump selection affects heat transfer rates and system efficiency.

**Reaction Engineering**: Reactor feed pumps, circulation systems, and product 
transfer. Flow control impacts residence time distribution and reaction kinetics.

**Process Control**: Pump models provide process dynamics for control system design. 
Variable speed drives enable flow control in automated process operations.
