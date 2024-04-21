from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import numpy as np
import networkx as nx
import os, sys, json
from typing import Type, List, Dict
from . import models
import game.util as util

@csrf_exempt
def network_config(self):
    network_config = util.get_network_config()
    return JsonResponse(network_config, status=status.HTTP_200_OK)

@csrf_exempt
def network_detail(self) -> JsonResponse:
    network_id = self.GET.get('chosen_network_id')
    network_detail = util.network_detail(network_id)
    return JsonResponse(network_detail, status=status.HTTP_200_OK)

@csrf_exempt
def model_ckpt(request) -> HttpResponse:
    model_name = request.GET.get('model_name')
    extension = request.GET.get('extension')

    path = f'models/Model_EMPIRICAL/{model_name}.ckpt.{extension}' 

    if os.path.exists(path):
        response = HttpResponse(content_type='application/octet-stream', status=status.HTTP_200_OK)
        with open(path, 'rb') as f:
            response.write(f.read())
        response['Content-Disposition'] = f'attachment; filename="{model_name}.ckpt.{extension}"'
        return response
    else:
        return HttpResponse("File not found", status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
def game_start(self) -> JsonResponse:
    player_id = self.GET.get('player_id')
    game_id = self.GET.get('game_id')
    network_id = self.GET.get('chosen_network_id')

    try:
        models.Player(id=player_id).save()
        print(f"player {player_id} save success")
        models.Game(
            id=game_id, 
            player = models.Player.objects.get(id=player_id), 
            network=network_id
        ).save()
        print(f"game {game_id} save success")
    except Exception as e:
        print("game_start", e)

    network_detail = util.network_detail(network_id)
    return JsonResponse(network_detail, status=status.HTTP_200_OK)       

@csrf_exempt
def get_tools(self) -> JsonResponse:
    tool_id = self.GET.get('chosen_tool_id')

    return JsonResponse(
        util.get_tool_config(tool_id), 
        status=status.HTTP_200_OK
    )

@csrf_exempt
def node_ranking(self) -> JsonResponse:
    data = json.loads(self.body)
    tool_id = data.get('chosen_tool_id')
    game_id = data.get('game_id') 
    round_number = data.get('roundId') 
    network_id = data.get('chosen_network_id')

    try:
        models.Round(
            game=models.Game.objects.get(id=game_id),
            round_number=round_number, 
            tool=tool_id,
            chosen_node=None,
            payoff=None,
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
        ranking = util.finder_ranking(G, graph=graph_name)
    else:
        ranking = util.hxa_ranking(G, criteria=tool)
    
    return JsonResponse(ranking, status=status.HTTP_200_OK)

@csrf_exempt
def payoff(self) -> JsonResponse:
    data = json.loads(self.body)
    gData = data.get('graphData')
    network_id = data.get('chosen_network_id')
    round_number = str(data.get('round_id'))
    game_id = data.get('game_id')
    sol = str(data.get('chosen_node_id'))
    
    graph_name = util.get_network_config(network_id)["name"]
    round = models.Round.objects.filter(game=game_id, round_number=round_number)
    
    try:
        round.update(chosen_node=sol)
        print(f"chosen_node: round {round_number} of game {game_id} update success")
    except Exception as e:
        print("chosen_node", e)

    all_chosen_node = [
        round.chosen_node 
            for round in models.Round.objects.filter(game_id=game_id).order_by('round_number')
    ]
    human_payoff = util.getHumanPayoff(graph_name, all_chosen_node) # TODO : need to check the value 
    finder_payoff = util.getFinderPayoff(graph_name)
    instant_finder_payoff = util.getInstantFinderPayoff(graph_name, all_chosen_node)
    isEnd = util.gameEnd(graph_name, all_chosen_node)
    try:
        round.update(payoff=human_payoff, is_end=isEnd)
        print(f"payoff: round {round_number} of game {game_id} update success")
    except Exception as e:
        print("payoff", e)

    return JsonResponse({
        "human_payoff": human_payoff, 
        "finder_payoff": finder_payoff, 
        "instant_finder_payoff": instant_finder_payoff,
        "isEnd": isEnd
    }, status=status.HTTP_200_OK)