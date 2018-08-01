"""
Gère les arguments
"""

from Manager import Agent, Intent, Entity
from json import load
import globals

import argparse


def get_project_id(credential_file):
    """
    Obtient le project_id du credential file
    Stock le résultat dans globals

    :param credential_file: Path vers le credential file
    """
    with open(credential_file) as f:
        json_cf = load(f)

    globals.project_id = json_cf["project_id"]


def execute(args: dict):
    """
    Execute le programme selon les arguments

    :param args: Arguments
    :return:
    """

    get_project_id(args.credentialfile)

    # TODO: Optimiser le code pour éviter la forêt de if

    if args.agent:
        agent = Agent.Agent()
        if args.importAgent:
            agent.import_agent(args.importAgent)
        elif args.exportAgent:
            agent.export_agent()

    elif args.intent:
        intent = Intent.Intent()
        if args.importMod:
            intent.import_mod(args.importMod, args.language)
        elif args.exportMod:
            intent.export_mod(args.exportMod)
        elif args.deleteMod:
            intent.remove_mod(args.deleteMod)

    elif args.entity:
        entity = Entity.Entity()
        if args.importMod:
            entity.import_mod(args.importMod, args.language)
        elif args.exportMod:
            entity.export_mod(args.exportMod)
        elif args.deleteMod:
            entity.remove_mod(args.deleteMod)


def parse_arguments():
    """
    Permet de parser les arguments.

    python3 program.py [-h] [-A [-i importFile | -e]] [[-I | -E][-i importFileList | -e exportList | -r removeList]]
    [-l language] -c credentialfile
    :return : Arguments parsés en variables
    """

    # Création du parseur
    parser = argparse.ArgumentParser(description='Outil permettant de gérer DialogFlow')


        ##### Agent #####
    agent = parser.add_argument_group("Agent")

        # Agent
    agent.add_argument('-A', '--agent', action='store_true',
                       help='Gérer un agent')

            ##### Agent - Actions #####
    agent_actions = agent.add_mutually_exclusive_group()

            # Importer / Restaurer
    agent_actions.add_argument('-ia', '--importAgent', type=str, dest='importAgent',
                               help='Importe / Restaure l\'agent sélectionnée. Fichier ZIP attendu')

            # Exporter
    agent_actions.add_argument('-ea', '--exportAgent', action='store_true', dest='exportAgent',
                               help='Exporte l\'agent dans le dossier "$data_export_folder/$ID_agent/Agents".\
                                     Nom(s) du/des module(s) attendu')


        ##### Intention / Entité #####
    int_ent = parser.add_argument_group("Intention & Entité")

            ##### Intention / Entité - Modules #####
    int_ent_mod = int_ent.add_mutually_exclusive_group()

            # Intention
    int_ent_mod.add_argument('-I', '--intent', action='store_true', help='Gérer une intention')

            # Entité
    int_ent_mod.add_argument('-E', '--entity', action='store_true', help='Gérer une entité')

        ##### Intention / Entité - Actions #####
    int_ent_actions = int_ent.add_mutually_exclusive_group()

            # Importer / restaurer
    int_ent_actions.add_argument('-i', '--importModList', type=str, dest='importMod', nargs='+',
                                 help='Importe / Restaure le module sélectionnée. \
                                 Fichier(s) de configuration JSON attendu')

            # Exporter
    int_ent_actions.add_argument('-e', '--exportModList', type=str, dest='exportMod', nargs='+',
                                 help='Exporte le module sélectionnée. Nom(s) du/des module(s) attendu')

            # Supprimer
    int_ent_actions.add_argument('-r', '--removeModList', type=str, dest='deleteMod', nargs='+',
                                 help='Supprime le module sélectionnée. Nom(s) du/des module(s) attendu')


    ##### Obligatoire #####
    # Fichier de compte service (OBLIGATOIRE)
    parser.add_argument('-c', '--credentialfile', type=str,
                        help='Sélectionne le fichier contenant les informations d\'authentification à DialogFlow. \
                        Fichier compte de service admin attendu', required=True)


    ##### Optionnel #####
    # Langage
    parser.add_argument('-l', '--language', type=str, dest='language', default='fr',
                        help='Défini la langue de l\'entité. Par défaut : fr')

    return parser.parse_args()
