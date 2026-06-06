from yaml import safe_load

class InvalidAuthConfig(ValueError): pass
class InvalidAccessConfig(ValueError): pass
class InvalidWorkspaceConfig(ValueError): pass

class Handler4Configs:
    def __init__(self, configs_file:str='configs.yaml', do_load:bool=True):
        with open(configs_file, 'r') as fp:
            self.raw_configs:dict = safe_load(fp)
        if not isinstance(self.raw_configs, dict):
            raise Exception(f'{configs_file} could not be loaded as a dict!')
        
        self.api_key_name = ''
        self.api_key_value = ''
        self.api_base_url = ''
        self.workspace_id = ''
        self.workspace_name = ''

        if do_load:
            self.load_auth_config()
            self.load_access_config()
            self.load_workspace_config()
    
    #================================================
    def load_auth_config(self) -> None:
        msg = 'One or both of the fields - [api_key_name, api_key_value] - were not found in auth config!'
        config = self.raw_configs.get('auth', '')
        try:
            if isinstance(config, dict):
                api_key_name = config['api_key_name']
                api_key_value = config['api_key_value']
            else:
                msg = 'Non-dict auth config!'
                raise KeyError
        except KeyError:
            raise InvalidAuthConfig(msg)   
        self.api_key_name = api_key_name
        self.api_key_value = api_key_value
        print('Successful auth config load :)')
    
    #================================================
    def load_access_config(self) -> None:
        config = self.raw_configs.get('access', '')
        msg = 'Field - api_base_url - was not found in access config!'
        try:
            if isinstance(config, dict):
                api_base_url = config['api_base_url']
            else:
                msg = 'Non-dict access config!'
                raise KeyError
        except KeyError:
            raise InvalidAccessConfig(msg)
        self.api_base_url = api_base_url
        print('Successful access config load :)')
    
    #================================================
    def load_workspace_config(self) -> None:
        config = self.raw_configs.get('workspace', '')
        msg = 'Fields - [workspace_id, workspace_name] - was not found in workspace config!'
        try:
            if isinstance(config, dict):
                workspace_id = config['workspace_id']
                workspace_name = config['workspace_name']
            else:
                msg = 'Non-dict workspace config!'
                raise KeyError
        except KeyError:
            raise InvalidWorkspaceConfig(msg)
        self.workspace_id = workspace_id
        self.workspace_name = workspace_name
        print('Successful workspace config load :)')
