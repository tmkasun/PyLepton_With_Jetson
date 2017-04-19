import cv2
import numpy as np
from pylepton_local import Lepton
import time
import subprocess  # doc https://goo.gl/iSGfZv


def change_dev_perm():
    print("Jetson Python CV2 version ={} ".format(cv2.__version__))
    proc = subprocess.Popen(['sudo', 'chmod', '777', '/dev/spidev0.0'])
    out, error = proc.communicate()
    print(out)
    return out, error


def capture(frames=100):
    with Lepton("/dev/spidev0.0") as lepton:
        print("Capturing ....")
        count = 1
        while frames > count:
            count += 1
            time.sleep(1)  # delays for 5 seconds
            raw_frame, _ = lepton.capture()
            raw_file = open("data/raw_sample_{}.csv".format(count), 'w+')
            np.savetxt(raw_file, raw_frame, delimiter=",", fmt='%i')
            raw_file.close()
            cv2.normalize(raw_frame, raw_frame, 0, 65535, cv2.NORM_MINMAX)  # extend contrast
            np.right_shift(raw_frame, 8, raw_frame)  # fit data into 8 bits
            cv2.imwrite("data/image_sample_{}.jpg".format(count), np.uint8(raw_frame))  # write it!
            # cv2.imshow('image', np.uint8(a))
            # key = cv2.waitKey(4) & 0xFF
            # if the `q` key was pressed, break from the loop
            # if key == ord("q"):
            #     break
            # cv2.waitKey(0)
            # video = cv2.VideoWriter('video.avi', -1, 1, (width, height)) # http://www.xavierdupre.fr/blog/2016-03-30_nojs.html or http://www.pyimagesearch.com/2016/02/22/writing-to-video-with-opencv/
    cv2.destroyAllWindows()


def main():
    change_dev_perm()
    capture()


if __name__ == '__main__':
    main()
