from dotenv import load_dotenv
import os
load_dotenv()
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")

database_name = DB_NAME
database_domain = DB_USER + ":" + DB_PASSWORD + "@" + DB_HOST

# database_path = 'postgres://{}/{}'.format('localhost:5432', database_name)
database_path = 'postgres+psycopg2://{}/{}'.format(database_domain, database_name)
