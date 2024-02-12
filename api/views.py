from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework_csv.renderers import CSVRenderer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from accounts.models import User

from backend.models import *
from backend.serializers import *
from backendfunctions import healthcheckdb, get_connection_string
from helpers import *

class index(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer, CSVRenderer]
    
    def get(self, request):
        return Response(data = {"homepage":"This is homepage!"}, status = status.HTTP_200_OK)

class healthcheck(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer, CSVRenderer]
    
    def get(self, request):
        connection_string = get_connection_string()
        if healthcheckdb():
            return Response(data = {"status":"OK", "dbconnection":connection_string}, status = status.HTTP_200_OK)
        else:
            return Response(data = {"status":"failed", "dbconnection":connection_string}, status = status.HTTP_200_OK)

class resetstations(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer, CSVRenderer]

    def post(self,request):
        if healthcheckdb():
            station = Station()
            station.resetstations()
            return Response({'status':'OK'},status = status.HTTP_200_OK)
        else:
            return Response({'status':'failed'},status = status.HTTP_200_OK)

class resetvehicles(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer, CSVRenderer]
    def post(self,request):
        if healthcheckdb():
            vehicle = Vehicle()
            vehicle.resetvehicles()
            return Response({'status':'OK'},status = status.HTTP_200_OK)
        else:
            return Response({'status':'failed'},status = status.HTTP_200_OK)

class resetpasses(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer, CSVRenderer]
    def post(self,request):
        if healthcheckdb():
            passvar = Pass()
            passvar.resetpasses()           
            try:
                user = User.objects.get(username='admin')
                flag = True
            except:
                flag = False
            
            if flag:
                user.delete()
                User.objects.create_superuser(username="admin", password="freepasses4all")
            else:
                User.objects.create_superuser(username="admin", password="freepasses4all")
                
            return Response({'status':'OK'},status = status.HTTP_200_OK)
        else:
            return Response({'status':'failed'}, status = status.HTTP_200_OK)

class passesperstationindex(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]
    def get(self,request):
        request_user = "nea_odos"
        stationsOperator = Station.objects.filter(stationProvider=request_user).values_list("stationID", flat=True)
        if not stationsOperator.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"nea_odos":list(stationsOperator)}, status = status.HTTP_200_OK)

class passesanalysisindex(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]
    def get(self,request):
        loggedOperator="nea_odos" 
        # loggedusername = request.user
        operatorsList = Station.objects.distinct('stationProvider').exclude(stationProvider=loggedOperator)\
                                          .values_list('stationProvider', flat=True)
        if not operatorsList.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"loggedOperator": loggedOperator, "operatorsList": list(operatorsList)}, status = status.HTTP_200_OK)

class passescostindex(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]
    def get(self,request):
        # user = request.user
        loggedOperator="nea_odos" 
        operatorsList = Station.objects.distinct('stationProvider').exclude(stationProvider=loggedOperator)\
                                          .values_list('stationProvider', flat=True)
        if not operatorsList.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"loggedOperator": loggedOperator, "operatorsList": list(operatorsList)}, status = status.HTTP_200_OK)

class chargesbyindex(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer, CSVRenderer]
    def get(self,request):
        request_user = "nea_odos"
        # stationsOperator = Station.objects.filter(stationProvider=request_user).values_list("stationID", flat=True)
        # if not stationsOperator.exists():
        #     return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"loggedOperator": request_user}, status = status.HTTP_200_OK)

