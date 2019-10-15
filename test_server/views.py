import logging
import sys
from random import choice, choices
from string import ascii_letters

import aiohttp
from aiohttp import web
from asyncio import sleep

TOTAL_CHUNK_COUNT = 1000
CHUNK_SIZE_BYTES = 1024
SECONDS_BETWEEN_CHUNKS = 1


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


async def chunked(request):
    response = web.StreamResponse(
        headers={
            'Content-Type': 'text/html'
        }
    )

    await response.prepare(request)
    for _ in range(TOTAL_CHUNK_COUNT):
        await sleep(SECONDS_BETWEEN_CHUNKS)
        await response.write(
            ''.join(choices(ascii_letters, k=CHUNK_SIZE_BYTES)).encode('utf-8')
        )
        await response.write(b'\r\n')
    await response.write_eof()
    return response


def redirect_cycle(request):
    redirect_rules = {
        'a': 'b',
        'b': 'c',
        'c': 'd',
        'd': 'a',
    }
    current_page_id = request.match_info['id']
    status, reason = get_random_redirect()
    return web.Response(
        status=status,
        reason=reason,
        headers={
            'Location': f'/redirect_cycle/{redirect_rules[current_page_id]}'
        }
    )
