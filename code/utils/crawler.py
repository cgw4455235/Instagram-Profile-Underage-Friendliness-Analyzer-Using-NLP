from itertools import islice
import os
from instaloader import Instaloader, Profile
from pathlib import Path


def download_random_n_posts(top_n: int, profile_name: str, subpath: str) -> None:
    crawler_user_name = os.getenv("instagram_user_name")
    crawler_password = os.getenv("instagram_password")
    L = Instaloader(download_videos=False)
    L.load_session_from_file(
        "acc_test_use", "/Users/chungewang/.config/instaloader/session-acc_test_use"
    )
    profile = Profile.from_username(L.context, profile_name)
    random_posts = profile.get_posts()

    destination_path = Path().absolute() / "code" / subpath / profile_name

    for post in islice(random_posts, top_n):
        L.download_post(post, destination_path)
