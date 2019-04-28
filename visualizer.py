from pydub import AudioSegment
import pyaudio
import numpy as np
from pydub.utils import get_array_type
import matplotlib.pyplot as plt
import time


np.set_printoptions(suppress=True)

CHUNK = 4096
RATE = 44100

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK, as_loopback=True)


for i in range(int(600*RATE/CHUNK)):
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    data = data * np.hanning(len(data)) 
    fft = abs(np.fft.fft(data).real)
    fft = fft[:int(len(fft)/2)]
    freq = np.fft.fftfreq(CHUNK,1.0/RATE)
    freq = freq[:int(len(freq)/2)] 
    freqPeak = freq[np.where(fft==np.max(fft))[0][0]]+1
    print("peak frequency: %d Hz"%freqPeak)
    plt.plot([i+100, i+100], [0, freqPeak], 'b', linewidth=4.0)
    plt.axis([i, i+100, 0, 1500])
    plt.title(i)
    plt.savefig("static/03.png",dpi=50)

stream.stop_stream()
stream.close()
p.terminate()

