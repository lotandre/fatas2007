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
from django.utils.translation import ugettext_lazy as _

author = 'Your name here'

doc = """
Your app description
"""


def seq_to_dict(s):
    r = {}
    l = len(s) - 1
    for i, j in enumerate(s):
        if i < l:
            r[j] = s[i + 1]
        else:
            r[j] = None
    return r


class Constants(BaseConstants):
    name_in_url = 'instructions'
    players_per_group = None
    num_rounds = 1

    treatment_list = ['annuity', 'combined', 'lump']
    round_seq = range(1, 4)


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            app_seq = self.session.config.get('app_sequence')
            treatment_seq = Constants.treatment_list.copy()
            treatment = random.choice(treatment_seq)
            reward_life = random.choice(Constants.round_seq)
            p.treatment = treatment
            p.participant.vars['treatment'] = treatment
            p.participant.vars['finished'] = ''
            p.reward_life = reward_life
            p.participant.vars['reward_life'] = reward_life

            app_instruction, app_trial1, app_trial2, app_trial3, app_quiz, \
                app_decision1, app_decision2, app_decision3, app_post, app_result = app_seq
            if p.treatment == 'annuity':
                new_app_seq = [app_instruction] + [app_trial1] + [app_quiz] + [app_decision1] + [app_post] \
                              + [app_result]
            elif p.treatment == 'combined':
                new_app_seq = [app_instruction] + [app_trial2] + [app_quiz] + [app_decision2] + [app_post] \
                              + [app_result]
            else:
                new_app_seq = [app_instruction] + [app_trial3] + [app_quiz] + [app_decision3] + [app_post] \
                              + [app_result]
            p.participant.vars['_updated_seq_apps'] = seq_to_dict(new_app_seq)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.StringField()
    reward_life = models.IntegerField()
    time_instruction = models.IntegerField()
    consent = models.StringField(blank=True)
    lang = models.StringField(
        label='Bitte wählen Sie Ihre Sprache. / Please, select your language.',
        choices=[('de', 'Deutsch'), ('en', 'English')],
        widget=widgets.RadioSelect,
        initial='de',
        blank=True
    )
    username = models.StringField(blank=True)
