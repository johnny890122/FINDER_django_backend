import json, os, requests, time
from io import BytesIO
from FINDER import FINDER
import networkx as nx
import requests
import game.util as util
from typing import Type

BASE_URL = "https://finder-django-backend-6331eb96b282.herokuapp.com/"
dqn = FINDER()

def lambda_handler(event, context): 
    # 1. prepare the graph data
    body = json.loads(event["body"])
    model_name = body["graph"]
    
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
    G = util.parse_network({"nodes": body["nodes"], "links": body["links"]})
    content = BytesIO(util.gml_format(G).encode('utf-8'))

    model_file = f"/tmp/{model_name}.ckpt"
    _, sol = dqn.Evaluate(content, model_file)

    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "sols": sol,
            }
        )
    }
