from .base import *

prod = True

if prod:
    print('ben calistim')
    from .production import *
else:
    print('ben calistim dev')
    from .development import *
