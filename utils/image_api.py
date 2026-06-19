import os
import requests
import io
from typing import Tuple, Optional
from PIL import Image, ImageDraw

from utils.constants import API_URL

def generate_image(prompt: str, size: str, api_key: str, mock: bool = False) -> Tuple[Optional[bytes], Optional[str]]:
    """
    Sends a request to Hugging Face Inference API to generate an image using FLUX.1-schnell.
    If mock is True, or if the api_key is missing/empty, it falls back to generating
    a beautiful visual placeholder locally using Pillow.
    
    Args:
        prompt (str): The enhanced prompt description.
        size (str): Selected image size like "512x512".
        api_key (str): Hugging Face Inference API Token.
        mock (bool): Force mock preview generation.
        
    Returns:
        Tuple[Optional[bytes], Optional[str]]: A tuple containing (image_bytes, error_message).
    """
    try:
        width, height = map(int, size.split('x'))
    except Exception:
        width, height = 512, 512

    # Fall back to mockup mode if API key is missing or mock is explicitly enabled
    if mock or not api_key or api_key.strip() == "" or api_key == "your_token_here":
        try:
            # Create a nice sci-fi/fantasy themed layout placeholder
            img = Image.new("RGB", (width, height), color=(18, 18, 29))
            draw = ImageDraw.Draw(img)
            
            # Subtle gradient circles in background
            draw.ellipse([width * 0.1, height * 0.1, width * 0.9, height * 0.9], fill=(28, 28, 48), outline=(60, 60, 110), width=1)
            draw.ellipse([width * 0.25, height * 0.25, width * 0.75, height * 0.75], fill=(38, 38, 68), outline=(80, 80, 160), width=1)
            
            # Outer neon border
            draw.rectangle([15, 15, width - 15, height - 15], outline=(100, 108, 255), width=2)
            
            # Corner accents
            accent_len = 30
            # Top-Left
            draw.line([15, 15, 15 + accent_len, 15], fill=(0, 240, 255), width=4)
            draw.line([15, 15, 15, 15 + accent_len], fill=(0, 240, 255), width=4)
            # Top-Right
            draw.line([width - 15, 15, width - 15 - accent_len, 15], fill=(0, 240, 255), width=4)
            draw.line([width - 15, 15, width - 15, 15 + accent_len], fill=(0, 240, 255), width=4)
            # Bottom-Left
            draw.line([15, height - 15, 15 + accent_len, height - 15], fill=(0, 240, 255), width=4)
            draw.line([15, height - 15, 15, height - 15 - accent_len], fill=(0, 240, 255), width=4)
            # Bottom-Right
            draw.line([width - 15, height - 15, width - 15 - accent_len, height - 15], fill=(0, 240, 255), width=4)
            draw.line([width - 15, height - 15, width - 15, height - 15 - accent_len], fill=(0, 240, 255), width=4)

            # Central icon shape (diamond)
            center_x, center_y = width // 2, height // 2
            d_size = 50
            draw.polygon([
                (center_x, center_y - d_size),
                (center_x + d_size, center_y),
                (center_x, center_y + d_size),
                (center_x - d_size, center_y)
            ], fill=(80, 70, 140), outline=(255, 0, 128), width=2)
            
            # Narrative message
            text = (
                "🎮 AI Game Character Creator 🎮\n\n"
                "[MOCK PREVIEW GENERATOR]\n"
                "To generate real AI art, add your\n"
                "HF_API_KEY in the .env file.\n\n"
                f"Enhancing Prompt:\n\"{prompt[:45]}...\""
            )
            
            draw.text((center_x, center_y), text, fill=(255, 255, 255), anchor="mm", align="center")
            
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return buf.getvalue(), None
        except Exception as e:
            return None, f"Failed to generate mock image placeholder: {str(e)}"

    # Setup Hugging Face API Request
    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json"
    }
    
    # Send request with prompt inputs. FLUX.1-schnell is text-to-image.
    payload = {
        "inputs": prompt,
        "parameters": {
            "width": width,
            "height": height
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        # Check for model loading states
        if response.status_code == 503:
            return None, "The model is currently starting up on Hugging Face servers. Please wait 10-20 seconds and try again."
        
        # Check for unauthorized API token
        if response.status_code == 401:
            return None, "Unauthorized. Your Hugging Face API token is invalid or has expired. Please check your credentials."
            
        if response.status_code != 200:
            error_msg = "Unknown API error"
            try:
                err_json = response.json()
                if isinstance(err_json, dict) and "error" in err_json:
                    error_msg = err_json["error"]
                elif isinstance(err_json, list) and len(err_json) > 0:
                    error_msg = str(err_json[0])
            except Exception:
                error_msg = response.text[:200]
            return None, f"Hugging Face API returned error ({response.status_code}): {error_msg}"
            
        return response.content, None
        
    except requests.exceptions.Timeout:
        return None, "The connection to Hugging Face API timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return None, f"An error occurred while connecting to Hugging Face: {str(e)}"
