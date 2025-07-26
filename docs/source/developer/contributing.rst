Contributing to the Standard Process Control Library
====================================================

We welcome contributions to the Standard Process Control Library! This guide will help you get started with contributing to the project.

Getting Started
---------------

**Prerequisites**

* Python 3.8 or higher
* Git version control
* Basic knowledge of chemical process control
* Familiarity with NumPy, SciPy, and scientific Python

**Development Setup**

1. **Fork the repository** on GitHub
2. **Clone your fork** locally::

    git clone https://github.com/gressling/sproclib.git
    cd sproclib

3. **Create a virtual environment**::

    python -m venv dev_env
    source dev_env/bin/activate  # On Windows: dev_env\Scripts\activate

4. **Install dependencies**::

    pip install -r requirements.txt
    pip install -e .  # Install in development mode

5. **Run tests** to verify setup::

    python test_library.py

Types of Contributions
----------------------

Code Contributions
~~~~~~~~~~~~~~~~~~

**New Process Models**
- Additional reactor types (PFR, batch reactors, etc.)
- Heat exchanger models
- Separation process models (distillation, absorption)
- Custom industry-specific models

**Control Algorithms**
- Advanced PID variants (PI-PD, 2-DOF PID)
- Robust control methods (H∞, μ-synthesis)
- Adaptive control algorithms
- Nonlinear control techniques

**Analysis Tools**
- Additional tuning methods
- Advanced optimization algorithms
- Statistical analysis tools
- Process monitoring and fault detection

**Example Implementation**::

    from process_control.models import ProcessModel
    import numpy as np
    
    class HeatExchanger(ProcessModel):
        \"\"\"Counter-current heat exchanger model.\"\"\"
        
        def __init__(self, UA, mcp_hot, mcp_cold, name="HeatExchanger"):
            super().__init__(name)
            self.UA = UA        # Heat transfer coefficient
            self.mcp_hot = mcp_hot   # Hot side heat capacity rate
            self.mcp_cold = mcp_cold # Cold side heat capacity rate
            
        def dynamics(self, t, state, inputs):
            \"\"\"Calculate state derivatives.\"\"\"
            T_hot_out, T_cold_out = state
            T_hot_in, T_cold_in, flow_hot, flow_cold = inputs
            
            # Heat transfer rate
            Q = self.UA * self.lmtd(T_hot_in, T_hot_out, T_cold_in, T_cold_out)
            
            # Energy balances
            dT_hot_dt = (flow_hot * self.mcp_hot * (T_hot_in - T_hot_out) - Q) / self.thermal_mass_hot
            dT_cold_dt = (flow_cold * self.mcp_cold * (T_cold_in - T_cold_out) + Q) / self.thermal_mass_cold
            
            return [dT_hot_dt, dT_cold_dt]

Documentation Contributions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Examples and Tutorials**
- Real-world case studies
- Step-by-step control design examples
- Industry application tutorials
- Educational exercises with solutions

**API Documentation**
- Improved docstring clarity
- Additional usage examples
- Parameter explanation and units
- Cross-references between related functions

**Theory Documentation**
- Mathematical derivations
- Control theory background
- Implementation details
- Best practices and guidelines

Testing Contributions
~~~~~~~~~~~~~~~~~~~~~

**Unit Tests**
- Test coverage for new functions
- Edge case testing
- Error handling verification
- Performance benchmarks

**Integration Tests**
- End-to-end workflow testing
- Cross-platform compatibility
- Real-world scenario validation
- Numerical accuracy verification

Development Guidelines
----------------------

Code Style
~~~~~~~~~~

We follow PEP 8 style guidelines with some modifications:

**General Rules:**
- Line length: 88 characters (Black formatter default)
- Use type hints for function signatures
- Write comprehensive docstrings (Google style)
- Include units in variable names when applicable

**Example Style**::

    def calculate_settling_time(
        response: np.ndarray,
        time: np.ndarray,
        final_value: float,
        tolerance: float = 0.02
    ) -> float:
        \"\"\"
        Calculate settling time for step response.
        
        Args:
            response: System response values
            time: Time vector (min)
            final_value: Final steady-state value
            tolerance: Settling criterion (fraction of final value)
            
        Returns:
            Settling time in same units as time vector
            
        Raises:
            ValueError: If response doesn't settle within time range
        \"\"\"
        # Implementation here
        pass

