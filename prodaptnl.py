"""
Project: ProdaptNLService
Author: Abishek KJ
Date: 25-May-2021
"""

from multiprocessing.dummy import Pool
import concurrent.futures
import pymongo
import requests
import ssl

import constant


def update_data(mongo_uri, users, posts, comments):
    db_client = pymongo.MongoClient(mongo_uri, ssl_cert_reqs=ssl.CERT_NONE)
    db = db_client.userFeeds
    for user_detail in sorted(users):
        key = {'userId': user_detail}
        data = {"$set": {'userId': user_detail,
                         'postIds': users[user_detail]['postIds']}}
        db.users.update_one(key, data, upsert=True)

    for post_detail in sorted(posts):
        key = {"postId": post_detail}
        data = {"$set": {"postId": post_detail,
                         "title": posts[post_detail]["title"],
                         "body": posts[post_detail]["body"],
                         "userId": posts[post_detail]["userId"],
                         "comments": posts[post_detail]["comments"]}}
        db.posts.update_one(key, data, upsert=True)

    for comment_detail in sorted(comments):
        key = {"commentId": post_detail}
        data = {"$set": {"commentId": comment_detail,
                         "name": comments[comment_detail]["name"],
                         "email": comments[comment_detail]["email"],
                         "body": comments[comment_detail]["body"],
                         }}
        db.comments.update_one(key, data, upsert=True)


def on_success():
    print(" DB update completed")


def on_failure():
    print(" Error while updating DB ")


class ProdaptNLService:

    def __init__(self, posts_data, comments_data):

        self.db_client = None
        self.db = None
        self.posts_data = posts_data
        self.comments_data = comments_data
        self.posts = {}
        self.users = {}
        self.comments = {}
        self.process_data_from_api()
        self.upload_data_to_db()

    @classmethod
    def get_data_from_external_api(cls):
        posts_response = requests.get(constant.POSTS_URL)
        if posts_response.status_code == 200:
            posts_response = posts_response.json()
        comments_response = requests.get(constant.COMMENTS_URL)
        if comments_response.status_code == 200:
            comments_response = comments_response.json()
        return cls(posts_response, comments_response)

    def process_data_from_api(self):
        for i in self.posts_data:
            user_id = i.get("userId")
            post_id = i.get("id")
            if user_id not in self.users:
                self.users[user_id] = {"userId": user_id,
                                       "postIds": []}
            if post_id not in self.posts:
                self.posts[post_id] = {"postId": post_id,
                                       "userId": user_id,
                                       "title": i.get("title"),
                                       "body": i.get("body"),
                                       "comments": []
                                       }
            if post_id not in self.users[user_id]["postIds"]:
                self.users[user_id]["postIds"].append(post_id)

        for i in self.comments_data:
            post_id = i.get("postId")
            comment_id = i.get("id")
            comment_detail = {"commentId": comment_id,
                              "name": i.get("name"),
                              "email": i.get("email"),
                              "body": i.get("body"),
                              "postId": post_id}
            if comment_id not in self.comments:
                self.comments[comment_id] = comment_detail
            if post_id in self.posts:
                if comment_id not in self.posts[post_id]["comments"]:
                    self.posts[post_id]["comments"].append(comment_detail)

    def get_posts(self):
        response = {"data": list(self.posts.values())}
        return response

    '''def get_post_by_id(self, post_id):
        response = {"data": self.posts[post_id]}
        return response

    def get_comment_by_id(self, comment_id):
        response = {"data": self.comments[comment_id]}
        return response'''

    def get_post_comment_by_id(self, id_field, value):
        response = {}
        if id_field == "post":
            response = {"data": self.posts[value]}
        elif id_field == "comment":
            response = {"data": self.comments[value]}
        return response

    @staticmethod
    def get_mongo_db_client(self):
        self.db_client = pymongo.MongoClient(
            f"mongodb+srv://{constant.DB_USER}:{constant.DB_PASSWORD}@userfeeds.48fue.mongodb.net/admin",
            ssl_cert_reqs=ssl.CERT_NONE)
        self.db = self.db_client.userFeeds
        return self.db_client, self.db

    def upload_data_to_db(self):
        mongo_uri = f"mongodb+srv://{constant.DB_USER}:{constant.DB_PASSWORD}@userfeeds.48fue.mongodb.net/admin"
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(update_data, mongo_uri, self.users, self.posts, self.comments)


prodapt_obj = ProdaptNLService.get_data_from_external_api()
