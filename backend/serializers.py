from rest_framework import serializers
from .models import *


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['stationID','stationProvider','stationName']

class StationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['stationID']

class VehicleSerializer(serializers.Serializer):
    vehicleID = serializers.CharField(max_length=255)
    tagID = serializers.CharField(max_length=255)
    tagProvider = serializers.CharField(max_length=255)
    providerAbbr = serializers.CharField(max_length=255)
    licenseYear = serializers.IntegerField()

    def create(self, validated_data):
        return Vehicle.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.vehicleID = validated_data.get('vehicleID', instance.vehicleID)
        instance.vehicleProvider = validated_data.get('vehicleProvider', instance.vehicleProvider)
        instance.vehicleName = validated_data.get('vehicleName', instance.vehicleName)
        instance.save()
        return instance

class PassSerializer(serializers.Serializer):
    passID = serializers.CharField(max_length=255)
    timestamp = serializers.DateTimeField()
    stationRef = serializers.CharField(max_length=255)
    vehicleRef = serializers.CharField(max_length=255)
    charge = serializers.FloatField()

    def create(self, validated_data):
        return Pass.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.passID = validated_data.get('passID', instance.passID)
        instance.timestamp = validated_data.get('timestamp', instance.timestamp)
        instance.stationRef = validated_data.get('stationRef', instance.stationRef)
        instance.vehicleRef = validated_data.get('vehicleRef', instance.vehicleRef)
        instance.charge = validated_data.get('charge', instance.charge)
        instance.save()
        return instance

class PassPerStationList(serializers.Serializer):
    passID = serializers.CharField(max_length=255)
    timestamp = serializers.DateTimeField()
