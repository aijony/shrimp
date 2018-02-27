# Module: sensor.py
import random
import time
from log import log

from bokeh.plotting import figure

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Software SPI configuration:
# CLK = 18
# MISO = 23
# MOSI = 24
# CS = 25

#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0

# Allows program to run even when not interfacing with the RPI
mcpFlag = False
try:

    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    mcpFlag = True
except:
    print("mcp not configured correctly")


class Sensor:
    """ A sensor object handles the following tasks:
        - Reading the mcp sensor data
        - Logging the data
        - Plotting the data with Bokeh

    Args:
        name (str): What the sensor is reading
        unit (str): What the sensor's unit should be
        index (int): Index for corresponding MCP sensor
                     (set to -1 to spoof data)
        adjust (lambda): A function that adjusts the 0-1023 input value
                         to unit value.
        color (str): The color of the graph
        initialVal (float): What is the first data point (useful for spoofing)

    Example:
        Sensor("Oxygen", "mg/l", 1, lambda x: x * 12.5, "red")
        Sensor("Nitrogen", "mg/l", 2)

    Todo:
        Using inheritance to make Sensor, SensorLog, SensorBokeh.


    """
    def __init__(self, name, unit, index, adjust=lambda x: x,
                 color="green", initialVal=0):
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
        """Reads and logs the data from via the mcp library.
        It also has to option to spoof data for demo purposes.
        Set sensor index to -1 to do so"""
        if self.index < 0:
            self.datum = self.spoofData()
        else:
            self.datum = (mcp.read_adc(self.index))
        self.datum = self.adjust(self.datum)
        self.logData()
        return self.datum

    def updatePlot(self, step):
        """Updates the Bokeh plot"""
        self.ds.data['x'].append(step)
        self.ds.data['y'].append(self.getData())
        self.ds.trigger('data', self.ds.data, self.ds.data)

    def spoofData(self):
        """Creates random data for demoing purposes"""
        return self.datum + random.uniform(.1, -.1)

    def logData(self):
        """Logs the data every minute"""
        if time.time() - self.lastLog > 59:
            self.lastLog = time.time()
            log(str(self.datum), self.name + ".log")
