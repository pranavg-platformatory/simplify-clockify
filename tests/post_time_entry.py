pwd = '..'
import os
from sys import path
path.insert(0, pwd)
from simplify_clockify_utils import Handler4PostingTimeEntries

handler = Handler4PostingTimeEntries(configs_file=os.path.join(pwd, 'configs.yaml'))
response = handler.post_time_entry_using_dict(
    {
        'billable': False,
        'description': 'Testing Testing 123',
        'end': '2026-06-06T00:00:00Z',
        'start': '2026-06-06T00:00:00Z',
        'projectId': '6888f8f9f6bba6345505d0de'
    }
)
print(response.json())