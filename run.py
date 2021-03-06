#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

from constants import *

from sin_data import SinData

from time_domain import TimeDomainView
from amp_phase import AmpPhaseSelectorView
from freq_domain3d import FreqDomain3DView
from freq_domain import FreqDomainMagView

import argparse

if __name__ != "__main__":
    # execute only if run as a script
    import sys
    sys.exit(0)

parser = argparse.ArgumentParser()

parser.add_argument('-f','--freq', nargs='+', 
                            help='Supply frequencies which will be cycled via the arrow keys.', required=False)

parser.add_argument('-q','--no-time', action='store_true', 
                            help="Don't open a time-domain view of the sinusoid.")
parser.add_argument('-w','--no-mag', action='store_true', 
                            help="Don't open a frequency-domain magnitude view of the sinusoid.")
parser.add_argument('-e','--no-complex', action='store_true', 
                            help="Don't open a complex frequency-domain view of the sinusoid.")


args = parser.parse_args()

if(args.freq is not None):
    args.freq = [float(x) for x in args.freq]

class Sinusoid(object):

    def __init__(self, freq = 1.0, amp = 1.0, phase = 0.0):

        self.frequency = freq
        self.amplitude = amp
        self.phase = phase


    def complex(self):
        return self.amplitude * np.exp(1j * self.phase)

    def time_domain(self):
        return self.amplitude * np.cos(2*np.pi * np.arange(0,1024) / float(WINDOW_SIZE) + self.phase)

scratch = []

def LayoutMultiWindow(args, UpdatePlots):
    global scratch

    figures = []
    axes = []
    update_views = []

    figures.append(plt.figure())
    figures[-1].canvas.set_window_title("Freq/Amp/Phase Controls")
    ax_ampphase = plt.axes([0.2, 0.2, 0.7, 0.7])
    view_ampphase = AmpPhaseSelectorView(ax_ampphase, params, figures[-1])

    ax_freqslider = plt.axes([0.15, 0.02, 0.75, 0.07], facecolor='lightgoldenrodyellow')


    sfreq = Slider(ax_freqslider, 'Freq', 0.1, FFT_N/2.0, valinit=params.frequency)


    if(not args.no_time):
        figures.append(plt.figure())
        figures[-1].canvas.set_window_title("Time Domain")
        axes.append(plt.axes())
        update_views.append(TimeDomainView(axes[-1]))

    if(not args.no_complex):
        figures.append(plt.figure())
        figures[-1].canvas.set_window_title("Frequency Domain (Complex)")
        axes.append(plt.subplot(111, projection='3d'))
        update_views.append(FreqDomain3DView(axes[-1]))

    if(not args.no_mag):
        figures.append(plt.figure())
        figures[-1].canvas.set_window_title("Frequency Domain (Magnitude)")
        axes.append(plt.axes())
        update_views.append(FreqDomainMagView(axes[-1]))


    sfreq.on_changed(freqSliderUpdate)
    figures[0].canvas.mpl_connect('key_press_event', KeyPress)

    view_ampphase.callback = UpdatePlots

    scratch.append(ax_freqslider)
    scratch.append(ax_ampphase)
    scratch.append(view_ampphase)
    return figures, axes, update_views, sfreq

params = Sinusoid()
if(args.freq is not None):
    params.frequency = args.freq[0]
    params.last_freq_index = 0




def freqSliderUpdate(val):
    params.frequency = val
    UpdatePlots()

def KeyPress(event):
    
    #LEFT and RIGHT rotate through the frequencies that
    #   were passed in to the script as an argument
    if(event.key == 'left'):
        if(args.freq == None): return
        params.last_freq_index -= 1
        if(params.last_freq_index < 0):
            params.last_freq_index = len(args.freq)-1

        sfreq.set_val(args.freq[params.last_freq_index])
        UpdatePlots()
    elif(event.key == 'right'):
        if(args.freq == None): return
        params.last_freq_index += 1
        if(params.last_freq_index >= len(args.freq)):
            params.last_freq_index = 0

        sfreq.set_val(args.freq[params.last_freq_index])
        UpdatePlots()


def UpdatePlots():
    data = SinData(params)

    for view in update_views:
        view.Update(data)

    for fig in figures:
        fig.canvas.draw_idle()

figures, axes, update_views, sfreq = LayoutMultiWindow(args, UpdatePlots)


UpdatePlots()

plt.show()

