# EEG_Signal_Processing

Analysis of a single channel EEG signal. This is used to find the band with highest bandpowwer which is used to determine the state of the brain. It can be used to conclude what the person is doing, according to previously found results.

There are two processing algorithms, welch periodogram and multitaper analysis. Both cut the given signal into small windows, then calculate their Power spectral density. Multitaper also applies some windowing functions with overlaps to reduce the artifacts produced by cutting the data into windows. Overall, both are optimizations of regular fourier transforms and PSDs to save computational resources at some expense of data resolution. However, to determine Relative and Absolute bandpower, the resolution is quite sufficient to make concrete inferences.
