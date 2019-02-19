from otree.api import Currency as c, currency_range, Bot, SubmissionMustFail
from . import pages
from .models import Constants
import random
from itertools import cycle


class PlayerBot(Bot):

    def play_round(self):
        # todo: test different city sizes and cases for homo, hetero
        cities_ids = ['01', '02']
        participants = list(range(len(self.subsession.get_players())))
        city = cycle(cities_ids)
        cities = []
        for i in participants:
            cities.append(next(city) + str(i))
        cities = set(cities)
        current_ids = set([p.city_id for p in self.subsession.get_players()])
        old_id = random.choice(list(current_ids))
        yield SubmissionMustFail(pages.IdCollecting, {'city_id': old_id})
        current_ids = set([p.city_id for p in self.subsession.get_players()])
        id = random.choice(list(cities - current_ids))
        yield (pages.IdCollecting, {'city_id': id})
