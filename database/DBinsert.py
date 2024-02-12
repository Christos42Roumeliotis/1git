#!\meta_env\Scripts\python.exe
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from configparser import ConfigParser
import time
import os
import sched

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

def insert_data():
   #Read data as dataframes
   stations = pd.read_csv(r"./sampledata01/sampledata01_stations.csv", index_col=0, sep = ';')
   stations.columns = map(str.lower, stations.columns)
   stations.index.rename(stations.index.name.lower(), inplace=True)
   vehicles = pd.read_csv(r"./sampledata01/sampledata01_vehicles_100.csv", index_col=0, sep = ';')
   vehicles.columns = map(str.lower, vehicles.columns)
   vehicles.index.rename(vehicles.index.name.lower(), inplace=True)

   params = config(filename = "metadb.ini")
   # Create an engine instance
   connection_string = 'postgresql+psycopg2://'+params['user']+':'+params['password']+'@'+params['host']+'/'+params['database']
   alchemyEngine   = create_engine(connection_string)
   # Connect to PostgreSQL server
   dbConnection    = alchemyEngine.connect()

   def insert_df_to_sql_table(dataframe, tablename, dbConnection):
    try:

        dataframe.to_sql(tablename, dbConnection, if_exists='append')

    except ValueError as vx:

        print(vx)

    except Exception as ex:  

        print(ex)
   
   insert_df_to_sql_table(vehicles, "vehicles", dbConnection)
   insert_df_to_sql_table(stations, "stations", dbConnection)


   ndays = len(os.listdir("./days/"))

   def insert_daypass(day):
      input_dir  = "./days/day"+str(day)+".csv"
      passdf = pd.read_csv(input_dir, index_col=0)
      passdf.drop(columns=["date"], inplace=True)
      passdf.columns = map(str.lower, passdf.columns)
      passdf.index.rename(passdf.index.name.lower(), inplace=True)
      insert_df_to_sql_table(passdf, "passes", dbConnection)  
   
   for day in range(0,300):
      insert_daypass(day)
   

   s = sched.scheduler(time.time, time.sleep)
   def do_something(sc, day, ndays): 
      day+=1
      print("Inserting Day"+str(day))

      insert_daypass(day)
    
      if day <ndays-1:
      # do your stuff
         s.enter(1, 1, do_something, (sc, day, ndays))

   s.enter(1, 1, do_something, (s, day, ndays))
   s.run()

   dbConnection.close()

if __name__ == '__main__':
    insert_data()
    print("DB initialization was completed \n")