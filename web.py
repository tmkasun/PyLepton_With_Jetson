import tornado.ioloop
import tornado.web
from tornado.websocket import WebSocketHandler
import cv2
import numpy as np
from pylepton_local import Lepton
import subprocess  # doc https://goo.gl/iSGfZv
import json
import glob


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        msg = "FLIR Lepton Data Service"
        self.write(msg)


class MockData:
    def __init__(self):
        self.path = "/home/tmkasun/Documents/pvt/projects/fyp/jetson/pylepton_jetson_module/samples/*.csv"
        files = glob.iglob(self.path)
        self.sorted_files = sorted(files, key=lambda name: int(name.split("_")[-1].split(".")[0]))
        self.samples = iter(self.sorted_files)

    def get_next_sample(self):
        try:
            next_frame = self.samples.next()
        except StopIteration as e:
            print("Re-sending file")
            self.reload_samples()
            next_frame = self.samples.next()
        frame = np.genfromtxt(next_frame, delimiter=",", defaultfmt="%i")
        return frame.astype(np.uint16)

    def reload_samples(self):
        self.samples = iter(self.sorted_files)


class ThermalDataHandler(WebSocketHandler):
    clients = []
    DEBUG = False

    def __init__(self, application, request, **kwargs):
        super(ThermalDataHandler, self).__init__(application, request, **kwargs)
        if not ThermalDataHandler.DEBUG:
            self.lepton = Lepton("/dev/spidev0.0")
            self.lepton.__enter__()
        self.mock_samples = MockData()

    def check_origin(self, origin):
        return True

    def open(self):
        if self not in ThermalDataHandler.clients:
            self.write_message("ACK")
            ThermalDataHandler.clients.append(self)

    def on_close(self):
        if self in ThermalDataHandler.clients:
            ThermalDataHandler.clients.remove(self)

    def on_message(self, message):
        self.write_message(self._get_data())

    def data_received(self, chunk):
        pass

    def _get_data(self):
        if ThermalDataHandler.DEBUG:
            raw_frame = self.mock_samples.get_next_sample()
        else:
            raw_frame, _ = self.lepton.capture()
            raw_frame.astype(np.uint16)
        return json.dumps(raw_frame.tolist())


def change_dev_params():
    print("Jetson Python CV2 version ={} ".format(cv2.__version__))
    proc = subprocess.Popen(['sudo', 'chmod', '777', '/dev/spidev0.0'])
    out, error = proc.communicate()
    print(out)
    return out, error


def make_app():
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/ws", ThermalDataHandler),
    ])


if __name__ == "__main__":
    change_dev_params()
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
