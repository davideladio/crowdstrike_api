# Script which will query all groups in your console
# and append that information to a csv file.
#
# This way you can execute this script periodically and
# keep all the results in a csv file where yo can
# track 'history' on the number of hosts in that group
#
import json
import objectpath
import csv
from datetime import datetime
import requests
import array as arr

#--------------------------------------------------------------#
#--------------------------------------------------------------#
#-------------------- FUNCTIONS DECLARATION -------------------#
#--------------------------------------------------------------#
#--------------------------------------------------------------#

#Funcion para obtener el token con el que consultar la api de crowdstrike
def get_token():
	payload = {'client_id': 'CLIENT_ID_HERE', 'client_secret': 'CLIENT_SECRET_HERE'}
	r = requests.post('https://api.crowdstrike.com/oauth2/token', data=payload)
	r_json = json.loads(r.text)
	token = r_json['access_token']
	return token

#obtengo el json con todos los grupos
def get_groups(token):
	bearer_token="bearer "+str(token)
	payload = {'accept': 'application/json', 'authorization': bearer_token}
	grupos = requests.get('https://api.crowdstrike.com/devices/combined/host-groups/v1?sort=name.asc', headers=payload)
	grupos_json = json.loads(grupos.text)
	return grupos_json

#funcion para obtener info de cada grupo
def update_deploy(lista_grupos_id, lista_grupos_name):

	#guardo el timestamp en una variable
	time = str(datetime.now(tz=None))[:10]
	
	#recorro la lista de ID's de grupos y guardo los datos de cada uno
	indice=0

	for id in lista_grupos_id:
		#configuro la llamada a la api con el id del grupo en cada caso
		url="https://api.crowdstrike.com/devices/combined/host-group-members/v1?id="
		url=url+id
		bearer_token="bearer "+str(token)
		payload = {'accept': 'application/json', 'authorization': bearer_token}
		datos_grupo = requests.get(url, headers=payload)
		datos_grupo_json = json.loads(datos_grupo.text)
		#para cada grupo guardo el numero de hosts que contiene
		hosts=datos_grupo_json['meta']['pagination']['total']
		#la geografia la obtengo de la lista de nombres de grupos
		name=lista_grupos_name[indice]

		#preparo el csv para ser escrito en modo 'append'
		#y guardo los datos de esta pasada del bucle
		with open('hosts.csv', mode='a') as hostsfile:
			hosts_writer = csv.writer(hostsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			hosts_writer.writerow([id, name, hosts, time])
		
		#incremento el indice para llvar el orden id-name de los grupos
		indice+=1

#--------------------------------------------------------------#
#--------------------------------------------------------------#
#--------------------- PROGRAM STARTS HERE --------------------#
#--------------------------------------------------------------#
#--------------------------------------------------------------#

#obtengo un token para consultar la api
token = get_token()

grupos=get_groups(token)

#cargo dos listas una con los IDs y una con los nombres de los grupos
lista_grupos_id=[]
lista_grupos_name=[]

for i in grupos['resources']:
	lista_grupos_id.append(i['id'])
	lista_grupos_name.append(i['name'])

update_deploy(lista_grupos_id, lista_grupos_name)
