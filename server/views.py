import logging
import sys
from random import choice

import aiohttp
from aiohttp import web


def get_random_redirect():
    code = (301, 302)
    reason = (
        'Sorry Mario but your princess is in another castle',
        'Mister can\'t you see we\'re having a dinner?',
        'Your call is very important to us',
    )
    return choice(code), choice(reason)


async def index(request):
    # add template with all possible urls
    python_version = f'{sys.version_info.major}.' \
                     f'{sys.version_info.minor}.' \
                     f'{sys.version_info.micro}'
    return web.Response(
        text=f'Simple HTTP server, '
             f'Python/{python_version}, '
             f'aiohttp/{aiohttp.__version__}'
    )


async def target_page(request):
    return web.Response(
        text='Well yes, that is just a page. Finally.'
    )


async def redirect_single(request):
    logging.info('')
    status, reason = get_random_redirect()
    return web.Response(
        status=status,
        reason=reason,
        headers={
            'Location': '/good_one'
        }
    )


async def redirect_multi(request):
    retries = max(
        int(request.match_info['retries']) - 1,
        1
    )
    status, reason = get_random_redirect()
    return web.Response(
        status=status,
        reason=reason,
        headers={
            'Location': f'/redirect_multi/{retries}' if retries > 1 else '/redirect_single'
        }
    )


async def redirect_infinite(request):
    status, reason = get_random_redirect()
    return web.Response(
        status=status,
        reason=reason,
        headers={
            'Location': '/redirect_infinite'
        }
    )


async def bad_size(request):
    return web.Response(
        headers={
            'Content-Length': '42'
        },
        text='Your browser think it is 42 bytes length. But it is not.'
    )
