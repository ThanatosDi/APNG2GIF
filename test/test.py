import os
import sys
from argparse import ArgumentParser

from apng import APNG

PATH = os.path.abspath(os.path.join(sys.argv[0],os.path.pardir))

def APNGplay(FILE, num:int=0, output=None):
    """set apng play number,0 = loop"""
    try:
        apng = APNG.open(FILE)
        apng.num_plays = 0
        if not output:
            output = os.path.splitext(FILE)[0]
        apng.save(os.path.join(PATH, f'{os.path.basename(output)}_new.png'))
    except Exception as e:
        print(f'Error : {str(e)}')

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", help="Input APNG file.", dest='input')
    parser.add_argument("-n", "--num", help="Play number", dest='num')
    parser.add_argument("-o", "--output", help="output APNG file", dest="output")
    args = parser.parse_args()
    APNGplay(args.input, args.num, args.output)
