import base64
import json
import urllib.parse
import urllib.request

import cv2
import numpy as np
from PIL import Image

from Thumbnail import LowerThumbnail
from Thumbnail import UpperThumbnail

std_len = 63


class ImageInput:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image_to_upload = Image.open(image_path)
        self.width = None
        self.height = None
        self.image_to_upload_base64 = None
        self.score_map = None
        self.gray_scale = None
        self.thumbnail = None
        self.width_thumbnail = None
        self.height_thumbnail = None

    def generateThumbnail(self):
        self.width = self.image_to_upload.size[0]
        self.height = self.image_to_upload.size[1]
        scale_width = self.width / 590
        scale_height = self.height / 260
        if scale_width > scale_height:
            scale_mode = 1
        else:
            scale_mode = 2

        if scale_mode == 1:
            self.width_thumbnail = 590
            self.height_thumbnail = int(self.height * 590 / self.width)
        else:
            self.height_thumbnail = 260
            self.width_thumbnail = int(self.width * 260 / self.height)
        self.thumbnail = UpperThumbnail(self.image_to_upload, self.width_thumbnail, self.height_thumbnail).thumbnail
        return self.thumbnail

    def encodeImage(self):
        image_to_upload_binary = open(self.image_path, "rb")
        self.image_to_upload_base64 = base64.b64encode(image_to_upload_binary.read())

    def request(self):
        params = {"image": self.image_to_upload_base64}
        params = urllib.parse.urlencode(params).encode(encoding="UTF8")

        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_seg"
        access_token = ""
        request_url = request_url + "?access_token=" + access_token

        request = urllib.request.Request(url=request_url, data=params)
        request.add_header("Content-Type", "application/x-www-form-urlencoded")
        response = urllib.request.urlopen(request)
        content = response.read()
        if content:
            print(content)

        content = json.loads(content)  # content为通过接口获取的返回json
        self.score_map = base64.b64decode(content["scoremap"])
        print(self.score_map)

    def getGrayscale(self):
        nparr = np.frombuffer(self.score_map, np.uint8)
        labelimg = cv2.imdecode(nparr, 1)
        labelimg = cv2.resize(labelimg, (self.width, self.height), interpolation=cv2.INTER_NEAREST)
        im_new = np.where(labelimg == 1, 255, labelimg)
        cv2.imwrite("score_map.jpg", im_new)
        self.gray_scale = Image.open("score_map.jpg")


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
        self.thumbnail = LowerThumbnail(self.width_thumbnail, self.height_thumbnail).thumbnail
        return self.thumbnail
