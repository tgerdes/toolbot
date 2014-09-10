import aiohttp.wsgi

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>It works!</h1>"


def factory():
    app.debug = True
    return aiohttp.wsgi.WSGIServerHttpProtocol(app,
                                               debug=True,
                                               readpayload=True)


def start_server(loop):
    f = loop.create_server(factory, '0.0.0.0', '8081')
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    return app
