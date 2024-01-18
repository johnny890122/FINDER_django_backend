from ._builtin import Page
from otree.api import *
from django.http import JsonResponse
from rest_framework import status
import networkx as nx
from db import Database

from django.views.decorators.csrf import csrf_exempt
from typing import Type
import utils, json

class GameStart(Page):
    @csrf_exempt
    def network_config(self):
        network_config = utils.get_network_config()
        return JsonResponse(network_config, status=status.HTTP_200_OK)
    
    @csrf_exempt
    def game_start(self):
        code = self.GET.get('chosen_network_id')
        player_id = self.GET.get('player_id')
        game_id = self.GET.get('session_id') # TODO : session -> game

        DB = Database()
        DB.insert(mapping={"id": player_id}, relation="player")
        DB.insert(mapping={"id": game_id, "player": player_id, "network_code": code}, relation="game")

        network_config = utils.get_network_config(code)
        network_name = network_config["name"]
        G = utils.read_sample(f"network_data/empirical/{network_name}.gml")
        network_detail = {
            "nodes": utils.G_nodes(G), "links": utils.G_links(G), 
        }

        return JsonResponse(network_detail, status=status.HTTP_200_OK)       

class SeekerDismantle(Page):
    @csrf_exempt
    def get_tools(self) -> Type[JsonResponse]:
        try:
            tool_id = self.GET.get('chosen_tool_id')
        except:
            tool_id = None

        return JsonResponse(
            utils.get_tool_config(tool_id), 
            status=status.HTTP_200_OK
        )

    @csrf_exempt
    def node_ranking(self) -> Type[JsonResponse]:
        data = json.loads(self.body)
        tool_id = data.get('chosen_tool_id')
        round_id = data.get('roundId') 
        game_id = data.get('gameId')
        
        DB = Database()
        DB.insert(mapping={
            "id": round_id, "game": game_id, 
            "tool_id": tool_id, "round_number": round_id, 
        }, relation="round")

        gData = data.get('graphData')
        G = utils.parse_network(gData)
        tool = utils.get_tool_config(tool_id)['name']
        if tool == "NO_HELP":
            ranking = {}
        elif tool == "FINDER":
            # TODO: implement finder
            pass 
        else:
            ranking = utils.hxa_ranking(G, criteria=tool)

        return JsonResponse(ranking, status=status.HTTP_200_OK)
    
    @csrf_exempt
    def payoff(self) -> Type[JsonResponse]:
        data = json.loads(self.body)
        netword_id = data.get('chosen_network_id')
        round_id = data.get('round_id')
        sol = data.get('chosen_node_id')
        
        gData = data.get('graphData')
        G = utils.parse_network(gData)
        
        human_payoff = utils.getRobustness(gData, netword_id, sol)
        finder_payoff = float() # TODO: implement finder payoff computation
        isEnd = utils.gameEnd(gData, sol)
        
        DB = Database()
        # TODO: insert FINDER payoff and human payoff
        DB.update({"chosen_node": sol}, relation="round", pk=round_id)

        return JsonResponse({
            "human_payoff": human_payoff, 
            "finder_payoff": finder_payoff, 
            "isEnd": isEnd
        }, status=status.HTTP_200_OK)

page_sequence = [GameStart]