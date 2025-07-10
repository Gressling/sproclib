"""
Transfer Function Analysis for SPROCLIB

This module provides transfer function representation and frequency domain analysis
for linear time-invariant systems in process control applications.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
from typing import Optional, Tuple, Dict, Any, List, Union
import matplotlib.pyplot as plt
from scipy import signal
import logging

logger = logging.getLogger(__name__)


class TransferFunction:
    """Transfer function representation and analysis."""
    
    def __init__(
        self,
        num: Union[List[float], np.ndarray],
        den: Union[List[float], np.ndarray],
        name: str = "G(s)"
    ):
        """
        Initialize transfer function G(s) = num(s)/den(s).
        
        Args:
            num: Numerator coefficients (highest order first)
            den: Denominator coefficients (highest order first)
            name: Transfer function name
        """
        self.num = np.array(num)
        self.den = np.array(den)
        self.name = name
        self.sys = signal.TransferFunction(self.num, self.den)
        
        logger.info(f"Transfer function '{name}' created")
    
    @classmethod
    def first_order_plus_dead_time(
        cls,
        K: float,
        tau: float,
        theta: float,
        name: str = "FOPDT"
    ) -> 'TransferFunction':
        """
        Create first-order plus dead time transfer function.
        G(s) = K * exp(-theta*s) / (tau*s + 1)
        
        Args:
            K: Process gain
            tau: Time constant
            theta: Dead time
            name: Transfer function name
            
        Returns:
            TransferFunction object (without dead time for analysis)
        """
        # Note: Dead time approximated with Pade approximation if needed
        num = [K]
        den = [tau, 1]
        tf = cls(num, den, name)
        tf.dead_time = theta
        return tf
    
    @classmethod
    def second_order(
        cls,
        K: float,
        zeta: float,
        wn: float,
        name: str = "Second Order"
    ) -> 'TransferFunction':
        """
        Create second-order transfer function.
        G(s) = K * wn² / (s² + 2*zeta*wn*s + wn²)
        
        Args:
            K: Process gain
            zeta: Damping ratio
            wn: Natural frequency
            name: Transfer function name
            
        Returns:
            TransferFunction object
        """
        num = [K * wn**2]
        den = [1, 2*zeta*wn, wn**2]
        return cls(num, den, name)
    
    def step_response(
        self,
        t: Optional[np.ndarray] = None,
        t_final: float = 10.0,
        input_magnitude: float = 1.0
    ) -> Dict[str, np.ndarray]:
        """
        Calculate step response.
        
        Args:
            t: Time vector (optional)
            t_final: Final time if t not provided
            input_magnitude: Step magnitude
            
        Returns:
            Dictionary with 't' and 'y' arrays
        """
        if t is None:
            t = np.linspace(0, t_final, 1000)
        
        tout, yout = signal.step(self.sys, T=t)
        yout *= input_magnitude
        
        # Add dead time if present
        if hasattr(self, 'dead_time') and self.dead_time > 0:
            theta = self.dead_time
            # Shift response by dead time
            t_shifted = tout - theta
            yout_shifted = np.zeros_like(yout)
            yout_shifted[t_shifted >= 0] = np.interp(
                t_shifted[t_shifted >= 0], tout, yout
            )
            yout = yout_shifted
        
        return {'t': tout, 'y': yout}
    
    def bode_plot(
        self,
        w: Optional[np.ndarray] = None,
        plot: bool = True
    ) -> Dict[str, np.ndarray]:
        """
        Generate Bode plot data.
        
        Args:
            w: Frequency vector (optional)
            plot: Whether to create plot
            
        Returns:
            Dictionary with frequency, magnitude, and phase data
        """
        if w is None:
            w = np.logspace(-2, 2, 1000)
        
        w, mag, phase = signal.bode(self.sys, w)
        
        if plot:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
            
            # Magnitude plot
            ax1.semilogx(w/(2*np.pi), 20*np.log10(mag))
            ax1.set_ylabel('Magnitude (dB)')
            ax1.grid(True, which='both', alpha=0.3)
            ax1.set_title(f'Bode Plot - {self.name}')
            
            # Phase plot
            ax2.semilogx(w/(2*np.pi), np.degrees(phase))
            ax2.set_ylabel('Phase (degrees)')
            ax2.set_xlabel('Frequency (Hz)')
            ax2.grid(True, which='both', alpha=0.3)
            
            plt.tight_layout()
            plt.show()
        
        return {
            'frequency': w,
            'magnitude': mag,
            'phase': phase,
            'magnitude_db': 20*np.log10(mag),
            'phase_deg': np.degrees(phase)
        }
    
    def poles_zeros(self) -> Dict[str, np.ndarray]:
        """Get poles and zeros of transfer function."""
        poles = self.sys.poles
        zeros = self.sys.zeros
        
        return {'poles': poles, 'zeros': zeros}
    
    def stability_analysis(self) -> Dict[str, Any]:
        """Analyze system stability."""
        poles = self.sys.poles
        
        # Check if all poles have negative real parts
        stable = np.all(np.real(poles) < 0)
        
        # Gain and phase margins
        try:
            gm, pm, wg, wp = signal.margin(self.sys)
            gm_db = 20 * np.log10(gm) if gm is not None else None
            pm_deg = np.degrees(pm) if pm is not None else None
        except:
            gm_db, pm_deg, wg, wp = None, None, None, None
        
        return {
            'stable': stable,
            'poles': poles,
            'gain_margin_db': gm_db,
            'phase_margin_deg': pm_deg,
            'gain_crossover_freq': wg,
            'phase_crossover_freq': wp
        }
    
    def frequency_response(
        self,
        w: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate frequency response.
        
        Args:
            w: Frequency vector [rad/s]
            
        Returns:
            Tuple of (magnitude, phase, frequency)
        """
        w, mag, phase = signal.bode(self.sys, w)
        return mag, phase, w
    
    def impulse_response(
        self,
        t: Optional[np.ndarray] = None,
        t_final: float = 10.0
    ) -> Dict[str, np.ndarray]:
        """
        Calculate impulse response.
        
        Args:
            t: Time vector (optional)
            t_final: Final time if t not provided
            
        Returns:
            Dictionary with 't' and 'y' arrays
        """
        if t is None:
            t = np.linspace(0, t_final, 1000)
        
        tout, yout = signal.impulse(self.sys, T=t)
        
        return {'t': tout, 'y': yout}
