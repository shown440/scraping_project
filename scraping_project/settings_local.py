from scraping_project.settings import *

from datetime import timedelta
import json
import os 


with open(BASE_DIR / 'env.json', 'r') as envf:
    env_ = json.load(envf)


# SECRET_KEY = os.getenv("SECRET_KEY") 
SECRET_KEY = env_["SECRET_KEY"] 
JWT_HASH_ALGO = env_["JWT_HASH_ALGO"] 



DATABASES = env_['dbconf']


# REST FRAMEWORK SETUP
REST_FRAMEWORK = { 
    # Default pagination setup
    'DEFAULT_PAGINATION_CLASS': 'mixins.pagination_mixins.pagination.StandardResultsSetPagination',

    # JWT AUTHENTICATION
    'DEFAULT_AUTHENTICATION_CLASSES': ( 
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    
}

# JWT CONFIGURATION
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30), #minutes=30
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': JWT_HASH_ALGO,    #'HS512',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=30), #minutes=30
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
}


# ### --------------------------------------------------------------- ###
# ### START Mail configuration
# ### --------------------------------------------------------------- ###
# # EMAIL_CONFIG = env_['pending_user_mail_conf']
# EMAIL_CONFIG = env_['pending_user_mail_conf_bhutan_adss']

# EMAIL_BACKEND = EMAIL_CONFIG['EMAIL_BACKEND']
# EMAIL_HOST = EMAIL_CONFIG['EMAIL_HOST']
# EMAIL_USE_TLS = EMAIL_CONFIG['EMAIL_USE_TLS']   
# EMAIL_PORT = EMAIL_CONFIG['EMAIL_PORT']
# EMAIL_HOST_USER = EMAIL_CONFIG['EMAIL_HOST_USER']
# EMAIL_HOST_PASSWORD = EMAIL_CONFIG['EMAIL_HOST_PASSWORD'] 
# ### --------------------------------------------------------------- ###
# ### END Mail configuration
# ### --------------------------------------------------------------- ###