
import numpy as np

from constants import *

class FreqDomainMagView(object):

    def __init__(self, axes):
        self.axes = axes

        self.axes.set_title("FFT (Magnitude)")

        self.axes.set_xlim([-WINDOW_SIZE/2, WINDOW_SIZE/2])
        self.axes.set_ylim([0, 0.3])
        self.axes.set_xlabel('Frequency (bin)')
        self.axes.set_ylabel('Magnitude')
        self.axes.grid()


        self.curve, = self.axes.plot([],[], label='Hi-res Spectrum')
        self.scatter = self.axes.scatter([],[], s=5, color='red', label='Lo-res Spectrum',)

        self.axes.legend()


    def Update(self, data):

        self.curve.set_data(data.bins_hi, data.spectrum_mag_hi)

        self.scatter.set_offsets(zip(*[data.bins_lo, data.spectrum_mag_lo]))
