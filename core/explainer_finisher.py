import os
import sys
import json
import asyncio
import time
from pathlib import Path

try:
    from notebooklm import NotebookLMClient
except ImportError:
    print("❌ Error: 'notebooklm-py' not installed.")
    sys.exit(1)

def load_config():
    config_path = Path("config.json")
    if not config_path.exists():
        config_path = Path("config.json.example")
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
        
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🔌 Connecting to NotebookLM to poll status for notebook: {notebook_id}")
    
    async with NotebookLMClient.from_storage(path=storage_state) as client:
        print("🔍 Polling video artifacts...")
        
        while True:
            artifacts = await client.artifacts.list(notebook_id)
            # Filter for videos
            videos = [a for a in artifacts if a.kind.value in ("video", "VIDEO")]
            
            if not videos:
                print("No video generation tasks found. Waiting 30s...")
                await asyncio.sleep(30)
                continue
                
            # Sort by latest
            videos.sort(key=lambda x: getattr(x, "created_at", 0), reverse=True)
            latest = videos[0]
            
            # Status: 1 = queued, 2 = generating/rendering, 3 = completed
            status = getattr(latest, "status", 0)
            title = getattr(latest, "title", "Untitled Video")
            art_id = latest.id
            
            print(f"📺 Latest video: '{title}' [{art_id}] | Status: {status}")
            
            if status == 3: # Ready
                output_file = output_dir / f"explainer_{int(time.time())}.mp4"
                print(f"⬇️ Video generation complete! Downloading to {output_file}...")
                
                # Download
                await client.artifacts.download_video(
                    notebook_id=notebook_id,
                    artifact_id=art_id,
                    output_path=str(output_file)
                )
                
                # Check file size & resolve potential nested path quirk
                if not output_file.exists() or output_file.stat().st_size < 1000:
                    # Look for nested download paths (notebooklm-py quirk on some platforms)
                    nested_search = list(Path.home().glob(f"**/{output_file.name}"))
                    if nested_search:
                        actual_path = nested_search[0]
                        print(f"🔄 Resolving nested path redirect: {actual_path} -> {output_file}")
                        output_file.write_bytes(actual_path.read_bytes())
                        try:
                            actual_path.unlink()
                        except:
                            pass
                
                print(f"🎉 Download finished! Size: {output_file.stat().st_size / (1024*1024):.2f} MB")
                break
            elif status == 2:
                print("⏳ Rendering is in progress... Waiting 60s.")
            elif status == 1:
                print("⏳ Queued (waiting for compute slot)... Waiting 60s.")
            else:
                print(f"⚠️ Unknown status: {status}. Retrying in 60s.")
                
            await asyncio.sleep(60)

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
