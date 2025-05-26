from diffusers import StableDiffusionPipeline
import torch
# if your machine is mac then st device=mps, other wise set it cuda  
device = "mps" if torch.backends.mps.is_available() else "cpu"
if torch.backends.mps.is_available():
    torch.mps.empty_cache()
    torch.mps.synchronize()
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
).to(device)

def generate_image(prompt, output_path="./"):
    image = pipe(prompt).images[0]
    image.save(output_path)
    print(f"Image saved to {output_path}")

# Example
generate_image("A futuristic city skyline with flying cars at sunset")
