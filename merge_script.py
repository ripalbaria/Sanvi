import requests

# Updated URLs
M3U_URLS = [
    "https://geefive.saqlainhaider8198.workers.dev/",
    "https://raw.githubusercontent.com/alex8875/m3u/refs/heads/main/jtv.m3u",
    "https://solii.saqlainhaider8198.workers.dev"
]
OUTPUT_FILE = "playlist.m3u"

def main():
    merged_content = ["#EXTM3U"]
    
    # 1. Grab and parse M3U files
    for url in M3U_URLS:
        print(f"Fetching: {url}")
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                # Filter out the header and empty lines
                lines = [line.strip() for line in r.text.splitlines() if line.strip()]
                for line in lines:
                    if not line.startswith("#EXTM3U"):
                        merged_content.append(line)
            else:
                print(f"Failed to fetch {url}: Status {r.status_code}")
        except Exception as e:
            print(f"Skipping M3U due to error: {url} ({e})")

    # 2. Write all at once (fastest I/O)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_content))
    
    print(f"\nDone! Created '{OUTPUT_FILE}' with {len(merged_content)//2} potential channels.")

if __name__ == "__main__":
    main()
