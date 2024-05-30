import plotly.graph_objs as go

# This function is used to generate a figure for the plot, it takes in a 2D array of data and returns a figure


def generateFigureForPlot(data):
    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        z=data,
        colorscale='Inferno'
    ))

    return fig


def find_element_by_id(component, target_id):
    if getattr(component, 'id', None) == target_id:
        return component

    if hasattr(component, 'children'):
        children = component.children
        if isinstance(children, list):
            for child in children:
                result = find_element_by_id(child, target_id)
                if result:
                    return result
        elif children is not None:
            result = find_element_by_id(children, target_id)
            if result:
                return result

    return None
