from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants, Player
from otree.api import *
from django.http import JsonResponse
from rest_framework import status

class Index(Page):
    form_model = 'player'
    form_fields = ['age']

    def __init__(self):
        self.template = {
            "test": "Hello World!"
        }

    def vars_for_template(self, player=None):
        print(self.player.session.code)
        return self.template

    def vars_for_react(self):
        # TODO: FIX the template bug
        template = {
            "test": "Hello World!"
        }
        return JsonResponse(template, status=status.HTTP_200_OK)

class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']


page_sequence = [Index, Demographics]

# https://github.com/oTree-org/otree-docs
# https://github.com/oTree-org/otree-core