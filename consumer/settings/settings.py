import os

FROM_EMAIL = os.environ.get('FROM_EMAIL', None)
FROM_EMAIL_NAME = os.environ.get('FROM_EMAIL_NAME', 'EmailSender')
FROM_EMAIL_PASSWORD = os.environ.get('FROM_EMAIL_PASSWORD', None)
BASE_BACKEND_URL = os.environ.get('BASE_BACKEND_URL', 'localhost')


API_KEY = os.environ.get('API_KEY', None)

