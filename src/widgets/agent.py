import dash.dcc
from dash import html, dcc
from src.Dataset import Dataset
import dash_bootstrap_components as dbc

def generate_agent_widget():
    return dbc.Stack([
        html.H5('Top 10 characteristics'),
        html.Div(id='characteristics-description'),
        html.H5('Prompt'),
        dash.dcc.Textarea(id='prompt'),
        dbc.Stack([
            html.Button("Generate prompt", id="generate-prompt-button", className="btn btn-outline-primary"),
            html.Button("Generate image", id="generate-image-button", className="btn btn-outline-primary")
        ],
            direction="horizontal",
            gap=2,
            className="agent-buttons"
        ),

        dcc.Loading(
            type="circle",
            children=html.Div(html.Img(id="generated-image"), className='generated-image-container')
        ),
    ], className='agent-container border-widget')

def get_top_characteristics(selected_data):
    if not len(selected_data):
        return []

    attr_data = Dataset.get_attr_data().loc[selected_data.index]

    characteristic_pairs = sorted(
        attr_data.columns.map(lambda col: (col, attr_data[col].sum())),
        key=lambda t: t[1],
        reverse=True
    )[:10]
    return list(map(lambda x: html.P(f'{x[0]}'), characteristic_pairs))