pwd = '..'
import os
from sys import path
path.insert(0, pwd)
from yaml import safe_load
from datetime import datetime, timedelta
from simplify_clockify_utils import Handler4PostingTimeEntries

handler = Handler4PostingTimeEntries(configs_file=os.path.join('configs.yaml'))

with open('../entries.yaml', 'r') as fp:
    data:list[dict] = safe_load(fp)

for record in data:
    startDate = datetime.date(datetime.strptime(record['startDate'], '%Y-%m-%d'))
    startTime = datetime.time(datetime.strptime(record['startTime'], '%H:%M'))
    taskStartTime = datetime.combine(startDate, startTime)
    for task in record['tasks']:
        description:str = task.get('description', '')
        timeTaken:float = float(task.get('timeTaken', 1))
        projectName:str = task.get('projectName', 'FDH-NA')
        billable:bool = task.get('billable', False)

        recordTaskStartTime = datetime.strftime(taskStartTime, '%Y-%m-%dT%H:%M:%SZ')
        taskEndTime = taskStartTime + timedelta(hours=timeTaken)
        recordTaskEndTime = datetime.strftime(taskEndTime, '%Y-%m-%dT%H:%M:%SZ')
        taskStartTime = taskEndTime

        response = handler.post_time_entry_using_params(description, recordTaskStartTime, recordTaskEndTime, projectName, billable)
        print(f"\nRESPONSE: {response}\n")