# Auto-Content-Creation-NotebookLM: The NotebookLM Content Generation Engine

Turn raw documents, articles, and text files into viral Landscape Explainers and Portrait Shorts using **NotebookLM** automation. 

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

This repository is designed to be fully self-contained, lightweight, and AI-agent friendly. IDEs and coding agents (like Claude Code, Cursor, Copilot) can parse this README and set up the entire workspace autonomously.

---

## 🍿 Demo Output Videos (Click to View)
Actual outputs generated using this engine:
* 📺 **Landscape Explainer Demo:** `demo/explainer_demo.mp4` (~46 MB)
* 📱 **Portrait Short Demo:** `demo/short_demo.mp4` (~4.2 MB)

* 👉 **Support Nextlief Project**: [Watch full demos & support our official site](https://kfcc876.github.io/nextlief)

---

## 📂 Project Structure

- `core/explainer_gen.py`: Triggers landscape video generation.
- `core/explainer_finisher.py`: Monitors generation and downloads the output.
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
2. Install a cookie exporter browser extension (e.g., *Cookie-Editor*).
3. Export cookies as **JSON** format.
4. Save the file into your local project workspace as `config/storage_state.json`.

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

### 2. Portrait Shorts Videos (VNC/Browser Automation)

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
