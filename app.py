from threading import Thread
from bokeh.embed import server_document
from bokeh.server.server import Server

from reports import modifyDoc
from log import log

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
    log(text, 'messages.log')
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
