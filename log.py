# Module: log.py
import os
import datetime
import time


def log(message, name):
    """Currently just logs the messages and text
       with a date file in text format."""
    dr = 'cache'
    ts = time.time()
    if not os.path.exists(dr):
        os.makedirs(dr)
    stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
    with open(dr + '/' + name, 'a') as f:
        f.write(stamp + ' - ' + message + '\n')
