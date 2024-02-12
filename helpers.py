from configparser import RawConfigParser
import pandas as pd
import datetime

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = RawConfigParser()
    parser.optionxform = str
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


def insert_df_to_sql_table(dataframe, tablename, dbConnection):
    try:
        dataframe.to_sql(tablename, dbConnection, if_exists='append')

    except ValueError as vx:

        print(vx)

    except Exception as ex:  

        print(ex)

def validate_date(input_date):
    if isinstance(input_date, datetime.date):
        flag = input_date<=datetime.date.today() and input_date>datetime.date(2018,12,31)
    else :
        flag = False
    return flag

get_string_date = lambda x : str(x[0:4])+"-"+str(x[4:6])+"-"+str(x[6:8]) if len(x)==8 and x.isdecimal() else False

def get_date_from_string(date_string):
    date_string = get_string_date(date_string)
    try:
        date_output = datetime.datetime.strptime(date_string,"%Y-%m-%d").date()
        return date_output
    except:
        return False