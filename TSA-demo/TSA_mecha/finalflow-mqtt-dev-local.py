# -*- coding: utf-8 -*

#import serial
import time
import sys
import os
import psutil
import RPi.GPIO as GPIO
#from adafruit_servokit import ServoKit
import os
import RPi.GPIO as GPIO
import uuid
#kit = ServoKit(channels=16)
from servo_actions_local import initialAvaIntroServo, myNameisAvaServo, Avadoyouhavequestion, checkAgentontheright, avagoodbye


import threading


#from iot_sub import mqtt_subscribe, mqtt_publish

sys.path.append('/home/pi/TSA-clean/TSA_voice_assistant/')
from raspberry_voice_assistant_local import synthesize_speech, call_lexv2, decode, get_voiceid, record_phrase, play_audio, set_color, color_start, translatelang

sys.path.append('/home/pi/TSA-clean/TSA_rekognition/')
from iot_sub_reko import mqtt_subscribe, mqtt_publish, mq, photo_capture
from detect_labels_image import detect_labels_local_file, detect_ppe_local_file

sys.path.append('/home/pi/TSA-clean/TSA_flight_status/')
from flight import scanflights

import json
#ser = serial.Serial("/dev/ttyUSB0", baudrate=115200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)

import platform
platform_sys=platform.system()

global intro 
intro = 0

def processKill():
    # Ask user for the name of process
    try:
        # iterating through each instance of the process
        PROCNAME = "ffplay"
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == PROCNAME:
                proc.kill()
        print("Process Successfully terminated")
    except:
        print("Error Encountered while running script or ffplay was not running")

def processCheck():
    # Ask user for the name of process
    try:
        # iterating through each instance of the process
        PROCNAME = "ffplay"
        for proc in psutil.process_iter():
           #print('proc.name: ',proc.name())
            # check whether the process name matches
            if proc.name() == PROCNAME:
                print("ffplay still running")
                return True
            else:
                #print('ffplay not found')
                pass
        return False
    except Exception as e:
        print("Error Encountered while running script for processCheck: ",e)


