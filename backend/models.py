from django.db import models

# Create your models here.

from django.db import models
import pandas as pd
from sqlalchemy import create_engine, table
from helpers import insert_df_to_sql_table, config
from django.db import connections
from backendfunctions import get_connection_string
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Station(models.Model):
    stationID = models.CharField(max_length=255, primary_key=True)
    stationProvider = models.CharField(max_length=255)
    stationName = models.CharField(max_length=255)

    def __str__(self):
        return self.stationID

    def clearStationTable(self):
        Station.objects.all().delete()

    def getOperatorFromStationID(self, stationID): 
        return Station.objects.get(stationID=stationID).stationProvider

    def insertStationTable(self, input_dir=r"./static/sampledata01_stations.csv", tablename='api_station'):
        alchemyEngine   = create_engine(get_connection_string())
        dbConnection    = alchemyEngine.connect()
        df = pd.read_csv(input_dir, index_col=0, sep = ';')
        insert_df_to_sql_table(df, tablename=Station.objects.model._meta.db_table, dbConnection=dbConnection)

    def resetstations(self):
        self.clearStationTable()
        self.insertStationTable()

class Vehicle(models.Model):
    vehicleID = models.CharField(max_length=255, primary_key=True)
    tagID = models.CharField(max_length=255)
    tagProvider = models.CharField(max_length=255)
    providerAbbr = models.CharField(max_length=255)
    licenseYear = models.IntegerField()

    def __str__(self):
        return self.vehicleID

    def clearVehicleTable(self):
        Vehicle.objects.all().delete()

    def getOperatorFromVehicleID(self, vehicleID): 
        return Vehicle.objects.get(vehicleID=vehicleID).tagProvider

    def getTagIDFromVehicleID(self, vehicleID):
        return Vehicle.objects.get(vehicleID=vehicleID).tagID

    def insertVehicleTable(self, input_dir=r"./static/sampledata01_vehicles_100.csv", tablename='api_vehicle'):
        alchemyEngine   = create_engine(get_connection_string())
        dbConnection    = alchemyEngine.connect()
        df = pd.read_csv(input_dir, index_col=0, sep = ';')
        insert_df_to_sql_table(df, tablename=Vehicle.objects.model._meta.db_table, dbConnection=dbConnection)

    def resetvehicles(self):
        self.clearVehicleTable()
        self.insertVehicleTable()

class Pass(models.Model):
    passID = models.CharField(max_length=255, primary_key=True)
    timestamp = models.DateTimeField()
    stationRef = models.CharField(max_length=255)
    # stationRef = models.ForeignKey(to = Station, on_delete = models.CASCADE)
    vehicleRef = models.CharField(max_length=255)
    # vehicleRef = models.ForeignKey(to = Vehicle, on_delete = models.CASCADE)
    charge = models.FloatField()

    def __str__(self):
        return self.passID

    def passType(self):
        stationOperator = Station.objects.get(stationID=self.stationRef).stationProvider
        tagOperator = Vehicle.objects.get(vehicleID=self.vehicleRef).tagProvider
        if stationOperator==tagOperator:
            output="home"
        else:
            output="visitor"
        return output

    def clearPassTable(self):
        Pass.objects.all().delete()

    def insertPassTable(self, tablename='api_pass'):
        alchemyEngine   = create_engine(get_connection_string())
        dbConnection    = alchemyEngine.connect()
        for day in range(0,500):
            input_dir  = r'./static/days/day'+str(day)+'.csv'
            passdf = pd.read_csv(input_dir, index_col=0)
            passdf.drop(columns=["date"], inplace=True)
            # passdf.columns = map(str.lower, passdf.columns)
            # passdf.index.rename(passdf.index.name.lower(), inplace=True)
            insert_df_to_sql_table(passdf, tablename=Pass.objects.model._meta.db_table, dbConnection=dbConnection)

    def resetpasses(self):
        self.clearPassTable()
        self.insertPassTable()

    def getPassesPerStation(self, stationID, start_date, end_date):
        return Pass.objects.filter(stationRef=stationID).filter(timestamp__range=(start_date,end_date)).order_by('timestamp')

    def stationIDListForOperator(self, operator):
        return list(Station.objects.filter(stationProvider=operator).values_list('stationID', flat = True))

    def vehicleIDListForOperator(self, operator):
        return list(Vehicle.objects.filter(tagProvider=operator).values_list('vehicleID', flat = True))

    def getPassesAnalysis(self, op1_ID, op2_ID, start_date, end_date):
        op1_stations_list = Pass().stationIDListForOperator(op1_ID)
        op2_vehicles_list = Pass().vehicleIDListForOperator(op2_ID)
        passes_filtered = Pass.objects.filter(stationRef__in=op1_stations_list).filter(vehicleRef__in=op2_vehicles_list) \
                                      .filter(timestamp__range=(start_date,end_date)).order_by('timestamp')
        return passes_filtered