import requests
from bs4 import BeautifulSoup

OLX_URL = "https://www.olx.pl/elektronika/gry-konsole/akcesoria-gamingowe/rzeszow/q-logitech-g29/?search%5Bdist%5D=5&search%5Bfilter_float_price:from%5D=50&search%5Bfilter_float_price:to%5D=800"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pl-PL,pl;q=0.9,en;q=0.8",
}

response = requests.get(
    OLX_URL,
    headers=headers,
    timeout=30
)

print("HTTP status:", response.status_code)
print("Downloaded:", len(response.text), "bytes")

if response.status_code != 200:
    print("OLX did not return a normal page.")
    print(response.text[:1000])
    raise SystemExit(1)

soup = BeautifulSoup(response.text, "html.parser")

print("Page title:", soup.title.get_text(strip=True) if soup.title else "NO TITLE")

# Покажемо перші посилання, які схожі на оголошення
links = []

for a in soup.find_all("a", href=True):
    href = a["href"]

    if "/d/oferta/" in href or "/d/ogloszenie/" in href:
        title = a.get_text(" ", strip=True)

        if title:
            links.append((title, href))

print()
print("Possible listings:", len(links))

for title, href in links[:10]:
    print("\nTITLE:", title[:150])
    print("URL:", href)
