from matplotlib import pyplot as plt
from numpy import arange, sin, round, fft, pi, asarray, floor, random

freq1 = 1
freq2 = 1.4
noise_variance = 0.9 ** 2

time = [round(value, 2) for value in arange(0, 10, 0.1)]
sin_value = round(sin(2 * pi * freq1 * asarray(time)), 3) + 1.5 * round(sin(2 * pi * freq2 * asarray(time)), 3)
noise = random.rand(len(time)) * noise_variance
sin_value = sin_value + noise
plt.figure(1)
plt.plot(time, sin_value)

fourier = fft.fft(sin_value)
freqs = fft.fftfreq(len(sin_value)) * len(sin_value) * (time[1] - time[0])
# print(type(int(floor(len(freqs) / 2))))
plt.figure(2)
plt.plot(freqs[0:int(floor(len(freqs) / 2))], abs(fourier[0:int(floor(len(freqs) / 2))]))
plt.show()
