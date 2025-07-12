"""
Test cases for SemiBatchReactor model

Tests cover fed-batch operation, variable volume,
and feeding strategies.

Author: SPROCLIB Development Team
"""

import pytest
import numpy as np
from unit.reactor.SemiBatchReactor import SemiBatchReactor


class TestSemiBatchReactor:
    """Test suite for SemiBatchReactor model."""
    
    @pytest.fixture
    def default_semi_batch(self):
        """Create a SemiBatchReactor instance with default parameters."""
        return SemiBatchReactor()
    
    @pytest.fixture
    def test_inputs(self):
        """Standard test inputs for SemiBatchReactor."""
        return np.array([350.0, 10.0, 2.0])  # [Tj, F_in, CA_in]
    
    def test_initialization_default(self, default_semi_batch):
        """Test SemiBatchReactor initialization."""
        reactor = default_semi_batch
        
        assert reactor.V_max == 200.0
        assert reactor.k0 == 7.2e10
        assert reactor.name == "SemiBatchReactor"
    
    def test_describe_method(self, default_semi_batch):
        """Test describe method for metadata."""
        metadata = default_semi_batch.describe()
        
        assert metadata['type'] == 'SemiBatchReactor'
        assert 'Fed-batch processes' in metadata['applications']
