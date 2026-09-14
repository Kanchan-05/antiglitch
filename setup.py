from setuptools import setup, find_packages

VERSION = "0.1"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="antiglitch",
    version=VERSION,
    description="A PyCBC plugin for generating an anti-glitch waveform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kanchan Soni",
    author_email="ksoni01@syr.edu",
    url="https://github.com/Kanchan-05/antiglitch",
    keywords=["gravitational waves", "pycbc", "anti-glitch"],
    packages=find_packages(),
    python_requires=">=3.11",

    entry_points={
        "pycbc.waveform.td": [
            "antiglitch = antiglitch.gen_waveform:antiglitch_waveform_td",
        ],
        "pycbc.waveform.fd": [
            "antiglitch = antiglitch.gen_waveform:antiglitch_waveform_fd",
        ],
    },

    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],

    install_requires=[
        "pycbc",
    ],
)
