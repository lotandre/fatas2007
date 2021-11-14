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
from django.utils.translation import ugettext_lazy as _


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'quiz'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():
            player.participant.vars['mis_q1'] = 0
            player.participant.vars['mis_q2'] = 0
            player.participant.vars['mis_q3'] = 0
            player.participant.vars['mis_q4'] = 0
            player.participant.vars['mis_q5'] = 0
            player.participant.vars['end'] = 0


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    quiz1 = models.StringField(
        label=_('1.	What decision do you make on each round?'),
        widget=widgets.RadioSelect
    )

    quiz2 = models.StringField(
        label=_('2.	What happens when a green card is drawn at the end of a period?'),
        widget=widgets.RadioSelect
    )

    quiz3 = models.StringField(
        label=_('3.	What happens when a red card is drawn at the end of a period?'),
        widget=widgets.RadioSelect
    )

    quiz4 = models.StringField(
        label=_('4. How is my additional compensation determined?'),
        widget=widgets.RadioSelect
    )

    quiz5 = models.StringField(
        label=_('5.	If you decide for a Payoff in Period 10, and draw the red card after Period 5, '
                'how much will you get paid?'),
        widget=widgets.RadioSelect
    )
