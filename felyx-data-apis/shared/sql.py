import os
import dotenv


def get_sql_connection_string():
    dotenv.load_dotenv()   
    return "DRIVER=%(SQL_DRIVER)s;SERVER=%(SQL_SERVER)s;PORT=1433;DATABASE=%(SQL_DATABASE)s;UID=%(SQL_USERNAME)s;PWD={%(SQL_PASSWORD)s}" % os.environ