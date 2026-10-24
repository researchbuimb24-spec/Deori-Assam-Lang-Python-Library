import requests
import json
import re

url = "https://glottolog.org/langdoc?sEcho=1&iColumns=11&sColumns=&iDisplayStart=0&iDisplayLength=100&language=deor1238"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest"
}
resp = requests.get(url, headers=headers)
data = resp.json()
print("Total records:", data.get("iTotalRecords"))
for idx, row in enumerate(data.get("aaData", []), 1):
    c1 = re.sub(r'<[^>]+>', ' ', str(row[1])).strip()
    c2 = re.sub(r'<[^>]+>', ' ', str(row[2])).strip()
    c5 = str(row[5]).strip()
    c7 = re.sub(r'<[^>]+>', ' ', str(row[7])).strip()
    link_m = re.search(r'href="([^"]+)"', str(row[1]))
    link = link_m.group(1) if link_m else ""
    print(f"{idx}. {c1} ({c5}): {c2} | Type: {c7} | Glottolog URL: {link}")

with open("glottolog_deori_13.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