def getTFminiData():
    intro = 0
    firstloop = 0
    langcode ='en_US'
    stop_threads = False
    background_thread = threading.Thread(target=initialAvaIntroServo, name='initialAvaIntroServo', args =(lambda : stop_threads, ))
    stop_threadsName = True
    stop_threadsAvadoyouhavequestion = True
    background_thread = threading.Thread(target=initialAvaIntroServo, name='initialAvaIntroServo', args =(lambda : stop_threads, ))
    myNameisAvaServo_thread = threading.Thread(target=myNameisAvaServo, name='myNameisAvaServo', args =(lambda : stop_threadsName, ))
    Avadoyouhavequestion_thread = threading.Thread(target=Avadoyouhavequestion, name='Avadoyouhavequestion', args =(lambda : stop_threadsAvadoyouhavequestion, ))
    while True:
        #count = ser.in_waiting
        count = 12
        # print('count: ',count)
        time.sleep(0.2)
        if count > 8:
            #recv = ser.read(9)
            #print('recv', recv)
            #ser.reset_input_buffer()
            #if recv[1]: # 0x59 is 'Y'*
            recv = [None] * 4
            print(recv)
            recv[0]="0x59"
            recv[1]="0x59"
            recv[2]=50
            recv[3]=200
            print(recv)
            if recv[0] == "0x59" and recv[1] == "0x59": # 0x59 is 'Y'
                print("hello1")
                low = int(recv[2])
                print("low dist",  low)
                high = int(recv[3])
                print("high dist", high)
                distance = low + high * 256
                distance = 150
                print("Distance is ", distance)
                #messages = json.dumps({"message" : "distance is %s" %distance, "lex-recognition-edge": "no"})
                #print('messages: ', messages)
                #pub = mqtt_publish(messages)
                #print('pub: ', pub)
                #distance = 25
                if 20 <= distance <= 180:
                    #Kill the AVAintro process
                    processKill()
                    print('background_thread', background_thread)
                    stop_threads = True
                    print('background_thread is_alive: ', threading.enumerate())
                    background_thread = threading.Thread(target=initialAvaIntroServo, name='initialAvaIntroServo'+str(uuid.uuid4()), args =(lambda : stop_threads, ))
                    firstloop = 0
                    stop_threadsName = False
                    stop_threadsAvadoyouhavequestion = False
                    print ("Start Lex flow")
                    try:
                        print('intro counter: ', intro)
                        if intro == 0:
                            lexcall = 0
                            print('intro counter: ', intro)
                            myNameisAvaServo_thread.start()
                            mqtt_publish('{"message": "I am TSA Bot.\\n How can I help?", "presence": "request" }')
                            welcome = '''
                            <speak>
                            Hello. I am T. S. A. Bot. How can I help?
                            You can say .<prosody volume="+12dB"> <lang xml:lang="en-ES">  Hola! </lang> </prosody> for spanish! <break time="1s"/>
                            </speak>
                            '''
                            synthesize_speech(welcome, 'ssml')
                            intro +=1
                            detect = 0
                            print('intro counter after intro: ', intro)
                        else:
                            print('intro counter follow up: ', intro)
                            if platform_sys !='Darwin':
                                set_color("white")
                                time.sleep(0.5)
                                set_color("off")
                            time.sleep(1)
                            if(langcode == 'en_US'):
                                synthesize_speech("Do you have a question?.", 'text')
                                mqtt_publish('{"message": "Do you have a question?", "presence": "request" }')
                            else:
                                synthesize_speech("<speak> <lang xml:lang='en-ES'>Tienes una pregunta? </lang> </speak>", 'ssml')
                                mqtt_publish('{"message": "Tienes una pregunta?", "presence": "request" }')
                            print('starting Avadoyouhavequestion_thread')
                            Avadoyouhavequestion_thread.start()
                            time.sleep(0.3)
                        session_id = str(uuid.uuid4())
                        if platform_sys != 'Darwin':
                            set_color('blue')
                        print('starting recording')
                        recording = record_phrase()
                        #print('recording: ', recording)
                        if detect == 0:
                            mqtt_publish('{"message": "Detecting language...", "presence": "request" }')
                            synthesize_speech('<speak> Detecting language. <amazon:effect phonation="soft"> Please wait.</amazon:effect> </speak>', 'ssml')
                            detect +=1
                        response = call_lexv2(session_id, bytes(recording), langcode)
                        #print('response: ', response)
                        #if platform_sys != 'Darwin':
                        #    set_color('off')
                        base64_message = decode(response['messages'])[0]['content']
                        #base64_message = 'Let me identify your items.'
                        print('base64_message', base64_message)
                        ##ADDED
                        if (lexcall == 0):
                            session_ides = str(uuid.uuid4())
                            responsees = call_lexv2(session_ides, bytes(recording), 'es_US')
                            print('responsesss: ',responsees)
                            base64_messagees = decode(responsees['messages'])[0]['content']
                            print('base64_messagees', base64_messagees)
                            ##END ADDED
                            if base64_messagees == 'hola':
                            #if base64_message == 'hola':
                                langcode='es_US'
                                #play_audio(responsees['audioStream'])
                                synthesize_speech("<speak> <lang xml:lang='en-ES'>Hola! Cambio de idioma to español </lang> </speak>", 'ssml')
                            lexcall +=1
                            unknownquestion = 0
                        if base64_message == 'I do not know how to answer your question.' and langcode == 'es_US' and unknownquestion == 0 :
                            synthesize_speech("<speak> <lang xml:lang='en-ES'>No sé cómo responder a la pregunta</lang> </speak>", 'ssml')
                            mqtt_publish('{"message": "No sé cómo responder a la pregunta", "presence": "request" }')
                        if base64_message == 'I do not know how to answer your question.' and unknownquestion == 0 :
                            print('Ignore')
                        else:
                            print('sending mqtt and playing audio')
                            mqtt_publish('{"message": "%s", "presence": "request" }' %(base64_message) )
                            play_audio(response['audioStream'])
                        unknownquestion += 1
                        if base64_message == 'Checking flight schedule to Boston.' :
                            envol = scanflights('BOS')
                            mqtt_publish('{"message": "%s", "presence": "request" }' %(str(envol)) )
                            synthesize_speech("%s" %(str(envol)), 'text')
                        if base64_message == 'Checking flight schedule to New-York.' :
                            envol = scanflights('JFK')
                            mqtt_publish('{"message": "%s", "presence": "request" }' %(str(envol)) )
                            synthesize_speech("%s" %(str(envol)), 'text')
                        if base64_message == 'Checking flight schedule to Los Angeles.' :
                            envol = scanflights('LAX')
                            mqtt_publish('{"message": "%s", "presence": "request" }' %(str(envol)) )
                            synthesize_speech("%s" %(str(envol)), 'text')
                        if base64_message == 'Let me identify your items.' or base64_message == 'Permítanme identificar sus artículos.':
                            mqtt_publish('{"message": "Let me identify your items.", "presence": "request" }')
                            print('play routine for items recognized')
                            if platform_sys !='Darwin':
                                set_color("purple")
                                time.sleep(0.2)
                                set_color("off")
                                time.sleep(0.2)
                                set_color("purple")
                                time.sleep(0.2)
                                set_color("off")
                                time.sleep(0.2)
                                set_color("purple")
                                time.sleep(0.2)
                                set_color("off")
                            if langcode == 'es_US':
                                mqtt_publish('{"message": "Análisis ...", "presence": "request" }')
                                synthesize_speech("<speak> <lang xml:lang='en-ES'>Análisis ...</lang> <break time='0.2s'/></speak>",'ssml')
                            else:
                                mqtt_publish('{"message": "Scanning ...", "presence": "request" }')
                                synthesize_speech('Scanning','text')
                            photocapt = photo_capture()
                            photo='/home/pi/TSA/TSA-demo/pic.jpg'
                            print("start image reco")
                            label_count=detect_labels_local_file(photo)
                            print("Labels detected: " + str(label_count))
                            dispose = ''
                            for item in label_count:
                                print(item)
                                print("item['id']: ", item['id']['S'])
                                dispose= dispose + item['id']['S'] + ', '
                            print("end image reco")
                            print('dispose: ', dispose)
                            if dispose == '':
                                set_color("green")
                                time.sleep(0.6)
                                set_color("off")
                                if langcode == 'es_US':
                                    mqtt_publish('{"message": "No he identificado ningún artículo para desechar.\\n Diríjase a la puerta", "presence": "request" }')
                                    synthesize_speech("<speak> <lang xml:lang='en-ES'>No he identificado ningún artículo para desechar, diríjase a la puerta</lang> </speak>",'ssml')
                                else:
                                    mqtt_publish('{"message": "I have not identified any item to dispose.", "presence": "request" }')
                                    synthesize_speech('I have not identified any item to dispose. Please proceed to the gate','text')
                                checkAgentontheright()
                            else:
                                set_color("red")
                                time.sleep(0.4)
                                set_color("off")
                                if langcode == 'es_US':
                                    dispose_es = translatelang(dispose,'es')
                                    mqtt_publish('{"message": "Alquile sus\\n %s\\n en la papelera y diríjase a la puerta", "presence": "request" }' %(dispose))
                                    synthesize_speech("<speak> <lang xml:lang='en-ES'>Alquile sus %s en la papelera y diríjase a la puerta</lang> </speak>" %(dispose_es),'ssml')
                                else:
                                    mqtt_publish('{"message": "Place your\\n %s\\n in the bin.", "presence": "request" }' %(dispose))
                                    synthesize_speech('please place your %s in the bin and proceed to the gate' %(dispose), 'text')
                            time.sleep(1)
                            try:
                                ppe_count=detect_ppe_local_file(photo)
                                print("PPE detected: " + str(ppe_count[0]))
                                if (len(ppe_count[0]['Persons']) == 1):
                                    print('PPE - Person detected')
                                    try:
                                        print(str((ppe_count[0]['Persons'][0]['BodyParts'][0]['EquipmentDetections'][0]['Type'] == 'FACE_COVER')))
                                        print('PPE - face covered')
                                    except:
                                        print('PPE - face not covered')
                                        if langcode == 'es_US':
                                            synthesize_speech("<speak> <lang xml:lang='en-ES'>Como recordatorio, use una máscara dentro del aeropuerto.</lang> </speak>",'ssml')
                                        else:
                                            synthesize_speech('As a reminder, please wear a mask inside the airport', 'text')
                                    try:
                                        nose = str(ppe_count[0]['Persons'][0]['BodyParts'][0]['EquipmentDetections'][0]['CoversBodyPart']['Value'])
                                        if (nose == 'True'):
                                            print('PPE - mask on nose')
                                        else:
                                            print('PPE not on nose')
                                            if langcode == 'es_US':
                                                synthesize_speech("<speak> <lang xml:lang='en-ES'>Como recordatorio, mantén la máscara en la nariz mientras estés en el aeropuerto.</lang> </speak>",'ssml')
                                            else:
                                                synthesize_speech('As a reminder, please keep your mask on your nose while at the airport','text')
                                    except:
                                        print('nose PPE failed')
                                else:
                                    print('nobody detected for PPE')
                                #print("PPE detected Face: " + str(ppe_count[0]['Persons'][0]['BodyParts'][0]['EquipmentDetections'][0]['Type']))
                                #print("PPE detected on Nose: " + str(ppe_count[0]['Persons'][0]['BodyParts'][0]['EquipmentDetections'][0]['CoversBodyPart']['Value']))
                            except Exception as e:
                                print('ppe exception:', e)
                        if base64_message == 'I am going to reboot.':
                            print('REBOOT REQUESTED')
                            mqtt_publish('{"message": "Rebooting system in 5s", "presence": "request" }')
                            time.sleep(5)
                            os.system('sudo reboot')
                        if base64_message == 'Bye bye.':
                            synthesize_speech('Have a nice day.')
                            mqtt_publish('{"message": "Have a safe flight.", "presence": "request" }')
                            #Wave byebye   
                            time.sleep(10)
                        session_state = decode(response['sessionState'])
                        #print('session_state: ',session_state)
                        dialog_action = session_state['dialogAction']['type']
                        state = session_state['intent']['state']
                        print('dialog action, state: ', dialog_action, state)
                        #if dialog_action == 'Close' and state == 'Fulfilled':
                        #    break
                    except Exception as e:
                        print('An error occured in sensor detected: ',e)
                    try:
                        print("Starting Avadoyouhavequestion_thread")
                        stop_threadsAvadoyouhavequestion = True
                        Avadoyouhavequestion_thread = threading.Thread(target=Avadoyouhavequestion, name='Avadoyouhavequestion', args =(lambda : stop_threadsAvadoyouhavequestion, ))
                    except Exception as e: print('stop Avadoyouhavequestion_thread error: ', e)
                    #messages = json.dumps({"message" : "starting Lex Flow", "lex-recognition-edge": "no", "lex-flow": "start"})
                    #mqtt_publish(messages)
                else:
                    langcode ='en_US'
                    ffpstatus = processCheck()
                    mqtt_publish('{"message": "", "presence": 0 }')
                    print('ffpstatus: ', ffpstatus)
                    #messages = json.dumps({"message" : "Stopping Lex Flow", "lex-recognition-edge": "no", "lex-flow": "stop"})
                    #mqtt_publish(messages)
                    try:
                        print("Starting myNameisAvaServo_thread")
                        stop_threadsName = True
                        myNameisAvaServo_thread = threading.Thread(target=myNameisAvaServo, name='myNameisAvaServo', args =(lambda : stop_threadsName, ))
                    except Exception as e: print('stop myNameisAvaServo_thread error: ', e)
                    try:
                        print("Starting Avadoyouhavequestion_thread")
                        stop_threadsAvadoyouhavequestion = True
                        Avadoyouhavequestion_thread = threading.Thread(target=Avadoyouhavequestion, name='Avadoyouhavequestion', args =(lambda : stop_threadsAvadoyouhavequestion, ))
                    except Exception as e: print('stop Avadoyouhavequestion_thread error: ', e)
                    stop_threads = False
                    if not ffpstatus:
                        print('starting TSA Intro loop')
                        #cmd1 = "ffplay -nostats -nodisp -autoexit /home/pi/TSA/TSA-demo/TSA_mecha/TSA_intro_default_loop.mp3 &"
                        cmd1 = "SDL_AUDIODRIVER='alsa' AUDIODEV='hw:1,0' ffplay -nostats -nodisp -autoexit /home/pi/TSA/TSA-demo/TSA_mecha/TSA_intro_default_loop.mp3 &"
                        os.system(cmd1)
                        time.sleep(2)
                    else: print('none')    
                    print('firstloop: ', firstloop)               
                    print('background_thread is_alive: ', background_thread.is_alive())
                    if not background_thread.is_alive() and firstloop == 0:
                        background_thread.start()
                        #background_thread.join(timeout=2)
                        firstloop = 1
                    print('background_thread is_alive2: ', background_thread.is_alive())
                    print('background_thread enumerate: ', threading.enumerate())
                    print ("Checking")
                    intro = 0
                time.sleep(0.5)

