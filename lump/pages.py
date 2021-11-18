from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from .generic_pages import Page
from django.utils.translation import ugettext_lazy as _
import time, math


def get_timeout_seconds(player):
    return player.participant.vars['expiry'] - time.time()


class Start(Page):
    form_model = 'player'
    get_timeout_seconds = get_timeout_seconds

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 10 and self.player.round_number == 1 and \
               self.participant.vars['end'] == 0 and self.participant.vars['consent'] == 'yes' and \
               get_timeout_seconds(self.player) > 3


class Decision(Page):
    form_model = 'player'
    get_timeout_seconds = get_timeout_seconds

    def is_displayed(self):
        return self.participant.vars['time_instruction'] >= 10 and (self.player.round_number in [1, 16, 31]) and \
               self.participant.vars['consent'] == 'yes' and self.participant.vars['end'] == 0 and \
               get_timeout_seconds(self.player) > 3

    def get_form_fields(self):
        formfield_list = []
        if self.player.round_number == 1:
            formfield_list = ['start_pay1', 'check_start_pay1', 'fix_payoff1']
        elif self.player.round_number == 16:
            formfield_list = ['start_pay2', 'check_start_pay2', 'fix_payoff2']
        elif self.player.round_number == 31:
            formfield_list = ['start_pay3', 'check_start_pay3', 'fix_payoff3']
        return formfield_list

    def error_message(self, values):
        if (self.player.round_number == 1 and not values['check_start_pay1']) or \
                (self.player.round_number == 16 and not values['check_start_pay2']) or \
                (self.player.round_number == 31 and not values['check_start_pay3']):
            return _('Please decide when you start your payoff.')

    def vars_for_template(self):
        life_num = math.floor((self.player.round_number-1)/15) + 1
        round_num = self.player.round_number - 15*(life_num - 1)
        payoff_seq = [100, 107, 115, 125, 136, 150, 167, 188, 214, 250, 300, 375, 500, 750, 1500]
        payoff_list = []
        round_num_bar = 0
        for i in range(0, 15):
            payoff_list.append(payoff_seq[i])
        if self.player.round_number < 16:
            round_num_bar = self.player.round_number + 33
        elif self.player.round_number in range(16, 31):
            round_num_bar = self.player.round_number + 39
        elif self.player.round_number > 30:
            round_num_bar = self.player.round_number + 45
        return {
            'life_num': life_num,
            'round_num': round_num,
            'payoff_list': payoff_list,
            'round_num_bar': round_num_bar
        }

    def before_next_page(self):
        if self.player.round_number == 1:
            self.participant.vars['start_pay1'] = self.player.start_pay1
            self.participant.vars['fix_payoff1'] = self.player.fix_payoff1
        if self.player.round_number == 16:
            self.participant.vars['start_pay2'] = self.player.start_pay2
            self.participant.vars['fix_payoff2'] = self.player.fix_payoff2
        if self.player.round_number == 31:
            self.participant.vars['start_pay3'] = self.player.start_pay3
            self.participant.vars['fix_payoff3'] = self.player.fix_payoff3


