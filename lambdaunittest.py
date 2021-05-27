import requests
import unittest
from prodaptnl import ProdaptNLService
from constant import POSTS_URL, COMMENTS_URL


class ProdaptNLServiceTest(unittest.TestCase):

    def test_external_api_calls(self):
        posts_response = requests.get(POSTS_URL)
        self.assertEqual(200, posts_response.status_code)
        comments_response = requests.get(COMMENTS_URL)
        self.assertEqual(200, comments_response.status_code)

    def test_get_posts(self):
        prodapt_obj = ProdaptNLService.get_data_from_external_api()
        posts = prodapt_obj.get_posts()
        self.assertIsInstance(posts, dict, "Posts should be a dictionary")
        self.assertIsInstance(posts.get("data"), list, "Data should be list of dictionaries")


if __name__ == '__main__':
    ProdaptNLServiceTest.test_get_posts()