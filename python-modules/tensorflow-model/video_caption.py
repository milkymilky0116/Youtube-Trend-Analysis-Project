from PyKomoran import *
from pytube import YouTube, captions
import pytube
import inspect

yt_link=YouTube('https://youtu.be/1CxGRz9hRk4')
caption=yt_link.captions['a.ko']
print(caption.xml_captions)
#print(caption.generate_srt_captions())

print(inspect.getfile(pytube))