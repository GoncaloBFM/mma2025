import threading
from io import BytesIO
from traceback import print_tb

import torch
from dash import Input, Output, callback, State
from diffusers import StableDiffusionPipeline

from src import config, utils

lock = threading.Lock()
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
).to('cuda' if torch.cuda.is_available() else ('mps' if torch.backends.mps.is_available() else 'cpu'))

@callback(
    Output('generated-image', 'src', allow_duplicate=True),
    Output('generate-prompt-button', 'disabled'),
    Output('generate-image-button', 'disabled'),
    Output('prompt', 'disabled'),
    State('prompt', 'value'),
    Input('generate-image-button', 'n_clicks'),
    background=True,
    prevent_initial_call=True,
)
def generate_image_from_prompt(prompt, _):
    print('Generate image button is pressed, waiting to acquire lock on model')
    with lock:
        print('Lock on model acquired')
        image = pipe(prompt).images[0]
    image = image.resize(config.GENERATED_IMAGE_SIZE)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return utils.encode_image(buffer.getvalue()), False, False, False

@callback(
    Output('prompt', 'value'),
    State("characteristics-description", 'children'),
    Input('generate-prompt-button', 'n_clicks'),
    prevent_initial_call=True,
)
def generate_prompt_from_characteristic(characteristics_html, _):
    print('Generate prompt button is pressed')
    characteristics = map(lambda x: x['props']['children'], characteristics_html)
    cleaned_phrases = list(map(lambda x: x.replace("has ", "").replace(":", "").replace("_", " ").strip(), characteristics))
    if len(cleaned_phrases) > 1:
        return "A bird with " +", ".join(cleaned_phrases[:-1]) + ", and " + cleaned_phrases[-1] + "."
    elif len(cleaned_phrases) == 1:
        return f"A bird with {cleaned_phrases[0]}."
    return ''

@callback(
    Output('generate-image-button', 'disabled', allow_duplicate=True),
    Output('generate-prompt-button', 'disabled', allow_duplicate=True),
    Output('prompt', 'disabled', allow_duplicate=True),
    Input('generate-image-button', 'n_clicks'),
    prevent_initial_call=True,
)
def generate_image_from_prompt(_):
    return True, True, True
