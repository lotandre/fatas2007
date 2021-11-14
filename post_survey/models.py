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
import numpy
from django.utils.translation import ugettext_lazy as _


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'post_survey'
    players_per_group = None
    num_rounds = 1

    list_risk_choice = ['win', 'loss']


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            list_risk_seq = Constants.list_risk_choice.copy()
            p.participant.vars['risk_outcome'] = numpy.random.choice(list_risk_seq, p=[0.33, 0.67])
            p.risk_outcome = p.participant.vars['risk_outcome']


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    birth_year = models.IntegerField(
        label=_('In which year are you born?'),
        blank=True
    )
    gender = models.StringField(
        choices=[('male', _('male')), ('female', _('female')), ('other', _('something else')),
                 ('no_answer', _('no answer'))],
        widget=widgets.RadioSelect,
        label=_('What is your gender?'),
        blank=True
    )
    education = models.StringField(
        label=_('Did you complete a study? If you have completed several studies, which one is the highest?'),
        widget=widgets.RadioSelect,
        choices=[('vocational', _('Apprenticeship (Dual system) qualification (Full-time Vocational Schools, '
                                  'On the Job Training)')),
                 ('bachelor', _('Bachelor, Qualification from trade and technical schools')),
                 ('master', _('Master, Diploma (Teachers\' Examination, Magister)')),
                 ('doctor', _('PhD, Doctor\'s degree')),
                 ('no_qualification', _('No vocational qualification attained')),
                 ('no_answer', _('no answer'))],
        blank=True
    )
    finance_ability = models.StringField(
        label=_('Did you take part in lectures, courses, '
                'or further training about finance or the handling of money during your school or vocational training?'),
        widget=widgets.RadioSelect,
        choices=[('yes', _('Yes, participated')),
                 ('no', _('No, did not participate')),
                 ('no_answer', _('No answer'))]
    )
    income = models.StringField(
        label=_('What do you estimate is your household\'s MONTHLY net disposable income, that is, '
                'the money that is available to the entire household after deducting taxes '
                'and social security contributions to cover expenses?'),
        widget=widgets.RadioSelect,
        choices=[
            ('below400', _('Less than EUR 400')), ('below800', _('EUR 400 until EUR 800')),
            ('below1200', _('EUR 800 until EUR 1200')), ('below1600', _('EUR 1200 until EUR 1600')),
            ('below2000', _('EUR 1600 until EUR 2000')), ('below2400', _('EUR 2000 until EUR 2400')),
            ('below2800', _('EUR 2400 until EUR 2800')), ('below3200', _('EUR 2800 until EUR 3200')),
            ('below3600', _('EUR 3200 until EUR 3600')), ('below4000', _('EUR 3600 until EUR 4000')),
            ('over4000', _('More than EUR 4000')), ('no_answer', _('No answer'))],
        blank=True
    )

    risk_choice = models.IntegerField()
    check_risk_choice = models.IntegerField(blank=True)
    risk_outcome = models.StringField(blank=True)

    time_choice = models.StringField(blank=True)
    total_time = models.IntegerField(blank=True)
