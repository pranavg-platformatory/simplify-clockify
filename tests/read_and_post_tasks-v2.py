pwd = '..'
import os
from sys import path
path.insert(0, pwd)
from yaml import safe_load
from simplify_clockify_utils import Handler4PostingTimeEntries

handler = Handler4PostingTimeEntries(configs_file=os.path.join(pwd, 'configs.yaml'))

with open(os.path.join(pwd, 'entries.yaml'), 'r') as fp:
    data:list[dict] = safe_load(fp)

response = handler.post_time_entry_using_entries_yaml_object(data)
print(response)