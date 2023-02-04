# VideoToRTSP
Simple python gstreamer app for create rtsp from video files and v4l2 devices

## Usage
```
$ python3 src/main.py   --help
usage: main.py [-h] [--v4l2_devices V4L2_DEVICES [V4L2_DEVICES ...]] [--video_files VIDEO_FILES [VIDEO_FILES ...]]

Create RTSP stream

options:
  -h, --help            show this help message and exit
  --v4l2_devices V4L2_DEVICES [V4L2_DEVICES ...]
                        V4L2 input devices
  --video_files VIDEO_FILES [VIDEO_FILES ...]
                        Video inputs

```

## Examples:

### USB camera
```
python3 src/main.py --v4l2_devices /dev/video0 
--------------------------------------------------------------------------------------------------------------------------------
source: /dev/video0
Use this command for visualize the RTSP stream:
gst-launch-1.0 rtspsrc location=rtsp://127.0.0.1:8100/f856e2a2-a429-11ed-9b91-379cd3c2a23d latency=10 ! decodebin ! videoconvert ! autovideosink
--------------------------------------------------------------------------------------------------------------------------------
Ctr+C to finish!
```

### Two USB cameras
```
python3 src/main.py --v4l2_devices /dev/video0 /dev/video5 
--------------------------------------------------------------------------------------------------------------------------------
source: /dev/video0
Use this command for visualize the RTSP stream:
gst-launch-1.0 rtspsrc location=rtsp://127.0.0.1:8100/182d83a6-a4ca-11ed-96ba-5fd91382719b latency=10 ! decodebin ! videoconvert ! autovideosink
--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------
source: /dev/video5
Use this command for visualize the RTSP stream:
gst-launch-1.0 rtspsrc location=rtsp://127.0.0.1:8200/182d83a7-a4ca-11ed-96ba-5fd91382719b latency=10 ! decodebin ! videoconvert ! autovideosink
--------------------------------------------------------------------------------------------------------------------------------
Ctr+C to finish!
```

### USB camera and two videos 
```
python3 src/main.py --v4l2_devices /dev/video0 --video_files videos/sample00.mp4 videos/sample01.mp4 
--------------------------------------------------------------------------------------------------------------------------------
source: /dev/video0
Use this command for visualize the RTSP stream:
gst-launch-1.0 rtspsrc location=rtsp://127.0.0.1:8100/619db3b2-a4ca-11ed-96ba-5fd91382719b latency=10 ! decodebin ! videoconvert ! autovideosink
--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------
source: videos/sample00.mp4
Use this command for visualize the RTSP stream:
gst-launch-1.0 rtspsrc location=rtsp://127.0.0.1:8200/619db3b3-a4ca-11ed-96ba-5fd91382719b latency=10 ! decodebin ! videoconvert ! autovideosink
--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------
source: videos/sample01.mp4
Use this command for visualize the RTSP stream:
gst-launch-1.0 rtspsrc location=rtsp://127.0.0.1:8300/619db3b4-a4ca-11ed-96ba-5fd91382719b latency=10 ! decodebin ! videoconvert ! autovideosink
--------------------------------------------------------------------------------------------------------------------------------
Ctr+C to finish!
```