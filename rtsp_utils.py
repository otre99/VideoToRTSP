import uuid
import multiprocessing
from multiprocessing import Event
import gi
gi.require_version("Gst", "1.0")
gi.require_version("GstRtspServer", "1.0")
from gi.repository import Gst, GstRtspServer, GLib

class UniquePorts:
    counter = 0
    port_numbers = [8100+i*100 for i in range(100)]

    @staticmethod
    def get_new_port() -> int:
        port = UniquePorts.port_numbers[UniquePorts.counter]
        UniquePorts.counter += 1
        return port

    @staticmethod
    def get_unique_factory_name():
        return str(uuid.uuid1())

def terminate_pipeline(p):
    if p.event.is_set():
        print(f"\nFinishing process {p.name}\n ")
        p.mainloop.quit()
    return True

class AnyToRTSP(multiprocessing.Process):
    V4L2_DEVICE = 0
    VIDEO_FILE = 1

    def __init__(self, source: str, input_type: int, event: Event):
        super(AnyToRTSP, self).__init__()
        self.port_number = UniquePorts.get_new_port()
        self.factory_name = UniquePorts.get_unique_factory_name()

        if input_type == AnyToRTSP.V4L2_DEVICE:
            self.gst_pipeline = f'v4l2src device={source} ! videoconvert ! video/x-raw,format=I420 ! x264enc tune=zerolatency ! rtph264pay name=pay0'
        elif input_type == AnyToRTSP.VIDEO_FILE:
            self.gst_pipeline = f'filesrc location={source} ! decodebin ! videoconvert ! video/x-raw,format=I420 ! x264enc tune=zerolatency ! rtph264pay name=pay0'
        else:
            raise RuntimeError("Wrong input type!")
        
        self.event = event

    def get_rtsp_uri(self):
        return f"rtsp://127.0.0.1:{self.port_number}/{self.factory_name}"

    def set_v4l2_device(self, v4l2_device: str):
        self.v4l2_device = v4l2_device

    def run(self):
        Gst.init(None)
        self.mainloop = GLib.MainLoop()
        server = GstRtspServer.RTSPServer()
        server.props.service = f"{self.port_number}"
        mounts = server.get_mount_points()
        factory = GstRtspServer.RTSPMediaFactory()
        factory.set_launch(self.gst_pipeline)
        mounts.add_factory(f"/{self.factory_name}", factory)
        server.attach(None)
        GLib.timeout_add_seconds(1, terminate_pipeline, self)
        self.mainloop.run()
