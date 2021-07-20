




# Import Librairies
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table

import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px


# Load datasets
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df2 = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})
fig2 = px.bar(df2, x="Fruit", y="Amount", color="City", barmode="group")


def create_dash_app(flask_app):

    dash_app = dash.Dash(
        server=flask_app, name="dash_test",
        url_base_pathname="/dash/",
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )


    # url, root-url and first-loading are used for routing
    url_bar_and_content_div = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='root-url', style={'display': 'none'}),
        html.Div(id='first-loading', style={'display': 'none'}),
        html.Div(id='page-content')
    ])

    layout_index = html.Div([
        dbc.Nav(
            [
                dbc.NavLink("Item App", href="home", active="exact"),
                dbc.NavLink("Data", href="page-1", active="exact"),
                dbc.NavLink("Stock", href="page-2", active="exact"),
            ], 
            className="navbar navbar-expand-md navbar-dark bg-dark",
            style={
                "font-weight": "bold"
            }
        ),
        html.Br(),
        html.Div([
            html.Div([
                html.Div([
                    html.H5("Card 1 Title"),
                ], className="card-body"),
                html.Div([
                    html.P("This is a paragraph to describe the app"),
                    html.Button("Info", className="btn btn-outline btn-info")
                ], className="card-text")
            ], className="card text-center", style={"margin-bottom": "10px"}),
            html.Div([
                html.Div([
                    html.H5("Card 2 Title"),
                ], className="card-body"),
                html.Div([
                    html.P("This is another paragraph to describe the app"),
                    html.Button("Info", className="btn btn-outline btn-info")
                ], className="card-text")
            ], className="card text-center", style={"margin-bottom": "10px"}),
            html.P("This is where I need help. I would like to have a link \
                 or a button here that brings me back into the home page of the Flask app. \
                Thank you if you decided to help me. This is my first app shared onto GitHub."),
        ], # className="col-md-8",
            style={"margin-bottom": "5px"}
        ),
    ])

    layout_page_1 = html.Div([
        dbc.Nav(
            [
                dbc.NavLink("waterSaved", href="home", active="exact"),
                dbc.NavLink("Données et Paramètres", href="page-1", active="exact"),
                dbc.NavLink("Anomalies Détectées", href="page-2", active="exact"),
            ], 
            className="navbar navbar-expand-md navbar-dark bg-dark",
            style={
                "font-weight": "bold"
            }
        ),
        html.Br(),
        html.H1(
            "Page 1 - Dash App",
            style={
                "text-align": "center", 'color': "#002E5D",
                "font-family": "Montserrat", "font-weight": "bold"
            }
        ),
        html.Div([
            dcc.Graph(id='graph-with-slider'),
            dcc.Slider(
                id='year-slider',
                min=df['year'].min(),
                max=df['year'].max(),
                value=df['year'].min(),
                marks={str(year): str(year) for year in df['year'].unique()},
                step=None
            )
        ])
    ], style={"padding": "0px 60px 0px 60px"})

    layout_page_2 = html.Div([
        dbc.Nav(
            [
                dbc.NavLink("waterSaved", href="home", active="exact"),
                dbc.NavLink("Données et Paramètres", href="page-1", active="exact"), 
                dbc.NavLink("Anomalies Détectées", href="page-2", active="exact"),
            ], 
            className="navbar navbar-expand-md navbar-dark bg-dark",
            style={
                "font-weight": "bold"
            }
        ),
        html.Br(),
        html.H1(
            "Page 2 Dash App", 
            style={
                "text-align": "center", 'color': "#002E5D",
                "font-family": "Montserrat", "font-weight": "bold"
            }
        ),  
        dcc.Graph(
            id='example-graph',
            figure=fig2
        )
    ], style={"padding": "0px 60px 0px 60px"})


    # index layout
    dash_app.layout = url_bar_and_content_div

    # "complete" layout, need at least Dash 1.12
    dash_app.validation_layout = html.Div([
        url_bar_and_content_div,
        layout_index,
        layout_page_1,
        layout_page_2,
    ])


    # The following callback is used to dynamically instantiate the root-url
    @dash_app.callback([dash.dependencies.Output('root-url', 'children'), dash.dependencies.Output('first-loading', 'children')],
                dash.dependencies.Input('url', 'pathname'),
                dash.dependencies.State('first-loading', 'children')
                )
    def update_root_url(pathname, first_loading):
        if first_loading is None:
            return pathname, True
        else:
            raise PreventUpdate

    # This is the callback doing the routing
    @dash_app.callback(dash.dependencies.Output('page-content', 'children'),
                [
                    dash.dependencies.Input('root-url', 'children'),
                    dash.dependencies.Input('url', 'pathname')
                ])
    def display_page(root_url, pathname):
        if root_url + "page-1" == pathname :
            return layout_page_1
        elif root_url + "page-2" == pathname :
            return layout_page_2
        else:
            return layout_index


    # Page 1 callbacks
    # Connect the Plotly graphs with Dash Components
    # Do not use [] around output if you only have one
    @dash_app.callback(
        Output('graph-with-slider', 'figure'),
        Input('year-slider', 'value'))
    def update_figure(selected_year):
        filtered_df = df[df.year == selected_year]

        fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                        size="pop", color="continent", hover_name="country",
                        log_x=True, size_max=55)

        fig.update_layout(transition_duration=500)

        return fig

    # This loop make it able for us to make the dash page secure with the Flask Login
    for view_function in dash_app.server.view_functions:
        if view_function.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_function] = login_required(
                dash_app.server.view_functions[view_function]
            )

    return dash_app