# def initialAvaIntroServo(stop):
#     # AVA moving head
#     while True:
#         lock.acquire()
#         print("kit.servo[10].angle = 120")
#         time.sleep(3)
#         if stop():
#             lock.release()
#             print('getting a stop thread for initialAvaIntroServo')
#             break
#         print("kit.servo[10].angle = 105")
#         time.sleep(3)
#         if stop():
#             lock.release()
#             print('getting a stop thread for initialAvaIntroServo')
#             break
#         print("kit.servo[10].angle = 90")
#         time.sleep(3)
#         if stop():
#             lock.release()
#             print('getting a stop thread for initialAvaIntroServo')
#             break
#         print("kit.servo[10].angle = 75")
#         time.sleep(3)
#         if stop():
#             lock.release()
#             print('getting a stop thread for initialAvaIntroServo')
#             break
#         print("kit.servo[10].angle = 60")
#         time.sleep(3)
#         if stop():
#             lock.release()
#             print('getting a stop thread for initialAvaIntroServo')
#             break
#         print("kit.servo[10].angle = 90")
#         time.sleep(3)
#         lock.release()
#         if stop():
#             print('getting a stop thread for initialAvaIntroServo')
#             break



# def myNameisAvaServo(stop):
#     #left hand hi movement
#     lock.acquire()
#     print("kit.servo[3].angle = 120")
#     time.sleep(0.2)
#     print("kit.servo[3].angle = 90")
#     time.sleep(0.2)
#     print("kit.servo[3].angle = 70")
#     time.sleep(0.2)
#     print("kit.servo[3].angle = 40")
#     time.sleep(3)
#     print("kit.servo[3].angle = 70")
#     time.sleep(0.2)
#     print("kit.servo[3].angle = 90")
#     time.sleep(0.2)
#     print("kit.servo[3].angle = 120")
#     time.sleep(0.2)
#     print("kit.servo[3].angle = 180")
#     time.sleep(2)
#     lock.release()
#     if stop():
#         print('getting a stop thread for myNameisAvaServo')

        
# def Avadoyouhavequestion(stop):
#     #eyemovement
#     lock.acquire()
#     print("kit.servo[8].angle = 120")
#     time.sleep(2)
#     print("kit.servo[8].angle = 90")
#     time.sleep(2)
#     lock.release()
#     if stop():
#         print('getting a stop thread for Avadoyouhavequestion')

# def checkAgentontheright():
#     #righthandmovement
#     print("kit.servo[13].angle = 90")
#     time.sleep(2)
#     print("kit.servo[13].angle = 0")
#     time.sleep(2)
#     lock.release()

# def avagoodbye(stop):
#     #left hand hi movement
#     lock.acquire()
#     kit.servo[13].angle = 120
#     time.sleep(0.2)
#     kit.servo[12].angle = 90
#     time.sleep(0.2)
#     kit.servo[3].angle = 70
#     time.sleep(0.2)
#     kit.servo[3].angle = 40
#     time.sleep(3)
#     kit.servo[3].angle = 70
#     time.sleep(0.2)
#     kit.servo[3].angle = 90
#     time.sleep(0.2)
#     kit.servo[3].angle = 120
#     time.sleep(0.2)
#     kit.servo[3].angle = 180
#     time.sleep(2)
#     lock.release()
#     if stop():
#         print('getting a stop thread for myNameisAvaServo')




if __name__ == '__main__':
    if platform_sys !='Darwin':
        color_start()
    lock = threading.Lock()
    try:
        #if ser.is_open == False:
        #    ser.open()
        #mqtt_subscribe()
        getTFminiData()
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()
