#!D:\git\di5cheng-IT-PaaS\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'aioworkers==0.13.0','console_scripts','aioworkers'
__requires__ = 'aioworkers==0.13.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('aioworkers==0.13.0', 'console_scripts', 'aioworkers')()
    )
