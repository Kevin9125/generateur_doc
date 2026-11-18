from core.AnalyseurCode import AnalyseurCode
from core.CreationDonneesEntrainementIA import CreationDonneesEntrainementIA

import json
import jsondiff
import torch
from jsondiff import diff

def main() -> None:

    analyseur = AnalyseurCode()
    test_fichier = ["src/main.py"]
    list_vide = []
    verif_data = ""
    analyseur.AnalyseFichiers(test_fichier)

    #with open("./tests/verif_json_solo.json", "r") as f:
        #verif_data = f.read()
    #formatted_verif_data = json.dumps(verif_data, indent=4)
    #print(result.data)
    #print(result.msg)
    #print(json.loads(formatted_verif_data))
    #_ = diff(result.data, json.loads(formatted_verif_data))
    #if _ == result.data:
        #print("Is equal")
    #else:
        #print("NONNNN")
    
 
    #CreationDonneesEntrainement(0)
    return None

if __name__ == "__main__":
    main()
