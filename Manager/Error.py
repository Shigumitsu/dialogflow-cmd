"""
Def
"""

from colorama import Fore, Style, init
import json


def status_details(status):
    """
    Affiche un message selon le code de retour de l'API DialogFlow

    :param status: JSON de retour de requête de DialogFlow
    """

    init(autoreset=True)

    status_text_success = {
        'OK': 'Commande effectué !',
        'Success': 'Commande effectué !',
        'Deprecated': 'Commande effectué !\n' +
                      Fore.YELLOW + '!!! Attention, un élément dans votre fichier est obsolète !!!',
    }

    status_text_error = {
        'Partial Content': 'Erreur: Votre fichier comporte une erreur',
        'Bad Request': 'Erreur: L\'outil à réaliser une mauvaise requête vers DialogFlow',
        'Unauthorized': 'Erreur: Vous n\'êtes pas autorisé à réaliser cet action',
        'Not Found': 'Erreur: L\'outil n\'arrive pas à accéder à DialogFlow (Mauvaise url ?)',
        'Not Allowed': 'Erreur: La méthode utilisé par DialogFlow n\'est pas autorisé par DialogFlow',
        'Not Acceptable': 'Erreur: Votre fichier comporte une/des erreur(s)',
        'Conflict': 'Erreur: Un conflit entre votre requête et le contenu de votre agent',
        'Too Many Requests': 'Erreur: Bravo! Vous avez réussi à réaliser beaucoup de requêtes en très peu de temps !'
    }

    if status.reason in status_text_success:
        print(Style.BRIGHT + Fore.GREEN + status_text_success[status.reason])
    elif status.reason in status_text_error:
        raise ValueError(status_text_error[status.reason] +
                         "\nDialogflow Status: " + status.reason +
                         "\nDialogflow JSON error: \n" + status.text)
    else:
        raise ValueError("Dialogflow Status: " + status.reason +
                         "\nDialogflow JSON error: \n" + status.text)