class passesperstation(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer, CSVRenderer]
    def get(self, request, stationID, date_from, date_to):
        start_date = get_date_from_string(date_from)
        end_date = get_date_from_string(date_to)
        if start_date and end_date and validate_date(start_date) and validate_date(end_date): 
            filtered_passes_per_station = Pass().getPassesPerStation(stationID, start_date, end_date)
            if not filtered_passes_per_station.exists():
                return Response(status=status.HTTP_204_NO_CONTENT)

            nr_passes = filtered_passes_per_station.count()
            serializer = PassSerializer(filtered_passes_per_station, many=True)

            serializer_list = list(serializer.data)
            passes_list=[]
            for i in range(0,nr_passes):
                flag = Station().getOperatorFromStationID(stationID=stationID)==\
                       Vehicle().getOperatorFromVehicleID(serializer_list[i]["vehicleRef"])
                pass_to_append = {
                    "PassIndex": i+1,
                    "PassId": serializer_list[i]['passID'],
                    "PassTimeStamp": serializer_list[i]['timestamp'],
                    "VehicleID": serializer_list[i]['vehicleRef'],
                    "TagProvider": Vehicle().getOperatorFromVehicleID(serializer_list[i]["vehicleRef"]),
                    "PassType": "home" if flag else "visitor",
                    "PassCharge": serializer_list[i]['charge']
                }
                passes_list.append(pass_to_append)

            output_response = {
                "Station": stationID,
                "StationOperator": Station().getOperatorFromStationID(stationID=stationID),
                "RequestTimestamp": datetime.datetime.now().strftime(("%d/%m/%Y, %H:%M:%S")),
                "PeriodFrom": start_date.strftime("%d/%m/%Y"),
                "PeriodTo": end_date.strftime("%d/%m/%Y"),
                "NumberOfPasses": nr_passes,
                "PassesList": passes_list
            }

            return Response(output_response, status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

class passesanalysis(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, op1_ID, op2_ID, date_from, date_to):
        start_date = get_date_from_string(date_from)
        end_date = get_date_from_string(date_to)
        if start_date and end_date and validate_date(start_date) and validate_date(end_date):
            filtered_passes_analysis = Pass().getPassesAnalysis(op1_ID, op2_ID, start_date, end_date)
            if not filtered_passes_analysis.exists():
                return Response(status=status.HTTP_204_NO_CONTENT)
            nr_passes = filtered_passes_analysis.count()
            serializer = PassSerializer(filtered_passes_analysis, many=True)

            serializer_list = list(serializer.data)
            passes_list=[]
            for i in range(0,nr_passes):
                flag = Station().getOperatorFromStationID(serializer_list[i]["stationRef"])==\
                       Vehicle().getOperatorFromVehicleID(serializer_list[i]["vehicleRef"])
                pass_to_append = {
                    "PassIndex": i+1,
                    "PassId": serializer_list[i]['passID'],
                    "StationID": serializer_list[i]['stationRef'],
                    "TimeStamp": serializer_list[i]['timestamp'],
                    "VehicleID": serializer_list[i]['vehicleRef'],
                    "Charge": serializer_list[i]['charge']
                }
                passes_list.append(pass_to_append)

            output_response = {
                "op1_ID": op1_ID,
                "op2_ID": op2_ID,
                "RequestTimestamp": datetime.datetime.now().strftime(("%d/%m/%Y, %H:%M:%S")),
                "PeriodFrom": start_date.strftime("%d/%m/%Y"),
                "PeriodTo": end_date.strftime("%d/%m/%Y"),
                "NumberOfPasses": nr_passes,
                "PassesList": passes_list
            }
            return Response(output_response, status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)


class passescost(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, op1_ID, op2_ID, date_from, date_to):
        start_date = get_date_from_string(date_from)
        end_date = get_date_from_string(date_to)
        if start_date and end_date and validate_date(start_date) and validate_date(end_date):
            filtered_passes_analysis = Pass().getPassesAnalysis(op1_ID, op2_ID, start_date, end_date)
            if not filtered_passes_analysis.exists():
                return Response(status=status.HTTP_204_NO_CONTENT)
            nr_passes = filtered_passes_analysis.count()
            passes_cost = round(filtered_passes_analysis.aggregate(models.Sum('charge'))['charge__sum'], 2)
            output_response = {
                "op1_ID": op1_ID,
                "op2_ID": op2_ID,
                "RequestTimestamp": datetime.datetime.now().strftime(("%d/%m/%Y, %H:%M:%S")),
                "PeriodFrom": start_date.strftime("%d/%m/%Y"),
                "PeriodTo": end_date.strftime("%d/%m/%Y"),
                "NumberOfPasses": nr_passes,
                "PassesCost": passes_cost
            }
            return Response(output_response, status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

class chargesby(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, op_ID, date_from, date_to):
        start_date = get_date_from_string(date_from)
        end_date = get_date_from_string(date_to)
        if start_date and end_date and validate_date(start_date) and validate_date(end_date):
            operatorsList = Station.objects.distinct('stationProvider').exclude(stationProvider=op_ID)\
                            .values_list('stationProvider', flat=True)
        
            ppolist=[]
            for operator in operatorsList:
                #calcuate passescost for visitor to home
                filtered_passes_analysis_home = Pass().getPassesAnalysis(op_ID, operator, start_date, end_date)
                if filtered_passes_analysis_home.exists():
                    nr_passes = filtered_passes_analysis_home.count()
                    passes_cost_home = round(filtered_passes_analysis_home.aggregate(models.Sum('charge'))['charge__sum'], 2)
                else:
                    passes_cost_home = 0 
                    nr_passes=0
                #calculate passescost for home to visitor
                filtered_passes_analysis_visitor = Pass().getPassesAnalysis(operator, op_ID, start_date, end_date)
                if filtered_passes_analysis_visitor.exists():
                    passes_cost_visitor = round(filtered_passes_analysis_visitor.aggregate(models.Sum('charge'))['charge__sum'], 2)
                else:
                    passes_cost_visitor = 0 
                
                op_dict = {
                    "VisitingOperator": operator,
                    "NumberOfPasses": nr_passes,
                    "PassesCost": round(passes_cost_home-passes_cost_visitor,2)
                }
                ppolist.append(op_dict)
            
            output_response={
                "op_ID": op_ID,
                "RequestTimestamp": datetime.datetime.now().strftime(("%d/%m/%Y, %H:%M:%S")),
                "PeriodFrom": start_date.strftime("%d/%m/%Y"),
                "PeriodTo": end_date.strftime("%d/%m/%Y"),
                "PPOList": ppolist
            }
            return Response(output_response, status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
