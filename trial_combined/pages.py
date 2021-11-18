from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from .generic_pages import Page
from django.utils.translation import ugettext_lazy as _


class Start(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 10 and self.player.round_number == 1 and \
               self.participant.vars['consent'] == 'yes'


class Decision(Page):
    form_model = 'player'
    form_fields = ['start_pay', 'check_start_pay', 'fix_payoff', 'bonus_payoff']

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 10 and self.player.round_number == 1 and \
               self.participant.vars['consent'] == 'yes'

    def error_message(self, values):
        if not values['check_start_pay']:
            return _('Please decide when you start your payoff.')

    def vars_for_template(self):
        round_num_bar = self.player.round_number + 9
        payoff_seq = [13, 14, 16, 19, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23]
        bonus_seq = [0, 0, 0, 0, 0, 25, 53, 85, 123, 170, 232, 318, 455, 716, 1477]
        payoff_list = []
        bonus_list = []
        for i in range(0, 15):
            payoff_list.append(payoff_seq[i])
            bonus_list.append(bonus_seq[i])
        return {
            'round_num_bar': round_num_bar,
            'payoff_list': payoff_list,
            'bonus_list': bonus_list
        }

    def before_next_page(self):
        self.participant.vars['start_pay'] = self.player.start_pay
        self.participant.vars['fix_payoff'] = self.player.fix_payoff
        self.participant.vars['bonus_payoff'] = self.player.bonus_payoff


class Draw(Page):
    form_model = 'player'
    form_fields = ['total_payoff']

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 10 and \
               self.player.round_number <= self.participant.vars['red_period'] and \
               self.participant.vars['consent'] == 'yes'

    def vars_for_template(self):
        round_num = self.player.round_number
        round_num_bar = self.player.round_number + 9
        start_pay = self.participant.vars['start_pay']
        fix_payoff = self.participant.vars['fix_payoff']
        bonus_payoff = self.participant.vars['bonus_payoff']
        red_period = self.participant.vars['red_period']
        green_card = 14 - self.player.round_number
        chance = 0
        if self.player.round_number < self.participant.vars['red_period']:
            chance = round(1 / (15 - self.player.round_number) * 100, 1)
        elif self.player.round_number == self.participant.vars['red_period']:
            chance = 100

        return {
            'round_num': round_num,
            'round_num_bar': round_num_bar,
            'start_pay': start_pay,
            'fix_payoff': fix_payoff,
            'bonus_payoff': bonus_payoff,
            'red_period': red_period,
            'green_card': green_card,
            'chance': chance
        }

    def before_next_page(self):
        self.participant.vars['total_payoff'] = self.player.total_payoff


class Summary(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 10 and \
               self.player.round_number == self.participant.vars['red_period'] \
               and self.participant.vars['consent'] == 'yes'

    def vars_for_template(self):
        total_payoff = self.participant.vars['total_payoff']
        return {
            'total_payoff': total_payoff
        }


page_sequence = [Start, Decision, Draw, Summary]