**Naming Conventions:**
- Variables: ``snake_case`` with units (e.g., ``temperature_K``, ``flow_rate_Lmin``)
- Functions: ``snake_case`` with descriptive names
- Classes: ``PascalCase`` 
- Constants: ``UPPER_SNAKE_CASE``

Documentation Style
~~~~~~~~~~~~~~~~~~~

**Docstring Format (Google Style)**::

    def tune_pid_controller(
        process_model: Dict[str, float],
        method: str = 'ziegler_nichols',
        controller_type: str = 'PID'
    ) -> Dict[str, float]:
        \"\"\"
        Tune PID controller parameters for given process model.
        
        This function implements several tuning methods for automatic
        calculation of PID parameters based on process characteristics.
        
        Args:
            process_model: Dictionary containing process parameters:
                - K: Process gain
                - tau: Time constant (min)
                - theta: Dead time (min)
            method: Tuning method ('ziegler_nichols', 'amigo', 'imc')
            controller_type: Type of controller ('P', 'PI', 'PID')
            
        Returns:
            Dictionary containing tuned parameters:
                - Kp: Proportional gain
                - Ki: Integral gain (1/min)
                - Kd: Derivative gain (min)
                
        Raises:
            ValueError: If method or controller_type is not supported
            TypeError: If process_model is not a dictionary
            
        Example:
            >>> process = {'K': 2.0, 'tau': 5.0, 'theta': 1.0}
            >>> params = tune_pid_controller(process, method='amigo')
            >>> print(f"Kp = {params['Kp']:.3f}")
            Kp = 1.234
            
        Note:
            The Ziegler-Nichols method is based on the original 1942 paper
            and may result in aggressive tuning. Consider AMIGO method for
            better robustness.
            
        References:
            Ziegler, J.G., Nichols, N.B. (1942). Optimum settings for 
            automatic controllers. Trans. ASME, 64, 759-768.
        \"\"\"

Testing Guidelines
~~~~~~~~~~~~~~~~~~

**Test Structure**::

    def test_pid_controller_basic_functionality():
        \"\"\"Test basic PID controller operation.\"\"\"
        # Arrange
        controller = PIDController(Kp=1.0, Ki=0.1, Kd=0.05)
        
        # Act
        output = controller.update(setpoint=10.0, process_variable=8.0, dt=0.1)
        
        # Assert
        assert output > 0, "Controller should produce positive output for positive error"
        assert isinstance(output, float), "Output should be a float"

**Test Categories:**
- **Unit tests** - Individual function/method testing
- **Integration tests** - Component interaction testing  
- **Regression tests** - Ensure existing functionality isn't broken
- **Performance tests** - Computational efficiency verification

Submission Process
------------------

Pull Request Workflow
~~~~~~~~~~~~~~~~~~~~~

1. **Create a feature branch**::

    git checkout -b feature/heat-exchanger-model

2. **Make your changes** following the guidelines above

3. **Add tests** for new functionality::

    def test_heat_exchanger_dynamics():
        \"\"\"Test heat exchanger model dynamics.\"\"\"
        # Test implementation

4. **Run the test suite**::

    python test_library.py
    # Ensure all tests pass

5. **Update documentation** if needed

6. **Commit your changes**::

    git add .
    git commit -m "Add heat exchanger model with counter-current flow"

7. **Push to your fork**::

    git push origin feature/heat-exchanger-model

8. **Create a Pull Request** on GitHub with:
   - Clear description of changes
   - Reference to any related issues
   - Test results and validation

Pull Request Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

**Good Pull Request:**
- **Single focus** - One feature or fix per PR
- **Clear title** - Descriptive and concise
- **Detailed description** - What, why, and how
- **Tests included** - New tests for new functionality
- **Documentation updated** - API docs and examples as needed

