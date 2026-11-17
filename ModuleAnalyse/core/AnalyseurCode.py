import json
#from core.Parsers import Parsers
from . import Result
from core.Parsers import ParserPython, ParserC, ParserRust

class AnalyseurCode:
    def __init__(self):
        self.parsers = [ParserPython(), ParserRust(), ParserC()]

    #Filtre les fichiers en fonction de si ils existent et si ils sont dans le bon format
    def VerificationFichiers(self, fichiers: list[str], result: Result.Result) -> Result.Result:  
        
        #Initialisation
        files_not_found = []
        liste_mauvais_format = []
        
        if fichiers != None and len(fichiers) > 0:

            #on utilise une copy de la liste afin de pouvoir supprimer des elements dans la liste sans affecter la liste parcouru
            for fichier in fichiers.copy():

                #Verifie si le fichier existe et peut être ouvert
                try:
                    open(fichier)

                except FileNotFoundError:
                    result.result_code = -1
                    files_not_found.append(fichier)
                    fichiers.remove(fichier)

                except:
                    result.result_code = -1
                    result.msg = f"an unregister exception as been raise, try to join the creator of the product"
                    break
                
                else:
                    #verifie si le type de fichier est accepté
                    index = fichier.rfind('.')
                    is_accepted = False

                    for parser in self.parsers:
                        if parser.extension == fichier[index+1:]:
                            is_accepted = True
                            break

                    if is_accepted == False:
                            liste_mauvais_format.append(fichier)
                            fichiers.remove(fichier)

            if len(files_not_found) > 0 or len(liste_mauvais_format) > 0:
                result.msg = f"{files_not_found} as not been found, please check the path of those files and retry. {liste_mauvais_format} are not code files, please put code file in this function"
            
            return result

        elif fichiers == None:
           raise ValueError("la variable ne peut pas être None")

        else:
           raise ValueError("La liste est vide")

    #Analyse les fichiers passer en paramètre et resort les principales classes avec leurs attributs et méthodes
    def AnalyseFichiers(self, fichiers : list[str]) -> tuple[Result.Result, str]:

        for fichier in fichiers:
            index = fichier.rfind('.')
            file_extension = fichier[index+1:]
            format_fichier = None
            parser = None
            contenu = ""
            
            '''
            #determine le type de langages
            for key in self.formats_accepter:
                if key == file_extension:
                      format_fichier = self.formats_accepter[key]
                      parser = Parser(format_fichier.modele_parser)
                      break
            '''
            with open(fichier) as file:
                contenu = file.read()
            
            parseur = ParserPython()
            json_module = parseur.ParseFiles(contenu)
            print(json_module)
            #print(cursor.node.named_children[0].text)
            #print(tree.root_node)
    
        




