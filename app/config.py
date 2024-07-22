from dotenv import load_dotenv
import os


app_secret_key = os.environ.get('APP_SECRET_KEY')

sqlalchemy_database_uri = os.environ.get('MY_SQLALCHEMY_DATABASE_URI')

sender_email = os.environ.get('SENDER_EMAIL') 

sender_password = os.environ.get('SENDER_PASSWORD') 