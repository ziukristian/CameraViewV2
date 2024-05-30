import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

initialImageControlCard = dbc.Card(
    [
        dbc.CardHeader("Initial Image Control"),
        dbc.CardBody(
            [
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Wavenumber (cm-1)"),
                        dbc.Input(placeholder="1450",
                                  type="number", value=1450),
                    ], size="sm", style={"flex": "1 1 45%"}
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Frames"),
                        dbc.Input(placeholder="5000",
                                  type="number", value=5000),
                    ], size="sm", style={"flex": "1 1 45%"}
                ),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Nanoseconds"),
                        dbc.Select(options=[
                            {"label": "500 ns", "value": 500},
                        ], value=500),
                    ], size="sm", style={"flex": "1 1 45%"}
                ),
                dbc.Button("Acquire Initial Image",
                           id="showGraphbtn", size="sm", color="primary", style={"flex": "1 1 45%"}),
            ],
            style={"display": "flex", "flexDirection": "row",
                   "gap": "5px", "flexWrap": "wrap"},

        ),
    ]
)

regionOfInterestCard = dbc.Card(
    [
        dbc.CardHeader("Region of Interest"),
        dbc.CardBody(
            [
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("Square size (px)"),
                        dbc.Select(options=[
                            {"label": "256x256", "value": 256},
                        ], value=256),
                    ], size="sm"
                ),
            ],
            style={"display": "flex", "flexDirection": "row",
                   "gap": "5px", "flexWrap": "wrap"},
        ),
    ]
)

hyperspectralControlCard = dbc.Card(
    [
        dbc.CardHeader("HyperSpectral Control"),
        dbc.CardBody([
            dbc.Switch(
                id="hyperspectral-switch",
                label="On/Off",
                value=False,  style={"flex": "1 1 45%"}
            ),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("Step (cm-1)"),
                    dbc.Select(options=[
                        {"label": "4", "value": 4},
                        {"label": "8", "value": 8},
                        {"label": "16", "value": 16},
                        {"label": "32", "value": 32},
                    ], value=4),
                ], size="sm", style={"flex": "1 1 45%"}
            ),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("Min. Wavenumber (cm-1)"),
                    dbc.Input(placeholder="1042",
                              type="number", value=1042),
                ], size="sm", style={"flex": "1 1 45%"}
            ),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("Max. Wavenumber (cm-1)"),
                    dbc.Input(placeholder="1840",
                              type="number", value=1840),
                ], size="sm", style={"flex": "1 1 45%"}
            ),
            dbc.Button("Start",
                       id="startHyperBtn", size="sm", color="success", style={"flex": "1 1 45%"}),
            dbc.Button("Stop",
                       id="stopHyperBtn", size="sm", color="danger", style={"flex": "1 1 45%"}),
            dbc.Progress(id="hyperProgressBar", label="0%", value=0, style={
                "flex": "1 1 45%", "marginTop": "10px"}),
        ], style={"display": "flex", "flexDirection": "row",
                  "gap": "5px", "flexWrap": "wrap"},)
    ]
)

saveDataCard = dbc.Card(
    [
        dbc.CardHeader("Save Data"),
        dbc.CardBody([
            dbc.Button("Save Initial Image (.txt)",
                       id="saveInitialTxtBtn", size="sm", color="secondary", style={"flex": "1 1 27%"}),
            dbc.Button("Save Hypercube (.npy)",
                       id="saveHyperNpyBtn", size="sm", color="secondary", style={"flex": "1 1 27%"}),
            dbc.Button("Save Hypercube (.txt)",
                       id="saveHyperTxtBtn", size="sm", color="secondary", style={"flex": "1 1 27%"}),
        ], style={"display": "flex", "flexDirection": "row",
                  "gap": "5px", "flexWrap": "wrap"},)
    ]
)

controls = html.Div(
    [
        initialImageControlCard,
        regionOfInterestCard,
        hyperspectralControlCard,
        saveDataCard
    ],
    style={
        "overflowY": "auto",
        "height": "90vh",
        "display": "flex",
        "flexDirection": "column",
        "gap": "5px",
    }
)

page = dbc.Container(
    [
        dcc.Interval(
            id='interval-hyper',
            interval=1*1000,  # Update every second (1000 milliseconds)
            n_intervals=0,  # Number of times the interval has triggered
            disabled=True
        ),
        dcc.Interval(
            id='interval-initial',
            interval=1*1000,  # Update every second (1000 milliseconds)
            n_intervals=0,  # Number of times the interval has triggered
            disabled=True
        ),
        html.H1("Camera View"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, sm=4),
                dbc.Col(dcc.Graph(id="plot-initial",
                        style={"aspectRatio": "1 / 1"}), sm=4),
                dbc.Col(dcc.Graph(id="plot-hyper",
                        style={"aspectRatio": "1 / 1"}), sm=4),
            ],
            align="center",
        ),
    ],
    fluid=True,
)
