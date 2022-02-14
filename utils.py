import json
import random
import sqlite3
import string
from time import sleep
import paho.mqtt.client as mqtt


BROKER_URL = 'localhost'
PORT = 1883
TOPIC = 'dinhkhoi/mqtt'
FLAG = True
index = 0
value = {}

def random_string():
    output =  ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
    return output

def data_simulation():
  random_values = []
  x = 0
  while x < 5:
    random_values.append({
      'name': random_string(),
      'description': random_string(),
      'price': random.randint(0,9)
    })
    x += 1
  return random_values

# Add record to database when mqtt disconnect
def add_record(conn, cursor, record):
  global index

  cursor.execute("SELECT * FROM records")
  results = cursor.fetchall()

  divide = index % 10

  if(len(results) < 10):
    cursor.execute("INSERT INTO records VALUES({0},'{1}','{2}', {3})"
    .format(len(results),record['name'], record['description'], record['price']))

  else:
    cursor.execute("UPDATE records SET name='{0}', description='{1}', price={2} WHERE id={3}"
      .format(record['name'], record['description'], record['price'], divide))
  
  index += 1
  conn.commit()


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to {BROKER_URL} with port {PORT} successfully!")
        else:
            print(f"Failed to connect, return code %d\n", rc)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(BROKER_URL, PORT)
    return client


def publish(client):
  def on_publish(client, userdata, rc):
      print("Data published")
      if rc != 0 :
        FLAG = False
        print(f"Result code: {rc}")

  while FLAG:
      global value
      sleep(1)
      value = {
        "data": data_simulation()
      }
      msg = json.dumps(value)
      result = client.publish(TOPIC, msg)
      client.on_publish = on_publish
      status = result[0]

      if status == 0:
        print(f"Send {msg} to {TOPIC}")
      else:
        # record_list = json.loads(value)
        conn = sqlite3.connect('db/video-record.db')
        cursor = conn.cursor()
        for record in value['data']:
          add_record(conn, cursor, record)


def disconnect(client):
  def on_disconnect(client,userdata,rc):
    if rc != 0:
      FLAG = False
      if FLAG == False:
        global value
        # Save record to database
        # record_list = json.loads(value)
        conn = sqlite3.connect('db/video-record.db')
        cursor = conn.cursor()
        for record in value['data']:
          add_record(conn, cursor, record)
        print('Add record successfully!')
  client.on_disconnect = on_disconnect

def subscribe(client):
    def on_message(client, userdata, msg):
        print(f"Recieve {msg.payload.decode()} from {msg.topic}")
    
    client.subscribe(TOPIC)
    client.on_message = on_message