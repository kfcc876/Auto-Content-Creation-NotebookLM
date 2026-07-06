import os
import sys
import json
import asyncio
from pathlib import Path

# Try importing notebooklm, print descriptive guide if missing
try:
    from notebooklm import NotebookLMClient
    from notebooklm.exceptions import AuthError
    from notebooklm.rpc import VideoStyle, VideoFormat
except ImportError:
    print("❌ Error: 'notebooklm-py' is not installed.")
    print("Please install it using: pip install notebooklm-py")
    sys.exit(1)

def load_config():
    config_path = Path("config.json")
    if not config_path.exists():
        config_path = Path("config.json.example")
    
    if not config_path.exists():
        print("❌ Config file not found. Copy config.json.example to config.json and fill details.")
        sys.exit(1)
        
    with open(config_path, "r") as f:
        return json.load(f)

async def main():
    config = load_config()
    
    storage_state = config.get("storage_state_path", "config/storage_state.json")
    notebook_id = config.get("notebook_id")
    output_dir = Path(config.get("output_dir", "output"))
    
    if not notebook_id or notebook_id == "YOUR_NOTEBOOK_ID_HERE":
        print("❌ Please configure a valid 'notebook_id' in config.json")
        sys.exit(1)
        
    if not os.path.exists(storage_state):
        print(f"❌ Storage state (cookies) not found at: {storage_state}")
        print("Please export your cookies and place them at the configured path.")
        print("Check README.md for instructions.")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🔌 Connecting to NotebookLM using storage state: {storage_state}")
    
    try:
        async with NotebookLMClient.from_storage(path=storage_state, timeout=30.0, keepalive=300.0) as client:
            print("✅ Successfully authenticated with NotebookLM Client.")
            
            # Setup generation details
            explainer_cfg = config.get("explainer", {})
            style_str = explainer_cfg.get("style", "ANIME")
            prompt_str = explainer_cfg.get("prompt", "")
            
            # Map string to VideoStyle enum
            video_style = getattr(VideoStyle, style_str, VideoStyle.ANIME)
            
            print(f"🎬 Triggering Landscape Explainer generation on notebook: {notebook_id}")
            print(f"🎨 Visual Style: {style_str}")
            print(f"📝 Prompt: {prompt_str[:120]}...")
            
            # Trigger generation
            artifact = await client.artifacts.generate_video(
                notebook_id=notebook_id,
                prompt=prompt_str,
                video_style=video_style,
                video_format=VideoFormat.EXPLAINER,
                wait=False  # Fire and forget; poll separately to prevent timeouts
            )
            
            print(f"🚀 Generation initiated! Artifact ID: {artifact.id}")
            print("You can poll and download this video using the finisher module or via NotebookLM UI.")
            
    except AuthError as e:
        print(f"🔐 Authentication Error: {e}")
        print("Your session might have expired. Try logging in again and refreshing cookies.")
    except Exception as e:
        print(f"❌ Generation failed: {e}")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
