import serial
import time


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def color_float(r, g, b):
    """ Returns color in float components (0-1) from normal 24 bit image data (0-255) """
    _r = r/255.0 if r else 0
    _g = g/255.0 if g else 0
    _b = b/255.0 if b else 0
    return (_r, _g, _b)


class Color(object):
    pass


class Color16(Color):
    def __init__(self, r, g, b):
        """ 16 Bit colors
            Packs 3 4-bit color values into two bytes
            Takes 3 floats between 0 and 1
        """
        if r > 1 or g > 1 or b > 1:
            raise Exception("Expected color values between 0 and 1, got %s, %s, %s" % r, g, b)

        color = int(31*r) << 11
        color |= int(31*g) << 5
        color |= int(31*b)
        self.int_color = color

    def as_bytes(self):
        """ Returns a list of int-encoded colors """
        return bytearray([self.int_color >> 8, self.int_color & 255])

    @classmethod
    def many_as_bytes(cls, pixels):
        bytes = []
        for pixel in pixels:
            bytes += Color16(*color_float(*pixel)).as_bytes()
        return bytearray(bytes)


COLORS = {
    Color16: 0
}


class Matrix(object):
    def __init__(self, dev, width, height, color_type=Color16, baudrate=200000, serial_timeout=1):
        self.width = width
        self.height = height
        self.color_type=color_type
        self.image = None

        self.dev = dev
        self.baudrate = baudrate 
        self.serial_timeout = serial_timeout
        self.ser = serial.Serial(dev, baudrate, timeout=serial_timeout)

    def update(self):
        """ Send matrix data to LED matrix. 
            Set wait_for_reply to wait for and return 1 byte reply, 
            wait_for_empty_buffer to continue reading until the buffer is empty
        """
        if not self.image:
            return

        pixels = list(self.image.getdata())
        # Start with header
        # First 4 bytes: Panel address / Header identifier
        # 5th byte: color type (currently unused)
        send_buffer = bytearray([
          0B10101010,
          0B01010101,
          0B11001100,
          0B00010001,
          COLORS[self.color_type]
        ])

        send_buffer += self.color_type.many_as_bytes(pixels)
        self.send(send_buffer)
        self.ser.flushInput()

    def send(self, send_buffer, wait_for_reply=True, wait_for_empty_buffer=True):
        retval = []
        self.ser.write(bytearray(send_buffer))

        self.ser.flush()
        if wait_for_reply:
            reply = self.ser.readline().strip()
            if wait_for_empty_buffer:
                retval.append(reply)
            else:
                return reply

        if wait_for_empty_buffer:
            while self.ser.inWaiting():
                retval.append(self.ser.readline().strip())

        return retval