class Draw(Page):
    form_model = 'player'
    get_timeout_seconds = get_timeout_seconds

    def get_form_fields(self):
        formfield_list = []
        if self.player.round_number < 16:
            formfield_list = ['total_payoff1']
        elif self.player.round_number in range(16, 31):
            formfield_list = ['total_payoff2']
        elif self.player.round_number > 30:
            formfield_list = ['total_payoff3']
        return formfield_list

    def is_displayed(self):
        advance = ''
        if self.player.round_number < 16 and self.player.round_number <= self.participant.vars['red_period_lump1']:
            advance = 'yes'
        elif self.player.round_number in range(16, 31) and \
                self.player.round_number <= self.participant.vars['red_period_lump2'] + 15:
            advance = 'yes'
        elif self.player.round_number > 30 and self.player.round_number <= self.participant.vars['red_period_lump3'] + 30:
            advance = 'yes'
        return self.participant.vars['time_instruction'] >= 10 and advance == 'yes' and \
               self.participant.vars['consent'] == 'yes' and self.participant.vars['end'] == 0 and \
               get_timeout_seconds(self.player) > 3

    def vars_for_template(self):
        life_num = math.floor((self.player.round_number-1)/15) + 1
        round_num = self.player.round_number - 15*(life_num - 1)
        start_pay = 0
        fix_payoff = 0
        red_period = 0
        round_num_bar = 0
        green_card = 0
        chance = 0

        if self.player.round_number < 16:
            start_pay = self.participant.vars['start_pay1']
            fix_payoff = self.participant.vars['fix_payoff1']
            red_period = self.participant.vars['red_period_lump1']
        elif self.player.round_number in range(16, 31):
            start_pay = self.participant.vars['start_pay2']
            fix_payoff = self.participant.vars['fix_payoff2']
            red_period = self.participant.vars['red_period_lump2']
        elif self.player.round_number > 30:
            start_pay = self.participant.vars['start_pay3']
            fix_payoff = self.participant.vars['fix_payoff3']
            red_period = self.participant.vars['red_period_lump3']

        if self.player.round_number < 16:
            round_num_bar = self.player.round_number + 33
            green_card = 15 - self.player.round_number - 1
            if self.player.round_number < self.participant.vars['red_period_lump1']:
                chance = round(1 / (15 - self.player.round_number) * 100, 1)
            elif self.player.round_number == self.participant.vars['red_period_lump1']:
                chance = 100

        elif self.player.round_number in range(16, 31):
            round_num_bar = self.player.round_number + 39
            green_card = 30 - self.player.round_number - 1
            if self.player.round_number < self.participant.vars['red_period_lump2'] + 15:
                chance = round(1 / (15 - (self.player.round_number - 15)) * 100, 1)
            elif self.player.round_number == self.participant.vars['red_period_lump2'] + 15:
                chance = 100

        elif self.player.round_number > 30:
            round_num_bar = self.player.round_number + 45
            green_card = 45 - self.player.round_number - 1
            if self.player.round_number < self.participant.vars['red_period_lump3'] + 30:
                chance = round(1 / (15 - (self.player.round_number - 30)) * 100, 1)
            elif self.player.round_number == self.participant.vars['red_period_lump3'] + 30:
                chance = 100

        return {
            'life_num': life_num,
            'round_num': round_num,
            'start_pay': start_pay,
            'fix_payoff': fix_payoff,
            'red_period': red_period,
            'round_num_bar': round_num_bar,
            'green_card': green_card,
            'chance': chance
        }

    def before_next_page(self):
        if self.player.round_number < 16:
            self.participant.vars['total_payoff1'] = self.player.total_payoff1
        elif self.player.round_number in range(16, 31):
            self.participant.vars['total_payoff2'] = self.player.total_payoff2
        elif self.player.round_number > 30:
            self.participant.vars['total_payoff3'] = self.player.total_payoff3


class Summary(Page):
    form_model = 'player'
    get_timeout_seconds = get_timeout_seconds

    def is_displayed(self):
        exit = ''
        if self.player.round_number < 16 and self.player.round_number == self.participant.vars['red_period_lump1']:
            exit = 'yes'
        elif self.player.round_number in range(16, 31) and \
                self.player.round_number == self.participant.vars['red_period_lump2'] + 15:
            exit = 'yes'
        elif self.player.round_number > 30 and self.player.round_number == self.participant.vars['red_period_lump3'] + 30:
            exit = 'yes'

        return self.participant.vars['time_instruction'] >= 10 and exit == 'yes' and \
               self.participant.vars['consent'] == 'yes' and self.participant.vars['end'] == 0 and \
               get_timeout_seconds(self.player) > 3

    def vars_for_template(self):
        life_num = math.floor((self.player.round_number-1)/15) + 1
        total_payoff = 0
        round_num_bar = 0
        if self.player.round_number < 16:
            total_payoff = self.participant.vars['total_payoff1']
            round_num_bar = 54
        elif self.player.round_number in range(16, 31):
            total_payoff = self.participant.vars['total_payoff2']
            round_num_bar = 74
        elif self.player.round_number > 30:
            total_payoff = self.participant.vars['total_payoff3']
            round_num_bar = 95
        return {
            'life_num': life_num,
            'total_payoff': total_payoff,
            'round_num_bar': round_num_bar
        }


page_sequence = [Start, Decision, Draw, Summary]
