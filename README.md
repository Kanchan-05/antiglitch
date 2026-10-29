# Antiglitch

A PyCBC waveform plugin for generating phenomenological anti-glitch waveforms with a log-Gaussian frequency profile.

The package provides frequency-domain and time-domain waveforms through PyCBC's standard waveform interface, using the approximant name antiglitch. It is intended for waveform studies and integration into PyCBC-based injection and matched-filter analyses. The waveform implementation references the model described in arXiv:2309.06594.

### Installation 

```
git clone git@github.com:Kanchan-05/antiglitch.git
cd antiglitch
python -m pip install -e .
```

To check that PyCBC discovers both waveform entry points:

```
from pycbc.waveform import fd_approximants, td_approximants
print("FD:", "antiglitch" in fd_approximants())
print("TD:", "antiglitch" in td_approximants())
```
Both checks should return `True`.

### Usage
See [test_waveform.ipynb](test_waveform.ipynb) for examples of generating and plotting anti-glitch waveforms in the time and frequency domains.

The plugin is available through PyCBC under the approximant name `antiglitch`.
