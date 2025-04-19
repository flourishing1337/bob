import requests
from bs4 import BeautifulSoup

# hitta.se scraper
def hitta_foretag(stad, sokord):
    url = f"https://www.hitta.se/sök?vad={sokord}&var={stad}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    companies = soup.find_all('li', attrs={'data-test': 'company-item'})

    results = []
    for company in companies:
        name_tag = company.find('h2', attrs={'data-test': 'search-result-title'})
        address_tag = company.find('div', class_='style_displayLocation__BN9e_')

        name = name_tag.get_text(strip=True) if name_tag else "Okänt namn"
        address = address_tag.get_text(strip=True) if address_tag else "Okänd adress"

        results.append({
            "name": name,
            "address": address,
        })

    return results

# allabolag.se scraper
def hitta_allabolag(sokord, plats):
    url = f"https://www.allabolag.se/what/{sokord}/where/{plats}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    company_tags = soup.find_all('a', class_='addax-cs_hl_hit_company_name_click')

    results = []
    for tag in company_tags:
        name = tag.get_text(strip=True)
        link = "https://www.allabolag.se" + tag['href']
        results.append({"name": name, "link": link})

    return results

if __name__ == "__main__":
    print("Resultat från hitta.se:")
    print(hitta_foretag("Strängnäs", "restaurang"))

    print("\nResultat från allabolag.se:")
    print(hitta_allabolag("restaurang", "Strängnäs"))
