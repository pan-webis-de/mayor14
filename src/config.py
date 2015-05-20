#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Configuration for pan
# ----------------------------------------------------------------------

import re

codes={
    'en': {
        'essays': re.compile('^[^\w]*EE'),
        'novels': re.compile('^[^\w]*EN'),
        'all': re.compile('^[^\w]*E'),
        'stopwords': 'english',
        'impostors': 'EN'
        },
    'nl': {
        'essays': re.compile('^[^\w]*DE'),
        'reviews': re.compile('^[^\w]*DR'),
        'all': re.compile('^[^\w]*D'),
        'stopwords': 'dutch',
        'impostors': 'DU'
        },
    'gr': {
        'news': re.compile('^[^\w]*GR'),
        'all': re.compile('^[^\w]*GR'),
        'stopwords': 'greek',
        'impostors': 'GR'
        },
    'es': {
        'news': re.compile('^[^\w]*SP'),
        'all': re.compile('^[^\w]*SP'),
        'stopwords': 'spanish',
        'impostors': 'SP'
        }
    }

