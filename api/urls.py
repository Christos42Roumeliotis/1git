from django.urls import path, include
from .views import *
from rest_framework import routers

urlpatterns = [
    # path('', include(router.urls)),
    path('', index.as_view(), name='index'),
    path('admin/healthcheck', healthcheck.as_view(), name = "healthcheck" ),
    path('admin/resetstations', resetstations.as_view(), name = "resetstations" ),
    path('admin/resetvehicles', resetvehicles.as_view(), name = "resetvehicles" ),
    path('admin/resetpasses', resetpasses.as_view(), name = "resetpasses" ),
    path('PassesPerStation/', passesperstationindex.as_view(), name = "passesperstationindex"),
    path('PassesPerStation/<str:stationID>/<str:date_from>/<str:date_to>', passesperstation.as_view(), name = "passesperstation"),
    path('PassesAnalysis/', passesanalysisindex.as_view(), name = "passesanalysisindex"),
    path('PassesAnalysis/<str:op1_ID>/<str:op2_ID>/<str:date_from>/<str:date_to>', passesanalysis.as_view(), name = "passesanalysis"),
    path('PassesCost/', passescostindex.as_view(), name = "passescostindex"),
    path('PassesCost/<str:op1_ID>/<str:op2_ID>/<str:date_from>/<str:date_to>', passescost.as_view(), name = "passescost"),
    path('ChargesBy/', chargesbyindex.as_view(), name = "chargesbyindex"),
    path('ChargesBy/<str:op_ID>/<str:date_from>/<str:date_to>', chargesby.as_view(), name = "chargesby"),
]