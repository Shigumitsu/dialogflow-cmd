import globals
from Config import config

from datetime import date, datetime
import pathlib
from dialogflow_v2 import AgentsClient


class Agent:
    """
    Classe qui gère les agents
    """

    def __init__(self):
        self.client = AgentsClient(credentials=globals.credentials)
        self.parent = self.client.project_path(globals.project_id)
        self.folder = '/Agents'

    def import_agent(self, filename):
        """
        Importe l'agent sur DialogFlow

        :param filename: Nom du fichier ZIP contenant la configuration du module
        """

        with open(filename, "rb") as f:
            file = f.read()

        self.client.restore_agent(self.parent, agent_content=file)

    def export_agent(self):
        """
        Exporte l'agent de DialogFlow
        """

        response = self.client.export_agent(self.parent)
        json_response = response.result()

        agent_bin = json_response.agent_content
        path = "/".join((config.data_export_folder, globals.project_id, self.folder))
        filename = "/".join((path, date.strftime(datetime.now(), "%Y%m%d_%H%M%S") + ".zip"))

        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

        with open(filename, "wb") as f:
            f.write(agent_bin)
