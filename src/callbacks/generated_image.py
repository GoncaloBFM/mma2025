

from dash import Input, Output, State, html,callback, callback_context, no_update
from dash.exceptions import PreventUpdate
from src.utils import generate_image_from_prompt
from src.widgets.generated_image import build_prompt_from_data

@callback(
        Output('prompt-text', 'children'),
        Output('generated-image-output', 'children'),
        Output('generate-image-btn', 'disabled'),
        Input('scatterplot', 'selectedData'),
        Input('generate-image-btn', 'n_clicks'),
        prevent_initial_call=True
    )
def unified_callback(selected_data, n_clicks):
    triggered = callback_context.triggered_id

    if not selected_data or 'points' not in selected_data:
        raise PreventUpdate

    # Build prompt from selection
    prompt = build_prompt_from_data(selected_data)
    prompt_display = html.Div([
        html.H5("Prompt Used:"),
        html.P(prompt, style={"fontStyle": "italic"})
    ])

    # If selection changed, show prompt and clear image
    if triggered == 'scatterplot':
        return prompt_display, None, False  # ❌ Clear image

    #  If button clicked, generate image
    if triggered == 'generate-image-btn':
        image_src = generate_image_from_prompt(prompt)
        image_display = html.Img(src=image_src, style={"maxWidth": "300px", "height": "auto"})
        return prompt_display, image_display, False

    return no_update, no_update, no_update
