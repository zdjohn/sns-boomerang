import os
from enum import Enum
"""
setting defaults, and constants
"""
TABLE_JOBS = os.environ.get('table-scheduled-jobs', 't-jobs')
TABLE_TOPICS = os.environ.get('table-topic-resource', 't-topics')
TABLE_SUBSCRIBERS = os.environ.get('table-subscribers', 't-subscribers')


class SubscriptionType(Enum):
    """subscription type that is supported"""
    API = 'api'
    LAMBDA = 'lambda'

