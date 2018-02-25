# Module: sensor.py
import random

from bokeh.plotting import figure


class Sensor:
    def __init__(self, name, unit, calibrate=0, color="mediumspringgreen"):
        self.name = name
        self.unit = unit
        self.calibrate = calibrate
        self.plot = figure(plot_width=800, plot_height=400,
                           title=name)
        self.plot.x_range.follow = "end"
        self.plot.x_range.follow_interval = 100
        self.plot.x_range.range_padding = 0
        self.plot.yaxis.axis_label = unit
        self.plot.xaxis.axis_label = "steps"
        r = self.plot.line([], [], color=color, line_width=2)
        self.ds = r.data_source

    def getData(self):
        self.calibrate = self.spoofData()
        return self.calibrate

    def updatePlot(self, step):
        self.ds.data['x'].append(step)
        self.ds.data['y'].append(self.getData())
        self.ds.trigger('data', self.ds.data, self.ds.data)

    def spoofData(self):
        return self.calibrate + random.uniform(.1, -.1)

#  LocalWords:  mediumspringgreen
