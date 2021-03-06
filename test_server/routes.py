from aiohttp import web

from test_server.views import (
    bad_size,
    chunked,
    index,
    redirect_infinite,
    redirect_multi,
    redirect_single,
    redirect_cycle,
    target_page,
)


def setup_routes(app):
    app.add_routes([
        web.get('/', index),
        web.get('/good_one', target_page),
        web.get('/redirect_single', redirect_single),
        web.get('/redirect_multi/{retries}', redirect_multi, name='redirect_multi'),
        web.get('/redirect_infinite', redirect_infinite),
        web.get('/redirect_cycle/{id}', redirect_cycle, name='redirect_cycle'),
        web.get('/bad_size', bad_size),
        web.get('/chunked', chunked),
    ])
