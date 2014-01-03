import pymongo
import os
import Image
import sys

base = sys.argv[1]
db = pymongo.Connection()['livre']
db.drop_collection('notebookPages')
notebooks = db['notebookPages']
for nb in os.listdir(base):
    nbPath = os.path.join(base, nb)
    for page, name in enumerate(sorted(os.listdir(nbPath))):
        try:
            im = Image.open(os.path.join(nbPath, name))
        except:
            continue
        dPage = {'type': 'image', 'page': page, 'filename': name, 'notebook': nb, 'width': im.size[0], 'height': im.size[1]}
        notebooks.insert(dPage)

    dPage['lastPage'] = True
    notebooks.update({'_id': dPage['_id']}, dPage)
