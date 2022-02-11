import paho.mqtt.client as mqtt

# Called when the broker responds to our connection request
def on_connect(client,userdata,flags,rc):
  print("Connected - rc:",rc)


# Called when a message has been received on a topic that the client has subscirbed to.
def on_message(client, userdata, message):
  global FLAG
  if str(message.topic) != pubtop:
    msg = message.payload.decode("utf-8")
    if str(msg) == '':
      FLAG = False
    print(str(message.topic),type(msg))

# Called when the client disconnects from the broker
def on_disconnect(client,userdata,rc):
  if rc != 0:
    print("Unexpected Disconnection")


broker_address = "localhost"
port = 1883

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
  client.connect(broker_address, port)
except Exception as e:
  print('Failed to connect to MQTT broker"')


pubtop = "/device/record2"
subtop = "/device/record1"
FLAG = True
chat = None

client.loop_start()
client.subscribe(subtop)

while True:
  if FLAG == False:
    break

client.disconnect()
client.loop_stop()