from utils.constants import STYLE_TEMPLATES

def build_prompt(user_prompt: str, style: str) -> str:
    """
    Builds a style-conditioned prompt from the user's input prompt and selected style.
    
    Args:
        user_prompt (str): The character description entered by the user.
        style (str): The chosen game style (e.g. Fantasy, Cyberpunk).
        
    Returns:
        str: The enhanced style-conditioned prompt.
    """
    if not user_prompt:
        return ""
    
    # Retrieve template or default to simple user prompt
    template = STYLE_TEMPLATES.get(style, "{prompt}")
    return template.format(prompt=user_prompt.strip())
