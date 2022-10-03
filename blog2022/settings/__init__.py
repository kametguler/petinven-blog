from .base import *

prod = False

if prod:
    print('ben calistim')
    from .production import *
else:
    print('ben calistim dev')
    from .development import *
