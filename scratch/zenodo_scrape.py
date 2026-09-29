import urllib.request
import re
try:
    req = urllib.request.Request('https://zenodo.org/record/4682056', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    files = re.findall(r'href="(/records/4682056/files/[^"]+)"', html)
    files += re.findall(r'href="(/record/4682056/files/[^"]+)"', html)
    print("Files found:", list(set(files)))
except Exception as e:
    print(f"Error: {e}")
