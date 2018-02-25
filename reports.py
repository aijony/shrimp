# Module: reports.py
from bokeh.driving import linear
from bokeh.layouts import column

import sensor as s

oxygen = 6.34


def modifyDoc(doc):
    sensorArray = []
    sensorArray.append(s.Sensor("Oxygen", "mg/l", -1, lambda x: x, "red", 6.67))
    sensorArray.append(s.Sensor("Oxygen", "mg/l", -1, lambda x: x + 10, "red", 6.67))

    @linear()
    def update(step):
        for sensor in sensorArray:
            sensor.updatePlot(step)

    for sensor in sensorArray:
        doc.add_root(column(sensor.plot))

    doc.add_periodic_callback(update, 100)
