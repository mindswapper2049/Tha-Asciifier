# coding=utf-8

import os
import threading
import time
import tkinter as tk
import tkinter.filedialog

import pdfkit

from ImageInput import ImageInput
from ImageOutput import ImageOutput


class GraphicalUI:
    _instance_lock = threading.Lock()

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            with GraphicalUI._instance_lock:
                if not hasattr(cls, "_instance"):
                    GraphicalUI._instance = object.__new__(cls)

        return GraphicalUI._instance

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tha Asciifier")
        self.window.geometry("960x540")
        self.window.resizable(0, 0)
        self.var_status = tk.StringVar()

        self.canvas_up = tk.Canvas(self.window, width=600, height=270)
        self.canvas_up.grid(row=0, column=0, columnspan=7)
        self.canvas_up.create_rectangle(4, 4, 596, 266, outline="grey")

        self.button_select_image_path = tk.Button(self.window, text="Choose path...", width=15, height=1,
                                                  command=self.selectImage)
        self.button_select_image_path.grid(row=0, column=7, sticky=tk.SW, padx=40, pady=4)

        self.canvas_down = tk.Canvas(self.window, width=600, height=270)
        self.canvas_down.grid(row=1, column=0, columnspan=7)
        self.canvas_down.create_rectangle(4, 4, 596, 266, outline="grey")

        self.canvas_progress = tk.Canvas(self.window, width=250, height=25, bg="white")
        self.canvas_progress.grid(row=1, column=7, columnspan=2, padx=40, pady=4, sticky=tk.N)
        self.progress_bar_blank_background = self.canvas_progress.create_rectangle(0, 0, 250, 25, fill="white")

        self.completion_status = tk.Label(self.window, textvariable=self.var_status, width=15, height=1)
        self.completion_status.grid(row=0, column=8, pady=4, sticky=tk.SW)

    def selectImage(self):
        image_path = tk.filedialog.askopenfilename()
        process(image_path)

    def showUpperThumbnail(self, thumbnail):
        graphical_ui.canvas_up.create_image(300, 135, image=thumbnail)
        graphical_ui.window.update()

    def showLowerThumbnail(self, thumbnail):
        graphical_ui.canvas_down.create_image(300, 135, image=thumbnail)
        graphical_ui.window.update()

    def writeAsciiArtImage(self):
        path_wk = r"wkhtmltox\bin\wkhtmltoimage.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wk)
        options = {
            "disable-smart-width": ""
        }
        ascii_text = "TEXT_IMAGE.txt"
        filename = os.path.splitext(ascii_text)[0]
        pdfkit.from_file(ascii_text, filename + ".jpg", configuration=config, options=options)
        os.remove("score_map.jpg")
        os.remove("image_to_upload_thumbnail.gif")
        os.remove("TEXT_IMAGE.txt")
        graphical_ui.var_status.set("Done.")

    def loop(self):
        self.window.mainloop()


graphical_ui = GraphicalUI()


class ProgressBar:  # 进度条
    def __init__(self):
        self.x = 100
        self.the_rec = graphical_ui.canvas_progress.create_rectangle(1.5, 1.5, 0, 20, width=0, fill="white")
        n = 250 / self.x
        for t in range(int(self.x) + 1):
            n = n + 250 / self.x
            graphical_ui.canvas_progress.coords(self.the_rec, (0, 0, n, 25))
            graphical_ui.window.update()
            time.sleep(0)

    def writeBar(self, time_estimated):
        the_rec = graphical_ui.canvas_progress.create_rectangle(1.5, 1.5, 0, 20, fill="green")
        n = 250 / self.x
        for i in range(int(self.x) + 1):
            n = n + 250 / self.x
            graphical_ui.canvas_progress.coords(the_rec, (0, 0, n, 25))
            graphical_ui.window.update()
            time.sleep(0.02)


def process(image_path):
    graphical_ui.var_status.set("Processing...")
    graphical_ui.window.update()

    progress_bar = ProgressBar()
    image_path = image_path.replace('/', '\\')
    image_input = ImageInput(image_path)

    progress_bar.writeBar(233)
    thumbnail = image_input.generateThumbnail()
    graphical_ui.showUpperThumbnail(thumbnail)
    image_input.encodeImage()
    image_input.request()
    image_input.getGrayscale()
    image_output = ImageOutput(image_input.image_to_upload, image_input.gray_scale,
                               image_input.width, image_input.height,
                               image_input.width_thumbnail, image_input.height_thumbnail)
    image_output.mapGrayScale()
    image_output.writeOutputFile()
    graphical_ui.writeAsciiArtImage()
    thumbnail = image_output.generateThumbnail()
    graphical_ui.showLowerThumbnail(thumbnail)
    os.remove("TEXT_IMAGE.gif")


if __name__ == "__main__":
    graphical_ui.loop()
