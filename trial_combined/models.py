from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'trial_comb'
    players_per_group = None
    num_rounds = 15

    red_seq = range(2, 16)


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.in_round(1).get_players():
            red_period = random.choice(Constants.red_seq)
            p.red_period = red_period
            p.participant.vars['red_period'] = red_period


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    red_period = models.IntegerField(blank=True)
    start_pay = models.IntegerField(blank=True)
    check_start_pay = models.IntegerField(blank=True)
    fix_payoff = models.IntegerField(blank=True)
    bonus_payoff = models.IntegerField(blank=True)
    total_payoff = models.IntegerField(blank=True)
