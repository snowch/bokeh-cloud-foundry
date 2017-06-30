import pandas as pd
from tornado.ioloop import IOLoop
import yaml
from jinja2 import Template

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, Div
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme
from bokeh.client import push_session

import os

# if running locally, listen on port 5000
PORT = int(os.getenv('PORT', '5000'))
HOST = "0.0.0.0"

try:
    # This is set in the cloud foundry manifest. If we are running on 
    # cloud foundry, this will be set for us.
    ALLOW_WEBSOCKET_ORIGIN = os.getenv("ALLOW_WEBSOCKET_ORIGIN").split(',')
except:
    # We are not running on cloud foundry so we must be running locally
    ALLOW_WEBSOCKET_ORIGIN = [ 'localhost:{0}'.format(PORT) ]


io_loop = IOLoop.current()

# This example simulates reading from a stream such as kafka

def modify_doc(doc):
    
    df_all = pd.read_csv('data.csv')
    df_all['Date'] = pd.to_datetime(df_all['Date'])

    start_data_df = df_all[0:350]
    
    start_data_df.loc[ :, 'color' ] = 'green'

    source = ColumnDataSource(data=start_data_df.to_dict(orient='list'))

    plot = figure(x_axis_type='datetime', 
                  y_range=(0, 10000000), 
                  y_axis_label='Y Label',
                  title="Title")

    plot.line('Date', 'ALL_EXCL_FUEL',   color='blue',      alpha=1, source=source)
    plot.line('Date', 'MOSTLY_FOOD',     color='lightblue', alpha=1, source=source)
    plot.line('Date', 'NON_SPECIALISED', color='grey',      alpha=1, source=source)

    plot.circle('Date', 'ALL_EXCL_FUEL', color='color', fill_alpha=0.2, size=4, source=source)

    def callback():
        # FIXME: how can we save this in the user's session?
        global curr_rec
        try:
            curr_rec
        except NameError:
            curr_rec = 350

        df = df_all[curr_rec:curr_rec+1]

        if df.shape[0] > 0:
            df.loc[ :, 'color' ] = 'blue'
            new_data = df.to_dict(orient='list')

            print(new_data)
            source.stream( new_data )
            curr_rec = curr_rec + 1

    doc.add_root(plot)
    doc.add_periodic_callback(callback, 250)


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
