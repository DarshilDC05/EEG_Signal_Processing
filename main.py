import matplotlib.pyplot as plt
import numpy as np
import scipy

#sampling frequency = 100Hz
#signal length = 30seconds

#frequency band ranges
delta_low, delta_upp = 0.5, 4
theta_low, theta_upp = 4, 8
alpha_low, alpha_upp = 8, 12
beta_low, beta_upp = 12, 30

#plot the eeg-data
signal = np.loadtxt('./eeg-data.txt')
signal_span = np.arange(0.01, 30.01, 0.01)
plt.subplot(2, 2, 1)
plt.plot(signal_span, signal)
plt.title("Input EEG Data")
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (Volts)")
plt.grid()

#x-axis resolution = sampling frequency/number of samples
sampling_frequency = 100
signal_length = 30
sample_size = sampling_frequency * signal_length
fourier_x_resolution = 1/signal_length
fourier_x = np.arange(0, sampling_frequency/2, fourier_x_resolution)

#computing the fourier transform
fft_raw = np.fft.fft(signal)
fft_value = np.abs(fft_raw)
fft_value = fft_value[0: 1500]/1500

#plotting to fourier transform
plt.subplot(2, 2, 2)
plt.plot(fourier_x, fft_value)
plt.title("Fourier Transform")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Voltage (Volts)")
plt.grid()

ip = input("Enter the method (welch or multitaper) you want to use to compute the bandpowers :")
if ip == 'welch' :
    # computing the welch's periodogram
    window = 4 * sampling_frequency
    frequency_range, pow_spec_density = scipy.signal.welch(signal, sampling_frequency, window='hann', nperseg=window)
    frequency_resolution = frequency_range[1] - frequency_range[0]

    # plotting welch's periodogram
    plt.subplot(2, 2, 3)
    plt.plot(frequency_range, pow_spec_density)
    plt.title("Welch's Periodogram")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power Spectral Density (V^2/Hz)")
    plt.grid()

elif ip == 'multitaper':
    #computing the multitaper periodogram
    import mne.time_frequency
    window = 4 * sampling_frequency
    pow_spec_density, frequency_range = mne.time_frequency.psd_array_multitaper(signal, sampling_frequency, adaptive=True, normalization='full', verbose=0)
    frequency_resolution = frequency_range[1] - frequency_range[0]

    #plotting the multitaper periodogram
    plt.subplot(2, 2, 3)
    plt.plot(frequency_range, pow_spec_density)
    plt.title("Multitaper")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power Spectral Density (V^2/Hz)")
    plt.grid()

#computing the bandpowers of frequency ranges
delta_range = np.logical_and(frequency_range>=delta_low, frequency_range<=delta_upp)
theta_range = np.logical_and(frequency_range>=theta_low, frequency_range<=theta_upp)
alpha_range = np.logical_and(frequency_range>=alpha_low, frequency_range<=alpha_upp)
beta_range = np.logical_and(frequency_range>=beta_low, frequency_range<=beta_upp)

total_bandpoower = np.trapezoid(pow_spec_density, dx = frequency_resolution)

delta_bandpower = np.trapezoid(pow_spec_density[delta_range], dx = frequency_resolution)
theta_bandpower = np.trapezoid(pow_spec_density[theta_range], dx = frequency_resolution)
alpha_bandpower = np.trapezoid(pow_spec_density[alpha_range], dx = frequency_resolution)
beta_bandpower = np.trapezoid(pow_spec_density[beta_range], dx = frequency_resolution)

delta_percent = (delta_bandpower/total_bandpoower)*100
theta_percent = (theta_bandpower/total_bandpoower)*100
alpha_percent = (alpha_bandpower/total_bandpoower)*100
beta_percent = (beta_bandpower/total_bandpoower)*100

print("Absolute Delta Power = %.2f uV^2" %delta_bandpower)
print("Relative Delta Power = %.2f percent" %delta_percent)
print("")
print("Absolute Theta Power = %.2f uV^2" %theta_bandpower)
print("Relative Theta Power = %.2f percent" %theta_percent)
print("")
print("Absolute Alpha Power = %.2f uV^2" %alpha_bandpower)
print("Relative Alpha Power = %.2f percent" %alpha_percent)
print("")
print("Absolute Beta Power = %.2f uV^2" %beta_bandpower)
print("Relative Beta Power = %.2f percent" %beta_percent)

#plotting the bandpowers
rel_data = {'Delta' : delta_percent, 'Theta' : theta_percent, 'Alpha' : alpha_percent, 'Beta' : beta_percent}
bands = list(rel_data.keys())
values = list(rel_data.values())

plt.subplot(2, 2, 4)
plt.bar(bands, values, width = 0.5)
plt.title("Band Distribution")
plt.xlabel("Frequency Bands")
plt.ylabel("Relative Abundance (%)")
plt.show()



