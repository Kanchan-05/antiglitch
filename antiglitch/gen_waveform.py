import numpy as np
from pycbc.types import FrequencySeries


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