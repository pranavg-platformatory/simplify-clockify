from.handler4getting_setup_info import Handler4GettingSetupInfo
from .models import TimeEntry
from typing import Any
from datetime import datetime, timedelta

class Handler4PostingTimeEntries(Handler4GettingSetupInfo):
    def __init__(self, configs_file:str='configs.yaml'):
        '''`handler4configs` overrides `configs_file` if not None.'''

        super().__init__(configs_file, handler4configs=None, store=True)

    #================================================

    def _post_time_entry_to_workspace_id(self, time_entry:TimeEntry) -> Any:
        return self.post(f'workspaces/{self.workspace.id}/time-entries', time_entry.to_dict()).json()

    #================================================
    
    def post_time_entry_using_dict(self, time_entry_dict:dict) -> Any:
        time_entry = TimeEntry(time_entry_dict) # intermediate validation step
        return self._post_time_entry_to_workspace_id(time_entry)
    
    #================================================
    # Post time entry to workspace using user-friendly parameters

    def post_time_entry_using_params(
        self,
        description:str,
        startTime:str,
        endTime:str,
        projectName:str='FDH-NA',
        billable:bool=False
    ) -> Any:
        time_entry_dict = {
            'description': description,
            'start': startTime,
            'end': endTime,
            'projectId': self.projects.get_id_for_name(projectName),
            'billable': billable
        }
        time_entry = TimeEntry(time_entry_dict) # intermediate validation step
        return self._post_time_entry_to_workspace_id(time_entry)

    #================================================
    # Post multiple time entries to workspace using the object derived from entries.yaml

    def post_time_entry_using_entries_yaml_object(self, data:list[dict]) -> list[Any]:
        time_entry_list = []
        for record in data:
            startDate = datetime.date(datetime.strptime(record['startDate'], '%Y-%m-%d'))
            startTime = datetime.time(datetime.strptime(record['startTime'], '%H:%M'))
            taskStartTime = datetime.combine(startDate, startTime)
            for task in record['tasks']:
                # Read values
                description:str = str(task.get('description', task.get('d', '')))
                timeTaken:float = float(task.get('timeTaken', task.get('t', 1)))
                projectName:str = str(task.get('projectName', task.get('p', 'FDH-NA')))
                billable:bool = bool(task.get('billable', task.get('b', False)))

                # Derived values
                projectId:str = self.projects.get_id_for_name(projectName)
                recordTaskStartTime:str = datetime.strftime(taskStartTime, '%Y-%m-%dT%H:%M:%SZ')
                taskEndTime:datetime = taskStartTime + timedelta(hours=timeTaken)
                recordTaskEndTime:str = datetime.strftime(taskEndTime, '%Y-%m-%dT%H:%M:%SZ')
                taskStartTime:datetime = taskEndTime

                # Construct time entry
                time_entry_dict = {
                    'description': description,
                    'start': recordTaskStartTime,
                    'end': recordTaskEndTime,
                    'projectId': projectId,
                    'billable': billable
                }

                # Intermediate validation step
                time_entry = TimeEntry(time_entry_dict)

                # Append to list
                time_entry_list.append(time_entry)
        
        responses = []
        for time_entry in time_entry_list:
            responses.append(self._post_time_entry_to_workspace_id(time_entry))
        return responses