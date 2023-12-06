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
from utils import read_sample, G_nodes, G_links, get_network_config

class GameStart(Page):
    def network_config(self):
        network_config = get_network_config()
        return JsonResponse(network_config, status=status.HTTP_200_OK)
    
    @csrf_exempt
    def game_start(self):
        network_config = get_network_config()
        code = self.GET.get('chosen_network_id')

        mapping_dict = {val["code"]: key for key, val in network_config.items()}
        network_name = mapping_dict[int(code)]
        G = read_sample(f"network_data/empirical/{network_name}.gml")

        network_detail = {
            "nodes": G_nodes(G), "links": G_links(G), 
        }

        return JsonResponse(network_detail, status=status.HTTP_200_OK)       

class Seeker_dismantle(Page):
    def node_ranking(self):
        network_config = get_network_config()
        gData = self.GET.get('gData')
        tool = self.GET.get('tool')

        if tool in ["degree", "closeness", "betweenness", "page_rank"]:
            centrality = node_centrality_criteria(G)
        # "degree_ranking": { n: v for n, v in zip(centrality["degree"]["node"], centrality["degree"]["value"])},
        # "closeness_ranking": { n: v for n, v in zip(centrality["closeness"]["node"], centrality["closeness"]["value"])},
        # "betweenness_ranking": { n: v for n, v in zip(centrality["betweenness"]["node"], centrality["betweenness"]["value"])},
        # "page_rank_ranking": { n: v for n, v in zip(centrality["page_rank"]["node"], centrality["page_rank"]["value"])},

        mapping_dict = {val["code"]: key for key, val in network_config.items()}
        network_name = mapping_dict[int(code)]
        G = read_sample(f"network_data/empirical/{network_name}.gml")

        node_ranking = {
            "nodes": G_nodes(G), "links": G_links(G), 
        }

        return JsonResponse(node_ranking, status=status.HTTP_200_OK)

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