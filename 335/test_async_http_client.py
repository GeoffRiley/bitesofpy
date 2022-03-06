import asyncio
from inspect import iscoroutinefunction
from multiprocessing import Process
from asyncio import sleep
from time import sleep as blocking_sleep, time
from random import sample

from aiohttp import web
import pytest

from async_http_client import get_results_from_urls

MAX_SLUG = 99
RESPONSE_DELAY_S = 0.1
ADDRESS = "http://localhost"


@pytest.fixture(scope="module")
def response_map():
    return {key: random_value for key, random_value in enumerate(sample(range(1000), MAX_SLUG + 1))}


def async_http_test_server(port, response_map):
    async def handle(request):
        try:
            slug = int(request.match_info.get('slug'))
        except ValueError:
            return web.HTTPNotFound()

        if 0 <= slug <= MAX_SLUG:
            await sleep(RESPONSE_DELAY_S)
            return web.Response(text=str(response_map[slug]))

        return web.HTTPNotFound()

    app = web.Application()
    app.add_routes([web.get('/{slug}', handle), ])
    web.run_app(app, host="localhost", port=port)


@pytest.fixture(scope="module")
def servers_port(response_map):
    for port in range(49_152, 65_535):
        server_process = Process(target=async_http_test_server, args=(port, response_map))
        server_process.start()
        blocking_sleep(1)  # See if server starts up on requested port.
        if server_process.exitcode is None:
            break
    else:
        raise Exception("Test setup error. Could not start test server.")

    yield port

    server_process.kill()


def test_if_async_function():
    assert iscoroutinefunction(get_results_from_urls), "In this exercise http_client has to be coroutine function!"


def test_simple_responses_unordered(response_map, servers_port):
    """At least correct responses. Order not relevant."""
    slug_list = [0, 10, 99]
    responses = asyncio.run(get_results_from_urls(ADDRESS, servers_port, slug_list))
    for slug, response in zip(slug_list, responses):
        if slug in response_map:
            assert (200, response_map[slug]) in responses
        else:
            assert (404, 0) in responses


def test_simple_responses_ordered(response_map, servers_port):
    """Correct responses in correct order."""
    slug_list = [0, 10, 99]
    responses = asyncio.run(get_results_from_urls(ADDRESS, servers_port, slug_list))
    compare_responses(responses, slug_list, response_map)


def test_out_of_range_responses(response_map, servers_port):
    """Properly handles 404 responses."""
    slug_list = [-1, 100]
    responses = asyncio.run(get_results_from_urls(ADDRESS, servers_port, slug_list))
    compare_responses(responses, slug_list, response_map)


def test_time_for_all_responses(response_map, servers_port):
    """Demonstrates full potential of asynchronous requests."""
    slug_list = list(range(MAX_SLUG + 1))
    start_time = time()
    responses = asyncio.run(get_results_from_urls(ADDRESS, servers_port, slug_list))
    duration = time() - start_time
    compare_responses(responses, slug_list, response_map)
    assert duration < 5 * RESPONSE_DELAY_S


def compare_responses(responses, slug_list, response_map):
    assert len(responses) == len(slug_list)

    for slug, response in zip(slug_list, responses):
        if slug in response_map:
            assert response.status_code == 200
            assert response.content == response_map[slug]
        else:
            assert response.status_code == 404
            assert response.content == 0