import requests
import json

# Your specific URLs
URLS = [
    "https://geefive.saqlainhaider8198.workers.dev/",
    "https://raw.githubusercontent.com/alex8875/m3u/refs/heads/main/jtv.m3u"
]
JSON_URL = "https://raw.githubusercontent.com/mdsarfraj1ali/play/refs/heads/main/Slivtv.json"
OUTPUT_FILE = "playlist.m3u"

def main():
    merged_content = "#EXTM3U\n"

    # 1. Process M3U URLs
    for url in URLS:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                # Remove the header if it exists to avoid duplicates
                content = r.text.replace("#EXTM3U", "").strip()
                merged_content += content + "\n"
        except Exception as e:
            print(f"Error loading {url}: {e}")

    # 2. Process the Slivtv JSON URL
    try:
        r = requests.get(JSON_URL, timeout=15)
        if r.status_code == 200:
            data = r.json()
            # This handles common JSON IPTV structures (modify if Slivtv uses different keys)
            items = data.get("channels", data if isinstance(data, list) else [])
            for item in items:
                name = item.get("name") or item.get("title", "Unknown")
                link = item.get("url") or item.get("link", "")
                logo = item.get("logo") or item.get("image", "")
                if link:
                    merged_content += f'#EXTINF:-1 tvg-logo="{logo}",{name}\n{link}\n'
    except Exception as e:
        print(f"Error loading JSON: {e}")

    # 3. Save the result
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(merged_content)

if __name__ == "__main__":
    main()
