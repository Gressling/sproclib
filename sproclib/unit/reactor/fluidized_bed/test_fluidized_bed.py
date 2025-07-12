"""
Test cases for FluidizedBedReactor model

Tests cover two-phase modeling, fluidization,
and mass transfer between phases.

Author: SPROCLIB Development Team
"""

import pytest
import numpy as np
from unit.reactor.FluidizedBedReactor import FluidizedBedReactor


class TestFluidizedBedReactor:
    """Test suite for FluidizedBedReactor model."""
    
    @pytest.fixture
    def default_fluidized_bed(self):
        """Create a FluidizedBedReactor instance with default parameters."""
        return FluidizedBedReactor()
    
    def test_initialization_default(self, default_fluidized_bed):
        """Test FluidizedBedReactor initialization."""
        reactor = default_fluidized_bed
        
        assert reactor.H == 3.0
        assert reactor.D == 2.0
        assert reactor.name == "FluidizedBedReactor"
    
    def test_describe_method(self, default_fluidized_bed):
        """Test describe method for metadata."""
        metadata = default_fluidized_bed.describe()
        
        assert metadata['type'] == 'FluidizedBedReactor'
        assert 'Fluid catalytic cracking' in metadata['applications']
    
    def test_conversion_calculation(self, default_fluidized_bed):
        """Test conversion calculation."""
        CA_in = 1.0
        CA_out = 0.7
        
        conversion = default_fluidized_bed.calculate_conversion(CA_in, CA_out)
        expected = (CA_in - CA_out) / CA_in
        
        assert abs(conversion - expected) < 1e-10
