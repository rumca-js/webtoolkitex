"""
Set of manual, real world tests
"""
import requests

from webtoolkit import PageRequestObject
import webtoolkit

from webtoolkitex import (
   UrlEx,
)
from webtoolkitex.webconfig import WebConfig


def print_bar():
    print("------------------------")


def is_true(text, condition):
    #if condition:
    #    print(f[{text}] OK")
    if not condition:
        print(f"Error: {text}")


def run_with_base_url(test_url, request=None, crawler_name=None, handler_name=None):

    if handler_name or crawler_name:
        print("ddjjdjd")
        request=PageRequestObject(test_url)

    if handler_name:
        request.handler_name = handler_name
    if crawler_name:
        request.crawler_name = crawler_name

    print("Running {} with UrlEx / request:{}".format(test_url, request))

    url = UrlEx(url=test_url, request=request)
    response = url.get_response()
    handler = url.get_handler()


    #if response is None:
    #    print("Missing response!")
    #    return response, handler

    #if response.is_invalid():
    #    print("Invalid response")
    #    return response, handler

    #if response.is_valid():
    #    print("Response is valid")

    #if response.get_text() is None:
    #    print("No text in response")
    #    return response, handler

    #if handler.get_title() is None:
    #    print("No title in url")
    #    return response, handler

    #if not handler.get_hash():
    #    print("No hash")

    #if not handler.get_body_hash():
    #    print("No body hash")

    #print("Response request: {}".format(response.request))

    print("Title: {}".format(handler.get_title()))

    entries_len = len(list(handler.get_entries()))
    print(f"Entries: {entries_len}")

    streams_len = len(list(handler.get_streams()))
    print(f"Streams: {streams_len}")

    properties = url.get_social_properties()
    #print(f"Social properties: {properties}")

    return response, handler


def test_baseurl__vanilla_google():
    test_url = "https://www.google.com"
    response,handler = run_with_base_url(test_url)

    entries_len = len(list(handler.get_entries()))
    streams_len = len(list(handler.get_streams()))

    is_true("Response is valid", response.is_valid())
    is_true("Title", handler.get_title() == "Google")
    is_true("Streams_len", streams_len == 1)
    is_true("Entries_len", entries_len == 0)

    return response,handler


def test_baseurl__youtube_video():
    test_url = "https://www.youtube.com/watch?v=9yanqmc01ck"
    response, handler = run_with_base_url(test_url)

    entries_len = len(list(handler.get_entries()))
    streams_len = len(list(handler.get_streams()))

    is_true("Response is valid", response.is_valid())
    is_true("Title", handler.get_title() == "The ULTIMATE 16-Player Gaming Setup is COMPLETE!")
    is_true("Streams_len", streams_len == 2)
    is_true("Entries_len", entries_len == 0)


def test_baseurl__youtube_channel__name():
    test_url = "https://www.youtube.com/@LinusTechTips"
    response, handler = run_with_base_url(test_url)

    entries_len = len(list(handler.get_entries()))
    streams_len = len(list(handler.get_streams()))

    is_true("Response is valid", response.is_valid())
    is_true("Title", handler.get_title() == "Linus Tech Tips")
    is_true("Streams_len", streams_len == 1)
    is_true("Entries_len", entries_len == 0)
    is_true("Feeds_len", len(handler.get_feeds()) == 1)

    #response, handler = run_with_base_url(test_url, handler_name="HttpPageHandler")

    #entries_len = len(list(handler.get_entries()))
    #streams_len = len(list(handler.get_streams()))

    #is_true("Response is valid", response.is_valid())
    #is_true("Title", handler.get_title() == "Linus Tech Tips")
    #is_true("Streams_len", streams_len == 1)
    #is_true("Entries_len", entries_len == 0)

    #response, handler = run_with_base_url(test_url, crawler_name="RequestsCrawler")

    #entries_len = len(list(handler.get_entries()))
    #streams_len = len(list(handler.get_streams()))

    #is_true("Response is valid", response.is_valid())
    #is_true("Title", handler.get_title() == "Linus Tech Tips")
    #is_true("Streams_len", streams_len == 1)
    #is_true("Entries_len", entries_len == 0)

    #response, handler = run_with_base_url(test_url, crawler_name="CurlCffiCrawler")

    #entries_len = len(list(handler.get_entries()))
    #streams_len = len(list(handler.get_streams()))

    #is_true("Response is valid", response.is_valid())
    #is_true("Title", handler.get_title() == "Linus Tech Tips")
    #is_true("Streams_len", streams_len == 1)
    #is_true("Entries_len", entries_len == 0)


def test_baseurl__odysee_channel():
    test_url = "https://odysee.com/$/rss/@BrodieRobertson:5"
    response, handler = run_with_base_url(test_url)


def test_baseurl__odysee_video():
    test_url = "https://odysee.com/servo-browser-finally-hits-a-major:24fc604b8d282b226091928dda97eb0099ab2f05"
    return run_with_base_url(test_url)


def test_baseurl__github():
    test_url = "https://github.com/rumca-js/crawler-buddy"
    return run_with_base_url(test_url)


def test_baseurl__reddit__channel():
    test_url = "https://www.reddit.com/r/wizardposting"
    return run_with_base_url(test_url)


def test_baseurl__reddit__news():
    test_url = "https://www.reddit.com/r/wizardposting/comments/1olomjs/screw_human_skeletons_im_gonna_get_more_creative/"
    return run_with_base_url(test_url)

def test_crawler(test_link, crawler_name=None):
    request = UrlEx(test_link).get_request_for_url(test_link)
    request.crawler_name = crawler_name
    return run_with_base_url(test_link, request=request)


def test_baseurl__is_allowed():
    test_url = "https://www.youtube.com/watch?v=Vzgimftolys&pp=ygUPbGludXMgdGVjaCB0aXBz"

    print("Running RemoteUrl test {} with handler".format(test_url))

    url = UrlEx(url=test_url)
    print("Robots allowed? {}".format(url.is_allowed()))


def main():
    WebConfig.use_print_logging()
    webtoolkit.WebConfig.use_print_logging()

    test_baseurl__vanilla_google()
    print_bar()
    test_baseurl__youtube_video()
    print_bar()
    test_baseurl__youtube_channel__name()
    print_bar()
    test_baseurl__odysee_video()
    print_bar()
    test_baseurl__odysee_channel()
    print_bar()
    test_baseurl__github()
    print_bar()
    test_baseurl__reddit__channel()
    print_bar()
    test_baseurl__reddit__news()
    print_bar()
    test_baseurl__is_allowed()
    print_bar()

    test_crawler("https://google.com", "RequestsCrawler")
    print_bar()
    test_crawler("https://google.com", "HttpxCrawler")
    print_bar()
    test_crawler("https://google.com", "StealthRequestsCrawler")
    print_bar()


main()
