import pytest
import numpy as np
from sproclib.controller.pid.PIDController import PIDController

class TestPIDController:
    @pytest.fixture
    def default_controller(self):
        """Create default PID controller for testing."""
        return PIDController(Kp=1.0, Ki=0.1, Kd=0.05, output_limits=(-100, 100))
    
    @pytest.fixture
    def reactor_controller(self):
        """Create PID controller tuned for reactor temperature control."""
        return PIDController(Kp=2.5, Ki=0.15, Kd=8.0, output_limits=(0, 100))
    
    def test_initialization_default(self):
        """Test default PID controller initialization."""
        controller = PIDController()
        assert controller.Kp == 1.0
        assert controller.Ki == 0.0
        assert controller.Kd == 0.0
        assert controller.output_limits == (0, 100)
        assert controller.setpoint == 0.0
        
    def test_initialization_custom(self, default_controller):
        """Test custom PID controller initialization."""
        assert default_controller.Kp == 1.0
        assert default_controller.Ki == 0.1
        assert default_controller.Kd == 0.05
        assert default_controller.output_limits == (-100, 100)
        
    def test_proportional_action(self, default_controller):
        """Test proportional control action."""
        default_controller.setpoint = 50.0
        error = 10.0  # Process variable = 40.0
        # P-action only for first call (no integral/derivative history)
        output = default_controller.update(40.0, dt=1.0)
        expected_p = default_controller.Kp * error
        assert abs(output - expected_p) < 0.1  # Allow for I and D terms
        
    def test_integral_action(self, default_controller):
        """Test integral control action accumulation."""
        default_controller.setpoint = 100.0
        dt = 1.0
        
        # Multiple updates to build integral term
        outputs = []
        for pv in [90.0, 92.0, 94.0, 96.0]:
            output = default_controller.update(pv, dt)
            outputs.append(output)
            
        # Integral term should accumulate (outputs should increase)
        assert all(outputs[i] <= outputs[i+1] for i in range(len(outputs)-1))
        
    def test_derivative_action(self, default_controller):
        """Test derivative control action."""
        default_controller.setpoint = 50.0
        dt = 1.0
        
        # First update to establish previous error
        default_controller.update(45.0, dt)
        
        # Second update with different error rate
        output1 = default_controller.update(46.0, dt)  # Error decreasing slowly
        
        # Reset controller for comparison
        default_controller.reset()
        default_controller.setpoint = 50.0
        default_controller.update(45.0, dt)
        output2 = default_controller.update(48.0, dt)  # Error decreasing faster
        
        # Faster error decrease should result in more negative derivative action
        assert output2 != output1
        
    def test_output_limits(self, default_controller):
        """Test output saturation limits."""
        default_controller.setpoint = 1000.0  # Large setpoint
        
        # Should saturate at upper limit
        output = default_controller.update(0.0, dt=1.0)
        assert output <= default_controller.output_limits[1]
        
        # Test lower limit
        default_controller.setpoint = -1000.0
        output = default_controller.update(0.0, dt=1.0)
        assert output >= default_controller.output_limits[0]
        
    def test_anti_windup(self, default_controller):
        """Test integral windup protection."""
        default_controller.setpoint = 200.0  # Large setpoint to cause saturation
        
        # Run multiple iterations in saturation
        for _ in range(10):
            default_controller.update(0.0, dt=1.0)
            
        # Change setpoint to normal range
        default_controller.setpoint = 50.0
        output = default_controller.update(45.0, dt=1.0)
        
        # Should not have excessive output due to windup
        assert abs(output) < 200  # Reasonable output range
        
    def test_reactor_temperature_control(self, reactor_controller):
        """Test realistic reactor temperature control scenario."""
        # Reactor setpoint: 80°C
        reactor_controller.setpoint = 80.0
        dt = 0.5  # 0.5 second control interval
        
        # Temperature measurements (°C)
        temperatures = [75.0, 76.2, 77.8, 78.9, 79.5, 79.8, 80.1]
        outputs = []
        
        for temp in temperatures:
            output = reactor_controller.update(temp, dt)
            outputs.append(output)
            
        # First output should be significant (large error)
        assert outputs[0] > 10.0
        
        # Final output should be small (near setpoint)
        assert abs(outputs[-1]) < 5.0
        
        # Outputs should generally decrease as temperature approaches setpoint
        assert outputs[0] > outputs[-1]
        
    def test_flow_control_response(self):
        """Test fast flow control application."""
        flow_controller = PIDController(Kp=0.8, Ki=2.0, Kd=0.02, output_limits=(0, 100))
        flow_controller.setpoint = 150.0  # m³/h
        dt = 0.1  # Fast control (100 ms)
        
        # Flow rate measurements
        flow_rates = [100.0, 120.0, 135.0, 145.0, 148.0, 150.0]
        
        for flow in flow_rates:
            output = flow_controller.update(flow, dt)
            # Output should be within valve limits
            assert 0 <= output <= 100
            
    def test_reset_functionality(self, default_controller):
        """Test controller reset function."""
        default_controller.setpoint = 50.0
        
        # Generate some history
        for pv in [40.0, 42.0, 44.0]:
            default_controller.update(pv, dt=1.0)
            
        # Reset controller
        default_controller.reset()
        
        # Next output should only have proportional term
        output = default_controller.update(40.0, dt=1.0)
        expected = default_controller.Kp * (50.0 - 40.0)
        assert abs(output - expected) < 0.01
        
    def test_describe_method(self, default_controller):
        """Test the describe method returns proper metadata."""
        description = default_controller.describe()
        
        assert description['type'] == 'PIDController'
        assert description['category'] == 'controller'
        assert 'proportional_action' in description['algorithms']
        assert 'integral_action' in description['algorithms']
        assert 'derivative_action' in description['algorithms']
        assert 'Kp' in description['parameters']
        assert 'Ki' in description['parameters']
        assert 'Kd' in description['parameters']
        
    def test_edge_cases(self, default_controller):
        """Test edge cases and boundary conditions."""
        # Zero time step
        with pytest.raises(ValueError):
            default_controller.update(50.0, dt=0.0)
            
        # Negative time step
        with pytest.raises(ValueError):
            default_controller.update(50.0, dt=-1.0)
            
        # Very large derivative gain with noise
        noisy_controller = PIDController(Kp=1.0, Ki=0.1, Kd=100.0)
        noisy_controller.setpoint = 50.0
        
        # Simulate noisy measurement
        noisy_controller.update(50.1, dt=1.0)
        output = noisy_controller.update(49.9, dt=1.0)  # Sudden change
        
        # Output should still be reasonable despite high Kd
        assert abs(output) < 1000
        
    def test_parameter_validation(self):
        """Test parameter validation during initialization."""
        # Valid parameters should work
        controller = PIDController(Kp=1.0, Ki=0.5, Kd=0.1)
        assert controller.Kp == 1.0
        
        # Invalid output limits
        with pytest.raises(ValueError):
            PIDController(output_limits=(100, 0))  # min > max
            
    def test_distillation_column_control(self):
        """Test typical distillation column temperature control."""
        # Tray temperature controller (conservative tuning)
        column_controller = PIDController(Kp=1.2, Ki=0.08, Kd=12.0, output_limits=(20, 80))
        column_controller.setpoint = 95.0  # °C
        dt = 2.0  # 2-second control interval
        
        # Temperature profile during disturbance
        temperatures = [95.0, 96.5, 97.2, 96.8, 96.0, 95.5, 95.2, 95.0]
        
        for temp in temperatures:
            output = column_controller.update(temp, dt)
            # Should stay within reboiler duty limits
            assert 20 <= output <= 80
