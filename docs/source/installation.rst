Installation
============

Requirements
------------

The Standard Process Control Library requires Python 3.8 or later and the following dependencies:

Core Dependencies
~~~~~~~~~~~~~~~~~

* **numpy** (>= 1.20.0) - Numerical computing
* **scipy** (>= 1.7.0) - Scientific computing and optimization
* **matplotlib** (>= 3.3.0) - Plotting and visualization

Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~

* **pyomo** (>= 6.0.0) - Optimization modeling (for advanced optimization features)
* **control** (>= 0.9.0) - Control systems library (for additional transfer function methods)

Installation Methods
--------------------

From Source (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Clone or download the library files
2. Navigate to the library directory
3. Install dependencies::

    pip install -r requirements.txt

4. Install the library in development mode::

    pip install -e .

Direct Installation
~~~~~~~~~~~~~~~~~~~

If the library is packaged, you can install directly::

    pip install sproclib

Virtual Environment (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's recommended to use a virtual environment::

    # Create virtual environment
    python -m venv process_control_env
    
    # Activate (Windows)
    process_control_env\\Scripts\\activate
    
    # Activate (Linux/Mac)
    source process_control_env/bin/activate
    
    # Install the library
    pip install -r requirements.txt

Verification
------------

Test your installation by running::

    python -c "from process_control import PIDController; print('Installation successful!')"

Or run the test suite::

    python test_library.py

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Import Error: No module named 'process_control'**
    Make sure you're in the correct directory or have installed the library properly.

**Missing dependencies**
    Install all required packages: ``pip install -r requirements.txt``

**PyOMO solver issues**
    For optimization features, you may need to install solvers like GLPK or IPOPT.

Platform-Specific Notes
~~~~~~~~~~~~~~~~~~~~~~~

**Windows**
    - Ensure you have Microsoft Visual C++ Build Tools for compiling certain packages
    - Use PowerShell or Command Prompt for installation

**Linux/Mac**
    - May require ``python3`` and ``pip3`` instead of ``python`` and ``pip``
    - Some packages may require development headers (``python3-dev`` on Ubuntu)

**Conda Users**
    The library works well with conda environments::
    
        conda create -n process_control python=3.9
        conda activate process_control
        pip install -r requirements.txt
