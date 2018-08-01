"""Permet de se connecter à l'API de DialogFlow"""

import globals
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession


def login(credential_file):
    """
    Initialise la variable auth_r, afin de l'utiliser pour réaliser des requêtes API
    via le compte de service

    :param credential_file: Fichier contenant l'identifiant du compte de service
    """

    scopes = ['https://www.googleapis.com/auth/cloud-platform']
    globals.credentials = service_account.Credentials.from_service_account_file(credential_file, scopes=scopes)
    globals.authr = AuthorizedSession(globals.credentials)
