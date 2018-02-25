# Module: sensor.py
import random
import time
from log import log

from bokeh.plotting import figure


class Sensor:
    def __init__(self, name, unit, calibrate=0, color="mediumspringgreen"):
        self.name = name
        self.unit = unit
        self.datum = calibrate
        self.plot = figure(plot_width=800, plot_height=400,
                           title=name)
        self.plot.x_range.follow = "end"
        self.plot.x_range.follow_interval = 100
        self.plot.x_range.range_padding = 0
        self.plot.yaxis.axis_label = unit
        self.plot.xaxis.axis_label = "steps"
        r = self.plot.line([], [], color=color, line_width=2)
        self.ds = r.data_source
        self.lastLog = time.time()

    def getData(self):
        self.datum = self.spoofData()
        self.logData()
        return self.datum

    def updatePlot(self, step):
        self.ds.data['x'].append(step)
        self.ds.data['y'].append(self.getData())
        self.ds.trigger('data', self.ds.data, self.ds.data)

    def spoofData(self):
        return self.datum + random.uniform(.1, -.1)

    def logData(self):
        if time.time() - self.lastLog > 59:
            log(self.datum, self.name + '.log')
