require 'dropcam'
dropcam = Dropcam::Dropcam.new("miniwb@me.com","robonaut")
camera = dropcam.cameras.first

# record the live stream for 30 seconds
camera.stream.save_live("#{camera.title}.flv", 30)

# to get access information to use a third party application
# RTMP/Flash Streaming
camera.stream.rtmp_details

# RTSP Streaming
camera.stream.rtsp_details
