import os
"""
setting defaults
"""
TABLE_JOBS = os.environ.get('table-scheduled-jobs', 't-jobs')
TABLE_TOPICS = os.environ.get('table-topic', 't-topics')
TABLE_SUBSCRIBERS = os.environ.get('table-subscribers', 't-subscribers')
