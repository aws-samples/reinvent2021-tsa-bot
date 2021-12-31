#!/usr/bin/env python3

# SPDX-FileCopyrightText: Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# SPDX-License-Identifier: MIT-0

from sys import byteorder
from array import array
import base64
import os
import pyaudio
import boto3
import uuid
import zlib
import json
import time
from waver import wavmaker

from pathlib import Path
from dotenv import load_dotenv

# Get the base directory
basepath = Path()
basedir = str(basepath.cwd())
# Load the environment variables
envars = os.path.dirname(basepath.cwd())+'/TSA_mecha/.env'
print(envars)
load_dotenv(envars)


session = boto3.Session(aws_access_key_id=os.getenv('AWS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))

#import iot_sub
#from iot_sub import mqtt_subscribe, mqtt_publish

import struct
#import pvporcupine
#print(pvporcupine.KEYWORDS)

import platform
platform_sys=platform.system()
print('platform: ',platform_sys)

porcupine = None
pa = None
audio_stream = None

from ctypes import *
from contextlib import contextmanager

if platform_sys != "Darwin":
    from gpiozero import LED
    from apa102 import APA102

    COLORS_RGB = dict(
        blue=(0, 0, 255),
        green=(0, 255, 0),
        orange=(255, 128, 0),
        pink=(255, 51, 153),
        purple=(128, 0, 128),
        red=(255, 0, 0),
        white=(255, 255, 255),
        yellow=(255, 255, 51),
        off=(0, 0, 0),
    )

    KEYWORDS_COLOR = {
        'picovoice': 'green',
        'porcupine': 'blue',
        'blueberry': 'orange',
        'terminator': 'off',
    }

    driver = APA102(num_led=12)
    power = LED(5)
    power.on()

    keywords = list(KEYWORDS_COLOR.keys())

#Change to reflect the bot and alias you created
#bot_id = 'AVLBAKUHJ9'
#bot_alias_id='4ZTMYYWUQA'
bot_id = 'ISXIO344FF'
bot_alias_id='ZWIGXTFIAU'

THRESHOLD = 500
CHUNK_SIZE = 2048
FORMAT = pyaudio.paInt16
RATE = 16000
#RATE = 44100
VOICE_ID = None

polly = session.client('polly')
lexv2 = session.client('lexv2-runtime')
translate = session.client(service_name='translate', region_name='us-east-1', use_ssl=True)

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    if platform_sys != 'Darwin':
        asound = cdll.LoadLibrary('libasound.so')
        asound.snd_lib_error_set_handler(c_error_handler)
        yield
        asound.snd_lib_error_set_handler(None)
        print("noalsoerr activated")
    else:
        yield
        print('no alsa err mode deactivated')

def is_silent(data):
    return max(data) < THRESHOLD

def record_phrase():

    with noalsaerr():
        num_silent = 0
        start = False
        p = pyaudio.PyAudio()

        #info = p.get_host_api_info_by_index(0)
        #numdevices = info.get('deviceCount')
        #for i in range(0, numdevices):
        #    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        #        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i))


        if platform_sys == 'Darwin':
            #stream config for mac
            stream = p.open(format=FORMAT, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)
        else:
            #stream config for RaspPiI
            #stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE, input_device_index=2)
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)
            #stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
            #stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024, input_device_index=1)
    
        stream.start_stream()
        recording = array('h')
        while True:
            data = array('h', stream.read(CHUNK_SIZE))
            if byteorder == 'big':
                data.byteswap()
            recording.extend(data)
            silent = is_silent(data)
            if silent and start:
                num_silent += 1
                sessionlength +=1
            elif not silent and not start:
                start = True
                num_silent = 0
                sessionlength = 0
            if start:
                sessionlength +=1
            if start and num_silent > 15:
                break
            if start and sessionlength > 80:
                break

        #try:
        #    wavmaker(stream)
        #except Exception as e:
        #    print('wavemaker issue: ', e)
        stream.stop_stream()
        stream.close()
        p.terminate()
        if platform_sys != 'Darwin':
            set_color("off")
            print("turning off leds and returning recorded voice")

        return recording

def play_audio(audio):
    p = pyaudio.PyAudio()
    #stream = p.open(format=FORMAT, channels=1, rate=RATE, output=True)
    stream = p.open(format=FORMAT, channels=1, rate=RATE, output=True, input_device_index=2)
    stream.write(audio.read())
    stream.stop_stream()
    stream.close()


def set_color(colori):
    color = COLORS_RGB[colori]
    for i in range(12):
        driver.set_pixel(i, color[0], color[1], color[2])
    driver.show()

def color_start():
    pixels_number = 12
    pixels  = [0, 0, 12, 12, 0, 0, 0, 24] * pixels_number

    cc = 0
    while cc  <= 20:
        for i in range(12):
            driver.set_pixel(i, pixels[4*i + 1], pixels[4*i + 2], pixels[4*i + 3])
            driver.show()
        time.sleep(0.2)
        pixels = pixels[-4:] + pixels[:-4]
        cc +=1

    set_color("off")

def translatelang(text,lang):
    result = translate.translate_text(Text=text, 
            SourceLanguageCode="en", TargetLanguageCode=lang)
    print('TranslatedText: ' + result.get('TranslatedText'))
    print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
    print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))
    return result.get('TranslatedText')


