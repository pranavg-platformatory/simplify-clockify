pwd = '..'
import os
from sys import path
path.insert(0, pwd)
from simplify_clockify_utils import Handler4GettingSetupInfo
from sys import argv

handler= Handler4GettingSetupInfo(configs_file=os.path.join(pwd, 'configs.yaml'))
response = handler.get(argv[1])
print(response.json())
