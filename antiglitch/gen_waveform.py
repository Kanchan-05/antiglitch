import numpy as np
from pycbc.types import FrequencySeries, TimeSeries

def antiglitch_waveform_fd(**kwds):
    """
    Generate a frequency-domain anti-glitch waveform with a log-Gaussian profile.
    Based on the model described in https://arxiv.org/abs/2309.06594.
    """
    
    delta_f = float(kwds["delta_f"])
    f_lower = float(kwds["f_lower"])
    f_final = float(kwds["f_final"])
    f0 = float(kwds["f0"])
    gbw = float(kwds["gbw"])
    amp = float(kwds["amp"])
    phase = float(kwds.get("coa_phase", 0.0))
    t0 = float(kwds.get("tc", 0.0))

    if delta_f <= 0 or f0 <= 0 or gbw <= 0:
        raise ValueError("delta_f, f0 and gbw must be positive.")
    if not 0 <= f_lower < f_final:
        raise ValueError("Require 0 <= f_lower < f_final.")

    n = int(np.floor(f_final / delta_f))
    freqs = np.arange(n + 1) * delta_f
    h = np.zeros(n + 1, dtype=np.complex128)
    mask = (freqs > 0) & (freqs >= f_lower)

    h[mask] = amp * np.exp(
        -0.5 * gbw * np.log(freqs[mask] / f0)**2
        + 1j * phase - 2j * np.pi * freqs[mask] * t0
    )

    hp = FrequencySeries(h, delta_f=delta_f)
    hc = FrequencySeries(np.zeros_like(h), delta_f=delta_f)
    return hp, hc

def antiglitch_waveform_td(**kwds):
    """Generate the TD waveform with its absolute peak at t=0."""
    delta_t = float(kwds["delta_t"])
    delta_f = float(kwds.get("delta_f") or 0.125)

    if delta_t <= 0 or delta_f <= 0:
        raise ValueError("delta_t and delta_f must be positive.")

    n_float = 1.0 / (delta_t * delta_f)
    n = int(round(n_float))
    if n < 4 or n % 2 or not np.isclose(n_float, n, rtol=0, atol=1e-6):
        raise ValueError("1 / (delta_t * delta_f) must be an even integer >= 4.")

    nyquist = 0.5 / delta_t
    fd_kwds = kwds.copy()
    fd_kwds["delta_f"] = delta_f
    fd_kwds["f_final"] = min(float(kwds.get("f_final") or nyquist), nyquist)
    fd_kwds["t0"] = 0.0
    hp_fd, _ = antiglitch_waveform_fd(**fd_kwds)

    spectrum = np.zeros(n // 2 + 1, dtype=np.complex128)
    spectrum[:len(hp_fd)] = hp_fd.numpy()
    spectrum[-1] = 0.0

    h = np.fft.irfft(spectrum, n=n) / delta_t

    # Put the largest absolute sample at the center of the array.
    peak_index = np.argmax(np.abs(h))
    h = np.roll(h, n // 2 - peak_index)

    # The central sample now has time exactly zero.
    epoch = -(n // 2) * delta_t
    hp = TimeSeries(h, delta_t=delta_t, epoch=epoch)
    hc = TimeSeries(np.zeros_like(h), delta_t=delta_t, epoch=epoch)
    return hp, hc