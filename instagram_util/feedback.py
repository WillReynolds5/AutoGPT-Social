

def get_post_metrics(username, client):

    # Get the user's own posts
    user_id = client.user_id_from_username(username)
    posts = client.user_medias(user_id, amount=100)  # Change 'amount' to get more posts

    # Collect metrics from posts
    metrics = []
    for post in posts:
        metrics.append({
            'id': post.id,
            'shortcode': post.code,
            'likes': post.like_count,
            'comments': post.comment_count,
            'caption': post.caption_text,
        })

    return metrics
