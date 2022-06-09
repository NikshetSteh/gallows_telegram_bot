TOKEN = "5363987082:AAF0g60EIWiKVNvg7VtW-6e_M41lkS50hzM"

DATABESE_PATH = "data\db\database.sqlite3"

USE_WEBHOOK = True

# host settings
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 8000