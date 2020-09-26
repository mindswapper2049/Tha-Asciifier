from PIL import Image

from Thumbnail import LowerThumbnail

std_len = 63


class ImageOutput:
    ascii_array = list("$@B%8&WM#ZO0QLCJUYXvuxrjft/|()1{}[]?*-_+~<>i!lI;:,^`.")
    ascii_array_length = len(ascii_array)
    unit = (256 + 1) / ascii_array_length

    def __init__(self, image, gray_scale, width, height, width_thumbnail, height_thumbnail):
        self.image = image
        self.gray_scale = gray_scale
        self.width = width
        self.height = height
        self.thumbnail = None
        self.width_thumbnail = width_thumbnail
        self.height_thumbnail = height_thumbnail

    def mapGrayScale(self):
        if self.width < self.height:
            width_out = std_len
            height_out = int(std_len * self.height / self.width)
        else:
            height_out = std_len
            width_out = int(std_len * self.width / self.height)

        scale_2 = max(self.width / width_out, self.height / height_out)
        self.width = int(self.width / scale_2 * 2)
        self.height = int(self.height / scale_2)
        self.gray_scale = self.gray_scale.resize((self.width, self.height), Image.NEAREST)
        self.image = self.image.resize((self.width, self.height), Image.NEAREST)
        self.writeOutputFile()

    def map_char(self, r, g, b, alpha=0):
        if alpha == 256:
            return '.'
        else:
            pos = int((256 - r) / self.unit)
            return self.ascii_array[pos]

    def writeOutputFile(self):
        file = open("TEXT_IMAGE.txt", 'w')
        for i in range(self.height):
            for j in range(self.width):
                char_0 = self.map_char(*self.gray_scale.getpixel((j, i)))
                if char_0 == '.':
                    file.write('.')
                else:
                    char_1 = self.map_char(*self.image.getpixel((j, i)))
                    file.write(char_1)
            file.write('\n')
        file.close()

    def generateThumbnail(self):
        self.thumbnail = LowerThumbnail(self.width_thumbnail, self.height_thumbnail)
