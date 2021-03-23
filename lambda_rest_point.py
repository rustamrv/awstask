import asyncio
from urllib import request
import json
import time
import logging
from urllib.error import URLError
from datetime import timedelta


async def get_urls(url):
    try:
        response = request.urlopen(url)
        start_time = time.monotonic()
        data = response.read()
        end = time.monotonic() - start_time
        response_data = {'website': url,
                         'total second': str(timedelta(seconds=end))}
    except TypeError as error:
        response_data = {
            "message": f"Error type {url} - {error} "
        }
    except URLError:
        response_data = {
            "message": f"URLError type {url}"
        }
    return response_data


async def main(event):
    try:
        data = json.loads(event["body"])
        urls_ = data["urls"]
    except TypeError as error:
        results = {'message': f'Error type urls {error}'}
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(results)
        }
    if isinstance(urls_, list):
        futures = [get_urls(url) for url in urls_]
    elif isinstance(urls_, str):
        futures = [get_urls(urls_)]
    else:
        futures = []
    completed, _ = await asyncio.wait(futures)
    results = [_data.result() for _data in completed]
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(results)
    }


def result_lambda(event, context=None):
    event_loop = asyncio.get_event_loop()
    res = event_loop.run_until_complete(main(event))
    return res
