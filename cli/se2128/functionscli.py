import click
import requests
import json
import configparser

authentication_info = 'Authentication.ini'
AUTH_TOKEN_HEADER = 'x-observatory-auth'
# AUTH_TOKEN_HEADER = 'Authorization'


def print_response(response, format="json"):
    if response.status_code==200:
        click.echo("Success")
        if format=="json":
            click.echo(json.dumps(response.json(), indent=2))
    elif response.status_code==204:
        click.echo("Bad request")
    elif response.status_code==401:
        click.echo("Not authorized")
    elif response.status_code==402:
        click.echo("No data")
    else:
        click.echo("Internal server error")

def login_authentication(username, token):
    parser = configparser.ConfigParser()
    parser['AUTHENTICATION'] = {'username': username, 'token': 'token '+token}
    
    with open(authentication_info, 'w') as configfile:
        parser.write(configfile)

def logout_authentication():
    parser = configparser.ConfigParser()
    parser['AUTHENTICATION'] = {'username': 'NoUser', 'token': 'token '}
    
    with open(authentication_info, 'w') as configfile:
        parser.write(configfile)

def get_login_response(username, password):
    data = {'username':username, 'password': password}
    return requests.post("http://127.0.0.1:9103/interoperability/api/login/", data=data)

def get_logout_response():
    token = get_auth_info()['token']
    headers = {AUTH_TOKEN_HEADER: token}
    return requests.post("http://127.0.0.1:9103/interoperability/api/logout/", headers = get_headers())

def get_auth_info(filename=authentication_info, section='AUTHENTICATION'):
    # create a parser
    parser = configparser.RawConfigParser()
    parser.optionxform = str
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    auth_info = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            auth_info[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return auth_info

def get_headers():
    headers = {AUTH_TOKEN_HEADER: get_auth_info()['token']}
    return headers