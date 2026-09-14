import numpy as np
from pycbc.types import FrequencySeries, TimeSeries


def antiglitch_waveform_td(**kwds):
    """Generate anti-glitch waveform in the time domain."""
 
    delta_t = kwds['delta_t'] 

    # Nyquist frequency determined by sampling rate
    f_nyquist = 1.0 / (2 * delta_t)
    delta_f = 1.0 if kwds.get('delta_f') is None else kwds['delta_f']
    
    # Prepare parameters for FD function
    fd_kwds = kwds.copy()
    fd_kwds['delta_f'] = delta_f
    fd_kwds['f_final'] = f_nyquist
    
    # Generate frequency domain waveform
    hp_fd, hc_fd = antiglitch_waveform_fd(**fd_kwds)
    
    # Convert to time domain
    hp = hp_fd.to_timeseries(delta_t=delta_t)
    hc = hc_fd.to_timeseries(delta_t=delta_t)
 
    return hp, hc
 
 
 

def antiglitch_waveform_fd(**kwds):
    """Generate a minimal anti-glitch waveform in the frequency domain."""

    delta_f = kwds['delta_f']
    f_lower = kwds['f_lower']
    f_final = kwds['f_final']

    # PyCBC frequency grid
    n = int(f_final / delta_f)
    freqs = np.arange(n + 1) * delta_f

    # Log-Gaussian spectral shape
    h = np.zeros_like(freqs, dtype=np.complex128)

    mask = freqs >= f_lower
    h[mask] = kwds['amp'] * np.exp(
        -0.5 * kwds['gbw']
        * (np.log(freqs[mask]) - np.log(kwds['f0']))**2
    )

    hp = FrequencySeries(h, delta_f=delta_f)
    hc = FrequencySeries(np.zeros_like(h), delta_f=delta_f)

    return hp, hc