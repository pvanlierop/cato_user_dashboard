import os
import pprint
from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from typing import Optional
from models import RemoteUser




# We store the API key in the .env File in the format
# API_KEY = "THIS IS YOUR API KEY YOU GENERATED FROM CATO"
load_dotenv()
CATO_API_KEY = os.environ.get("API_KEY")
CATO_CUSTOMER = os.environ.get("CATO_CUSTOMER")

transport = RequestsHTTPTransport(url="https://api.catonetworks.com/api/v1/graphql2", headers={'x-api-key': CATO_API_KEY,
                                       'Content-Type': 'application/json'}, verify=False)

client = Client(transport=transport)

def search_user(client, search_query):

    query = gql(
        """
        query entityLookup($id: ID!, $checkName: String) {
            entityLookup(accountID: $id, type: vpnUser, search: $checkName) {
                items {
                entity {
                    id
                    name
                }
                helperFields
                }   
            }
        }
    """
    )

    params = {"id": CATO_CUSTOMER, "checkName": search_query}

    result = client.execute(query, variable_values=params)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)
    for remoteuser in result['entityLookup']['items']:
        print("ID:", remoteuser['entity']['id'])
        print("Name:", remoteuser['entity']['name'])
        print("Email:", remoteuser['helperFields']['email'])


def active_users(client, user_id: Optional[int] = None):

    query = gql(
        """
        query userSnapShot($id: ID!) {
            accountSnapshot(id: $id) {
                id
                users {
                    connectivityStatus
                    version
                    connectedInOffice
                    uptime
                    id
                    deviceName
                    popName
                    remoteIPInfo {
                        ip
                        countryCode
                        city
                        state
                        provider
                        latitude
                        longitude
                    }
                    osVersion
                    osType
                    info {
                        email
                        phoneNumber
                        name
                    }
                }
            }
            }
    """
    )
    params = {"id": CATO_CUSTOMER}
    result = client.execute(query, variable_values=params)

    # we hold the output using the Pydantic Model RemoteUser for all of the Remote Users key details
    remoteusers = []
    for entry in result['accountSnapshot']['users']:
        user = RemoteUser
        user.name = entry['info']['name']
        user.email = entry['info']['email']
        user.phonenumber = entry['info']['phoneNumber']
        user.officemode = entry['connectedInOffice']
        user.devicename = entry['deviceName']
        user.id = entry['id']
        user.ostype = entry['osType']
        user.osversion = entry['osVersion']
        user.popname = entry['popName']
        user.ip = entry['remoteIPInfo']['ip']
        user.city = entry['remoteIPInfo']['city']
        user.state = entry['remoteIPInfo']['state']
        user.countrycode = entry['remoteIPInfo']['countryCode']
        user.latitude = entry['remoteIPInfo']['latitude']
        user.longitude = entry['remoteIPInfo']['longitude']
        user.provider = entry['remoteIPInfo']['provider']
        user.uptime = entry['uptime']
        user.version = entry['version']
        remoteusers.append(user)
    
    return remoteusers
    

        
    


#search_user(client, 'L')
wholeuserlist = active_users(client)
for i in wholeuserlist:
        print(i.name, i.email, i.devicename)