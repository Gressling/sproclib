Slurry Transport Examples
=========================

This section provides practical examples of slurry transport modeling and analysis using the transport module.

Overview
--------

Slurry transport is critical in many chemical and mineral processing applications. These examples cover:

- Basic slurry flow calculations
- Particle settling and suspension
- Pipeline design considerations
- Pump selection and operation

Key challenges in slurry transport include particle settling, erosion, and maintaining adequate flow velocities.

Basic Slurry Flow Modeling
---------------------------

Example 1: Two-Phase Slurry Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from transport.continuous.liquid import SlurryPipeline
    import numpy as np
    
    # Create a slurry pipeline system
    pipeline = SlurryPipeline(
        diameter=0.15,  # 15 cm diameter
        length=200,     # 200 m length
        roughness=0.0003  # Higher roughness for slurry
    )
    
    # Define slurry properties
    slurry_properties = {
        'liquid_density': 1000,    # kg/m³ (water)
        'particle_density': 2650,  # kg/m³ (sand)
        'particle_diameter': 0.0005,  # 0.5 mm particles
        'volume_concentration': 0.15,  # 15% solids by volume
        'liquid_viscosity': 0.001   # Pa·s
    }
    
    pipeline.set_slurry_properties(**slurry_properties)
    
    # Calculate slurry mixture properties
    mixture_density = pipeline.calculate_mixture_density()
    mixture_viscosity = pipeline.calculate_mixture_viscosity()
    
    print(f"Mixture density: {mixture_density:.1f} kg/m³")
    print(f"Mixture viscosity: {mixture_viscosity:.4f} Pa·s")

Example 2: Critical Velocity Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Calculate critical velocity to prevent settling
    critical_velocity = pipeline.calculate_critical_velocity()
    
    # Analyze pressure drop vs velocity
    velocities = np.linspace(0.5, 3.0, 50)
    pressure_drops = []
    
    for velocity in velocities:
        flow_rate = velocity * np.pi * (pipeline.diameter/2)**2
        pressure_drop = pipeline.calculate_pressure_drop(flow_rate)
        pressure_drops.append(pressure_drop)
    
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(12, 8))
    
    # Plot pressure drop vs velocity
    plt.subplot(2, 1, 1)
    plt.plot(velocities, pressure_drops)
    plt.axvline(x=critical_velocity, color='r', linestyle='--', 
                label=f'Critical velocity: {critical_velocity:.2f} m/s')
    plt.xlabel('Velocity (m/s)')
    plt.ylabel('Pressure Drop (Pa/m)')
    plt.title('Slurry Pipeline Pressure Drop vs Velocity')
    plt.legend()
    plt.grid(True)
    
    # Plot settling velocity analysis
    plt.subplot(2, 1, 2)
    particle_sizes = np.linspace(0.0001, 0.002, 50)  # 0.1 to 2 mm
    settling_velocities = []
    
    for size in particle_sizes:
        pipeline.set_slurry_properties(particle_diameter=size, **{k: v for k, v in slurry_properties.items() if k != 'particle_diameter'})
        settling_vel = pipeline.calculate_settling_velocity()
        settling_velocities.append(settling_vel)
    
    plt.plot(particle_sizes * 1000, settling_velocities)  # Convert to mm
    plt.xlabel('Particle Size (mm)')
    plt.ylabel('Settling Velocity (m/s)')
    plt.title('Particle Settling Velocity vs Size')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

Advanced Slurry Transport
-------------------------

