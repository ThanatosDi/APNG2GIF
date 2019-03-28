from apng import APNG

FILE = 'example/example.png'

apng = APNG.open(FILE)
apng.num_plays = 0
apng.save('1.png')