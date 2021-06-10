import datetime
import hashlib
import os
import random
import string
from datetime import datetime
from pprint import pprint

import instagram_private_api
import instagram_web_api
import requests
from instagram_private_api.endpoints import highlights
from instagram_web_api import (Client, ClientCompatPatch, ClientError,
                               ClientLoginError)
from app.plugins.instagram.instagram_client import api
from app.plugins.instagram.parser import (fetch_one_story_by_index, fetch_stories,
                                      fetch_stories_count, pk_to_username,
                                      username_to_pk)

PASS = os.environ['PASS']
LOGIN = os.environ['LOGIN']



# web_api = MyClient(username=LOGIN, password=PASS)
# login = web_api.login()


# searching_username = 'iammargosq'
# search_results = api.search_users(searching_username)
# search_id = search_results['users'][0]['pk']
# pprint(search_id)

# user_pk = username_to_pk(api, 'iammargosq')
# all_highlights = api.highlights_user_feed(user_pk)
# highlight_reels = web_api.highlight_reel_media(user_pk)

# highlight_id = all_highlights['tray'][0]['id'].split(':')[1]
# highlight_reel_media = api.highlight_reel_media([highlight_id])

# print(all_highlights)
# pprint(highlight_reel_media)
