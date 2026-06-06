import requests
from .handler4configs import Handler4Configs
from .models import *

class InvalidHandler4RequestsInitArgs(Exception): pass

class Handler4Requests:
    def __init__(self, configs_file:str, handler4configs:Handler4Configs):
        '''`handler4configs` overrides `configs_file` if not None.'''

        if handler4configs is None:
            if isinstance(configs_file, str) and configs_file != '':
                handler4configs = Handler4Configs(configs_file)
            else:
                raise InvalidHandler4RequestsInitArgs('handler4configs is None but a non-empty string for configs_file is not given!')
        self.handler4configs = handler4configs
        self.auth_headers = {'x-api-key': self.handler4configs.api_key_value}
        
    #================================================
    # Generic get

    def get(self, path:str) -> requests.Response:
        return requests.get(
            url=self.handler4configs.api_base_url + path,
            headers=self.auth_headers
        )
        
    #================================================
    # Generic post

    def post(self, path:str, json:dict) -> requests.Response:
        return requests.post(
            url=self.handler4configs.api_base_url + path,
            json=json,
            headers={**self.auth_headers, }
        )
    # NOTE:
    # - Using the `json` argument in the above post method call rather than the `data` argument is crucial
    # - Using the `data` argument fails to serialise the given dictionary as a valid JSON, leading to the following error response:
    #   {'message': "Content-Type 'application/x-www-form-urlencoded;charset=UTF-8' is not supported", 'code': 3000}