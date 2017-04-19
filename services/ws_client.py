from Tkinter import TclError

import tornado
from tornado import gen
from tornado.websocket import websocket_connect
import numpy as np
import json

import matplotlib.pyplot as plt
from matplotlib import cm
import plotly  # https://plot.ly/python/reference
import plotly.graph_objs as go

dpi = 80.0
xpixels, ypixels = 600, 800
fig = plt.figure(figsize=(ypixels / dpi, xpixels / dpi), dpi=dpi)

# Plot 2D image
ax = fig.add_subplot(111)


def plot_3d(frame):
    color_map = cm.nipy_spectral  # cm.gist_rainbow #cm.gist_ncar # http://matplotlib.org/users/colormaps.html
    X, Y = np.arange(0, 80, 1), np.arange(0, 60, 1)
    X, Y = np.meshgrid(X, Y)
    Z = frame
    Z[:, -1] = Z[:, -2]  # Replace distroded last column with its predecessor
    # Z[Z>8310] = 8310 # Filter out higher intensity values
    # Z[Z < 8200] = 8200 # Filter out lower intensity values
    ax.imshow(frame, cmap=color_map, interpolation='nearest')  # color map type = coolwarm
    try:
        plt.pause(0.05)
    except TclError as e:
        print(e)


@gen.coroutine
def handle_ws():
    url = "ws://jetson.local.knnect.com:8080/ws" #"ws://localhost:8080/ws"  #
    conn = yield websocket_connect(url)
    while True:
        msg = yield conn.read_message()
        if msg is None: break
        conn.write_message("ACK")
        # print("Got the message {}".format(msg))
        if msg == u"ACK": continue
        json_frame = json.loads(msg)
        frame = np.array(json_frame).reshape((60, 80))
        plot_3d(frame)
        yield gen.sleep(0.1)


def main():
    # connection = handle_ws()
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.add_callback(handle_ws)
    ioloop.start()


if __name__ == '__main__':
    main()
