from .config import *
from . import country

try:
    from .local_config import *
except:
    pass

try:
    from local_config import *
except:
    pass

try:
    from newstest_config import *
except:
    pass
