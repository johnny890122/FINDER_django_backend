import json, os, requests, time
from io import BytesIO
from FINDER import FINDER
import networkx as nx
import requests
import game.util as util
from typing import Type
from pathlib import Path
import threading

CKPT_URL = "https://wql0ljgy3c.execute-api.us-east-1.amazonaws.com/deploy/folder/item"
HEROKU_URL = "https://finder-django-backend-6331eb96b282.herokuapp.com/"
dqn = FINDER()

def download_ckpt(model_name: str, ext: str):
    # ckpt_path = f"{model_name}.ckpt.{ext}"
    # ckpt_response = requests.get(
    #     url = CKPT_URL + f"?folder=finder-ckpt&item={ckpt_path}", 
    # )

    ckpt_response = requests.get(
        url = HEROKU_URL + 'ckpt', 
        params = {'model_name': model_name, 'extension': ext}
    )

    if ckpt_response.status_code == 200:
        with open(f"/tmp/{model_name}.ckpt.{ext}", "wb") as f:
            f.write(ckpt_response.content)
    else:
        pass 

def lambda_handler(event, context): 
    # 1. prepare the graph data
    body = json.loads(event["body"])
    model_name = body["graph"]
    
    # 2. prepare the ckpt data
    # TODO: 1. do not need to download the ckpt file every time
    # TODO: 2. use threading to accelerate the process
    threads = []
    time0 = time.time()
    for ext in ["index", "data-00000-of-00001", "meta"]:
        thread = threading.Thread(target=download_ckpt, args=(model_name, ext))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    time1 = time.time()
    print(time1 - time0)
    
    # 3. do the prediction
    time0 = time.time()
    G = util.parse_network({"nodes": body["nodes"], "links": body["links"]})
    content = BytesIO(util.gml_format(G).encode('utf-8'))

    model_file = f"/tmp/{model_name}.ckpt"
    _, sol = dqn.Evaluate(content, model_file)
    time1 = time.time()
    print(time1 - time0)

    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "sols": sol,
            }
        )
    }
