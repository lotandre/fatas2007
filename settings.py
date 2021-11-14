from os import environ


SESSION_CONFIGS = [
    {
        'name': 'Fatas2007',
        'display_name': 'Fatas2007',
        'num_demo_participants': 20,
        'app_sequence': ['instructions', 'trial_annuity', 'trial_combined', 'trial_lump', 'quiz',
                         'annuity', 'combined', 'lump', 'post_survey', 'result'],
        'language': 'de',
    },
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'
LANGUAGE_SESSION_KEY = '_language'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='game', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '9cigdshykc8l*kqfa1j*uv^h#91nu(%upxe8_f$6bepw*joeol'

INSTALLED_APPS = ['otree']
MIDDLEWARE_CLASSES = ['django.middleware.locale.LocaleMiddleware', ]
