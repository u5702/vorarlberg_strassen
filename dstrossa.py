import json
import requests
from bs4 import BeautifulSoup

def starts_with_digit(s):
    return s[0].isdigit() if s else False

link_file =  open("ortschaften_vorarlberg.json", "r", encoding="utf-8")
json_file = open("vorarlberg.json", "w", encoding="utf-8")
ortschaften_data = json.load(link_file)
ortschaften_strassen = []

for ort in ortschaften_data:
    name = ort["name"]
    link = ort["link"]
    url = "https://strasse-plz-ort.at" + link

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        streets = [h3.text.strip() for h3 in soup.find_all("h3")]
        strassen = []

        for street in streets:
            if(not starts_with_digit(street)):
                strassen.append(street)

        ortschaften_strassen.append({
            "ort": ort["name"],
            "strassen": strassen
        })

    else:
        print("ERROR!\n")

json.dump(ortschaften_strassen, json_file, ensure_ascii=False, indent=4)
json_file.close()
link_file.close()