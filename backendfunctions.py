from django.db import connections
from django.conf import settings

def healthcheckdb():
    dbConnection = connections['default']
    try:
        # with dbConnection.cursor() as cursor:
        #     cursor.execute("SELECT 1")
        #     return True
        dbConnection.ensure_connection()
    except:
        return False

    return True

def get_connection_string(db='default'):
    user = settings.DATABASES[db]['USER']
    password = settings.DATABASES[db]['PASSWORD']
    database_name = settings.DATABASES[db]['NAME']
    host = settings.DATABASES[db]['HOST']
    port = settings.DATABASES[db]['PORT']
    # connection_string = 'postgresql+psycopg2://'+params['user']+':'+params['password']+'@'+params['host']+'/'+params['database']
    connection_string ='postgresql://{user}:{password}@{host}:5432/{database_name}'.format(
        user=user,
        password=password,
        database_name=database_name,
        host=host,
    )
    return connection_string
    
