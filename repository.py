import plotly.graph_objs as go
import time
import numpy as np

# This function is used to generate a figure for the plot, it takes in a 2D array of data and returns a figure


def generateFigureForPlot(data):
    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        z=data,
        colorscale='Inferno'
    ))

    return fig


def findElementById(component, target_id):
    if getattr(component, 'id', None) == target_id:
        return component

    if hasattr(component, 'children'):
        children = component.children
        if isinstance(children, list):
            for child in children:
                result = findElementById(child, target_id)
                if result:
                    return result
        elif children is not None:
            result = findElementById(children, target_id)
            if result:
                return result

    return None


def getInitialImage(scope):
    scope["InitialImageLoading"] = True
    time.sleep(4)
    scope["InitialImageData"] = np.load('data.npy')
    scope["InitialImageLoading"] = False


def getHyperspectral(scope):
    scope["HyperspectralLoading"] = True
    for i in range(10+1):
        if scope["HyperspectralLoading"] == False:
            scope["HyperspectralData"] = None
            return
        scope["BarProgress"] = i*10
        time.sleep(1)

    scope["HyperspectralData"] = np.load('data.npy')
    scope["HyperspectralLoading"] = False
