"""
IMAGE GENERATION MODULE
Uses Stable Diffusion (free tier) to generate AI images
Integrates with autonomous agent
"""

import os
import requests
import json
from typing import List, Optional

# ================== CONFIGURATION ==================

MEDIA_DIR = "/app/media"
os.makedirs(MEDIA_DIR, exist_ok=True)

# Free image generation APIs
REPLICATE_API = os.environ.get("REPLICATE_API_TOKEN", "")  # Free tier available
HF_API = os.environ.get("HF_API_TOKEN", "")  # Hugging Face free inference

class ImageGenerator:
    """Generate AI images using free APIs"""

    @staticmethod
    def generate_with_replicate(prompt: str, niche: str) -> Optional[str]:
        """Generate image using Replicate (free tier)"""
        try:
            import replicate

            output = replicate.run(
                "black-forest-labs/flux-schnell",
                input={
                    "prompt": prompt,
                    "go_fast": True,
                    "guidance": 3.5,
                }
            )

            if output and len(output) > 0:
                img_url = output[0]
                filename = f"replicate_{niche}_{int(__import__('time').time())}.jpg"
                filepath = os.path.join(MEDIA_DIR, filename)

                img_data = requests.get(img_url, timeout=30).content
                with open(filepath, 'wb') as f:
                    f.write(img_data)

                print(f"✓ Generated: {filename}")
                return filepath

        except Exception as e:
            print(f"✗ Replicate error: {str(e)[:50]}")

        return None

    @staticmethod
    def generate_with_hugging_face(prompt: str, niche: str) -> Optional[str]:
        """Generate image using Hugging Face (free inference API)"""
        try:
            api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3-medium"
            headers = {"Authorization": f"Bearer {HF_API}"}

            payload = {
                "inputs": prompt,
                "parameters": {
                    "negative_prompt": "low quality, blurry",
                    "num_inference_steps": 20
                }
            }

            response = requests.post(api_url, headers=headers, json=payload, timeout=60)

            if response.status_code == 200:
                filename = f"hf_{niche}_{int(__import__('time').time())}.jpg"
                filepath = os.path.join(MEDIA_DIR, filename)

                with open(filepath, 'wb') as f:
                    f.write(response.content)

                print(f"✓ Generated: {filename}")
                return filepath

        except Exception as e:
            print(f"✗ HF error: {str(e)[:50]}")

        return None

    @staticmethod
    def generate_carousel_images(prompts: List[str], niche: str) -> List[str]:
        """Generate 3 images for carousel"""
        images = []

        print(f"\n🎨 Generating {len(prompts)} images for carousel...")

        for i, prompt in enumerate(prompts):
            print(f"  Image {i+1}: {prompt[:40]}...")

            # Try Replicate first, fallback to HF
            img = ImageGenerator.generate_with_replicate(prompt, niche)

            if not img:
                img = ImageGenerator.generate_with_hugging_face(prompt, niche)

            if img:
                images.append(img)

        return images

# ================== USAGE ==================

def main():
    """Test image generation"""
    print("IMAGE GENERATOR TEST")
    print("="*80)

    prompts = [
        "Professional AI technology workspace with holographic elements, neon blue lighting",
        "Digital transformation in modern business, abstract technology",
        "Future workplace with intelligent AI systems, clean design"
    ]

    images = ImageGenerator.generate_carousel_images(prompts, "future_tech_ai")

    print(f"\nGenerated {len(images)} images:")
    for img in images:
        print(f"  ✓ {img}")

if __name__ == "__main__":
    main()
