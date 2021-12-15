# with a file populated with hostnames (one per row) called
# hosts.txt localted in /files this script will retrieve
# all information for those hosts and create a csv file
# called 'resultado.csv' located at /files which will contain
# for every given host the following information:
# Hostname
# Host ID
# Sensor Version
# Groups (a list of groups that hostname belong to)
#
# Here is the code for this script:

# ---------------------------------------------------------------

# imports que usaremos
from os import getgroups
import requests
import json
import logging
import requests
import csv
import logging

# uso decouple para separar código y secrets
from decouple import config

# definición de las funciones que usaremos en nuestro programa

# get_token() Recupero token para hacer uso del mismo llamando a la api de crowdstrike
def get_token():
    payload = {'client_id': clientid, 'client_secret': clientsecret}
    r = requests.post('https://api.crowdstrike.com/oauth2/token', data=payload)
    return r.json()['access_token']

# get_hostnames() Leemos los hostnames a procesar de un txt y precargamos una lista con ellos
def get_hostnames():
    with open('../files/hosts.txt') as fichero_hostnames:
        for line in fichero_hostnames:
            hostnames.append(line.rstrip('\n'))
    return hostnames

def get_hostid(token, hostname):
    url="https://api.crowdstrike.com/devices/queries/devices/v1?filter=hostname%3A"
    url=url+"'"+hostname+"'"
    bearer_token="Bearer "+str(token)
    payload = {'accept': 'application/json', 'authorization': bearer_token}
    # aquí con el request es donde llamamos a la api y obtenemos todos
    # los resultados en un json
    datos_hostname = requests.get(url, headers=payload)
    if datos_hostname.status_code==200:
        hostid=str(datos_hostname.json()['resources'])
        # eliminamos los corchetes y las comillas del valor del hostid 
        # extraído del json
        hostid=hostid[2:len(hostid)-2]
        # Esta sería otra forma de hacerlo usando la fúrmula replace()
        # pero no me gusta como queda... tendría que ver datos de
        # eficiencia, rendimiento, etc...
        # con replace quedaría: 
        # hostid=hostid.replace('[\'', '').replace('\']', '')
        # mensaje log ¡éxito!
        logging.info("get_hostid SUCCESS %s --> %s", hostname, hostid)
        #devolvemos valor
        return hostid
    else:
        # mensaje log indicando error 
        logging.warning("get_hostid ERROR %s", hostname)
        # devolvemos 0 como muestra de que es un error
        # ningún hostid vale 0
        return 0 

def get_groups(token, hostids):
    # construyo la url a utilizar concatenando los hostids
    url=''
    for elemento in hostids:
        elemento="&ids="+elemento
        url=url+elemento 
    url=url[1:]
    url="https://api.crowdstrike.com/devices/entities/devices/v1?"+url

    # construimos el resto de la petición get
    bearer_token="Bearer "+str(token)
    payload = {'accept': 'application/json', 'authorization': bearer_token}
    # traemos los grupos de cada hostid
    grupos = requests.get(url, headers=payload)

    if grupos.status_code==200:
        return grupos.json()
    else:
        # devolvemos 0 como muestra de que es un error
        # ningún hostid vale 0
        logging.warning('Error recuperando grupos de los hostids indicados')
        return 0 

def translate_group(token, groupid):
    url='https://api.crowdstrike.com/devices/entities/host-groups/v1?ids='+groupid
    bearer_token="Bearer "+str(token)
    payload = {'accept': 'application/json', 'authorization': bearer_token}
    groupname=requests.get(url, headers=payload)
    return groupname.json()['resources'][0]['name']


########################################################################   
########################################################################
###############                 START                 ##################
########################################################################
########################################################################

# configuramos el logging
logging.basicConfig(filename='../files/logs.data',
                    level=logging.DEBUG,
                    format='%(asctime)s : %(levelname)s : %(message)s',
                    filemode='w')

#indicamos en el fichero de log que iniciamos la ejecucicón del programa
logging.info('START')

# inicializamos variables
hostnames = []
clientid=config('CLIENT_ID')
clientsecret=config('SECRET_KEY')

# obtenemos el token necesario para atacar la API
token=get_token()

# recupero los hostnames del fichero
hostnames=get_hostnames()

# recupero los hostid de los hostnames
hostids=[]
for elemento in hostnames: hostids.append(get_hostid(token,elemento))
# recupero los grupos de cada host en un json con toda la información y 
# y que puede explotarse para extraer aun más información en el futuro
grupos=get_groups(token, hostids)

# proceso los grupos encontrados solo cuando el script no haya 
# devuelto 0
if grupos != 0:
    # preparo el fichero en el que vuelco el resultado 'resultado.csv'
    with open('../files/resultado.csv', mode='w') as hostsfile:
        hosts_writer = csv.writer(hostsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # preparo y escribo la cabezera del csv
        hosts_writer.writerow(["Hostname", "Host ID", "Agent Version", "Groups"])
    
    # para cada host consultado añado la informacion de los grupos y vuelco todo a una
    # nueva linea del csv
    for host in grupos['resources']:
        # voy a obtener los nombres de los grupos usando la función translate
        # definida arriba
        nombres_grupos=[]
        for g in host['groups']:
            nombres_grupos.append(translate_group(token, g))
            # y escribo los datos del host a una fila del csv - así con todos
        with open('../files/resultado.csv', mode='a') as hostsfile:
            hosts_writer = csv.writer(hostsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # hosts_writer.writerow([id, name, hosts, time])
            hosts_writer.writerow([host['hostname'], host['device_id'], host['agent_version'], nombres_grupos])
else:
    logging.warning('Error recuperando grupos')

#indicamos en el fichero de log que finalizamos la ejecucicón del programa
logging.info('END')
