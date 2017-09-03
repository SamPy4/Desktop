import paho.mqtt.client as mqtt
from subprocess import call
import gtts, os, time

port = 1883
serverPath = "85468PATH"
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(serverPath + "/#")


def verify(verification):
    if verification:
        client.publish(serverPath + "/verify", "#00FF00")
    else:
        client.publish(serverPath + "/verify", "#FF0000")
    return

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))



    command = str(msg.payload)[1:]

    # if msg.topic == serverPath + "/range":
    #     volume = str(msg.payload)[1:]
    #     call(["amixer", "-D", "pulse", "sset", "Master", volume, "%"])


    if msg.topic == serverPath + "/swich":
        verify(True)
        send()
        verify(False)

    if msg.topic == serverPath + "/lock":
        verify(True)
        os.system("rundll32.exe user32.dll, LockWorkStation")
        verify(False)

    if msg.topic == serverPath + "/shutdown":
        verify(True)
        os.system("shutdown -s -t 1")
        verify(False)

    if msg.topic == serverPath + "/speech":
        verify(True)
        text = str(msg.payload)[1:]

        print(text)

        if '\xc3\xa4' in text:
            text = text.replace("\xc3\xa4", "ä")
            print("KORVATTU Ä")

        if "\xc3\xb6" in text:
            text = text.replace("\xc3\xb6", "ö")
            print("KORVATTU Ö")


        gtts.gTTS(text=text, lang="fi").save("speech.mp3")
        os.system("speech.mp3")
        verify(False)

def send():
    client.publish(serverPath + "/var1", "50")
    print("sent")

def sendVariables():
    pass




client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

# mainloop starts here
while True:
    client.loop()
    sendVariables()
    time.sleep(0.1)
    print("-------------")
