from .models import Note, Post, User
from datetime import datetime

def get_timestamp(post):
    created = post.date
    current  = datetime.now()
    difference = current - created
    days = difference.days
    seconds = difference.seconds

    if days > 0:
        time_ago = f"{days} days ago"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if hours > 0:
            time_ago = f"{hours} hours ago"
        elif minutes > 0:
            time_ago = f"{minutes} minutes ago"
        else:
            time_ago = "just now"

    return time_ago

def get_num_posts(user):
    num_posts = len(user.posts)
    if num_posts == 1:
        return "1 post"
    else:
        return str(num_posts) + ' posts'