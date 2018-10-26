from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from sorter.pages import SorterWP


class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    SorterWP,
    MyPage,
    ResultsWaitPage,
    Results
]
