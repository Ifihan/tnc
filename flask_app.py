from threading import Timer
import os
from urllib.parse import urljoin
from PIL import Image, ImageFont, ImageDraw
from flask import Flask, request, url_for, redirect


app = Flask(__name__)
BASE_PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(BASE_PATH, "static")
FONT_PATH = os.path.join(STATIC_PATH, "fonts")
CERTIFICATE_PATH = os.path.join(STATIC_PATH, "certificates")
GENERATED_PATH = os.path.join(STATIC_PATH, "generated")


@app.route("/")
def index():
    return "Hello World"


@app.route("/generate/")
def generate():
    certificate = make_certificate("certificate.png", **request.args)
    return redirect(certificate)


def delete_file(img_title):
    os.unlink(os.path.join(GENERATED_PATH, img_title))


def make_certificate(filename, first_name, last_name):
    # set certificate style
    font = "Coustard-Regular.ttf"

    # name style
    color = "#000000"
    size = 70
    y = 580

    # name text
    text = "{} {}".format(first_name, last_name).upper()
    raw_img = Image.open(os.path.join(CERTIFICATE_PATH, filename))
    img = raw_img.copy()
    draw = ImageDraw.Draw(img)

    # draw name
    PIL_font = ImageFont.truetype(os.path.join(FONT_PATH, font), size)
    w, h = draw.textsize(text, font=PIL_font)
    W, H = img.size
    x = (W - w) / 2
    draw.text((x, y), text, fill=color, font=PIL_font)

    # save certificate
    img_title = "{}-{}.png".format(first_name, last_name)
    img.save(os.path.join(GENERATED_PATH, img_title))
    task = Timer(30, delete_file, (img_title,))
    task.start()
    base_64 =  urljoin(request.host_url, url_for("static", filename="generated/" + img_title))

    return base_64

if __name__ == "__main__":
    app.run(debug=True)