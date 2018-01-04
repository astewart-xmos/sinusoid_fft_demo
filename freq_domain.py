
import numpy as np

from constants import *

class FreqDomainMagView(object):

    def __init__(self, axes):
        self.axes = axes

        self.axes.set_title("FFT (Magnitude)")

        self.axes.set_xlim([-WINDOW_SIZE/2, WINDOW_SIZE/2])
        self.axes.set_ylim([-0.3, 0.3])
        self.axes.set_xlabel('Frequency (bin)')
        self.axes.set_ylabel('Magnitude')
        self.axes.grid()


        self.curve, = self.axes.plot([],[], label='Hi-res Spectrum')
        self.scatter = self.axes.scatter([],[], s=5, color='red', label='Lo-res Spectrum',)

        self.axes.legend()

        self.bins = np.arange(-WINDOW_SIZE/2, WINDOW_SIZE/2)
        self.bins_hires = np.arange(-WINDOW_SIZE*UPSAMPLE/2, WINDOW_SIZE*UPSAMPLE/2) / float(UPSAMPLE)


    def Update(self, F_sig_hires, F_sig):

        mag = np.abs(F_sig)
        phase = np.angle(F_sig)

        mag_hires = np.abs(F_sig_hires)
        phase_hires = np.angle(F_sig_hires)


        self.curve.set_data(self.bins_hires, mag_hires)

        self.scatter.set_offsets(zip(*[self.bins, mag]))
