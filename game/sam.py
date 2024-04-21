import json, os, requests
from io import BytesIO
from FINDER import FINDER
import networkx as nx
import requests
import game.util as util
from typing import Type

BASE_URL = "https://finder-django-backend-6331eb96b282.herokuapp.com/"

# TODO: fix tensorflow compatibility issue
def lambda_handler(event, context): 
    
    # 1. prepare the graph data
    body = json.loads(event["body"])
    # body = event["body"]
    network_id = body["network_id"]
    response = requests.get(
        url = BASE_URL + 'graphs/', 
        params = {'chosen_network_id': network_id}
    )
    dct = eval(response.text)
    model_name = dct["name"]
    
    # 2. prepare the ckpt data
    for ext in ["index", "data-00000-of-00001", "meta"]:
        ckpt_response = requests.get(
            url = BASE_URL + 'ckpt', 
            params = {'model_name': model_name, 'extension': ext}
        )
        if ckpt_response.status_code == 200:
            with open(f"/tmp/{model_name}.ckpt.{ext}", "wb") as f:
                f.write(ckpt_response.content)
        else:
            pass 
    
    # 3. do the prediction
    G = util.parse_network(dct)
    content = BytesIO(util.gml_format(G).encode('utf-8'))
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
