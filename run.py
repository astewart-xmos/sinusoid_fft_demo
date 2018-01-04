#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from mpl_toolkits.mplot3d import Axes3D

from constants import *

from time_domain import TimeDomainView
from amp_phase import AmpPhaseSelectorView
from freq_domain3d import FreqDomain3DView
from freq_domain import FreqDomainMagView

if __name__ != "__main__":
    # execute only if run as a script
    import sys
    sys.exit(0)


class Sinusoid(object):

    def __init__(self, freq = 1.0, amp = 1.0, phase = 0.0):

        self.frequency = freq
        self.amplitude = amp
        self.phase = phase


    def complex(self):
        return self.amplitude * np.exp(1j * self.phase)

    def time_domain(self):
        return self.amplitude * np.cos(2*np.pi * np.arange(0,1024) / float(WINDOW_SIZE) + self.phase)



params = Sinusoid()


fig_selection = plt.figure()
ax_ampphase = plt.axes([0.2, 0.2, 0.7, 0.7])
view_ampphase = AmpPhaseSelectorView(ax_ampphase, params, fig_selection)
ax_freqslider = plt.axes([0.15, 0.02, 0.75, 0.07], facecolor='lightgoldenrodyellow')
sfreq = Slider(ax_freqslider, 'Freq', 0.1, FFT_N/2.0, valinit=params.frequency)


fig_timedomain = plt.figure()
ax_timedomain = plt.axes()
view_timedomain = TimeDomainView(ax_timedomain)

fig_freqdomain3d = plt.figure()
ax_freqdomain3d = plt.subplot(111, projection='3d')
view_freqdomain3d = FreqDomain3DView(ax_freqdomain3d)


fig_freqdomain2d = plt.figure()
ax_freqdomain2d = plt.axes()
view_freqdomain2d = FreqDomainMagView(ax_freqdomain2d)



def freqSliderUpdate(val):
    params.frequency = val
    UpdatePlots()

def UpdatePlots():
    _, windowed = view_timedomain.Update(params)

    F_sig = np.fft.fft(windowed, FFT_N) / FFT_N
    F_sig = np.fft.fftshift(F_sig)

    F_sig_hires = np.fft.fft(windowed, FFT_N*UPSAMPLE) / FFT_N
    F_sig_hires = np.fft.fftshift(F_sig_hires)

    view_freqdomain3d.Update(F_sig_hires, F_sig)
    view_freqdomain2d.Update(F_sig_hires, F_sig)

    fig_selection.canvas.draw_idle()
    fig_timedomain.canvas.draw_idle()
    fig_freqdomain3d.canvas.draw_idle()
    fig_freqdomain2d.canvas.draw_idle()

sfreq.on_changed(freqSliderUpdate)
view_ampphase.callback = UpdatePlots

UpdatePlots()

plt.show()

