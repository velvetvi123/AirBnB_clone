#!/usr/bin/python3
"""Module pour le point d'entrée de l'interpréteur de commande."""

import cmd
from models.base_model import BaseModel
from models import storage
import re
import json


class HBNBCommand(cmd.Cmd):

    """Classe pour l'interpréteur de commande."""

    prompt = "(hbnb) "

    def default(self, line):
        """Capture les commandes si rien d'autre ne correspond."""
        # print("DEF:::", line)
        self._precmd(line)

    def _precmd(self, line):
        """Intercepte les commandes pour tester class.syntax()"""
        # print("PRECMD:::", line)
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line
        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(
                    1) or "") + " " + (match_attr_and_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(command)
        return command

    def update_dict(self, classname, uid, s_dict):
        """Méthode d'assistance pour update() avec un dictionnaire."""
        s = s_dict.replace("'", '"')
        d = json.loads(s)
        if not classname:
            print("** nom de classe manquant **")
        elif classname not in storage.classes():
            print("** la classe n'existe pas **")
        elif uid is None:
            print("** identifiant d'instance manquant **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** aucune instance trouvée **")
            else:
                attributes = storage.attributes()[classname]
                for attribute, value in d.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def do_EOF(self, line):
        """Gère le caractère de fin de fichier (EOF)."""
        print()
        return True

    def do_quit(self, line):
        """Quitte le programme."""
        return True

    def emptyline(self):
        """Ne fait rien sur ENTER."""
        pass

    def do_create(self, line):
        """Crée une instance."""
        if line == "" or line is None:
            print("** nom de classe manquant **")
        elif line not in storage.classes():
            print("** la classe n'existe pas **")
        else:
            b = storage.classes()[line]()
            b.save()
            print(b.id)

    def do_show(self, line):
        """Affiche la représentation en chaîne d'une instance."""
        if line == "" or line is None:
            print("** nom de classe manquant **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** la classe n'existe pas **")
            elif len(words) < 2:
                print("** identifiant d'instance manquant **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** aucune instance trouvée **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, line):
        """Supprime une instance basée sur le nom de la classe et l'identifiant."""
        if line == "" or line is None:
            print("** nom de classe manquant **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** la classe n'existe pas **")
            elif len(words) < 2:
                print("** identifiant d'instance manquant **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** aucune instance trouvée **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, line):
        """Affiche toutes les représentations en chaîne de toutes les instances."""
        if line != "":
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** la classe n'existe pas **")
            else:
                nl = [str(obj) for key, obj in storage.all().items()
                      if type(obj).__name__ == words[0]]
                print(nl)
        else:
            new_list = [str(obj) for key, obj in storage.all().items()]
            print(new_list)

    def do_count(self, line):
        """Compte les instances d'une classe."""
        words = line.split(' ')
        if not words[0]:
            print("** nom de classe manquant **")
        elif words[0] not in storage.classes():
            print("** la classe n'existe pas **")
        else:
            matches = [
                k for k in storage.all() if k.startswith(
                    words[0] + '.')]
            print(len(matches))

    def do_update(self, line):
        """Met à jour une instance en ajoutant ou mettant à jour un attribut."""
        if line == "" or line is None:
            print("** nom de classe manquant **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** nom de classe manquant **")
        elif classname not in storage.classes():
            print("** la classe n'existe pas **")
        elif uid is None:
            print("** identifiant d'instance manquant **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** aucune instance trouvée **")
            elif not attribute:
                print("** nom d'attribut manquant **")
            elif not value:
                print("** valeur manquante **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass  # bon, reste une chaîne de caractères alors
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