**Pull Request Template**::

    ## Description
    Brief description of the changes made.
    
    ## Type of Change
    - [ ] Bug fix
    - [ ] New feature
    - [ ] Documentation update
    - [ ] Performance improvement
    - [ ] Code refactoring
    
    ## Testing
    - [ ] All existing tests pass
    - [ ] New tests added for new functionality
    - [ ] Manual testing completed
    
    ## Documentation
    - [ ] Docstrings updated
    - [ ] Examples updated/added
    - [ ] README updated if needed
    
    ## Checklist
    - [ ] Code follows style guidelines
    - [ ] Self-review completed
    - [ ] No breaking changes (or clearly documented)

Code Review Process
~~~~~~~~~~~~~~~~~~~

**Review Criteria:**
- **Functionality** - Does the code work as intended?
- **Style** - Follows project style guidelines?
- **Tests** - Adequate test coverage?
- **Documentation** - Clear and complete?
- **Performance** - Efficient implementation?

**Review Timeline:**
- Initial review within 3-5 business days
- Follow-up reviews within 1-2 business days
- Merge after approval from at least one maintainer

Specific Contribution Areas
---------------------------

High-Priority Contributions
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Process Models:**
- Heat exchangers (shell-and-tube, plate)
- Distillation columns (dynamic models)
- Separation processes (absorption, extraction)
- Polymerization reactors

**Control Algorithms:**
- Model Predictive Control (MPC) enhancements
- Cascade control implementation
- Feedforward control methods
- Robust control techniques

**Analysis Tools:**
- Parameter estimation algorithms
- Process monitoring and fault detection
- Economic optimization
- Uncertainty quantification

Example Contributions
~~~~~~~~~~~~~~~~~~~~

**Simple Contribution - New Tuning Method**::

    def lambda_tuning(process_params, lambda_factor=2.0):
        \"\"\"
        Lambda tuning method for PID controllers.
        
        Args:
            process_params: Process model parameters (K, tau, theta)
            lambda_factor: Closed-loop time constant factor
            
        Returns:
            PID parameters dictionary
        \"\"\"
        K = process_params['K']
        tau = process_params['tau']
        theta = process_params['theta']
        
        # Lambda tuning formulas
        lambda_cl = lambda_factor * theta
        Kp = tau / (K * (lambda_cl + theta))
        Ki = 1 / tau
        Kd = 0  # PI controller
        
        return {'Kp': Kp, 'Ki': Ki, 'Kd': Kd}

**Complex Contribution - New Process Model**

See the heat exchanger example above for a complete implementation.

Community Guidelines
--------------------

Communication
~~~~~~~~~~~~~

**Channels:**
- GitHub Issues for bug reports and feature requests
- GitHub Discussions for questions and general discussion
- Pull Request comments for code-specific discussions

**Guidelines:**
- Be respectful and professional
- Provide context and details in issues
- Search existing issues before creating new ones
- Use clear, descriptive titles

Issue Reporting
~~~~~~~~~~~~~~~

**Bug Reports Should Include:**
- Python version and platform
- Library version
- Minimal code example to reproduce
- Expected vs. actual behavior
- Full error traceback if applicable

**Feature Requests Should Include:**
- Clear description of the proposed feature
- Use case and motivation
- Proposed API or interface
- Willingness to contribute implementation

Getting Help
~~~~~~~~~~~~

**For Contributors:**
- Check existing documentation first
- Search GitHub issues and discussions
- Ask specific questions with context
- Provide code examples when asking for help

**For New Contributors:**
- Look for "good first issue" labels
- Start with documentation improvements
- Ask for guidance on implementation approach
- Don't hesitate to ask questions

Recognition
-----------

**Contributors will be:**
- Listed in the project contributors file
- Acknowledged in release notes
- Invited to join the project team for significant contributions
- Referenced in academic citations when appropriate

**Types of Recognition:**
- Code contributions (features, fixes, optimizations)
- Documentation improvements
- Testing and quality assurance
- Community support and issue triage
- Educational content creation

Thank you for your interest in contributing to the Standard Process Control Library! Your contributions help make this tool better for the entire chemical engineering community.
