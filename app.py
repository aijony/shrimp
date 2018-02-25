from threading import Thread
import os
import datetime
import time

from bokeh.embed import server_document
from bokeh.server.server import Server

from reports import modifyDoc

from flask import render_template, Flask, request
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/reports')
def reports():
    script = server_document('http://localhost:5006/reports')
    return render_template("reports.html", script=script, template="Flask")


@app.route('/input')
def input():
    return render_template('input.html')


@app.route('/input', methods=['POST'])
def input_post():
    text = request.form['text']
    ts = time.time()
    if not os.path.exists('cache'):
        os.makedirs('cache')
    stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
    with open('cache/log.txt', 'a') as f:
        f.write(stamp + ' - ' + text + '\n')
    return render_template('input.html')


def bk_worker():
    server = Server({'/reports': modifyDoc},
                    allow_websocket_origin=["localhost:8000"])
    server.start()
    server.io_loop.start()


Thread(target=bk_worker).start()


if __name__ == '__main__':
    print('Flask on http://localhost:8000/')
    print()
    app.run(port=8000)
