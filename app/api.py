from abc import ABC, abstractmethod
from serpapi import GoogleSearch

import requests
from bs4 import BeautifulSoup

import json
import keys
import os
from app import consts


class BasicApi(ABC):

    @property
    @abstractmethod
    def _FOLDER_NAME(self): ...

    @abstractmethod
    def getImages(self, entry): ...


class ScraperApi(BasicApi, ABC):

    @property
    @abstractmethod
    def _WEBSITE_URL(self): ...

    @property
    @abstractmethod
    def _PARSER(self): ...

    @property
    @abstractmethod
    def _SEARCH_ATTRIBUTES(self): ...

    @property
    @abstractmethod
    def _IMAGE_KEY(self): ...

    def getImages(self, entry):
        if os.path.exists(consts.DEFAULT_MOCK_PATH.format(self._FOLDER_NAME, entry)):
            with open(consts.DEFAULT_MOCK_PATH.format(self._FOLDER_NAME, entry), encoding='utf-8') as file:
                results = json.load(file)
        else:
            req = requests.get(self._WEBSITE_URL % entry)
            soup = BeautifulSoup(req.text, features=self._PARSER)

            results = []
            for link in soup.find_all(attrs=self._SEARCH_ATTRIBUTES):
                results.append(link.get(self._IMAGE_KEY))

            with open(consts.DEFAULT_MOCK_PATH.format(self._FOLDER_NAME, entry), 'w') as file:
                json.dump(results, file)

        return results


class GoogleApi(BasicApi):
    _FOLDER_NAME = 'google'
    _BASIC_GOOGLE_API_PARAMS = {
        "hl": "pl",
        "gl": "pl",
        "tbm": "isch",
        "api_key": keys.API_KEY
    }
    _ENTRY_KEY = 'q'
    _IMAGES_RESULTS_KEY = 'images_results'
    _IMAGE_URL_KEY = 'original'

    def __init__(self):
        self.params = self._BASIC_GOOGLE_API_PARAMS

    def getImages(self, entry):
        if os.path.exists(consts.DEFAULT_MOCK_PATH.format(self._FOLDER_NAME, entry)):
            with open(consts.DEFAULT_MOCK_PATH.format(self._FOLDER_NAME, entry), encoding='utf-8') as file:
                results = json.load(file)
        else:
            results = self._search(entry)
            with open(consts.DEFAULT_MOCK_PATH.format(self._FOLDER_NAME, entry), 'w') as file:
                json.dump(results, file)

        if self._IMAGES_RESULTS_KEY not in results:
            raise ValueError('No images found :(')

        images = []
        for image_result in results[self._IMAGES_RESULTS_KEY]:
            if self._IMAGE_URL_KEY in image_result:
                images.append(image_result[self._IMAGE_URL_KEY])

        return images

    def _search(self, entry):
        self.params[self._ENTRY_KEY] = entry
        search = GoogleSearch(self.params)
        results = search.get_dict()
        print(results)

        return results


class BingApi(ScraperApi):
    _FOLDER_NAME = 'bing'
    _WEBSITE_URL = "https://www.bing.com/images/search?q=%s"
    _PARSER = "html.parser"
    _SEARCH_ATTRIBUTES = {"class": "mimg"}
    _IMAGE_KEY = 'src'


class YahooApi(ScraperApi):
    _FOLDER_NAME = 'yahoo'
    _WEBSITE_URL = "http://images.search.yahoo.com/search/images?p=%s&imgl=fsu"
    _PARSER = "html.parser"
    _SEARCH_ATTRIBUTES = {"class": "process"}
    _IMAGE_KEY = 'data-src'


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
