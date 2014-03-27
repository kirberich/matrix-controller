import argparse
from PIL import Image
import random
import time
import urllib, cStringIO

from display import Display
from matrix import Matrix

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Show image stream from url on led matrix, will refetch image for every frame')
    parser.add_argument('dev', type=str, help='serial device the arduino is connected to')
    parser.add_argument('url', type=str, help='url for image stream')
    args = parser.parse_args()

    matrix = Matrix(args.dev, 32, 32)

    display = Display(fonts=[]) # Add font paths here
    display.add_matrix(matrix)

    while True:
        begin = time.time()

        f = cStringIO.StringIO(urllib.urlopen(args.url).read())
        img = Image.open(f)
        img.thumbnail((32, 32), Image.ANTIALIAS)
        size = img.size

        display.clear()

        display.bounding_image.paste(img, (0, (32-size[1])/2))

        display.update()
        print "%.1ffps" % (1/(time.time() - begin))