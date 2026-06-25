# 🎮 AI Game Character Creator & RPG Workspace

AI Game Character Creator is a premium, production-quality Streamlit creative dashboard designed for game developers, indie studios, and hobbyist worldbuilders. 

It leverages Hugging Face's state-of-the-art **FLUX.1-schnell** text-to-image engine and the **Qwen2.5-7B-Instruct** text-generation model to materialize character concepts, roll RPG stats, and write rich backstories in an all-in-one immersive workspace.

---

## ✨ Features

- **🎨 Glassmorphic SaaS Dashboard**: A beautiful, responsive dark-mode UI with frosted-glass card surfaces, hover lift animations, soft input focus glows, and ambient neon-orange accents.
- **🪄 Character Blueprint Builder**: Dropdown controllers (Class, Accent Color, Environment, and Lighting) that automatically compile a high-fidelity prompt to jumpstart your design.
- **🎲 RPG Attributes Simulator**: Rolls core attributes (Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma) using randomized 3d6 dice. Displays stats in a clean, non-wrapping 2x3 grid.
- **📜 AI Character Lore Generator**: Automatically synthesizes immersive character bios, factions, and special abilities in markdown format. Falls back to smart procedural template generation if serverless endpoints are offline.
- **🖼️ Art Style Conditioning**: Pre-configured thematic prompt modifiers for classic gaming genres:
  - *Fantasy* (magical settings, watercolor digital painting)
  - *Cyberpunk* (neon illumination, techwear, cybernetic details)
  - *Sci-Fi* (nanotech armor, holograms, stellar backgrounds)
  - *Medieval* (chainmail realism, castle ruins, oil-painted lighting)
  - *Anime* (vibrant cel-shading, clean linework, key visual style)
- **💾 Dual Downloader**: Action buttons to download your concept art as a **PNG** image, and your generated backstory bio as a **TXT** file.
- **⭐ Saved Characters Gallery (Favorites)**: Save your favorite syntheses (art, lore, and rolled stats) to a persistent local library card strip.
- **🕒 Recent Generations & Session History**: Quick-load thumbnail strip and collapsible log of the last 10 generations, allowing you to instantly restore previous character drafts back into the workspace.

---

## 🛠️ Architecture and File Structure

```text
ai-game-character-creator/
├── app.py                  # Main Streamlit dashboard interface & CSS styling
├── requirements.txt        # Package dependencies
├── .env.example            # Configuration variables template
├── .gitignore              # Files ignored by Git
├── README.md               # Project documentation
└── utils/
    ├── constants.py        # Style templates, sizes, and random prompt seeds
    ├── image_api.py        # Hugging Face FLUX.1 API & local Pillow mock fallback
    ├── prompt_builder.py   # Prompt-engineering template builder
    └── lore_api.py         # Hugging Face Qwen2.5 API & procedural generator fallback
```

---

## 🚀 Installation & Local Setup

### 1. Prerequisites
- **Python 3.11** installed on your system.
- A Hugging Face account and API token. Get yours at [Hugging Face Settings](https://huggingface.co/settings/tokens).

### 2. Clone the Repository
```bash
git clone https://github.com/Rachitgargg/AI_Character_Generator.git
cd AI_Character_Generator
```

### 3. Create and Activate a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies:

* **macOS / Linux**:
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```
* **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure environment variables
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Open the `.env` file in a text editor and paste your Hugging Face API key:
```ini
HF_API_KEY=hf_your_actual_token_here
```
*Note: If the API key is not configured, the app will run in **Demo Mock Mode**, generating beautiful Pillow vector placeholder art and procedural lore so you can still test the interface.*

---

## 🏃 Running the Application

### Option A: From an Activated Terminal (Recommended)
If you have activated your virtual environment, simply run:
```bash
streamlit run app.py
```

### Option B: Direct Path Execution
If you want to run the application directly without manual activation:
```bash
./venv/bin/streamlit run app.py
```

Once launched, Streamlit will boot the local server and automatically open the dashboard in your default browser at:
👉 **[http://localhost:8501](http://localhost:8501)**

---

## 🌐 Deployment Instructions

You can easily host this application publicly on **Streamlit Community Cloud**:
1. Push your code to your public GitHub repository.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Click **New app**, select this repository, branch (`main`), and set the main file path to `app.py`.
4. Click **Advanced Settings** (next to the deploy button).
5. In the **Secrets** text box, add your API key:
   ```toml
   HF_API_KEY = "hf_your_actual_token_here"
   ```
6. Click **Save** and then click **Deploy!** Streamlit will automatically install dependencies and host your creative workspace on a public URL.
