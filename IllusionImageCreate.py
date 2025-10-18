from PIL import Image, ImageEnhance
import numpy as np


def illusion_image_create(image_path):
    img = _create_4K(image_path)
    strip = _create_strip(img.size[0], img.size[1])
    canvas = Image.new("RGB", img.size, "white")
    for i in [strip, img]:
        canvas.paste(i, (0, 0), i)
    return canvas

def _change_alpha( img):
    datas = img.getdata()
    new_data = []
    for item in datas:
        new_data.append((127, 127, 127, 255-(item[0]+item[1]+item[2])//3))
    img.putdata(new_data)
    return img

def _create_4K( path):
    img = Image.open(path).convert('L').convert("RGBA")
    width, height = img.size
    new_width = 4000
    new_height = int((new_width/ width) * height)
    img = img.resize((new_width, new_height))
    img = _change_alpha(ImageEnhance.Brightness(img).enhance(1.0))
    return img

def _create_strip(sizeX, sizeY):
    nd = np.zeros((sizeY, sizeX, 4)).astype('uint8')
    nd[0:sizeY, 0:sizeX, 3] = 255
    for i in range(sizeY):
        nd[i, 0:sizeX, 0:3] = 0 if i % 2 != 0 else 255
    img = Image.fromarray(nd)
    return img
