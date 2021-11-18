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
    name_in_url = 'annu'
    players_per_group = None
    num_rounds = 45

    red_seq = range(1, 16)


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.in_round(1).get_players():
            red_period1 = random.choice(Constants.red_seq)
            p.red_period1 = red_period1
            p.participant.vars['red_period_annu1'] = red_period1

            red_period2 = random.choice(Constants.red_seq)
            p.red_period2 = red_period2
            p.participant.vars['red_period_annu2'] = red_period2

            red_period3 = random.choice(Constants.red_seq)
            p.red_period3 = red_period3
            p.participant.vars['red_period_annu3'] = red_period3


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    red_period1 = models.IntegerField(blank=True)
    start_pay1 = models.IntegerField(blank=True)
    check_start_pay1 = models.IntegerField(blank=True)
    fix_payoff1 = models.IntegerField(blank=True)
    total_payoff1 = models.IntegerField(blank=True)

    red_period2 = models.IntegerField(blank=True)
    start_pay2 = models.IntegerField(blank=True)
    check_start_pay2 = models.IntegerField(blank=True)
    fix_payoff2 = models.IntegerField(blank=True)
    total_payoff2 = models.IntegerField(blank=True)

    red_period3 = models.IntegerField(blank=True)
    start_pay3 = models.IntegerField(blank=True)
    check_start_pay3 = models.IntegerField(blank=True)
    fix_payoff3 = models.IntegerField(blank=True)
    total_payoff3 = models.IntegerField(blank=True)