def word():
    try:
        with noalsaerr():
            porcupine = pvporcupine.create(keywords=["picovoice", "blueberry"])
            #porcupine = pvporcupine.create(keyword_paths=['picovoice/hey-t-s-a-bot__en_mac_2021-10-21-utc_v1_9_0.ppn'])
    
            pa = pyaudio.PyAudio()
    
            audio_stream = pa.open(
                            rate=porcupine.sample_rate,
                            channels=1,
                            format=pyaudio.paInt16,
                            input=True,
                            #input_device_index=2,
                            frames_per_buffer=porcupine.frame_length)
         
            print('[Listening...]')
    
            while True:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                keyword_index = porcupine.process(pcm)

                if keyword_index >= 0:
                    print("Hotword '%s' Detected" % keywords[keyword_index])
                    if platform_sys != 'Darwin':
                        set_color(COLORS_RGB[KEYWORDS_COLOR[keywords[keyword_index]]])
                    return "hotword"

    except Exception as e: print('word exception: ',e)

    finally:
            if porcupine is not None:
                porcupine.delete()

            if audio_stream is not None:
                audio_stream.close()
                print('audio stream closed')

            if pa is not None:
                pa.terminate()
                print("pa terminated")

def synthesize_speech(message,text_type):
    global VOICE_ID
    if VOICE_ID is None:
        VOICE_ID = get_voiceid()
    response = polly.synthesize_speech(
        Engine='standard',
        OutputFormat = 'pcm',
        Text = message,
        VoiceId = VOICE_ID,
        TextType=text_type
    )
    audio = response['AudioStream']
    play_audio(audio)

def call_lexv2(session_id, recording, locale_Id):
    try:
        print('locale_Id: ', locale_Id)
        response = lexv2.recognize_utterance(
            botId=bot_id,
            botAliasId=bot_alias_id,
            localeId=locale_Id,
            sessionId=session_id,
            requestContentType='audio/l16; rate=16000; channels=1',
            responseContentType='audio/pcm',
            inputStream=recording
        )
        print("Lex response ", response)

        return response
    except Exception as e: 
        print("there is an error: ", e)
        synthesize_speech("I could not understand", "text")
        return "none"

def decode(data):
    decoded_data = base64.b64decode(data)
    decompressed_data = zlib.decompress(decoded_data, 16+zlib.MAX_WBITS)
    return json.loads(decompressed_data)

def get_voiceid():
    lexv2_model = session.client('lexv2-models')
    bot_alias = lexv2_model.describe_bot_alias(
        botAliasId = bot_alias_id,
        botId = bot_id
    )
    bot_locale = lexv2_model.describe_bot_locale(
        botId = bot_id,
        botVersion = bot_alias['botVersion'],
        localeId = 'en_US'
    )
    return bot_locale['voiceSettings']['voiceId']

def main():
    print("starting")
    #word()
    #print ('bot: ', bot)
    print("going to record")
    session_id = str(uuid.uuid4())
    #while 1:
    while iot_sub.launchlextt:
        try:
            if platform_sys != 'Darwin':
                        set_color(COLORS_RGB[KEYWORDS_COLOR['porcupine']])
            print('iot_sub.launchlextt2: ', iot_sub.launchlextt)
            recording = record_phrase()
            if not iot_sub.launchlextt:
                print('stop in middle')
                break
            response = call_lexv2(session_id, bytes(recording))
            if response == 'none':
                break    
            play_audio(response['audioStream'])
            session_state = decode(response['sessionState'])
            dialog_action = session_state['dialogAction']['type']
            state = session_state['intent']['state']
            if dialog_action == 'Close' and state == 'Fulfilled':
                break
        except Exception as e:
            print(e)

if __name__ == "__main__":
    bot = True
    global launchlex 
    launchlex = False
    #sub = mqtt_subscribe()
    intro = 0
    close = 0
    if platform_sys !='Darwin':
        color_start()
    while bot:
        pass
        #print('bot: ',bot)
        #print('iot_sub.launchlextt: ', iot_sub.launchlextt)
        #print('sub: ', sub)
        #if iot_sub.launchlextt:
            #if intro == 0:
                # synthesize_speech("Hello. I am T. S. A. Bot. How can I help?")
                # main()
                # intro +=1
                # close += 1
            #else:
                # time.sleep(4)
                # print("Do you have a question?.")
                # synthesize_speech("Do you have a question?.")
                # main()
                #synthesize_speech("Do you have another question?.")
                #synthesize_speech("Would you like to try again?.")
                # if platform_sys !='Darwin':
                #     set_color(COLORS_RGB["white"])
                #     time.sleep(0.5)
                #     set_color(COLORS_RGB["off"])
                #iot_sub.launchlextt = False
        # else:
        #     if close != 0:
        #         synthesize_speech("Thank you. Have a nice day!")
        #         close = 0
        #     intro = 0
        #     pass
        # time.sleep(2)

        #while 1:
        #    key = input("Please input y/n: ")
        #    if key == 'y':
        #        break
        #    elif key == 'n':
        #        bot = False
        #        break
        #    else:
        #        synthesize_speech("Please input y or n.")
    #synthesize_speech("Thank you. Have a nice day!")
