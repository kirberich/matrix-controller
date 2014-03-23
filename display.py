from PIL import Image, ImageDraw, ImageFont


class Rect(object):
    """ Simple rectangle """
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def as_tuple(self):
        return (self.x1, self.y1, self.x2, self.y2)


class DisplayMatrix(object):
    """ Part of a display, represents one Matrix and its position on the display """

    def __init__(self, matrix, x, y):
        self.matrix = matrix
        self.x = x
        self.y = y

        # Bounding box of matrix in display coordinates for convenience 
        self.display_box = Rect(x, y, x + matrix.width, y + matrix.height)


class Display(object):
    """ Virtual display, made up of one or more led matrices """

    def __init__(self, fonts=[]):
        self.display_matrices = []
        self.bounding_image = None
        self.draw = None

        self.fonts = []
        for font_path in fonts:
            self.fonts.append(ImageFont.truetype(font_path, 22, encoding="unic"))

    def add_matrix(self, matrix, x=0, y=0):
        display_matrix = DisplayMatrix(matrix, x, y)
        self.display_matrices.append(display_matrix)

        # Calculate new bounding image
        max_x = 0
        max_y = 0

        for display_matrix in self.display_matrices:
            box = display_matrix.display_box
            max_x = max(max_x, box.x2)
            max_y = max(max_y, box.y2)

        self.bounding_image = Image.new("RGB", (max_x, max_y), "black")
        self.draw = ImageDraw.Draw(self.bounding_image)

    def clear(self):
        self.bounding_image = Image.new("RGB", self.bounding_image.size, "black")
        self.draw = ImageDraw.Draw(self.bounding_image)

    def line(self, x1, y1, x2, y2, color):
        self.lines([(x1, y1, x2, y2)], color)

    def lines(self, lines, color):
        self.draw.line(lines, fill=color) 

    def point(self, x, y, color):
        self.points([(x,y)], color)

    def points(self, points, color):
        self.draw.point(points, fill=color)

    def polygon(self, points, color, fill=None):
        self.draw.polygon(points, outline=color, fill=fill)

    def rect(self, x1, y1, x2, y2, color, fill=None):
        self.draw.rectangle((x1, y1, x2, y2), outline=color, fill=fill)

    def text(self, x, y, text, font_index, color):
        font = self.fonts[font_index]
        self.draw.text((x, y), text, font=font, fill=color)    

    def get_text_size(self, text, font_index):
        return self.draw.textsize(text, font=self.fonts[font_index])

    def update(self):
        """ Generate sub-images for every matrix, update matrix content and trigger matrix updates """
        for display_matrix in self.display_matrices:
            cropped = self.bounding_image.crop(display_matrix.display_box.as_tuple())
            display_matrix.matrix.image = cropped
            display_matrix.matrix.update()