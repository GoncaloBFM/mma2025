import base64
import numpy
import openai
import os
import torch
from PIL import Image
from io import BytesIO
from diffusers import StableDiffusionPipeline

device = "mps" if torch.backends.mps.is_available() else "cpu"

def encode_image(image):
    source = f'data:image/png;base64,{base64.b64encode(image).decode()}'
    return source





# Setup model once (do this at import time)
#for mac device = "mps" if torch.backends.mps.is_available() else "cpu"
#for linux/windows device =  "cuda" if torch.backends.mps.is_available() else "cpu"

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
).to(device)

from PIL import Image
from io import BytesIO
import base64

def generate_image_from_prompt(prompt: str, save_path: str = None, size: tuple = (200, 300)) -> str:
    # Generate image from the model
    image: Image.Image = pipe(prompt).images[0]

    image = image.resize(size, Image.Resampling.LANCZOS)

   
    if save_path:
        image.save(save_path)
        print(f"Image saved to: {save_path}")

    #Return base64 for Dash display
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    base64_image = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{base64_image}"



