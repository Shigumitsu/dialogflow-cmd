"""
Module qui envoie des requêtes à l'API Dialogflow
"""

from Manager.Error import status_details
import globals

def get_query(url):
    """
    Envoi une requête GET à l'API de Dialogflow

    :param url: Fin de l'url de "https://dialogflow.googleapis.com/v2/projects/$PROJECT_ID/"
    :return: Réponse de l'API de Dialogflow
    """
    response = globals.authr.request('GET',
                                     "https://dialogflow.googleapis.com/v2/projects/" +
                                     globals.project_id +
                                     "/" +
                                     url)

    status_details(response)
    return response


def post_query(url, data):
    """

    :param url: Fin de l'url de "https://dialogflow.googleapis.com/v2/projects/$PROJECT_ID/"
    :param data: Contenu du fichier
    :return: Réponse de l'API de Dialogflow
    """
    response = globals.authr.request('POST',
                                     "https://dialogflow.googleapis.com/v2/projects/" +
                                     globals.project_id +
                                     "/" +
                                     url,
                                     data=data)

    status_details(response)
    return response
