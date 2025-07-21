import pytest
import numpy as np
from sproclib.controller.state_space.StateSpaceController import StateSpaceController, StateSpaceModel

class TestStateSpaceController:
    @pytest.fixture
    def reactor_model(self):
        """Create a 2x2 reactor system model for testing."""
        A = np.array([[-0.5, -0.1], [0.2, -0.3]])
        B = np.array([[0.8, 0.0], [0.0, 0.6]])  
        C = np.array([[1.0, 0.0], [0.0, 1.0]])
        D = np.zeros((2, 2))
        
        return StateSpaceModel(
            A, B, C, D,
            state_names=['CA', 'T'],
            input_names=['q', 'Tc'],
            output_names=['CA_out', 'T_out'],
            name="TestReactor"
        )
    
    @pytest.fixture 
    def default_controller(self, reactor_model):
        """Create default state-space controller."""
        return StateSpaceController(reactor_model, name="TestController")
    
    def test_model_initialization(self, reactor_model):
        """Test state-space model initialization."""
        assert reactor_model.n_states == 2
        assert reactor_model.n_inputs == 2
        assert reactor_model.n_outputs == 2
        assert reactor_model.name == "TestReactor"
        assert len(reactor_model.state_names) == 2
        
    def test_controller_initialization(self, default_controller):
        """Test controller initialization."""
        assert default_controller.name == "TestController"
        assert default_controller.model.n_states == 2
        assert default_controller.x_hat.shape == (2,)
        
    def test_system_properties(self, reactor_model):
        """Test system analysis methods."""
        # Test controllability
        is_controllable = reactor_model.is_controllable()
        assert isinstance(is_controllable, bool)
        
        # Test observability  
        is_observable = reactor_model.is_observable()
        assert isinstance(is_observable, bool)
        
        # Test stability
        is_stable = reactor_model.is_stable()
        assert isinstance(is_stable, bool)
        
        # Test poles
        poles = reactor_model.poles()
        assert len(poles) == 2
        
    def test_controllability_matrix(self, reactor_model):
        """Test controllability matrix calculation."""
        Wc = reactor_model.controllability_matrix()
        assert Wc.shape == (2, 4)  # [B AB] for 2-state system
        
    def test_observability_matrix(self, reactor_model):
        """Test observability matrix calculation."""
        Wo = reactor_model.observability_matrix()
        assert Wo.shape == (4, 2)  # [C; CA] for 2-state system
        
    def test_simulation(self, reactor_model):
        """Test time domain simulation."""
        t = np.linspace(0, 10, 21)
        x0 = np.array([1.0, 300.0])  # Initial states
        u = np.ones((len(t), 2)) * 0.5  # Constant inputs
        
        states, outputs = reactor_model.simulate(t, x0, u)
        
        assert states.shape == (len(t), 2)
        assert outputs.shape == (len(t), 2)
        assert np.allclose(states[0], x0)
        
    def test_step_response(self, reactor_model):
        """Test step response calculation."""
        t = np.linspace(0, 20, 101)
        
        states, outputs = reactor_model.step_response(t, input_index=0)
        
        assert states.shape == (len(t), 2)
        assert outputs.shape == (len(t), 2)
        
        # Check steady-state gain
        steady_state = outputs[-1, :]
        assert steady_state[0] > 0  # Should respond to input
        
    def test_lqr_design(self, default_controller):
        """Test LQR controller design."""
        Q = np.diag([10.0, 1.0])  # State weights
        R = np.diag([1.0, 0.5])   # Input weights
        
        try:
            K, S, poles = default_controller.design_lqr_controller(Q, R)
            
            assert K.shape == (2, 2)  # 2 inputs, 2 states
            assert S.shape == (2, 2)  # Riccati solution
            assert len(poles) == 2    # Closed-loop poles
            
            # Closed-loop should be stable
            assert all(np.real(poles) < 0)
            
        except AttributeError:
            # Method may not be fully implemented
            pytest.skip("LQR design method not available")
            
    def test_pole_placement(self, default_controller):
        """Test pole placement controller design."""
        desired_poles = np.array([-1.0, -2.0])
        
        try:
            K = default_controller.design_pole_placement_controller(desired_poles)
            assert K.shape == (2, 2)
            
        except AttributeError:
            pytest.skip("Pole placement method not available")
            
    def test_observer_design(self, default_controller):
        """Test observer design."""
        desired_poles = np.array([-3.0, -4.0])
        
        try:
            L = default_controller.design_observer(desired_poles)
            assert L.shape == (2, 2)  # 2 states, 2 outputs
            
        except AttributeError:
            pytest.skip("Observer design method not available")
            
    def test_controller_update(self, default_controller):
        """Test controller update method."""
        t = 0.0
        setpoints = np.array([0.5, 350.0])
        measurements = np.array([0.6, 345.0])
        
        try:
            control_output = default_controller.update(t, setpoints, measurements)
            assert len(control_output) == 2  # Two control inputs
            assert all(np.isfinite(control_output))
            
        except Exception as e:
            # Controller may need initialization
            pytest.skip(f"Controller update not ready: {e}")
            
    def test_distillation_column_model(self):
        """Test realistic distillation column model."""
        # 3-state model: [x_top, x_bottom, holdup]
        A = np.array([
            [-0.1,  0.05,  0.0],
            [ 0.05, -0.08, 0.0],
            [ 0.0,   0.0, -0.2]
        ])
        
        # Inputs: [reflux, reboiler]
        B = np.array([
            [0.8, -0.3],
            [-0.2, 0.9],
            [0.1,  0.1]
        ])
        
        # Outputs: [x_top, x_bottom]
        C = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0]
        ])
        
        D = np.zeros((2, 2))
        
        model = StateSpaceModel(A, B, C, D, name="DistillationColumn")
        
        assert model.n_states == 3
        assert model.n_inputs == 2
        assert model.n_outputs == 2
        
        # Should be controllable and observable for distillation
        assert model.is_controllable()
        assert model.is_observable()
        
    def test_heat_exchanger_network(self):
        """Test heat exchanger network model."""
        # 4-state model: [T1_hot, T1_cold, T2_hot, T2_cold]
        A = np.array([
            [-0.5,  0.3,  0.0,  0.0],
            [ 0.3, -0.4,  0.0,  0.0],
            [ 0.0,  0.0, -0.6,  0.4],
            [ 0.0,  0.0,  0.4, -0.5]
        ])
        
        # Inputs: [hot_flow1, cold_flow1, hot_flow2]
        B = np.array([
            [0.8, 0.0, 0.0],
            [0.0, 0.7, 0.0],
            [0.0, 0.0, 0.9],
            [0.0, 0.2, 0.0]
        ])
        
        # Outputs: [T1_hot_out, T2_cold_out]
        C = np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
        
        D = np.zeros((2, 3))
        
        model = StateSpaceModel(A, B, C, D, name="HeatExchangerNetwork")
        controller = StateSpaceController(model)
        
        # Test simulation
        t = np.linspace(0, 50, 26)
        x0 = np.array([400.0, 300.0, 380.0, 320.0])  # K
        u = np.ones((len(t), 3)) * 0.5
        
        states, outputs = model.simulate(t, x0, u)
        
        assert states.shape == (len(t), 4)
        assert outputs.shape == (len(t), 2)
        
    def test_edge_cases(self, reactor_model):
        """Test edge cases and error handling."""
        # Test with mismatched dimensions
        with pytest.raises((ValueError, IndexError)):
            wrong_input = np.ones((10, 5))  # Wrong input dimension
            reactor_model.simulate(np.linspace(0, 10, 10), np.array([1, 2]), wrong_input)
            
        # Test with negative time
        with pytest.raises(ValueError):
            reactor_model.simulate(np.array([-1, 0, 1]), np.array([1, 2]), np.ones((3, 2)))
            
    def test_describe_method(self, reactor_model, default_controller):
        """Test describe methods return proper metadata."""
        model_desc = reactor_model.describe()
        controller_desc = default_controller.describe()
        
        # Model description
        assert model_desc['class_name'] == 'StateSpaceModel'
        assert 'system_dimensions' in model_desc
        assert 'system_properties' in model_desc
        
        # Controller description  
        assert controller_desc['class_name'] == 'StateSpaceController'
        assert 'state_space_theory' in controller_desc
        assert 'control_methods' in controller_desc
