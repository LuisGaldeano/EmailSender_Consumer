import os

FROM_EMAIL = os.environ.get('FROM_EMAIL')
FROM_EMAIL_NAME = os.environ.get('FROM_EMAIL_NAME', 'EmailSender')
FROM_EMAIL_PASSWORD = os.environ.get('FROM_EMAIL_PASSWORD')

