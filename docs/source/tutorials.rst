Tutorials
=========

Step-by-step tutorials for learning process control with SPROCLIB. These tutorials are designed
to build your knowledge progressively from basic concepts to advanced applications.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   tutorials/installation_tutorial
   tutorials/first_steps
   tutorials/basic_concepts
   tutorials/semantic_introduction

.. toctree::
   :maxdepth: 2
   :caption: Control Fundamentals

   tutorials/pid_control_basics
   tutorials/system_identification
   tutorials/frequency_domain
   tutorials/stability_analysis

.. toctree::
   :maxdepth: 2
   :caption: Process Modeling

   tutorials/tank_modeling
   tutorials/reactor_modeling
   tutorials/heat_exchanger_modeling
   tutorials/transport_systems

.. toctree::
   :maxdepth: 2
   :caption: Advanced Control

   tutorials/cascade_control
   tutorials/feedforward_control
   tutorials/model_predictive_control
   tutorials/robust_control

.. toctree::
   :maxdepth: 2
   :caption: Optimization

   tutorials/parameter_estimation
   tutorials/economic_optimization
   tutorials/batch_scheduling
   tutorials/real_time_optimization

.. toctree::
   :maxdepth: 2
   :caption: Industrial Applications

   tutorials/plant_wide_control
   tutorials/safety_systems
   tutorials/alarm_management
   tutorials/performance_monitoring

Overview
--------

Learning Path
~~~~~~~~~~~~~

**Beginner Path (0-3 months experience):**

1. :doc:`tutorials/installation_tutorial` - Get SPROCLIB running
2. :doc:`tutorials/first_steps` - Your first control system
3. :doc:`tutorials/basic_concepts` - Fundamental control theory
4. :doc:`tutorials/pid_control_basics` - Master PID control
5. :doc:`tutorials/tank_modeling` - Simple process modeling

**Intermediate Path (3-12 months experience):**

1. :doc:`tutorials/system_identification` - Model real processes
2. :doc:`tutorials/frequency_domain` - Frequency analysis
3. :doc:`tutorials/reactor_modeling` - Complex process dynamics
4. :doc:`tutorials/cascade_control` - Advanced control structures
5. :doc:`tutorials/parameter_estimation` - Optimize model parameters

**Advanced Path (1+ years experience):**

1. :doc:`tutorials/model_predictive_control` - Modern control methods
2. :doc:`tutorials/economic_optimization` - Profit maximization
3. :doc:`tutorials/plant_wide_control` - System integration
4. :doc:`tutorials/real_time_optimization` - Online optimization
5. :doc:`tutorials/safety_systems` - Critical safety applications

Tutorial Features
~~~~~~~~~~~~~~~~~

Each tutorial includes:

* **Clear Learning Objectives** - What you'll accomplish
* **Prerequisites** - Required background knowledge
* **Step-by-Step Instructions** - Detailed implementation guide
* **Working Code Examples** - Complete, runnable code
* **Exercises** - Practice problems with solutions
* **Further Reading** - Additional resources and references

**Interactive Elements:**

* Jupyter notebook versions available
* Code snippets you can copy and run
* Visualization and plotting examples
* Real-world data and scenarios
* Troubleshooting guides

Getting Started
---------------

**Prerequisites:**

* Basic Python programming knowledge
* Elementary understanding of differential equations
* Familiarity with chemical engineering concepts (helpful but not required)

**Installation:**

Before starting the tutorials, ensure SPROCLIB is properly installed::

    pip install sproclib

**Verify Installation:**

Run this quick test::

    import sproclib
    from sproclib.analysis import TransferFunction
    
    # Create a simple process
    process = TransferFunction.first_order_plus_dead_time(K=1.0, tau=5.0, theta=1.0)
    print(f"Process: {process}")
    print("Installation successful!")

Tutorial Structure
------------------

Beginner Tutorials
~~~~~~~~~~~~~~~~~~

**Installation and Setup**
  Complete guide to installing SPROCLIB and setting up your development environment.

**First Steps with Process Control**
  Build your first control system in 15 minutes using the semantic plant design API.

**Basic Control Concepts**
  Learn fundamental concepts: process variables, controllers, setpoints, and disturbances.

**PID Control Fundamentals**
  Master proportional, integral, and derivative control with hands-on examples.

Intermediate Tutorials
~~~~~~~~~~~~~~~~~~~~~

**System Identification**
  Learn to identify process models from experimental data using various methods.

**Frequency Domain Analysis**
  Understand Bode plots, Nyquist diagrams, and stability analysis.

**Advanced Process Modeling**
  Model complex processes including reactors, heat exchangers, and separation units.

**Control System Design**
  Design robust control systems with proper tuning and performance analysis.

Advanced Tutorials
~~~~~~~~~~~~~~~~~~

**Model Predictive Control**
  Implement MPC for multivariable processes with constraints and optimization.

**Economic Optimization**
  Optimize process economics while maintaining product quality and safety.

**Plant-Wide Control**
  Design control systems for complete chemical plants with multiple units.

**Safety and Reliability**
  Implement safety instrumented systems and fault-tolerant control.

Tutorial Examples
-----------------

**Example: Tank Level Control Tutorial Structure**

