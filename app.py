from flask.helpers import make_response
from python_graphql_client import GraphqlClient
import asyncio
import threading
from flask import Flask, render_template, json

power = 0
def print_handle(data):
    global power
    power = data["data"]["liveMeasurement"]["power"]
    currentL1 = data["data"]["liveMeasurement"]["currentL1"]
    currentL2 = data["data"]["liveMeasurement"]["currentL2"]
    currentL3 = data["data"]["liveMeasurement"]["currentL3"]
    print(power, currentL1, currentL2, currentL3)

client = GraphqlClient(endpoint="wss://api.tibber.com/v1-beta/gql/subscriptions")

query = """
subscription{
  liveMeasurement(homeId:"c70dcbe5-4485-4821-933d-a8a86452737b"){
    timestamp
    power
    currentL1
    currentL2
    currentL3
  }
}
"""
def update():
    asyncio.run(client.subscribe(query=query, headers={'Authorization': "d1007ead2dc84a2b82f0de19451c5fb22112f7ae11d19bf2bedb224a003ff74a"}, handle=print_handle))

thread = threading.Thread(target=update)
thread.start()

app = Flask(__name__)

@app.route("/")
def index():
    global power
    print(str(power) + " has been sent")
    return render_template("show_power.html", power=power)

@app.route("/data", methods=["GET", "POST"])
def data():
    global power
    response = make_response(json.dumps(power))
    response.content_type = "application/json"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0")