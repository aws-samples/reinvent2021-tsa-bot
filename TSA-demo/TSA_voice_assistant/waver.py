import pyaudio
import wave
import os
import numpy as np
from sys import byteorder
from array import array



#CHUNK = 1024
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
#RATE = 44100
RATE = 16000
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=RATE,
                 input=True,
                 frames_per_buffer=CHUNK)

# print("* recording")

def wavmaker(stream):
    frames = []
    recording = array('h')

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        sch = stream.read(CHUNK)
        data = sch
        frames.append(data)
        datab = array('h', sch)
        if byteorder == 'big':
            datab.byteswap()
        recording.extend(datab)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    os.system('ffmpeg -i output.wav -ar 16000 -ac 1 trackb.wav -y')

    #print(recording)
    return recording

def main():
    top = wavmaker(stream)


if __name__ == "__main__":
    main()