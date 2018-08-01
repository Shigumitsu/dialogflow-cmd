"""
"Fichier de démarrage" du projet Python
"""

import sys
from Manager.OAuth2 import login
from Manager.Argument import parse_arguments, execute
from os import path

def main():
    """
    Initialisation du programme
    """
    args = parse_arguments()
    login(args.credentialfile)
    execute(args)


if __name__ == "__main__":
    sys.exit(int(main() or 0))
