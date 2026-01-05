import requests
import json

# Your URLs
M3U_URLS = [
    "https://raw.githubusercontent.com/alex8875/m3u/refs/heads/main/z5.m3u",
    "https://raw.githubusercontent.com/alex8875/m3u/refs/heads/main/jtv.m3u"
]
JSON_URL = "https://raw.githubusercontent.com/ripalbaria/play/refs/heads/main/Slivtv.json"
OUTPUT_FILE = "playlist.m3u"

def main():
    merged_content = ["#EXTM3U"]
    
    # 1. Quickly grab M3U files
    for url in M3U_URLS:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                # Filter out the header and add lines
                lines = [line for line in r.text.splitlines() if line.strip() and not line.startswith("#EXTM3U")]
                merged_content.extend(lines)
        except:
            print(f"Skipping M3U: {url}")

    # 2. Fast-parse the JSON file
    try:
        r = requests.get(JSON_URL, timeout=10)
        if r.status_code == 200:
            data = r.json()
            # If the JSON is a list of channels, process it directly
            channels = data if isinstance(data, list) else data.get("channels", [])
            
            for item in channels:
                name = item.get("name") or item.get("title")
                link = item.get("url") or item.get("link")
                logo = item.get("logo") or ""
                
                if name and link:
                    merged_content.append(f'#EXTINF:-1 tvg-logo="{logo}",{name}')
                    merged_content.append(link)
    except Exception as e:
        print(f"JSON error: {e}")

    # 3. Write all at once (fastest I/O)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_content))
    print("Done! Playlist created fast.")

if __name__ == "__main__":
    main()
