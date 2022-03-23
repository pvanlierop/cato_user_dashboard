import os
import pprint
from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport



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

search_user(client, 'L')