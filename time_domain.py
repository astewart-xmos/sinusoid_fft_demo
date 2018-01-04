
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

        self.window = np.hanning(WINDOW_SIZE+1)[:WINDOW_SIZE]

    def Update(self, params):

        t = np.arange(0, WINDOW_SIZE)
        s = params.amplitude * np.cos(2*np.pi * params.frequency * t / float(WINDOW_SIZE) + params.phase)

        s_windowed = s * self.window

        self.curve.set_data(t, s)
        self.curve_windowed.set_data(t, s_windowed)

        return s, s_windowed
