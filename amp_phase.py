
import numpy as np

from constants import *


#These drag modes describe different options for adjusting the
# amplitude and phase
DM_NONE = 0
DM_FREE = 1
DM_AMP_ONLY = 2
DM_PHASE_ONLY = 3

class AmpPhaseSelectorView(object):

    def __init__(self, axes, params, fig):
        self.axes = axes
        self.params = params
        self.fig = fig
        self.callback = None
        self.dragging = DM_NONE

        self.axes.set_title("Sinusoid Amplitude/Phase")

        self.axes.set_xlim([-1.0, 1.0])
        self.axes.set_ylim([-1.0, 1.0])
        self.axes.set_xlabel('Real')
        self.axes.set_ylabel('Imag')
        self.axes.grid()
        self.axes.set_facecolor('lightgoldenrodyellow')


        self.scatter = self.axes.scatter([],[], c='green')
        self.curve, = self.axes.plot([], [], c='green')

        self.Update()

        cid = fig.canvas.mpl_connect('button_press_event', self.onbuttondown)
        cid = fig.canvas.mpl_connect('motion_notify_event', self.onmotion)
        cid = fig.canvas.mpl_connect('button_release_event', self.onbuttonup)

    def Update(self):

        cplx = self.params.complex()

        self.scatter.set_offsets([(cplx.real, cplx.imag)])
        self.curve.set_data([0, cplx.real], [0, cplx.imag])

    def onbuttondown(self, event):
        ax = event.inaxes

        if(ax != self.axes):
            return

        if(event.button != 1):
            return

        if(event.key == 'control'):
            self.dragging = DM_AMP_ONLY
        elif(event.key == 'shift'):
            self.dragging = DM_PHASE_ONLY
        else:
            self.dragging = DM_FREE

        self.onmotion(event)

    def onbuttonup(self, event):
        ax = event.inaxes

        if(ax != self.axes):
            return
        if(event.button != 1):
            return

        self.onmotion(event)
        self.dragging = DM_NONE

    def onmotion(self, event):
        ax = event.inaxes

        if(ax != self.axes):
            return
        if(self.dragging == DM_NONE):
            return

        x = event.xdata
        y = event.ydata

        cplx = x + 1j*y

        if(self.dragging in [DM_AMP_ONLY, DM_FREE]):
            self.params.amplitude = np.abs(cplx)
        if(self.dragging in [DM_PHASE_ONLY, DM_FREE]):
            self.params.phase = np.angle(cplx)

        self.Update()

        if(self.callback is not None):
            self.callback()