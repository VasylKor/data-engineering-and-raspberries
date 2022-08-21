from distutils.log import debug
from pydoc import classname
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import mysql.connector as connection
import configparser
import os
import datetime
import numpy as np

# Setting folder as working directory
pathname = os.path.dirname(os.path.abspath(__file__))
os.chdir(pathname)

# Reading configuration
config = configparser.ConfigParser()
config.read("../config/py_config.txt")
db_param = config["mariadb"]

source_table = db_param["source_table"]
user=db_param["user"]
password=db_param["pwd"]
hostname=db_param["host"]
port=int(db_param["port"])
database=db_param["schema"]

try:
    mydb = connection.connect(host=hostname, database = database,user=user, passwd=password,use_pure=True)
    
    query = f"""select hostname, timestamp, cpu_percent, cpu_temp
                from {source_table} 
                where `timestamp` >= NOW() - INTERVAL 1 MONTH
            """
    data = pd.read_sql(query,mydb)
    
    
    mydb.close()
except Exception as e:
    mydb.close()
    print(str(e))



external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Monitor your Pi's"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Rpi S", className="header-title"
                ),
                html.P(
                    children="Monitor raspberries",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Host", className="menu-title"),
                        dcc.Dropdown(
                            id="host-filter",
                            options=[
                                {"label": host, "value": host}
                                for host in np.sort(data.hostname.unique())
                            ],
                            value="raspberryone",
                            clearable=True,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.timestamp.min(),
                            max_date_allowed=data.timestamp.max(),
                            start_date=data.timestamp.min(),
                            end_date=data.timestamp.max(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="cpu-temp-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="cpu-usage-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        dcc.Interval(
            id='interval-component',
            interval=30000, # in milliseconds
            n_intervals=0
        )
    ]
)


@app.callback(
    [Output("cpu-temp-chart", "figure"), Output("cpu-usage-chart", "figure")],
    [
        Input("host-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("interval-component","n_intervals")
    ],
)
def update_charts(host, start_date, end_date, n):

    mask = (
        (data.hostname == host)
        & (data.timestamp >= start_date)
        & (data.timestamp <= end_date)
    )

    filtered_data = data.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["timestamp"],
                "y": filtered_data["cpu_temp"],
                "type": "lines",
                "hovertemplate": "%{y:.2f}°C<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "CPU temperature",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"ticksuffix": "°C", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["timestamp"],
                "y": filtered_data["cpu_percent"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "CPU Usage", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug=False)