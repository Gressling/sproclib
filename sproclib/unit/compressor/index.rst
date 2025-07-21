Compressor Unit Operations
========================

.. toctree::
   :maxdepth: 2
   
   Compressor

Process Models Overview
----------------------

**Compressor**: Gas compression model for industrial applications including natural gas pipeline transmission, refrigeration cycles, and process gas handling. Implements isentropic compression theory with efficiency corrections for realistic performance predictions in chemical process plants.

Unit Operations Context
----------------------

Gas compression is a fundamental unit operation in chemical engineering, essential for:

- **Mass Transfer Operations:** Providing driving force for gas absorption and distillation
- **Fluid Mechanics:** Overcoming pressure drops in piping systems and process equipment  
- **Heat Transfer:** Enabling vapor compression refrigeration and heat pump cycles
- **Reaction Engineering:** Pressurizing reactants for high-pressure synthesis reactions

The compressor model integrates with other process equipment in typical plant flowsheets:

- Upstream: Gas separation units, reactors producing gas streams
- Downstream: Heat exchangers for intercooling, process vessels requiring pressurized gas
- Control: Pressure and flow control loops, anti-surge protection systems

Typical industrial applications include natural gas transmission pipelines (20-80 bar suction, compression ratios 1.5-2.5), petrochemical hydrogen recycle systems (10-200 bar), and refrigeration plants (1-25 bar with R-134a, ammonia, or CO₂ refrigerants).
