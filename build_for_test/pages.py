from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants, Player
from otree.api import *
from django.http import JsonResponse
from rest_framework import status
from django.conf import settings
import networkx as nx

# settings.configure(DEBUG=True)
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
        # TODO: implement store session_id  to database
        code = self.GET.get('chosen_network_id')
        session_id =  self.GET.get('session_id')
        player_id = self.GET.get('player_id')

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
        print(data.keys())
        gData, tool_id = data.get('graphData'), data.get('chosen_tool_id')
        print("tool_id", tool_id)

        G = utils.parse_network(gData)

        # TODO: implement store tool to database
        session_id =  data.get('session_id')
        player_id = data.get('player_id')
        code = data.get('chosen_network_id')
        round_number = data.get('round_number')

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
        gData, tool = self.GET.get('gData'), self.GET.get('tool')
        netword_id = str(self.GET.get('netword_id'))
        sol = str(self.GET.get('sol'))
        G = utils.parse_network(gData)
        
        payoff_in_round = utils.getRobustness(gData, netword_id, sol)
        # TODO: implement accumulate payoff from round 1
        human_payoff = float()

        # TODO: implement finder payoff computation
        finder_payoff = [float() for _ in range(5)]

        isEnd = utils.gameEnd(gData, sol)

        return JsonResponse({
            "human_payoff": human_payoff, 
            "finder_payoff": finder_payoff, 
            "isEnd": isEnd
        }, status=status.HTTP_200_OK)

page_sequence = [GameStart]

# https://github.com/oTree-org/otree-docs
# https://github.com/oTree-org/otree-core