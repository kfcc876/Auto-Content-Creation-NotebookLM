#!/bin/bash
# mobile_xdotool.sh v1 — Mobile/Termux xdotool-based automation.
# Coordinates-based workaround for Termux environments with Xvfb/VNC.

# Exit on any error
set -e

# Load configurations
CONFIG_FILE="config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    CONFIG_FILE="config.json.example"
fi

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Config file not found!"
    exit 1
fi

# Parse configs using python helper
get_config_val() {
    python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('$1', '$2'))"
}

get_coord() {
    python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['shorts_automation']['coordinates']['$1']['$2'])"
}

NOTEBOOK_ID=$(get_config_val "notebook_id" "")
DISPLAY_NUM=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['shorts_automation'].get('vnc_display', ':1'))")
PORT=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['shorts_automation'].get('vnc_port', 5900))")
FIREFOX_PROFILE=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['shorts_automation'].get('firefox_profile_path', ''))")

export DISPLAY=$DISPLAY_NUM

if [ -z "$NOTEBOOK_ID" ] || [ "$NOTEBOOK_ID" = "YOUR_NOTEBOOK_ID_HERE" ]; then
    echo "❌ Please configure a valid 'notebook_id' in config.json"
    exit 1
fi

echo "[Automation] 📱 Starting coordinate-based Shorts automation on Display $DISPLAY_NUM"

# ── 1. Service setup ──────────────────────────────────────────
if ! pgrep -x "Xvfb" > /dev/null; then
    echo "[Automation] 🧹 Cleaning up old locks..."
    pkill -9 -f firefox 2>/dev/null || true
    pkill -9 -f x11vnc 2>/dev/null || true
    pkill -9 -f Xvfb 2>/dev/null || true
    rm -f /tmp/.X1-lock /tmp/.X11-unix/X1
    echo "[Automation] 🖥️ Starting Virtual Display (Xvfb)..."
    Xvfb $DISPLAY_NUM -screen 0 1280x800x24 &
    sleep 2
fi

if ! pgrep -x "x11vnc" > /dev/null; then
    echo "[Automation] 🌐 Starting x11vnc on port $PORT..."
    x11vnc -display $DISPLAY_NUM -rfbport $PORT -forever -shared -nopw &
    sleep 3
fi

# Find profile path
PROFILE_ARG=""
if [ -n "$FIREFOX_PROFILE" ]; then
    PROFILE_ARG="-profile $FIREFOX_PROFILE"
fi

if ! pgrep -x "firefox" > /dev/null; then
    echo "[Automation] 🌐 Launching Firefox to Notebook..."
    firefox $PROFILE_ARG "https://notebooklm.google.com/notebook/$NOTEBOOK_ID" &
    sleep 15
else
    echo "[Automation] 🌐 Firefox already running, opening notebook in new tab..."
    firefox -new-tab "https://notebooklm.google.com/notebook/$NOTEBOOK_ID" 2>/dev/null &
    sleep 12
fi

# ── 2. Click Coordination Sequence ─────────────────────────────
# Coords derived from config
X_ACC=$(get_coord "account_select" "x")
Y_ACC=$(get_coord "account_select" "y")
X_NXT=$(get_coord "login_next" "x")
Y_NXT=$(get_coord "login_next" "y")
X_CRD=$(get_coord "notebook_card_fallback" "x")
Y_CRD=$(get_coord "notebook_card_fallback" "y")
X_STU=$(get_coord "studio_button" "x")
Y_STU=$(get_coord "studio_button" "y")
X_VO=$(get_coord "video_overview" "x")
Y_VO=$(get_coord "video_overview" "y")
X_SHR=$(get_coord "short_format_tab" "x")
Y_SHR=$(get_coord "short_format_tab" "y")
X_GEN=$(get_coord "generate_button" "x")
Y_GEN=$(get_coord "generate_button" "y")

# Auto-login sequence (in case login page is visible)
echo "[Automation] 🔐 Attempting auto-login fallback..."
xdotool mousemove $X_ACC $Y_ACC click 1
sleep 1
xdotool key Return
sleep 5
xdotool mousemove $X_NXT $Y_NXT click 1
sleep 10

# List page fallback (if direct navigation redirected to home)
echo "[Automation] Fallback card click (if on list page)..."
xdotool mousemove $X_CRD $Y_CRD click 1
sleep 8

# Studio activation
echo "[Automation] 🎬 Clicking Studio..."
xdotool mousemove $X_STU $Y_STU click 1
sleep 5

# Video Overview (Direct click)
echo "[Automation] 📺 Clicking Video Overview..."
xdotool mousemove $X_VO $Y_VO click 1
sleep 5

# Select format tab
echo "[Automation] 📱 Selecting Short Video format..."
xdotool mousemove $X_SHR $Y_SHR click 1
sleep 3

# Trigger Gen
echo "[Automation] 🟢 Triggering Shorts Generation..."
xdotool mousemove $X_GEN $Y_GEN click 1
sleep 5

echo "[Automation] ✅ Short Video Generation triggered successfully!"
exit 0
