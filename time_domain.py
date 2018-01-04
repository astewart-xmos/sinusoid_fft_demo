
import numpy as np

from constants import *

class TimeDomainView(object):

    def __init__(self, axes):
        self.axes = axes

        self.axes.set_title("Time Domain")

        self.axes.set_xlim([0, WINDOW_SIZE])
        self.axes.set_ylim([-1.0, 1.0])
        self.axes.set_xlabel('Sample')
        self.axes.set_ylabel('Value')
        self.axes.grid()

        self.curve, = self.axes.plot([], label='Raw')
        self.curve_windowed, = self.axes.plot([], label='Windowed')

        self.axes.legend()

    def Update(self, data):
        self.curve.set_data(data.sample_indices, data.sinusoid)
        self.curve_windowed.set_data(data.sample_indices, data.sinusoid_w)
