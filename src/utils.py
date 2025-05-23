import base64

import numpy

import openai
import os
from diffusers import StableDiffusionPipeline
import torch
device = "mps" if torch.backends.mps.is_available() else "cpu"

def encode_image(image):
    source = f'data:image/png;base64,{base64.b64encode(image).decode()}'
    return source



"""import requests
import base64
import os

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")  # Or paste it here directly

API_URL = API_URL = API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}"
}

def generate_image_from_prompt(prompt: str):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    if response.status_code != 200:
        print(f"Image generation failed: {response.status_code}, {response.text}")
        return None

    image_bytes = response.content
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/png;base64,{base64_image}"""

from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import base64
from io import BytesIO

# Setup model once (do this at import time)
#device = "mps" if torch.backends.mps.is_available() else "cpu"

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

    # ✅ Return base64 for Dash display
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    base64_image = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{base64_image}"



