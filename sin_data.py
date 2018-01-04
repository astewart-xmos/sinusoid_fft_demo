
import numpy as np

from constants import *


class SinData(object):
    """
    This class stores the data needed for rendering most of the views.

    It really just helps provide a more uniform API for interacting with the views.
    """

    def __init__(self, params):

        self.amplitude = params.amplitude
        self.phase = params.phase
        self.frequency = params.frequency

        self.window = np.hanning(WINDOW_SIZE+1)[:WINDOW_SIZE]
        self.sample_indices = np.arange(0, WINDOW_SIZE)
        self.sinusoid = params.amplitude * np.cos(2*np.pi * params.frequency 
                                    * self.sample_indices / float(WINDOW_SIZE) + params.phase)

        self.sinusoid_windowed = self.window * self.sinusoid

        self.bins_lo = np.arange(-FFT_N/2, FFT_N/2) / float(1)
        self.bins_hi = np.arange(-(FFT_N*UPSAMPLE)/2, (FFT_N*UPSAMPLE)/2) / float(UPSAMPLE)

        self.spectrum_lo = np.fft.fft(self.sinusoid_windowed, FFT_N) / FFT_N
        self.spectrum_hi = np.fft.fft(self.sinusoid_windowed, FFT_N*UPSAMPLE) / FFT_N

        self.spectrum_lo = np.fft.fftshift(self.spectrum_lo)
        self.spectrum_hi = np.fft.fftshift(self.spectrum_hi)

        self.spectrum_real_lo = np.real(self.spectrum_lo)
        self.spectrum_imag_lo = np.imag(self.spectrum_lo)

        self.spectrum_real_hi = np.real(self.spectrum_hi)
        self.spectrum_imag_hi = np.imag(self.spectrum_hi)

        self.spectrum_mag_lo = np.abs(self.spectrum_lo)
        self.spectrum_mag_hi = np.abs(self.spectrum_hi)


