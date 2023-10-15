from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants


class index(Page):
    form_model = 'player'
    form_fields = ['crt_bat', 'crt_widget', 'crt_lake']

class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']


class CognitiveReflectionTest(Page):
    form_model = 'player'
    form_fields = ['crt_bat', 'crt_widget', 'crt_lake']


page_sequence = [index, Demographics, CognitiveReflectionTest]
