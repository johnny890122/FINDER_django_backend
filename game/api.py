# from .build_for_test._builtin import Page
from django.http import JsonResponse
from rest_framework import status
import networkx as nx
# from db import Database
from django.views.decorators.csrf import csrf_exempt
from typing import Type
import game.util as util, json
import os

from typing import Type, List, Dict
from io import BytesIO
import pyximport

# pyximport.install()
from game.FINDER import FINDER
dqn = FINDER()

def finder_ranking(G: Type[nx.Graph], graph: str) -> Dict[str, int]:
    G_content = BytesIO(util.gml_format(G).encode('utf-8'))
    model_file = f'./models/Model_EMPIRICAL/{graph}.ckpt'
    # with FINDER() as dqn:
    _, sol = dqn.Evaluate(G_content, model_file)
    
    ranking = {}
    for i, node in enumerate(sol):
        ranking[str(node)] = i+1
    for node in G.nodes():
        if node not in ranking.keys():
            ranking[str(node)] = len(sol)+1

    return ranking

@csrf_exempt
def network_config(self):
    network_config = util.get_network_config()
    return JsonResponse(network_config, status=status.HTTP_200_OK)

@csrf_exempt
def game_start(self):
    code = self.GET.get('chosen_network_id')
    player_id = self.GET.get('player_id')
    game_id = self.GET.get('session_id') # TODO : session -> game

    # DB = Database()
    # DB.insert(mapping={"id": player_id}, relation="player")
    # DB.insert(mapping={"id": game_id, "player": player_id, "network_code": code}, relation="game")

    network_config = util.get_network_config(code)
    network_name = network_config["name"]
    print(os.getcwd())
    G = util.read_sample(f"data/empirical/{network_name}.gml")

    network_detail = {
        "nodes": util.G_nodes(G), "links": util.G_links(G), 
    }

    return JsonResponse(network_detail, status=status.HTTP_200_OK)       

@csrf_exempt
def get_tools(self) -> Type[JsonResponse]:
    try:
        tool_id = self.GET.get('chosen_tool_id')
    except:
        tool_id = None

    return JsonResponse(
        util.get_tool_config(tool_id), 
        status=status.HTTP_200_OK
    )

@csrf_exempt
def node_ranking(self) -> Type[JsonResponse]:
    data = json.loads(self.body)
    tool_id = data.get('chosen_tool_id')
    round_id = data.get('roundId') 
    game_id = data.get('gameId') 
    round_number = data.get('round')
    network_id = data.get('chosen_network_id')
    # DB = Database()
    # DB.insert(mapping={
    #     "id": round_id, "game": game_id, 
    #     "tool_id": tool_id, "round_number": round_number, 
    # }, relation="round")

    gData = data.get('graphData')
    G = util.parse_network(gData)
    graph_name = util.get_network_config(network_id)["name"]
    tool = util.get_tool_config(tool_id)['name']

    if tool == "NO_HELP":
        ranking = {}
    elif tool == "FINDER":
        ranking = finder_ranking(G, graph=graph_name)
    else:
        ranking = util.hxa_ranking(G, criteria=tool)

    return JsonResponse(ranking, status=status.HTTP_200_OK)

@csrf_exempt
def payoff(self) -> Type[JsonResponse]:
    data = json.loads(self.body)
    gData = data.get('graphData')
    netword_id = str(data.get('chosen_network_id'))
    round_id = str(data.get('roundId'))
    sol = str(data.get('chosen_node_id'))
    G = util.parse_network(gData)
    
    human_payoff = util.getRobustness(gData, netword_id, sol)
    finder_payoff = float() # TODO: implement finder payoff computation
    isEnd = util.gameEnd(gData, sol)
    
    # DB = Database()
    # TODO: insert FINDER payoff
    # DB.update({"chosen_node": sol, "payoff": human_payoff}, relation="round", pk=round_id)

    return JsonResponse({
        "human_payoff": human_payoff, 
        "finder_payoff": finder_payoff, 
        "isEnd": isEnd
    }, status=status.HTTP_200_OK)