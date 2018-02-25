# Module: log.py
import os
import datetime
import time


def log(message, name):
    dr = 'cache'
    ts = time.time()
    if not os.path.exists(dr):
        os.makedirs(dr)
    stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
    with open(dir + '/' + name, 'a') as f:
        f.write(stamp + ' - ' + message + '\n')
