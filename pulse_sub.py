from python_graphql_client import GraphqlClient
import asyncio

def print_handle(data):
    print(data["data"]["liveMeasurement"]["power"])

client = GraphqlClient(endpoint="wss://api.tibber.com/v1-beta/gql/subscriptions")

query = """
subscription{
  liveMeasurement(homeId:"c70dcbe5-4485-4821-933d-a8a86452737b"){
    timestamp
    power
  }
}
"""

asyncio.run(client.subscribe(query=query, headers={'Authorization': "d1007ead2dc84a2b82f0de19451c5fb22112f7ae11d19bf2bedb224a003ff74a"}, handle=print_handle))
