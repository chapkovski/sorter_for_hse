from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from string import digits


class IdCollecting(Page):
    form_model = 'player'
    form_fields = ['city_id']

    def city_id_error_message(self, value):
        ONLY_DIGITS_MSG = 'You should insert only numbers'
        UNCORRECT_ID_MSG = 'Please check that you inserted correct id!'
        NON_UNIQUE_MSG = 'You are using someone else ID!'
        l = list(value)
        config_keys = ['homo', 'hetero', ]
        homo, hetero, = (self.session.config.get(i) for i in config_keys)
        previous_ids = [p.city_id for p in self.subsession.get_players()]
        if len(l) < 3:
            return UNCORRECT_ID_MSG
        city_code = value[:2]

        if value in previous_ids:
            return NON_UNIQUE_MSG
        if any(i not in digits for i in l):
            return ONLY_DIGITS_MSG
        if any([homo, hetero]):
            if city_code not in self.session.vars['cities_list']:
                return UNCORRECT_ID_MSG
        else:
            if city_code not in Constants.cities.keys():
                return UNCORRECT_ID_MSG

    def before_next_page(self):
        self.participant.vars['city_code'] = self.player.city_id[:2]
        self.participant.vars['city_name'] = Constants.cities[self.participant.vars['city_code']]


from itertools import groupby


class SorterWP(WaitPage):
    group_by_arrival_time = True

    def is_displayed(self):
        self.participant.vars['arrived_to_sorting'] = True
        return True

    def get_players_for_group(self, waiting_players):
        # todo: make group size flexible
        group_size = 2
        num_parts = self.session.num_participants
        num_arrived = len([p for p in self.session.get_participants() if p.vars.get('arrived_to_sorting')])
        config_keys = ['homo', 'hetero', 'city_1', 'city_2']
        homo, hetero, city_1_code, city_2_code = (self.session.config.get(i) for i in config_keys)
        # if there are less than two cities participating, no sense to deal with homo or hetero
        if len(self.session.vars['cities_list']) < 2:
            homo = hetero = False
        parts = sorted(waiting_players, key=lambda x: x.participant.vars['city_code'])
        grouper = groupby(parts, key=lambda x: x.participant.vars['city_code'])

        if homo:
            for g, gl in grouper:
                # if the size of any group is large enough, we pass their players further
                if len(list(gl)) >= group_size:
                    players = [p for p in waiting_players if p.participant.vars.get('city_code') == g][:group_size]
                    return players

        if hetero:
            # if number of groups is large enough so we can pick enough unique players from them we pass them forward
            if len(list(grouper)) >= group_size:
                a_player = [p for p in waiting_players if p.participant.vars.get('city_code') == city_1_code][0]
                b_player = [p for p in waiting_players if p.participant.vars.get('city_code') == city_2_code][0]
                players = [a_player, b_player]
                return players
        if len(waiting_players) >= group_size:

            # if it is not neither homo nor hetero then we don't care about matching
            # if number of cities participating is less than 2, then we don't care about matching either
            if (len(self.session.vars['cities_list']) < group_size
                or num_parts - num_arrived <= 0
                or not any([homo, hetero])):
                return waiting_players[:group_size]


page_sequence = [
    IdCollecting,
]
