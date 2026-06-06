pwd = '..'
import os
from sys import path
path.insert(0, pwd)
from simplify_clockify_utils import Handler4GettingSetupInfo

handler= Handler4GettingSetupInfo(configs_file=os.path.join(pwd, 'configs.yaml'))
print(handler.get_user())
print(handler.get_workspace())
print(handler.get_projects())
