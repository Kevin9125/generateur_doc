from tree_sitter import Parser, Language, Query, QueryCursor, TreeCursor, Node
from abc import ABCMeta, ABC

import tree_sitter_python
import tree_sitter_c
import tree_sitter_rust
import json

class ModeleParser(metaclass = ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def RegisterClass(self):
        pass

    @abstractmethod
    def RegisterFunction(self):
        pass

    @abstractmethod
    def RegisterAttributs(self):
        pass

    @abstractmethod
    def RegisterReturn(self):
        pass

class ParserPython(ModeleParser):
    def __init__(self):
        self.parseur = Parser(Language(tree_sitter_python.language()))

    def ParseFiles(self, contenu : str) -> None:
        
        #Initialisation
        tree = self.parseur.parse(bytes(contenu, "utf8"))
        cursor = tree.walk()
        dict_module = {}

        #Creation du dictionnaire
        for child in cursor.node.children:
            dict_module = self.RegisterClass(child)

        
        #transformation du dictionnaire en json
        if type(dict_module) == dict:
            json_module = json.dumps(dict_module, indent=4)
        else:
            raise TypeError("probleme de type lors de la transformation en json")

        return json_module
       

    def RegisterClass(self, node: Node, dict_module: dict = {}) -> dict:
        dict_classe = {}
        class_name = ""
        for child in node.named_children:
            match child.type:

                #noeud representant le nom attribuer à ce qu'il represente dans le code 
                #(exemple noeud.type = "function definition" : identifier = nom_fonction)
                case "identifier":
                    class_name = self.NettoyageStr(str(child.text))
                
                #noeud representant le corps de la classe (la ou sont les methodes)
                case "block":
                    for function in child.named_children:
                        dict_classe = self.RegisterFunction(function, dict_classe)


        dict_module[class_name] = dict_classe
        pass
        return dict_module
            
    def RegisterFunction(self, node : Node, dict_classe: dict = {}) -> dict:
        parameters_name = []
        func_name = ""

        for child in node.named_children:
            match child.type:
                case "identifier":
                    func_name = self.NettoyageStr(str(child.text))
                    
                case "parameters":
                    for arg in child.named_children:
                        parameters_name.append(self.NettoyageStr(str(arg.text)))

                case "block":
                    for grand_child in child.named_children:

                        if grand_child.type == "expression_statement":
                            dict_classe = self.RegisterAttributs(grand_child, dict_classe)

                        elif grand_child.type == "return_statement":
                            dict_classe = self.RegisterReturn(grand_child, dict_classe)

                        else: 
                            pass

        
        #defini une entrée "methodes" dans le dictionnaire si elle n'existe pas déjà
        if not "methodes" in dict_classe:
            dict_classe["methodes"] = {}

        dict_classe["methodes"][func_name] = {}
        dict_classe["methodes"][func_name]["arguments"] = parameters_name
        return dict_classe
    
    
    def RegisterAttributs(self, node: Node, dict_classe: dict) -> dict:

        attribut = None
        val = None

        if not "attributs" in dict_classe:
            dict_classe["attributs"] = {}

        for child in node.named_children:
            if child.type == "assignment":
                
                for grand_child in child.named_children:
 
                    if grand_child.type == "attribute":
                        attribut = self.NettoyageStr(str(grand_child.text))

                    elif grand_child.type == "identifier":
                        val = self.NettoyageStr(str(grand_child.text))

                    if val != None:
                        try:
                            int(val) != "None"
                        
                        except ValueError:
                            val = str(val)

                        else:
                            val = int(val)

        if attribut != None and val != None:
            dict_classe["attributs"][str(attribut)] = val

        return dict_classe

    def RegisterReturn(self, node: Node, dict_classe: dict):
        dict_classe["return"] = self.NettoyageStr(str(node.named_children[0].text))
        
        return dict_classe

    def NettoyageStr(self, string: str) -> str:
        CARACTERE = "\'"
        premiere_occurence = string.find(CARACTERE)
        dernière_occurence = string.rfind(CARACTERE)
        return string[premiere_occurence+1:dernière_occurence]
        
        
    
    



