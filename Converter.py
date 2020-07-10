import os
import cv2
import time
import numpy as np
from PIL import Image
from numpy import ndarray
from os import system


class Converter:
    def __init__(self, framerate=30):
        self.frames = []
        # self.reprs = ["X ", "x "]
        self.reprs = ["  ", ". ", ", ", "; ", "o ", "@ ", "* ", "0 ", "# "]
        self.framerate = framerate
        self.terminal_size = self.get_terminal_size()

    def convert_video(self, path, size_ratio=1.0, contrast=1.0, sharpen=1.0, invert=False, rotation=0, auto_scale=False):
        frames = self.extract_frame_from_video(path)
        if invert:
            self.reprs.reverse()

        for i, frame in enumerate(frames):
            # Load image
            image = Image.fromarray(frame)
            self.__generate_frame(image, size_ratio, contrast, sharpen, rotation, auto_scale)
            self.clear()
            print(round(i/len(frames), 3) * 100, "% Complete")

    def convert_image(self, path, size_ratio=1.0, contrast=1.0, sharpen=1.0, invert=False, rotation=0, auto_scale=False):
        # Load image
        image = Image.open(path)

        if invert:
            self.reprs.reverse()

        self.__generate_frame(image, size_ratio, contrast, sharpen, rotation, auto_scale)

    def live_stream(self, size_ratio=0.07, contrast=1.0, sharpen=1.0, invert=False, auto_scale=False):
        if invert:
            self.reprs.reverse()
        cap = cv2.VideoCapture(0)
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            frame = Image.fromarray(frame)
            self.__generate_frame(frame, size_ratio, contrast, sharpen, rotation=0, auto_scale=auto_scale)
            self.clear()
            print(self.frames[0])
            self.frames = []

            # self.convert_image()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def show(self):
        for frame in self.frames:
            print(frame)
            time.sleep(1/self.framerate)

    def play_video(self, num_loops=1):
        terminal_width = str(self.frames[0].find("\n"))
        terminal_height = str(int(self.frames[0].find("\n")/2) + 2)
        os.system('resize -s ' + terminal_height + " " + terminal_width)
        self.clear()
        print("Done :)")
        time.sleep(0.5)
        for _ in range(num_loops):
            for frame in self.frames:
                self.clear()
                print(frame)
                time.sleep(1 / self.framerate)

    def save_frames(self):
        np.save("Frames/frames", np.array(self.frames))

    def load_frames(self, path):
        self.frames = np.load("Frames/"+path)

    def __generate_frame(self, image, size_ratio=1.0, contrast=1.0, sharpen=1.0, rotation=0, auto_scale=True):
        assert 0 < contrast

        # set the contrast to its inverse (this is to make it simple in the input)
        contrast = 1/contrast

        # Crop it to a square
        width, height = image.size
        new_length = min(width, height)
        center = width/2, height/2
        left = center[0] - new_length/2
        right = center[0] + new_length/2
        upper = center[1] - new_length/2
        lower = center[1] + new_length/2
        box = left, upper, right, lower
        image = image.crop(box)

        # Resize & rotate the image
        width = int(image.size[0]*size_ratio)
        height = int(image.size[1]*size_ratio)

        # Will auto scale to fit the terminal size
        if width > self.terminal_size[0] or height > self.terminal_size[1] or auto_scale:
            self.terminal_size = self.get_terminal_size()
            size_ratio_x = self.terminal_size[0]/image.size[0]
            size_ratio_y = self.terminal_size[1]/image.size[1]
            size_ratio = min(size_ratio_x, size_ratio_y)
            width = int(image.size[0] * size_ratio)
            height = int(image.size[1] * size_ratio)

        image = image.resize((width, height), Image.ANTIALIAS)
        image = image.rotate(rotation)

        # Convert image to array
        image = np.array(image)

        # Gray scale the image
        rgb_weights = [0.2989, 0.5870, 0.1140]
        image: ndarray = np.dot(image[..., :3], rgb_weights)

        # Gather all of the pixels
        pixels = list(image.tolist())

        # Create a frame and fill it with unicode
        frame = ""
        for row in pixels:
            for pv in row:

                # Normalize the pixel
                pv = pv/255

                # Sharpen the pixel
                pv = self.sharpen(pv, sharpen)

                # Map the value to a unicode character
                mapped_index = int((pv/contrast) * (len(self.reprs) - 1))
                mapped_index = self.clamp(mapped_index, 0, len(self.reprs) - 1)

                # Add the character to the frame
                frame += self.reprs[mapped_index]

            frame += "\n"

        self.frames.append(frame)

    @staticmethod
    def extract_frame_from_video(path):
        vid_cap = cv2.VideoCapture(path)
        success, frame = vid_cap.read()
        count = 0

        frames = []
        while success:
            frames.append(frame)
            success, frame = vid_cap.read()
            count += 1
        return frames

    @staticmethod
    def sharpen(pixel, value):
        return pixel ** value

    @staticmethod
    def clamp(value, min_val, max_val):
        if min_val <= value <= max_val:
            return int(value)
        if min_val > value:
            return int(min_val)
        if max_val < value:
            return int(max_val)

    @ staticmethod
    def rgb2gray(rgb):
        r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

        return gray

    # define our clear function
    @staticmethod
    def clear():
        system('clear')

    @staticmethod
    def get_terminal_size():
        import os
        env = os.environ

        def ioctl_GWINSZ(fd):
            try:
                import fcntl, termios, struct, os
                cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                                                     '1234'))
            except:
                return
            return cr

        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass
        if not cr:
            cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

            ### Use get(key[, default]) instead of a try/catch
            # try:
            #    cr = (env['LINES'], env['COLUMNS'])
            # except:
            #    cr = (25, 80)
        return int(cr[1]), int(cr[0])


# converter = Converter(framerate=30)
# converter.convert_video("Random stuff/Sami.mp4",
#                         0.06, 3, 1.1,  False, rotation=-90)
# converter.play_video()
#
# converter = Converter(framerate=30)
# converter.convert_video("Random stuff/riley2.mp4",
#                         0.065, 3, 1, True, rotation=0)
# converter.play_video()

# converter = Converter()
# converter.live_stream(invert=False)
