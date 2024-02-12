#!\meta_env\Scripts\python.exe
import psycopg2
from sqlalchemy import create_engine
from configparser import ConfigParser

#Config function

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

# Create Database
def create_database():
   try:
      # read connection parameters
      params = config(filename = "database.ini")
      # connect to the PostgreSQL server
      print('Connecting to the PostgreSQL database...')
      conn = psycopg2.connect(**params)
      conn.autocommit = True
      # create a cursor
      cur = conn.cursor() 
      sqlcommands = (
      """DROP DATABASE IF EXISTS metadb""",
      """CREATE DATABASE metadb"""
      )

   # execute a statement
      for command in sqlcommands:
         cur.execute(command)
      # cur.execute("SELECT version()")
   except (Exception, psycopg2.DatabaseError) as error:
      print(error)
   finally:
      if conn is not None:
         conn.close()

   #Create Tables

   try:
      # read connection parameters
      params = config(filename = "metadb.ini")
      # connect to the PostgreSQL server
      print('Connecting to the PostgreSQL database...')
      conn = psycopg2.connect(**params)
      conn.autocommit = True
      # create a cursor
      cur = conn.cursor()
      tablecommands = (
      """
      CREATE TABLE Stations (
         stationID VARCHAR(255) PRIMARY KEY,
         stationProvider VARCHAR(255) NOT NULL,
         stationName VARCHAR(255) NOT NULL
      )
      """,
      """ CREATE TABLE Vehicles (
               vehicleID VARCHAR(255) PRIMARY KEY,
               tagID VARCHAR(255) NOT NULL,
               tagProvider VARCHAR(255) NOT NULL,
               providerAbbr VARCHAR(255) NOT NULL,
               licenseYear INT NOT NULL
               )
      """,
      """
      CREATE TABLE Passes (
               passID VARCHAR(255) PRIMARY KEY,
               timestamp TIMESTAMP NOT NULL,
               stationRef VARCHAR(255) NOT NULL,
               vehicleRef VARCHAR(255) NOT NULL,
               charge REAL NOT NULL
      )
      """)
   # execute a statement
      print('PostgreSQL database version:')
      # cur.execute(sql)
      # cur.execute("SELECT version()")
      for command in tablecommands:
         cur.execute(command)
   except (Exception, psycopg2.DatabaseError) as error:
      print(error)
   finally:
      if conn is not None:
         conn.close()



if __name__ == '__main__':
    create_database()
    print("DB initialization was completed \n")
