from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
from dotenv import load_dotenv
import threading
import os
from uuid import uuid4
import json
from picamera import PiCamera
from pathlib import Path
from dotenv import load_dotenv

# Get the base directory
basepath = Path()
basedir = str(basepath.cwd())
# Load the environment variables
envars = os.path.dirname(basepath.cwd())+'/TSA_mecha/.env'
print(envars)
load_dotenv(envars)

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
proxy_options=None


print("endpoint: ",os.getenv('ENDPOINT'))
print("http_proxy_options: ",os.getenv('HTTP_PROXY_OPTIONS'))
print(os.getenv('TOPIC'))
print(os.getenv('CERT_FILEPATH'))
print(os.getenv('PRI_KEY_FILEPATH'))
print(os.getenv('CA_FILEPATH'))

proxy_options=None
# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

class mq:
     def __init__(self):
          self._mqm = 0
       
     # function to get value of _mqm
     def get_mqm(self):
         print("getter method called")
         return self._mqm
       
     # function to set value of _mqm
     def set_mqm(self, a):
         print("setter method called")
         self._mqm = a
  
     
     mqm = property(get_mqm, set_mqm) 

def photo_capture():
    os.system('libcamera-still -r -o /home/pi/TSA/TSA-demo/pic.jpg')

def photo_captureb():
    camera = PiCamera()
    camera.start_preview(alpha=192)
    #sleep(1)
    camera.capture("/tmp/pic"+str(uuid4())+".jpg")
    camera.capture("/home/pi/TSA/TSA-demo/pic.jpg")
    camera.stop_preview()
    camera.close()

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)

mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=os.getenv('ENDPOINT'),
        port=int(os.getenv('PORT')),
        cert_filepath=os.getenv('CERT_FILEPATH'),
        pri_key_filepath=os.getenv('PRI_KEY_FILEPATH'),
        ca_filepath=os.getenv('CA_FILEPATH'),
        client_bootstrap=client_bootstrap,
        http_proxy_options=proxy_options,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=os.getenv('CLIENT_ID')+str(uuid4()),
        clean_session=False,
        keep_alive_secs=30)

connect_future = mqtt_connection.connect()
print (connect_future)

# Future.result() waits until a result is available
connect_future.result()
print("Connected!")

def mqtt_subscribe():
    received_count = 0
    received_all_event = threading.Event()



    # Callback when the subscribed topic receives a message
    def on_message_received(topic, payload, dup, qos, retain, **kwargs):
        print("Received message from topic '{}': {}".format(topic, payload))
        global received_count
        received_count = 0
        received_count += 1
        if received_count == 0:
            received_all_event.set()
        global aa
        try:
            print("message: ",json.loads(payload.decode("utf-8"))["lex-request"])
            mess = json.loads(payload.decode("utf-8"))["lex-request"]
            if (mess == "reboot"):
                print("Message detected: " + str(mess))
                os.system('sudo reboot')
        except Exception as e:
            print(e)
        try:
            print("edge: ",json.loads(payload.decode("utf-8"))["lex-recognition-edge"])
            trigg = json.loads(payload.decode("utf-8"))["lex-recognition-edge"]
            if (trigg == "yes"):
                #photo = photo_capture()
                photo='/Users/kedouard/Documents/SA/Labs/TSA bot/TSABot_dev_team_oct12/TSA-demo/TSA_rekognition/samples_img/waterbottle.jpeg'
                print("start image reco")
                label_count=detect_labels_local_file(photo)
                print("Labels detected: " + str(label_count))
                print("end image reco")
                

                #label_count=detect_labels_local_file(photo)
                #logging.info("label count: ", label_count)
                #print("Labels detected: " + str(label_count))
                #li = [mess.get('Name') for mess in label_count]
                #print(li)
                #messages = json.dumps({"message" : li, "lex-recognition-edge": "no"})
                #print('messages: ', messages)
                #pub = mqtt_connection.publish(topic='lcd-message', payload=messages, qos=mqtt.QoS.AT_LEAST_ONCE)
                #print("pub: ", pub)
        except Exception as e:
            print('error at edge reco level: ',e)

    # Subscribe
    print("Subscribing to topic '{}'...".format(os.getenv('TOPIC')))
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic='lcd-message',
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)

    subscribe_result = subscribe_future.result()
    print("Subscribed with {}".format(str(subscribe_result['qos'])))

    #return "top"

    #received_all_event.wait()
    print("{} message(s) received.".format(received_count))

def mqtt_publish(message):
    try:
        pub = mqtt_connection.publish(topic='lcd-message', payload=message, qos=mqtt.QoS.AT_LEAST_ONCE)
        return pub
    except Exception as e:
        print('error in pub: ', e)
