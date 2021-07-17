import pytube
import inspect

from pytube.__main__ import YouTube
print(inspect.getfile(pytube))

test=YouTube('https://youtu.be/VawIB4N_gmM')
print(test.metadata)