Example 3: Multi-Size Particle Distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class MultiSizeSlurryModel:
        def __init__(self, pipeline):
            self.pipeline = pipeline
            self.particle_distributions = []
        
        def add_particle_size(self, diameter, volume_fraction):
            """Add a particle size class to the distribution"""
            self.particle_distributions.append({
                'diameter': diameter,
                'volume_fraction': volume_fraction
            })
        
        def calculate_weighted_properties(self):
            """Calculate weighted average properties"""
            total_volume_fraction = sum(p['volume_fraction'] for p in self.particle_distributions)
            
            weighted_diameter = sum(
                p['diameter'] * p['volume_fraction'] 
                for p in self.particle_distributions
            ) / total_volume_fraction
            
            return weighted_diameter, total_volume_fraction
        
        def analyze_size_distribution(self):
            """Analyze the effect of particle size distribution"""
            results = []
            
            for particle in self.particle_distributions:
                self.pipeline.set_slurry_properties(
                    particle_diameter=particle['diameter'],
                    volume_concentration=particle['volume_fraction'],
                    **{k: v for k, v in slurry_properties.items() 
                       if k not in ['particle_diameter', 'volume_concentration']}
                )
                
                critical_vel = self.pipeline.calculate_critical_velocity()
                settling_vel = self.pipeline.calculate_settling_velocity()
                
                results.append({
                    'diameter': particle['diameter'],
                    'volume_fraction': particle['volume_fraction'],
                    'critical_velocity': critical_vel,
                    'settling_velocity': settling_vel
                })
            
            return results
    
    # Example with multiple particle sizes
    multi_size_model = MultiSizeSlurryModel(pipeline)
    
    # Add different particle size classes
    multi_size_model.add_particle_size(diameter=0.0002, volume_fraction=0.05)  # Fine
    multi_size_model.add_particle_size(diameter=0.0005, volume_fraction=0.08)  # Medium
    multi_size_model.add_particle_size(diameter=0.001, volume_fraction=0.02)   # Coarse
    
    # Analyze the distribution
    size_analysis = multi_size_model.analyze_size_distribution()
    
    # Plot results
    diameters = [r['diameter'] * 1000 for r in size_analysis]  # Convert to mm
    critical_vels = [r['critical_velocity'] for r in size_analysis]
    settling_vels = [r['settling_velocity'] for r in size_analysis]
    
    plt.figure(figsize=(10, 6))
    plt.plot(diameters, critical_vels, 'o-', label='Critical Velocity')
    plt.plot(diameters, settling_vels, 's-', label='Settling Velocity')
    plt.xlabel('Particle Diameter (mm)')
    plt.ylabel('Velocity (m/s)')
    plt.title('Velocity Requirements vs Particle Size')
    plt.legend()
    plt.grid(True)
    plt.show()

Example 4: Pump Selection for Slurry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from transport.continuous.liquid import SlurryPump
    
    class SlurryPumpSelector:
        def __init__(self, pipeline, slurry_properties):
            self.pipeline = pipeline
            self.slurry_properties = slurry_properties
        
        def calculate_pump_requirements(self, target_velocity):
            """Calculate pump requirements for target velocity"""
            # Calculate flow rate
            area = np.pi * (self.pipeline.diameter / 2)**2
            flow_rate = target_velocity * area
            
            # Calculate total head requirements
            pressure_drop = self.pipeline.calculate_pressure_drop(flow_rate)
            static_head = 10  # Assume 10 m static head
            friction_head = pressure_drop / (self.pipeline.mixture_density * 9.81)
            
            total_head = static_head + friction_head + 5  # 5 m safety margin
            
            # Calculate power requirements
            efficiency = 0.75  # Typical pump efficiency
            power = (self.pipeline.mixture_density * 9.81 * flow_rate * total_head) / efficiency
            
            return {
                'flow_rate': flow_rate,
                'total_head': total_head,
                'power': power,
                'friction_head': friction_head
            }
        
        def analyze_pump_curves(self):
            """Analyze pump performance across velocity range"""
            velocities = np.linspace(1.0, 4.0, 30)
            pump_data = []
            
            for vel in velocities:
                requirements = self.calculate_pump_requirements(vel)
                pump_data.append({
                    'velocity': vel,
                    **requirements
                })
            
            return pump_data
    
    # Pump selection analysis
    pump_selector = SlurryPumpSelector(pipeline, slurry_properties)
    pump_analysis = pump_selector.analyze_pump_curves()
    
    # Extract data for plotting
    velocities = [p['velocity'] for p in pump_analysis]
    flow_rates = [p['flow_rate'] * 3600 for p in pump_analysis]  # Convert to m³/h
    heads = [p['total_head'] for p in pump_analysis]
    powers = [p['power'] / 1000 for p in pump_analysis]  # Convert to kW
    
    # Plot pump requirements
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12))
    
    ax1.plot(velocities, flow_rates)
    ax1.axvline(x=critical_velocity, color='r', linestyle='--', label='Critical Velocity')
    ax1.set_ylabel('Flow Rate (m³/h)')
    ax1.set_title('Pump Requirements vs Pipeline Velocity')
    ax1.grid(True)
    ax1.legend()
    
    ax2.plot(velocities, heads)
    ax2.axvline(x=critical_velocity, color='r', linestyle='--')
    ax2.set_ylabel('Total Head (m)')
    ax2.grid(True)
    
    ax3.plot(velocities, powers)
    ax3.axvline(x=critical_velocity, color='r', linestyle='--')
    ax3.set_xlabel('Pipeline Velocity (m/s)')
    ax3.set_ylabel('Power (kW)')
    ax3.grid(True)
    
    plt.tight_layout()
    plt.show()

