from flask import Flask, redirect, url_for, render_template, request, session
from functools import wraps
import os
import random
from datetime import datetime, timedelta
import pytz
app = Flask(__name__)

import pymongo
from bson.objectid import ObjectId

db = pymongo.Connection()['livre']
cardCollection = db['cards']
annotationCollection = db['annotations']
agentCollection = db['agents']
cardIds = [card['_id'] for card in cardCollection.find()]

def ensure_agent(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'agent' not in session:
            session['agent'] = str(agentCollection.insert({'origin': 'web', 'dtCreated': datetime.now(pytz.UTC)}, safe=True))
            session.permanent = True
        return f(*args, **kwargs)
    return decorated_function

def transformCard(card):
    d = dict(card)
    d['_id'] = str(d['_id'])
    d['path'] = url_for('static', filename=os.path.join('cards', d['filename']))
    d['width'] = d['width'] // 2
    d['height'] = d['height'] // 2
    d.setdefault('rotate', 0)
    return d

@app.route('/favicon.ico')
def favicon():
    return redirect('/static/favicon.ico')


@app.route('/')
def index():
    """ This will be deprecated / relocated when there are other features besides "card"."""
    return redirect(url_for('card'))

def randomCard():
    return redirect(url_for('card', cardId=random.choice(cardIds)))

@app.route('/card')
@app.route('/card/<cardId>')
def card(cardId=None):
    if cardId is None:
        return randomCard()
    card = cardCollection.find_one({'_id': ObjectId(cardId)})
    if card['width'] < card['height']:
        orientation = 'vertical'
    else:
        orientation = 'horizontal'
    return render_template('card.html', orientation=orientation, **transformCard(card))


@app.route('/annotate', methods=['POST'])
@ensure_agent
def annotate():
    r = dict(request.form.items())
    if r.get('quality') or r.get('transcription'):
        if r.get('quality') == "null":
            r['quality'] = None
        r['agent'] = session['agent']
        r['dt'] = datetime.now(pytz.UTC)
        annotationCollection.insert(r)
    return randomCard()


if __name__ == '__main__':
    app.secret_key = 'n\xef\xda(\xd86\xd6\x14\xf0F\xc3"g\x96={\xe1\x8e\xd5r\x98\x91\xe2I'
    app.run(host='0.0.0.0', port=8080, debug=False)
