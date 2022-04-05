import re
import sys

from pytest import main

try:
    import ipdb as debugger
except ImportError:
    import pdb as debugger

sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])

if '--dbg' in sys.argv:
    sys.argv.remove('--dbg')
    debugger.set_trace()
sys.exit(main())
