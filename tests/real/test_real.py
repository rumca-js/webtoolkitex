"""
Set of manual, real world tests
"""
import requests
import unittest

from webtoolkit import PageRequestObject
import webtoolkit

from webtoolkitex import (
   UrlEx,
)
from webtoolkitex.webconfig import WebConfig


class TestBaseUrl(unittest.TestCase):

    def setUp(self):
        WebConfig.use_print_logging()
        webtoolkit.WebConfig.use_print_logging()

    def run_with_base_url(self, test_url, request=None, crawler_name=None, handler_name=None):
        if handler_name or crawler_name:
            request=PageRequestObject(test_url)

        if handler_name:
            request.handler_name = handler_name
        if crawler_name:
            request.crawler_name = crawler_name

        print("Running {} with UrlEx / request:{}".format(test_url, request))

        url = UrlEx(url=test_url, request=request)
        response = url.get_response()
        handler = url.get_handler()

        self.assertTrue(handler.get_title())
        self.assertTrue(handler.get_hash())
        self.assertTrue(handler.get_body_hash())

        self.assertTrue(response is not None)
        self.assertTrue(response.is_valid())
        self.assertTrue(response.get_text())
        self.assertTrue(response.get_hash())
        self.assertTrue(response.get_body_hash())

        return response, handler, url

    def test_baseurl__vanilla_google(self):
        test_url = "https://www.google.com"
        response, handler, url = self.run_with_base_url(test_url)

        self.assertEqual(handler.__class__.__name__, "HttpPageHandler")
        self.assertEqual(response.request.crawler_type.__class__.__name__, "CurlCffiCrawler")

        entries_len = len(list(handler.get_entries()))
        streams_len = len(list(handler.get_streams()))

        self.assertTrue(response.is_valid())
        self.assertTrue(handler.get_title() == "Google")
        self.assertTrue(streams_len == 1)
        self.assertTrue(entries_len == 0)

    def test_baseurl__youtube_video(self):
        test_url = "https://www.youtube.com/watch?v=9yanqmc01ck"
        response, handler, url = self.run_with_base_url(test_url)

        self.assertEqual(handler.__class__.__name__, "YouTubeVideoHandlerJson")
        self.assertEqual(response.request.crawler_type.__class__.__name__, "RequestsCrawler")

        entries_len = len(list(handler.get_entries()))
        streams_len = len(list(handler.get_streams()))

        self.assertTrue(response.is_valid())
        self.assertTrue(handler.get_title() == "The ULTIMATE 16-Player Gaming Setup is COMPLETE!")
        self.assertTrue(streams_len == 1)
        self.assertTrue(entries_len == 0)

    def test_baseurl__youtube_channel__id(self):
        test_url = "https://www.youtube.com/channel/UCXuqSBlHAE6Xw-yeJA0Tunw"
        response, handler, url = self.run_with_base_url(test_url)

        self.assertEqual(handler.__class__.__name__, "YouTubeChannelHandlerJson")
        self.assertEqual(response.request.crawler_type.__class__.__name__, "RequestsCrawler")

        entries_len = len(list(handler.get_entries()))
        streams_len = len(list(handler.get_streams()))
        self.assertTrue(handler.get_title() == "Linus Tech Tips")
        self.assertTrue(streams_len == 2)
        self.assertTrue(entries_len > 0)
        self.assertTrue(len(handler.get_feeds()) == 1)

        self.assertTrue(response.is_valid())

    def test_baseurl__youtube_channel__name(self):
        test_url = "https://www.youtube.com/@LinusTechTips"
        response, handler, url = self.run_with_base_url(test_url)

        self.assertEqual(handler.__class__.__name__, "YouTubeChannelHandlerJson")
        self.assertEqual(response.request.crawler_type.__class__.__name__, "RequestsCrawler")

        entries_len = len(list(handler.get_entries()))
        streams_len = len(list(handler.get_streams()))
        self.assertTrue(handler.get_title() == "Linus Tech Tips")
        self.assertTrue(streams_len == 2)
        self.assertTrue(entries_len > 0)
        self.assertTrue(len(handler.get_feeds()) == 1)

        self.assertTrue(response.is_valid())

    def test_baseurl__youtube_channel__name__requests(self):
        test_url = "https://www.youtube.com/@LinusTechTips"
        request = PageRequestObject(test_url)
        request.crawler_name="RequestsCrawler"

        response, handler, url = self.run_with_base_url(test_url, request=request)

        self.assertEqual(handler.__class__.__name__, "YouTubeChannelHandlerJson")
        self.assertEqual(response.request.crawler_type.__class__.__name__, "RequestsCrawler")

        entries_len = len(list(handler.get_entries()))
        streams_len = len(list(handler.get_streams()))
        self.assertEqual(handler.get_title(), "Linus Tech Tips")
        self.assertEqual(streams_len, 2)
        self.assertTrue(entries_len > 0)
        self.assertTrue(len(handler.get_feeds()) == 1)

        self.assertTrue(response.is_valid())

    #def test_baseurl__youtube_channel__name__curl(self):
    #    test_url = "https://www.youtube.com/@LinusTechTips"
    #    request = PageRequestObject(test_url)
    #    request.crawler_name="CurlCffiCrawler"
    #    request.settings={"impersonate" : "firefox"}

    #    response, handler, url = self.run_with_base_url(test_url, request=request)

    #    self.assertEqual(handler.__class__.__name__, "YouTubeChannelHandlerJson")
    #    self.assertEqual(response.request.crawler_type.__class__.__name__, "CurlCffiCrawler")

    #    entries_len = len(list(handler.get_entries()))
    #    streams_len = len(list(handler.get_streams()))
    #    self.assertEqual(handler.get_title(), "Linus Tech Tips")
    #    self.assertEqual(streams_len, 2)
    #    self.assertTrue(entries_len > 0)
    #    self.assertTrue(len(handler.get_feeds()) == 1)

    #    self.assertTrue(response.is_valid())

    def test_baseurl__odysee_channel(self):
        test_url = "https://odysee.com/$/rss/@BrodieRobertson:5"
        response, handler, url = self.run_with_base_url(test_url)

        self.assertEqual(handler.__class__.__name__, "OdyseeChannelHandler")
        self.assertEqual(response.request.crawler_type.__class__.__name__, "CurlCffiCrawler")

        entries_len = len(list(handler.get_entries()))
        streams_len = len(list(handler.get_streams()))
        self.assertTrue(streams_len == 2)
        self.assertTrue(entries_len > 0)

    def test_baseurl__odysee_video(self):
        test_url = "https://odysee.com/servo-browser-finally-hits-a-major:24fc604b8d282b226091928dda97eb0099ab2f05"
        response, handler, url = self.run_with_base_url(test_url)

        self.assertEqual(handler.__class__.__name__, "OdyseeVideoHandler")
        self.assertEqual(response.request.crawler_type.__class__.__name__, "CurlCffiCrawler")

        entries_len = len(list(handler.get_entries()))
        streams_len = len(list(handler.get_streams()))
        self.assertTrue(streams_len == 1)
        self.assertTrue(entries_len == 0)

    def test_baseurl__github(self):
        test_url = "https://github.com/rumca-js/crawler-buddy"
        response, handler, url = self.run_with_base_url(test_url)

        self.assertEqual(handler.__class__.__name__, "GitHubUrlHandler")
        self.assertEqual(response.request.crawler_type.__class__.__name__, "CurlCffiCrawler")

        entries_len = len(list(handler.get_entries()))
        streams_len = len(list(handler.get_streams()))
        self.assertTrue(streams_len == 1)
        self.assertTrue(entries_len == 0)

    def test_baseurl__reddit__channel(self):
        test_url = "https://www.reddit.com/r/wizardposting"
        response, handler, url = self.run_with_base_url(test_url)

        self.assertEqual(handler.__class__.__name__, "RedditUrlHandler")
        self.assertEqual(response.request.crawler_type.__class__.__name__, "CurlCffiCrawler")

        entries_len = len(list(handler.get_entries()))
        streams_len = len(list(handler.get_streams()))
        self.assertTrue(streams_len == 1)
        self.assertTrue(entries_len == 0)

    def test_baseurl__reddit__news(self):
        test_url = "https://www.reddit.com/r/wizardposting/comments/1olomjs/screw_human_skeletons_im_gonna_get_more_creative/"
        response, handler, url = self.run_with_base_url(test_url)

        self.assertEqual(handler.__class__.__name__, "RedditUrlHandler")
        self.assertEqual(response.request.crawler_type.__class__.__name__, "CurlCffiCrawler")

        entries_len = len(list(handler.get_entries()))
        streams_len = len(list(handler.get_streams()))
        self.assertTrue(streams_len == 1)
        self.assertTrue(entries_len == 0)

    def test_baseurl__social_properties__youtube_channel(self):
        test_url = "https://www.youtube.com/channel/UCXuqSBlHAE6Xw-yeJA0Tunw"

        response, handler, url = self.run_with_base_url(test_url)

        properties = url.get_social_properties()
        self.assertTrue(len(properties) > 0)

    def test_baseurl__social_properties__youtube_video(self):
        test_url = "https://www.youtube.com/watch?v=9yanqmc01ck"

        response, handler, url = self.run_with_base_url(test_url)

        properties = url.get_social_properties()
        self.assertTrue(len(properties) > 0)

    def test_baseurl__social_properties__github(self):
        test_url = "https://github.com/rumca-js/crawler-buddy"

        response, handler, url = self.run_with_base_url(test_url)

        properties = url.get_social_properties()
        self.assertTrue(len(properties) > 0)

    def test_baseurl__social_properties__reddit__channel(self):
        test_url = "https://www.reddit.com/r/wizardposting"

        response, handler, url = self.run_with_base_url(test_url)

        properties = url.get_social_properties()
        self.assertTrue(len(properties) > 0)

    def test_baseurl__social_properties__reddit__post(self):
        test_url = "https://www.reddit.com/r/wizardposting/comments/1olomjs/screw_human_skeletons_im_gonna_get_more_creative/"

        response, handler, url = self.run_with_base_url(test_url)

        properties = url.get_social_properties()
        self.assertTrue(len(properties) > 0)

    def test_baseurl__is_allowed(self):
        test_url = "https://www.youtube.com/watch?v=Vzgimftolys&pp=ygUPbGludXMgdGVjaCB0aXBz"

        print("Running RemoteUrl test {} with handler".format(test_url))

        url = UrlEx(url=test_url)
        self.assertTrue(url.is_allowed())
