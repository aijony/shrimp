# Module: reports.py
from bokeh.plotting import figure
from bokeh.driving import linear
from bokeh.layouts import column
import random

import sensor as s

oxygen = 6.34


def modifyDoc(doc):
    plot = figure(plot_width=800, plot_height=400)
    plot.x_range.follow = "end"
    plot.x_range.follow_interval = 100
    plot.x_range.range_padding = 0

    r1 = plot.line([], [], color="firebrick", line_width=2)
    r2 = plot.line([], [], color="navy", line_width=2)

    ds1 = r1.data_source
    ds2 = r2.data_source

    sensorArray = []
    sensorArray.append(s.Sensor("Oxygen", "mg/l", 6.34, "red"))

    @linear()
    def update(step):
        ds1.data['x'].append(step)
        ds1.data['y'].append(random.randint(0, 100))
        ds2.data['x'].append(step)
        ds2.data['y'].append(random.randint(0, 100))
        ds1.trigger('data', ds1.data, ds1.data)
        ds2.trigger('data', ds2.data, ds2.data)
        sensorArray[0].updatePlot(step)

    doc.add_root(column(plot, sensorArray[0].plot))

    doc.add_periodic_callback(update, 100)


