from .handler4configs import Handler4Configs
from .handler4requests import Handler4Requests
from .models import User, Workspace, Project, ProjectList

class WorkspaceNotFound(Exception): pass

class Handler4GettingSetupInfo(Handler4Requests):
    def __init__(self, configs_file:str='configs.yaml', handler4configs:Handler4Configs=None, store:bool=True):
        '''`handler4configs` overrides `configs_file` if not None.'''

        super().__init__(configs_file, handler4configs)

        self.user:User = None
        self.workspace:Workspace = None
        self.projects:ProjectList = None

        if store:
            self.get_user(store=True)
            self.get_workspace(store=True)
            self.get_projects(store=True)

    #================================================
    # Get user

    def get_user(self, store:bool=True) -> User:
        info = self.get('user').json()
        user = User(info)
        if store:
            self.user = user
        return user

    #================================================
    # Get workspace

    #------------------------------------
    # Helper 1

    def _get_workspaces(self) -> list[Workspace]:
        _info = self.get('workspaces').json()
        workspaces = []
        for info in _info:
            workspaces.append(Workspace(info))
        return workspaces

    #------------------------------------
    # Helper 2

    def _get_workspace_with_id(self, id:str) -> Workspace:
        workspaces = self._get_workspaces()
        for workspace in workspaces:
            if workspace.id == id:
                return workspace
        raise WorkspaceNotFound(f'No workspace found with ID {id}')
    
    #------------------------------------
    # Helper 3

    def _get_workspace_with_name(self, name:str) -> Workspace:
        workspaces = self._get_workspaces()
        for workspace in workspaces:
            if workspace.name == name:
                return workspace
        raise WorkspaceNotFound(f'No workspace found with name {name}')

    #------------------------------------
    # Primary workspace getter method

    def get_workspace(self, store:bool=True) -> Workspace:
        try:
            workspace = self._get_workspace_with_id(self.handler4configs.workspace_id)
        except WorkspaceNotFound:
            workspace = self._get_workspace_with_name(self.handler4configs.workspace_name)
        if store:
            self.workspace = workspace
        return workspace
        
    #================================================
    # Get projects

    #------------------------------------
    # Helper

    def _get_projects_for_workspace_id(self, workspace_id:str) -> list[Project]:
        _info = self.get(f'workspaces/{workspace_id}/projects').json()
        projects = []
        for info in _info:
            projects.append(Project(info, workspace_id))
        return projects
    
    #------------------------------------
    # Primary project getter method

    def get_projects(self, store:bool=True) -> ProjectList:
        projects = ProjectList(self._get_projects_for_workspace_id(self.workspace.id))
        if store:
            self.projects = projects
        return projects