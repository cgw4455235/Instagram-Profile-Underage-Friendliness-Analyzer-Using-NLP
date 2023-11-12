from itertools import islice
from math import ceil
import os
from instaloader import Instaloader, Profile
from argparse import ArgumentParser
from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect


def download_top_n_posts(top_n: int, profile_name: str) -> None:
    crawler_user_name = os.getenv('instagram_user_name')
    crawler_password = os.getenv('instagram_password')
    L = Instaloader()
    L.login(crawler_user_name, crawler_password)
    profile = Profile.from_username(L.context, profile_name)
    posts_sorted_by_likes = sorted(
        profile.get_posts(), key=lambda p: p.likes + p.comments, reverse=True
    )

    for post in islice(
        posts_sorted_by_likes, 5
    ):
        L.download_post(post, profile_name)

download_top_n_posts(10, 'name')