#!/bin/bash
# calibrate_coords.sh
# Utility to capture screenshots inside Termux VNC sessions to easily verify / retrieve pixel coordinates.

DISPLAY_NUM=$(python3 -c "import json; print(json.load(open('config.json')).get('shorts_automation', {}).get('vnc_display', ':1'))" 2>/dev/null || echo ":1")
export DISPLAY=$DISPLAY_NUM
OUT_FILE="output/vnc_calibration.png"

mkdir -p output

if ! pgrep -x "Xvfb" > /dev/null; then
    echo "❌ Error: Xvfb is not running on Display $DISPLAY_NUM."
    echo "Run the automation script first to launch the browser and display servers."
    exit 1
fi

echo "📸 Taking screenshot of display $DISPLAY_NUM..."
if command -v import &> /dev/null; then
    import -window root "$OUT_FILE"
    echo "✅ Screenshot saved to $OUT_FILE"
    echo "Please open this file using a VNC Viewer or file manager to verify UI positions."
elif command -v scrot &> /dev/null; then
    scrot "$OUT_FILE"
    echo "✅ Screenshot saved to $OUT_FILE"
else
    echo "❌ Neither 'import' (imagemagick) nor 'scrot' is installed."
    echo "Please install imagemagick: pkg install imagemagick"
fi
