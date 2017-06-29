import pandas as pd
from tornado.ioloop import IOLoop
import yaml
from jinja2 import Template

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme

import os

# if running locally, listen on port 5000
PORT = int(os.getenv('PORT', '5000'))

HOST = "0.0.0.0"

# this is set in the cloud foundry manifest 
try:
    ALLOW_WEBSOCKET_ORIGIN = os.getenv("ALLOW_WEBSOCKET_ORIGIN").split(',')
except:
    ALLOW_WEBSOCKET_ORIGIN = [ 'localhost:{0}'.format(PORT) ]

print('ALLOW_WEBSOCKET_ORIGIN', ALLOW_WEBSOCKET_ORIGIN)

io_loop = IOLoop.current()

def modify_doc(doc):
    data_url = "http://www.neracoos.org/erddap/tabledap/B01_sbe37_all.csvp?time,temperature&depth=1&temperature_qc=0&time>=2016-02-15&time<=2017-03-22"

    df = pd.read_csv(data_url, parse_dates=True, index_col=0)
    df = df.rename(columns={'temperature (celsius)': 'temperature'})
    df.index.name = 'time'

    source = ColumnDataSource(data=df)

    plot = figure(x_axis_type='datetime', 
                  y_range=(0, 25), 
                  y_axis_label='Temperature (Celsius)',
                  title="Sea Surface Temperature at 43.18, -70.43")
    plot.line('time', 'temperature', source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            data = df.rolling('{0}D'.format(new)).mean()
        source.data = ColumnDataSource(data=data).data

    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change('value', callback)

    doc.template = Template('''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Template Example</title>
        {{ bokeh_js }}
        {{ bokeh_css }}
    </head>
    <body>
        <h1>Plot with Template</h1>
    {{ plot_div }}
    {{ plot_script }}
    </body>
</html>''')

    doc.add_root( column(slider, plot) )

    doc.theme = Theme(json=yaml.load("""
        attrs:
            Figure:
                background_fill_color: "#DDDDDD"
                outline_line_color: white
                toolbar_location: above
                height: 500
                width: 800
            Grid:
                grid_line_dash: [6, 4]
                grid_line_color: white
    """))


bokeh_app = Application(FunctionHandler(modify_doc))

server = Server(
        {'/': bokeh_app}, 
        io_loop=io_loop,
        allow_websocket_origin=ALLOW_WEBSOCKET_ORIGIN,
        **{'port': PORT, 'address': HOST}
        )
server.start()

if __name__ == '__main__':
    io_loop.add_callback(server.show, "/")
    io_loop.start()
