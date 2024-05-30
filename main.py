import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import numpy as np
from dash import Input, Output, dcc, html
from sklearn import datasets
from sklearn.cluster import KMeans
import time

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
    "HyperspectralInProgress": False,
}


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = page.page


@app.callback(
    Output("plot-initial", "figure", allow_duplicate=True), [Input("showGraphbtn", "n_clicks")], prevent_initial_call=True,
)
def loadInitialGraph(n):
    element = repo.find_element_by_id(page.page, "startHyperBtn")
    element.color = "primary"
    data = np.load('data.npy')[2]
    return repo.generateFigureForPlot(data)


@app.callback(
    Output("plot-hyper", "figure"), [Input("startHyperBtn", "n_clicks")], prevent_initial_call=True
)
def loadHyperGraph(n):
    data = np.load('data.npy')[2]
    return repo.generateFigureForPlot(data)


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
