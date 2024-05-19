#!/usr/bin/python3
"""Définit la classe FileStorage."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Représente un moteur de stockage abstrait.

    Attributs:
        __file_path (str): Le nom du fichier où sauvegarder les objets.
        __objects (dict): Un dictionnaire d'objets instanciés.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Retourne le dictionnaire __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Ajoute un objet au dictionnaire __objects avec la clé <nom_de_la_classe>.id"""
        ocname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ocname, obj.id)] = obj

    def save(self):
        """Sérialise __objects dans le fichier JSON __file_path."""
        odict = FileStorage.__objects
        objdict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """Désérialise le fichier JSON __file_path en __objects, si le fichier existe."""
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return






