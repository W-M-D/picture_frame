import imghdr
import os
import sys
import subprocess
import pycurl
import time
import os
import getopt
from StringIO import StringIO
from Tkinter import *
from PIL import Image
from PIL import ImageTk


try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(25,GPIO.IN,pull_up_down=GPIO.PUD_UP)

global current_button  
    

def get_stream(stream_number):
  buffer = StringIO()
  streams= ["https://nexusapi.camera.home.nest.com/get_image?uuid=491567dcb751497da1fa738675e69a57&width=1920", "https://nexusapi.camera.home.nest.com/get_image?uuid=105b06ffae6f4a1197c6d440e0180f38&width=768","https://nexusapi.camera.home.nest.com/get_image?uuid=1e5cd590b5eb42cb8647d305e1bd0d32&width=768"]
  cookie= "Cookie: _ga=GA1.2.966868959.1461273764; _ga=GA1.3.966868959.1461273764; website_2=73de26ba804842418f97af6751cf366672a0823608927e484f8e2989ef732fcb1a1a7205; eu_compliance=2; n=eyJoYXMiOnsiMTM3MDg3OCI6eyJzdHIiOjF9fSwiaWRzIjpbIjEzNzA4NzgiXX0%3D"
  delete_frame = "" 
  current_frame = ""
  buffer_frame = ""
  download_size = 0
  headers= []
  i = 0 
  headers.append(cookie)
  for i in range(0,10):
      nest_stream = pycurl.Curl()
      nest_stream.setopt(pycurl.URL,streams[stream_number])
      nest_stream.setopt(pycurl.HTTPHEADER,headers)
      nest_stream.setopt(pycurl.WRITEFUNCTION, buffer.write)
      nest_stream.setopt(nest_stream.ENCODING, 'gzip,deflate')
      
      
      buffer_frame = "/tmp/{num}.jpg".format(num=i)

      with open(buffer_frame, 'w') as f:
        nest_stream.setopt(nest_stream.WRITEFUNCTION, f.write)
        nest_stream.perform()
        download_size = nest_stream.getinfo(nest_stream.CONTENT_LENGTH_DOWNLOAD)
        nest_stream.close()
    if i >= 2:
          current_frame = "/tmp/{num}.jpg".format(num=i-2)
          if imghdr.what(buffer_frame) == 'jpeg':
          eog = subprocess.Popen(["eog","-wf",buffer_frame]) 
    if i >= 6:
          delete_frame = "/tmp/{num}.jpg".format(num=i-6)
          os.remove(delete_frame)
      except:
        e = sys.exc_info()[0]
        print(e)

def picture_slideshow(picture_paths):
        global current_picture
    while(1):
        print current_button
        try:
            eog = subprocess.Popen(["eog","-wf", picture_paths[int(current_picture)]])
            time.sleep(4)
        except:
            e = sys.exc_info()[0]
            print(e)
            continue

        current_picture += 1
        

def stream_one_callback(chan):
    global current_button
    print("got to stream one")
    print(chan)
    if chan == 18:
        picture_slideshow(picture_paths)
    if chan == 23:
        current_button = 0
        get_stream(current_button)          
    if chan == 24:
        current_button = 1
        get_stream(current_button)          
    if chan == 25:
        current_button = 2
        get_stream(current_button)          

    
      
if __name__ == '__main__': 
    i = 0 
    current_button = -1
    picture_paths = []
    for path, subdirs, files in os.walk("/media/pi/My Passport/Images"):
        for name in files:
           picture_paths.append(os.path.join(path, name))


    GPIO.add_event_detect(18, GPIO.FALLING, callback=stream_one_callback, bouncetime=300)  
    GPIO.add_event_detect(23, GPIO.FALLING, callback=stream_one_callback, bouncetime=300)  
    GPIO.add_event_detect(24, GPIO.FALLING, callback=stream_one_callback, bouncetime=300)  
    GPIO.add_event_detect(25, GPIO.FALLING, callback=stream_one_callback, bouncetime=300)  
    while(1):
              stream_one_callback(18)


