from otree.api import Currency as c, currency_range
from .models import Constants
from ._builtin import Page as oTreePage, WaitPage
import datetime
from .generic_pages import Page
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from itertools import chain
from .generic_pages import Page
import time


def get_timeout_seconds(player):
    return player.participant.vars['expiry'] - time.time()


class Result(Page):
    form_model = 'player'
    form_fields = ['finished', 'total_payoff', 'total_time']
    get_timeout_seconds = get_timeout_seconds

    def is_displayed(self):
        if self.participant.vars['time_instruction'] >= 10 and self.participant.vars['end'] == 0 and \
                self.participant.vars['consent'] == 'yes' and get_timeout_seconds(self.player) > 3:
            return self.participant.vars['time_choice'] != 'delay0'
        else:
            return False

    def vars_for_template(self):
        reward_life = self.participant.vars['reward_life']
        reward_str = 'total_payoff' + str(self.participant.vars['reward_life'])
        reward = self.participant.vars[reward_str]

        reward_euro = round(reward/23, 2)
        risk_choice = self.participant.vars['risk_choice']
        invest_num = reward_euro * self.participant.vars['risk_choice']

        if self.participant.vars['risk_outcome'] == 'win':
            earn_invest_num = 3.5 * risk_choice * reward_euro
            if self.participant.vars['lang_chosen'] == 'en':
                risk_outcome = 'win'
            else:
                risk_outcome = 'Gewinn'
        else:
            earn_invest_num = 0
            if self.participant.vars['lang_chosen'] == 'en':
                risk_outcome = 'loss'
            else:
                risk_outcome = 'Verlust'

        earn_safe_num = (100 - risk_choice) * reward_euro
        invest = round(invest_num/100, 2)
        earn_invest = round(earn_invest_num/100, 2)
        earn_safe = round(earn_safe_num/100, 2)
        total_num = earn_invest + earn_safe
        total = round(total_num, 2)

        if self.participant.vars['time_choice'] == 'delay1':
            pay_time = _('in 1 month')
            bonus_time_num = total * 0.05
            total1_num = total + bonus_time_num
        elif self.participant.vars['time_choice'] == 'delay2':
            pay_time = _('in 2 months')
            bonus_time_num = total * 0.103
            total1_num = total + bonus_time_num
        else:
            pay_time = _('in 3 months')
            bonus_time_num = total * 0.158
            total1_num = total + bonus_time_num

        bonus_time = round(bonus_time_num, 2)
        total1 = round(total1_num, 2)

        return {
            'reward_life': reward_life,
            'reward_euro': reward_euro,
            'risk_outcome': risk_outcome,
            'risk_choice': risk_choice,
            'invest': invest,
            'earn_invest': earn_invest,
            'total': total,
            'pay_time': pay_time,
            'bonus_time': bonus_time,
            'total1': total1
        }

    def before_next_page(self):
        self.participant.vars['finished'] = '1'
        end_datetime = datetime.datetime.now()
        start_time = self.participant.vars['start_time']
        self.player.total_time = round((end_datetime - start_time).total_seconds())

    def js_vars(self):
        username_value = self.participant.label
        return dict(url='https://survey.maximiles.com/complete?p=73955_afc22f02&m='+username_value)


class Result_nodelay(Page):
    form_model = 'player'
    form_fields = ['finished', 'total_payoff', 'total_time']
    get_timeout_seconds = get_timeout_seconds

    def is_displayed(self):
        if self.participant.vars['time_instruction'] >= 10 and self.participant.vars['end'] == 0 and \
                self.participant.vars['consent'] == 'yes' and get_timeout_seconds(self.player) > 3:
            return self.participant.vars['time_choice'] == 'delay0'
        else:
            return False

    def vars_for_template(self):
        reward_life = self.participant.vars['reward_life']
        reward_str = 'total_payoff' + str(self.participant.vars['reward_life'])
        reward = self.participant.vars[reward_str]

        reward_euro = round(reward/23, 2)
        risk_choice = self.participant.vars['risk_choice']
        invest_num = reward_euro * self.participant.vars['risk_choice']

        if self.participant.vars['risk_outcome'] == 'win':
            earn_invest_num = 3.5 * risk_choice * reward_euro
            if self.participant.vars['lang_chosen'] == 'en':
                risk_outcome = 'win'
            else:
                risk_outcome = 'Gewinn'
        else:
            earn_invest_num = 0
            if self.participant.vars['lang_chosen'] == 'en':
                risk_outcome = 'loss'
            else:
                risk_outcome = 'Verlust'

        earn_safe_num = (100 - risk_choice) * reward_euro
        invest = round(invest_num/100, 2)
        earn_invest = round(earn_invest_num/100, 2)
        earn_safe = round(earn_safe_num/100, 2)
        total_num = earn_invest + earn_safe
        total = round(total_num, 2)

        return {
            'reward_life': reward_life,
            'reward_euro': reward_euro,
            'risk_outcome': risk_outcome,
            'risk_choice': risk_choice,
            'invest': invest,
            'earn_invest': earn_invest,
            'total': total
        }

    def before_next_page(self):
        self.participant.vars['finished'] = '1'
        end_datetime = datetime.datetime.now()
        start_time = self.participant.vars['start_time']
        self.player.total_time = round((end_datetime - start_time).total_seconds())

    def js_vars(self):
        username_value = self.participant.label
        return dict(url='https://survey.maximiles.com/complete?p=73955_afc22f02&m='+username_value)


class Timeout(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 10 and self.participant.vars['end'] == 0 and \
               self.participant.vars['finished'] == '' and self.participant.vars['consent'] == 'yes'

    def js_vars(self):
        username_value = self.participant.label
        return dict(url='https://survey.maximiles.com/quality?p=73955&m='+username_value)


page_sequence = [Result, Result_nodelay, Timeout]
