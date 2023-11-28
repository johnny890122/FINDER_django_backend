from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants, Player
from otree.api import *
from django.http import JsonResponse
from rest_framework import status
from django.conf import settings

# settings.configure(DEBUG=True)
from django.views.decorators.csrf import csrf_exempt
import json

class GameStart(Page):
    def network_config(self):
        with open('_static/global/network_config.json', "r") as json_file:
            network_config = json.load(json_file)
        return JsonResponse(network_config, status=status.HTTP_200_OK)
    
    # def vars_for_react(self):
    #     if self.GET.get('pk') == "abc":
    #         template = {
    #             "test": "abc"
    #         }
    #     else:
    #         template = {
    #             "test": 1111
    #         }

    #     return JsonResponse(template, status=status.HTTP_200_OK)       

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