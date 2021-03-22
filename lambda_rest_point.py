from urllib import request
import asyncio
import json
import time
import logging
from urllib.error import URLError


async def get_urls(events, context):
    data = json.loads(events['body'])
    response_data = []
    try:
        urls_ = data['urls']
    except KeyError:
        logging.error('Error key urls')
        response_data = {'message': 'Error key urls'}
        urls_ = []
    if isinstance(urls_, list):
        for url in urls_:
            try:
                data_url = request.urlopen(url)
                start = time.time()
                page = data_url.read()
                end = time.time()
                data_url.close()
                response_data.append({'website': url,
                                      'total second': end})
            except TypeError:
                response_data.append({
                    "message": f"Error type {url}"
                })
            except URLError:
                response_data.append({
                    "message": f"URLError type {url}"
                })
    elif isinstance(urls_, str):
        try:
            data_url = request.urlopen(urls_)
            start = time.time()
            page = data_url.read()
            end = time.time()
            data_url.close()
            response_data = {'website': urls_,
                             'total second': end}
        except TypeError:
            response_data = {
                "message": f"Error type {urls_}"
            }
        except URLError:
            response_data = {
                "message": f"URLError type {urls_}"
            }

    else:
        response_data = {'message': f"Error type{urls_}"}
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(response_data)
    }


async def async_result_lambda(events, context):
    return await asyncio.create_task(get_urls(events, context))


def result_lambda(event, context=None):
    return asyncio.run(async_result_lambda(event, context))