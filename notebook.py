from flask import Flask, redirect, url_for, render_template, request, session
from functools import wraps
import os
import random
from datetime import datetime, timedelta
import pytz
app = Flask(__name__)

import pymongo

db = pymongo.Connection()['livre']
pageCollection = db['notebookPages']
pageIds = [page['_id'] for page in pageCollection.find()]


def transformCard(card):
    d = dict(card)
    d['_id'] = str(d['_id'])
    d['path'] = url_for('static', filename=os.path.join('notebooks', d['notebook'], d['filename']))
    d['width'] = d['width'] // 2
    d['height'] = d['height'] // 2
    d['notebook'] = d['notebook'].lstrip('N')
    if d['page'] > 1:
        d['lastPageNumber'] = d['page'] - 1
    else:
        d['lastPageNumber'] = None
    if not d.get('lastPage'):
        d['nextPageNumber'] = d['page'] + 1
    else:
        d['nextPageNumber'] = None
    return d


@app.route('/favicon.ico')
def favicon():
    return redirect('/static/favicon.ico')


@app.route('/')
def index():
    """ This will be deprecated / relocated when there are other features besides "card". Hahaha."""
    return redirect(url_for('notebook'))


@app.route('/notebook')
@app.route('/notebook/<notebook>/<page>')
def notebook(notebook=None, page=None):
    if page is None:
        return redirect(url_for('notebook', notebook=1, page=1))
#    import IPython; IPython.embed()
    page = pageCollection.find_one({'notebook': 'N{}'.format(notebook),
            'page': int(page)})
    return render_template('notebook.html', **transformCard(page))


if __name__ == '__main__':
    app.secret_key = 'n\xef\xda(\xd86\xd6\x14\xf0F\xc3"g\x96={\xe1\x8e\xd5r\x98\x91\xe2I'
    app.debug = True
    app.run(host='0.0.0.0', port=8081)