Erosion and Wear Analysis
-------------------------

Example 5: Pipeline Erosion Modeling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class ErosionModel:
        def __init__(self, pipeline):
            self.pipeline = pipeline
        
        def calculate_erosion_rate(self, velocity, particle_properties):
            """Calculate erosion rate using empirical correlations"""
            # Simplified erosion model (actual models are more complex)
            particle_hardness = particle_properties.get('hardness', 7)  # Mohs scale
            particle_angularity = particle_properties.get('angularity', 0.7)  # 0-1 scale
            
            # Erosion rate proportional to velocity^n (typically n=2.5-3)
            base_erosion_rate = 1e-8  # m/year at 1 m/s reference
            velocity_exponent = 2.7
            
            erosion_rate = (base_erosion_rate * 
                          (velocity ** velocity_exponent) * 
                          (particle_hardness / 7) * 
                          particle_angularity)
            
            return erosion_rate
        
        def predict_pipeline_lifetime(self, operating_velocity, wall_thickness, 
                                    minimum_thickness=0.002):
            """Predict pipeline lifetime based on erosion"""
            particle_props = {
                'hardness': 7,  # Quartz hardness
                'angularity': 0.8
            }
            
            erosion_rate = self.calculate_erosion_rate(operating_velocity, particle_props)
            allowable_erosion = wall_thickness - minimum_thickness
            
            lifetime_years = allowable_erosion / erosion_rate
            return lifetime_years
    
    # Erosion analysis
    erosion_model = ErosionModel(pipeline)
    
    velocities = np.linspace(1.0, 4.0, 30)
    wall_thickness = 0.008  # 8 mm wall thickness
    
    lifetimes = [erosion_model.predict_pipeline_lifetime(v, wall_thickness) 
                for v in velocities]
    
    plt.figure(figsize=(10, 6))
    plt.plot(velocities, lifetimes)
    plt.axvline(x=critical_velocity, color='r', linestyle='--', 
                label=f'Critical velocity: {critical_velocity:.2f} m/s')
    plt.xlabel('Operating Velocity (m/s)')
    plt.ylabel('Predicted Lifetime (years)')
    plt.title('Pipeline Lifetime vs Operating Velocity')
    plt.legend()
    plt.grid(True)
    plt.show()

Troubleshooting
---------------

Common Slurry Transport Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Particle Settling**
   - Increase flow velocity above critical velocity
   - Use pulsed flow or air injection
   - Consider pipeline inclination

2. **Excessive Erosion**
   - Reduce velocity where possible
   - Use erosion-resistant materials
   - Implement velocity reduction strategies

3. **Pump Wear**
   - Select appropriate pump materials
   - Use proper impeller designs for slurries
   - Implement regular maintenance schedules

4. **Pipeline Blockages**
   - Maintain adequate velocities
   - Install flushing systems
   - Monitor concentration levels

Design Guidelines
~~~~~~~~~~~~~~~~~

- Maintain velocity 1.2-1.5 times critical velocity
- Consider particle size distribution effects
- Account for pipeline inclination
- Plan for maintenance access
- Include instrumentation for monitoring

See Also
--------

- :doc:`pipeline_flow_examples`
- :doc:`peristaltic_pump_examples`
- :doc:`../multiphase_flow`
- :doc:`../../api/transport_package`
