# from .build_for_test._builtin import Page
from django.http import JsonResponse
from rest_framework import status
import networkx as nx
# from db import Database
from django.views.decorators.csrf import csrf_exempt
from typing import Type
import game.util as util
import os, sys, json
from typing import Type, List, Dict
from io import BytesIO
import numpy as np

def finder_sol(G: Type[nx.Graph], graph: str):
    mapping = {node: str(idx) for idx, node in enumerate(G.nodes())}
    reversed_mapping = {str(idx): node for idx, node in enumerate(G.nodes())}
    reorder_G = nx.relabel_nodes(G, mapping, copy=False)

    G_content = BytesIO(util.gml_format(reorder_G).encode('utf-8'))
    model_file = f'./models/Model_EMPIRICAL/{graph}.ckpt'

    _, sols = util.dqn.Evaluate(G_content, model_file)
    for idx, sol in enumerate(sols):
        sols[idx] = reversed_mapping[str(sol)]
    return sols

def finder_ranking(G: Type[nx.Graph], graph: str) -> Dict:
    sols = finder_sol(G, graph)
    ranking = {}
    for i, node in enumerate(sols):
        ranking[str(node)] = i+1
    for node in G.nodes():
        if node not in ranking.keys():
            ranking[str(node)] = len(sols)+1

    return ranking

def finderRobustness(gData: Dict, graph: str) -> List[float]:
    G = util.parse_network(gData) # TODO : payoff 的顯示問題
    sols = finder_sol(G, graph)
    payoff = []
    for sol in sols:
        payoff.append(util.getRobustness(gData, graph, sol))
    return np.cumsum(payoff).tolist()

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

    try:
        models.Round(
            game=models.Game.objects.get(id=game_id),
            round_number=round_number, 
            tool=tool_id,
        ).save()
        print(f"round {round_number} of game {game_id} save success")
    except Exception as e:
        print("node_ranking", e)

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
    network_id = data.get('chosen_network_id')
    round_id = str(data.get('roundId'))
    sol = str(data.get('chosen_node_id'))
    G = util.parse_network(gData)
    
    graph_name = util.get_network_config(network_id)["name"]
    round_robustness = util.getRobustness(gData, graph_name, sol)

    round = models.Round.objects.filter(
        game=game_id, round_number=round_number
    )
    try:
        round.update(robustness=round_robustness, chosen_node=sol)
        print(f"robustness: round {round_number} of game {game_id} update success")
    except Exception as e:
        print("robustness", e)

    all_robustness = [0] + [
        round.robustness 
            for round in models.Round.objects.filter(
                game_id=game_id
            ).order_by('round_number')
    ]
    # print(all_robustness)
    human_payoff = util.getPayoff(all_robustness) # TODO : need to check the value 

    finder_payoff = finderRobustness(gData, graph_name)
    isEnd = util.gameEnd(gData, sol)
    try:
        round.update(payoff=human_payoff, is_end=isEnd)
        print(f"payoff: round {round_number} of game {game_id} update success")
    except Exception as e:
        print("payoff", e)

    return JsonResponse({
        "human_payoff": human_payoff, 
        "finder_payoff": finder_payoff, 
        "isEnd": isEnd
    }, status=status.HTTP_200_OK)