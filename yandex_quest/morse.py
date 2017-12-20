import wave
from scipy.ndimage.filters import gaussian_filter

wav = wave.open("music.wav", mode="r")
(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
content = wav.readframes(nframes)

from matplotlib import pyplot as plot
import numpy as np
import math
types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

duration = nframes / framerate
w, h = 800, 300
DPI = 72
peak = 256 ** sampwidth / 2
k = nframes/w/32

samples = np.fromstring(content, dtype=types[sampwidth])

samples = abs(samples[1::10])


blurred = gaussian_filter(samples, sigma=10)
blurred[blurred <= 250] = 0
blurred[blurred > 250] = 1
#
# blurred = gaussian_filter(samples, sigma=1)
#
# blurred[blurred <= 250] = 0
# blurred[blurred > 250] = 1


#blurred = gaussian_filter(samples, sigma=1)

#
# blurred[blurred <= 500] = 0
# blurred[blurred > 500] = 1
cur = 0
lenz = 0
ans = list()
for i in range(len(blurred)):
    if blurred[i] != 0:
        if lenz > 1150:
            ans.append(' ')
        lenz = 0
    if blurred[i] == 0:
        lenz += 1
        if cur  >= 950:
            if cur >= 2000:
                ans.append('-')
            else:
                ans.append('.')
        cur = 0
    cur += blurred[i]
    blurred[i] = lenz


with open('output.txt', 'w') as file:
    for elem in ans:
        file.write(elem)


for i in range(len(blurred)):
    print ( blurred[i] )
#
#
# print()

plot.plot(blurred)

plot.show()

