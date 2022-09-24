import os
import requests
import json
from .errors import *


class BaseAPI():
    """
    Base class for the pypaystack python API wrapper for paystack
    Not to be instantiated directly.
    """

    _BASE_END_POINT = "https://hacker-news.firebaseio.com/v0" 

    # def __init__(self):
    #     pass

    @staticmethod
    def _url(path:str):
        if not path.startswith('/'):
            path = '/' + path
        return BaseAPI._BASE_END_POINT + path

    @staticmethod
    def _handle_request(url):

        """
        Generic function to handle all API url calls
        Returns a JSON object, could be a list, dict, int or str, depends on the json
        """
        response = requests.get(url)


        # response = request(url, headers=self._headers(), data=payload, verify=True)
        if response.status_code == 404:
            return None

        return response.json()
