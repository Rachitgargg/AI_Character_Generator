import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

# Import utilities
from utils.constants import STYLES, IMAGE_SIZES, RANDOM_CHARACTER_IDEAS, DEFAULT_MODEL
from utils.prompt_builder import build_prompt
from utils.image_api import generate_image

# Load environment variables
load_dotenv()
api_key = os.getenv("HF_API_KEY", "")

# Streamlit Page Setup
st.set_page_config(
    page_title="AI Game Character Creator",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling via markdown
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        margin-bottom: 0.1rem;
        padding-top: 10px;
    }
    
    .subtitle {
        color: #a0aec0;
        font-size: 1.1rem;
        margin-bottom: 1.8rem;
    }
    
    .panel-card {
        background-color: #1a1a2e;
        border: 1px solid #303056;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 1.2rem;
    }
    
    /* Styled tags/badges */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        text-transform: uppercase;
        margin-right: 6px;
    }
    
    .badge-fantasy { background-color: #8A2BE2; color: #FFF; }
    .badge-cyberpunk { background-color: #FF007F; color: #FFF; }
    .badge-scifi { background-color: #00BFFF; color: #FFF; }
    .badge-medieval { background-color: #D2691E; color: #FFF; }
    .badge-anime { background-color: #FF4500; color: #FFF; }
</style>
""", unsafe_allow_html=True)

# Initialize Session States
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "current_image" not in st.session_state:
    st.session_state.current_image = None
if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""
if "current_enhanced" not in st.session_state:
    st.session_state.current_enhanced = ""
if "current_style" not in st.session_state:
    st.session_state.current_style = "Fantasy"
if "current_size" not in st.session_state:
    st.session_state.current_size = "512x512"

def randomize_prompt():
    import random
    st.session_state.prompt_input = random.choice(RANDOM_CHARACTER_IDEAS)

# HEADER SECTION
st.markdown("<h1 class='main-title'>🎮 AI Game Character Creator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Generate unique, high-quality game character concept art powered by state-of-the-art AI models.</p>", unsafe_allow_html=True)

# SIDEBAR CONFIGURATION
with st.sidebar:
    st.image("https://img.icons8.com/isometric/512/controller.png", width=80)
    st.markdown("### 🛠️ Character Parameters")
    
    # 1. Style Selection
    selected_style = st.selectbox(
        "Choose Art Style:",
        options=STYLES,
        index=STYLES.index(st.session_state.current_style) if st.session_state.current_style in STYLES else 0,
        help="Applies thematic prompt modifiers to achieve the desired aesthetics."
    )
    st.session_state.current_style = selected_style
    
    # 2. Image Size Selector
    selected_size = st.selectbox(
        "Select Resolution:",
        options=IMAGE_SIZES,
        index=IMAGE_SIZES.index(st.session_state.current_size) if st.session_state.current_size in IMAGE_SIZES else 0,
        help="Higher resolutions provide finer detail but might take longer to generate."
    )
    st.session_state.current_size = selected_size
    
    # 3. Random Idea Generator
    st.markdown("---")
    st.markdown("#### 💡 Need Inspiration?")
    st.button("🎲 Generate Random Idea", on_click=randomize_prompt, width="stretch")
    
    # 4. Project Information
    st.markdown("---")
    st.markdown("### ℹ️ Project Info")
    st.markdown(f"**Model:** `{DEFAULT_MODEL}`")
    st.markdown("**Framework:** Streamlit + Python 3.11")
    
    # API Credentials Status indicator
    if not api_key:
        st.warning("⚠️ HF_API_KEY is not configured in `.env`. Application is running in **Demo Mode** (local mockup generation).")
    else:
        st.success("🔑 Hugging Face API key connected.")

# MAIN CONTENT AREA
col_input, col_display = st.columns([5, 4], gap="large")

with col_input:
    st.markdown("### 📝 Define Your Character")
    
    # Text Area for Character Description
    user_prompt = st.text_area(
        "Character Description:",
        key="prompt_input",
        placeholder="Describe your character in detail (e.g., 'A stealthy dark elf rogue hiding in the shadows holding twin glowing daggers')...",
        height=150,
        help="Specify features like gender, race, equipment, armor, pose, colors, and background scenery."
    )
    
    # Highlight chosen style badge
    badge_class = f"badge-{selected_style.lower()}"
    st.markdown(f"Active Theme Modifier: <span class='badge {badge_class}'>{selected_style}</span>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generate Button
    generate_clicked = st.button("🚀 Generate Character concept art", width="stretch")
    
    if generate_clicked:
        if not user_prompt.strip():
            st.warning("⚠️ Please provide a character description or generate a random idea first.")
        else:
            final_prompt = build_prompt(user_prompt, selected_style)
            
            with st.spinner("🧙‍♂️ Materializing your character... (This might take a moment)"):
                # Call Image API
                # If API key is missing, image_api.py falls back to mock mode internally
                img_bytes, error_msg = generate_image(final_prompt, selected_size, api_key)
                
                if error_msg:
                    st.error(f"❌ Generation failed: {error_msg}")
                elif img_bytes:
                    st.session_state.current_image = img_bytes
                    st.session_state.current_prompt = user_prompt
                    st.session_state.current_enhanced = final_prompt
                    st.session_state.current_style = selected_style
                    st.session_state.current_size = selected_size
                    
                    # Store in History
                    history_entry = {
                        "prompt": user_prompt,
                        "enhanced_prompt": final_prompt,
                        "style": selected_style,
                        "size": selected_size,
                        "timestamp": datetime.now().strftime("%I:%M:%S %p"),
                        "image_bytes": img_bytes
                    }
                    st.session_state.history.insert(0, history_entry)
                    if len(st.session_state.history) > 10:
                        st.session_state.history.pop()
                    
                    st.rerun()

with col_display:
    st.markdown("### 🎨 Generated Artwork")
    
    if st.session_state.current_image is not None:
        # Display Generated Image
        st.image(
            st.session_state.current_image, 
            caption=f"Generated: {st.session_state.current_prompt[:60]}...", 
            width="stretch"
        )
        
        # Download and Information Panel
        with st.container():
            st.markdown("#### Details")
            st.markdown(f"**Style:** `{st.session_state.current_style}` | **Dimensions:** `{st.session_state.current_size}`")
            st.markdown("**Enhanced Prompt sent to AI:**")
            st.code(st.session_state.current_enhanced, language="text")
            
            # Download Button
            st.download_button(
                label="💾 Download Concept Art",
                data=st.session_state.current_image,
                file_name=f"game_character_{st.session_state.current_style.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png",
                width="stretch"
            )
    else:
        # Placeholder state before any generation
        st.info("💡 Enter your description on the left and click **Generate** to materialize your character concept art here.")
        # Visual placeholder card
        st.markdown(
            """
            <div style="border: 2px dashed #303056; border-radius: 12px; height: 320px; display: flex; align-items: center; justify-content: center; background-color: #111122;">
                <div style="text-align: center; color: #5a5a8a;">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                        <circle cx="8.5" cy="8.5" r="1.5"></circle>
                        <polyline points="21 15 16 10 5 21"></polyline>
                    </svg>
                    <p style="margin-top: 10px; font-weight: 500;">No artwork generated yet</p>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

# PROMPT HISTORY SECTION
st.markdown("---")
st.markdown("### ⏳ Prompt History (Recent 10 Generations)")

if not st.session_state.history:
    st.caption("No characters generated in this session yet.")
else:
    # Display history grid/list
    for idx, item in enumerate(st.session_state.history):
        with st.expander(f"🕒 {item['timestamp']} - {item['style']} - {item['prompt'][:60]}..."):
            h_col1, h_col2 = st.columns([1, 2], gap="medium")
            with h_col1:
                st.image(item["image_bytes"], width="stretch")
            with h_col2:
                st.markdown(f"**Original prompt:** {item['prompt']}")
                st.markdown(f"**Style:** `{item['style']}` | **Size:** `{item['size']}`")
                st.markdown(f"**Full API Prompt:**")
                st.code(item["enhanced_prompt"], language="text")
                st.download_button(
                    label="💾 Download this image",
                    data=item["image_bytes"],
                    file_name=f"history_{item['style'].lower()}_{idx}.png",
                    mime="image/png",
                    key=f"dl_history_{idx}"
                )
