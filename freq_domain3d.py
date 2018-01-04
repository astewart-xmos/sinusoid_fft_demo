
import numpy as np

from constants import *

class FreqDomain3DView(object):

    def __init__(self, axes):
        self.axes = axes

        self.axes.set_title("FFT (3D)")

        self.axes.set_xlim3d([-WINDOW_SIZE/2, WINDOW_SIZE/2])
        self.axes.set_ylim3d([-0.3, 0.3])
        self.axes.set_zlim3d([-0.3, 0.3])
        self.axes.set_xlabel('Frequency (bin)')
        self.axes.set_ylabel('Real')
        self.axes.set_zlabel('Imag')
        self.axes.grid()


        self.curve, = self.axes.plot([],[],[], label='Hi-res Transform')
        self.scatter = self.axes.scatter(xs=[],ys=[],zs=[], s=5, color='red', label='Lo-res Transform',)
        self.curve_reference = self.axes.plot([-FFT_N/2, FFT_N/2], [0,0], [0,0], 
            linestyle='dashed', color='black')

        self.axes.legend()


    def Update(self, data):

        self.curve.set_data(data.hi.bins, data.hi.spectrum.real)
        self.curve.set_3d_properties(data.hi.spectrum.imag)

        self.scatter.remove()
        self.scatter = self.axes.scatter(xs=[],ys=[],zs=[], color='red', label='Lo-res Transform')
        self.scatter.set_offsets(zip(*[data.lo.bins, data.lo.spectrum.real]))
        self.scatter.set_3d_properties(data.lo.spectrum.imag,'z')
