import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from dash import Input, Output, dcc, html
from sklearn import datasets
from sklearn.cluster import KMeans
import time
import threading


# Custom imports
import repository as repo
import page

scope = {
    "Wavenumber": 1450,
    "Frames": 5000,
    "Nanoseconds": 500,
    "SquareSize": 256,
    "Hyperspectral": False,
    "Step": 4,
    "MinWavenumber": 1042,
    "MaxWavenumber": 1840,
    "BarProgress": 0,
    "InitialImageLoading": False,
    "InitialImageData": None,
    "HyperspectralLoading": False,
    "HyperspectralData": None,
}


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = page.page


# Press "Aquire Initial Image" button to start the thread
@app.callback(
    Output("showGraphbtn", "disabled", allow_duplicate=True),
    Output("startHyperBtn", "disabled", allow_duplicate=True),
    Output("stopHyperBtn", "disabled", allow_duplicate=True),
    Output("interval-initial", "disabled", allow_duplicate=True),
    [Input("showGraphbtn", "n_clicks")],
    prevent_initial_call=True,
)
def loadInitialGraph(n):
    scope["InitialImageLoading"] = True

    thread = threading.Thread(
        target=repo.getInitialImage, args=(scope,)).start()

    return True, True, True, False


# Check for the progress of the initial image loading
@app.callback(
    Output('plot-initial', 'figure'),
    Output('interval-initial', 'disabled'),
    Output("showGraphbtn", "disabled", allow_duplicate=True),
    Output("stopHyperBtn", "disabled", allow_duplicate=True),
    Output("startHyperBtn", "disabled", allow_duplicate=True),
    Input('interval-initial', 'n_intervals'),
    prevent_initial_call=True
)
def checkInitialImageProgress(n):
    if scope["InitialImageLoading"] == False:
        fig = repo.generateFigureForPlot(scope["InitialImageData"][2])
        disabledInterval = True
        return fig, True, False, False, False
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


# Press "Start" button to start the thread and get hyperspectral data
@app.callback(
    Output("interval-hyper", "disabled", allow_duplicate=True),
    Output("startHyperBtn", "disabled", allow_duplicate=True),
    Output("showGraphbtn", "disabled", allow_duplicate=True),
    [Input("startHyperBtn", "n_clicks")],
    prevent_initial_call=True
)
def startHyper(n):
    thread = threading.Thread(
        target=repo.getHyperspectral, args=(scope,)).start()
    return False, True, True


# This callback will update the hyperspectral progress bar and load the hyperspectral image
@app.callback(
    Output('plot-hyper', 'figure', allow_duplicate=True),
    Output('interval-hyper', 'disabled', allow_duplicate=True),
    Output("startHyperBtn", "disabled", allow_duplicate=True),
    Output("showGraphbtn", "disabled", allow_duplicate=True),
    Output('hyperProgressBar', 'label', allow_duplicate=True),
    Output('hyperProgressBar', 'value', allow_duplicate=True),
    Input('interval-hyper', 'n_intervals'),
    prevent_initial_call=True
)
def checkHyperspectralProgress(n):
    if scope["HyperspectralLoading"] == False:
        scope['BarProgress'] = 0
        disabledInterval = True
        if scope["HyperspectralData"] is None:
            return dash.no_update, True, False, False, f"{scope['BarProgress']}%", scope["BarProgress"]
        fig = repo.generateFigureForPlot(scope["HyperspectralData"][2])
        return fig, True, False, False, f"{scope['BarProgress']}%", scope["BarProgress"]
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, f"{scope['BarProgress']}%", scope["BarProgress"]


# Press "Stop" button to stop the hyperspectral data loading
@app.callback(
    Output('hyperProgressBar', 'value'),
    Input('stopHyperBtn', 'n_clicks'),
    prevent_initial_call=True
)
def stopHyperspectral(n):
    scope["HyperspectralLoading"] = False
    return dash.no_update

# This callback will draw a rectangle on the plot when a point is clicked


@app.callback(
    Output('plot-initial', 'figure', allow_duplicate=True),
    Input('plot-initial', 'clickData'),
    prevent_initial_call=True,
    allow_duplicate=True
)
def drawRectangle(clickData):
    if clickData is None:
        return dash.no_update

    # Extract clicked point coordinates
    x_click = clickData['points'][0]['x']
    y_click = clickData['points'][0]['y']

    # Define the rectangle coordinates
    rect_x0 = x_click - 5
    rect_x1 = x_click + 5
    rect_y0 = y_click - 5
    rect_y1 = y_click + 5

    # Create the rectangle shape
    rectangle = {
        'type': 'rect',
        'x0': rect_x0,
        'x1': rect_x1,
        'y0': rect_y0,
        'y1': rect_y1,
        'line': {
            'color': 'rgba(50, 171, 96, 1)',
        }
    }

    # Get the current figure
    fig = repo.generateFigureForPlot(np.load('data.npy')[2])

    # Add the rectangle to the figure layout
    fig.update_layout(
        shapes=[rectangle],
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
