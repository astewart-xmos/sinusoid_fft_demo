
import numpy as np

from constants import *

class Obj(object):
    def __init__(self):
        pass

class SpectrumInfo(object):

    def __init__(self, sinusoid, fft_n):

        self.complex = np.fft.fftshift(np.fft.fft(sinusoid, fft_n) / FFT_N)

        self.real = np.real(self.complex)
        self.imag = np.imag(self.complex)
        self.mag =  np.abs(self.complex)
        self.phase = np.angle(self.complex)


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

        self.sinusoid_d = np.zeros(WINDOW_SIZE)
        self.sinusoid_d[1:] = self.sinusoid[:WINDOW_SIZE-1]

        self.sinusoid_w = self.window * self.sinusoid
        self.sinusoid_dw = self.window * self.sinusoid_d


        self.lo = Obj()
        self.lo.bins = np.arange(-FFT_N/2, FFT_N/2) / float(1)

        self.hi = Obj()
        self.hi.bins = np.arange(-(FFT_N*UPSAMPLE)/2, (FFT_N*UPSAMPLE)/2) / float(UPSAMPLE)

        self.lo.spectrum = SpectrumInfo(self.sinusoid_w, FFT_N)
        self.lo.spectrum_d = SpectrumInfo(self.sinusoid_dw, FFT_N)

        self.hi.spectrum = SpectrumInfo(self.sinusoid_w, FFT_N*UPSAMPLE)
        self.hi.spectrum_d = SpectrumInfo(self.sinusoid_dw, FFT_N*UPSAMPLE)



