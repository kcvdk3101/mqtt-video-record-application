import json
import sqlite3
import paho.mqtt.client as mqtt

BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883
FLAG = True
PUBTOP = "/device/record1"
index = 0

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


# Called when the broker responds to our connection request
def on_connect(client,userdata,flags,rc):
  if rc == 0:
      client.connected_flag = True #set flag
      print("Connected OK")
  else:
      print("Bad connection Returned code=",rc)
      client.bad_connection_flag=True

# Called when a message has completed transmission to the broker
def on_publish(client, userdata, mid):
  return

# Called when the client disconnects from the broker
def on_disconnect(client,userdata,rc):
  global data_input

  if rc != 0:
    FLAG = False
    if FLAG == False:
      # Save record to database
      record_list = json.loads(data_input)
      conn = sqlite3.connect('db/video-record.db')
      cursor = conn.cursor()
      for record in record_list['data']:
        add_record(conn, cursor, record)
      print('Add record successfully!')


client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect

try:
    client.connect(BROKER_ADDRESS, BROKER_PORT)
except:
    FLAG = False
    print('Connection failed')
    exit(1)

client.loop_start()

value = {
  "data": [
      {
          "id": 11,
          "name": "record 11",
          "description": "record 11 description",
          "price": 11 
      },
      {
          "id": 2,
          "name": "record 2",
          "description": "record 2 description",
          "price": 2 
      },
      {
          "id": 3,
          "name": "record 3",
          "description": "record 3 description",
          "price": 3 
      },
      {
          "id": 4,
          "name": "record 4",
          "description": "record 4 description",
          "price": 4 
      },
      {
          "id": 5,
          "name": "record 5",
          "description": "record 5 description",
          "price": 5 
      },
      {
          "id": 16,
          "name": "record 16",
          "description": "record 16 description",
          "price": 16 
      }
  ]
}


while True:
  data_input = json.dumps(value)
  client.publish(PUBTOP, data_input)
  if FLAG == False or len(data_input) == 0:
    break
    

client.loop_stop()
client.disconnect()
