
from datetime import datetime, timezone
from typing import List

from fastapi_rss import RSSFeed, Item, Enclosure, EnclosureAttrs

from app.models.schemas.instagram import Story, Post
from app.plugins.instagram.stories import (fetch_count_stories,
                                       fetch_one_story_by_index, fetch_stories)

from requests import get


def stories_to_rss(stories: list[Story]):
    pass

def posts_to_rss(posts: list[Post], username: str):
    enclosures = []
    posts = posts[:5]
    for p in posts:
        image_url = p["items"][0]["content_url"]
        headers = dict(get(image_url).headers)
        en = Enclosure(
            content="photo",
            attrs=EnclosureAttrs(url=image_url, 
            length=headers["x-full-image-content-length"],
            type=headers["Content-Type"])
        )
        enclosures.append(en)
    items = [Item(title=f"New post by {username}",
                description=f"this is post",
                enclosure=enclosures[i], 
                pub_date=datetime.fromtimestamp(post["created_at"])
                )
             for i, post in enumerate(posts)]

    feed_data = {
        'title': f"{username}'s posts on Instagram",
        'link': 'example.com',
        'description': ':)',
        'language': 'en-us',
        'last_build_date': datetime.now(),
        'docs': 'http://backend.userland.com/rss',
        # 'category': [Category(
            # content='1765', attrs=CategoryAttrs(domain='Syndic8')
        # )],
        'managing_editor': 'test@userland.com',
        'ttl': 40,
        'item': items
    }
    feed = RSSFeed(**feed_data)
    return feed


    # stories = fetch_stories(username)
    # return stories
