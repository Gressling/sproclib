"""
Test cases for FixedBedReactor model

Tests cover initialization, bed properties, catalytic reactions,
and axial profiles.

Author: SPROCLIB Development Team
"""

import pytest
import numpy as np
from unit.reactor.FixedBedReactor import FixedBedReactor


class TestFixedBedReactor:
    """Test suite for FixedBedReactor model."""
    
    @pytest.fixture
    def default_fixed_bed(self):
        """Create a FixedBedReactor instance with default parameters."""
        return FixedBedReactor()
    
    @pytest.fixture
    def test_inputs(self):
        """Standard test inputs for FixedBedReactor."""
        return np.array([0.1, 1000.0, 450.0, 430.0])  # [u, CAi, Ti, Tw]
    
    def test_initialization_default(self, default_fixed_bed):
        """Test FixedBedReactor initialization with default parameters."""
        reactor = default_fixed_bed
        
        assert reactor.L == 5.0
        assert reactor.D == 1.0
        assert reactor.epsilon == 0.4
        assert reactor.rho_cat == 1500.0
        assert reactor.dp == 0.005
        assert reactor.n_segments == 20
        assert reactor.name == "FixedBedReactor"
        
        # Check derived properties
        assert reactor.A_cross > 0
        assert reactor.V_void > 0
        assert reactor.W_cat_segment > 0
    
    def test_reaction_rate(self, default_fixed_bed):
        """Test reaction rate calculation."""
        CA = 1000.0  # mol/m³
        T = 450.0    # K
        
        rate = default_fixed_bed.reaction_rate(CA, T)
        
        assert rate > 0
        assert isinstance(rate, (int, float, np.number))
    
    def test_steady_state_calculation(self, default_fixed_bed, test_inputs):
        """Test steady-state calculation."""
        x_ss = default_fixed_bed.steady_state(test_inputs)
        
        assert len(x_ss) == 2 * default_fixed_bed.n_segments
        
        # Extract profiles
        n_seg = default_fixed_bed.n_segments
        CA_profile = x_ss[:n_seg]
        T_profile = x_ss[n_seg:]
        
        assert all(ca >= 0 for ca in CA_profile)
        assert all(t > 0 for t in T_profile)
    
    def test_conversion_calculation(self, default_fixed_bed):
        """Test conversion calculation."""
        n_seg = default_fixed_bed.n_segments
        CA_inlet = 1000.0
        CA_outlet = 700.0
        
        CA_profile = np.linspace(CA_inlet, CA_outlet, n_seg)
        T_profile = np.full(n_seg, 450.0)
        x = np.concatenate([CA_profile, T_profile])
        
        conversion = default_fixed_bed.calculate_conversion(x)
        expected_conversion = (CA_inlet - CA_outlet) / CA_inlet
        
        assert abs(conversion - expected_conversion) < 1e-10
    
    def test_describe_method(self, default_fixed_bed):
        """Test describe method for metadata."""
        metadata = default_fixed_bed.describe()
        
        assert metadata['type'] == 'FixedBedReactor'
        assert metadata['category'] == 'reactor'
        assert 'L' in metadata['parameters']
        assert 'epsilon' in metadata['parameters']
    
    def test_bed_properties(self, default_fixed_bed):
        """Test bed property calculations."""
        reactor = default_fixed_bed
        
        # Check volume calculations
        total_volume = np.pi * (reactor.D/2)**2 * reactor.L
        assert abs(reactor.V_total - total_volume) < 1e-10
        
        void_volume = total_volume * reactor.epsilon
        assert abs(reactor.V_void - void_volume) < 1e-10
        
        # Check catalyst mass per segment
        expected_W_cat = reactor.rho_cat * (1 - reactor.epsilon) * reactor.A_cross * reactor.dz
        assert abs(reactor.W_cat_segment - expected_W_cat) < 1e-10
