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
import utils

class GameStart(Page):
    def network_config(self):
        network_config = utils.get_network_config()
        return JsonResponse(network_config, status=status.HTTP_200_OK)
    
    @csrf_exempt
    def game_start(self):
        network_config = utils.get_network_config()
        code = self.GET.get('chosen_network_id'),
        # TODO: implement store session_id  to database
        try:
            session_id =  self.GET.get('session_id')
        except:
            session_id = None
        mapping_dict = {val["code"]: key for key, val in network_config.items()}
        network_name = mapping_dict[int(code)]
        G = utils.read_sample(f"network_data/empirical/{network_name}.gml")

        network_detail = {
            "nodes": utils.G_nodes(G), "links": utils.G_links(G), 
        }

        return JsonResponse(network_detail, status=status.HTTP_200_OK)       

class Seeker_dismantle(Page):
    def node_ranking(self) -> Type[JsonResponse]:
        gData, tool = self.GET.get('gData'), self.GET.get('tool')
        # TODO: implement store data  to database
        try:
            session_id =  self.GET.get('session_id')
            code = self.GET.get('chosen_network_id')
            round_number = self.GET.get('round_number')
        except:
            session_id = None
            code = None
            tool = None
            round_number = None

        assert tool in ["degree", "closeness", "betweenness", "page_rank", "finder"]
        
        G = utils.parse_network(gData)
        if tool in ["degree", "closeness", "betweenness", "page_rank"]:
            ranking = utils.hxa_ranking(G, criteria=tool)
        else:
            # TODO: implement finder
            ranking = {}
        return JsonResponse(ranking, status=status.HTTP_200_OK)
    
    def payoff(self) -> Type[JsonResponse]:
        gData, tool = self.GET.get('gData'), self.GET.get('tool')
        # TODO: implement payoff computation
        human_payoff = float()
        finder_payoff = [float() for _ in range(5)]

        # TODO: implement decide whether the game is end
        isEnd = bool()

        return JsonResponse({
            "human_payoff": human_payoff, 
            "finder_payoff": finder_payoff, 
            "isEnd": isEnd
        }, status=status.HTTP_200_OK)

# class session(Page):
#     @csrf_exempt
#     def create(self):
        
#         data = json.loads(self.body)
#         print(data, type(data))
#         template = {
#             "difficulty": data['difficulty'],
#             "sessionId": "id"
#         }
#         return JsonResponse(template, status=status.HTTP_200_OK)

# class Demographics(Page):
#     form_model = 'player'
#     form_fields = ['age', 'gender']


page_sequence = [GameStart]

# https://github.com/oTree-org/otree-docs
# https://github.com/oTree-org/otree-core