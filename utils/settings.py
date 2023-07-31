from dotenv import dotenv_values

settings = dotenv_values('.env')

SECRET_KEY = settings['SECRET_KEY']
ALGORITHM = settings['ALGORITHM']
TOKEN_EXPIRATION_TIME_IN_MIN = int(settings['TOKEN_EXPIRATION_TIME_IN_MIN'])
POSTGRES_USER = settings['POSTGRES_USER']
POSTGRES_PASSWORD = settings['POSTGRES_PASSWORD']
ENDPOINT = settings['ENDPOINT']
PORT = int(settings['PORT'])
DB = settings['DB']