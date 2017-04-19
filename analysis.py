import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import plotly  # https://plot.ly/python/reference
import plotly.graph_objs as go


def get_sample():
    frame = np.genfromtxt("samples/raw_sample_63.csv", delimiter=",", defaultfmt="%i")
    return frame.astype(np.uint16)


def raw_image():
    frame = get_sample()
    dpi = 80.0
    xpixels, ypixels = 600, 800
    fig = plt.figure(figsize=(ypixels / dpi, xpixels / dpi), dpi=dpi)
    ax = fig.add_subplot(111)
    res = ax.imshow(frame, cmap=cm.jet, interpolation='nearest')
    cb = fig.colorbar(res)
    plt.show()


def normalized_image():
    frame = get_sample()
    cv2.normalize(frame, frame, 0, 65535, cv2.NORM_MINMAX)  # extend contrast
    np.right_shift(frame, 8, frame)  # fit data into 8 bits
    image_frame = np.uint8(frame)
    enlarged_image_frame = cv2.resize(image_frame, (0, 0), fx=30, fy=30, interpolation=cv2.INTER_NEAREST)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    res = ax.imshow(enlarged_image_frame, cmap=cm.jet, interpolation='nearest')
    cb = fig.colorbar(res)
    plt.show()


"""
https://plot.ly/python/matplotlib-colorscales/
"""


def matplotlib_to_plotly(cmap, pl_entries=255):
    h = 1.0 / (pl_entries - 1)
    pl_colorscale = []

    for k in range(pl_entries):
        C = map(np.uint8, np.array(cmap(k * h)[:3]) * 255)
        pl_colorscale.append([k * h, 'rgb' + str((C[0], C[1], C[2]))])

    return pl_colorscale


def plot_3d():
    color_map = cm.nipy_spectral  # cm.gist_rainbow #cm.gist_ncar # http://matplotlib.org/users/colormaps.html
    plotly_cmap = matplotlib_to_plotly(color_map)
    frame = get_sample()
    X, Y = np.arange(0, 80, 1), np.arange(0, 60, 1)
    X, Y = np.meshgrid(X, Y)
    Z = frame
    Z[:, -1] = Z[:, -2]  # Replace distroded last column with its predecessor
    # Z[Z>8310] = 8310 # Filter out higher intensity values
    # Z[Z < 8200] = 8200 # Filter out lower intensity values
    enable_contours = False
    dpi = 80.0
    xpixels, ypixels = 600, 800
    fig = plt.figure(figsize=(ypixels / dpi, xpixels / dpi), dpi=dpi)

    # Plot 2D image
    ax = fig.add_subplot(121)
    res = ax.imshow(frame, cmap=color_map, interpolation='nearest')  # color map type = coolwarm

    # Plot 3D image
    ax = fig.add_subplot(1, 2, 2, projection='3d')
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=color_map, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=10)

    from plotly.graph_objs import ColorBar, Contours
    data = [
        go.Surface(
            z=Z,
            colorbar=ColorBar(
                title='IR Intensity'
            ),
            colorscale=plotly_cmap,
            contours=Contours(
                z={
                    "show": enable_contours
                }
            )
        ),

    ]
    layout = go.Layout(
        title='3D IR Intensity Graph',
        autosize=False,
        width=1300,
        height=900,
        margin=dict(
            l=65,
            r=50,
            b=65,
            t=90
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='elevations-3d-surface.html')

    plt.show()


def main():
    # raw_image()
    # normalized_image()
    plot_3d()


if __name__ == '__main__':
    main()
