import os
import subprocess
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
GPIO.setmode(GPIO.BOARD)
chan_list = [11,12]
GPIO.setup(chan_list, GPIO.IN) 
  


def stream_loader(streams,x): 
  if x != -1:
      stream = subprocess.Popen(["google-chrome", "--app","--start-fullscreen",streams[x]])
  while True:
    for i,chan in enumerate(chan_list):
      if GPIO.input(chan) == True:
	if i == x:
	  stream.send_signal(SIGTERM) 
	  return 
	else:
	  stream.send_signal(SIGTERM)
	  return stream_loader(streams[i],i)
	    
	      
if __name__ == '__main__': 
  streams= ["https://home.nest.com/camera/105b06ffae6f4a1197c6d440e0180f38", "https://home.nest.com/camera/1e5cd590b5eb42cb8647d305e1bd0d32" ]
  picture_paths="~/Pictures"
  eog = subprocess.Popen(["eog", picture_paths])
  stream_loader(streams,-1)
      