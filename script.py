import requests
import json
import extract

# Système d'extraction de données JSON
#------------------------------------------------------------------------------------#
def extract_element_from_json(obj, path):
    '''
    Extracts an element from a nested dictionary or
    a list of nested dictionaries along a specified path.
    If the input is a dictionary, a list is returned.
    If the input is a list of dictionary, a list of lists is returned.
    obj - list or dict - input dictionary or list of dictionaries
    path - list - list of strings that form the path to the desired element
    '''
    def extract(obj, path, ind, arr):
        '''
            Extracts an element from a nested dictionary
            along a specified path and returns a list.
            obj - dict - input dictionary
            path - list - list of strings that form the JSON path
            ind - int - starting index
            arr - list - output list
        '''
        key = path[ind]
        if ind + 1 < len(path):
            if isinstance(obj, dict):
                if key in obj.keys():
                    extract(obj.get(key), path, ind + 1, arr)
                else:
                    arr.append(None)
            elif isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        extract(item, path, ind, arr)
            else:
                arr.append(None)
        if ind + 1 == len(path):
            if isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        arr.append(item.get(key, None))
            elif isinstance(obj, dict):
                arr.append(obj.get(key, None))
            else:
                arr.append(None)
        return arr
    if isinstance(obj, dict):
        return extract(obj, path, 0, [])
    elif isinstance(obj, list):
        outer_arr = []
        for item in obj:
            outer_arr.append(extract(item, path, 0, []))
        return outer_arr

#------------------------------------------------------------------------------------#

# Identifiants
ID = "abc" # Identifiant
PSSWD = "abc" # Mot de passe

# URL de login de l'API EcoleDirecte
url = 'https://api.ecoledirecte.com/v3/login.awp?data={"identifiant": ID, "motdepasse": PSSWD}'

# Requète "POST" en direction de l'API.
response = requests.post(url)
print("Requète bien envoyée.")

# Affichage des résultats non traités (facultatif)
#print(response.text)

# Ecriture de "results.json" avec les résultats NON TRAITES
file = open("results.json", "w")
file.write(response.text)
file.close()
print("Résultats enregistrés.")

# Extraction de données
data = json.load(open('results.json'))
wanted = extract_element_from_json(data, ["token"])

# Affichage des données extraites
print("Token :")
print(wanted)

#------------------------------------------------------------------------------------#
# Par exemple pour le cahier de textes

url = "https://api.ecoledirecte.com/v3/eleves/5590/cahierdetexte.awp?verbe=get"

TOKEN = wanted # A changer possiblement

payload = f"data={\n\t\"token\": \{TOKEN}\n}"
headers= {}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text)
file = open("script_results.json", "w")
file.write(response.text)
file.close()
