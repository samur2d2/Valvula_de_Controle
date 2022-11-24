from paho.mqtt import client as mqtt_client

# username = 'emqx'
# password = 'public'

def connect_mqtt(brokerIp, clientName, portNum):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(clientName)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(brokerIp, portNum)
    return client

def Publish(client, msg, topicName):
    result = client.publish(topicName, msg)
    status = result[0]
    if status == 0:
        print(f"Sent `{msg}` to topic `{topicName}`.")
    else:
        print(f"Failed to send message to topic {topicName}")

def Sent(mensagem, brokerIp, portNum, topicName, clientName):
    client = connect_mqtt(brokerIp, clientName, portNum)
    Publish(client, mensagem, topicName)
    client.disconnect