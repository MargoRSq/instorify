from plugins.instagram.clients.private_api import private_api


# getting pk(id) of instagram account from username
def username_to_pk(username: str) -> int:
    search_results = private_api.username_info(username)
    return search_results['user']['pk']

# instagram id(pk) to instagram username
def pk_to_username(pk: int) -> str:
    search_results = private_api.user_info(pk)
    return search_results['user']['username']

# fetching "following" accounts
def fetch_following_pk(pk: int) -> list[int]:

    uuid = private_api.generate_uuid()
    results = private_api.user_following(pk, uuid)
    followers = results['users']

    list_acconts_pk = []
    for human in followers:
        list_acconts_pk.append(human['pk'])

    return list_acconts_pk
