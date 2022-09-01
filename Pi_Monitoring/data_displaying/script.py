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
    
    query = f"""select 
                    *
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
                            min_date_allowed=datetime.date(2017, 6, 21),
                            max_date_allowed=datetime.date(2050, 12, 31), # must be parametrized
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
                html.Div(
                    children=dcc.Graph(
                        id="ram-usage-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="ram-used-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="ram-free-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="ram-swap-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="disk-usage-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="disk-used-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="disk-free-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="net-sent-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="net-received-chart", config={"displayModeBar": False},
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
    [
        Output("cpu-temp-chart", "figure"), 
        Output("cpu-usage-chart", "figure"),
        Output("ram-usage-chart", "figure"),
        Output("ram-used-chart","figure"),
        Output("ram-free-chart","figure"),
        Output("ram-swap-chart","figure"),
        Output("disk-usage-chart", "figure"),
        Output("disk-used-chart","figure"),
        Output("disk-free-chart","figure"),
        Output("net-sent-chart","figure"),
        Output("net-received-chart","figure"),
    ],
    [
        Input("host-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("interval-component","n_intervals")
    ],
)
def update_charts(host, start_date, end_date, n):

    try:
        mydb = connection.connect(host=hostname, database = database,user=user, passwd=password,use_pure=True)
        
        query = f"""select 
                        *
                    from {source_table} 
                    where `timestamp` >= NOW() - INTERVAL 1 MONTH
                """
        data = pd.read_sql(query,mydb)
        
        
        mydb.close()
    except Exception as e:
        mydb.close()
        print(str(e))

    mask = (
        (data.hostname == host)
        & (data.timestamp >= start_date)
        & (data.timestamp <= end_date)
    )

    filtered_data = data.loc[mask, :]

    cpu_temp_chart_figure = {
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
                "text": "CPU Temperature",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"ticksuffix": "°C", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    cpu_usage_chart_figure = {
        "data": [
            {
                "x": filtered_data["timestamp"],
                "y": filtered_data["cpu_percent"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "CPU Usage Percent", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"ticksuffix": "%","fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    ram_usage_chart_figure = {
        "data": [
            {
                "x": filtered_data["timestamp"],
                "y": filtered_data["ram_percent"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "RAM Usage Percent", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"ticksuffix": "%","fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    ram_used_chart_figure = {
        "data": [
            {
                "x": filtered_data["timestamp"],
                "y": filtered_data["ram_used"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Used RAM Bytes", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"ticksuffix": "B","fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    ram_free_chart_figure = {
        "data": [
            {
                "x": filtered_data["timestamp"],
                "y": filtered_data["ram_available"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Free RAM Bytes", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"ticksuffix": "B","fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    ram_swap_chart_figure = {
        "data": [
            {
                "x": filtered_data["timestamp"],
                "y": filtered_data["ram_swap_percent"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Swapped RAM Percent", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"ticksuffix": "%","fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    disk_usage_chart_figure = {
        "data": [
            {
                "x": filtered_data["timestamp"],
                "y": filtered_data["disk_percent"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Disk Usage Percent", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"ticksuffix": "%","fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    disk_used_chart_figure = {
        "data": [
            {
                "x": filtered_data["timestamp"],
                "y": filtered_data["disk_used"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Used Disk Bytes", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"ticksuffix": "B","fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    disk_free_chart_figure = {
        "data": [
            {
                "x": filtered_data["timestamp"],
                "y": filtered_data["disk_free"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Free Disk Bytes", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"ticksuffix": "B","fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    net_sent_chart_figure = {
        "data": [
            {
                "x": filtered_data["timestamp"],
                "y": filtered_data["net_sent"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Sent Bytes", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"ticksuffix": "B","fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    net_received_chart_figure = {
        "data": [
            {
                "x": filtered_data["timestamp"],
                "y": filtered_data["net_received"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Received Bytes", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"ticksuffix": "B","fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    return cpu_temp_chart_figure, cpu_usage_chart_figure, ram_usage_chart_figure, \
            ram_used_chart_figure, ram_free_chart_figure, ram_swap_chart_figure, \
            disk_usage_chart_figure, disk_used_chart_figure, disk_free_chart_figure, \
            net_sent_chart_figure, net_received_chart_figure


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug=False)