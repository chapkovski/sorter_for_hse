from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv
from string import digits

author = 'Philipp Chapkovski, HSE, Moscow, chapkovski@gmail.com'

doc = """
A single-player, single-page app collecting ids for players from several cities.
"""

NO_CITY_REGISTERED_MSG = '{}: No such city in cities list'
BOTH_SORTING_OPTS_MSG = 'You cannot choose both hetero and homo sorting'
WRONG_CITY_CODE_MSG = 'This city code ({}) is wrong. Check it out!'


class Constants(BaseConstants):
    name_in_url = 'sorter'
    players_per_group = None
    num_rounds = 1

    with open('sorter/cities.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        cities = {row['code']: row['city'] for row in reader}
    for k in cities.keys():
        l = list(k)
        assert all(i in digits for i in l) and len(l) == 2, WRONG_CITY_CODE_MSG.format(k)


class Subsession(BaseSubsession):
    def creating_session(self):
        homo, hetero = self.session.config['homo'], self.session.config['hetero']
        assert not all([homo, hetero]), BOTH_SORTING_OPTS_MSG
        config_cities = [v for k, v in self.session.config.items() if
                         k.startswith('city_') and v.strip() not in (None, '')]
        for c in config_cities:
            assert c in Constants.cities, NO_CITY_REGISTERED_MSG.format(c)
        self.session.vars['cities_list'] = list(set(config_cities))


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    city_id = models.StringField(label='Insert your participant ID')
