import json, os, requests
from io import BytesIO
# from FINDER import FINDER
import networkx as nx
import requests
import game.util as util
from typing import Type

BASE_URL = "https://finder-django-backend-6331eb96b282.herokuapp.com/"

#TODO: load the model and check the content is the same 
def lambda_handler(event, context): 
    body = json.loads(event["body"])
    # body = event["body"]
    network_id = body["network_id"]
    model_name = util.get_network_config(network_id)["name"]

    response = requests.get(
        url = BASE_URL + 'graphs/', 
        params = {'chosen_network_id': network_id}
    )

    # TODO: fix tensorflow compatibility issue
    G = util.parse_network(eval(response.text))

    for ext in ["index", "data-00000-of-00001", "meta"]:
        ckpt_response = requests.get(
            url = BASE_URL + 'ckpt', 
            params = {'model_name': model_name, 'extension': ext}
        )
        if ckpt_response.status_code == 200:
            with open(f"{model_name}.ckpt.{ext}", "wb") as f:
                f.write(ckpt_response.content)
        else:
            pass 

    # sols = util.finder_sol(G)
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
