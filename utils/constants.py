# Style options available in the selector
STYLES = ["Fantasy", "Cyberpunk", "Sci-Fi", "Medieval", "Anime"]

# Style-conditioned prompt templates
# These append modifiers to the user prompt to achieve the selected aesthetic
STYLE_TEMPLATES = {
    "Fantasy": "{prompt}, fantasy game character, epic armor, cinematic lighting, detailed concept art, highly detailed, digital painting, unreal engine 5 render, character concept design",
    "Cyberpunk": "{prompt}, cyberpunk character, neon lights, futuristic city background, techwear, detailed concept art, ultra realistic, cybernetic enhancements, volumetric lighting",
    "Sci-Fi": "{prompt}, sci-fi space character, futuristic armor, spacesuit, holographic interfaces, alien planet background, hard surface design, highly detailed, realistic sci-fi concept art",
    "Medieval": "{prompt}, medieval knight warrior character, historical chainmail armor, castle background, dramatic lighting, gritty realism, detailed digital illustration, oil painting style",
    "Anime": "{prompt}, anime character design, vibrant colors, detailed illustration, studio quality, digital anime art style, key visual, beautiful detailed eyes, clean lineart"
}

# Image size options
IMAGE_SIZES = ["512x512", "768x768", "1024x1024"]

# Random character ideas for the idea generator
RANDOM_CHARACTER_IDEAS = [
    "Shadow Assassin with glowing daggers and a hooded cloak",
    "Dragon Knight in ornate scale armor holding a flaming greatsword",
    "Space Marine scout with high-tech visor and plasma rifle",
    "Cyber Ninja crouching on a neon-lit skyscraper ledge",
    "Desert Mage wielding an ancient staff with swirling sand magic",
    "Undead Archer drawing a bow of green spectral energy",
    "Valiant Paladin with a silver shield emitting divine golden light",
    "Clockwork Alchemist surrounded by steam gears and colorful potions",
    "Elven Ranger tracking prey in a luminous mystical forest",
    "Cybernetic Mercenary with a mechanical arm and tactical combat gear"
]

# Model configuration
DEFAULT_MODEL = "black-forest-labs/FLUX.1-schnell"
API_URL = f"https://router.huggingface.co/hf-inference/models/{DEFAULT_MODEL}"
