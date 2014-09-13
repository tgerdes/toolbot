import re
import json
import asyncio
import random
import aiohttp


GOOGLE_IMAGE_API = 'http://ajax.googleapis.com/ajax/services/search/images'


def plugin(bot):
    @bot.respond(re.compile(r'(image|img)( me)? (.*)', re.I))
    def image_me(msg):
        asyncio.Task(imageMe(msg, msg.match.group(3), cb=msg.reply))


@asyncio.coroutine
def imageMe(msg, query, animated=False, faces=False, cb=None):
    q = {'v': '1.0', 'rsz': '8', 'q': query, 'safe': 'active'}
    if animated:
        q['imgtype'] = 'animated'
    elif faces:
        q['imgtype'] = 'face'
    resp = yield from aiohttp.request("get", GOOGLE_IMAGE_API, params=q)
    data = yield from resp.read()

    images = json.loads(data.decode('utf8'))['responseData']['results']
    if images:
        img = random.choice(images)
        cb(ensureImageExtension(img['unescapedUrl']))


def ensureImageExtension(url):
    ext = url.rsplit('.', 1)[1]
    if ext.lower() in ('png', 'jpeg', 'jpg', 'gif'):
        return url
    else:
        return url + ".png"
