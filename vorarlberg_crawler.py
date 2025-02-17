import json
import requests
from bs4 import BeautifulSoup


def startsWithDigit(s):
    return s[0].isdigit() if s else False


json_file = open("vorarlberg.json", "w+", encoding="utf-8")
ortschaften_links_json = []
ortschaften_strassen_json = []

for i in range(1,7):

    url = f"https://strasse-plz-ort.at/ortschaften/vorarlberg/{i}"
    response = requests.get(url)

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, "html.parser")
        ortschaften = soup.find_all("div", class_="threecolumn card")
    
        for card in ortschaften:

            name = card.find("h2").text.strip()
            link = card.find("a")["href"]
            
            ortschaften_links_json.append({
                "name": name,
                "link": link
            })
            
    else:
        print("ERROR!\n")


for ort in ortschaften_links_json:

    name = ort["name"]
    link = ort["link"]
    url = "https://strasse-plz-ort.at" + link
    response = requests.get(url)

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, "html.parser")
        strassen = [h3.text.strip() for h3 in soup.find_all("h3")]
        strassen_json = []

        for strasse in strassen:

            if(not startsWithDigit(strasse)):
                strassen_json.append(strasse)

        ortschaften_strassen_json.append({
            "ort": ort["name"],
            "strassen_json": strassen_json
        })

    else:
        print("ERROR!\n")

json.dump(ortschaften_strassen_json, json_file, ensure_ascii=False, indent=4)

json_file.close()
