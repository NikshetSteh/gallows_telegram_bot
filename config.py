import os

TOKEN = os.getenv("TOKEN")

USE_WEBHOOK = True

#database host setting
DATABESE_HOST = os.getenv("DATABESE_HOST")
DATABESE_USER = os.getenv("DATABESE_USER")
DATABESE_PASSWORD = os.getenv("DATABESE_PASSWORD")

# host settings
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)