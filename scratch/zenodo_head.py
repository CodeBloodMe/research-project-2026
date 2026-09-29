import urllib.request
try:
    url = 'https://zenodo.org/records/4682056/files/data_set.tar.gz?download=1'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    response = urllib.request.urlopen(req)
    print("Code:", response.getcode())
    print("Content-Length:", response.headers.get('Content-Length'))
except Exception as e:
    print(f"Error: {e}")
