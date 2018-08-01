import pathlib

import globals
from Manager.Error import status_details
from Manager.Query import get_query, post_query
from Config import config

import json
import re


class Entity:
    """
    Classe qui gère les entités
    """

    def __init__(self):
        self.folder = "/Entities"

    def _get_list_dict(self):
        """
        :return: Dictionnaire contenant la liste de tous les entités
        """
        list_response = get_query("agent/entityTypes")

        return json.loads(list_response.text)

    def _get_name_idurl_dict(self):
        """
        :return: Dictionnaire de name -> id url
        """
        list_dict = self._get_list_dict()
        name_idurl_dict = {}

        for entity in list_dict["entityTypes"]:
            name_idurl_dict[entity["displayName"]] = entity["name"]

        return name_idurl_dict

    def _get_name_id_dict(self):
        """
        :return: Dictionnaire de name -> id
        """
        list_dict = self._get_list_dict()
        name_id_dict = {}

        for entity in list_dict["entityTypes"]:
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

        for entity in file_dict["entityTypeBatchInline"]["entityTypes"]:
            if "name" in entity:
                entity.pop("name", None)
            if entity["displayName"] not in name_idurl_dict:
                continue
            entity["name"] = name_idurl_dict[entity["displayName"]]

        return json.dumps(file_dict)

    def import_mod(self, filenames, language):
        """
        Importe l'entity sur DialogFlow

        :param filenames: Nom du fichier JSON contenant la configuration du module
        :param language: Langage source de l'entité
        """

        base_file = "Config/Entities/import_base.json"
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

        base_json = re.sub('\$ENTITIES', concat_files_json, base_json)
        base_json = self._get_id(base_json)

        response = post_query("agent/entityTypes:batchUpdate", base_json)
        status_details(response)

    def export_mod(self, modnames):
        """
        Exporte l'entity de DialogFlow

        :param modnames: Nom de l'entitée
        """
        name_id_dict = self._get_name_id_dict()

        for modname in modnames:
            if modname not in name_id_dict:
                raise ValueError("Il n'y a pas d'entité qui s'appelle " + modname + "!")

            response = get_query("agent/entityTypes/" + name_id_dict[modname])
            status_details(response)
            name_entity = json.loads(response.text)["displayName"]

            # TODO: Fonction pour créer un nouveau dossier et write dans un fichier
            path = "/".join((config.data_export_folder, globals.project_id, self.folder))
            filename = '/'.join((path, name_entity + ".json"))

            pathlib.Path(path).mkdir(parents=True, exist_ok=True)

            with open(filename, 'w') as f:
                f.write(response.text)

    def remove_mod(self, modnames):
        """
        Supprime l'entity de DialogFlow

        :param modnames: Nom des entités
        """
        name_idurl_dict = self._get_name_idurl_dict()
        entity_list = []

        for modname in modnames:
            if modname not in name_idurl_dict:
                print("Attention : Il n'y a pas d'entité qui s'appelle " + modname + "!")
                continue

            entity_list.append(name_idurl_dict[modname])

        dict_json = {"entityTypeNames": entity_list}

        response = post_query("agent/entityTypes/:batchDelete", data=json.dumps(dict_json))
        status_details(response)
