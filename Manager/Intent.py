import globals
from Manager.Error import status_details
from Manager.Query import get_query, post_query
from Config import config

import json
import re
import pathlib


class Intent:
    """
    Classe qui gère les intentions
    """
    def __init__(self):
        self.folder = "/Intents"

    def _get_list_dict(self):
        """
        :return: Dictionnaire contenant la liste de tous les entités
        """
        list_response = get_query("agent/intents")

        return json.loads(list_response.text)

    def _get_name_idurl_dict(self):
        """
        :return: Dictionnaire de name -> id url
        """
        list_dict = self._get_list_dict()
        name_idurl_dict = {}

        for entity in list_dict["intents"]:
            name_idurl_dict[entity["displayName"]] = entity["name"]

        return name_idurl_dict

    def _get_name_id_dict(self):
        """
        :return: Dictionnaire de name -> id
        """
        list_dict = self._get_list_dict()
        name_id_dict = {}

        for entity in list_dict["intents"]:
            name_id_dict[entity["displayName"]] = re.search('[^\/]+$', entity["name"]).group(0)

        return name_id_dict

    def _get_id(self, file_json):
        """
        Ajoute automatiquement les id des entités

        :param file_json: String contenant le JSON des entités
        :return: file_json avec les id des entités
        """

        file_dict = json.loads(file_json)
        name_idurl_dict = self._get_name_idurl_dict()

        for intent in file_dict["intentBatchInline"]["intents"]:
            if "name" in intent:
                intent.pop("name", None)
            if intent["displayName"] not in name_idurl_dict:
                continue
            intent["name"] = name_idurl_dict[intent["displayName"]]

        return json.dumps(file_dict)

    def import_mod(self, filenames, language):
        """
        Importe l'/les intent(s) sur DialogFlow

        :param filenames: Nom du/des fichier(s) JSON contenant la configuration du/des module(s)
        :param language: Langage source de l'intent
        """
        base_file = "Config/Intents/import_base.json"
        concat_files_json = ''

        with open(base_file) as f:
            base_json = f.read()

        base_json = re.sub('\$LANGUAGE', '"' + language + '"', base_json)

        # TODO: Mettre la boucle for et le regex dans une fonction
        for i, filename in enumerate(filenames, start=1):
            with open(filename, "r") as f:
                file_json = f.read()

            concat_files_json += file_json

            if i is not len(filenames):
                concat_files_json += ','

        base_json = re.sub('\$INTENTS', concat_files_json, base_json)
        base_json = self._get_id(base_json)

        response = post_query("agent/intents:batchUpdate", base_json)
        status_details(response)

    def export_mod(self, modnames):
        """
        Exporte l'/les intent(s) de DialogFlow

        :param modnames: Nom de l'/des intent(s)
        """
        name_id_dict = self._get_name_id_dict()

        for modname in modnames:
            if modname not in name_id_dict:
                raise ValueError("Il n'y a pas d'intentions qui s'appelle " + modname + "!")

            response = get_query("agent/intents/" + name_id_dict[modname])
            status_details(response)
            name_intent = json.loads(response.text)["displayName"]

            # TODO: Fonction pour créer un nouveau dossier et write dans un fichier
            path = "/".join((config.data_export_folder, globals.project_id, self.folder))
            filename = '/'.join((path, name_intent + ".json"))

            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            with open(filename, 'w') as f:
                f.write(response.text)

    def remove_mod(self, modnames):
        """
        Supprime l'/les intent(s) de DialogFlow

        modnames : Nom de l'/ des intent(s)
        """
        name_idurl_dict = self._get_name_idurl_dict()
        intent_list = []

        for modname in modnames:
            if modname not in name_idurl_dict:
                print("Attention : Il n'y a pas d'intention qui s'appelle " + modname + "!")
                continue

            intent_list.append({"name": name_idurl_dict[modname]})

        dict_json = {"intents": intent_list}

        response = post_query("agent/intents:batchDelete", data=json.dumps(dict_json))
        status_details(response)
