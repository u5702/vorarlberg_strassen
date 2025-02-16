from bs4 import BeautifulSoup
import requests
import json

file = open("ortschaften_vorarlberg.json", "a", encoding="utf-8")
ortschaften_data = []

for i in range(1,7):

    url = f"https://strasse-plz-ort.at/ortschaften/vorarlberg/{i}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        ortschaften = soup.find_all("div", class_="threecolumn card")
    
        for card in ortschaften:
            name = card.find("h2").text.strip()
            link = card.find("a")["href"]
            
            ortschaften_data.append({
                "name": name,
                "link": link
            })
            
    else:
        print("ERROR!\n")

json.dump(ortschaften_data, file, ensure_ascii=False, indent=4)
file.close()