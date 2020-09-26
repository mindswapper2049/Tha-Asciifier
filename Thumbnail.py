import tkinter as tk

from PIL import Image


class UpperThumbnail:
    def __init__(self, image_to_upload, width, height):
        self.image_to_upload = image_to_upload
        self.width = width
        self.height = height
        thumbnail = self.image_to_upload.resize((self.width, self.width), Image.ANTIALIAS)
        thumbnail.save("image_to_upload_thumbnail.gif", "gif")
        self.thumbnail = tk.PhotoImage(file="image_to_upload_thumbnail.gif")
        print(self.thumbnail)


class LowerThumbnail:
    def __init__(self, width, height):
        self.output_image = Image.open("TEXT_IMAGE.jpg")
        self.width = width
        self.height = height
        thumbnail = self.output_image.resize((self.width, self.height), Image.ANTIALIAS)
        thumbnail.save("TEXT_IMAGE.gif", "gif")
        self.thumbnail = tk.PhotoImage(file="TEXT_IMAGE.gif")
        print(self.thumbnail)
