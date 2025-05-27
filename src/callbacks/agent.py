from io import BytesIO

import torch
from dash import Input, Output, callback, State
from diffusers import StableDiffusionPipeline

from src import config, utils

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
).to('cuda' if torch.cuda.is_available() else ('mps' if torch.backends.mps.is_available() else 'cpu'))

@callback(
    Output('generated-image', 'src', allow_duplicate=True),
    Output('generate-image-button', 'disabled'),
    Output('prompt', 'disabled'),
    State('prompt', 'value'),
    Input('generate-image-button', 'n_clicks'),
    prevent_initial_call=True,
)
def generate_image_from_prompt(prompt, _):
    image = pipe(prompt).images[0]
    image = image.resize(config.GENERATED_IMAGE_SIZE)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return utils.encode_image(buffer.getvalue()), False, False

@callback(
    Output('generate-image-button', 'disabled', allow_duplicate=True),
    Output('prompt', 'disabled', allow_duplicate=True),
    Input('generate-image-button', 'n_clicks'),
    prevent_initial_call=True,
)
def generate_image_from_prompt(_):
    return True, True