.. code-block:: none

    tutorials/tank_modeling.rst
    ├── Learning Objectives
    ├── Prerequisites  
    ├── Theory Background
    │   ├── Mass Balance Equations
    │   ├── Linearization Concepts
    │   └── Control Challenges
    ├── Implementation Steps
    │   ├── Step 1: Model Creation
    │   ├── Step 2: Linearization
    │   ├── Step 3: Controller Design
    │   ├── Step 4: Simulation
    │   └── Step 5: Performance Analysis
    ├── Exercises
    │   ├── Basic Problems
    │   ├── Advanced Challenges
    │   └── Solutions
    └── Further Reading

**Code Example from Tutorial:**

.. code-block:: python

    # From tutorials/tank_modeling.rst
    from sproclib.units import Tank
    from sproclib.utilities import tune_pid, step_response
    
    # Step 1: Create tank model
    tank = Tank(A=10.0, h_max=5.0, name="Level Tank")
    
    # Step 2: Linearize around operating point
    operating_point = {'h': 2.5, 'q_in': 5.0}
    linear_model = tank.linearize(operating_point)
    
    # Step 3: Design controller
    pid_params = tune_pid(linear_model, method='amigo')
    
    # Step 4: Analyze performance
    response = step_response(linear_model, amplitude=0.5)

Supporting Materials
-------------------

**Downloadable Resources:**

* Jupyter notebooks for interactive learning
* Python scripts for all examples
* Data files for real-world examples
* Solution keys for exercises

**Video Content:**

* Tutorial walkthroughs (when available)
* Concept explanations with animations
* Live coding sessions
* Q&A recordings

**Additional Support:**

* Community forum for questions
* GitHub issues for technical problems
* Office hours (when available)
* Peer learning groups

Contributing to Tutorials
-------------------------

We welcome contributions to improve and expand the tutorial collection:

**Ways to Contribute:**

* **Fix errors** or improve clarity in existing tutorials
* **Add new tutorials** for specialized topics
* **Create exercises** and practice problems
* **Develop interactive content** with Jupyter notebooks
* **Record video walkthroughs** for complex topics

**Tutorial Guidelines:**

* Start with clear learning objectives
* Use practical, realistic examples
* Include complete, tested code
* Provide exercises for practice
* Reference relevant theory and literature

See :doc:`contributing` for detailed guidelines on contributing tutorials.

Feedback and Improvements
-------------------------

Help us improve the tutorials:

* **Report Issues** - Found errors or unclear explanations?
* **Suggest Topics** - What tutorials would help you most?
* **Share Success Stories** - How did the tutorials help your learning?
* **Rate Tutorials** - Let us know which tutorials work best

Your feedback helps us create better learning resources for the entire community.

Next Steps
----------

Ready to start learning? Begin with:

1. :doc:`tutorials/installation_tutorial` - Set up your environment
2. :doc:`tutorials/first_steps` - Build your first control system
3. Choose your learning path based on your experience level

Happy learning with SPROCLIB!
        # Energy cost (higher temperature = higher cost)
        avg_temp = np.mean(T_profile)
        energy_cost = (avg_temp - 300) * 0.1 * 120  # $/K/min * K * min
        
        profit = product_value - energy_cost
        
        return -profit  # Negative for minimization

**Step 3: Solve Optimization**

::

    from scipy.optimize import minimize
    
    # Initial guess - constant temperature
    initial_temp_profile = np.ones(13) * 320  # 320 K
    
    # Constraints - temperature limits
    bounds = [(300, 400) for _ in range(13)]  # 300-400 K for each point
    
    # Optimize
    result = minimize(
        objective_function,
        initial_temp_profile,
        method='L-BFGS-B',
        bounds=bounds
    )
    
    optimal_temps = result.x
    max_profit = -result.fun
    
    print(f"Maximum profit: ${max_profit:.2f}")
    print(f"Optimal temperature profile:")
    
    time_points = np.linspace(0, 120, 13)
    for i, (t, T) in enumerate(zip(time_points, optimal_temps)):
        print(f"  t={t:5.1f} min: T={T:5.1f} K")

**Step 4: Analyze Results**

::

    # Compare optimal vs. constant temperature operation
    plt.figure(figsize=(12, 8))
    
    # Plot optimal temperature profile
    plt.subplot(2, 2, 1)
    plt.plot(time_points, optimal_temps, 'ro-', label='Optimal')
    plt.axhline(y=320, color='b', linestyle='--', label='Constant (320K)')
    plt.ylabel('Temperature (K)')
    plt.xlabel('Time (min)')
    plt.legend()
    plt.grid(True)
    plt.title('Temperature Profiles')
    
    # Simulate both cases and plot concentrations
    # ... (simulation code)
    
    plt.tight_layout()
    plt.show()

Next Steps
----------

After completing these tutorials, you should be able to:

1. **Model chemical processes** using the provided classes
2. **Design PID controllers** with automated tuning
3. **Analyze system performance** using frequency domain methods
4. **Optimize process operations** for economic objectives

Continue with:

* **Advanced Examples** - More complex multi-unit processes
* **Theory Section** - Mathematical background on control concepts
* **API Reference** - Detailed documentation of all functions and classes

For more advanced topics, explore:

* **Model Predictive Control** for multivariable processes
* **Batch Scheduling** for campaign optimization
* **Nonlinear Control** for highly nonlinear processes
