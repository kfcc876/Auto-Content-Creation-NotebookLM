# Auto-Content-Creation-NotebookLM: The NotebookLM Content Generation Engine

Turn raw documents, articles, and text files into viral Landscape Explainers and Portrait Shorts using **NotebookLM** automation. 

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
* 👉 **Support Nextlief Project**: [Watch full demos & support our official site](https://kfcc876.github.io/nextlief)
* 👉 **Support / Donate via Ko-fi**: [Support on Ko-fi (Ko-fi.com/nextlief)](https://ko-fi.com/nextlief)

---

## 🍿 Demo Output Videos (Click Play to Watch)
Actual outputs generated using this engine:

<h3>📺 Landscape Explainer Video Demo</h3>
<video src="https://github.com/kfcc876/Auto-Content-Creation-NotebookLM/releases/download/media-assets/The_Great_UK_Kebab_Fraud.mp4" controls="controls" width="100%"></video>

<h3>📱 Portrait Shorts Video Demo</h3>
<video src="https://github.com/kfcc876/Auto-Content-Creation-NotebookLM/releases/download/media-assets/The_Great_British_Kebab_Fraud.mp4" controls="controls" width="100%"></video>

* 👉 **Support Nextlief Project**: [Watch full demos & support our official site](https://kfcc876.github.io/nextlief)

---

## 📂 Project Structure

- `core/explainer_gen.py`: Triggers landscape video generation.
- `core/explainer_finisher.py`: Monitors generation and downloads the output.
- `core/uploader_template.py`: Optional multi-platform uploader framework template (YT, FB, IG, TG, DM).
- `automation/pc_playwright.py`: DOM selector-based automation for PC/Linux. (Recommended for AI agents).
- `automation/mobile_xdotool.sh`: Coordinate-based automation for Termux/Mobile environments.
- `automation/calibrate_coords.sh`: Utility to capture screenshots to easily calibrate mobile click positions.
- `templates/hinglish-style-guide.md`: Voice, pacing, and vocabulary template to lock conversational Hinglish audio profile.
- `templates/msd-template.md`: Master Source Document (MSD) data container.

---

## 🚀 Setup Instructions for AI Agents & Developers

### Step 1: Install Dependencies
Install Python dependencies. System packages are required for graphical mobile simulation.
```bash
pip install -r requirements.txt
playwright install firefox
```

*For Termux/Mobile environment system setup:*
```bash
pkg install xdotool imagemagick Xvfb x11vnc firefox
```

### Step 2: Authentication (Google Cookies Setup)
NotebookLM requires browser cookie state to authenticate. Do **not** share your credentials. Instead:
1. Open a browser and log into [NotebookLM](https://notebooklm.google.com).
2. Export cookies as **JSON** format.
3. Save the file into your local project workspace as `config/storage_state.json`.

*🤖 **AI Agent Instruction:** If you are an AI agent setting up this repo, you can launch the browser in non-headless mode, wait for the user to complete login manually, and then programmatically grab the storage/cookie state and dump it to `config/storage_state.json` autonomously.*

---

## 🎬 Running Content Generation

### 1. Landscape Explainer Videos
Copy the configuration template and fill in your target `notebook_id`:
```bash
cp config.json.example config.json
```

Run the pipeline:
1. **Trigger Generation:**
   ```bash
   python core/explainer_gen.py
   ```
2. **Monitor & Download:**
   ```bash
   python core/explainer_finisher.py
   ```

### 3. Optional: Auto-Uploading Generated Videos
If you want to automatically upload generated explainers and shorts directly to YouTube, Facebook, Instagram, Dailymotion, or Telegram:
1. Copy the credentials template to your local path:
   ```bash
   cp config/platform-credentials.json.example config/platform-credentials.json
   ```
2. Populate the keys in `config/platform-credentials.json` (do not commit this file!).
3. Use the uploader module:
   ```bash
   python core/uploader_template.py --video output/your_video.mp4 --title "My Title" --description "SEO text" --platforms youtube,telegram,instagram --is-short
   ```
*Note: This script contains simulation wrappers and integration stubs. Add your own standard SDK calls (like google-api-python-client or Graph API client requests) to make it live for your channel setup.*

---

#### **Method A: PC/Server (DOM Selector Headless)**
Runs out-of-the-box on standard systems using DOM target selectors. Playwright will log in with your storage state and click the correct elements:
```bash
python automation/pc_playwright.py
```
*If a login screen is encountered, run with `--no-headless` to perform manual interactive login in the browser window.*

#### **Method B: Mobile/Termux (Xvfb Coordinates)**
Shorts generation in lightweight mobile shells runs over Xvfb. Since viewport layouts can vary, coordinates can be modified in `config.json`:
1. **Launch displays & script:**
   ```bash
   bash automation/mobile_xdotool.sh
   ```
2. **Calibrate (If clicks miss):**
   Run the calibration helper to take a VNC screenshot and verify coordinates in `output/vnc_calibration.png`:
   ```bash
   bash automation/calibrate_coords.sh
   ```

---

## 📝 Writing & Style Standards

To get high-quality conversational output, always populate your NotebookLM notebooks in this exact source order:
1. **Source #1:** `templates/hinglish-style-guide.md` (Locks voice profile).
2. **Source #2:** `templates/msd-template.md` (Filled with your topic data).
3. **Source #3+:** Research URLs, transcripts, or reference articles.

---

## 🔒 Security & Privacy Notice
`config.json` and `config/storage_state.json` contain active authentication cookies. They are ignored by git via `.gitignore` to prevent leakage. Never commit these files.
