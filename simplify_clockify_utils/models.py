class MissingRequiredField(Exception): pass
class InvalidTimeEntry(Exception): pass

class User:
    def __init__(self, info:dict):
        self.id:str = info.get('id', '')
        self.name:str = info.get('name', '')
        self.email:str = info.get('email', '')
    
    def __str__(self) -> str:
        return f'user id={self.id}:\n- name: {self.name}\n- email: {self.email}'

class Workspace:
    def __init__(self, info:dict):
        self.id:str = info.get('id', '')
        self.name:str = info.get('name', '')
        self.cakeOrganizationId:str = info.get('cakeOrganizationId', '')
    
    def __str__(self) -> str:
        return f'workspace id={self.id}:\n- name: {self.name}\n- cakeOrganizationId: {self.cakeOrganizationId}'

class Project:
    def __init__(self, info:dict, workspaceId:str=''):
        self.id:str = info.get('id', '')
        self.name:str = info.get('name', '')
        self.workspaceId:str = workspaceId

    def __str__(self) -> str:
        return f'project id={self.id}:\n- name: {self.name}\n- workspaceId: {self.workspaceId}'

class ProjectList: # we assume that all projects here are from the same workspace
    def __init__(self, project_list:list[Project]):
        self.id_to_name_map = {}
        self.name_to_id_map = {}
        self.project_list = project_list
        for project in project_list:
            self.id_to_name_map[project.id] = project.name
            self.name_to_id_map[project.name] = project.id
        
    def get_name_for_id(self, id:str) -> str:
        return self.id_to_name_map.get(id, '')
    
    def get_id_for_name(self, name:str) -> str:
        return self.name_to_id_map.get(name, '')

    def __str__(self) -> str:
        s = []
        for project in self.project_list:
            s.append(str(project))
        return '\n'.join(s)

class CustomAttribute:
    def __init__(self, info:dict):
        self.name:str = info.get('name', '') # required
        self.namespace:str = info.get('namespace', '') # required
        self.value:str = info.get('value', '') # required

        if self.name == '' or self.namespace == '' or self.value == '':
            raise MissingRequiredField(f'name, namespace and value should be present for customAttribute!')
        
    def __str__(self) -> str:
        return f'customAttribute::name={self.name},namespace={self.namespace},value{self.value}'

class CustomField:
    def __init__(self, info:dict):
        self.customFieldId:str = info.get('customFieldId', '') # required
        self.sourceType:str = info.get('sourceType', '')
        self.value:str = info.get('value', '')

        if self.customFieldId == '':
            raise MissingRequiredField(f'customFieldId should be present for customField!')
        
    def __str__(self) -> str:
        return f'customField::customFieldId={self.customFieldId},sourceType={self.sourceType},value{self.value}'


class TimeEntry: # this class is mainly used for data validation
    _field2expected_type = {
        'billable': bool,
        'customAttributes': [CustomAttribute],
        'customFields': [CustomField],
        'description': str,
        'end': str,
        'projectId': str,
        'start': str,
        'tagIds': [str],
        'taskId': str,
        'type': str
    }
    def __init__(self, info:dict, do_validate:bool=True):
        self.billable:bool = info.get('billable', None)
        self.customAttributes:list[CustomAttribute] = [CustomAttribute(i) for i in info.get('customAttributes', [])]
        self.customFields:CustomField = [CustomField(i) for i in info.get('customFields', [])]
        self.description:str = info.get('description', None)
        self.end:str = info.get('end', None)
        self.projectId:str = info.get('projectId', None)
        self.start:str = info.get('start', None)
        self.tagIds:list[str] = info.get('tagIds', None)
        self.taskId:str = info.get('taskId', None)
        self.type:str = info.get('type', None)

        if self.customAttributes == []:
            self.customAttributes = None
        if self.customFields == []:
            self.customFields = None
        
        if do_validate:
            self.validate()
    
    def get_custom_attributes(self) -> list[str]:
        return [attribute for attribute in self.__dir__() if not (attribute.startswith('_') or callable(self.__getattribute__(attribute)))]

    def validate(self):
        attributes = self.get_custom_attributes()
        checks = []
        for attribute in attributes:
            value = self.__getattribute__(attribute)
            if value is None:
                continue
            expected_type = self._field2expected_type[attribute]
            is_valid = True
            if isinstance(expected_type, list):
                if not isinstance(value, list):
                    is_valid = False
                else:
                    is_valid = all([isinstance(v, expected_type[0]) for v in value])
            else: 
                is_valid = isinstance(value, expected_type)
            checks.append(is_valid)
        if not all(checks):
            raise InvalidTimeEntry
        print(f'Time entry validated: {self}')
    
    def to_dict(self) -> dict:
        attributes = self.get_custom_attributes()
        d = {}
        for attribute in attributes:
            value = self.__getattribute__(attribute)
            if not (value is None):
                d[attribute] = value
        return d
    
    def __str__(self) -> str:
        attributes = self.get_custom_attributes()
        s = ['timeEntry::']
        for attribute in attributes:
            value = self.__getattribute__(attribute)
            if not (value is None):
                s.append(f'- {attribute} = {value}')
        return '\n'.join(s)
