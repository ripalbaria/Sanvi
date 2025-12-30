import requests
import json

# Your specific URLs
M3U_URLS = [
    "https://geefive.saqlainhaider8198.workers.dev/",
    "https://raw.githubusercontent.com/alex8875/m3u/refs/heads/main/jtv.m3u"
]
JSON_URL = "https://raw.githubusercontent.com/mdsarfraj1ali/play/refs/heads/main/Slivtv.json"
OUTPUT_FILE = "playlist.m3u"

def main():
    merged_content = "#EXTM3U\n"
    
    # 1. Process M3U links
    for url in M3U_URLS:
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                # Remove header and add to content
                clean_text = r.text.replace("#EXTM3U", "").strip()
                merged_content += clean_text + "\n"
                print(f"Added M3U from: {url}")
        except Exception as e:
            print(f"Error loading M3U {url}: {e}")

    # 2. Process Slivtv JSON with advanced detection
    try:
        r = requests.get(JSON_URL, timeout=20)
        if r.status_code == 200:
            data = r.json()
            
            # Detect if JSON is a list or a dictionary with a nested list
            channels = []
            if isinstance(data, list):
                channels = data
            elif isinstance(data, dict):
                # Look for common keys where channels are hidden
                for key in ['channels', 'data', 'streams', 'stream', 'list']:
                    if key in data and isinstance(data[key], list):
                        channels = data[key]
                        break
            
            count = 0
            for item in channels:
                if isinstance(item, dict):
                    # Try every possible name for 'name' and 'url'
                    name = item.get("name") or item.get("title") or item.get("channel_name", "Unknown")
                    url = item.get("url") or item.get("link") or item.get("stream_url")
                    logo = item.get("logo") or item.get("image") or item.get("tvg-logo", "")
                    
                    if url and name:
                        merged_content += f'#EXTINF:-1 tvg-logo="{logo}",{name}\n{url}\n'
                        count += 1
            print(f"Successfully added {count} channels from JSON.")
    except Exception as e:
        print(f"Error loading JSON: {e}")

    # 3. Save the final file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(merged_content)

if __name__ == "__main__":
    main()
