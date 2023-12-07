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

        self.negative_sentiment_result_content = ttk.Label(
            root, text="Unknown", font=("Calibri", 30)
        )
        self.negative_sentiment_result_content.grid(row=2, column=1, sticky="w")

        # show Instagram Image
        # Violence
        self.violent_image_label = ttk.Label(
            root,
            text="Violent Instagram Image (empty if nonexistent): ",
            font=("Calibri", 20),
        )
        self.violent_image_label.grid(row=3, column=0, sticky="nw", padx=10, pady=10)
        self.violent_image_panel = ttk.Label(root)
        self.violent_image_panel.grid(row=3, column=1, sticky="w")

        # Education
        self.educational_image_label = ttk.Label(
            root,
            text="Educational Instagram Image (empty if nonexistent): ",
            font=("Calibri", 20),
        )
        self.educational_image_label.grid(
            row=4, column=0, sticky="nw", padx=10, pady=10
        )
        self.educational_image_panel = ttk.Label(root)
        self.educational_image_panel.grid(row=4, column=1, sticky="w")

        # Negative Sentiment
        self.negative_sentiment_image_label = ttk.Label(
            root,
            text="Negative Instagram Image (empty if nonexistent): ",
            font=("Calibri", 20),
        )
        self.negative_sentiment_image_label.grid(
            row=5, column=0, sticky="nw", padx=10, pady=10
        )
        self.negative_sentiment_image_panel = ttk.Label(root)
        self.negative_sentiment_image_panel.grid(row=5, column=1, sticky="w")

        # show Instagram post text
        self.violent_text_label = ttk.Label(
            root,
            text="Sample Violent Instagram Post Text (empty if nonexistent): ",
            font=("Calibri", 30),
        )
        self.violent_text_label.grid(row=6, column=0, sticky="nw", padx=10, pady=0)
        self.violent_text_content = ttk.Label(
            root, font=("Calibri", 25), wraplength=500
        )
        self.violent_text_content.grid(row=6, column=1, sticky="w")

        self.educational_text_label = ttk.Label(
            root,
            text="Sample Educational Instagram Post Text (empty if nonexistent): ",
            font=("Calibri", 30),
        )
        self.educational_text_label.grid(row=7, column=0, sticky="nw", padx=10, pady=0)
        self.educational_text_content = ttk.Label(
            root, font=("Calibri", 25), wraplength=500
        )
        self.educational_text_content.grid(row=7, column=1, sticky="w")

        self.negative_text_label = ttk.Label(
            root,
            text="Sample Negative Sentiment Instagram Post Text (empty if nonexistent): ",
            font=("Calibri", 30),
        )
        self.negative_text_label.grid(row=8, column=0, sticky="nw", padx=10, pady=0)
        self.negative_text_content = ttk.Label(
            root, font=("Calibri", 25), wraplength=500
        )
        self.negative_text_content.grid(row=8, column=1, sticky="w")

    def set_display_content(
        self,
        violent_img_path,
        violent_instagram_post_text,
        educational_img_path,
        educational_instagram_post_text,
        negative_text_post,
        negative_img_post,
        is_violent_topic_in_instagram_post_text,
        is_violent_topic_in_instagram_post_img,
        is_educational_topic_in_instagram_post_text,
        is_educational_topic_in_instagram_post_img,
        is_negative_sentiment_in_text_present,
        is_negative_sentiment_in_img_present,
        instagram_profile_name,
    ):
        self.violent_result_content.config(
            text=f"The Instagram profile {instagram_profile_name} contains violent content"
            if is_violent_topic_in_instagram_post_text
            or is_violent_topic_in_instagram_post_img
            else f"The Instagram profile {instagram_profile_name} does not contain violent content"
        )

        self.educational_result_content.config(
            text=f"The Instagram profile {instagram_profile_name} contains educational content"
            if is_educational_topic_in_instagram_post_text
            or is_educational_topic_in_instagram_post_img
            else f"The Instagram profile {instagram_profile_name} does not contain educational content"
        )
        self.negative_sentiment_result_content.config(
            text=f"The Instagram profile {instagram_profile_name} contains highly negative sentiment content"
            if is_negative_sentiment_in_text_present
            or is_negative_sentiment_in_img_present
            else f"The Instagram profile {instagram_profile_name} does not contain highly negative sentiment content"
        )

        if is_violent_topic_in_instagram_post_img and os.path.exists(violent_img_path):
            img = Image.open(violent_img_path)
            img = img.resize((250, 250), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.violent_image_panel.config(image=img)
            self.violent_image_panel.image = img
        if is_educational_topic_in_instagram_post_img and os.path.exists(
            educational_img_path
        ):
            img = Image.open(educational_img_path)
            img = img.resize((250, 250), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.educational_image_panel.config(image=img)
            self.educational_image_panel.image = img
        print(os.path.exists(negative_img_post))
        if is_negative_sentiment_in_img_present and os.path.exists(negative_img_post):
            img = Image.open(negative_img_post)
            img = img.resize((250, 250), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.negative_sentiment_image_panel.config(image=img)
            self.negative_sentiment_image_panel.image = img
        if is_violent_topic_in_instagram_post_text:
            self.violent_text_content.config(text=violent_instagram_post_text)
        if is_educational_topic_in_instagram_post_text:
            self.educational_text_content.config(text=educational_instagram_post_text)
        if is_negative_sentiment_in_text_present:
            self.negative_text_content.config(text=negative_text_post)


def get_ui(
    violent_img_path,
    violent_instagram_post_text,
    educational_img_path,
    educational_instagram_post_text,
    negative_text_post,
    negative_img_post,
    profile_name,
    is_violent_topic_in_post_text,
    is_violent_topic_in_post_img,
    is_educational_topic_in_post_text,
    is_educational_topic_in_post_img,
    is_negative_sentiment_in_text_present,
    is_negative_sentiment_in_img_present,
) -> None:
    root = tk.Tk()
    front_end = InstagramUnderageFriendlinessCheck(root)
    front_end.set_display_content(
        violent_img_path=violent_img_path,
        violent_instagram_post_text=violent_instagram_post_text,
        educational_img_path=educational_img_path,
        educational_instagram_post_text=educational_instagram_post_text,
        negative_text_post=negative_text_post,
        negative_img_post=negative_img_post,
        is_violent_topic_in_instagram_post_text=is_violent_topic_in_post_text,
        is_violent_topic_in_instagram_post_img=is_violent_topic_in_post_img,
        is_educational_topic_in_instagram_post_text=is_educational_topic_in_post_text,
        is_educational_topic_in_instagram_post_img=is_educational_topic_in_post_img,
        is_negative_sentiment_in_text_present=is_negative_sentiment_in_text_present,
        is_negative_sentiment_in_img_present=is_negative_sentiment_in_img_present,
        instagram_profile_name=profile_name,
    )
    root.mainloop()
