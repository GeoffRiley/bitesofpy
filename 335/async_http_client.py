import asyncio
from typing import Iterable, NamedTuple

import aiohttp

HTTP_OK = 200


class Result(NamedTuple):
    status_code: int
    content: int


async def check_return(client_session: aiohttp.ClientSession,
                       url: str) -> Result:
    async with client_session.get(url) as resp:
        if resp.status == HTTP_OK:
            return Result(resp.status, int(await resp.content.read()))
        return Result(resp.status, 0)


async def get_results_from_urls(address: str, port: int,
                                slugs: list) -> Iterable[Result]:
    """Get results from http responses.

    ** NOTE: `address` includes the prefix 'http://', it is not just an address

    Get responses by making requests to urls.
    Construct url like this: {address}:{port}/{slug}, where address and port
    are constant, but slug changes.
    Result.status_code is status code of response.
    Result.content is content of response if status_code is 200, otherwise it
    is 0.
    Results must be ordered according to the order of slugs in list and their
    respective responses. Requests must be sent in a asynchronous way.
    (Cannot be sequential and blocking.)
    """
    task_list = []

    async with aiohttp.ClientSession() as cs:
        task_list.extend(
            check_return(cs, f'{address}:{port}/{slug}') for slug in slugs)

        result = await asyncio.gather(*task_list)
    return result
