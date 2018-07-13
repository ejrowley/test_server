import asyncio
import argparse
import aiohttp

parser = argparse.ArgumentParser(
        description='Script for checking the response from http services')
parser.add_argument('urls', nargs='+', help='the urls to checked')
parser.add_argument('--timeout', default=3000, help='the number of milliseconds to wait for a response')
parser.add_argument('--interval', default=1000, help='the interval between requests')
parser.add_argument('--auth', default=None, help='user:password')

async def check_url_coroutine(session, url, timeout, basic_auth):
    try:
        if basic_auth:
            user, password = basic_auth.split(':', 1)
            auth = aiohttp.BasicAuth(user, password)
        else:
            auth = None

        async with session.get(url, auth=auth) as response:
            print ('url: ' + url + ' ' + str(response.status))
            await response.text()
    except Exception as e:
        print('error:' + str(e))

async def execute_request_batch(loop, urls, timeout, basic_auth):
    timeout = aiohttp.ClientTimeout(timeout)
    async with aiohttp.ClientSession(loop=loop, timeout=timeout) as session:
        tasks = [check_url_coroutine(session, url, timeout, basic_auth) for url in urls]
        await asyncio.gather(*tasks)

async def main_loop(loop, urls, timeout, basic_auth):
    while True:
        await asyncio.sleep(1)
        await execute_request_batch(loop, urls, timeout, basic_auth)

def main():
    args = parser.parse_args()
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    run_main_loop = asyncio.ensure_future(main_loop(loop, args.urls, args.timeout, args.auth))

    loop.run_forever()

main()
