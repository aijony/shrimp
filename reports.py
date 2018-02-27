# Module: reports.py
from bokeh.driving import linear
from bokeh.layouts import column
from bokeh.server.server import Server

import sensor as s


def sensorInit(sensorArray):
    sensorArray.append(s.Sensor("Oxygen", "mg/l", -1,
                                lambda x: x, "red", 6.67))
    sensorArray.append(s.Sensor("Nitrogen", "mg/l", -1,
                                lambda x: x, "blue", 29.67))


def sensorLoop(sensorArray):
    for sensor in sensorArray:
        sensor.getData()


def modifyDoc(doc):
    sensorArray = []
    sensorInit(sensorArray)

    @linear()
    def update(step):
        sensorLoop(sensorArray)
        for sensor in sensorArray:
            sensor.updatePlot(step)

    for sensor in sensorArray:
        doc.add_root(column(sensor.plot))

    doc.add_periodic_callback(update, 500)


def bokehLoop():
    server = Server({'/reports': modifyDoc},
                    allow_websocket_origin=["localhost:8000"])
    server.start()
    server.io_loop.start()
