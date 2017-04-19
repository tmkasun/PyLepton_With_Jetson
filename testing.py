# from __future__ import print_function
#
# import numpy as np
# import pandas as pd
#
# from bokeh.util.browser import view
# from bokeh.document import Document
# from bokeh.embed import file_html
# from bokeh.layouts import gridplot
# from bokeh.models.glyphs import Circle, Line
# from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Range1d
# from bokeh.resources import INLINE
#
# raw_columns=[
#     [10.0,   8.04,   10.0,   9.14,   10.0,   7.46,   8.0,    6.58],
#     [8.0,    6.95,   8.0,    8.14,   8.0,    6.77,   8.0,    5.76],
#     [13.0,   7.58,   13.0,   8.74,   13.0,   12.74,  8.0,    7.71],
#     [9.0,    8.81,   9.0,    8.77,   9.0,    7.11,   8.0,    8.84],
#     [11.0,   8.33,   11.0,   9.26,   11.0,   7.81,   8.0,    8.47],
#     [14.0,   9.96,   14.0,   8.10,   14.0,   8.84,   8.0,    7.04],
#     [6.0,    7.24,   6.0,    6.13,   6.0,    6.08,   8.0,    5.25],
#     [4.0,    4.26,   4.0,    3.10,   4.0,    5.39,   19.0,   12.5],
#     [12.0,   10.84,  12.0,   9.13,   12.0,   8.15,   8.0,    5.56],
#     [7.0,    4.82,   7.0,    7.26,   7.0,    6.42,   8.0,    7.91],
#     [5.0,    5.68,   5.0,    4.74,   5.0,    5.73,   8.0,    6.89]]
#
# quartet = pd.DataFrame(data=raw_columns, columns=
# ['Ix','Iy','IIx','IIy','IIIx','IIIy','IVx','IVy'])
#
#
# circles_source = ColumnDataSource(
#     data = dict(
#         xi   = quartet['Ix'],
#         yi   = quartet['Iy'],
#         xii  = quartet['IIx'],
#         yii  = quartet['IIy'],
#         xiii = quartet['IIIx'],
#         yiii = quartet['IIIy'],
#         xiv  = quartet['IVx'],
#         yiv  = quartet['IVy'],
#     )
# )
#
# x = np.linspace(-0.5, 20.5, 10)
# y = 3 + 0.5 * x
# lines_source = ColumnDataSource(data=dict(x=x, y=y))
#
# xdr = Range1d(start=-0.5, end=20.5)
# ydr = Range1d(start=-0.5, end=20.5)
#
# def make_plot(title, xname, yname):
#     plot = Plot(x_range=xdr, y_range=ydr, plot_width=400, plot_height=400,
#                 border_fill_color='white', background_fill_color='#e9e0db')
#     plot.title.text = title
#
#     xaxis = LinearAxis(axis_line_color=None)
#     plot.add_layout(xaxis, 'below')
#
#     yaxis = LinearAxis(axis_line_color=None)
#     plot.add_layout(yaxis, 'left')
#
#     plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
#     plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
#
#     line = Line(x='x', y='y', line_color="#666699", line_width=2)
#     plot.add_glyph(lines_source, line)
#
#     circle = Circle(
#         x=xname, y=yname, size=12,
#         fill_color="#cc6633", line_color="#cc6633", fill_alpha=0.5
#     )
#     plot.add_glyph(circles_source, circle)
#
#     return plot
#
# #where will this comment show up
# I   = make_plot('I',   'xi',   'yi')
# II  = make_plot('II',  'xii',  'yii')
# III = make_plot('III', 'xiii', 'yiii')
# IV  = make_plot('IV',  'xiv',  'yiv')
#
# grid = gridplot([[I, II], [III, IV]], toolbar_location=None)
#
# doc = Document()
# doc.add_root(grid)
#
# if __name__ == "__main__":
#     doc.validate()
#     filename = "anscombe.html"
#     with open(filename, "w") as f:
#         f.write(file_html(doc, INLINE, "Anscombe's Quartet"))
#     print("Wrote %s" % filename)
#     view(filename)


# import plotly
# print plotly.__version__  # version >1.9.4 required
# from plotly.graph_objs import Scatter, Layout
# plotly.offline.plot({
#     "data": [
#         Scatter(x=[1, 2, 3, 4], y=[4, 1, 3, 7])
#     ],
#     "layout": Layout(
#         title="hello world"
#     )
# })



import plotly
import plotly.graph_objs as go
import numpy as np

import pandas as pd

# Read data from a csv
z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')

data = [
    go.Surface(
        z=np.genfromtxt("samples/raw_sample_8.csv", delimiter=",", defaultfmt="%i")
    )
]
layout = go.Layout(
    title='Mt Bruno Elevation',
    autosize=False,
    width=1300,
    height=900,
    margin=dict(
        l=65,
        r=50,
        b=65,
        t=90
    )
)
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='elevations-3d-surface.html')