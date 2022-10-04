from .base import *

prod = os.getenv("ENV_VAR", 'False').lower() in ('true', '1', 't', "True")

if prod:
    from .production import *
else:
    from .development import *
