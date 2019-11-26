import os
from argparse import ArgumentParser

from apng import APNG
from PIL import Image


def FileSize(file):
    """取得檔案大小"""
    fsize = os.path.getsize(file)
    return fsize

def flat(l):
    for k in l:
        if not isinstance(k, (list, tuple)):
            yield k
        else:
            yield from flat(k)

def gen_frame(path):
    im = Image.open(path)
    alpha = im.getchannel('A')
    # Convert the image into P mode but only use 255 colors in the palette out of 256
    im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
    # Set all pixel values below 128 to 255 , and the rest to 0
    mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
    # Paste the color of index 255 and use alpha as a mask
    im.paste(255, mask)
    # The transparency index is 255
    im.info['transparency'] = 255
    return im

def deapng(apngfile):
    pngs = [] #圖片陣列變數
    apng = APNG.open(apngfile) #開啟 APNG 圖片，用APNG套件開啟
    for i, (png, control) in enumerate(apng.frames):
        if os.path.exists('images'):
            if not os.path.isdir('images'):
                os.mkdir('images')
        else:
            os.mkdir('images')
        png.save(f"images/{i}.png") #保存 png 檔
        if FileSize(f'images/{i}.png') < 1024:
            pngs.append(pngs[-2:])
        else:
            pngs.append(f'images/{i}.png')
    pngs = list(flat(pngs))
    return pngs

def mRGBA(apngfile, output=None):
    pngs = deapng(apngfile)
    img = []
    for image in pngs:
        img.append(gen_frame(image))
    PILimage = img[0]
    if not output:
        output = os.path.splitext(apngfile)[0]
    PILimage.save(f'{output}.gif', save_all=True, append_images=img[0:], loop=0, disposal=2)
    clean(pngs)

def mP(apngfile, output=None):
    pngs = deapng(apngfile)
    img = []
    for image in pngs:
        img.append(Image.open(image).copy())
    PILimage = Image.open(pngs[0])
    if not output:
        output = os.path.splitext(apngfile)[0]
    PILimage.save(f'{os.path.splitext(apngfile)[0]}.gif', save_all=True, append_images=img[0:], loop=0, transparency=0, disposal=2)
    clean(pngs)

def clean(imglist):
    for img in imglist:
        os.remove(img)

def apng2gif(apngfile, output=None):
    try:
        if Image.open(apngfile).mode == 'P':
            mP(apngfile, output)
        if Image.open(apngfile).mode == 'RGBA':
            mRGBA(apngfile, output)
    except Exception as e:
        print(f'Error : {str(e)}')