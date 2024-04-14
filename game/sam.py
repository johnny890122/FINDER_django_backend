import json, os
from io import BytesIO
# from FINDER import FINDER
import networkx as nx
import requests
import game.util as util
from typing import Type

BASE_URL = "https://finder-django-backend-6331eb96b282.herokuapp.com/"

def lambda_handler(event, context): 
    network_id = event["network_id"]
    response = requests.get(
        url = BASE_URL + 'graphs/', 
        params = {'chosen_network_id': network_id}
    )

    G = util.parse_network(eval(response.text))

    # dqn = FINDER()
    # val, sol = dqn.Evaluate(content, model)
    sol = None

    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "predicted_label": sol,
            }
        )
    }
