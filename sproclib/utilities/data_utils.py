"""
Data Utilities for SPROCLIB

This module provides data processing utilities for process control
including filtering, resampling, and data analysis functions.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
from typing import Optional, Tuple, Dict, Any, List
from scipy import signal
import logging

logger = logging.getLogger(__name__)


def filter_data(
    data: np.ndarray,
    filter_type: str = 'lowpass',
    cutoff: float = 0.1,
    order: int = 2,
    method: str = 'butterworth'
) -> np.ndarray:
    """
    Filter time series data.
    
    Args:
        data: Input data array
        filter_type: Type of filter ('lowpass', 'highpass', 'bandpass')
        cutoff: Cutoff frequency (normalized)
        order: Filter order
        method: Filter method ('butterworth', 'chebyshev', 'bessel')
        
    Returns:
        Filtered data array
    """
    try:
        if method.lower() == 'butterworth':
            if filter_type.lower() == 'lowpass':
                b, a = signal.butter(order, cutoff, btype='low')
            elif filter_type.lower() == 'highpass':
                b, a = signal.butter(order, cutoff, btype='high')
            elif filter_type.lower() == 'bandpass':
                if isinstance(cutoff, (list, tuple)) and len(cutoff) == 2:
                    b, a = signal.butter(order, cutoff, btype='band')
                else:
                    raise ValueError("Bandpass filter requires two cutoff frequencies")
            else:
                raise ValueError(f"Unknown filter type: {filter_type}")
        else:
            raise ValueError(f"Unknown filter method: {method}")
        
        # Apply filter
        filtered_data = signal.filtfilt(b, a, data)
        
        return filtered_data
    
    except Exception as e:
        logger.error(f"Data filtering error: {e}")
        return data  # Return original data if filtering fails


def resample_data(
    t: np.ndarray,
    data: np.ndarray,
    new_dt: float,
    method: str = 'linear'
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Resample time series data.
    
    Args:
        t: Original time array
        data: Original data array
        new_dt: New sampling interval
        method: Interpolation method
        
    Returns:
        New time array and resampled data
    """
    from scipy.interpolate import interp1d
    
    try:
        # Create new time array
        t_new = np.arange(t[0], t[-1], new_dt)
        
        # Interpolate data
        interpolator = interp1d(t, data, kind=method, bounds_error=False, fill_value='extrapolate')
        data_new = interpolator(t_new)
        
        return t_new, data_new
    
    except Exception as e:
        logger.error(f"Data resampling error: {e}")
        return t, data


def detect_outliers(
    data: np.ndarray,
    method: str = 'iqr',
    threshold: float = 1.5
) -> np.ndarray:
    """
    Detect outliers in data.
    
    Args:
        data: Input data array
        method: Detection method ('iqr', 'zscore', 'modified_zscore')
        threshold: Threshold for outlier detection
        
    Returns:
        Boolean array indicating outliers
    """
    try:
        if method.lower() == 'iqr':
            Q1 = np.percentile(data, 25)
            Q3 = np.percentile(data, 75)
            IQR = Q3 - Q1
            lower = Q1 - threshold * IQR
            upper = Q3 + threshold * IQR
            outliers = (data < lower) | (data > upper)
        
        elif method.lower() == 'zscore':
            z_scores = np.abs((data - np.mean(data)) / np.std(data))
            outliers = z_scores > threshold
        
        elif method.lower() == 'modified_zscore':
            median = np.median(data)
            mad = np.median(np.abs(data - median))
            modified_z_scores = 0.6745 * (data - median) / mad
            outliers = np.abs(modified_z_scores) > threshold
        
        else:
            raise ValueError(f"Unknown outlier detection method: {method}")
        
        return outliers
    
    except Exception as e:
        logger.error(f"Outlier detection error: {e}")
        return np.zeros(len(data), dtype=bool)


def smooth_data(
    data: np.ndarray,
    window_size: int = 5,
    method: str = 'moving_average'
) -> np.ndarray:
    """
    Smooth data using various methods.
    
    Args:
        data: Input data array
        window_size: Size of smoothing window
        method: Smoothing method ('moving_average', 'savgol', 'exponential')
        
    Returns:
        Smoothed data array
    """
    try:
        if method.lower() == 'moving_average':
            # Simple moving average
            kernel = np.ones(window_size) / window_size
            smoothed = np.convolve(data, kernel, mode='same')
        
        elif method.lower() == 'savgol':
            # Savitzky-Golay filter
            from scipy.signal import savgol_filter
            polyorder = min(3, window_size - 1)
            smoothed = savgol_filter(data, window_size, polyorder)
        
        elif method.lower() == 'exponential':
            # Exponential smoothing
            alpha = 2.0 / (window_size + 1)
            smoothed = np.zeros_like(data)
            smoothed[0] = data[0]
            for i in range(1, len(data)):
                smoothed[i] = alpha * data[i] + (1 - alpha) * smoothed[i-1]
        
        else:
            raise ValueError(f"Unknown smoothing method: {method}")
        
        return smoothed
    
    except Exception as e:
        logger.error(f"Data smoothing error: {e}")
        return data


def calculate_statistics(data: np.ndarray) -> Dict[str, float]:
    """
    Calculate basic statistics for data.
    
    Args:
        data: Input data array
        
    Returns:
        Dictionary with statistical measures
    """
    try:
        stats = {
            'mean': np.mean(data),
            'median': np.median(data),
            'std': np.std(data),
            'var': np.var(data),
            'min': np.min(data),
            'max': np.max(data),
            'range': np.max(data) - np.min(data),
            'skewness': calculate_skewness(data),
            'kurtosis': calculate_kurtosis(data)
        }
        
        return stats
    
    except Exception as e:
        logger.error(f"Statistics calculation error: {e}")
        return {}


def calculate_skewness(data: np.ndarray) -> float:
    """Calculate skewness of data."""
    try:
        n = len(data)
        mean = np.mean(data)
        std = np.std(data)
        
        if std == 0:
            return 0.0
        
        skewness = (n / ((n-1) * (n-2))) * np.sum(((data - mean) / std) ** 3)
        return skewness
    
    except Exception:
        return 0.0


def calculate_kurtosis(data: np.ndarray) -> float:
    """Calculate kurtosis of data."""
    try:
        n = len(data)
        mean = np.mean(data)
        std = np.std(data)
        
        if std == 0:
            return 0.0
        
        kurtosis = (n * (n+1) / ((n-1) * (n-2) * (n-3))) * np.sum(((data - mean) / std) ** 4) - 3 * (n-1)**2 / ((n-2) * (n-3))
        return kurtosis
    
    except Exception:
        return 0.0


__all__ = [
    'filter_data',
    'resample_data',
    'detect_outliers',
    'smooth_data',
    'calculate_statistics',
    'calculate_skewness',
    'calculate_kurtosis'
]
