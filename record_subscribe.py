# import paho.mqtt.client as mqtt

# BROKER_ADDRESS = "localhost"
# BROKER_PORT = 1883
# FLAG = True
# PUBTOP = "/device/record2"
# SUBTOP = "/device/record1"
# chat = None

# # Called when the broker responds to our connection request
# def on_connect(client,userdata,flags,rc):
#   if rc == 0:
#     FLAG = True
#     print(f"Connected to {BROKER_ADDRESS} with port {BROKER_PORT} successfully!") 
#   else:
#     print("Bad connection Returned code=",rc)  


# # Called when a message has been received on a topic that the client has subscirbed to.
# def on_message(client, userdata, message):
#   if str(message.topic) != PUBTOP:
#     msg = message.payload.decode("utf-8")
#     print(str(message.topic),msg)

# # Called when the client disconnects from the broker
# def on_disconnect(client,userdata,rc):
#   if rc != 0:
#     FLAG = False
#     print("Unexpected Disconnection")

# client = mqtt.Client()
# client.connect(BROKER_ADDRESS, BROKER_PORT)
# client.on_connect = on_connect

# client.subscribe(SUBTOP)
# client.on_message = on_message


# client.loop_forever()

from utils import *
def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to {BROKER_URL} with port {PORT} successfully!")
            subscribe(client)
        else:
            print(f"Failed to connect, return code %d\n", rc)
def run():
    client = connect_mqtt()
    client.on_connect = on_connect
    client.loop_forever()


if __name__ == '__main__':
    run()