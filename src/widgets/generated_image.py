from dash import html, dcc
import dash_bootstrap_components as dbc
from src.Dataset import Dataset
from src.utils import generate_image_from_prompt  # ← local version 




def create_generated_image_widget():
    return html.Div([
        html.Button("Generate", id="generate-image-btn", n_clicks=0, disabled=True, className="btn btn-primary mb-3"),

        html.Div([
            # Prompt (left side)
            html.Div(id='prompt-text', style={
                "flex": "1",
                "padding": "15px",
                "backgroundColor": "#f8f9fa",
                "border": "1px solid #dee2e6",
                "borderRadius": "8px",
                "marginRight": "10px",
                "minWidth": "250px",
                "maxWidth": "100%"
            }),

            # Image + Spinner (right side)
            dcc.Loading(
                id="loading-spinner",
                type="cube",# circle
                children=html.Div(
                    id='generated-image-output',
                    style={
                        "flex": "1",
                        "padding": "15px",
                        "border": "1px solid #dee2e6",
                        "borderRadius": "8px",
                        "minWidth": "250px",
                        "maxWidth": "100%"
                    }
                )
            )
        ], style={
            "display": "flex",
            "flexDirection": "row",
            "alignItems": "flex-start",
            "justifyContent": "flex-start",
            "flexWrap": "wrap",  #Ensures mobile responsiveness
            "gap": "10px"
        })
    ])

def draw_generated_image(data_selected=None):
    if data_selected is None or len(data_selected) == 0:
        return "Select data on the scatterplot"

    attr_data = Dataset.get_attr_data().loc[data_selected.index]

    # Get top 10 characteristic-value pairs
    characteristic_pairs = sorted(
        attr_data.columns.map(lambda col: (col, attr_data[col].sum())),
        key=lambda t: t[1],
        reverse=True
    )[:10]

    # Clean and rephrase
    cleaned_phrases = []
    for attr_name, _ in characteristic_pairs:
        attr_clean = attr_name.replace("has ", "").replace(":", "").replace("_", " ")
        cleaned_phrases.append(attr_clean.strip())

    # Build the prompt
    if len(cleaned_phrases) > 1:
        prompt = (
            "A bird with " +
            ", ".join(cleaned_phrases[:-1]) +
            ", and " + cleaned_phrases[-1] + "."
        )
    elif len(cleaned_phrases) == 1:
        prompt = f"A bird with {cleaned_phrases[0]}."
    else:
        prompt = "A bird with distinctive features."

    # Generate image
    image_src = generate_image_from_prompt(prompt)

    # Display prompt + image
    layout = dbc.Stack([
        html.Div([
            html.H5("Prompt Used:"),
            html.P(prompt, style={"fontStyle": "italic"})
        ]),
        html.Img(src=image_src, style={"maxWidth": "300px", "height": "auto"})
    ], direction="horizontal", className="agent-container")

    return layout


from src.Dataset import Dataset

import pandas as pd

def build_prompt_from_data(selected_data):
    # Safety check
    if not selected_data or 'points' not in selected_data:
        return "A bird with distinctive features."

    # Extract selected row indices from scatterplot
    indices = [p['pointIndex'] for p in selected_data['points']]
    df = pd.DataFrame(index=indices)

    # Get attributes for selected rows
    attr_data = Dataset.get_attr_data().loc[df.index]

    # Get top 10 characteristics
    characteristic_pairs = sorted(
        attr_data.columns.map(lambda col: (col, attr_data[col].sum())),
        key=lambda t: t[1],
        reverse=True
    )[:10]

    # Clean and rephrase
    cleaned_phrases = []
    for attr_name, _ in characteristic_pairs:
        attr_clean = attr_name.replace("has ", "").replace(":", "").replace("_", " ")
        cleaned_phrases.append(attr_clean.strip())

    # Build final prompt
    if len(cleaned_phrases) > 1:
        prompt = (
            "A bird with " +
            ", ".join(cleaned_phrases[:-1]) +
            ", and " + cleaned_phrases[-1] + "."
        )
    elif len(cleaned_phrases) == 1:
        prompt = f"A bird with {cleaned_phrases[0]}."
    else:
        prompt = "A bird with distinctive features."

    return prompt
