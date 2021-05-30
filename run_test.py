import os

from stories_parser.parser import *


TOKEN = os.environ['ACCESS_TOKEN']
PASS = os.environ['PASS']
LOGIN = os.environ['LOGIN']

me = 14800273205
me_fake = 48100881427
searching_username = 'iammargosq'

api = instagram_private_api.Client(LOGIN, PASS)

following = fetch_following_pk(api, me)

counter = 0
for human in following:
    counter += len(fetch_stories(api, human))
    print(counter)
    