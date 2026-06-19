# 🎮 AI Game Character Creator

AI Game Character Creator is a production-quality Streamlit web application designed to generate game character concept art using Hugging Face's state-of-the-art text-to-image models. It leverages the powerful **FLUX.1-schnell** model to convert descriptive prompts into detailed, thematic character concept sheets.

The application allows developers, artists, and game designers to quickly prototype character designs in several classic gaming aesthetics (Fantasy, Cyberpunk, Sci-Fi, Medieval, and Anime).

---

## ✨ Features

- **🎮 Style-Conditioned Prompts**: Automatically enhances user-entered prompts with curated atmospheric details, rendering styles, and lighting modifiers according to the selected genre.
- **🖼️ Style Selection**: Support for key gaming visual styles:
  - *Fantasy* (magical settings, armor, digital painting)
  - *Cyberpunk* (neon lights, techwear, cybernetics)
  - *Sci-Fi* (space armor, holograms, futuristic weapons)
  - *Medieval* (gritty realism, chainmail, classical backgrounds)
  - *Anime* (vibrant colors, clean lineart, key visual style)
- **📐 Customizable Resolutions**: Options for 512x512, 768x768, and 1024x1024 images.
- **💡 Random Character Idea Generator**: Sidebar integration providing instant concept prompts (e.g. Shadow Assassin, Desert Mage) to spark creativity.
- **💾 Easy Downloader**: Direct download buttons to save generated concept art as PNG files locally.
- **⏳ Prompt History**: Stores the last 10 generations in a session state panel so users can review prompts, visual results, and redownload historic concept art.
- **🛠️ Demo Mode**: Gracefully falls back to local placeholder graphics if the Hugging Face API token is not specified, allowing immediate evaluation of UI flows.

---

## 🛠️ Architecture and File Structure

```text
ai-game-character-creator/
├── app.py                  # Main Streamlit web application interface
├── requirements.txt        # Package dependencies
├── .env.example            # Configuration variables template
├── .gitignore              # Files ignored by Git
├── README.md               # Project documentation
└── utils/
    ├── constants.py        # Style options, templates, sizes, and random prompt seeds
    ├── image_api.py        # Hugging Face Inference API and local mockup fallback logic
    └── prompt_builder.py   # Style template formatter utility
```

---

## 🚀 Installation & Local Setup

### 1. Prerequisites
- Python 3.11 installed.
- A Hugging Face account and API token. Get yours at [Hugging Face Settings](https://huggingface.co/settings/tokens).

### 2. Clone the Repository
```bash
git clone https://github.com/Rachitgargg/AI_Character_Generator.git
cd AI_Character_Generator
```

### 3. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup Environment Variables
Copy `.env.example` to `.env` and fill in your Hugging Face API key:
```bash
cp .env.example .env
```
Open `.env` and configure your key:
```ini
HF_API_KEY=your_huggingface_api_token_here
```

---

## 🏃 Running the Application

Launch the Streamlit app locally:
```bash
streamlit run app.py
```
This will open the application in your default web browser (usually at `http://localhost:8501`).

---

## 🌐 Deployment Instructions

You can easily deploy this application to **Streamlit Community Cloud**:
1. Push your code to your GitHub repository.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Click **New app**, select the repository (`AI_Character_Generator`), branch (`main`), and main file path (`app.py`).
4. Under **Advanced Settings**, add your environment variables under secrets:
   ```toml
   HF_API_KEY = "your_actual_token_here"
   ```
5. Click **Deploy!**

---

## ⚠️ Known Limitations

- **Rate Limits**: The Hugging Face free Inference API has rate limitations. For heavy usage, consider using a paid token or dedicated endpoints.
- **Cold Start Time**: The model may take 10-20 seconds to load upon the first request or after periods of inactivity.

---

## 🔮 Future Improvements

- Add support for other models like Stable Diffusion 3 or FLUX.1-dev.
- Support negative prompts for more precise image output control.
- Implement an image-to-image feature to iterate on existing characters.
- Add character stats generators based on the generated art.
