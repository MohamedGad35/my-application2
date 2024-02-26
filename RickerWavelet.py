# This script is written to create a ricker wavelet 

import numpy as np 
import matplotlib.pyplot as plt

#wavelet paramters
waveletlength=0.265 # wavelength 
dt=0.001  #sampling rate
frequency= 40 # wavelet frequency in Hz

def ricker_wavelet(wavelength, dt, peak_frequency):
    '''This function is used to estimate ricker wavelet  '''
    time = np.arange(-waveletlength/2, (waveletlength-dt)/2, dt)
    wavelet = (1.0 - 2.0*(np.pi**2)*(frequency**2)*(time**2)
                 ) * np.exp(-(np.pi**2)*(frequency**2)*(time**2))
    return  time, wavelet

#create a ricker wavelet
time, wavelet = ricker_wavelet(waveletlength, dt, frequency)

#plotting the ricker wavelet
fig = plt.figure(figsize=(10, 10))
fig.set_facecolor('violet')
ax0 = fig.add_subplot()
plt.plot(time, wavelet)
plt.title('%d Hz Ricker wavelet' %frequency, fontsize = 16 )
plt.xlim(-waveletlength/4, waveletlength/4)
plt.xlabel( 'Two-way time (sec)', fontsize = 16)
plt.ylabel('Amplitude', fontsize = 16)
plt.fill_between(time, wavelet, 0,  wavelet > 0.0, color='blue', alpha = 0.6)
plt.fill_between(time, wavelet, 0, wavelet < 0.0, color='red', alpha = 0.6)
plt.grid()
#plt.ylim(-1, 1)