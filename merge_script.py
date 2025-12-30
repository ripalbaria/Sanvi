import requests
import json

# Your URLs
M3U_URLS = [
    "https://geefive.saqlainhaider8198.workers.dev/",
    "https://raw.githubusercontent.com/alex8875/m3u/refs/heads/main/jtv.m3u"
]
JSON_URL = "https://raw.githubusercontent.com/mdsarfraj1ali/play/refs/heads/main/Slivtv.json"
OUTPUT_FILE = "playlist.m3u"

def extract_from_json(data):
    """Deeply searches JSON for anything that looks like a channel."""
    channels = []
    
    # If it's a list, check each item
    if isinstance(data, list):
        for item in data:
            channels.extend(extract_from_json(item))
            
    # If it's a dictionary, look for keys or go deeper
    elif isinstance(data, dict):
        name = data.get("name") or data.get("title") or data.get("channel_name")
        url = data.get("url") or data.get("link") or data.get("stream_url")
        logo = data.get("logo") or data.get("image") or ""
        
        # If we found a name and a link, it's a channel!
        if name and url and (url.startswith("http") or url.startswith("rtmp")):
            channels.append({"name": name, "url": url, "logo": logo})
        
        # Also keep searching deeper into all other keys (like 'values' or 'folder')
        for value in data.values():
            if isinstance(value, (dict, list)):
                channels.extend(extract_from_json(value))
                
    return channels

def main():
    merged_content = "#EXTM3U\n"
    
    # 1. Add M3U Files
    for url in M3U_URLS:
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                merged_content += r.text.replace("#EXTM3U", "").strip() + "\n"
        except:
            print(f"Failed to load M3U: {url}")

    # 2. Add JSON File (Using Deep Search)
    try:
        r = requests.get(JSON_URL, timeout=20)
        if r.status_code == 200:
            json_data = r.json()
            found_channels = extract_from_json(json_data)
            
            # Remove duplicates and add to file
            seen_urls = set()
            for ch in found_channels:
                if ch['url'] not in seen_urls:
                    merged_content += f'#EXTINF:-1 tvg-logo="{ch["logo"]}",{ch["name"]}\n{ch["url"]}\n'
                    seen_urls.add(ch['url'])
            print(f"Deep search found {len(seen_urls)} channels in JSON.")
    except Exception as e:
        print(f"JSON Error: {e}")

    # 3. Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(merged_content)

if __name__ == "__main__":
    main()
