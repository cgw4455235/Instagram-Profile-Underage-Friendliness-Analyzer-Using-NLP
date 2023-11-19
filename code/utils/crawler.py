from itertools import islice
import os
from instaloader import Instaloader, Profile
from pathlib import Path


def download_top_n_posts(top_n: int, profile_name: str) -> None:
    crawler_user_name = os.getenv("instagram_user_name")
    crawler_password = os.getenv("instagram_password")
    L = Instaloader()
    L.login(crawler_user_name, crawler_password)
    profile = Profile.from_username(L.context, profile_name)
    posts_sorted_by_likes = sorted(
        profile.get_posts(), key=lambda p: p.likes + p.comments, reverse=True
    )
    destination_path = Path().absolute() / "code" / profile_name

    for post in islice(posts_sorted_by_likes, top_n):
        L.download_post(post, destination_path)
