import os
import json
import logging
import pathlib

from typing import Dict, List
from pydantic import Json

logger = logging.getLogger(__name__)


RESSOURCE_FOLDER = 'data'
FILE_SCORE_DESCRIPTIONS = 'score-description.json'


class ResourceCatalog():
    def __init__(self):
        self.__data_folder: str = os.path.join(pathlib.Path(__file__).parent.resolve(), RESSOURCE_FOLDER)

        # add loading of other static ressources here
        self._file_score_description: str = os.path.join(self.__data_folder, FILE_SCORE_DESCRIPTIONS)
        
        self._score_description: List[Dict[str, str]] = None

    def __load_json(self, file_path: str) -> Json:
        if self._score_description is None:
            if os.path.exists(file_path):
                try:
                    with open(file_path, encoding='UTF-8') as file:
                        return json.load(file)
                except Exception as ex:
                    logger.error('Error when loading ressource catalog [%s] : %s', file_path, str(ex))
                    return []  # return something

    def get_score_description(self) -> List[Dict[str, str]]:
        return self.__load_json(self._file_score_description)


catalog = ResourceCatalog()
