# Automatic Library Creation System - Prompt Templates

## 🎯 **Purpose**
This document contains the refined prompt templates used to create the Standard Process Control Library. These prompts can be adapted for automatically generating comprehensive Python libraries in any domain for integration with [Paramus.AI](https://paramus.ai).

## 📋 **Core Methodology**

### **Phase-Based Development Approach**
1. **Research & Analysis** - Study existing resources and identify patterns
2. **Architecture Design** - Define modular structure with classes and functions
3. **Implementation** - Create core modules with comprehensive documentation
4. **Testing & Validation** - Ensure functionality and reliability
5. **Documentation** - Generate Sphinx docs and user guides
6. **Integration Ready** - Package for deployment and reuse

---

## 🚀 **MAIN LIBRARY CREATION PROMPT**

### **Template Structure**
```markdown
Create a comprehensive, modern Python library for [DOMAIN] (inspired by [SOURCE] and [REFERENCE_URL]), including [N] core classes and [N] essential functions for [KEY_FEATURES]. The library should be well-structured, documented, tested, and include Sphinx documentation.

**Requirements:**
1. **Research Phase**: Analyze [SOURCE] and identify key concepts, algorithms, and code patterns
2. **Core Classes**: Implement [N] classes covering [SPECIFIC_AREAS]
3. **Essential Functions**: Create [N] utility functions for [SPECIFIC_OPERATIONS]
4. **Modular Structure**: Organize into logical modules ([MODULE_NAMES])
5. **Documentation**: Include README, examples, tests, and Sphinx docs
6. **Production Ready**: Error handling, validation, type hints, docstrings

**Deliverables:**
- Modular library with clean architecture
- Comprehensive documentation and examples
- Test suite with validation
- Sphinx documentation with API reference
- Requirements file with dependencies
- Summary document for reuse
```

---

## 📚 **DOMAIN-SPECIFIC PROMPT EXAMPLES**

### **Chemical Engineering Prompt**
```markdown
Create a comprehensive, modern Python library for **chemical process control**, including 10 core classes and 10 essential functions for modeling, simulation, PID control, optimization, frequency analysis, and batch scheduling. The library should be well-structured, documented, tested, and include Sphinx documentation.

**Core Classes to Implement:**
1. PIDController - Advanced PID with anti-windup, bumpless transfer
2. TuningRule - Ziegler-Nichols, AMIGO, Relay tuning methods
3. ProcessModel - Abstract base for all process models
4. CSTR - Continuous stirred tank reactor models
5. Tank - Gravity-drained tank for level control
6. LinearApproximation - Linearization around operating points
7. TransferFunction - Frequency domain analysis
8. Simulation - ODE integration for dynamics
9. Optimization - Process optimization with PyOMO
10. StateTaskNetwork - Batch scheduling

**Essential Functions:**
1. step_response - System response analysis
2. bode_plot - Frequency domain plots
3. linearize - Model linearization
4. tune_pid - Automated PID tuning
5. simulate_process - Dynamic simulation
6. optimize_operation - Process optimization
7. fit_fopdt - Parameter identification
8. stability_analysis - Stability assessment
9. disturbance_rejection - Control design
10. model_predictive_control - MPC implementation
```

### **Machine Learning Prompt**
```markdown
Create a comprehensive, modern Python library for **machine learning operations** (inspired by MLOps best practices and scikit-learn), including 10 core classes and 10 essential functions for data preprocessing, model training, evaluation, deployment, and monitoring. The library should be well-structured, documented, tested, and include Sphinx documentation.

**Core Classes to Implement:**
1. DataProcessor - Data cleaning and preprocessing
2. FeatureEngineer - Feature extraction and selection
3. ModelTrainer - Training pipeline with cross-validation
4. ModelEvaluator - Comprehensive model evaluation
5. HyperparameterOptimizer - Automated hyperparameter tuning
6. ModelRegistry - Model versioning and storage
7. Pipeline - End-to-end ML pipeline
8. MonitoringSystem - Model performance monitoring
9. DeploymentManager - Model deployment and serving
10. ExperimentTracker - Experiment logging and comparison

**Essential Functions:**
1. load_data - Data loading with validation
2. preprocess_features - Feature preprocessing
3. train_model - Model training with logging
4. evaluate_model - Model evaluation metrics
5. tune_hyperparameters - Hyperparameter optimization
6. deploy_model - Model deployment
7. monitor_drift - Data/model drift detection
8. generate_report - Automated reporting
9. compare_models - Model comparison
10. predict_batch - Batch prediction
```

### **Financial Engineering Prompt**
```markdown
Create a comprehensive, modern Python library for **quantitative finance** (inspired by QuantLib and modern portfolio theory), including 10 core classes and 10 essential functions for portfolio optimization, risk management, derivatives pricing, backtesting, and market analysis. The library should be well-structured, documented, tested, and include Sphinx documentation.

**Core Classes to Implement:**
1. Portfolio - Portfolio management and optimization
2. RiskModel - Risk assessment and VaR calculation
3. DerivativesPricer - Options and derivatives pricing
4. BacktestEngine - Strategy backtesting framework
5. MarketDataProvider - Real-time market data interface
6. TradingStrategy - Strategy development framework
7. RiskMetrics - Risk calculation and reporting
8. AssetModel - Asset pricing models
9. OptimizationEngine - Portfolio optimization
10. ReportGenerator - Financial reporting

**Essential Functions:**
1. calculate_returns - Return calculation
2. optimize_portfolio - Portfolio optimization
3. price_option - Options pricing
4. calculate_var - Value at Risk
5. backtest_strategy - Strategy backtesting
6. analyze_correlation - Correlation analysis
7. estimate_volatility - Volatility modeling
8. generate_scenarios - Monte Carlo scenarios
9. calculate_sharpe - Performance metrics
10. hedge_portfolio - Risk hedging
```

---

## 🔧 **IMPLEMENTATION PHASE PROMPTS**

### **Phase 1: Research & Analysis**
```markdown
**Research Prompt:**
"Analyze the [SOURCE] repository/course/documentation at [URL]. Identify the key concepts, algorithms, design patterns, and code structures. Extract the most important classes, functions, and workflows that should be included in a modern Python library for [DOMAIN]. Focus on:

1. Core mathematical models and algorithms
2. Common use cases and workflows
3. Integration points with popular libraries
4. Best practices and design patterns
5. Essential functionality that practitioners need

Provide a detailed analysis with specific examples from the source material."
```

### **Phase 2: Architecture Design**
```markdown
**Architecture Prompt:**
"Based on the research analysis, design a modular Python library architecture for [DOMAIN]. Create:

1. **Module Structure**: Define 4-6 logical modules with clear responsibilities
2. **Class Hierarchy**: Design [N] core classes with inheritance and composition
3. **Function Library**: Specify [N] essential utility functions
4. **Integration Points**: Define how modules interact and dependencies
5. **API Design**: Create clean, intuitive interfaces for users

The architecture should be extensible, maintainable, and follow Python best practices."
```

### **Phase 3: Implementation**
```markdown
**Implementation Prompt:**
"Implement the [DOMAIN] library according to the designed architecture. For each module:

1. **Create comprehensive docstrings** with examples
2. **Add type hints** for all functions and methods
3. **Include error handling** and input validation
4. **Follow PEP 8** style guidelines
5. **Add logging** where appropriate
6. **Ensure thread safety** where needed

Start with [MODULE_NAME] and implement all classes and functions with full functionality."
```

### **Phase 4: Testing & Validation**
```markdown
**Testing Prompt:**
"Create a comprehensive test suite for the [DOMAIN] library:

1. **Unit Tests**: Test each class and function individually
2. **Integration Tests**: Test module interactions
3. **Example Tests**: Validate example code works correctly
4. **Edge Case Tests**: Test boundary conditions and error cases
5. **Performance Tests**: Ensure acceptable performance

Use pytest framework and aim for >90% code coverage. Include both basic functionality tests and advanced feature tests."
```

### **Phase 5: Documentation**
```markdown
**Documentation Prompt:**
"Create comprehensive Sphinx documentation for the [DOMAIN] library:

1. **Setup Sphinx** with modern theme and extensions
2. **API Reference**: Auto-generate from docstrings
3. **User Guide**: Installation, quickstart, tutorials
4. **Examples**: Comprehensive examples with explanations
5. **Theory Guide**: Mathematical background and concepts
6. **Developer Guide**: Contributing guidelines and architecture

Ensure documentation is professional, complete, and user-friendly."
```

---

## 🎨 **CUSTOMIZATION PARAMETERS**

### **Domain-Specific Variables**
```python
DOMAIN_VARIABLES = {
    "DOMAIN": "Target subject area (e.g., 'chemical process control')",
    "SOURCE": "Primary reference (e.g., 'process control course materials')",
    "REFERENCE_URL": "Source URL for analysis",
    "N_CLASSES": "Number of core classes (typically 8-12)",
    "N_FUNCTIONS": "Number of essential functions (typically 8-12)",
    "KEY_FEATURES": "Main capabilities (e.g., 'modeling, simulation, control')",
    "SPECIFIC_AREAS": "Domain-specific areas to cover",
    "SPECIFIC_OPERATIONS": "Key operations the functions should perform",
    "MODULE_NAMES": "Logical module organization"
}
```

### **Technical Parameters**
```python
TECHNICAL_CONFIG = {
    "PYTHON_VERSION": "3.8+",
    "DOCUMENTATION": "Sphinx with RTD theme",
    "TESTING": "pytest with coverage",
    "STYLE": "Black formatter + flake8",
    "TYPE_CHECKING": "mypy",
    "DEPENDENCIES": "Specify core libraries needed"
}
```

---

## 🤖 **AUTOMATION INTEGRATION**

### **Paramus.AI Integration Points**
```markdown
**Integration Workflow:**
1. **Input Processing**: Parse domain, source, and requirements
2. **Template Selection**: Choose appropriate prompt template
3. **Parameter Substitution**: Fill in domain-specific variables
4. **Phase Execution**: Run development phases sequentially
5. **Quality Assurance**: Validate outputs and run tests
6. **Documentation Generation**: Create complete documentation
7. **Package Creation**: Prepare for distribution/deployment

**API Endpoints for Paramus.AI:**
- `/generate-library` - Main library generation endpoint
- `/validate-library` - Quality assurance and testing
- `/update-library` - Incremental updates and improvements
- `/document-library` - Documentation generation
- `/package-library` - Packaging and distribution prep
```

### **Quality Metrics**
```python
QUALITY_METRICS = {
    "code_coverage": ">90%",
    "documentation_completeness": "All public APIs documented",
    "test_success_rate": "100% passing tests",
    "style_compliance": "PEP 8 compliant",
    "type_coverage": ">80% type hints",
    "example_validation": "All examples executable"
}
```

---

## 📋 **PROMPT IMPROVEMENT SUGGESTIONS**

### **Enhanced Research Phase**
```markdown
"Additionally analyze GitHub repositories, academic papers, and industry standards related to [DOMAIN]. Compare different implementation approaches and identify the most robust, scalable, and user-friendly patterns. Consider integration with popular ecosystem libraries and modern development practices."
```

### **Advanced Architecture Design**
```markdown
"Design for extensibility by future AI agents. Include plugin architecture, configuration management, and clear extension points. Consider microservice compatibility and cloud-native deployment patterns."
```

### **Production-Ready Implementation**
```markdown
"Include observability (logging, metrics, tracing), configuration management, caching strategies, and performance optimization. Design for horizontal scaling and containerization."
```

---

## 🚀 **SUCCESS CRITERIA**

### **Library Quality Checklist**
- ✅ Modular, extensible architecture
- ✅ Comprehensive documentation (README + Sphinx)
- ✅ Complete test suite with high coverage
- ✅ Type hints and docstrings throughout
- ✅ Working examples demonstrating all features
- ✅ Professional code quality and style
- ✅ Clear installation and usage instructions
- ✅ Integration-ready package structure

### **User Experience Goals**
- ✅ Easy installation and setup
- ✅ Intuitive API design
- ✅ Clear documentation and examples
- ✅ Helpful error messages
- ✅ Good performance characteristics
- ✅ Extensible for custom needs

---

## 🔄 **ITERATION & IMPROVEMENT**

### **Feedback Loop Integration**
```markdown
"After library creation, collect usage patterns, performance metrics, and user feedback. Use this data to improve future library generation prompts and identify common enhancement patterns."
```

### **Continuous Improvement**
```markdown
"Regularly update prompt templates based on:
1. New best practices in software development
2. Emerging patterns in domain-specific libraries
3. User feedback and usage analytics
4. Technology stack evolution
5. Integration requirements with Paramus.AI ecosystem"
```

---

## 📚 **CONCLUSION**

This prompt template system enables automated generation of high-quality, production-ready Python libraries across diverse domains. The phase-based approach ensures comprehensive coverage of all aspects from research to documentation, while the parameterized templates allow easy customization for different subject areas.

**Key Benefits:**
- 🚀 **Rapid Development**: Generate complete libraries in hours vs. weeks
- 🎯 **Consistent Quality**: Standardized structure and best practices
- 📚 **Complete Documentation**: Professional docs included automatically
- 🔧 **Production Ready**: Testing, validation, and packaging included
- 🤖 **AI-Friendly**: Designed for integration with AI development systems

The templates can be continuously improved based on usage patterns and feedback, making the system more effective over time for the Paramus.AI platform.
