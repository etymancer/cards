import pymongo
import os
import Image

db = pymongo.Connection()['livre']
cards = db['cards']
for fn in os.listdir('cards'):
	im = Image.open(os.path.join('cards', fn))
        cards.insert({'type': 'image', 'filename': fn, 'width': im.size[0], 'height': im.size[1]})


