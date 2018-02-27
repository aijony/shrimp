from threading import Thread

from bokeh.embed import server_document
from flask import render_template, Flask, request

from reports import sensorInit, sensorLoop, bokehLoop
from log import log

app = Flask(__name__)

# Do no modify
sensorArray = []


@app.route('/')
def index():
    """Home page"""
    return render_template('home.html')


@app.route('/reports')
def reports():
    """Report page / Bokeh Page"""
    script = server_document('http://localhost:5006/reports')
    return render_template("reports.html", script=script, template="Flask")


@app.route('/input')
def input():
    """Page with input"""
    return render_template('input.html')


@app.route('/input', methods=['POST'])
def input_post():
    """Process input from input page"""
    text = request.form['text']
    log(text, 'messages.log')
    return render_template('input.html')


if __name__ == '__main__':
    print('Flask on http://localhost:8000/')
    print()

    # Create background sensor readings for logging
    sensorInit(sensorArray)
    Thread(target=sensorLoop, args=(sensorArray,)).start()

    # Create foreground sensor readings for web server
    Thread(target=bokehLoop).start()
    app.run(port=8000)
