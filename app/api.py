from abc import ABC, abstractmethod
from serpapi import GoogleSearch

import json
import keys
from app import consts


class BasicApi(ABC):

    @abstractmethod
    def getImages(self, entry): ...


class GoogleApi(BasicApi):
    _BASIC_GOOGLE_API_PARAMS = {
        "hl": "pl",
        "gl": "pl",
        "tbm": "isch",
        "api_key": keys.API_KEY
    }
    _ENTRY_KEY = 'p'
    _IMAGES_RESULTS_KEY = 'images_results'
    _IMAGE_URL_KEY = 'original'

    def __init__(self):
        self.params = self._BASIC_GOOGLE_API_PARAMS

    def getImages(self, entry):
        results = self._search(entry, use_mock=True)

        if self._IMAGES_RESULTS_KEY not in results:
            raise ValueError('No images found :(')

        images = []
        for image_result in results[self._IMAGES_RESULTS_KEY]:
            if self._IMAGE_URL_KEY in image_result:
                images.append(image_result[self._IMAGE_URL_KEY])

        return images

    def _search(self, entry, use_mock=False):
        if not use_mock:
            self.params[self._ENTRY_KEY] = entry
            search = GoogleSearch(self.params)
            results = search.get_dict()
        else:
            with open('../mocks/mock.json') as f:
                results = json.load(f)

        return results


class BingApi(BasicApi):

    def getImages(self, entry):
        pass


class YahooApi(BasicApi):

    def getImages(self, entry):
        pass


class ApiProvider:
    @staticmethod
    def getApi(searchEngine):
        if searchEngine == consts.SearchEngines.GOOGLE.value:
            return GoogleApi()
        elif searchEngine == consts.SearchEngines.BING.value:
            return BingApi()
        elif searchEngine == consts.SearchEngines.YAHOO.value:
            return YahooApi()
        else:
            raise ValueError('Unsupported search engine')
