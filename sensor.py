# Module: sensor.py
import random
import time
from log import log

from bokeh.plotting import figure

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Software SPI configuration:
CLK = 18
MISO = 23
MOSI = 24
CS = 25
mcpFlag = False

try:
    mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
    mcpFlag = True
except:
    print("mcp not configured correctly")

# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


class Sensor:
    def __init__(self, name, unit, index, adjust=lambda x: x,
               color="mediumseagreen", initialVal=0):
        self.name = name
        self.unit = unit
        self.index = index
        self.datum = initialVal
        self.lastLog = time.time() - 60
        self.adjust = adjust

        # Plot Config
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
        if self.index < 0:
            self.datum = self.spoofData()
        else:
            self.datum = (mcp.read_adc(self.index))
        self.datum = self.adjust(self.datum)
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
            self.lastLog = time.time()
            log(str(self.datum), self.name + ".log")
