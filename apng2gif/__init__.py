from argparse import ArgumentParser

import apng2gif.apng2gif


def main():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", help="Input APNG file.", dest='input')
    parser.add_argument("-o", "--output", help="output GIF file", dest="output")
    args = parser.parse_args()
    apng2gif(args.input, args.output)
