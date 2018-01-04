#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from mpl_toolkits.mplot3d import Axes3D

from constants import *

from time_domain import TimeDomainView
from amp_phase import AmpPhaseSelectorView

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


fig = plt.figure()

ax_ampphase = plt.axes([0.05, 0.15, 0.4, 0.8])
view_ampphase = AmpPhaseSelectorView(ax_ampphase, params, fig)


ax_freqslider = plt.axes([0.05, 0.02, 0.35, 0.07], facecolor='lightgoldenrodyellow')
sfreq = Slider(ax_freqslider, 'Freq', 0.1, FFT_N/2.0, valinit=params.frequency)


ax_timedomain = plt.axes([0.5, 0.05, 0.45, 0.9])
view_timedomain = TimeDomainView(ax_timedomain)


ax_freqdomain3d = plt.axes([0.05, 0.05, 0.4, 0.4], projection='3d')

# fig.canvas.draw_idle()




# ctrl_ax.subplots_adjust(left=0.25, bottom=0.25)


# # fig, ax = plt.subplots()
# plt.subplots_adjust(left=0.25, bottom=0.25)
# t = np.arange(0.0, 1.0, 0.001)
# a0 = 5
# f0 = 3
# s = a0*np.sin(2*np.pi*f0*t)
# l, = plt.plot(t, s, lw=2, color='red')
# plt.axis([0, 1, -10, 10])

# axcolor = 'lightgoldenrodyellow'
# axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
# axamp = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

# sfreq = Slider(axfreq, 'Freq', 0.1, 30.0, valinit=f0)
# samp = Slider(axamp, 'Amp', 0.1, 10.0, valinit=a0)


# def update(val):
#     amp = samp.val
#     freq = sfreq.val
#     l.set_ydata(amp*np.sin(2*np.pi*freq*t))
#     fig.canvas.draw_idle()
# sfreq.on_changed(update)
# samp.on_changed(update)

# resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
# button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


# def reset(event):
#     sfreq.reset()
#     samp.reset()
# button.on_clicked(reset)

# rax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)
# radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)


# def colorfunc(label):
#     l.set_color(label)
#     fig.canvas.draw_idle()
# radio.on_clicked(colorfunc)


def freqSliderUpdate(val):
    params.frequency = val
    UpdatePlots()

def UpdatePlots():
    view_timedomain.Update(params)
    fig.canvas.draw_idle()

sfreq.on_changed(freqSliderUpdate)
view_ampphase.callback = UpdatePlots

view_timedomain.Update(params)

plt.show()

