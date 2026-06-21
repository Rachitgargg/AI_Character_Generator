import requests
import random
from typing import Optional

# Hugging Face text generation model
LORE_MODEL = "Qwen/Qwen2.5-7B-Instruct"
LORE_API_URL = f"https://router.huggingface.co/hf-inference/models/{LORE_MODEL}"

def generate_procedural_lore(user_prompt: str, style: str) -> str:
    """
    Generates a structured RPG character backstory and profile procedurally in Python.
    Used as a fallback when API key is missing or HF servers are offline/rate-limited.
    """
    p = user_prompt.lower()
    
    # Determine Class/Archetype & Abilities
    if any(k in p for k in ["mage", "wizard", "sorcerer", "magic", "spell", "witch"]):
        role = "Arcane Scholar (Mage)"
        abilities = "• **Astral Flare**: Unleashes a localized burst of cosmic energy dealing high area damage.\n• **Mana Barrier**: Shields the user by converting damage directly into mana consumption."
    elif any(k in p for k in ["ninja", "assassin", "rogue", "stealth", "shadow", "thief"]):
        role = "Shadow Operative (Assassin)"
        abilities = "• **Twilight Veil**: Blends into shadows, making the character invisible for 5 seconds.\n• **Toxic Pierce**: Inflicts a poisonous blade strike that causes ongoing damage over time."
    elif any(k in p for k in ["sci-fi", "space", "marine", "futuristic", "cyber", "robot", "android"]):
        role = "Cyber Raider (Specialist)"
        abilities = "• **Overdrive Matrix**: Increases combat and movement speed by 40% for a short duration.\n• **Nanite Reconstitution**: Deploys repair nanites to automatically heal injuries."
    elif any(k in p for k in ["knight", "warrior", "paladin", "shield", "sword", "soldier"]):
        role = "Vanguard Protector (Warrior)"
        abilities = "• **Iron Bulwark**: Raises shield to block 80% of incoming frontal damage.\n• **Valor Strike**: A powerful heavy attack that stuns opponents for 2 seconds."
    elif any(k in p for k in ["archer", "ranger", "hunter", "bow"]):
        role = "Elite Scout (Ranger)"
        abilities = "• **Seeker Shot**: Fires a tracking arrow that bypasses cover to hit enemies.\n• **Rain of Arrows**: Showers a designated area with physical projectiles."
    else:
        role = "Nomadic Wanderer (Adventurer)"
        abilities = "• **Adrenaline Surge**: Boosts movement speed and evasion in critical health.\n• **Counter Strike**: Parries incoming attacks and responds with a swift counter-blow."

    # Style-specific lists
    names_map = {
        "Fantasy": ["Eldrin Thorne", "Lyra Whisperwind", "Vaelen Frostwood", "Kaelen Emberforge", "Sariel Leafborn"],
        "Cyberpunk": ["Jax-07", "Cypher V", "Neon Rex", "Valkyrie X", "Hack-Slinger Zero"],
        "Sci-Fi": ["Commander Dax", "Dr. Nova Vance", "Zael Voidwalker", "Captain Rayne", "Astraea Prime"],
        "Medieval": ["Sir Roderick the Bold", "Lady Beatrice", "Lord Alistair", "Gerald of the Iron Keep", "Isolde the Just"],
        "Anime": ["Kaito Hyuga", "Asuka Shikinami", "Rin Okumura", "Sora Hikari", "Haruka Takahashi"]
    }
    
    factions_map = {
        "Fantasy": ["The Obsidian Order", "High Mages of the Citadel", "Elves of Lothlorien Alliance", "Keepers of the Sacred Grove"],
        "Cyberpunk": ["Syndicate 99", "Megacorp Division Delta", "The Undergrid Runners", "Neon Rebellion"],
        "Sci-Fi": ["United Star Alliance", "Void Syndicate", "Orion Border Colonists", "Nexus AI Network"],
        "Medieval": ["The Iron Shield Alliance", "Knights of the Round Table", "The Crown Guard of Valoria", "Highland Clans"],
        "Anime": ["Celestial Academy Guild", "Kurogane Adventurer Guild", "Shadow Vanguard Clan", "Elementalist Circle"]
    }

    name = random.choice(names_map.get(style, ["Alistair Gray"]))
    faction = random.choice(factions_map.get(style, ["The Wanderers Guild"]))

    # Procedural backstory template builder
    templates = [
        f"A veteran practitioner of the {role} craft, {name} belongs to the ranks of {faction}. Driven by the memory of a fallen home and equipped with exceptional training, they travel the realm in search of answers, using their skills to survive the dangerous journeys.",
        f"Whispers of {name}'s feats as a skilled {role} are heard throughout the territories of {faction}. Guided by their faction's ancient teachings, they keep to the shadows and specialize in neutralizing targets before any alarms are raised.",
        f"Once an apprentice within {faction}, {name} evolved into a formidable {role} after surviving a critical betrayal. They now operate on their own terms, seeking vengeance and carrying legendary secrets that could alter the balance of power."
    ]
    backstory = random.choice(templates)

    # Return Markdown formatted lore profile
    return f"""### 👤 {name}
* **Style Theme:** {style}
* **Role / Class:** {role}
* **Faction:** {faction}

#### 📖 Backstory
{backstory}

#### ✨ Special Abilities
{abilities}
"""

def generate_lore(prompt: str, style: str, api_key: str) -> str:
    """
    Queries Hugging Face Inference API for Qwen2.5-7B-Instruct to write character lore.
    Falls back to generate_procedural_lore if the request fails, times out, or has no api_key.
    """
    if not api_key or api_key.strip() == "" or api_key == "your_token_here":
        return generate_procedural_lore(prompt, style)

    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json"
    }

    # Format the prompt for Qwen Instruct chat format
    system_instruction = (
        "You are an expert creative RPG writer. Generate a short, immersive character profile "
        "containing Name, Role/Class, Faction, Backstory, and Special Abilities in a clean, "
        "readable Markdown format. Do not use conversational intro or outro text. Output only the "
        "formatted profile."
    )
    user_message = f"Create character lore. Description: {prompt}. Art Style Theme: {style}."
    
    formatted_prompt = (
        f"<|im_start|>system\n{system_instruction}<|im_end|>\n"
        f"<|im_start|>user\n{user_message}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )

    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "max_new_tokens": 350,
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(LORE_API_URL, headers=headers, json=payload, timeout=20)
        
        if response.status_code == 200:
            res_json = response.json()
            # Hugging Face serverless returns either list or dict
            text = ""
            if isinstance(res_json, list) and len(res_json) > 0:
                text = res_json[0].get("generated_text", "")
            elif isinstance(res_json, dict):
                text = res_json.get("generated_text", "")
                
            # Clean up potential chat wrapper tokens
            if text:
                text = text.replace("<|im_end|>", "").strip()
                return text

        # If API returned an error (e.g. rate limit, model starting up), fallback
        return generate_procedural_lore(prompt, style)
        
    except Exception:
        # Catch timeouts, connection errors, and fall back safely
        return generate_procedural_lore(prompt, style)
