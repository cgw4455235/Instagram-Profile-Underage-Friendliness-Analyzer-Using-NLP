import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os


class InstagramUnderageFriendlinessCheck:
    def __init__(self, root):
        self.root = root
        root.title("Instagram Underage Friendliness Check")

        # Tell user result of analysis
        self.result_label = ttk.Label(root, text="Result: ", font=("Calibri", 30))
        self.result_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.violent_result_content = ttk.Label(
            root, text="Unknown", font=("Calibri", 30)
        )
        self.violent_result_content.grid(row=0, column=1, sticky="w")

        self.educational_result_content = ttk.Label(
            root, text="Unknown", font=("Calibri", 30)
        )
        self.educational_result_content.grid(row=1, column=1, sticky="w")

        # show Instagram Image
        self.image_label = ttk.Label(
            root, text="Instagram Image: ", font=("Calibri", 30)
        )
        self.image_label.grid(row=2, column=0, sticky="nw", padx=10, pady=10)
        self.image_panel = ttk.Label(root)
        self.image_panel.grid(row=2, column=1, sticky="w")

        # show Instagram post text
        self.text_label = ttk.Label(
            root, text="Sample Instagram Post Text: ", font=("Calibri", 30)
        )
        self.text_label.grid(row=3, column=0, sticky="nw", padx=10, pady=0)
        self.text_content = ttk.Label(root, font=("Calibri", 25), wraplength=500)
        self.text_content.grid(row=3, column=1, sticky="w")

    def set_display_content(
        self,
        violent_img_path,
        violent_instagram_post_text,
        educational_img_path,
        educational_instagram_post_text,
        is_violent_topic_in_instagram_post,
        is_educational_topic_in_instagram_post,
        instagram_profile_name,
    ):
        self.violent_result_content.config(
            text=f"The Instagram profile {instagram_profile_name} contains violent content"
            if is_violent_topic_in_instagram_post
            else f"The Instagram profile {instagram_profile_name} does not contain violent content"
        )
        if not is_violent_topic_in_instagram_post:
            self.educational_result_content.config(
                text=f"The Instagram profile {instagram_profile_name} contains educational content"
                if is_educational_topic_in_instagram_post
                else f"The Instagram profile {instagram_profile_name} does not educational violent content"
            )

        if os.path.exists(violent_img_path):
            img = Image.open(violent_img_path)
            img = img.resize((250, 250), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.image_panel.config(image=img)
            self.image_panel.image = img
        else:
            self.image_panel.config(image="")
        if is_violent_topic_in_instagram_post:
            self.text_content.config(text=violent_instagram_post_text)
        elif is_educational_topic_in_instagram_post:
            self.text_content.config(text=educational_instagram_post_text)


def get_ui(
    violent_img_path,
    violent_instagram_post_text,
    educational_img_path,
    educational_instagram_post_text,
    profile_name,
    is_violent_topic_in_instagram_post,
    is_educational_topic_in_instagram_post,
) -> None:
    root = tk.Tk()
    front_end = InstagramUnderageFriendlinessCheck(root)
    front_end.set_display_content(
        violent_img_path=violent_img_path,
        violent_instagram_post_text=violent_instagram_post_text,
        educational_img_path=educational_img_path,
        educational_instagram_post_text=educational_instagram_post_text,
        is_violent_topic_in_instagram_post=is_violent_topic_in_instagram_post,
        is_educational_topic_in_instagram_post=is_educational_topic_in_instagram_post,
        instagram_profile_name=profile_name,
    )
    root.mainloop()
