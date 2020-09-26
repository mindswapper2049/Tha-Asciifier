import base64
import json
import urllib.parse
import urllib.request

import cv2
import numpy as np
from PIL import Image

from Thumbnail import UpperThumbnail


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
        self.thumbnail = UpperThumbnail(self.image_to_upload, self.width_thumbnail, self.height_thumbnail)

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
