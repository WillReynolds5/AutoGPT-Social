import instaloader
from collections import Counter
from itertools import islice

L = instaloader.Instaloader()

# Define a function to get related hashtags
def get_related_hashtags(hashtags, max_posts=100):
    related_hashtags_counter = Counter()
    for hashtag in hashtags:
        posts = L.get_hashtag_posts(hashtag)
        for post in islice(posts, max_posts):
            for tag in post.caption_hashtags:
                if tag not in hashtags:
                    related_hashtags_counter[tag] += 1
    hashtag_string = ""
    for tag in related_hashtags_counter:
        if related_hashtags_counter[tag] > 3:
            hashtag_string += tag + " "
    return hashtag_string
