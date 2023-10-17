import requests  # pip3 install requests
from pprint import pprint


GET = requests.get
POST = requests.post

# if using Heroku, change this to https://YOURAPP.herokuapp.com
SERVER_URL = 'http://localhost:8000'

def call_api(method, *path_parts, **params) -> dict:
    path_parts = '/'.join(path_parts)
    url = f'{SERVER_URL}/api/{path_parts}/'
    resp = method(url, json=params, headers={'otree-rest-key': REST_KEY})
    print(url)
    if not resp.ok:
        msg = (
            f'Request to "{url}" failed '
            f'with status code {resp.status_code}: {resp.text}'
        )
        raise Exception(msg)
    return resp.json()

data = call_api(GET, 'otree_version')
pprint(data)