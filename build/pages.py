from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants, Player
from otree.api import *


class index(Page):
    form_model = 'player'
    form_fields = ['age']
    @staticmethod
    def vars_for_template():
        return {
            "test": "hello"
        }

class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']


page_sequence = [index]
