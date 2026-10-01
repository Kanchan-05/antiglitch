import numpy as np
from pycbc.types import FrequencySeries, TimeSeries

def antiglitch_waveform_td(**kwds):
    """Generate anti-glitch waveform in the time domain,
    centered at t = 0.
    """

    delta_t = kwds['delta_t']

    # Sampling frequency and Nyquist
    sample_rate = 1.0 / delta_t
    f_nyquist = sample_rate / 2.0

    # Choose duration of TD waveform
    duration = 1.0

    # Corresponding frequency resolution
    delta_f = 1.0 / duration

    # Generate FD waveform
    fd_kwds = kwds.copy()
    fd_kwds['delta_f'] = delta_f
    fd_kwds['f_final'] = f_nyquist

    hp_fd, hc_fd = antiglitch_waveform_fd(**fd_kwds)

    # Convert to TD
    hp_raw = hp_fd.to_timeseries(delta_t=delta_t)
    hc_raw = hc_fd.to_timeseries(delta_t=delta_t)

    # Move FFT t=0 from index 0 to center of array
    hp_data = np.fft.fftshift(np.asarray(hp_raw))
    hc_data = np.fft.fftshift(np.asarray(hc_raw))

    N = len(hp_data)

    # Set middle sample to t = 0
    epoch = -(N // 2) * delta_t

    hp = TimeSeries(hp_data, delta_t=delta_t, epoch=epoch)

    hc = TimeSeries(hc_data, delta_t=delta_t, epoch=epoch)

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