# import json
# import sqlite3
# from time import sleep
# import paho.mqtt.client as mqtt

# from utils import *

# BROKER_ADDRESS = "localhost"
# BROKER_PORT = 1883
# FLAG = True
# PUBTOP = "/device/record1"
# SUBTOP = "/device/record2"
# index = 0

# # Called when the broker responds to our connection request
# def on_connect(client,userdata,flags,rc):
#   if rc == 0:
#       client.connected_flag = True #set flag
#       print("Connected OK")
#   else:
#       print("Bad connection Returned code=",rc)
#       client.bad_connection_flag=True

# # Called when a message has completed transmission to the broker
# def on_publish(client, userdata, mid):
#   print('Data pulished')

# # Called when the client disconnects from the broker
# def on_disconnect(client,userdata,rc):
#   global data_input

#   if rc != 0:
#     FLAG = False
#     if FLAG == False:
#       # Save record to database
#       record_list = json.loads(data_input)
#       conn = sqlite3.connect('db/video-record.db')
#       cursor = conn.cursor()
#       for record in record_list['data']:
#         add_record(conn, cursor, record)
#       print('Add record successfully!')


# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_publish = on_publish
# client.on_disconnect = on_disconnect
# client.connect(BROKER_ADDRESS, BROKER_PORT)

# client.loop_start()

# while True:
#   sleep(1)
#   data_input = json.dumps(value)
#   client.publish(PUBTOP, data_input)
#   if FLAG == False or len(data_input) == 0:
#     print("Failed to send message to {PUBTOP}")
#   else:
#     print(f"Send {data_input} to {PUBTOP}")


from utils import connect_mqtt, disconnect, publish


def run():
  client = connect_mqtt()
  client.loop_start()
  disconnect(client)
  publish(client)


if __name__ == '__main__':
  run()