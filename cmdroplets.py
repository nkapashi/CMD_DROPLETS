import requests
import json
from time import sleep
import sys


class Droplet(object):
    # replace below with your auth token
    authId = '--'
    dropletUrl = 'https://api.digitalocean.com/v2/droplets'
    requestHeaders = {'content-type': "application/json", 'authorization': "Bearer " + authId}

    def __init__(self, name, dropletId = None):
        self.name = name
        self.dropletId = dropletId
        self.createDataDict = getDropletParams()
        self.createDataDict['name'] = self.name
        self.createData = json.dumps(self.createDataDict)

    def start(self):
        self.response = requests.request("POST", Droplet.dropletUrl, data=self.createData, headers=Droplet.requestHeaders)
        self.dropletId = self.response.json()['droplet']['id']
        return self.dropletId
    
    def delete(self):
        """Delete Droplet. Accepts Droplet Id as param"""
        requests.request("DELETE", str(Droplet.dropletUrl) + '/' + str(self.dropletId), headers=Droplet.requestHeaders)

def getDropletParams():
    try:
        with open('droplets.json') as file:
            dropletParams = json.load(file)
        return dropletParams
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(e)
        sys.exit("Can not continue. Exiting...")

def getActiveDroplets():
    """ Return a dictionary with droplets name as key and droplet id and ip address as value"""
    activeDropletsJsonData = requests.request("GET", Droplet.dropletUrl, headers=Droplet.requestHeaders)
    dropletsDict = {}
    for item in activeDropletsJsonData.json()['droplets']:
        dropletsDict[item['name']] = [item['id'], item['networks']['v4'][0]['ip_address'], Droplet(item['name'], item['id'])]
    return dropletsDict

def printDroplets(droplets):
    if len(droplets) > 0:
        for k, v in droplets.items():
            print(k, v[0:2])
    else:
        print("No active droplets found.")

def userSelection():
    userSelection  = input("Select an option: 1 - List, 2 - Delete, 3 - Create > ")
    return userSelection

def getRegions():
    regionsData = requests.request("GET", "https://api.digitalocean.com/v2/regions", headers=Droplet.requestHeaders)
    regionList = []
    for item in regionsData.json()['regions']:
        regionList.append(item['slug'])
    return regionList

droplets = getActiveDroplets()
while True:
    selection = userSelection()
    if selection == '1':
         droplets = getActiveDroplets()
         printDroplets(droplets)
    elif selection == '2':
         name = input("provide droplet name to delete > ")
         try:
             droplets[name][2].delete()
             sleep(2)
         except(KeyError):
            print(f"Droplet with name {name} does not exist.")
         finally:
             droplets = getActiveDroplets()
             printDroplets(droplets)
    elif selection == '3':
        name = input("provide a name > ")
        Droplet(name).start()
        sleep(2)
        droplets = getActiveDroplets()
        printDroplets(droplets)

    else:
        print(f"Not supported option selection {selection}.")