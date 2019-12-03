import os
import tempfile
from argparse import ArgumentParser

from apng import APNG
from PIL import Image


class APNG2GIF(object):
    """APNG2GIF  

        Convert APNG to GIF

    Arguments:
        object {[type]} -- [description]
    """
    def __init__(self):
        self.cwd = os.getcwd()
        self.tf = None
    
    def filesize(self, file):
        """filesize
        
        Arguments:
            file {[str]} -- [file path]
        
        Returns:
            [int] -- [file size]
        """        
        fsize = os.path.getsize(file)
        return fsize

    def flat(self, l):
        for k in l:
            if not isinstance(k, (list, tuple)):
                yield k
            else:
                yield from self.flat(k)

    def gen_frame(self, path):
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

    def deapng(self, apngfile):
        pngs = [] #圖片陣列變數
        apng = APNG.open(apngfile) #開啟 APNG 圖片，用APNG套件開啟
        self.tf = tempfile.mkdtemp('_APNG2GIF_images')
        for i, (png, control) in enumerate(apng.frames):
            png.save(f"{self.tf}/{i}.png") #保存 png 檔
            if self.filesize(f'{self.tf}/{i}.png') < 1024:
                pngs.append(pngs[-2:])
            else:
                pngs.append(f'{self.tf}/{i}.png')
        pngs = list(self.flat(pngs))
        return pngs

    def mRGBA(self, apngfile, loop=0, output=None):
        pngs = self.deapng(apngfile)
        img = []
        for image in pngs:
            img.append(self.gen_frame(image))
        PILimage = img[0]
        if not output:
            output = os.path.splitext(apngfile)[0]
        PILimage.save(f'{output}.gif', save_all=True, append_images=img[0:], loop=loop, disposal=2)
        self.clean(pngs)

    def mP(self, apngfile, loop=0, output=None):
        pngs = self.deapng(apngfile)
        img = []
        for image in pngs:
            img.append(Image.open(image).copy())
        PILimage = Image.open(pngs[0])
        output = os.path.abspath(output)
        print(output)
        print(os.path.dirname(output))
        # PILimage.save(f'{os.path.splitext(apngfile)[0]}.gif', save_all=True, append_images=img[0:], loop=loop, transparency=0, disposal=2)
        # self.clean(pngs)

    def clean(self, imglist):
        for img in imglist:
            os.remove(img)

    def apng2gif(self, apngfile, output=None):
        if Image.open(apngfile).mode == 'P':
            self.mP(apngfile, output=output)
        if Image.open(apngfile).mode == 'RGBA':
            self.mRGBA(apngfile, output=output)
            
if __name__=='__main__':
    test = APNG2GIF()
    apngfile = './example/example.png'
    test.apng2gif(apngfile, output='D:/VSCode')
    # absf = 'C:/Users/ThanatosDi/Desktop/Github/APNG2GIF/example/example.png'
    # # print(test.deapng('example/example.png'))
    # print(os.getcwd())
    # print(os.path.join(os.getcwd(), 'example/example.png'))
    # print(os.path.relpath(apngfile))
    # print(os.path.dirname(os.path.abspath(absf)))