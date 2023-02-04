import argparse
from rtsp_utils import AnyToRTSP
import time
import signal
from multiprocessing import Event

process_event = Event()

def print_info(source, rtsp_uri):
    print("-"*128)
    print(f"source: {source}")
    print("Use this command for visualize the RTSP stream:")
    print(
        f"gst-launch-1.0 rtspsrc location={rtsp_uri} latency=10 ! decodebin ! videoconvert ! autovideosink")
    print("-"*128)

def main(FLAGS):
    global process_event

    running_process = []
    # v4l2 devices
    for source in FLAGS.v4l2_devices:
        p = AnyToRTSP(source=source, input_type=AnyToRTSP.V4L2_DEVICE, event=process_event)
        print_info(source=source, rtsp_uri=p.get_rtsp_uri())
        running_process.append(p)
        p.start()

    # video files
    for source in FLAGS.video_files:
        p = AnyToRTSP(source=source, input_type=AnyToRTSP.VIDEO_FILE, event=process_event)
        print_info(source=source, rtsp_uri=p.get_rtsp_uri())
        running_process.append(p)
        p.start()

    print("Ctr+C to finish!")
    for p in running_process:
        p.join()

def terminate_app(_signo, _stack_frame):
    global process_event
    process_event.set()

signal.signal(signal.SIGINT, terminate_app)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create RTSP stream")
    parser.add_argument('--v4l2_devices', nargs='+',
                        help="V4L2 input devices", default=[])
    parser.add_argument('--video_files', nargs='+',
                        help="Video inputs", default=[])

    FLAGS, unparsed_args = parser.parse_known_args()
    if len(unparsed_args):
        print("Warning: unknow arguments {}".format(unparsed_args))

    main(FLAGS=FLAGS)
