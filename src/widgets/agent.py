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
            html.Button("Generate", id="generate-image-button", className="btn btn-outline-primary"),
            dcc.Loading(
                type="circle",
                children=html.Div(html.Img(id="generated-image"), className='generated-image-container')
            ),
    ], className='agent-container border-widget')

def get_top_characteristics(selected_data):
    if not len(selected_data):
        return "A bird with distinctive features."

    attr_data = Dataset.get_attr_data().loc[selected_data.index]

    characteristic_pairs = sorted(
        attr_data.columns.map(lambda col: (col, attr_data[col].sum())),
        key=lambda t: t[1],
        reverse=True
    )[:10]
    return characteristic_pairs

def build_characteristics_description(characteristic_pairs):
    return list(map(lambda x: html.P(f'{x[0]}: {x[1]}'), characteristic_pairs))

def build_prompt(characteristics_pairs):
    cleaned_phrases = list(map(lambda x: x[0].replace("has ", "").replace(":", "").replace("_", " ").strip(), characteristics_pairs))

    if len(cleaned_phrases) > 1:
        return "A bird with " +", ".join(cleaned_phrases[:-1]) + ", and " + cleaned_phrases[-1] + "."
    elif len(cleaned_phrases) == 1:
        return f"A bird with {cleaned_phrases[0]}."