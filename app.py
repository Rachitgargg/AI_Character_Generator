import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

# Import utilities
from utils.constants import STYLES, IMAGE_SIZES, RANDOM_CHARACTER_IDEAS, DEFAULT_MODEL
from utils.prompt_builder import build_prompt
from utils.image_api import generate_image
from utils.lore_api import generate_lore


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
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root colors and global typography */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0d0c0a !important;
        color: #f5f1ea !important;
    }
    
    /* Target the main container app view */
    [data-testid="stAppViewContainer"] {
        background-color: #0d0c0a;
        background-image: radial-gradient(circle at 50% 0%, rgba(245, 158, 11, 0.08) 0%, transparent 50%),
                          radial-gradient(circle at 0% 100%, rgba(234, 88, 12, 0.05) 0%, transparent 40%);
        background-attachment: fixed;
    }
    
    /* Main layout container constraint */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 1400px !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
    }
    
    /* Target Sidebar */
    [data-testid="stSidebar"] {
        background-color: #141210 !important;
        border-right: 1px solid #2e2620 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 1rem;
    }
    
    /* Headings styling */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Sora', sans-serif !important;
        color: #f5f1ea !important;
    }
    
    h3 {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        margin-bottom: 12px !important;
        letter-spacing: -0.025em !important;
    }
    
    .main-title {
        font-family: 'Sora', sans-serif;
        font-weight: 800;
        background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        margin-bottom: 0.1rem;
        letter-spacing: -0.03em;
    }
    
    .subtitle {
        color: #a39a8c;
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
        font-weight: 400;
    }

    /* SaaS Description Styling */
    .project-description {
        color: #a39a8c;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 1.2rem;
        max-width: 900px;
    }
    
    /* Premium Card Container Styling with Glassmorphism & Hover Lift */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(26, 23, 20, 0.75) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(245, 158, 11, 0.15) !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.5) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        padding: 1.5rem !important;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(245, 158, 11, 0.35) !important;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6), 0 0 20px rgba(245, 158, 11, 0.08) !important;
        transform: translateY(-3px) !important;
    }
    
    /* Inputs Styling (TextArea, SelectBox, etc.) with Focus Glow */
    textarea, [data-testid="stSelectbox"] div[role="combobox"], [data-testid="stTextInput"] input {
        background-color: #0d0c0a !important;
        color: #f5f1ea !important;
        border: 1px solid #3a322a !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    textarea::placeholder {
        color: #6b6358 !important;
    }

    /* Hover effect on dropdowns/inputs */
    [data-testid="stSelectbox"] div[role="combobox"]:hover, textarea:hover, [data-testid="stTextInput"] input:hover {
        border-color: rgba(245, 158, 11, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    
    textarea:focus, [data-testid="stSelectbox"] div[role="combobox"]:focus-within, [data-testid="stTextInput"] input:focus {
        border-color: #f59e0b !important;
        box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.2) !important;
        outline: none !important;
        transform: translateY(0px) !important;
    }
    
    /* Primary Gradient Button (Generate) with Pulse Glow */
    [data-testid="baseButton-primary"], div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #f59e0b 0%, #ea580c 100%) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 600 !important;
        font-family: 'Sora', sans-serif !important;
        border-radius: 8px !important;
        padding: 0.65rem 2rem !important;
        transition: all 0.25s ease !important;
        width: 100% !important;
        height: auto !important;
        animation: generate-pulse 2s infinite alternate !important;
    }
    
    [data-testid="baseButton-primary"]:hover, div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #fbbf24 0%, #f97316 100%) !important;
        animation: none !important;
        box-shadow: 0 8px 25px rgba(234, 88, 12, 0.45), 0 0 15px rgba(245, 158, 11, 0.2) !important;
        transform: translateY(-2px) !important;
    }
    
    [data-testid="baseButton-primary"]:active, div.stButton > button[kind="primary"]:active {
        transform: translateY(1px) !important;
        box-shadow: 0 4px 10px rgba(234, 88, 12, 0.3) !important;
    }

    @keyframes generate-pulse {
        0% {
            box-shadow: 0 4px 12px rgba(234, 88, 12, 0.2), 0 0 0 0px rgba(245, 158, 11, 0.1);
        }
        100% {
            box-shadow: 0 4px 20px rgba(234, 88, 12, 0.45), 0 0 0 6px rgba(245, 158, 11, 0.35);
        }
    }
    
    /* Secondary Action Button Styling */
    [data-testid="baseButton-secondary"] {
        background-color: #0d0c0a !important;
        color: #a39a8c !important;
        border: 1px solid #3a322a !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="baseButton-secondary"]:hover {
        color: #ffffff !important;
        border-color: #f59e0b !important;
        background-color: rgba(245, 158, 11, 0.05) !important;
        transform: translateY(-1px);
    }
    
    /* Expander / Accordion styling */
    [data-testid="stExpander"] {
        background-color: rgba(26, 23, 20, 0.75) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid #2e2620 !important;
        border-radius: 10px !important;
        overflow: hidden;
        transition: all 0.25s ease !important;
    }
    
    [data-testid="stExpander"]:hover {
        background-color: rgba(33, 28, 23, 0.85) !important;
        border-color: rgba(245, 158, 11, 0.25) !important;
        transform: translateY(-1px);
    }
    
    [data-testid="stExpander"] summary {
        font-weight: 600 !important;
        color: #a39a8c !important;
        padding: 10px 14px !important;
        transition: color 0.2s ease !important;
    }
    
    [data-testid="stExpander"] summary:hover {
        color: #f5f1ea !important;
    }
    
    /* Styled tags/badges (Consistently warm amber-orange pill) */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        text-transform: uppercase;
        margin-right: 6px;
        background: rgba(245, 158, 11, 0.15) !important;
        color: #f59e0b !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
    }
    
    .badge-fantasy, .badge-cyberpunk, .badge-scifi, .badge-medieval, .badge-anime {
        background: rgba(245, 158, 11, 0.15) !important;
        color: #f59e0b !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
    }
    
    /* Details Table Styling */
    .info-table {
        width: 100%;
        border-collapse: collapse;
        border: 1px solid #2e2620;
        border-radius: 8px;
        overflow: hidden;
        margin-top: 10px;
        margin-bottom: 15px;
        background-color: #161310;
    }
    .info-table tr {
        background-color: #161310;
        transition: background-color 0.2s ease;
    }
    .info-table tr:nth-child(even) {
        background-color: #1c1813;
    }
    .info-table tr:hover {
        background-color: rgba(245, 158, 11, 0.06);
    }
    .info-table td {
        padding: 10px 14px;
        border-bottom: 1px solid #2e2620;
        font-size: 0.85rem;
    }
    .info-table td.label {
        color: #a39a8c;
        font-weight: 500;
        width: 40%;
    }
    .info-table td.value {
        color: #f5f1ea;
        font-family: 'Inter', sans-serif;
    }
    
    /* Code block background */
    code {
        background-color: #0d0c0a !important;
        border: 1px solid #2e2620 !important;
        color: #f59e0b !important;
    }
    
    /* Image Frame & Shadow */
    [data-testid="stImage"] img {
        border-radius: 12px !important;
        border: 1px solid #2e2620 !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6) !important;
        transition: all 0.3s ease !important;
        padding: 14px !important;
        background-color: #0d0c0a !important;
        animation: fadeIn 0.4s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Favorites Grid */
    .fav-card {
        background-color: #1a1714;
        border: 1px solid #2e2620;
        border-radius: 12px;
        padding: 10px;
        transition: all 0.2s ease;
    }
    .fav-card:hover {
        border-color: #f59e0b;
        transform: translateY(-2px);
    }

    /* Glowing tag/pill tag in the sidebar logo block */
    .side-pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.65rem;
        font-weight: 700;
        background: rgba(245, 158, 11, 0.15) !important;
        border: 1px solid rgba(245, 158, 11, 0.35) !important;
        color: #f59e0b !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        line-height: 1;
        animation: pill-glow 2s infinite alternate !important;
    }
    @keyframes pill-glow {
        0% {
            box-shadow: 0 0 4px rgba(245, 158, 11, 0.2);
            border-color: rgba(245, 158, 11, 0.35);
        }
        100% {
            box-shadow: 0 0 12px rgba(245, 158, 11, 0.5);
            border-color: rgba(245, 158, 11, 0.6);
        }
    }

    /* Dashboard Stat Chips layout */
    .stat-container {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 2rem;
        margin-top: 0.5rem;
    }
    .stat-chip {
        background: rgba(26, 23, 20, 0.65);
        border: 1px solid rgba(46, 38, 32, 0.6);
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 0.8rem;
        color: #a39a8c;
        display: flex;
        align-items: center;
        gap: 6px;
        transition: all 0.25s ease;
        backdrop-filter: blur(8px);
    }
    .stat-chip:hover {
        border-color: rgba(245, 158, 11, 0.3);
        color: #f5f1ea;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
    }
    .stat-chip strong {
        color: #f59e0b;
    }

    /* Silhouette / empty-state animations */
    .rotating-ring {
        transform-origin: center;
        animation: rotate-ring 12s linear infinite;
    }
    @keyframes rotate-ring {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    .shimmering-avatar {
        animation: avatar-pulse 3s ease-in-out infinite alternate;
    }
    @keyframes avatar-pulse {
        0% {
            opacity: 0.45;
            filter: drop-shadow(0 0 2px rgba(245, 158, 11, 0.15));
        }
        100% {
            opacity: 0.95;
            filter: drop-shadow(0 0 15px rgba(245, 158, 11, 0.6));
        }
    }
    .empty-state-card {
        border: 1px dashed rgba(245, 158, 11, 0.25) !important;
        border-radius: 16px !important;
        height: 380px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: rgba(26, 23, 20, 0.4) !important;
        backdrop-filter: blur(8px);
        box-shadow: inset 0 4px 20px rgba(0, 0, 0, 0.5) !important;
        transition: all 0.3s ease;
    }
    .empty-state-card:hover {
        border-color: rgba(245, 158, 11, 0.45) !important;
        box-shadow: inset 0 4px 20px rgba(0, 0, 0, 0.6), 0 0 15px rgba(245, 158, 11, 0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session States
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "trigger_regeneration" not in st.session_state:
    st.session_state.trigger_regeneration = False

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
if "current_lore" not in st.session_state:
    st.session_state.current_lore = ""
if "current_rpg_stats" not in st.session_state:
    st.session_state.current_rpg_stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
if "rpg_stats" not in st.session_state:
    st.session_state.rpg_stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}


def randomize_prompt():
    import random
    st.session_state.prompt_input = random.choice(RANDOM_CHARACTER_IDEAS)


# HEADER SECTION
st.markdown("""
<div style="display: flex; align-items: center; gap: 14px; margin-bottom: 0.1rem; padding-top: 10px;">
    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 0 8px rgba(245, 158, 11, 0.35));">
        <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="url(#header-grad)" stroke="#f59e0b" stroke-width="1.5" stroke-linejoin="round"/>
        <path d="M2 17L12 22L22 17" stroke="#ea580c" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M2 12L12 17L22 12" stroke="#f59e0b" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        <defs>
            <linearGradient id="header-grad" x1="2" y1="2" x2="22" y2="12" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#f59e0b" />
                <stop offset="100%" stop-color="#ea580c" />
            </linearGradient>
        </defs>
    </svg>
    <h1 class='main-title' style='margin: 0; padding: 0;'>AI Game Character Creator</h1>
</div>
""", unsafe_allow_html=True)
st.markdown("<p class='project-description'>Forge details, design visual concepts, and generate rich character backstories in an all-in-one creative dashboard. Powered by the state-of-the-art <b>FLUX.1-schnell</b> engine, this workspace is designed for game developers, indie studios, and hobbyist worldbuilders to materialize ideas into production-ready visual assets.</p>", unsafe_allow_html=True)

# Dashboard Stat Chips Row
st.markdown("""
<div class="stat-container">
    <div class="stat-chip">🚀 Powered by <strong>FLUX.1-schnell</strong></div>
    <div class="stat-chip">🔥 <strong>1.2k+</strong> Characters Created</div>
    <div class="stat-chip">🎮 <strong>Indie Studio</strong> Ready</div>
    <div class="stat-chip">🎨 <strong>5 Art</strong> Archetypes</div>
</div>
""", unsafe_allow_html=True)

# SIDEBAR CONFIGURATION
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding-top: 15px; margin-bottom: 12px;">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 0 10px rgba(245, 158, 11, 0.3)); margin-bottom: 6px;">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" fill="url(#side-logo-grad)" stroke="#f59e0b" stroke-width="1.5" stroke-linejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="#ea580c" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="#f59e0b" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <defs>
                <linearGradient id="side-logo-grad" x1="2" y1="2" x2="22" y2="12" gradientUnits="userSpaceOnUse">
                    <stop offset="0%" stop-color="#f59e0b" />
                    <stop offset="100%" stop-color="#ea580c" />
                </linearGradient>
            </defs>
        </svg>
        <h3 style="font-family: 'Sora', sans-serif; font-weight: 800; font-size: 1.15rem; margin: 4px 0 2px 0; letter-spacing: 0.05em; color: #f5f1ea; line-height: 1.2;">CHARACTER LAB</h3>
        <p style="font-size: 0.72rem; color: #a39a8c; margin: 0 0 10px 0; font-style: italic; line-height: 1.3;">Materialize your imagination into production-ready assets.</p>
        <span class="side-pill">Visual Gen Core</span>
    </div>
    """, unsafe_allow_html=True)



    
    st.markdown("### 🛠️ Configuration")
    
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
    with st.expander("💡 Need Inspiration?"):
        st.markdown("<p style='font-size: 0.8rem; color: #94a3b8; line-height: 1.4; margin-bottom: 12px;'>Generate a randomized character concept prompt to kickstart your creative workflow.</p>", unsafe_allow_html=True)
        st.button("🎲 Generate Random Idea", on_click=randomize_prompt, width="stretch")
    
    # 4. Project Information
    with st.expander("ℹ️ Core Engine Info"):
        st.markdown(f"<p style='font-size: 0.85rem; margin-bottom: 8px;'><b>AI Model:</b> <code>{DEFAULT_MODEL}</code></p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.85rem; margin-bottom: 12px;'><b>Framework:</b> Streamlit + Python 3.11</p>", unsafe_allow_html=True)
        
        # API Credentials Status indicator
        if not api_key:
            st.warning("⚠️ HF_API_KEY is not configured in `.env`. Running in Demo Mock Mode.")
        else:
            st.success("🔑 Hugging Face API key active.")


# MAIN CONTENT AREA
col_input, col_display = st.columns([5, 4], gap="large")


with col_input:
    with st.container(border=True):
        st.markdown("### 📝 Define Your Character")
        
        # Text Area for Character Description
        user_prompt = st.text_area(
            "Character Description:",
            value=st.session_state.prompt_input,
            placeholder="Describe your character in detail (e.g., 'A stealthy dark elf rogue hiding in the shadows holding twin glowing daggers')...",
            height=150,
            help="Specify features like gender, race, equipment, armor, pose, colors, and background scenery."
        )
        st.session_state.prompt_input = user_prompt
        
        # Highlight chosen style badge
        badge_class = f"badge-{selected_style.lower()}"
        st.markdown(f"Active Theme Modifier: <span class='badge {badge_class}'>{selected_style}</span>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Generate Button
        generate_clicked = st.button("🚀 Generate Character concept art", type="primary", width="stretch")
        
        # Check both the primary generate button and the trigger_regeneration flag
        if generate_clicked or st.session_state.trigger_regeneration:
            # Determine which values to use
            if generate_clicked:
                prompt_to_use = user_prompt
                style_to_use = selected_style
                size_to_use = selected_size
            else:
                prompt_to_use = st.session_state.current_prompt
                style_to_use = st.session_state.current_style
                size_to_use = st.session_state.current_size
            
            # Reset flag
            st.session_state.trigger_regeneration = False
            
            if not prompt_to_use.strip():
                st.warning("⚠️ Please provide a character description or generate a random idea first.")
            else:
                final_prompt = build_prompt(prompt_to_use, style_to_use)
                
                with st.spinner("🧙‍♂️ Generating art with FLUX.1 and writing character lore..."):
                    # Call Image API
                    img_bytes, error_msg = generate_image(final_prompt, size_to_use, api_key)
                    
                    if error_msg:
                        st.error(f"❌ Generation failed: {error_msg}")
                    elif img_bytes:
                        # Call Lore API
                        lore_text = generate_lore(prompt_to_use, style_to_use, api_key)
                        
                        st.session_state.current_image = img_bytes
                        st.session_state.current_prompt = prompt_to_use
                        st.session_state.current_enhanced = final_prompt
                        st.session_state.current_style = style_to_use
                        st.session_state.current_size = size_to_use
                        st.session_state.current_lore = lore_text
                        st.session_state.current_rpg_stats = st.session_state.rpg_stats.copy()
                        
                        # Store in History
                        history_entry = {
                            "prompt": prompt_to_use,
                            "enhanced_prompt": final_prompt,
                            "style": style_to_use,
                            "size": size_to_use,
                            "timestamp": datetime.now().strftime("%I:%M:%S %p"),
                            "image_bytes": img_bytes,
                            "lore": lore_text,
                            "rpg_stats": st.session_state.rpg_stats.copy()
                        }
                        st.session_state.history.insert(0, history_entry)
                        if len(st.session_state.history) > 10:
                            st.session_state.history.pop()
                        st.rerun()

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 🪄 Character Blueprint Builder")
        st.markdown("<p style='font-size: 0.8rem; color: #a39a8c; margin-top: -8px; margin-bottom: 12px;'>Choose attributes to automatically assemble a high-fidelity description prompt.</p>", unsafe_allow_html=True)
        
        b_col1, b_col2 = st.columns(2, gap="small")
        with b_col1:
            char_class = st.selectbox(
                "Archetype Class:",
                options=["Knight / Warrior", "Mage / Spellcaster", "Rogue / Assassin", "Ranger / Archer", "Cyber-Ninja", "Bio-Mech Soldier"],
                index=0,
                key="blueprint_class"
            )
            visual_color = st.selectbox(
                "Accent Color Theme:",
                options=["Sunlight Gold", "Volcanic Crimson", "Ethereal Cyan", "Shadow Purple", "Bio-Green", "Crimson Amber"],
                index=2,
                key="blueprint_color"
            )
        with b_col2:
            environment = st.selectbox(
                "Environment Background:",
                options=["Mystic Forest Glow", "High-Tech Cyberpunk Alley", "Ancient Runed Dungeon", "Volcanic Throne Room", "Desolate Alien Desert", "Astral Nebula Plane"],
                index=0,
                key="blueprint_env"
            )
            lighting = st.selectbox(
                "Lighting / Mood:",
                options=["Volumetric Cinematic Rays", "Moody Dark Chiaroscuro", "Neon Synthwave Glow", "Dramatic Rim Lighting", "Golden Hour Sunset"],
                index=0,
                key="blueprint_light"
            )
            
        if st.button("🪄 Assemble Blueprint & Write Prompt", key="assemble_blueprint", width="stretch"):
            constructed = f"A legendary {char_class.lower()} wearing detailed armor with {visual_color.lower()} glowing accents, standing in a {environment.lower()}, shot with {lighting.lower()}, masterpiece concept art."
            st.session_state.prompt_input = constructed
            st.rerun()

        st.markdown("<hr style='margin: 12px 0; border: 0; border-top: 1px solid rgba(245, 158, 11, 0.15);'>", unsafe_allow_html=True)
        st.markdown("##### 🎲 Attributes Simulator")
        
        r1_col1, r1_col2, r1_col3 = st.columns(3, gap="small")
        st.markdown("<div style='margin-top: 6px;'></div>", unsafe_allow_html=True)
        r2_col1, r2_col2, r2_col3 = st.columns(3, gap="small")
        s_cols = [r1_col1, r1_col2, r1_col3, r2_col1, r2_col2, r2_col3]
        stats_keys = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        
        for idx, key in enumerate(stats_keys):
            with s_cols[idx]:
                st.markdown(f"<div style='text-align: center; background: rgba(245, 158, 11, 0.05); border: 1px solid rgba(245, 158, 11, 0.2); border-radius: 6px; padding: 6px 4px;'>"
                            f"<div style='font-size: 0.72rem; color: #a39a8c; font-weight: bold;'>{key}</div>"
                            f"<div style='font-size: 1.25rem; color: #f59e0b; font-weight: 800; margin-top: 2px;'>{st.session_state.rpg_stats[key]}</div>"
                            f"</div>", unsafe_allow_html=True)
                            
        if st.button("🎲 Roll Attributes", key="roll_stats", width="stretch"):
            import random
            st.session_state.rpg_stats = {k: sum(random.randint(1, 6) for _ in range(3)) for k in stats_keys}
            st.toast("Attributes rolled! 🎲")
            st.rerun()

with col_display:

    with st.container(border=True):
        st.markdown("### 🎨 Generated Artwork")
        
        if st.session_state.current_image is not None:
            # Display Generated Image (styled with padding inside via CSS)
            st.image(
                st.session_state.current_image, 
                width="stretch"
            )
        else:
            # Polished empty state with dynamic animated SVG silhouette
            st.markdown("""
            <div class="empty-state-card">
                <div style="text-align: center; color: #a39a8c; padding: 20px; display: flex; flex-direction: column; align-items: center;">
                    <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-bottom: 16px;">
                        <defs>
                            <linearGradient id="shimmer-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#3a322a" />
                                <stop offset="50%" stop-color="#f59e0b" />
                                <stop offset="100%" stop-color="#3a322a" />
                            </linearGradient>
                            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                                <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
                                <feMerge>
                                    <feMergeNode in="coloredBlur"/>
                                    <feMergeNode in="SourceGraphic"/>
                                </feMerge>
                            </filter>
                        </defs>
                        <!-- Background ring -->
                        <circle cx="50" cy="50" r="42" stroke="rgba(245, 158, 11, 0.15)" stroke-width="1.5" fill="none" />
                        <!-- Glowing rotating ring -->
                        <circle cx="50" cy="50" r="42" stroke="url(#shimmer-grad)" stroke-width="2" fill="none" filter="url(#glow)" class="rotating-ring" />
                        <!-- Shimmering hero avatar silhouette -->
                        <path d="M50 22 C43 22 37 28 37 36 C37 42 40 47 45 50 C35 54 29 63 29 74 C29 76 31 78 33 78 L67 78 C69 78 71 76 71 74 C71 63 65 54 55 50 C60 47 63 42 63 36 C63 28 57 22 50 22 Z" fill="url(#shimmer-grad)" filter="url(#glow)" class="shimmering-avatar" />
                    </svg>
                    <h4 style="color: #f5f1ea; font-family: 'Sora', sans-serif; font-size: 1.15rem; margin-bottom: 8px; font-weight: 700;">Awaiting Concept Art</h4>
                    <p style="font-size: 0.85rem; max-width: 280px; margin: 0 auto; line-height: 1.45; color: #a39a8c;">Enter a description, pick a visual theme, and click generate to materialize your hero.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Details, actions, and lore card (only if image is generated)
    if st.session_state.current_image is not None:
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("### 📋 Character Details & Actions")
            
            # Action Toolbar columns (4 columns)
            t_col1, t_col2, t_col3, t_col4 = st.columns(4, gap="small")
            with t_col1:
                st.download_button(
                    label="🖼️ PNG",
                    data=st.session_state.current_image,
                    file_name=f"character_{st.session_state.current_style.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png",
                    width="stretch",
                    key="dl_main"
                )
            with t_col2:
                st.download_button(
                    label="📜 Lore",
                    data=st.session_state.current_lore,
                    file_name=f"lore_{st.session_state.current_style.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    width="stretch",
                    key="dl_lore"
                )
            with t_col3:
                if st.button("🔁 Regen", key="regen_main", width="stretch"):
                    st.session_state.trigger_regeneration = True
                    st.rerun()
            with t_col4:
                # Check favorited
                is_fav = False
                for fav in st.session_state.favorites:
                    if fav["image_bytes"] == st.session_state.current_image:
                        is_fav = True
                        break
                        
                fav_label = "❤️ Unsave" if is_fav else "⭐ Save"
                if st.button(fav_label, key="fav_main", width="stretch"):
                    if is_fav:
                        st.session_state.favorites = [f for f in st.session_state.favorites if f["image_bytes"] != st.session_state.current_image]
                        st.toast("Removed from Saved Characters!")
                    else:
                        fav_entry = {
                            "prompt": st.session_state.current_prompt,
                            "enhanced_prompt": st.session_state.current_enhanced,
                            "style": st.session_state.current_style,
                            "size": st.session_state.current_size,
                            "timestamp": datetime.now().strftime("%I:%M:%S %p"),
                            "image_bytes": st.session_state.current_image,
                            "lore": st.session_state.current_lore,
                            "rpg_stats": st.session_state.current_rpg_stats.copy()
                        }
                        st.session_state.favorites.append(fav_entry)
                        st.toast("Added to Saved Characters! 🌟")
                    st.rerun()
            
            # Metadata Table and Details Card
            st.markdown(f"""
            <table class="info-table">
                <tr>
                    <td class="label">Style Theme</td>
                    <td class="value">{st.session_state.current_style}</td>
                </tr>
                <tr>
                    <td class="label">Resolution</td>
                    <td class="value">{st.session_state.current_size}</td>
                </tr>
                <tr>
                    <td class="label">AI Model</td>
                    <td class="value">FLUX.1-schnell</td>
                </tr>
                <tr>
                    <td class="label">Status</td>
                    <td class="value" style="color: #10b981; font-weight: bold;">✓ Synthesized</td>
                </tr>
            </table>
            """, unsafe_allow_html=True)
            
            # RPG Stats Display
            st.markdown("#### 🎲 Character Attributes Sheet")
            r1_col1, r1_col2, r1_col3 = st.columns(3, gap="small")
            st.markdown("<div style='margin-top: 6px;'></div>", unsafe_allow_html=True)
            r2_col1, r2_col2, r2_col3 = st.columns(3, gap="small")
            s_cols = [r1_col1, r1_col2, r1_col3, r2_col1, r2_col2, r2_col3]
            stats_keys = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
            for idx, key in enumerate(stats_keys):
                with s_cols[idx]:
                    st.markdown(f"<div style='text-align: center; background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 8px; padding: 8px 6px;'>"
                                f"<div style='font-size: 0.75rem; color: #a39a8c; font-weight: bold; letter-spacing: 0.05em;'>{key}</div>"
                                f"<div style='font-size: 1.35rem; color: #f59e0b; font-weight: 800; margin-top: 2px;'>{st.session_state.current_rpg_stats.get(key, 10)}</div>"
                                f"</div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            
            # Character Lore Panel
            if st.session_state.current_lore:
                st.markdown("#### 📜 Generated Backstory")
                st.markdown(st.session_state.current_lore)
            
            # Prompts display
            st.markdown("#### 📝 Prompts Details")
            st.markdown("**Original Description:**")
            st.code(st.session_state.current_prompt, language="text")
            
            st.markdown("**Enhanced Prompt sent to AI Model:**")
            st.code(st.session_state.current_enhanced, language="text")

    # Recent Generations thumbnail strip (occupies empty space productively)
    if st.session_state.history:
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("### 🕒 Recent Generations")
            st.markdown("<p style='font-size: 0.8rem; color: #94a3b8; margin-top: -8px; margin-bottom: 12px;'>Click any thumbnail below to instantly load that character draft back into the workspace.</p>", unsafe_allow_html=True)
            
            recent_items = st.session_state.history[:4]
            cols_hist = st.columns(4, gap="small")
            for idx, item in enumerate(recent_items):
                with cols_hist[idx]:
                    st.image(item["image_bytes"], width="stretch")
                    if st.button("👁️ Load", key=f"quick_hist_{idx}", width="stretch"):
                        st.session_state.current_image = item["image_bytes"]
                        st.session_state.current_prompt = item["prompt"]
                        st.session_state.current_enhanced = item["enhanced_prompt"]
                        st.session_state.current_style = item["style"]
                        st.session_state.current_size = item["size"]
                        st.session_state.current_lore = item.get("lore", "")
                        st.session_state.current_rpg_stats = item.get("rpg_stats", {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10})
                        st.session_state.rpg_stats = st.session_state.current_rpg_stats.copy()
                        st.rerun()


# SAVED CHARACTERS / FAVORITES GALLERY
if st.session_state.favorites:
    st.markdown("---")
    st.markdown("### ⭐ Saved Characters Gallery")
    
    # Grid of favorites
    cols = st.columns(4, gap="medium")
    for idx, fav in enumerate(st.session_state.favorites):
        col_idx = idx % 4
        with cols[col_idx]:
            # Custom container card
            st.markdown(f"""
            <div class="fav-card">
                <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 6px; display: flex; justify-content: space-between;">
                    <span style="font-weight: 600; color: #00F2FE;">{fav['style']}</span>
                    <span>{fav['timestamp']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.image(fav["image_bytes"], width="stretch")
            st.markdown(f"<p style='font-size: 0.85rem; line-height: 1.4; color: #cbd5e1; margin: 8px 0;'>{fav['prompt'][:45]}...</p>", unsafe_allow_html=True)
            
            f_col1, f_col2, f_col3 = st.columns([2, 2, 1], gap="small")
            with f_col1:
                st.download_button(
                    label="🖼️ PNG",
                    data=fav["image_bytes"],
                    file_name=f"favorite_{fav['style'].lower()}_{idx}.png",
                    mime="image/png",
                    key=f"dl_fav_{idx}",
                    width="stretch"
                )
            with f_col2:
                st.download_button(
                    label="📜 Lore",
                    data=fav.get("lore", "No lore recorded."),
                    file_name=f"favorite_lore_{fav['style'].lower()}_{idx}.txt",
                    mime="text/plain",
                    key=f"dl_fav_lore_{idx}",
                    width="stretch"
                )
            with f_col3:
                if st.button("🗑️", key=f"del_fav_{idx}", width="stretch", help="Remove from saved list"):
                    st.session_state.favorites.pop(idx)
                    st.toast("Removed from Saved Characters!")
                    st.rerun()


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
                
                h_btn_col1, h_btn_col2 = st.columns(2, gap="small")
                with h_btn_col1:
                    st.download_button(
                        label="💾 Download",
                        data=item["image_bytes"],
                        file_name=f"history_{item['style'].lower()}_{idx}.png",
                        mime="image/png",
                        key=f"dl_history_{idx}",
                        width="stretch"
                    )
                with h_btn_col2:
                    if st.button("👁️ Load into View", key=f"load_history_{idx}", width="stretch"):
                        st.session_state.current_image = item["image_bytes"]
                        st.session_state.current_prompt = item["prompt"]
                        st.session_state.current_enhanced = item["enhanced_prompt"]
                        st.session_state.current_style = item["style"]
                        st.session_state.current_size = item["size"]
                        st.session_state.current_lore = item.get("lore", "")
                        st.session_state.current_rpg_stats = item.get("rpg_stats", {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10})
                        st.session_state.rpg_stats = st.session_state.current_rpg_stats.copy()
                        st.rerun()


