
import pandas as pd
import requests
import click
import json
import configparser
from .functionscli import *
from sqlalchemy import create_engine
# from ...backend.backendfunctions import *
# from ...backend.helpers import *
from django.db import connections
from django.conf import settings

AUTH_TOKEN_HEADER = 'x-observatory-auth'
authentication_info = 'Authentication.ini'

@click.group()
def main():
    pass

@click.command(help = "Database Connection Check")
def healthcheck():
    print_response(requests.get("http://127.0.0.1:9103/interoperability/api/admin/healthcheck"))

@click.command(help = "Reset passes table and superuser")
def resetpasses():
    print_response(requests.post("http://127.0.0.1:9103/interoperability/api/admin/resetpasses"))

@click.command(help = "Reset stations table")
def resetstations():
    print_response(requests.post("http://127.0.0.1:9103/interoperability/api/admin/resetstations"))

@click.command(help = "Reset vehicles table")
def resetvehicles():
    print_response(requests.post("http://127.0.0.1:9103/interoperability/api/admin/resetvehicles"))

@click.command(help = "Passes for a given station for a specific time period")
@click.option("--station", required=True, type=str)
@click.option("--datefrom", required=True, type=str)
@click.option("--dateto", required=True, type=str)
@click.option("--format", default="json",required = False, type=str)
def passesperstation(station, datefrom, dateto, format):
    print_response(requests.get("http://127.0.0.1:9103/interoperability/api/PassesPerStation/{0}/{1}/{2}?format={3}" \
                                .format(station,datefrom,dateto,format), headers=get_headers()))

@click.command(help ="Passes of vehicles with op2 tag from station operated by op1 for a give time period")
@click.option("--op1", required=True, type=str)
@click.option("--op2", required=True, type=str)
@click.option("--datefrom", required=True, type=str)
@click.option("--dateto", required=True, type=str)
@click.option("--format", default="json",required = False, type=str)
def passesanalysis(op1, op2, datefrom, dateto, format):
    print_response(requests.get("http://127.0.0.1:9103/interoperability/api/PassesAnalysis/{0}/{1}/{2}/{3}?format={4}" \
                                .format(op1,op2,datefrom,dateto,format), headers=get_headers()))

@click.command(help ="Cost for passes of vehicles with op2 tag from station operated by op1 for a give time period")
@click.option("--op1", required=True, type=str)
@click.option("--op2", required=True, type=str)
@click.option("--datefrom", required=True, type=str)
@click.option("--dateto", required=True, type=str)
@click.option("--format", default="json",required = False, type=str)
def passescost(op1, op2, datefrom, dateto, format):
    print_response(requests.get("http://127.0.0.1:9103/interoperability/api/PassesCost/{0}/{1}/{2}/{3}?format={4}" \
                                .format(op1,op2,datefrom,dateto,format), headers=get_headers()))

@click.command(help="Charges for op to all the other operators")
@click.option("--op", required=True, type=str)
@click.option("--datefrom", required=True, type=str)
@click.option("--dateto", required=True, type=str)
@click.option("--format", default="json",required = False, type=str)
def chargesby(op, datefrom, dateto, format):
    print_response(requests.get("http://127.0.0.1:9103/interoperability/api/ChargesBy/{0}/{1}/{2}?format={3}" \
                                .format(op,datefrom,dateto,format), headers=get_headers()))

@click.command(help = "Login User")
@click.option("--username", required=True, type=str)
@click.option("--passw", required=True, type=str)
def login(username,passw):
    if not username.isalnum():
        print("username is not alphanumerical")
    else:
        response = get_login_response(username, passw)
        if response.status_code==200:
            json_data = json.loads(response.text)
            login_authentication(username, json_data['token'])
            click.echo("User Logged In ")
        else:
            click.echo("There was an error in authentication")

@click.command(help = "Logout User")
def logout():
    response = get_logout_response()
    if response.status_code==200:
        click.echo("UserLoggedOut")
        logout_authentication()
    else:
        print_response(response)

@click.command()
def printtoken():
    params = get_headers()
    click.echo(params)

# @click.command(help ="Admin Options")
# @click.option("--usermod", required=True, type=str)
# @click.option("--username", required=True, type=str)
# @click.option("--passw", required=True, type=str)
# @click.option("--passesup", required=True, type=str)
# @click.option("--source", default="json",required = False, type=str)
# def passescost(op1, op2, datefrom, dateto, format):
#     print_response(requests.get("http://127.0.0.1:9103/interoperability/api/PassesCost/{0}/{1}/{2}/{3}?format={4}" \
#                                 .format(op1,op2,datefrom,dateto,format), headers=get_headers()))


# @click.command()
# @click.option("--source", required=True, type=str)
# def passesupd(source):        
#         alchemyEngine   = create_engine(get_connection_string())
#         dbConnection    = alchemyEngine.connect()
#         passdf = pd.read_csv(source, index_col=0)
#         passdf.drop(columns=["date"], inplace=True)
#         insert_df_to_sql_table(passdf, "api_passes", dbConnection)

main.add_command(healthcheck)
main.add_command(resetpasses)
main.add_command(resetstations)
main.add_command(resetvehicles)
main.add_command(passesperstation)
main.add_command(passesanalysis)
main.add_command(passescost)
main.add_command(chargesby)
# main.add_command(passesupd)
main.add_command(login)
main.add_command(logout)
main.add_command(printtoken)

if __name__ == '__main__':
    main()