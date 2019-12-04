import os
import shutil
import tempfile
from argparse import ArgumentParser

from apng import APNG
from PIL import Image

__version__ = '1.0.1'

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
        apng = APNG.open(os.path.abspath(apngfile)) #開啟 APNG 圖片，用APNG套件開啟
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
        if output:
            savepath = os.path.abspath(output)
            if not savepath.endswith('.gif'):
                savepath += '.gif'
        else:
            savepath = os.path.join(os.getcwd(), os.path.splitext(os.path.basename(apngfile))[0])
            savepath += '.gif'
        PILimage.save(f'{savepath}', save_all=True, append_images=img[0:], loop=loop, disposal=2)
        self.clean()

    def mP(self, apngfile, loop=0, output=None):
        pngs = self.deapng(apngfile)
        img = []
        for image in pngs:
            img.append(Image.open(image).copy())
        PILimage = Image.open(pngs[0])
        if output:
            savepath = os.path.abspath(output)
            if not savepath.endswith('.gif'):
                savepath += '.gif'
        else:
            savepath = os.path.join(os.getcwd(), os.path.splitext(os.path.basename(apngfile))[0])
            savepath += '.gif'
        PILimage.save(f'{savepath}', save_all=True, append_images=img[0:], loop=loop, transparency=0, disposal=2)
        self.clean()

    def clean(self):
        shutil.rmtree(self.tf)

    def apng2gif(self, apngfile, output=None):
        if Image.open(apngfile).mode == 'P':
            self.mP(apngfile, output=output)
        if Image.open(apngfile).mode == 'RGBA':
            self.mRGBA(apngfile, output=output)

def main():
    apng2gif = APNG2GIF()
    parser = ArgumentParser(prog='apng2gif', description='convert APNG to GIF.')
    parser.add_argument("-i", "--input", help="Input APNG file.", dest='input')
    parser.add_argument("-o", "--output", help="output GIF file", dest="output")
    args = parser.parse_args()
    if args.input:
        apng2gif.apng2gif(args.input, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()