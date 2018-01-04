
import numpy as np

from constants import *

class FreqDomain3DView(object):

    def __init__(self, axes):
        self.axes = axes

        self.axes.set_title("FFT (3D)")

        self.axes.set_xlim3d([-WINDOW_SIZE/2, WINDOW_SIZE/2])
        self.axes.set_ylim3d([-1.0, 1.0])
        self.axes.set_zlim3d([-1.0, 1.0])
        self.axes.set_xlabel('Frequency (bin)')
        self.axes.set_ylabel('Real')
        self.axes.set_zlabel('Imag')
        self.axes.grid()


        self.curve, = self.axes.plot([],[],[], label='Hi-res Transform', zorder = 5)
        self.scatter = self.axes.scatter(xs=[],ys=[],zs=[], color='red', zorder = 10)
        self.curve_reference = self.axes.plot([-FFT_N/2, FFT_N/2], [0,0], [0,0], 
            linestyle='dashed', color='black', label='Lo-res Transform', zorder = 1)

        self.axes.legend()


    def Update(self, windowed_signal):

        F_sig = np.fft.fft(windowed_signal, FFT_N) / (FFT_N)
        F_sig = np.fft.fftshift(F_sig)

        F_sig_hires = np.fft.fft(windowed_signal, FFT_N*UPSAMPLE) / (FFT_N*UPSAMPLE / 16)
        F_sig_hires = np.fft.fftshift(F_sig_hires)

        bins = np.arange(-WINDOW_SIZE/2, WINDOW_SIZE/2)
        real = np.real(F_sig)
        imag = np.imag(F_sig)

        bins_hires = np.arange(-WINDOW_SIZE*UPSAMPLE/2, WINDOW_SIZE*UPSAMPLE/2) / float(UPSAMPLE)
        real_hires = np.real(F_sig_hires)
        imag_hires = np.imag(F_sig_hires)


        self.curve.set_data(bins_hires, real_hires)
        self.curve.set_3d_properties(imag_hires)

        self.scatter.remove()
        self.scatter = self.axes.scatter(xs=[],ys=[],zs=[], color='red', zorder = 10)
        self.scatter.set_offsets(zip(*[bins, real]))
        self.scatter.set_3d_properties(imag,'z')
        self.scatter.set_color('red')

        return bins, real, imag
