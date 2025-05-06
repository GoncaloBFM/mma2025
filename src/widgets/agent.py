from dash import html
import plotly.graph_objects as go

from src.Dataset import Dataset
import dash_bootstrap_components as dbc

def create_agent():
    return html.Div("Select data on the scatterplot", id='agent', className='stretchy-widget border-widget')

def draw_agent(data_selected=None):
    if data_selected is None or len(data_selected) == 0:
        return "Select data on the scatterplot"

    attr_data = Dataset.get_attr_data().loc[data_selected.index]
    top_characteristics = list(map(lambda t: t[0], sorted(
        attr_data.columns.map(lambda col: (col, attr_data[col].sum())),
        key=lambda t: t[1],
        reverse=True
    )[:10]))
    characteristics_stack = dbc.Stack(list(map(lambda characteristic: html.P(characteristic), ['TOP CHARACTERISTICS']+top_characteristics)), direction="vertical")
    content = dbc.Stack([characteristics_stack, html.Img(src='https://picsum.photos/200/300')], direction="horizontal", className='agent-container')

    return content
